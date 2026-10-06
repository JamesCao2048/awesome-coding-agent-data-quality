# Curation and evidence

This collection includes resources that explain how to build, check, diagnose or repair coding-agent tasks, execution environments, or grading rules. Leaderboard performance alone is insufficient for inclusion.

## Organizing an entry

Choose one category by the work's main contribution:

| Category | Meaning |
| --- | --- |
| `construction` | Building training/evaluation data and checking it before release. |
| `audits` | Empirical studies of defects in existing data or evaluation results. |
| `batch-auditing` | Reusable checking, diagnosis or repair methods and infrastructure. |
| `meta-evaluation` | Evaluating the quality of an auditor or detector. |
| `protocol` | Measurement conditions, contamination, leakage and version interpretation. |

Add any applicable facets: `environment`, `task`, `verifier`, `protocol`, `contamination`. Multiple facets do not require duplicate entries. Mark `adjacent: true` when the empirical evidence concerns function-level tests, scientific workflows or other neighboring settings rather than the core repository-task setting.

Set `applies_to` to `training-data`, `benchmark`, or both. These tags describe the work's demonstrated or explicitly studied quality application. Training-task construction and screening receive `Training data`; evaluation-task construction, benchmark auditing and evaluation reliability receive `Benchmark`. Merely evaluating a training method on a benchmark does not justify both tags, and potential reuse of an audit tool on training data does not establish that use.

Each work appears once in the categorized list. **Quality auditing** provides a brief orientation after the categories. SPICE and ABA are automated methods; TVB primarily evaluates auditors and stays under `meta-evaluation`. Contribution and attribution sections are repository information, separated from literature in the contents.

Use a recognizable `display_name` (for example, `ScaleSWE`) in the list and preserve the complete publication title in `title`. When an `artifact_url` is provided, set an accurate `artifact_label`, such as `Code`, `Data`, `Project`, `Rubric` or `Author article`.

## Quality dimensions

Use tags appear in the README for quick scanning. The structured catalog also records which quality dimensions a work addresses:

| Facet | What it checks |
| --- | --- |
| `environment` | Whether the runtime, dependencies and resources support reliable execution. |
| `task` | Whether the requirement is clear, consistent and achievable with the available information. |
| `verifier` | Whether grading accepts valid solutions and rejects incorrect or incomplete ones. |
| `protocol` | Whether run settings, score parsing and benchmark versions support a valid comparison. |
| `contamination` | Whether evaluation information is unintentionally memorized or exposed in accessible task artifacts. |

`standalone_audit` is a separate property: an independent audit can introduce an automated method or an evaluation dataset, so it need not appear in the empirical-audits category.

## Evidence required

Each record in `data/resources.json` needs a primary URL and one or two original sentences explaining its quality relevance. Where a limitation changes how the work should be used, include it in the annotation. Support proposed additions with a source section or passage in the pull request. Use official papers, author repositories, technical blogs and maintainer discussions. Other lists and search snippets are discovery leads.

- **`abstract-reviewed`**: metadata and abstract inspected; detailed methods are not established.
- **`primary-page-reviewed`**: an official article, repository, dataset card or documentation was inspected.
- **`fulltext-reviewed`**: relevant full-text sections inspected; this does not claim every experiment or statement was independently checked.

No reading status implies experimental reproduction. Keep source-reported results separate from editorial interpretation. Preserve benchmark versions, sampling procedures, denominators and metric definitions. In particular, a selected difficult subset is not a random sample of a whole benchmark, and agreement with an annotation rubric is not proof of semantic correctness.

Identify duplicate works by DOI, arXiv ID and confirmed title aliases before adding records. Preserve the version actually inspected; use the first public year unless the entry concerns a later revision. Do not infer a publication venue from a filename or a workshop submission.

## Collection helpers

Python 3.10+ is sufficient; the scripts use the standard library.

```sh
# Discover unreviewed candidates. Results are not imported into the catalog.
python3 scripts/collect.py search --provider arxiv --query 'all:"SWE-bench" AND all:"quality"' --limit 5
python3 scripts/collect.py search --provider crossref --query 'SWE-bench benchmark quality' --limit 5

# Cache a primary source with its retrieval time, URL, status and hash.
python3 scripts/collect.py fetch --id anthropic-infrastructure-noise

# After reviewing sources and editing curated records:
python3 scripts/catalog.py
python3 scripts/catalog.py --check
```

Snapshots and unreviewed search results stay in ignored `.cache/`. A successful HTTP request is not evidence review; an API failure is not evidence that no relevant work exists. Full texts are linked rather than redistributed. The published catalog contains short annotations and source links.
