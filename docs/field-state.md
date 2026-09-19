# Field state and evidence model

Accessed 2026-09-19. AMC is a **portable Markdown skill** for a coding-agent
host. It is not a runtime, framework, optimizer service, desktop OS or hosted
project coordinator.

This file classifies sources, compares mechanisms (not brands), and records
what AMC takes. It does not prove that AMC improves quality, price or speed.

Canonical claims, origin, enforcement and outcome live in
[claim-ledger.md](claim-ledger.md). Do not duplicate those entries here.

## Evidence grades

| Grade | Meaning | May justify | Must not be treated as |
|---|---|---|---|
| **A** | Peer-reviewed paper or a documented controlled study with stated method and limits | A bounded design rule for a similar task type | A guarantee on AMC's hosts or issues |
| **B** | Preprint or lab report with method and limits | A cautious design hypothesis | Established universal research |
| **C** | Official product documentation or a vendor engineering report | How that host/SDK actually works | A coding-quality ranking |
| **D** | Repository observation or practitioner note | An implementable pattern, with its failure modes | A measured outcome gain |
| **E** | AMC product decision or hypothesis | The local rule, labelled as ours | External evidence |

A paper result, a vendor recommendation, a trend and an AMC rule are different
kinds of claim. None is silently promoted to another.

**Claim axes** (independent; see [claim-ledger.md](claim-ledger.md)):

| Axis | Values | Use |
|---|---|---|
| Origin | primary_source · reasoned_inference · local_observation | Where the mechanism came from |
| Enforcement | instruction_only · validator_enforced · host_enforced · externally_attested | What actually binds |
| Outcome | not_verified · observed · repeatedly_observed | What we have seen happen |

Grades A–E measure source quality. They are not outcome status. A green
validator is deterministic contract proof, not behavioral proof.

**Confidence** on an AMC rule: **high** = source and product class match;
**medium** = source is adjacent or limited; **low** = local conservative choice.

## Product classes

| Class | What it is | Examples | AMC relation |
|---|---|---|---|
| Host / harness | Model loop, tools, permissions, context compaction | Codex, Claude Code, Cursor, Gemini CLI | AMC is a guest here |
| Runtime SDK | Library that runs the agent loop in your process | [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents), [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) | Out of class |
| Framework | Code-defined graphs, sessions, middleware | [Google ADK](https://google.github.io/adk-docs/graphs/), [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/), [LangGraph](https://docs.langchain.com/oss/python/langgraph/use-graph-api) | Out of class |
| Desktop orchestrator | Daemon, worktrees, live UI | Agent Orchestrator | Out of class |
| Hosted coordinator | Cloud threads, shared project memory, vendor UI | [Claude Code Projects](https://code.claude.com/docs/en/claude-projects) | Out of class |
| Optimizer / learner | Offline search over instructions or kernels | NVIDIA AVO, Microsoft SkillOpt, Karpathy autoresearch | Offline only |
| Portable skill | Loaded text plus optional scripts | AMC, Superpowers, Spec Kit | AMC's class |

Do not compare AMC to ADK, LangGraph or Agent Framework as if they shipped the
same product.

## Mechanism comparison

What each system can **enforce in code** versus what AMC can **ask a host to do**.

| Mechanism | Hosts (Codex / Claude Code / Cursor) | ADK / Agent Framework / LangGraph | AO | CALO | Superpowers / Spec Kit | AMC as a skill |
|---|---|---|---|---|---|---|
| Single-agent default | Native loop | Supported; MS docs: use a function if a function suffices | Workers are first-class | Role files still run in Codex | Superpowers prefers process skills first | Cautious default for sequential coding |
| Multi-agent | Optional subagents; extra tokens | First-class graphs and orchestrations | Always-on workers | Named roles | SDD: implementer+review per task if chosen | Sequential specialist allowed; fan-out only for independent jobs |
| Execution graph | Implicit in the lead | Code DAG / checkpointed graph | Session board | Prompt roles | Plan file + SDD | Dynamic dependencies in the lead; no graph DB |
| Context selection | Host compaction; skills progressive disclosure | Session state, context providers | Workspace files | Profile text | Skill load-before-action | Selective packets; over-compression loses facts |
| Persistent state / resume | Host session + git | Checkpointers, workflow resume, hosted event logs | Daemon + worktrees | Codex session | Plan/todo files | Compact mission record; reconcile before trust |
| Model routing | Native model/effort | Router functions, per-node models | Adapter-dependent | Explicit role pins | Model hints in SDD | Capability classes; host maps names |
| Writer isolation | Worktrees, sandbox, Cloud VMs | Sandbox clients, branch context — still code, not magically exclusive files | Implemented worktrees | Relies on Codex | Worktree skill | **Ask the host**; serialize if unavailable |
| Verification | User + tests | Guardrails, graph nodes | Auto-review service | Reviewer role | Per-task review in SDD | Risk-based independent review; lead accepts |
| Observability | Host traces/UI | Built-in tracing (OpenAI SDK default on), middleware | Live board | Token notes | Session text | Mission fields; no AMC tracer |
| Human-in-the-loop | Host approvals | Interrupts, HITL nodes, Managed Agents | Desktop | Host | User partner | Authority/stop rules; host owns the dialog |
| Offline learning | None built in | Eval services optional | None | None | None | SkillOpt-like split, never mid-run |
| MCP / tools | Host MCP + skills | MCP clients in the SDK/framework | Host tools | Codex | Skills | Use host tools; skills ≠ MCP |

Skills and MCP solve different problems: skills are procedural instructions with
progressive disclosure; MCP is a tool/protocol surface. They can be complementary.
A harness source-audit that counted skills in 9/11 systems and MCP in 8/11 is an
**adoption count (B, abstract)**, not a quality result and not “skills beat MCP”.

## What AMC takes and rejects

| Mechanism | Source (grade) | AMC takes | AMC rejects | Confidence |
|---|---|---|---|---|
| Direct sequential coding as default | Kim et al. Nature MMI 2026 (**A**); Anthropic effective-agents 2024-12-19 (**C**) | Stay with the lead on understood dependent work | “Multi-agent never helps”; a live 45% classifier | high for sequential coding, medium elsewhere |
| Sequential specialist isolation | Anthropic orchestrator-workers (**C**); OpenAI subagents (**C**); AMC Truth Layer (**E**) | Bounded sequential jobs for specialization or context isolation | Independence required for every delegated job | high for the split, low for payoff |
| Parallel fan-out only if independent | Local Context Diamond (**D**); Nature Finance +80.8% vs PlanCraft −39..−70% (**A**) | Exclusive scopes; lead integrates | Fixed team; always-on SDD | high |
| Central verification | Nature independent error amp ~17× vs centralized ~4× (**A**) | Lead acceptance; review when material | Swarm of unchecked writers | high |
| Host isolation for parallel writers | OpenAI subagents (**C**); Cursor worktrees / Cloud Agents (**C**); AO worktrees (**D**) | Require host isolation or serialize | Prompt-scope as a sandbox | high |
| Selective context | Anthropic context engineering (**C**); OpenAI skills / Astra blog (**C**) | Task packets; load references on need | Dumping the skill library; word-count as quality | high |
| Durable progress | Anthropic long-running harness (**C**); OpenAI exec plans (**C**) | Mission record + reconcile | Custom context DB; required initializer agent | high |
| Orchestrator-worker when subtasks are unpredictable | Anthropic effective-agents (**C**) | Native subagents for that shape, still lead-owned | Copying orchestrator-worker as the default coding topology | medium |
| Frozen evaluator | NVIDIA AVO (**B**); local AVO (**D**) | Only when a score exists | Everyday coding as AVO | high |
| Offline learning split | SkillOpt (**B**); Sleep (**D**) | Train/select/holdout; no auto-adopt | Mid-run skill rewrite | high |
| Capability routing | RouteLLM (**B**); OpenAI subagent effort notes (**C**); CALO (**D**) | Classes, not frozen model names | Obligatory Astra/Luna pairing | medium |
| Delete stale scaffolding | Managed Agents 2026-04-08 (**C**); Astra skills blog 2026-09-11 (**C**); METR horizons (**A**/lab) | Prefer fewer rules over time | Last year's ceremony as a team | medium |
| Cost with accuracy | AI Agents That Matter (**B**); OpenAI eval guidance (**C**) | Unknown prices stay unknown | Homemade superiority farms | high |
| Cost-aware delegation | Nature finance vs sequential (**A**); Anthropic research-system tokens (**C**); OpenAI subagent guidance (**C**); AMC policy (**E**) | Break-even preflight, artifact handoff, worker/retry/reviewer ceilings, optional intent profiles | Strong-lead/cheap-worker as identity; star counts as quality or price proof | medium |

## Actors checked this pass

Official docs unless noted. Dates are page access 2026-09-15 unless a later
fetch is named.

### OpenAI (**C**, except eval paper grades)

- [Skills](https://developers.openai.com/codex/skills), [plugins](https://developers.openai.com/codex/plugins), [subagents](https://developers.openai.com/codex/subagents), [config](https://developers.openai.com/codex/config-reference)
- [Agents SDK](https://developers.openai.com/api/docs/guides/agents): harness vs compute; [sandbox agents](https://developers.openai.com/api/docs/guides/agents/sandboxes) (beta); [tracing](https://openai.github.io/openai-agents-python/tracing/) default on
- [Eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), [exec plans](https://developers.openai.com/cookbook/articles/codex_exec_plans)
- [Astra skills blog](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) 2026-09-11: short descriptions, progressive disclosure, stale AGENTS.md overconstrains stronger models

Codex spawns subagents when asked; extra tokens; default depth 1; caution parallel writers. Skills are loaded text. The Agents SDK is a different product class from AMC.

### Anthropic (**C**)

- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) 2024-12-19: start simple; add complexity when measured; **orchestrator-workers** for complex work whose subtasks cannot be predicted (coding across unknown files is their example); evaluator-optimizer needs real criteria
- [Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [long-running harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [Managed Agents](https://www.anthropic.com/engineering/managed-agents) 2026-04-08, [multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents): overflow context, not a default team
- [Claude Code Projects](https://code.claude.com/docs/en/claude-projects) fetched 2026-09-19: hosted coordinator; cloud threads; VM + own branch; project memory vs CLAUDE.md; 200 threads/day hard cap; public beta Pro/Max. Soft: routing judgment, memory drafts. Hard: VM, branch, thread cap, skip-permissions. **Out of AMC class.**
- [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview): loop in your process; Managed Agents is hosted

The multi-agent research system reported a higher internal research score with
an Opus lead and Sonnet workers, at about 15× the tokens of ordinary chat, and
notes that most coding tasks have fewer truly parallel subtasks. That is cost
structure, not a claim that AMC is cheaper.

Do not quote Anthropic as “never orchestrate”. They document both the cost of complexity and a legitimate orchestrator-worker pattern.

### Google (**A** paper + **C** ADK)

- Kim et al., *Capable language models can outgrow the benefits of collaboration*, [Nature Machine Intelligence](https://www.nature.com/articles/s42256-026-01268-y) 8, 1157–1172 (2026), DOI [10.1038/s42256-026-01268-y](https://doi.org/10.1038/s42256-026-01268-y). Preprint [arXiv:2512.08296](https://arxiv.org/html/2512.08296) HTML v3.
  - 260 configs, six benchmarks, matched tools/prompts/compute, five topologies.
  - SWE-bench Verified and Terminal-Bench: **20-instance subsets** (Verified: seed-42 shuffle of 500). Bootstrap CIs are wide.
  - Tested **fixed** SAS / independent / centralized / decentralized / hybrid topologies, not host-native coding harnesses.
  - Nature SWE-bench Verified: all MAS slightly worse than SAS (independent −12.8%). ~45% is a **selection rule**, not a coefficient that survived cluster-robust correction.
- [ADK 2.0](https://google.github.io/adk-docs/2.0/) (Python GA 2026-05-19): graph workflows, dynamic workflows, collaborative coordinator/subagents. A **framework**, not a skill.

### Microsoft (**B** SkillOpt + **C** Agent Framework)

- [Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/): successor to AutoGen and Semantic Kernel; agents, harness agent, graph workflows, MCP, checkpointing, HITL. “If you can write a function, do that instead of an agent.”
- SkillOpt [arXiv:2605.23904](https://arxiv.org/abs/2605.23904) v2; pin [79124b37](https://github.com/microsoft/SkillOpt/tree/79124b37e9a6371e13b753f8bcd7adb1e493ade1)
- OEO [arXiv:2608.09629](https://arxiv.org/abs/2608.09629) v1

### NVIDIA (**B**)

- AVO [arXiv:2603.24517](https://arxiv.org/abs/2603.24517) v1 2026-03-25; ARC-AGI-3 [blog](https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/) 2026-08-21. No published same-compute baseline agent. Transfer to ordinary software tasks is invalid without a frozen evaluator.

### Karpathy (**D**)

- [autoresearch](https://github.com/karpathy/autoresearch) commit `228791f` (MIT, 2026-03-09): one editable surface, frozen eval, one metric, keep/discard, fixed time budget. Evidence for measurable optimizer loops, not for general-purpose agent swarms.

### Open-source frameworks and coding harnesses

- [LangGraph](https://docs.langchain.com/oss/python/langgraph/use-graph-api) (**C**): StateGraph, checkpointers, interrupts/HITL. Code persistence, not a skill.
- [Harness Engineering](https://arxiv.org/abs/2609.00006) (**B**, abstract): 11 production coding harnesses; none imported a general agent framework; none used vector retrieval for code. Skills 9/11, MCP 8/11 — adoption, not quality.
- [Same model, different harness](https://arxiv.org/abs/2608.26218) (**B**, abstract): tight-window Verified F2PF 28%→49% with frozen weights.
- [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) (**D**): ~100-line bash loop; reported >74% SWE-bench Verified with recent models.
- Cursor [worktrees](https://cursor.com/docs/configuration/worktrees) / [Cloud Agents](https://cursor.com/docs/cloud-agent) (**C**)
- [obra/superpowers](https://github.com/obra/superpowers) plugin v6.1.1 / pin [b36e082](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797) (**D**): SessionStart hook injects bootstrap; SDD = fresh implementer + spec-reviewer + two-stage review if chosen; `verification-before-completion` is instruction-only; worktree skill fails open. Vendor README says “proven techniques”; AMC does not treat that as outcome proof.
- [github/spec-kit](https://github.com/github/spec-kit) (**D**): specs, not a multi-agent runtime
- Agent Orchestrator pin [15e9ea97](https://github.com/Untrivial-ai/agent-orchestrator/tree/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6); comparison fork [63a04f0](https://github.com/byensitmagnus/agent-orchestrator/tree/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03) (**D**)
- donvito CALO pin [575e74eb](https://github.com/donvito/codex-astra-luna-orchestrator/tree/575e74ebcf9b199513151a8996665a71cf64ce50); fork [014b1d7](https://github.com/byensitmagnus/codex-astra-luna-orchestrator/tree/014b1d7c48c39087beec8aa4f1ca022053ac17b3) (**D**)

### Popular orchestrator repositories (**D**, snapshot 2026-09-15)

Star counts measure demand for coordination, not better code. Treat these as
practice examples. They are not research proof that AMC, or their workflows,
improve quality, price or speed.

The shared trend is isolated workspaces, fresh context per job, provider/model
routing, limited concurrency, persistent mission state, artifact handoffs,
risk-based or async review, and visible token/cost use. AMC should collect those
mechanisms. It should not take the products as dependencies.

| Project | Stars (popularity) | Pin | AMC takes | AMC does not copy |
|---|---|---|---|---|
| [Agent Orchestrator](https://github.com/Untrivial-ai/agent-orchestrator/tree/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6) | 12,056 | [15e9ea97](https://github.com/Untrivial-ai/agent-orchestrator/tree/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6) | Fact-based status, exclusive workspaces, isolation | Desktop app, daemon, always-on workers |
| [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode/tree/5281b19e0d64f8e6dc6767f2130299a88af2dc71) | 39,172 | [5281b19](https://github.com/Yeachan-Heo/oh-my-claudecode/tree/5281b19e0d64f8e6dc6767f2130299a88af2dc71) | Host adapters, role routing, limited concurrency | “Team mode recommended” as a universal default |
| [DeerFlow](https://github.com/bytedance/deer-flow/tree/14c9d44440780e63563e935046db8708e121a5b1) | 82,462 | [14c9d44](https://github.com/bytedance/deer-flow/tree/14c9d44440780e63563e935046db8708e121a5b1) | Resource limits, compact artifact handoffs | Gateway, database and runtime architecture |
| [Superpowers](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797) | 286,856 | [b36e082](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797) | Progressive disclosure, specialized workflows | Mandatory implementer/reviewer chain on small tasks |
| [wshobson/agents](https://github.com/wshobson/agents/tree/4236bb91f8395b0435f1d8b8baf9e8e4c69a8620) | 39,667 | [4236bb9](https://github.com/wshobson/agents/tree/4236bb91f8395b0435f1d8b8baf9e8e4c69a8620) | Capability routing, host profiles | Their model hierarchy as a documented benchmark |
| [Ralph Orchestrator](https://github.com/mikeyobrien/ralph-orchestrator/tree/edc2b3268c9bd0c08a12c8193a7ace7ab2789261) | 3,138 | [edc2b32](https://github.com/mikeyobrien/ralph-orchestrator/tree/edc2b3268c9bd0c08a12c8193a7ace7ab2789261) | Stop conditions, fail-closed checks | Autonomous loops without a clear end |
| [Astra–Luna Orchestrator](https://github.com/donvito/codex-astra-luna-orchestrator/tree/575e74ebcf9b199513151a8996665a71cf64ce50) | 1,336 | [575e74eb](https://github.com/donvito/codex-astra-luna-orchestrator/tree/575e74ebcf9b199513151a8996665a71cf64ce50) | Optional host mapping | Proof of better quality or lower price |

### Other papers

- RouteLLM [arXiv:2406.18665](https://arxiv.org/abs/2406.18665) (**B**)
- ACL 2024 error localization ([2024.findings-acl.826](https://aclanthology.org/2024.findings-acl.826/)) (**A**)
- AI Agents That Matter [arXiv:2407.01502](https://arxiv.org/abs/2407.01502) (**B**)
- Collaboration tax [arXiv:2608.22152](https://arxiv.org/abs/2608.22152) (**B**, abstract)
- METR time horizons ([metr.org/time-horizons](https://metr.org/time-horizons/), [Kwa et al.](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)) (**A**/lab; >16h measurements unreliable)

## Corrected claims

These statements were too strong in earlier AMC docs and are withdrawn:

1. **“Skills beat MCP.”** Not documented. Different jobs; complementary. 9/11 vs 8/11 is adoption.
2. **“Direct-first is a natural law.”** It is a cautious default for ordinary sequential coding. Nature still shows large MAS gains on decomposable finance-style work. Anthropic still documents orchestrator-workers for unpredictable complex subtasks.
3. **Google as a coding-host guarantee.** Keep n=20 SWE/Terminal subsets, fixed topologies, wide CIs, and “selection rule not scaling law” for ~45%.
4. **Vendor blogs and preprints as established universal research.** Grade them **B** or **C**.
5. **External sources as proof that AMC is better.** They can justify design. AMC quality, price and speed stay **NOT VERIFIED**.
6. **Agent-authored `docs/reviews/` as independent public review.** Same-lead engineering notes only.
7. **Popular orchestrator repos as research evidence.** Grade **D**. Stars show demand for coordination, not output quality.
8. **“Delegate only when independent.”** Too strict. Independence is required for parallel ready jobs. Sequential specialist isolation is a separate route (`sequential_delegated`).
9. **Claude Code Projects as an AMC feature or competitor in the same class.** Different product: hosted coordinator, not a portable skill.
10. **Superpowers “proven techniques” as AMC evidence.** Vendor language. Superpowers verification is instruction-only.

## AMC kernel mapping

Implemented in `SKILL.md` plus loaded references. Not in the runtime ZIP: this
file, history, evals.

| Kernel rule | Why it exists | Limit |
|---|---|---|
| One lead, adaptive graph | Host is the real harness (**C**); Markdown cannot enforce a DAG (**E**) | Agents can ignore the skill |
| Sequential default | Nature SWE subset (**A**) + Anthropic simplicity (**C**) | Not a ban on sequential specialists or fan-out |
| Sequential specialist | Anthropic orchestrator-workers (**C**); OpenAI subagents (**C**) | Extra hop is not a quality claim |
| Scout then decide | Context Diamond (**D**); information value vs cost (**E**) | Scout is not a team recruiter |
| Independent fan-out + host isolation | Diamond (**D**) + host isolation docs (**C**) + Nature error amp (**A**) | Isolation is the host's job |
| Risk-based review | Anthropic evaluator-optimizer (**C**); verification-loop (**D**) | Fresh context ≠ independent errors |
| Mission reconcile | Long-running harness (**C**); AO fact-derived status (**D**) | Schema PASS can still lie in prose |
| AVO only with evaluator | NVIDIA (**B**) | No score → milestones, not search |
| Learning offline | SkillOpt (**B**) | No Sleep from ordinary success |
| Cost-aware delegation | Nature/Anthropic/OpenAI (**A**/**C**) + local policy (**E**) | Not a claim that AMC is cheaper |

Local Context Diamond, AVO, SkillOpt/Sleep, verification-loop, security-review,
deployment-patterns and strategic-compact remain design sources. They are not
installed by AMC.

## What this file does not prove

AMC behavioral quality, cost, speed, host auto-activation and global adoption
remain **NOT VERIFIED**. The closed nine-run Codex comparison is a historical
negative: no unique candidate.9 win, Superpowers contamination on every arm.
See [candidate.9 postmortem](../evals/candidate.9/README.md).
