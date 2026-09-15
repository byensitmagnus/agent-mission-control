# Source audit 15 September 2026

AMC should stay a **direct-first brake**, not a claim that extra agents, extra
skills or extra scaffolding make coding work better, cheaper or faster.

This audit inventories every source already named in this repository, adds
sources that were missing from that list, and records 2025–2026 trends. It
does not change `SKILL.md`. It is not a product-quality measurement.

## Method

| Item | Bound |
|---|---|
| Date | 2026-09-15 |
| Scope | Host docs, published papers, public repos and practitioner notes already cited here, plus extra sources that constrain the same design choice |
| Not in scope | New AMC subject-run farms, merge, release, install |
| Evidence kinds | A paper result, a vendor recommendation and an AMC rule are different. None is silently promoted to another |
| Verification | Primary pages and abstracts were fetched this pass unless a row says **abstract/search**. Nature Machine Intelligence was read from the journal page; the Google arXiv HTML v3 was read as the preprint |

Numbers below are the sources' numbers on their tasks. They do not transfer to
this repository's issues.

## Verdict for coding work

1. On software-engineering issue resolution, extra agents did not help in the
   controlled study AMC already cites. The peer-reviewed Nature version reports
   slight **degradation for every MAS topology** versus a single agent on a
   20-instance SWE-bench Verified subset.
2. Production coding agents are a **model plus a host harness**. Changing the
   harness changed results with frozen weights. A Markdown skill cannot replace
   that harness.
3. Skills beat extra orchestration as a packaging trend. Too many skills, and
   skills that over-trigger, hurt discovery.
4. Isolation that actually prevents overlapping writes is **worktrees, VMs or
   host permissions**, not a prompt scope.
5. Superpowers, Spec Kit and role-preset orchestrators are popular. Their
   default “always split / always review / always pin roles” is **not** what
   the coding evidence supports.

AMC's useful product stance: keep ordinary coding direct; add a scout, a
parallel worker or a reviewer only when the task is independent, the claim is
material, or the host can isolate writers.

## 2025–2026 trends

| Trend | What it is | What it is not | AMC take |
|---|---|---|---|
| Harness over framework | Eleven production coding harnesses were source-audited; none imported a general agent framework; none used vector retrieval for code. Skills shipped in 9/11, MCP in 8/11. | Proof that AMC is a harness. AMC is loaded text inside someone else's loop. | Do not grow a daemon, graph engine or RAG memory. |
| Same model, different harness | Tight-context treatment raised mean fail-to-pass on a 169-task SWE-bench Verified cohort from 28% to 49% without retuning weights. | Proof that AMC compaction text matches that treatment. | Host context policy dominates skill prose. |
| Simple loop still scores | mini-SWE-agent is ~100 lines of bash-in-a-loop and reports >74% on SWE-bench Verified with recent models. | Proof that tools or hosts are useless. It is a research baseline, not a desktop product. | Complexity must earn its keep. |
| Skills as the unit | OpenAI and Anthropic ship progressive disclosure. Willison (16 Oct 2025) argued skills may matter more than MCP. OpenAI (11 Sep 2026) now warns that too many long skill descriptions get truncated and over-trigger. | Proof that installing more skills improves outcomes. | Keep AMC one short router. Domain skills stay out of the kernel. |
| Isolation moves to the OS | Cursor worktrees / best-of-n, Cursor Cloud Agents (per-agent VMs), Agent Orchestrator worktrees, Claude background agents. | Proof that a skill can sandbox writers. | AMC must not claim exclusive files unless the host isolates them. |
| Subagents for overflow, not teams | Claude Code: use a subagent when a side task would flood the parent with logs/search. Codex: spawn when asked; extra tokens; default `max_depth` 1; caution parallel writers. | A mandate to run implementer+reviewer on every task. | Scout and review stay exceptions. |
| Stronger models retire scaffolding | Anthropic Managed Agents (8 Apr 2026): model-specific scaffolding goes stale. OpenAI Astra blog: recipes that helped weaker models now overconstrain. METR: 50% time horizon has been doubling on the order of months; measurements above 16 hours on the current suite are unreliable. | Proof that instructions are obsolete tomorrow. | Periodically delete rules. Do not add a fixed team because last year's model needed one. |
| Collaboration has a tax | Coordination can help parallel decomposable work and hurt sequential work. Independent MAS amplified trace errors ~17× versus ~4× with a central checker. A 2026 “collaboration tax” paper finds the tax falls with capability and is a conversational cascade, not a missing-reasoner problem. | A ban on all multi-agent use. Finance-style parallel research still gained ~+81%. | Default direct. Parallelize only independent packets. Centralize verification of material claims. |
| Fashionable SDD | Superpowers: if SDD is chosen, fresh implementer per task plus review. Spec Kit: specify/plan/tasks, little native multi-agent. High install counts are not coding benchmarks. | Evidence that mandatory subagent SDD beats a strong single agent on SWE-bench. | Do not copy always-on SDD. Keep explicit-procedure override when the user names Superpowers or Spec Kit. |
| Cost is part of quality | *AI Agents That Matter* (2024) and OpenAI eval guidance: do not add agent complexity without evidence; report cost with accuracy. | A requirement that AMC run its own farm. | No homemade research program. Unknown prices stay unknown. |

## Every source already in this repository

Columns: **Says** is the source. **AMC uses** is the adapted rule. **Must not take** is the overclaim.

### Local skills and companion repos

| Source | Says | AMC uses | Must not take |
|---|---|---|---|
| Local Context Diamond | Fan-out only if at least two jobs are genuinely independent; exclusive files; lead integrates. | Routing default and dependency test. | Fixed fan-out, mandatory companion ownership. |
| Local AVO | Improve a measurable target with a frozen evaluator and recoverable incumbent. | Optimization reference for scored search. | Everyday coding as an AVO loop. |
| Local Sleep, Sleep-Learned, continuous-learning-v2 | Observations are data. Held-out tests before claiming a learned skill win. | Learning reference; no auto-promotion. | Nightly training, memory as policy. |
| Local verification-loop, security-review, deployment-patterns | Executed, change-specific proof; risk-triggered review; rollback evidence. | Verification reference. | Blanket stack checklists as PASS. |
| Local strategic-compact | Keep milestone, artifact, failed approach, next action. | Resume/handoff facts. | A custom context database. |
| [Untrivial Agent Orchestrator](https://github.com/Untrivial-ai/agent-orchestrator/tree/15e9ea971f1711ec8b50e157d6eb300db6cbe0d6) | Desktop/daemon, Kanban, worktrees, session restore, fact-derived status. | Reconcile current identity; no overlapping replacement writers. | Copy the daemon, board or worktree manager into a skill. |
| [donvito Codex Astra/Luna](https://github.com/donvito/codex-astra-luna-orchestrator/tree/575e74ebcf9b199513151a8996665a71cf64ce50) | Install named role/model/effort pins. | Opt-in example profile; capability classes. | Obligatory Astra/Luna sequence or “strongest model reviews everything”. |

Inspected comparison forks (not runtime dependencies): AO
[63a04f0](https://github.com/byensitmagnus/agent-orchestrator/tree/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03),
CALO
[014b1d7](https://github.com/byensitmagnus/codex-astra-luna-orchestrator/tree/014b1d7c48c39087beec8aa4f1ca022053ac17b3).
See [choosing.md](choosing.md) and [research-priorities.md](research-priorities.md).

### Lab papers already cited

| Source | Says | AMC uses | Must not take |
|---|---|---|---|
| [NVIDIA AVO](https://arxiv.org/abs/2603.24517) v1, 2026-03-25 | Seven-day kernel search; execution feedback; stagnation intervention. No published same-compute baseline agent. | Recoverable incumbent, frozen evaluator, failed-attempt notes. | Supervisor daemon, week-long search, NVIDIA percentages as AMC gains. |
| [NVIDIA ARC-AGI-3 blog](https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/), 2026-08-21 | 100.00 RHAE on 25 public environments. Not a controlled architecture ablation. | Long-horizon persistence is a harness/model story. | ARC score as AMC quality. |
| [ARC scoring](https://docs.arcprize.org/methodology) | Task completion and action efficiency. | Metric literacy. | Price or coding-host comparison. |
| [Microsoft SkillOpt](https://arxiv.org/abs/2605.23904) v2, 2026-05-25; pin [79124b37](https://github.com/microsoft/SkillOpt/tree/79124b37e9a6371e13b753f8bcd7adb1e493ade1) | Train/selection/test split; scored trajectories. Gains are in that training setup. | Outcome-driven learning gates. | Instruction-density scoring; silent live adoption. |
| [OEO](https://arxiv.org/abs/2608.09629) v1, 2026-08-10 | Adaptive optimizer vs SkillOpt/GEPA; capability-dependent structure; some budget overruns. | Do not strip budgets or data boundaries. | Identify Luna with the paper's weak models. |
| [RouteLLM](https://arxiv.org/abs/2406.18665) | Route easy queries cheaper on its benchmarks. | Capability-aware job assignment is allowed. | Sol/Luna ranking for multi-turn coding. |
| [ACL 2024 error localization](https://aclanthology.org/2024.findings-acl.826/) | Locating an error ≠ repairing it. | Critique < reproducible failure. | Current-model limits from 2024 tasks. |
| [AI Agents That Matter](https://arxiv.org/abs/2407.01502) | Evaluate cost with accuracy; weak holdouts are common. | Proportionate validation; closed nine-run record. | Homemade superiority claims. |
| Google scaling blog + [arXiv 2512.08296](https://arxiv.org/html/2512.08296) HTML v3 | 260 configs, 6 benchmarks. Finance MAS up to +80.8%. PlanCraft MAS −39% to −70%. SWE-bench Verified: all MAS slightly worse than SAS. Independent error amp 17.2×; centralized 4.4×. n=20 Docker subset for SWE/Terminal. | Direct-first; parallel only if independent; centralize material review. | Copy 45% as a live AMC classifier. Treat Workbench as a coding benchmark (it is workplace tool-use). |

**Nature correction to the Google citation.** The peer-reviewed paper is Kim et
al., *Capable language models can outgrow the benefits of collaboration*,
[Nature Machine Intelligence](https://www.nature.com/articles/s42256-026-01268-y)
8, 1157–1172 (2026), DOI [10.1038/s42256-026-01268-y](https://doi.org/10.1038/s42256-026-01268-y).
It keeps the 260-configuration design. It states the ~45% figure as a
**validated selection rule** (94% sign match on 16 SWE-bench Verified and
Terminal-Bench model×benchmark cells), **not** a coefficient that survived
cluster-robust correction. SWE-bench Verified in Nature: SAS mean 0.488; hybrid
−1.3%, centralized −2.6%, decentralized −6.4%, independent −12.8%. HTML v3
cell means differ slightly (SAS 0.522; independent −14.9%). Use Nature for the
claim; keep the subset-size limit either way.

### Host documentation already cited

| Source | Says | AMC uses | Must not take |
|---|---|---|---|
| [OpenAI skills](https://developers.openai.com/codex/skills) | Name/description first; load body on use; catalog capped. | One short entrypoint; conditional references. | Stuff every domain skill into AMC. |
| [OpenAI subagents](https://developers.openai.com/codex/subagents) | Helpful when work is highly parallel. Extra tokens. Default depth 1. Caution parallel writers. | Native spawn; exclusive files; no required team. | Treat enablement as “Codex wants a team”. |
| [OpenAI config](https://developers.openai.com/codex/config-reference) | Host owns models, sandbox, agents. | Do not recreate host settings. | Frozen named-model core. |
| [OpenAI exec plans](https://developers.openai.com/cookbook/articles/codex_exec_plans) | Durable plan/progress for multi-hour work. Cookbook, not a trial. | Mission record, not a second transcript. | Mandatory filename or extra initializer agent. |
| [OpenAI eval best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Representative cases; do not add complexity without evidence. | Engineering checks ≠ model quality. | Unrepresentative demos as proof. |
| [OpenAI pricing](https://learn.chatgpt.com/docs/pricing) / [caching](https://developers.openai.com/api/docs/guides/prompt-caching) | Uncached, cached and output are different. | Resource checkpoint; unknown stays unknown. | Hardcoded prices in the skill. |
| [OpenAI plugins](https://developers.openai.com/codex/plugins); [openai/skills](https://github.com/openai/skills) deprecated | Distribute via plugins. | Skill and plugin packaging. | Catalog membership as quality. |
| [Anthropic long-running harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Premature completion; poorly documented partial work. | Incremental artifacts. | Required initializer/coder pair. |
| [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Focused worker context; distilled return; over-compression loses facts. | Packets with enough interfaces and evidence pointers. | Minimal word-count as a quality metric. |
| [Anthropic Managed Agents](https://www.anthropic.com/engineering/managed-agents), 2026-04-08 | Scaffolding goes stale; hosted session/harness/sandbox. | Delete obsolete rules; use host state. | Recreate that hosted service. |
| [Anthropic multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system) | Parallel research can help; large token overhead. | Research ≠ tightly coupled coding. | Token blow-up as “thoroughness”. |
| [Anthropic building effective agents](https://www.anthropic.com/engineering/building-effective-agents), 2024-12-19 | Start simple. Workflows vs agents. Add complexity only when measured. Evaluator-optimizer needs real criteria. | Composable patterns, not a compulsory pipeline. | Orchestrator-workers as the default coding shape. |
| Python [json](https://docs.python.org/3/library/json.html#repeated-names-within-an-object) | Duplicate keys keep the last value. | Eval-loader research note only. | Product behavior. |

Live host pages are not pinned client compatibility specs.

## Extra sources consulted this pass

These were not in [sources.md](sources.md) before this audit. They constrain
the same design choice. They are not new AMC dependencies.

| Source | Kind | Claim used here | Limit |
|---|---|---|---|
| Kim et al., Nature Mach. Intell. 2026, DOI 10.1038/s42256-026-01268-y | Peer-reviewed | Coding-adjacent MAS did not beat SAS; 45% is a selection rule; independent error amplification is large | 20-instance SWE/Terminal subsets; not AMC's issues |
| [Collaboration tax](https://arxiv.org/abs/2608.22152) v1, 2026-08-23 | Preprint, **abstract** | Two-agent tax is structured, falls with capability, and is a four-stage conversational cascade | 32 solo-tractable tasks, not SWE-bench |
| [Harness Engineering](https://arxiv.org/abs/2609.00006) v1 | Preprint, **abstract** | Production harnesses are hand-rolled; skills lead MCP slightly; no general agent framework imports | Source anatomy, not an outcome trial of AMC |
| [Same model, different harness](https://arxiv.org/abs/2608.26218) v1, 2026-08-26 | Preprint, **abstract** | Harness change moved Verified F2PF 28%→49% in a tight 20,480-token window | That harness treatment ≠ AMC Markdown |
| [Self-orchestration](https://arxiv.org/abs/2608.26480) | Preprint, **search** | Manager gains are conditional; manager token load can be ~3× | Not used as an AMC routing number |
| [Harness-Bench](https://arxiv.org/abs/2605.27922) | Preprint, **search** | Harnesses themselves are becoming a benchmark target | Not executed here |
| [METR time horizons](https://metr.org/time-horizons/); [Kwa et al. 2025](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/); [TH1.1](https://metr.org/blog/2026-1-29-time-horizon-1-1/) | Lab + NeurIPS | Human-duration 50% horizon has been doubling on the order of ~3–7 months depending on window; >16h measurements unreliable on the current suite | Horizon ≠ wall-clock AMC runtime; wide CIs |
| [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) | Public repo + docs | A tiny bash loop remains competitive on SWE-bench Verified | Different product class from AMC |
| [obra/superpowers](https://github.com/obra/superpowers) SDD skill | Public repo | If you choose SDD: fresh implementer per task, then review; workers must not spawn nested reviewers (observed duplicate seats) | High stars ≠ SWE-bench win; SDD is optional even inside Superpowers |
| [github/spec-kit](https://github.com/github/spec-kit) | Public repo | Specify → plan → tasks. Specs, not a multi-agent runtime | Spec process ≠ measured coding gain |
| [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) | Host docs | Subagent = overflow context and tool limits, not a default team. Description bloat warns at 15k tokens | Separate “agent teams” product exists; AMC is not that |
| [OpenAI Astra skills blog](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), 2026-09-11 | Host blog | Short descriptions, progressive disclosure, delete stale AGENTS.md, do not overconstrain stronger models | Astra-specific persistence notes are host advice |
| [Cursor worktrees](https://cursor.com/docs/configuration/worktrees) / [Cloud Agents](https://cursor.com/docs/cloud-agent) | Host docs | Isolation is a checkout or a VM | AMC cannot provide that |
| [Simon Willison on skills](https://simonwillison.net/2025/Oct/16/claude-skills/) | Practitioner | Skills as portable procedural memory; agents remain tools in a loop | Opinion, not a trial |
| [Simon Willison, agents](https://simonwillison.net/2025/Sep/18/agents/) | Practitioner | An agent is a model using tools in a loop; a skilled operator still matters | Opinion |

## Other repos versus the sources

| Repo / product | What it claims or does | Source alignment | Conflict |
|---|---|---|---|
| AMC | Direct-first portable skill; native host tools; no daemon | Matches Google/Nature on coding, Anthropic/OpenAI simplicity, harness-vs-framework finding | Cannot enforce isolation or prevent false PASS in natural language |
| Agent Orchestrator | Worktrees, daemon, Kanban, live sessions | Matches the isolation trend (OS, not prompt) | Different product. Its auto-review service is not an AMC requirement |
| Codex Astra/Luna orchestrator | Named role/model pins | Allowed as an opt-in host profile | Conflicts with “start simple” if made mandatory |
| Superpowers | Aggressive skill invocation; optional SDD with per-task implementer+review | Review-when-material matches Anthropic evaluator-optimizer | Always-per-task MAS conflicts with Nature SWE-bench result and collaboration tax |
| Spec Kit | Written specs before code | Harmless as an explicit user procedure | Not evidence for more agents |
| Claude Code / Codex / Cursor | Host loop, skills, optional subagents, worktrees/VMs | They **are** the harness papers' subject | AMC is a guest in that loop |
| mini-SWE-agent | Minimal loop, high Verified score | Supports “do not add a framework” | Not a workflow skill for Magnus's hosts |

## Logic that survives the extra sources

1. **Task structure beats ideology.** Parallel decomposable work can gain a lot.
   Sequential, tool-dense, already-strong single-agent work can lose. Coding
   issue resolution in the Google/Nature study sat in the second bucket.
2. **A central checker beats independent workers** when errors must not
   multiply. That supports lead-owned acceptance and occasional independent
   review. It does not support a swarm of unchecked writers.
3. **The host is the optimizer.** Harness studies move scores without new
   weights. AMC should stay small enough not to fight the host.
4. **Instructions rot.** METR horizons and Managed Agents / Astra guidance all
   say last year's ceremony becomes today's drag. AMC should lose rules over
   time, not accumulate them.
5. **Markdown does not enforce behavior.** Superpowers itself documents workers
   ignoring nested-review bans. AMC's validator can reject a false table PASS;
   it cannot make an agent find a hidden 429.

## Product implication for candidate.9

Keep the kernel as written: smallest graph, lead owns acceptance, load
references only when needed, no companion orchestrator, no homemade farm.

Do **not** add, on the basis of this audit:

- always-on implementer/reviewer pairs
- a required team topology
- a 45% live classifier
- a copied worktree/VM manager
- more skills in the runtime ZIP
- new subject-run batches

Behavioral quality, cost and speed versus direct work remain **NOT VERIFIED**.

## Source record for this pass

Accessed 2026-09-15. Primary fetches: Nature MMI page, arXiv HTML 2512.08296 v3,
Anthropic effective-agents / long-running / context / managed-agents /
multi-agent-research / Claude subagents, OpenAI skills / subagents / Astra blog,
Superpowers SDD skill, mini-SWE-agent docs, Cursor worktrees/cloud-agent search
results, METR time-horizon pages.

Abstract-only this pass: 2608.22152, 2609.00006, 2608.26218.

Search-only this pass: 2608.26480, 2605.27922, selected Willison posts.

Earlier repo pins (NVIDIA, SkillOpt, OEO, RouteLLM, ACL, AO, CALO) were already
recorded on 2026-09-12/13 and were not re-executed.
