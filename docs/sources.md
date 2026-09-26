# Sources and what AMC actually reuses

Agent Mission Control (AMC) is a small Markdown workflow for a coding-agent host. It
borrows **ideas**, then implements them as its own short rules. It does not bundle,
copy, install, or depend on the source projects' code, services, agents, databases,
schedulers, or model APIs. The runtime is [SKILL.md](../skills/agent-mission-control/SKILL.md) plus the linked
reference files below. Evidence grades, mechanism comparison and actor notes are in
[field state](field-state.md). Pins and limits also live in the
[research basis](research-basis.md) and [provenance record](../skills/agent-mission-control/references/provenance.md).

Grade: **A** peer-reviewed or controlled study · **B** preprint/lab · **C** official
docs · **D** repo/practitioner · **E** AMC decision. Grades are not quality scores.

| Source | Grade | Adapted mechanism in AMC | Where it runs |
| --- | --- | --- | --- |
| Author's local Context Diamond skill (not published here) | D | Only split genuinely independent work; exclusive files; lead integrates. | [routing](../skills/agent-mission-control/references/packets.md) |
| Author's local AVO skill (not published here) and [NVIDIA AVO v1](https://arxiv.org/abs/2603.24517v1) (2026-03-25) | D / B | Only where a measurable evaluator is frozen: baseline, candidate lineage, failed attempts and bounded next hypotheses. Ordinary long work uses milestones. NVIDIA's kernel results are domain evidence, not an AMC outcome claim. | [optimization](../skills/agent-mission-control/references/optimization.md) |
| [Microsoft SkillOpt](https://github.com/microsoft/SkillOpt/tree/79124b37e9a6371e13b753f8bcd7adb1e493ade1), the author's local Sleep skill (not published here) | B / D | Train/selection/holdout; no live adoption. | [learning](../skills/agent-mission-control/references/learning.md) |
| The author's local Sleep-Learned skill (not published here) and a locally modified ECC-origin continuous-learning-v2 skill | D | Observations are data, never automatic policy. | [learning](../skills/agent-mission-control/references/learning.md) |
| Agent Orchestrator: inspected upstream pin [15e9ea97](https://github.com/Untrivial-ai/agent-orchestrator/tree/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6), requested fork pin [63a04f0](https://github.com/byensitmagnus/agent-orchestrator/tree/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03) | D | Reconcile mission record with observed files; avoid overlapping replacement writers. Its daemon/worktree behavior is host product behavior, not something Markdown can enforce. | [resume](../skills/agent-mission-control/references/resume.md) |
| CALO: inspected upstream pin [575e74eb](https://github.com/donvito/codex-astra-luna-orchestrator/tree/575e74ebcf9b199513151a8996665a71cf64ce50), requested fork pin [014b1d7](https://github.com/byensitmagnus/codex-astra-luna-orchestrator/tree/014b1d7c48c39087beec8aa4f1ca022053ac17b3) | D | Choose available model/effort for a bounded job; keep lead ownership and mappings optional. Presets do not prove better quality or lower cost. | [routing](../skills/agent-mission-control/references/packets.md) |
| ECC-origin verification-loop, security-review and deployment-patterns skills as installed on the author's machine | D | Task-specific checks and risk-driven independent review. | [verification](../skills/agent-mission-control/references/verification.md) |
| ECC-origin strategic-compact skill as installed on the author's machine | D | Preserve milestone, artifact, failed approach, next action. | [resume](../skills/agent-mission-control/references/resume.md) |
| [OpenAI skills](https://developers.openai.com/codex/skills), [subagents](https://developers.openai.com/codex/subagents), [config](https://developers.openai.com/codex/config-reference) | C | Use native skill/subagent facilities; descriptions identify the coding task and boundary. Specialists are optional; parallel writers need host isolation. Rechecked 2026-09-24. | [SKILL.md](../skills/agent-mission-control/SKILL.md) |
| [Anthropic long-running](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [effective agents](https://www.anthropic.com/engineering/building-effective-agents) | C | Recoverable progress and selective context. Use a specialist where expertise or fresh context helps; pass required upstream artifacts only for real dependencies. Parallel fan-out waits for independent jobs; parallel writers need host isolation. Orchestrator-worker is not the default. Rechecked 2026-09-24. | [routing](../skills/agent-mission-control/references/packets.md), [resume](../skills/agent-mission-control/references/resume.md) |
| [Kim et al., Nature MMI 2026](https://www.nature.com/articles/s42256-026-01268-y) | A | Cautious sequential default for coding-like work; fan-out when independent; centralize material review. n=20 SWE/Terminal subsets; fixed topologies. | [routing](../skills/agent-mission-control/references/packets.md) |
| AMC cost-aware delegation policy | E | Break-even preflight, worker/retry/reviewer ceilings, compact artifacts, optional intent profiles. Not a claim that AMC is cheaper. | [resources](../skills/agent-mission-control/references/resources.md#cost-aware-delegation), [profiles](../examples/profiles.md) |
| [Google ADK 2.0 graph workflows](https://adk.dev/graphs/) | C | Runtime nodes/edges express workflow control and artifact flow; AMC uses this only for real execution dependencies in the lead's plan. It does not imply a persistent knowledge graph or justify adding a graph runtime. Rechecked 2026-09-24. | [field state](field-state.md#mechanism-comparison) |
| [Claude-Cortex](https://github.com/NickCrew/Claude-Cortex/tree/bb47af79ad3befe01ae01940fcf5f16e30a1b6df) | D | Adapt independent scrutiny of complex claims and bounded repair: the author's own assessment is insufficient; the lead accepts after evidence and findings are resolved. Repeated failure prompts diagnosis of that slice while other authorized work continues. Pin rechecked 2026-09-24. This is AMC's adaptation, not a measured quality gain. | [verification](../skills/agent-mission-control/references/verification.md#complex-slices) |
| [obra/superpowers](https://github.com/obra/superpowers/tree/8ca22dba9a94f28898bbce59f2537ff4d87c747d) `verification-before-completion` and `requesting-code-review` (MIT) | D | Release gate: a table of excuses that do not change the verdict, and a read-only reviewer briefed with the requirement, diff and check output, never the session history. Paraphrased, not copied. Checked 2026-09-26. | [SKILL.md](../skills/agent-mission-control/SKILL.md) |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices), [skill authoring](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [Google ADK patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/), [OpenAI agent guide](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | C | The author does not grade its own work. A separate critic or a person approves irreversible, high-stakes steps. Fragile operations get fixed steps, with more detail for small models. Checked 2026-09-26; not measured in AMC. | [SKILL.md](../skills/agent-mission-control/SKILL.md) |

## What is deliberately absent

AMC has no always-on supervisor, fixed team shape, mandatory optimizer loop,
standing implement/review/test/lint pipeline, skill-recommendation daemon,
learning daemon, graph database, custom context store, transcript collection,
billing system, automatic adoption, or four exclusive modes. Companion skills
must not take turns owning the task. Named host models are optional profile
examples, not the core definition. Context packs are an information boundary,
**not** a security sandbox; parallel writers need host isolation.

The repository mechanisms above were inspected at their exact pinned snapshots.
At the 2026-09-24 audit, AO upstream `main` was `96f2b39` and CALO upstream
`main` was `30b7d0b`; these newer heads were observed but not inspected, so no
behavioral claim is inferred from them. This is a design synthesis, not an
endorsement or a claim that source benchmarks transfer to your project. Skills
and MCP are complementary, not ranked. Use the
[resource checkpoint](../skills/agent-mission-control/references/resources.md) when real telemetry exists;
unknown numbers stay unknown.

## Same-class vs other-class sources

Frameworks and SDKs constrain design by showing what AMC **cannot** implement as
a skill. They are not competitors in the same product class.

| Source | Grade | Constraint |
|---|---|---|
| [Google ADK 2.0](https://adk.dev/graphs/) | C | Code graphs express runtime workflow control and artifact flow. That is a framework, not a portable skill. AMC records only real execution dependencies in its lead-owned plan; rechecked 2026-09-24. |
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
