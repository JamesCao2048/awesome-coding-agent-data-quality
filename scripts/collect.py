#!/usr/bin/env python3
"""Cache unreviewed literature candidates and source bytes; never edit the catalog."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import signal
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 15 * 1024 * 1024
TIMEOUT = 20
ATOM = {"a": "http://www.w3.org/2005/Atom"}
USER_AGENT = "awesome-coding-agent-data-quality/0.1 (public-source research collector)"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def cache_directory(kind: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    path = ROOT / ".cache" / kind / f"{stamp}-{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


@contextmanager
def deadline():
    """Bound the whole request on POSIX; socket operations also have a timeout."""
    enabled = hasattr(signal, "setitimer")
    if enabled:
        previous = signal.getsignal(signal.SIGALRM)

        def expired(_signum, _frame):
            raise TimeoutError(f"Request exceeded {TIMEOUT} seconds")

        signal.signal(signal.SIGALRM, expired)
        signal.setitimer(signal.ITIMER_REAL, TIMEOUT)
    try:
        yield
    finally:
        if enabled:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)


def validate_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise ValueError("Source URL must use http or https and include a host")
    if parts.username is not None or parts.password is not None:
        raise ValueError("URLs containing credentials are not accepted")
    return urllib.parse.urlunsplit(parts._replace(fragment=""))


class PublicRedirects(urllib.request.HTTPRedirectHandler):
    max_redirections = 5
    max_repeats = 2

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def retrieve(url: str, directory: Path) -> tuple[bytes, dict]:
    """Store response bytes, including HTTP error bodies, within a fixed size cap."""
    result = {
        "requested_url": url,
        "started_at": now(),
        "final_url": None,
        "http_status": None,
        "content_type": None,
        "tls_ca_source": "Python defaults / SSL_CERT_FILE / SSL_CERT_DIR",
        "timeout_seconds": TIMEOUT,
        "max_bytes": MAX_BYTES,
        "complete": False,
        "error": None,
    }
    payload = bytearray()
    started = time.monotonic()
    try:
        url = validate_url(url)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        context = ssl.create_default_context()
        # Some python.org macOS installs ship without a configured CA bundle.
        # Use the existing system bundle only if defaults contain no roots and
        # the caller has not explicitly selected a trust store. Keep verification.
        system_ca = Path("/etc/ssl/cert.pem")
        if (sys.platform == "darwin" and not context.get_ca_certs()
                and not os.environ.get("SSL_CERT_FILE") and not os.environ.get("SSL_CERT_DIR")
                and system_ca.is_file()):
            context.load_verify_locations(cafile=str(system_ca))
            result["tls_ca_source"] = str(system_ca)
        opener = urllib.request.build_opener(PublicRedirects(), urllib.request.HTTPSHandler(context=context))
        with deadline():
            try:
                response = opener.open(request, timeout=TIMEOUT)
            except urllib.error.HTTPError as error:
                response = error  # Preserve the server's error response as evidence.
                result["error"] = f"HTTP {error.code}: {error.reason}"
            with response:
                result.update(
                    final_url=response.geturl(),
                    http_status=response.status,
                    content_type=response.headers.get("Content-Type"),
                )
                while True:
                    if time.monotonic() - started >= TIMEOUT:
                        raise TimeoutError(f"Request exceeded {TIMEOUT} seconds")
                    chunk = response.read(min(64 * 1024, MAX_BYTES + 1 - len(payload)))
                    if not chunk:
                        result["complete"] = True
                        break
                    payload.extend(chunk)
                    if len(payload) > MAX_BYTES:
                        del payload[MAX_BYTES:]
                        raise ValueError(f"Response exceeds the {MAX_BYTES}-byte limit; cached bytes are truncated")
    except (OSError, ValueError, TimeoutError, urllib.error.URLError, http.client.HTTPException) as error:
        result["error"] = f"{type(error).__name__}: {error}"
    result.update(
        finished_at=now(),
        elapsed_seconds=round(time.monotonic() - started, 3),
        bytes_saved=len(payload),
        sha256=hashlib.sha256(payload).hexdigest(),
        body_file="response.bin",
    )
    (directory / "response.bin").write_bytes(payload)
    return bytes(payload), result


def text_at(element: ET.Element, path: str) -> str:
    return " ".join((element.findtext(path, default="", namespaces=ATOM) or "").split())


def arxiv_candidates(body: bytes) -> list[dict]:
    root = ET.fromstring(body)
    if root.tag != "{http://www.w3.org/2005/Atom}feed":
        raise ValueError("arXiv response is not an Atom feed")
    records = []
    for entry in root.findall("a:entry", ATOM):
        title, url = text_at(entry, "a:title"), text_at(entry, "a:id")
        if title.lower() == "error" or "/errors" in url:
            raise ValueError(f"arXiv API error: {text_at(entry, 'a:summary')[:300]}")
        if not title or not url:
            raise ValueError("arXiv entry is missing title or ID")
        records.append({
            "candidate_status": "unreviewed",
            "title": title,
            "url": url,
            "arxiv_id": url.rsplit("/", 1)[-1],
            "authors": [text_at(author, "a:name") for author in entry.findall("a:author", ATOM)],
            "published": text_at(entry, "a:published"),
            "updated": text_at(entry, "a:updated"),
            "abstract": text_at(entry, "a:summary"),
        })
    return records


def crossref_candidates(body: bytes) -> list[dict]:
    data = json.loads(body)
    if not isinstance(data, dict) or data.get("status") != "ok":
        raise ValueError("Crossref response has no successful API status")
    message = data.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("items"), list):
        raise ValueError("Crossref response is missing its items array")
    records = []
    for item in message["items"]:
        if not isinstance(item, dict):
            raise ValueError("Crossref item is not an object")
        titles = item.get("title")
        if not isinstance(titles, list) or not titles or not isinstance(titles[0], str):
            raise ValueError("Crossref item is missing a title")
        authors = item.get("author", [])
        if not isinstance(authors, list) or any(not isinstance(a, dict) for a in authors):
            raise ValueError("Crossref authors have an unexpected shape")
        records.append({
            "candidate_status": "unreviewed",
            "title": titles[0],
            "url": item.get("URL"),
            "doi": item.get("DOI"),
            "authors": [" ".join(str(a.get(k, "")) for k in ("given", "family")).strip() for a in authors],
            "publication_date": item.get("published", item.get("issued")),
            "venue": item.get("container-title", []),
            "type": item.get("type"),
            "abstract": item.get("abstract"),
        })
    return records


def search(args: argparse.Namespace) -> int:
    if args.provider == "arxiv":
        params = {"search_query": args.query, "start": 0, "max_results": args.limit}
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
        parser = arxiv_candidates
    else:
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query": args.query, "rows": args.limit})
        parser = crossref_candidates
    directory = cache_directory("search")
    body, log = retrieve(url, directory)
    log.update(operation="search", provider=args.provider, query=args.query, limit=args.limit,
               candidate_status="unreviewed", imported_into_catalog=False)
    records = []
    if log["error"] is None:
        try:
            records = parser(body)[:args.limit]
        except (ValueError, TypeError, KeyError, ET.ParseError) as error:
            log["error"] = f"API parse error ({type(error).__name__}): {error}"
    log["candidate_count"] = len(records) if log["error"] is None else None
    # None distinguishes an unsuccessful search from a successful empty result.
    write_json(directory / "candidates.json", {"status": "unreviewed", "candidates": records})
    write_json(directory / "log.json", log)
    print(json.dumps({"cache": str(directory), "candidates": log["candidate_count"], "error": log["error"]}))
    return 1 if log["error"] else 0


def fetch(args: argparse.Namespace) -> int:
    url = args.url
    if args.id:
        records = json.loads((ROOT / "data" / "resources.json").read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError("data/resources.json must contain an array")
        matches = [r for r in records if isinstance(r, dict) and r.get("id") == args.id]
        if len(matches) != 1:
            raise ValueError(f"Expected one resource with ID {args.id!r}; found {len(matches)}")
        url = matches[0].get("url")
        if not isinstance(url, str) or not url:
            raise ValueError(f"Resource {args.id!r} has no URL")
    directory = cache_directory("sources")
    _, log = retrieve(url, directory)
    log.update(operation="fetch", resource_id=args.id, review_status="not-reviewed-by-fetch",
               notice="HTTP retrieval is not evidence review or experimental reproduction")
    write_json(directory / "metadata.json", log)
    print(json.dumps({"cache": str(directory), "http_status": log["http_status"], "error": log["error"]}))
    return 1 if log["error"] else 0


def bounded_limit(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("limit must be an integer from 1 to 50") from None
    if not 1 <= number <= 50:
        raise argparse.ArgumentTypeError("limit must be between 1 and 50")
    return number


def nonempty_query(value: str) -> str:
    if not value.strip():
        raise argparse.ArgumentTypeError("query cannot be empty")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    discover = commands.add_parser("search", help="Cache unreviewed API candidates without importing them")
    discover.add_argument("--provider", choices=("arxiv", "crossref"), required=True)
    discover.add_argument("--query", type=nonempty_query, required=True)
    discover.add_argument("--limit", type=bounded_limit, default=5)
    discover.set_defaults(run=search)
    snapshot = commands.add_parser("fetch", help="Cache source bytes; this does not mark a resource reviewed")
    source = snapshot.add_mutually_exclusive_group(required=True)
    source.add_argument("--id", help="Resource ID in data/resources.json")
    source.add_argument("--url", help="Direct public primary-source URL")
    snapshot.set_defaults(run=fetch)
    args = parser.parse_args()
    try:
        return args.run(args)
    except (OSError, ValueError) as error:
        print(f"collect: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
