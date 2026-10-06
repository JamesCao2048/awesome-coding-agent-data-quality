#!/usr/bin/env python3
"""Validate the curated registry and render Markdown. No network or dependencies."""

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "construction": ("Data construction and validation", "How training tasks, execution environments and benchmark datasets are built and screened before use."),
    "audits": ("Quality audits and empirical studies", "Investigations of defects in existing datasets, tests and evaluation results."),
    "batch-auditing": ("Automated checking and repair", "Reusable methods and tools for finding, diagnosing and repairing quality problems at scale."),
    "meta-evaluation": ("Evaluating the auditors", "Benchmarks and methods for measuring whether a checker detects the right defect for the right reason."),
    "protocol": ("Evaluation protocols and contamination", "Resource limits, measurement noise, leakage and versioning that affect interpretation."),
}
FACETS = {"environment", "task", "verifier", "protocol", "contamination"}
USES = {"training-data": "Training data", "benchmark": "Benchmark"}
VERIFICATION = {"fulltext-reviewed", "primary-page-reviewed", "abstract-reviewed"}
REQUIRED = {"id", "title", "year", "type", "url", "category", "facets", "scope", "summary_en", "verification", "standalone_audit", "applies_to", "display_name", "venue_label", "affiliation"}


def validate(records):
    if not isinstance(records, list) or not records:
        raise ValueError("resources.json must be a nonempty array")
    ids, urls = set(), set()
    for r in records:
        missing = REQUIRED - r.keys()
        if missing:
            raise ValueError(f"{r.get('id', '?')}: missing {sorted(missing)}")
        name = r["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in ids:
            raise ValueError(f"invalid/duplicate ID: {name}")
        ids.add(name)
        if r["url"] in urls:
            raise ValueError(f"duplicate primary URL: {r['url']}")
        urls.add(r["url"])
        if r["category"] not in CATEGORIES or r["verification"] not in VERIFICATION:
            raise ValueError(f"{name}: invalid category/verification")
        if not isinstance(r["year"], int) or not 2000 <= r["year"] <= 2026:
            raise ValueError(f"{name}: invalid year for this snapshot")
        if not r["facets"] or not set(r["facets"]) <= FACETS:
            raise ValueError(f"{name}: invalid facets")
        if not isinstance(r["applies_to"], list) or not r["applies_to"] or not set(r["applies_to"]) <= USES.keys() or len(r["applies_to"]) != len(set(r["applies_to"])):
            raise ValueError(f"{name}: invalid applies_to tags")
        if not isinstance(r["standalone_audit"], bool):
            raise ValueError(f"{name}: standalone_audit must be boolean")
        unexpected = r.keys() - (REQUIRED | {"artifact_url", "artifact_label", "adjacent"})
        if unexpected:
            raise ValueError(f"{name}: unsupported catalog fields: {sorted(unexpected)}")
        if r.get("artifact_url") and not r.get("artifact_label"):
            raise ValueError(f"{name}: missing artifact_label")
        for url in [r["url"], *([r["artifact_url"]] if r.get("artifact_url") else [])]:
            parsed = urlparse(url)
            if parsed.scheme not in {"https", "http"} or not parsed.netloc:
                raise ValueError(f"{name}: invalid URL {url}")
        for field in ("title", "summary_en", "display_name", "venue_label", "affiliation"):
            if not isinstance(r[field], str) or not r[field].strip():
                raise ValueError(f"{name}: empty {field}")


def render(records):
    counts = Counter(r["category"] for r in records)
    readme = f"""# Awesome Coding Agent Data Quality

A curated collection of **papers, tools and technical resources for trustworthy coding-agent training data and benchmarks**.

A task can run successfully and still be a bad training or evaluation example: its instructions may omit a requirement, its tests may reject a valid solution, or an incorrect patch may receive full credit. This collection covers how those problems are prevented, discovered and repaired.

**{len(records)} resources · Updated October 7, 2026**

**Use tags:** `Training data` identifies work on training-task data or training environments; `Benchmark` identifies work on evaluation data or evaluation reliability. Both tags appear when a work addresses both. These tags describe the quality application studied, not merely whether a paper uses a benchmark to evaluate its model.

**Publication labels:** papers show the verified venue and first-author affiliation; **Preprint** means a manuscript is available but its conference venue was not verified. Blogs show the author organization or publisher; unavailable affiliations are marked explicitly.

**Quality dimensions:** work may check the environment, task, verifier, evaluation protocol or contamination. A verifier is the test or rule that decides whether a solution succeeds. See the [tag guide](docs/curation.md#quality-dimensions) for definitions.

The core is repository-level software-engineering tasks and agent training environments. Relevant terminal tasks are also included. Function-level tests, scientific workflows and broader agent methods are labeled **Adjacent** where their evidence does not directly establish repository-task quality.

## Contents

**Literature**

""".splitlines()
    for key, (title, _) in CATEGORIES.items():
        readme.append(f"- [{title}](#{key}) ({counts[key]})")
    readme += ["- [Quality auditing](#quality-auditing) — where to start", "", "**About this list**", "", "- [How to use this list](#how-to-use-this-list)", "- [Contributing](#contributing)", "- [Attribution](#attribution)", ""]
    for cat, (title, intro) in CATEGORIES.items():
        readme += [f'<a id="{cat}"></a>', "", f"## {title}", "", intro, ""]
        for r in sorted((x for x in records if x["category"] == cat), key=lambda x: (-x["year"], x["title"].casefold())):
            uses = " ".join(f"`{USES[x]}`" for x in r["applies_to"])
            prefix = "**Adjacent.** " if r.get("adjacent") else ""
            note = " **Abstract only.**" if r["verification"] == "abstract-reviewed" else ""
            artifact = f" [{r['artifact_label']}]({r['artifact_url']})." if r.get("artifact_url") else ""
            publication = r["venue_label"] if r["type"] == "paper" else f"{r['year']}; {r['type']}"
            readme += [f"- **[{r['display_name']}]({r['url']})** ({publication}; {r['affiliation']}) {uses} — {prefix}{r['summary_en']}{note}{artifact}", ""]
    readme += """## Quality auditing

For automated task review, start with [SPICE](https://arxiv.org/abs/2507.09108), which labels issue clarity and test adequacy, and [Auto Benchmark Audit (ABA)](https://arxiv.org/abs/2605.26079), which investigates defects using task materials or recorded runs. To assess whether an auditor finds the right defect, [Task Verification Bench (TVB)](https://posttrain.dev/task-verification-bench-paper.pdf) provides reference defects and scoring; its role is covered under [Evaluating the auditors](#meta-evaluation).

## How to use this list

- **Building a training dataset:** start with construction and validation, then compare independent checks such as SPICE and test-strengthening methods.
- **Interpreting a benchmark score:** check the exact version, then follow the sources under [quality audits](#audits) and [evaluation protocols](#protocol). Distinguish task defects from execution or reporting differences.
- **Choosing an auditing method:** compare the artifacts it needs, the evidence it produces and how its findings were validated. Label agreement, defect-detection accuracy and execution success are different measurements.

This is a curated collection, not an exhaustive systematic review. Inclusion does not certify a dataset or tool. Entries provide short annotations and original sources; an **Abstract only** label means the methods have not been reviewed in full text.

## Contributing

Suggest a resource or correction by [opening an issue](https://github.com/JamesCao2048/awesome-coding-agent-data-quality/issues/new), or send a pull request. Each entry should explain **what is checked, how it is checked and what the evidence does not establish**. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [curation guide](docs/curation.md).

The catalog is generated from [`data/resources.json`](data/resources.json). Run `python3 scripts/catalog.py` after editing records, then `python3 scripts/catalog.py --check` to check consistency.

## Attribution

Annotations are original. Linked papers, datasets and software retain their authors' licenses. List-structure references include [awesome-code-agents](https://github.com/EuniAI/awesome-code-agents), [awesome-coding-agent-eval](https://github.com/gudo7208/awesome-coding-agent-eval) and the [Awesome manifesto](https://github.com/sindresorhus/awesome/blob/main/awesome.md).
""".splitlines()
    readme.append("")
    return {ROOT / "README.md": "\n".join(readme)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated files are out of date")
    args = parser.parse_args()
    try:
        records = json.loads((ROOT / "data/resources.json").read_text())
        validate(records)
        for path, content in render(records).items():
            if args.check:
                if not path.exists() or path.read_text() != content:
                    raise ValueError(f"generated file is out of date: {path.relative_to(ROOT)}")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
        print(f"Validated {len(records)} records; generated files {'match' if args.check else 'written'}.")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(1, f"catalog: {exc}\n")


if __name__ == "__main__":
    main()
