# Research basis for Agent Mission Control

Agent Mission Control should remain a small, adaptive orchestration skill that
uses native host tools. Its useful responsibilities are choosing work, assigning
sufficient context and capability, preserving progress, and requiring evidence
before acceptance. A separate workflow engine, compulsory agent team or automatic
skill-training service is not justified for this project.

This review covers the whole repository: runtime instructions, context and
handoff templates, model configuration, optimization, recovery, verification,
learning, resource accounting, packaging, CI, fixtures and public claims. External
research informs the design. Local engineering checks establish specific software
properties. Neither establishes that this AMC candidate outperforms ordinary
competent development or saves money across tasks.

## Evidence and its limits

Primary publications and current platform documentation were checked on
2026-09-13. A paper's measured outcome, a vendor's engineering recommendation and
AMC's implementation choice are different kinds of evidence. None is silently
promoted to another. Historical local cases are useful regressions, not a random
sample or an untouched test set. No new paid behavioral experiment accompanies
this update.

### NVIDIA: sustained execution with feedback

[NVIDIA's AVO paper, v1, 25 March 2026](https://arxiv.org/abs/2603.24517v1)
reports seven days of B200 attention-kernel optimization, more than 500 explored
directions and 40 committed versions. Reported causal MHA gains reach 3.5%
over cuDNN and 10.5% over FlashAttention-4 in the evaluated configurations.
Sections 3-4 describe a single lineage, execution-based correctness and throughput,
persistent history and conditional intervention during stagnation. Correct
candidates may match or improve the incumbent. Table 1 ablates kernel changes,
not memory or supervisor contributions. The preprint supplies no controlled
same-compute baseline agent, detailed model/prompt specification or total token
bill. The concrete internal agent is not a published open-source skill.

The later [NVIDIA ARC-AGI-3 report, 21 August 2026](https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/)
reports 100.00 RHAE on 25 public environments, all 183 levels, with Opus 5.
Its 6,624 versus VISTA's 7,542 actions is about 12% fewer, explicitly not a
controlled architectural ablation. Private competition sets were not evaluated.
[ARC's scoring methodology](https://docs.arcprize.org/methodology) measures task
completion and environment-action efficiency; this is not an all-system price
comparison.

**AMC decision:** preserve execution feedback, useful failed-attempt diagnoses,
recoverable artifacts and conditional reconsideration. A fixed two-failure
checkpoint and strict tie rejection are local conservative choices, not NVIDIA
findings. Do not require a seven-day search, supervisor daemon or population of
agents. Long implementation can use observable milestones without pretending
that every task has a numerical optimization score.

### OpenAI and Anthropic: context, tools and incremental work

[OpenAI's multi-hour execution-plan example](https://developers.openai.com/cookbook/articles/codex_exec_plans)
uses a maintained plan, progress, decisions and observable acceptance so work can
resume without relying on previous chat. It is a cookbook example rather than a
universal requirement for a particular filename or a controlled performance study.
[Anthropic's long-running harness report](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
describes premature completion and poorly documented partial work across context
windows; incremental implementation and durable artifacts address those problems.
Its initializer/coding-agent arrangement is one implementation, not a required
extra pair of AMC agents.

[Anthropic's newer Managed Agents report, 8 April 2026](https://www.anthropic.com/engineering/managed-agents)
warns that model-specific scaffolding can become obsolete as capabilities change.
It separates durable sessions, the agent harness and execution sandbox behind
interfaces. For AMC, this supports periodically removing obsolete instructions
and using the host's existing state and permission boundaries. It does not justify
recreating that hosted service inside a portable skill.

[Anthropic's context-engineering guidance](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
supports focused subagent contexts and distilled returns. It also describes
compaction and structured notes. Overcompression can lose information needed
later. AMC therefore sends enough requirements, interfaces and evidence references
for the assigned job, rather than optimizing packets to the fewest possible words.
The lead preserves the overall state, not every worker transcript.

[OpenAI's skills documentation](https://learn.chatgpt.com/docs/build-skills)
describes name/description discovery and loading the selected skill body. This
supports one short AMC entrypoint and conditional references. Daily domain skills
remain available for their actual tasks; their entire bodies do not belong in
AMC or every context pack. A larger skill library is not evidence that every
skill was available, selected or executed on a particular run.

**AMC decision:** keep the existing mission record, native compaction and source
files. Record the current milestone, known-working artifact, failed approaches
and next action before handoff. Do not create another context database, transcript
mirror, fixed initializer agent or mandatory plan file. Context isolation is an
information boundary; host permissions enforce execution boundaries.

### Team shape and model choice

[Google Research's 2026 scaling study](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
compares 180 configurations across financial reasoning, browsing, planning and
tool-use tasks. Coordination helps suitable decomposable tasks but can hurt
sequential tasks. Its task-specific thresholds are not universal AMC triggers or
measurements on the FPS app. [Anthropic's research-system report](https://www.anthropic.com/engineering/multi-agent-research-system)
also finds value in parallel exploration while reporting substantial token
overhead; research results do not automatically transfer to tightly coupled coding.

[RouteLLM](https://arxiv.org/abs/2406.18665) demonstrates cost/quality trade-offs
from stronger/weaker model routing on its evaluated benchmarks. That is useful
support for capability-aware allocation, but routing individual queries does not
validate an entire multi-turn software workflow or establish current Sol/Luna
performance.

[Current OpenAI subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents)
allows independent model and effort choices, recommends caution with parallel
writers and distinguishes narrow repeatable work from ambiguous multi-step work.
It describes low effort for simple work, medium as balanced, and high for complex
logic or review. Additional agents consume resources. File ownership still needs
to be explicit; a concurrency ceiling is not a desired team size.

**AMC decision:** the selected competent lead owns architecture and final
acceptance. Use a scout for valuable uncertainty, not every task or subtask.
Give weaker workers narrower contracts and clearer checks. Parallelize ready,
independent work; serialize shared writes and real dependencies. The opt-in
profile now illustrates Sol/medium lead, Luna/medium generic workers,
Terra/medium investigation/implementation, Terra/high material review and
Luna/medium narrow verification. These are editable starting points, not a
research-proven ranking or an automatic change to installed settings.

### Verification, learning and adaptive procedure

[Anthropic's evaluator-optimizer guidance](https://www.anthropic.com/engineering/building-effective-agents)
conditions refinement on useful evaluation criteria and feedback. Its patterns
are composable, not a compulsory sequence. An [ACL 2024 error-localization study](https://aclanthology.org/2024.findings-acl.826/)
distinguishes locating a reasoning error from repairing one when its location
is supplied. The older tasks/models do not establish current model limits, but
reinforce why a confident critique is weaker evidence than a reproducible failure.
A fresh reviewer can still share the implementer's blind spots.

[Microsoft SkillOpt, v2, 25 May 2026](https://arxiv.org/abs/2605.23904v2)
uses scored trajectories, bounded edits, rejected-edit memory and separate
train/selection/test data. Its reported best-or-tied results across 52 evaluated
cells concern its training setup, not arbitrary hand-written instructions.
Section 4 separates selection feedback from final tests. The procedure involves
real training/evaluation work; an exported skill avoids extra deployment model
calls, but its text still contributes input and its training was not free.

A newer [Microsoft-associated OEO preprint, 10 August 2026](https://arxiv.org/abs/2608.09629v1)
compares adaptive optimization with SkillOpt and GEPA. It reports 12 wins, one
tie and one narrow loss in 14 comparisons using a GPT-5.5 optimizer. The median
34.3% figure concerns the configured SkillOpt **target-interaction** token budget,
not total cost. Section 3.1 explicitly reports some optimizer-budget overruns;
section 3.3 finds that medium Qwen3.5-27B benefits more from prescribed SkillOpt
and weak Qwen3.5-4B fails to act through the unchanged OEO interface. The result
supports capability-dependent structure, not removing budgets, data boundaries
or evaluation, and does not identify Luna with those tested weak models.

**AMC decision:** keep fixed authority and acceptance while allowing a capable
lead to adapt the route. Add detail to a worker contract when its task needs it.
Require reproducible findings and current checks; do not equate reviewer agreement
with correctness. Separate source-backed maintenance from outcome-driven skill
learning. Maintenance can be reviewed and locally checked without a fabricated
mini-benchmark. Empirical improvement claims still require comparable outcomes
and appropriate untouched final data. Without that budget, retain a lesson note
and no improvement claim; do not launch automatic Sleep/SkillOpt training.

### Cost and evaluation under a small budget

[OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
warns against unrepresentative cases and adding agent complexity without evidence.
[AI Agents That Matter](https://arxiv.org/abs/2407.01502) argues for evaluating
cost alongside accuracy and identifies weak holdouts and reproducibility as
problems. These support proportionate validation; they do not make a one-pair
comparison statistically reliable or require every engineering fix to become a
model benchmark.

[OpenAI's pricing documentation](https://learn.chatgpt.com/docs/pricing)
distinguishes model-specific input, cached input and output rates. [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
depends on eligible reusable prefixes and request settings. Cache-write charges,
service tiers and changed context can alter the economics. A high cache fraction
or smaller raw prompt does not alone establish savings.

For an applicable rate card, estimate each model's uncached input, cached reads
and output separately, then add observable write/tool/tier charges. Include lead,
children, failed attempts and repairs. Preserve missing data as unknown. Report
setup and research separately from task execution, while retaining both in the
whole-run total. API price estimates, included subscription capacity and observed
credit charges are different quantities. Do not hardcode current prices into a
portable skill or implement a billing system from incomplete local counters.

**AMC decision:** routine progress comes from necessary real work and executable
acceptance checks. Record confirmed defects, false alarms, regressions, repair
and resource observations when useful. Do not create repeat runs merely to fill
a model matrix. A future comparison needs a specific decision, frozen conditions,
authorization and budget; a general superiority claim needs substantially more
than these development examples.

## Whole-project review and implemented changes

The implementation remains a Markdown skill plus existing Python tooling. The
source snapshot before this update contained 117 files, including pre-existing
uncommitted work. The current runtime changes are candidate.4; installed/global
skills and Codex settings are separate and were not modified.

| Area inspected | Decision and evidence boundary |
|---|---|
| SKILL.md and workflow ownership | Retain one entrypoint. Add grounded long-work routing and explicit authority/source separation. No fixed team or extra service. |
| Context, evidence and mission templates | Existing contracts already cover task, scope, dependencies and proof. Keep their schema; add handoff guidance in existing references instead of another template. |
| Optimization and recovery references | Distinguish milestone progress from scored optimization; preserve failed hypotheses and recoverable checkpoints. Label tie and stagnation rules as AMC choices. |
| Verification and domain skills | Preserve risk-based review and executed checks. Clarify that fresh context does not ensure independent errors; use relevant domain expertise without importing a whole skill library. |
| Learning and contribution policy | Permit source-backed maintenance with appropriate engineering checks. Keep empirical learning claims separate, with protected final tests when such experiments are actually authorized. |
| Optional Codex configuration | Replace expensive example defaults with the scoped profile above. Keep supported overrides, ownership and sandbox settings; no automatic installation. |
| Usage collector and controls | Fix lexical timestamp comparison. Parse timezone-aware instants, refuse malformed/naive times, and test boundary equality, precision and offsets. Observed snapshots remain distinct from billing. |
| FPS fixture preparation | Reuse the existing linked-ancestor guard before resolving output paths. Reject a linked parent and dangling manifest link before writes. These are path-safety checks, not an adversarial C# sandbox. |
| Packager and validators | Preserve standard-library implementation, identical runtime bytes in skill/plugin forms, safe path/refusal controls and fixed archives. Bump candidate version. A dirty development snapshot needs exact hashes, not an assumed identity from version/origin alone. |
| CI and historical evaluations | Existing CI runs local structural, packaging, accounting, preservation and replay checks. Official plugin validation is a manual local check; the historical v3 preparation self-check requires its external snapshots. Neither gap is concealed as current automated proof. |
| README, provenance, security and assets | Link this report, keep experimental/no-endorsement claims and dated security guidance. Preserve current visuals and existing source-license boundaries. No unrelated redesign or source copying. |

The earlier pinned Untrivial and donvito implementations remain credited in
[provenance](../references/provenance.md). Their useful ownership/native-runtime
mechanisms were already adopted; their schedulers and fixed delegation triggers
are not required here. This review does not claim a new execution of those
upstream systems or that every unrelated daily business skill was imported.

## Engineering acceptance and ongoing use

Two concrete faults were reproduced before repair: an equivalent cutoff without
fractional seconds miscounted usage, and linked replay output paths accepted
writes. Their new controls fail the old behavior and pass the corrections. These
observations justify the fixes without measuring model quality.

Run the existing local checks after affected changes:

```sh
python scripts/validate.py
python scripts/test_validate.py
python scripts/test_prepare_eval.py
python scripts/test_package_plugin.py
python scripts/test_usage_snapshot.py
python evals/preservation_check.py --self-check
python evals/fps_replay.py --self-check
```

The JSON replay requires a .NET 8 SDK; use its documented explicit path if needed.
These commands do not launch agents. Package acceptance additionally checks the
actual generated skill/plugin and records source/ZIP identities. The official
plugin validator is available in the local skill-development environment; it is
not a vendored dependency or a claim that GitHub ran it.

On ordinary work, choose the relevant task checks, retain the failure and its
repair, and preserve unrelated passing evidence. For example, a difficult FPS
release problem can begin with a lead-owned investigation, delegate one independent
boundary audit, repair from an executed counterexample, and finish against the
real release gates. It need not exercise every AMC mechanism. A feature depending
on the previous change stays sequential even when it spans many files.

**Current evidence level:** research-guided design with local engineering
validation. Comparative model quality, cost savings, automatic host activation,
global adoption and the FPS application's complete release readiness are not
established by this update. Prior failed or limited experiments remain intact.

Local acceptance on 2026-09-13 passed all seven check groups above, both official
package validators and a fresh independent source/engineering review. The 16
runtime files match byte-for-byte between source and generated skill/plugin.
All 74 historical evaluation, fixture and result files covered by the preservation
check remain identical to the pre-task snapshot. These are engineering outcomes,
not comparative model results. The candidate remains local and uninstalled.

## Source record

Sources were accessed on 2026-09-13. Primary empirical work above is identified by
version/date where available: NVIDIA AVO v1 (2026-03-25), NVIDIA ARC blog
(2026-08-21), SkillOpt v2 (2026-05-25), OEO v1 (2026-08-10), Google scaling report
(2026-01-28), RouteLLM (2024), ACL error-localization paper (2024), and AI Agents
That Matter (2024). The arXiv preprints are not described as peer-reviewed results.

OpenAI skills, subagents, pricing, caching, evaluation and execution-plan pages
are live platform guidance, not a pinned client compatibility specification.
Anthropic's effective-agents (2024-12-19), context-engineering (2025-09-29),
research-system (2025-06-13), long-running-harness (2025-11-26) and
Managed Agents (2026-04-08) articles are engineering reports. ARC scoring describes the benchmark's metric. Exact source
links appear next to the claims they support; AMC decisions and repository
observations are explicitly separated from those claims.
