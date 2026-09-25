# Design sources and limits

AMC is an independent synthesis. These are design sources, not dependencies or
runtime instructions. Only mechanisms are paraphrased; no upstream code or
substantial text is copied. Local inspection on 2026-09-12 checked SkillOpt's MIT
license and Untrivial/donvito Apache-2.0 licenses. NVIDIA's publication is not an
open-source implementation license. Source mechanisms are not reproduced
benchmark gains or guaranteed AMC improvements.

| Source | Problem, mechanism and use in AMC | Cost, failure mode and boundary |
|---|---|---|
| Local Context Diamond | Dependency test, minimal context, exclusive ownership, fresh review and owner feedback; adapted in work routing | Useful independent work only; contexts/review add cost. Reject fixed fan-out and mandatory companion ownership. Native agents execute. |
| Local AVO and [NVIDIA AVO](https://arxiv.org/abs/2603.24517) | Execution feedback, recoverable incumbent, frozen evaluator, lineage and stagnation diagnosis; adapted in execution feedback and measured improvement | Candidate search requires an evaluator; long work can use observable milestones. Published system results do not isolate the mechanism. No supervisor daemon. |
| [Microsoft SkillOpt](https://github.com/microsoft/SkillOpt/tree/79124b37e9a6371e13b753f8bcd7adb1e493ade1) and local Sleep | `evaluation/gate.py`, `skillopt_sleep/cycle.py`, `staging.py`: score selection, train/selection/test separation, source pins and recoverable adoption; adapted in separate learning | Replay and held-out evaluation cost real work. Reject live adoption and instruction-density scoring. Source tests were inspected; execution unavailable here without pytest. No learner installed. |
| Local Sleep-Learned and continuous-learning-v2 | Scoped observations subordinate to evidence/current instructions; candidate lessons with activation and contradiction risk | No automatic promotion of memory to policy, global hooks or transcript collection. Domain-specific learned rules remain conditional. |
| [Untrivial Agent Orchestrator](https://github.com/Untrivial-ai/agent-orchestrator/tree/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6) | `SessionRecord.ControllerOwner`, fact-derived status, bounded workspace observation and retained ambiguity; adapted as current identity/evidence reconciliation and no overlapping replacement writer | Its launch generations, recovery database and worktree lifecycle serve its own runtime. AMC uses native lifecycle and Git; no copied daemon, scheduler, database or handoff saga. |
| [donvito Astra/Luna Orchestrator](https://github.com/donvito/codex-astra-luna-orchestrator/tree/575e74ebcf9b199513151a8996665a71cf64ce50) | Explicit model/effort role pins, short bounded jobs and lead integration; adapted in opt-in project examples | Role pins can defeat generic defaults; multi-file triggers can waste work. Reject obligatory role sequence and strongest-model review by default. |
| Local verification-loop, security-review and deployment-patterns | Change-specific executed proof, risk-triggered trust-boundary checks, actual artifact/runtime/data/rollback evidence | Domain implementation remains in relevant skills/native CI, scanners and release tools. Reject blanket stack checklists, new rollout infrastructure and a passing build as production proof. |
| [Claude-Cortex](https://github.com/NickCrew/Claude-Cortex/tree/bb47af79ad3befe01ae01940fcf5f16e30a1b6df) | README principle that the writer does not grade its own work, plus severity split and a hard stop; adapted as complex-slice acceptance in independent review. Pin `bb47af79`, observed 2026-09-22. Grade **D**. | Its CLI, TUI, Homebrew install, watch daemon and always-on code/test/lint loops are a different product. A different model family is not independent errors. No Cortex package is installed. |
| Local strategic-compact | Preserve semantic mission facts before context loss | Native host owns compaction/history. No AMC hook, transcript replica or custom context engine. |
| [OpenAI Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [Config](https://developers.openai.com/codex/config-reference) | Progressive disclosure, native roles, independent model/effort settings and host permissions; retain native execution | Source-level support is not a tested host compatibility matrix. Shared prompt/catalog overhead and account billing need actual telemetry. |

Relevant local implementations were read, including their source-level failure
modes and activation boundaries; unrelated advertising, document and business
skills were not imported. Other process skills were inventoried for overlap,
not activated automatically. Exact inspected anchors and evidence levels are
retained in the iteration's external mining reports. Historical source comparisons belong to repository development, not the
installed runtime.


## Research-guided maintenance (2026-09-13)

[OpenAI long-work guidance](https://developers.openai.com/cookbook/articles/codex_exec_plans)
and [Anthropic harness guidance](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
support recoverable incremental progress. [Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
supports focused work and distilled returns. [Google's scaling study](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
and the peer-reviewed [Kim et al. Nature Machine Intelligence paper](https://www.nature.com/articles/s42256-026-01268-y)
limit the case for unconditional delegation. [OEO](https://arxiv.org/abs/2608.09629)
provides qualified evidence for adapting procedure to optimizer capability, not
removing external constraints. [Field state](https://github.com/byensitmagnus/agent-mission-control/blob/main/docs/field-state.md) grades
those sources A–E and records extra harness, collaboration-tax, METR,
Superpowers, Spec Kit, ADK, Agent Framework, LangGraph and host-doc checks. These inform
AMC's design; no benchmark gains or universal model ranking transfer to this
skill. The whole-project research report is repository development material,
deliberately outside the installed runtime.
