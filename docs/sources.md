# Sources and what AMC actually reuses

Agent Mission Control (AMC) is a small Markdown workflow for a coding-agent host. It
borrows **ideas**, then implements them as its own short rules. It does not bundle,
copy, install, or depend on the source projects' code, services, agents, databases,
schedulers, or model APIs. The runtime is [SKILL.md](../SKILL.md) plus the linked
reference files below. Evidence grades, mechanism comparison and actor notes are in
[field state](field-state.md). Pins and limits also live in the
[research basis](research-basis.md) and [provenance record](../references/provenance.md).

Grade: **A** peer-reviewed or controlled study · **B** preprint/lab · **C** official
docs · **D** repo/practitioner · **E** AMC decision. Grades are not quality scores.

| Source | Grade | Adapted mechanism in AMC | Where it runs |
| --- | --- | --- | --- |
| Local Context Diamond | D | Only split genuinely independent work; exclusive files; lead integrates. | [routing](../references/packets.md) |
| Local AVO and [NVIDIA AVO](https://arxiv.org/abs/2603.24517) | D / B | Frozen evaluator, recoverable baseline, failed-attempt notes. Ordinary long work uses milestones. | [optimization](../references/optimization.md) |
| [Microsoft SkillOpt](https://github.com/microsoft/SkillOpt/tree/79124b37e9a6371e13b753f8bcd7adb1e493ade1), local Sleep | B / D | Train/selection/holdout; no live adoption. | [learning](../references/learning.md) |
| Local Sleep-Learned and continuous-learning-v2 | D | Observations are data, never automatic policy. | [learning](../references/learning.md) |
| [Untrivial](https://github.com/Untrivial-ai/agent-orchestrator/tree/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6) | D | Reconcile mission record with files; no overlapping replacement writers. | [resume](../references/resume.md) |
| [donvito](https://github.com/donvito/codex-astra-luna-orchestrator/tree/575e74ebcf9b199513151a8996665a71cf64ce50) | D | Choose available model/effort for a bounded job; keep lead ownership. | [routing](../references/packets.md) |
| Local verification-loop, security-review and deployment-patterns | D | Task-specific checks and risk-driven independent review. | [verification](../references/verification.md) |
| Local strategic-compact | D | Preserve milestone, artifact, failed approach, next action. | [resume](../references/resume.md) |
| [OpenAI skills](https://developers.openai.com/codex/skills), [subagents](https://developers.openai.com/codex/subagents), [config](https://developers.openai.com/codex/config-reference) | C | Use the host; do not recreate it. | [SKILL.md](../SKILL.md) |
| [Anthropic long-running](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [effective agents](https://www.anthropic.com/engineering/building-effective-agents) | C | Recoverable progress and selective context. A specialist may follow a named earlier artifact. Parallel fan-out waits for independent jobs. Parallel writers need host isolation. Orchestrator-worker is not the default. Rechecked 2026-09-23. | [routing](../references/packets.md), [resume](../references/resume.md) |
| [Kim et al., Nature MMI 2026](https://www.nature.com/articles/s42256-026-01268-y) | A | Cautious sequential default for coding-like work; fan-out when independent; centralize material review. n=20 SWE/Terminal subsets; fixed topologies. | [routing](../references/packets.md) |
| AMC cost-aware delegation policy | E | Break-even preflight, worker/retry/reviewer ceilings, compact artifacts, optional intent profiles. Not a claim that AMC is cheaper. | [resources](../references/resources.md#cost-aware-delegation), [profiles](../examples/profiles.md) |

## What is deliberately absent

AMC has no always-on supervisor, fixed team shape, mandatory optimizer loop,
learning daemon, graph database, custom context store, transcript collection,
billing system, automatic adoption, or four exclusive modes. Companion skills
must not take turns owning the task. Named host models are optional profile
examples, not the core definition. Context packs are an information boundary,
**not** a security sandbox; parallel writers need host isolation.

This is a design synthesis, not an endorsement or a claim that source benchmarks
transfer to your project. Skills and MCP are complementary, not ranked. Use the
[resource checkpoint](../references/resources.md) when real telemetry exists;
unknown numbers stay unknown.

## Same-class vs other-class sources

Frameworks and SDKs constrain design by showing what AMC **cannot** implement as
a skill. They are not competitors in the same product class.

| Source | Grade | Constraint |
|---|---|---|
| [Google ADK](https://google.github.io/adk-docs/graphs/) | C | Code graphs and coordinator/subagents are a framework, not a portable skill. |
| [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/) | C | Successor to AutoGen/Semantic Kernel; workflows, HITL, MCP, tracing. |
| [LangGraph](https://docs.langchain.com/oss/python/langgraph/use-graph-api) | C | Checkpointers and interrupts need a runtime. |
| [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents) / [sandbox agents](https://developers.openai.com/api/docs/guides/agents/sandboxes) | C | Harness vs compute; tracing lives in the SDK. |
| [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) | C | Loop in-process; Managed Agents is hosted. |
| [Harness Engineering](https://arxiv.org/abs/2609.00006) | B | Production harnesses are hand-rolled. Skills 9/11 and MCP 8/11 is adoption, not quality. |
| [Same model, different harness](https://arxiv.org/abs/2608.26218) | B | Host context policy can move SWE-bench scores with frozen weights. |
| [Collaboration tax](https://arxiv.org/abs/2608.22152) | B | Two-agent coordination has a capability-dependent cost. |
| [METR time horizons](https://metr.org/time-horizons/) | A/lab | Scaffolding rots as horizons grow. |
| [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) | D | A tiny loop remains competitive on SWE-bench Verified. |
| [Cursor worktrees](https://cursor.com/docs/configuration/worktrees) / [Cloud Agents](https://cursor.com/docs/cloud-agent) | C | Writer isolation is a checkout or a VM. |
| [obra/superpowers](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797), [github/spec-kit](https://github.com/github/spec-kit) | D | Popular procedures; not SWE-bench evidence for always-on MAS. |
| [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode/tree/5281b19e0d64f8e6dc6767f2130299a88af2dc71) | D | Host adapters and limited concurrency; not “team mode” as a universal default. |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow/tree/14c9d44440780e63563e935046db8708e121a5b1) | D | Resource limits and compact handoffs; not their runtime. |
| [wshobson/agents](https://github.com/wshobson/agents/tree/4236bb91f8395b0435f1d8b8baf9e8e4c69a8620) | D | Capability routing idea; not their model hierarchy as a benchmark. |
| [mikeyobrien/ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator/tree/edc2b3268c9bd0c08a12c8193a7ace7ab2789261) | D | Stop conditions and fail-closed checks; not an autonomous loop without an end. |
