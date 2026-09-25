# Historical iteration-2 source decision

The ownership choices below describe iteration 2. Iteration 3 absorbs useful
mechanisms into standalone AMC; current mapping and license decisions are in
[design sources](../skills/agent-mission-control/references/provenance.md). Source observations below remain
relevant; companion requirements and Luna-only constraints are superseded.

# Source-backed ownership decision

2026-09-12. This records inspected implementations and published guidance, not
upstream benchmark reproduction. The implemented candidate remains a portable
skill, with an optional Astra/Luna profile. No runtime service was added.

## Smallest useful boundary

| Owner | Responsibility | Does not own |
|---|---|---|
| Astra / selected lead | Architecture, scope, tradeoffs, integration, final evidence | Every mechanical investigation |
| Luna / focused worker | One bounded investigation, edit, test or review | Goal changes, model escalation or aggregate PASS |
| Mission Control | Cross-phase semantic facts, ownership reconciliation, acceptance gates | A second session runtime or competing execution loop |
| Context Diamond | Applicable substantial fan-out: dependency test, contracts, isolation, verification | Outer optimization selection |
| AVO | Frozen evaluator, candidate lineage, feedback, selection and bounded repair | Ordinary engineering by default |
| Offline learning | Completed-task evidence, separate validation and staged skill evolution | Mutation of the live governing skill |
| Native Codex / host | Sessions, tool execution, subagent lifecycle, history/compaction, runtime events | Deciding whether project acceptance evidence is sufficient |

One focused investigation can use a native scoped worker without a full fan-out
workflow. An applicable companion takes precedence over the local portable
fallback for its mechanism. Distinct nested responsibilities are allowed: AVO
may request Diamond jobs, but retains candidate selection. AMC reuses the result
and adequate current review; it does not repeat either procedure.

## Compared implementations: adopt and reject

**Context Diamond, current local implementation.** Its SKILL.md defines a minimal
context pack, the fake-edge dependency test, bounded contracts, separate writable
scopes, fresh verification and a completion contract. These are procedural
instructions, not a scheduler. Adopt it as the one owner when applicable. Do not
repeat its fan-out/reduce/verify sequence inside AMC or use it for a small
sequential change. Its general Terra/Sol routing yields to this session's explicit
Luna-only constraint; no global skill was modified.

**Local AVO.** Its SKILL.md freezes correctness and metric priority, reruns the
incumbent, records parent/score/diagnosis, keeps recoverable candidates and calls
for reconsideration after repeated non-improvement. Adopt those boundaries through
the existing owner. Reject mandatory optimization for ordinary implementation.
AMC's absent-companion fallback is shorter and uses strict improvement, including
keeping the incumbent on ties. Global skills and aliases were freshly hashed in
external design-mining/instruction-surface.json.

**SkillOpt / Sleep, commit 79124b37.** The trainer owns rollout/state effects while
[evaluation/gate.py](https://github.com/microsoft/SkillOpt/blob/79124b37e9a6371e13b753f8bcd7adb1e493ade1/skillopt/evaluation/gate.py)
compares scores. [Sleep cycle.py](https://github.com/microsoft/SkillOpt/blob/79124b37e9a6371e13b753f8bcd7adb1e493ade1/skillopt_sleep/cycle.py)
separates training/selection from final test scoring; the test result is write-only
for selection. No-regression is configurable, not a universal default guarantee.
[staging.py](https://github.com/microsoft/SkillOpt/blob/79124b37e9a6371e13b753f8bcd7adb1e493ade1/skillopt_sleep/staging.py)
pins identities/hashes and supports recoverable adoption. Adopt held-out validation,
recoverable lineage and separate staged adoption through the existing offline
workflow. Reject a new learner in AMC, automatic live adoption and the optional
instruction-word-density bonus: more MUST/ALWAYS words are not task quality.
No upstream tests or learning jobs were executed.

**Astra/Luna Orchestrator, commit 575e74eb.** Its
[actual skill](https://github.com/donvito/codex-astra-luna-orchestrator/blob/575e74ebcf9b199513151a8996665a71cf64ce50/profiles/pro/agents/skills/astra-orchestrator/SKILL.md)
has a root-only path but also MUST-delegate triggers for multi-file work and
exploration. Model/role instructions pin bounded Luna work and lead-owned escalation;
they do not prove savings. Adopt bounded roles, short inputs and explicit escalation
ownership. Reject mechanical multi-file delegation and an obligatory Astra reviewer.
Our optional example routes every child role to Luna without changing core portability.

**Agent Orchestrator, commit 15e9ea97.**
[SessionRecord/ControllerOwner](https://github.com/Untrivial-ai/agent-orchestrator/blob/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6/backend/internal/domain/session.go#L91)
store facts and fence controller ownership;
[toSessionWithFacts](https://github.com/Untrivial-ai/agent-orchestrator/blob/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6/backend/internal/service/session/service.go#L1001)
derives status from persisted session and PR facts.
[ObserveWorkspace](https://github.com/Untrivial-ai/agent-orchestrator/blob/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6/backend/internal/adapters/workspace/gitworktree/workspace.go#L987)
validates a managed path and reads bounded Git state. Adopt fact-based reconciliation
and no overlapping replacement owner. Keep existing resume safeguards. Reject a new
Kanban/daemon/worktree manager: this product has no demonstrated need for a second
runtime. Source-level protections are not independently reproduced upstream results.

**NVIDIA AVO.** The [paper](https://arxiv.org/abs/2603.24517) and
[architecture publication](https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/)
describe execution feedback, persistent lineage, recoverability and supervisor
intervention. Published system results do not isolate those components as AMC
improvements. Adopt their principles through local AVO; reject benchmark-number
transfer, unbounded search and another supervisor absent a measured failure.

## Native platform constraints

Current [Astra guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)
warns that conflicting skill instructions can change behavior and recommends
calibrating delegation/testing. This supports narrow activation, one owner and
preserving current checks rather than repeated blanket verification.

[AGENTS discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
loads global then applicable project instructions. The fresh local audit found no
repo-ancestor AGENTS file and a global AMC different from the candidate. File
presence/catalog metadata is not body activation. The candidate is not installed.
[Skills](https://learn.chatgpt.com/docs/build-skills) load descriptions first and
bodies on selection; large catalogs can truncate descriptions or omit entries.
Front-load the intended mission-state trigger and test exact source loading before
any future behavioral attribution. Do not compensate by loading every skill.

[Native subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
provide separate work contexts and collect results; their own model/tool work adds
tokens. At inspected Codex commit c4017a87,
[multi_agents_v2/spawn.rs](https://github.com/openai/codex/blob/c4017a87aacc7558002b7cb510025e967c1d765e/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs)
parses fork modes/model configuration and delegates lifecycle to agent_control.
[compact.rs](https://github.com/openai/codex/blob/c4017a87aacc7558002b7cb510025e967c1d765e/codex-rs/core/src/compact.rs)
handles history replacement, initial-context reinjection and compaction events.
This source is current upstream, not proof of the exact installed binary build.

[App-server](https://learn.chatgpt.com/docs/app-server) exposes thread history,
approvals/events and compaction. The [Agents API](https://developers.openai.com/api/docs/guides/agents-api/architecture)
is a separate hosted-harness integration with application/environment responsibilities.
Neither requires AMC to implement another session engine. API
[compaction](https://developers.openai.com/api/docs/guides/compaction) is platform
context management; it does not prove that a saved project PASS is still valid.

[Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
requires matching eligible rendered prefixes. Preserve stable instructions and
append bounded work; fewer bytes alone do not prove cheaper execution, and compaction
can change cache reuse. Do not change host caching/config or add padding in this task.
[Native usage](https://developers.openai.com/api/docs/guides/agents-api/observability)
can distinguish root and child work; local rollout telemetry is used here instead
of assuming API billing applies to this ChatGPT-authenticated run.

[Evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
requires evidence to justify multi-agent complexity. Reuse the 19-run corpus, keep
its false negatives and attribution limits visible, and do not count ten source
interpretations as ten executed engineering tasks. No new end-to-end runs are
needed to accept this narrower reviewed candidate; superiority remains unproved.
