# Sources and what AMC actually reuses

Agent Mission Control (AMC) is a small Markdown workflow for a coding-agent host. It
borrows **ideas**, then implements them as its own short rules. It does not bundle,
copy, install, or depend on the source projects' code, services, agents, databases,
schedulers, or model APIs. The runtime is [SKILL.md](../SKILL.md) plus the linked
reference files below. The detailed, dated evidence and source pins are in the
[research basis](research-basis.md) and [provenance record](../references/provenance.md).
The 15 September 2026 [source audit](source-audit-2026-09-15.md) checks every
row below against extra papers, host docs, other repos and 2025–2026 trends.

| Source | Adapted mechanism in AMC | Where it runs |
| --- | --- | --- |
| Local Context Diamond | Only split genuinely independent work; give each owner a small task packet and exclusive files; lead integrates. | [routing](../references/packets.md) |
| Local AVO and [NVIDIA AVO paper](https://arxiv.org/abs/2603.24517) | For measurable improvement, keep a recoverable baseline, freeze the evaluator, record attempts, and reconsider after stagnation. Ordinary long work uses visible milestones instead. | [optimization](../references/optimization.md) |
| [Microsoft SkillOpt](https://github.com/microsoft/SkillOpt/tree/79124b37e9a6371e13b753f8bcd7adb1e493ade1), local Sleep | For empirical learning, separate candidate changes from selection and held-out tests; stage a lesson for review. Ordinary maintenance uses source and engineering checks. | [learning](../references/learning.md) |
| Local Sleep-Learned and continuous-learning-v2 | Treat observations as evidence with limits, never as automatic policy. | [learning](../references/learning.md) |
| [Untrivial](https://github.com/Untrivial-ai/agent-orchestrator/tree/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6) | Reconcile a mission record with current files and agent state; avoid overlapping replacement writers. | [resume](../references/resume.md) |
| [donvito](https://github.com/donvito/codex-astra-luna-orchestrator/tree/575e74ebcf9b199513151a8996665a71cf64ce50) | Choose available model/effort for a bounded job when the host supports it; keep lead ownership. | [routing](../references/packets.md) |
| Local verification-loop, security-review and deployment-patterns | Use task-specific checks, baselines, rollback evidence and risk-driven independent review. | [verification](../references/verification.md) |
| Local strategic-compact | Preserve the milestone, artifact, failed approach and next action before interruption. | [resume](../references/resume.md) |
| [OpenAI skills](https://developers.openai.com/codex/skills), [subagents](https://developers.openai.com/codex/subagents), [config](https://developers.openai.com/codex/config-reference) | Use the host's native skills, agents, permissions and settings rather than recreate them. | [SKILL.md](../SKILL.md) |
| [Anthropic long-running work](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Google's scaling study](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) and [Kim et al., Nature Machine Intelligence 2026](https://www.nature.com/articles/s42256-026-01268-y) | Keep progress recoverable, return distilled findings, and add coordination only where the task can benefit. On coding-adjacent SWE-bench Verified cells, extra agents did not beat a single agent. | [routing](../references/packets.md), [resume](../references/resume.md) |

## What is deliberately absent

AMC has no always-on supervisor, fixed team shape, mandatory optimizer loop,
learning daemon, custom context database, transcript collection, billing system,
automatic adoption, or four exclusive modes. Companion skills must not take turns
owning the task. Named host models are optional profile examples, not the core
definition. These systems add coordination, privacy, maintenance, or evaluation
cost without helping routine work. Context packs are an information
boundary, **not** a security sandbox; the host's permissions still matter.

This is a design synthesis, not an endorsement or a claim that source benchmarks,
model rankings, savings, or compatibility transfer to your project. Use the
[resource checkpoint](../references/resources.md) when real budget or telemetry
exists; unknown numbers stay unknown.

## Also consulted 15 September 2026

These sources were checked in the [source audit](source-audit-2026-09-15.md).
They are not extra installations.

| Source | Why it constrains AMC |
|---|---|
| [Harness Engineering](https://arxiv.org/abs/2609.00006) | Production coding agents are a model plus a hand-rolled harness, not a guest skill plus a framework. |
| [Same model, different harness](https://arxiv.org/abs/2608.26218) | Host context policy can move SWE-bench scores with frozen weights. |
| [The Collaboration Tax](https://arxiv.org/abs/2608.22152) | Two-agent coordination has a measurable, capability-dependent cost. |
| [METR time horizons](https://metr.org/time-horizons/) | Longer autonomous tasks make last year's scaffolding rot. |
| [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) | A tiny loop remains competitive on SWE-bench Verified. |
| [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) | Subagents isolate overflow context; they are not a default team. |
| [OpenAI Astra skills blog](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Too many long skill descriptions get truncated and over-trigger. |
| [obra/superpowers](https://github.com/obra/superpowers), [github/spec-kit](https://github.com/github/spec-kit) | Popular SDD/spec workflows; not coding-benchmark evidence for always-on MAS. |
| [Cursor worktrees](https://cursor.com/docs/configuration/worktrees) / [Cloud Agents](https://cursor.com/docs/cloud-agent) | Writer isolation is a checkout or a VM. |
