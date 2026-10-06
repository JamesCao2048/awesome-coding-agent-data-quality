# Awesome Coding Agent Data Quality

A curated collection of **papers, tools and technical resources for trustworthy coding-agent training data and benchmarks**.

A task can run successfully and still be a bad training or evaluation example: its instructions may omit a requirement, its tests may reject a valid solution, or an incorrect patch may receive full credit. This collection covers how those problems are prevented, discovered and repaired.

**46 resources · Updated October 7, 2026**

**Use tags:** `Training data` identifies work on training-task data or training environments; `Benchmark` identifies work on evaluation data or evaluation reliability. Both tags appear when a work addresses both. These tags describe the quality application studied, not merely whether a paper uses a benchmark to evaluate its model.

**Publication labels:** papers show the verified venue and first-author affiliation; **Preprint** means a manuscript is available but its conference venue was not verified. Blogs show the author organization or publisher; unavailable affiliations are marked explicitly.

**Quality dimensions:** work may check the environment, task, verifier, evaluation protocol or contamination. A verifier is the test or rule that decides whether a solution succeeds. See the [tag guide](docs/curation.md#quality-dimensions) for definitions.

The core is repository-level software-engineering tasks and agent training environments. Relevant terminal tasks are also included. Function-level tests, scientific workflows and broader agent methods are labeled **Adjacent** where their evidence does not directly establish repository-task quality.

## Contents

**Literature**

- [Data construction and validation](#construction) (21)
- [Quality audits and empirical studies](#audits) (7)
- [Automated checking and repair](#batch-auditing) (11)
- [Evaluating the auditors](#meta-evaluation) (3)
- [Evaluation protocols and contamination](#protocol) (4)
- [Quality auditing](#quality-auditing) — where to start

**About this list**

- [How to use this list](#how-to-use-this-list)
- [Contributing](#contributing)
- [Attribution](#attribution)

<a id="construction"></a>

## Data construction and validation

How training tasks, execution environments and benchmark datasets are built and screened before use.

- **[ScaleSWE](https://arxiv.org/abs/2602.09892)** (Preprint 2026; Affiliation unverified) `Training data` — ScaleSWE coordinates agents for Docker setup, test generation, and problem-statement synthesis from GitHub pull requests.

- **[Multi-SWT-Bench](https://arxiv.org/abs/2609.34752)** (Preprint 2026; Kyushu University) `Benchmark` — Multi-SWT-Bench adapts multilingual repository issues into a benchmark for generating tests that reproduce the reported bug. It filters tasks by executing developer-written tests against buggy and fixed repository states.

- **[Nemotron Terminal Data Engineering](https://arxiv.org/abs/2602.21193)** (NeurIPS 2026; NVIDIA) `Training data` — This work describes engineering a large terminal-agent training corpus from seed tasks and synthetic tasks, with executable environments, test expectations, and dataset-level filtering. It is broader than repository issue resolution but includes concrete task and trajectory quality controls. [Dataset collection](https://huggingface.co/collections/nvidia/nemotron-terminal).

- **[SWE-rebench V2](https://arxiv.org/abs/2602.23866)** (ICML 2026; Nebius) `Training data` `Benchmark` — Extends automated collection across languages, adding setup synthesis, issue-clarity filtering, and diagnostic metadata about task quality.

- **[SWE-World](https://arxiv.org/abs/2602.03419)** (Preprint 2026; Renmin University of China) `Training data` — **Adjacent.** Replaces expensive repository execution with learned transition and reward models while preserving deterministic file operations. [Code](https://github.com/RUCAIBox/SWE-World).

- **[SetUpAgent](https://arxiv.org/abs/2503.07701)** (ICML 2025; LogicStar AI) `Benchmark` — SetUpAgent turns real issue-linked pull requests into executable repository tasks by reconstructing environments and checking the reference fix against tests. Its pipeline is useful for studying setup reliability and test-level filtering during benchmark construction.

- **[MCTS-Refined CoT](https://arxiv.org/abs/2506.12728)** (ASE 2025; Northeastern University) `Training data` — MCTS-Refined CoT filters and refines repository-issue reasoning traces using stepwise gold-aligned checks for localization and patching. It is relevant to trajectory quality for fine-tuning, rather than a standalone task benchmark audit. [Project](https://mcts-refine.github.io/).

- **[Multi-SWE-bench](https://proceedings.neurips.cc/paper_files/paper/2025/hash/5afa9cb1e917b898ad418216dc726fbd-Abstract-Datasets_and_Benchmarks_Track.html)** (NeurIPS 2025; ByteDance Seed) `Benchmark` — Multi-SWE-bench extends issue-resolution evaluation across languages and documents a construction pipeline combining runnable repository environments, patch/test execution, and human annotation. The final NeurIPS dataset contains 2,132 tasks, including the reused 500-task SWE-bench Verified subset and additional multilingual instances. [Code](https://github.com/multi-swe-bench/multi-swe-bench).

- **[R2E-Gym](https://arxiv.org/abs/2504.07164)** (COLM 2025; University of California, Berkeley) `Training data` — Constructs executable training tasks from commits with synthesized tests and issue descriptions; uses test execution and learned scoring models to rank candidate repairs. [Code](https://github.com/R2E-Gym/R2E-Gym).

- **[SWE-bench-Live](https://arxiv.org/abs/2505.23419)** (NeurIPS 2025; Microsoft) `Benchmark` — Introduces SWE-bench-Live and RepoLaunch to collect recent real issues and automate their execution environments. [Project](https://swe-bench-live.github.io/).

- **[SWE-Bench Pro](https://arxiv.org/abs/2509.16941)** (ICML 2026; Scale AI) `Benchmark` — Constructs harder repository tasks with human-augmented requirements, explicit interfaces, reviewed tests, and containerized environments.

- **[SWE-Factory](https://arxiv.org/abs/2506.10954)** (FSE 2026; Sun Yat-sen University) `Training data` `Benchmark` — Automates issue collection and environment setup, then checks whether tests fail before a reference fix and pass afterward. [Code](https://github.com/DeepSoftwareAnalytics/swe-factory).

- **[SWE-rebench](https://arxiv.org/abs/2505.20411)** (NeurIPS 2025; Nebius) `Training data` `Benchmark` — Combines automated executable-task collection with learned quality assessment and continuously refreshed evaluation tasks.

- **[SWE-smith](https://arxiv.org/abs/2504.21798)** (NeurIPS 2025; Stanford University) `Training data` — Creates an environment first, then injects synthetic bugs into existing repositories and generates issue descriptions for agent training. [Project](https://swesmith.com/).

- **[SWE-Flow](https://arxiv.org/abs/2506.09003)** (ICML 2025; Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences) `Training data` `Benchmark` — SWE-Flow synthesizes repository-level software tasks from existing tests and their runtime dependencies. It filters unusable tests and uses a runtime dependency graph to derive code-generation tasks from tested behavior. [Code](https://github.com/Hambaobao/SWE-Flow).

- **[SWE-Playground](https://arxiv.org/abs/2512.12216)** (Preprint 2025; Tsinghua University) `Training data` — SWE-Playground creates synthetic repository environments and tasks for coding-agent training, with separate generation and execution checks for task tests and implementations. Its issue-adaptation experiments also connect synthetic tasks to real repository issues. [Code](https://github.com/neulab/SWE-Playground).

- **[SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)** (2024; blog; OpenAI) `Benchmark` — Human-screened SWE-bench subset and public annotation rubric, useful as a baseline for checking whether issue descriptions and hidden tests define a fair task.

- **[SWE-bench Multimodal](https://proceedings.iclr.cc/paper_files/paper/2025/hash/07d6332ae36730707fddddba736d7b6c-Abstract-Conference.html)** (ICLR 2025; Stanford University) `Benchmark` — SWE-bench Multimodal extends issue-resolution tasks to software whose behavior is assessed through visual interfaces. The official benchmark page documents the September 2026 Multimodal V2 update with 480 tasks, reproducible selection, removal of known flaky or ungradeable tests, and environment/grading maintenance. [Benchmark](https://www.swebench.com/multimodal.html).

- **[SWT-Bench](https://papers.nips.cc/paper_files/paper/2024/hash/94f093b41fc2666376fb1f667fe282f3-Abstract-Conference.html)** (NeurIPS 2024; ETH Zurich) `Benchmark` — SWT-Bench evaluates whether agents can write tests that reproduce real repository bugs and validate fixes. Its construction filters issue/PR cases using execution of the reference fix and generated or collected reproduction tests. [Code](https://github.com/logic-star-ai/SWT-Bench).

- **[SWE-Gym](https://arxiv.org/abs/2412.21139)** (ICML 2025; University of California, Berkeley) `Training data` — Builds executable training tasks from real GitHub issues, then uses the resulting interactions to train agents and trajectory verifiers. [Code](https://github.com/SWE-Gym/SWE-Gym).

- **[SWE-bench](https://arxiv.org/abs/2310.06770)** (ICLR 2024; Princeton University) `Benchmark` — Foundational issue-to-pull-request benchmark construction pipeline, connecting a repository snapshot, a natural-language issue, a reference patch, and executable tests. [Project](https://www.swebench.com/).

<a id="audits"></a>

## Quality audits and empirical studies

Investigations of defects in existing datasets, tests and evaluation results.

- **[SWE-bench Pro Determinacy Audit](https://www.june.kim/a-determinacy-audit-of-swebench-pro)** (2026; report; Not stated in the report) `Benchmark` — This independent report audits all 728 public SWE-bench Pro tasks for whether the materials given to a solver determine the behavior checked by hidden tests. It reports a 15.0% conservative underdetermination floor, including a mechanically supported subset, and three reference patches that fail the official verifier. [Per-task receipts and audit code](https://github.com/kimjune01/swebench-pro-audit).

- **[SWE-Bench Pro audit (OpenAI)](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)** (2026; blog; OpenAI) `Benchmark` — Audits SWE-Bench Pro through automated triage, investigator agents with repository/environment access, and independent software-engineer review.

- **[SWE-Bench Pro Verified](https://arxiv.org/abs/2609.08149)** (Preprint 2026; East China Normal University; Shanghai Artificial Intelligence Laboratory) `Benchmark` — Repairs SWE-Bench Pro through two tracks: reducing accessible solution/evaluation leakage and refining confirmed task-description or test defects. [Code](https://github.com/open-compass/AgentCompass).

- **[SWE-bench Verified audit (OpenAI)](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)** (2026; blog; OpenAI) `Benchmark` — OpenAI documents residual test/specification defects in SWE-bench Verified and evidence that frontier models can recall some benchmark solutions.

- **[PatchDiff](https://arxiv.org/abs/2503.15223)** (ICSE 2026; Zhejiang University) `Benchmark` — Studies test-passing SWE-bench Verified patches using broader developer tests and PatchDiff, which generates tests exposing behavioral differences between an agent patch and the reference fix. [Code](https://github.com/ZJU-CTAG/PatchDiff).

- **[SWE-Bench+](https://arxiv.org/abs/2410.06992)** (AIware 2026; York University) `Benchmark` — Audits SWE-bench patches that passed existing tests and distinguishes exposed solutions, incorrect or incomplete fixes, and legitimate alternatives to the reference patch. [Data](https://zenodo.org/records/13879453).

- **[EvalPlus](https://arxiv.org/abs/2305.01210)** (NeurIPS 2023; University of Illinois Urbana-Champaign) `Benchmark` — **Adjacent.** EvalPlus augments code-generation benchmarks with automatically generated test inputs to expose incorrect programs that small original test suites accept. **Abstract only.** [Code](https://github.com/evalplus/evalplus).

<a id="batch-auditing"></a>

## Automated checking and repair

Reusable methods and tools for finding, diagnosing and repairing quality problems at scale.

- **[Auto Benchmark Audit (ABA)](https://arxiv.org/abs/2605.26079)** (Preprint 2026; Duke University) `Benchmark` — Organizes instructions, environment files and grading code for evidence-linked audits using task materials or recorded agent runs, including coding benchmarks. [Code](https://github.com/IsThatYou/auto-bench-audit).

- **[Automated Transcript Analysis](https://arxiv.org/abs/2607.27518)** (Preprint 2026; Independent; Arcadia Impact (work completed there)) `Benchmark` — Develops transcript scanners for ground-truth access, tool failures, guessing and answer-format ambiguity; includes SWE-bench Verified, KernelBench and Terminal-Bench cases.

- **[Coding Agents as Test-Suite Auditors](https://arxiv.org/abs/2608.01715)** (Preprint 2026; Harbin Institute of Technology) `Benchmark` — **Adjacent.** This work uses coding agents to generate adversarial tests that check whether official online-judge suites accept buggy submissions. A multi-step certification process independently checks expected outputs and input legality, making the discovered verifier gaps auditable. [Evidence package and research artifacts](https://github.com/xieTwim/test-suite-auditors).

- **[Continuous Benchmarks](https://www.tbench.ai/news/continuous-benchmarks)** (2026; blog; Laude Institute) `Benchmark` — Treats benchmarks as maintained software, with production feedback informing quality checks and versioned changes.

- **[BenchJack](https://arxiv.org/abs/2605.12673)** (Preprint 2026; University of California, Berkeley) `Benchmark` — Uses coding agents to find ways of receiving credit without completing a task, then repairs exposed grading weaknesses, including SWE-bench cases. [Code](https://github.com/benchjack/benchjack).

- **[PAIChecker](https://arxiv.org/abs/2607.28587)** (ASE 2026; The Chinese University of Hong Kong, Shenzhen) `Training data` `Benchmark` — PAIChecker treats mismatches between a GitHub issue and its linked pull request as a construction defect in SWE-bench-like datasets. It proposes a multi-agent checker that combines issue/PR evidence with code-level validation. [Code and annotations](https://github.com/manyiResearch/PAIChecker).

- **[PROBE](https://arxiv.org/abs/2604.01518)** (ASE 2026; Concordia University) `Benchmark` — PROBE uses variants of a reference repair to identify potential gaps in a benchmark's tests. It generates additional tests that distinguish reference repairs from surviving variants, then checks their robustness under behavior-preserving transformations.

- **[Terminal-Bench Science quality checks](https://github.com/harbor-framework/terminal-bench-science/blob/main/CONTRIBUTING.md)** (2026; tool; Harbor Framework) `Benchmark` — **Adjacent.** Combines static checks, rubric review, reference-solution runs and no-op runs in a task contribution workflow. [Rubric](https://github.com/harbor-framework/terminal-bench-science/blob/main/rubrics/task-implementation.toml).

- **[BenchGuard](https://arxiv.org/abs/2604.24955)** (Preprint 2026; University of Washington; Phylo, Inc.) `Benchmark` — **Adjacent.** BenchGuard cross-checks instructions, reference programs, evaluation scripts and environment configurations, evaluated primarily on scientific agent tasks.

- **[SPICE](https://arxiv.org/abs/2507.09108)** (ASE 2025; Queen’s University) `Training data` `Benchmark` — Automates SWE-bench-style dataset review with separate issue-clarity and test-adequacy assessments, following the SWE-bench Verified annotation rubric. [Code & data](https://github.com/SAILResearch/SPICEBench).

- **[UTBoost](https://aclanthology.org/2025.acl-long.189/)** (ACL 2025; The Chinese University of Hong Kong, Shenzhen) `Benchmark` — Augments SWE-bench tests to expose previously accepted incorrect patches and separately fixes evaluation-log parsing errors that can corrupt pass/fail annotations. [Code](https://github.com/CUHK-Shenzhen-SE/UTBoost).

<a id="meta-evaluation"></a>

## Evaluating the auditors

Benchmarks and methods for measuring whether a checker detects the right defect for the right reason.

- **[TRACE](https://proceedings.mlr.press/v306/deshpande26a.html)** (ICML 2026; Patronus AI) `Benchmark` — **Adjacent.** Introduces TRACE, a human-checked synthetic trajectory benchmark for evaluating reward-hack detectors in code environments; contrasts isolated classification with comparison across trajectories. [Data](https://huggingface.co/datasets/PatronusAI/trace-dataset).

- **[Task Verification Bench (TVB)](https://posttrain.dev/task-verification-bench-paper.pdf)** (Preprint 2026; Delphik) `Benchmark` — Task Verification Bench evaluates whether agents can identify benchmark defects, using SWE-bench human annotations and Terminal-Bench repair histories as reference evidence. [Author article](https://posttrain.dev/blog/can-llms-detect-benchmark-defects).

- **[SWE-Mutation](https://arxiv.org/abs/2605.22175)** (ACL Findings 2026; University of Science and Technology of China) `Benchmark` — SWE-Mutation benchmarks the discriminative power of test suites by checking whether semantically meaningful code mutants can still pass. It also studies how an agentic mutation process changes the difficulty of evaluating test-generation systems. [Code and benchmark](https://github.com/Sunny4Coding/SWE-Mutation).

<a id="protocol"></a>

## Evaluation protocols and contamination

Resource limits, measurement noise, leakage and versioning that affect interpretation.

- **[Infrastructure noise in coding evaluations](https://www.anthropic.com/engineering/infrastructure-noise)** (2026; blog; Anthropic) `Benchmark` — Measures how sandbox resource allocation changes coding-evaluation reliability and scores.

- **[Terminal-Bench 4.0 quality update](https://www.tbench.ai/news/terminal-bench-4-0)** (2026; blog; Laude Institute) `Benchmark` — Documents task fixes, resource calibration and version rules for rerunning or regrading evaluations.

- **[SWE-bench Verified: Ability or Memory?](https://arxiv.org/abs/2512.10218)** (Preprint 2025; Central Peel Secondary School) `Benchmark` — This study probes possible benchmark exposure by asking two Claude models to localize edited files from issue text with deliberately limited context. The authors report much higher localization on SWE-bench Verified than on BeetleBox and SWE-rebench, which is consistent with possible task familiarity but does not establish training-set contamination.

- **[Saving SWE-Bench](https://arxiv.org/abs/2510.08996)** (CAIN 2026; Microsoft) `Benchmark` — This work rewrites formal GitHub issues into user-style prompts derived from coding-assistant interaction patterns, then compares agent performance on the original and mutated task descriptions. It measures how task presentation can change reported bug-fixing performance, rather than auditing hidden-test correctness. [Mutated benchmark and code](https://github.com/microsoft/SWE-Bench-Mutated-CAIN26).

## Quality auditing

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

---

⭐ If you find this list useful, please consider giving it a star!
