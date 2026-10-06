# Contributing

Recommend a resource or report a correction by [opening an issue](https://github.com/JamesCao2048/awesome-coding-agent-data-quality/issues/new). A primary URL and a sentence explaining its relevance are enough to start; include a source section or concrete correction when available. You do not need to edit JSON or run scripts to suggest an addition.

For a pull request, update `data/resources.json`, run `python3 scripts/catalog.py`, then `python3 scripts/catalog.py --check`. Include the generated README changes.

See the [curation guide](docs/curation.md) for category definitions, evidence levels and collection commands. Keep each public annotation to one or two sentences and link to the original paper, article or tool. Include source sections supporting the annotation in the pull request description.

A useful entry answers: **what is checked, how is it checked, and what remains unproven?**

Use one category (`construction`, `audits`, `meta-evaluation`, `batch-auditing`, or `protocol`) and any applicable facets (`environment`, `task`, `verifier`, `protocol`, `contamination`). Multiple facets do not require duplicate entries. `standalone_audit` describes the work's purpose; it does not claim every component of a dataset has been audited. Set `adjacent: true` for resources whose evidence is primarily from neighboring settings.

Add `applies_to` (`training-data`, `benchmark`, or both) according to the source-supported application. Do not label a benchmark-only audit as training-data validation merely because the method might transfer.

Use a familiar `display_name` for quick scanning, preserve the full paper title in `title`, and label additional links accurately with `artifact_label` (`Code`, `Data`, `Project`, `Rubric` or `Author article`).

For papers, set `venue_label` to an officially verified conference abbreviation and year, or `Preprint YEAR` when the venue has not been verified. Set `affiliation` to the first author's institution(s) in the inspected paper version. Blogs may use the stated author organization or publishing organization. Use contemporaneous author or institutional sources to clarify a missing paper affiliation; do not substitute a current employer for the institution associated with the work. Mark unresolved affiliations as `Affiliation unverified`. Include metadata sources with the proposed change.

Distinguish papers, blogs, benchmarks, datasets, and tools. Use the earliest public year, unless the entry specifically describes a later revision. Identify the source/version supporting a proposed change in the pull request; do not infer publication venues. Abstract-only entries are allowed for discovery but must be visibly labeled.

Please do not submit only a leaderboard score, an unsubstantiated defect allegation, copied abstracts, or private/unpublished materials. Full texts remain with their authors; this repository stores links and original short annotations.
