# Claim ledger

Canonical claim register for Agent Mission Control. Reviewed 2026-09-19.

Do not copy these entries into other files. Point here.

Three independent axes per claim:

| Axis | Values |
|---|---|
| Origin | `primary_source` · `reasoned_inference` · `local_observation` |
| Enforcement | `instruction_only` · `validator_enforced` · `host_enforced` · `externally_attested` |
| Outcome | `not_verified` · `observed` · `repeatedly_observed` |

Source grades A–E in [field-state.md](field-state.md) measure source quality.
They are not outcome status. A green `python evals/control_contract.py --self-check`
is deterministic contract proof, not behavioral proof.

---

## AMC-CLASS-001 — product class

- **mechanism:** portable_skill
- **claim:** AMC is a portable Markdown skill/plugin that routes work on an existing host. It is not a harness, SDK, graph framework, desktop daemon, or hosted project coordinator.
- **sources:** Anthropic Skills (2026-09-15), OpenAI Codex skills (2026-09-14), AMC `SKILL.md`, `scripts/package_plugin.py`
- **source_supported_fact:** Skills are folders of instructions, scripts and resources that a host may load. Hosts own the loop, tools and traces.
- **architectural_inference:** AMC should stay installable as a skill and keep host adapters thin.
- **does_not_prove:** That a skill outperforms a hosted coordinator or a desktop orchestrator.
- **adoption:** adopted
- **enforcement:** validator_enforced for package layout; host_enforced for actual skill loading
- **implementation:** `SKILL.md`, `.claude-plugin/plugin.json`, `scripts/package_plugin.py`, `scripts/validate.py`
- **outcome_status:** observed (install/package checks). Behavioral value `not_verified`
- **confidence:** high for class; low for product value
- **review_date:** 2026-09-19

## AMC-LEAD-001 — one lead owns acceptance

- **mechanism:** lead_ownership
- **claim:** One lead owns the complete objective and the final verdict. Workers are candidates until the lead accepts current artifacts.
- **sources:** Anthropic Building Effective Agents (orchestrator-workers, 2024-12-19 / 2025-01-xx live docs); Google ADK LLM-driven delegation; Microsoft Agent Framework agents-as-tools
- **source_supported_fact:** Official patterns keep a coordinator that decomposes work and integrates results. They do not require a named model.
- **architectural_inference:** AMC keeps one lead and treats worker “done” as incomplete until evidence.
- **does_not_prove:** That one lead plus workers beats one strong session on ordinary tasks.
- **adoption:** adopted
- **enforcement:** instruction_only in the installed skill; validator_enforced if a Mission View / control-contract file is checked in-repo
- **implementation:** `SKILL.md`, `templates/mission-view.md`, `evals/control_contract.py`
- **outcome_status:** not_verified (behavior). Deterministic schema checks `observed` in-repo
- **confidence:** medium
- **review_date:** 2026-09-19

## AMC-ROUTE-001 — direct work is the default

- **mechanism:** direct_default
- **claim:** Ordinary sequential tasks stay with the lead. Extra agents are not identity.
- **sources:** Anthropic Building Effective Agents (start simple; add complexity only when it helps); Microsoft Agent Framework (prefer functions/agents-as-tools before workflows); AMC `evals/decision_kernel.py` case 01
- **source_supported_fact:** Vendor docs recommend the simplest pattern that can finish the job. They do not forbid specialists.
- **architectural_inference:** `simple_sequential` must not spawn jobs. That is a contract, not a quality claim.
- **does_not_prove:** Direct work is always cheaper or better.
- **adoption:** adopted
- **enforcement:** validator_enforced (`SIMPLE_SEQUENTIAL_DELEGATION`) when a contract file is checked; instruction_only in live host chats
- **implementation:** `evals/decision_kernel.py`, `evals/control_contract.py`, `SKILL.md`
- **outcome_status:** not_verified
- **confidence:** high for the default; low for payoff
- **review_date:** 2026-09-19

## AMC-ROUTE-002 — sequential delegation ≠ parallel fan-out

- **mechanism:** route_split
- **claim:** Sequential specialist isolation is a different route from independent parallel jobs. Independence is required for parallel ready jobs, not for every delegated job.
- **sources:** Anthropic orchestrator-workers; OpenAI Codex subagents (context isolation, inherit parent model/effort unless set); Kim et al. Multi-Agent Collaboration Mechanisms (hits parallel MAS on sequential tasks, not serial specialists); AMC Truth Layer `sequential_delegated`
- **source_supported_fact:** Official hosts support sequential subagents and parallel workers as separate mechanisms. Kim et al. does not forbid serial specialist isolation.
- **architectural_inference:** SKILL text that AND-gated all delegation on independence was too strict relative to the control contract.
- **does_not_prove:** Sequential specialists beat a stronger single session.
- **adoption:** adopted (contract 2026-09-18; skill text aligned 2026-09-19)
- **enforcement:** validator_enforced for route names and observation receipts; instruction_only for the live routing decision
- **implementation:** `evals/control_contract.py` `ROUTES`, `SKILL.md`, `docs/how-it-works.md`
- **outcome_status:** not_verified
- **confidence:** high for the split; low for when to spend the extra hop
- **review_date:** 2026-09-19

## AMC-CTX-001 — focused context packets

- **mechanism:** focused_context_packets
- **claim:** A bounded worker should receive the job, inputs, authority, owned files, proof target and stable project rules — not the entire lead transcript.
- **sources:** Anthropic Effective Context Engineering for AI Agents (2026-09-13): high-signal context, just-in-time retrieval; OpenAI Skills progressive disclosure (metadata → SKILL.md → resources)
- **source_supported_fact:** Both vendors treat context as a scarce, compiled resource. They do not specify AMC’s packet schema.
- **architectural_inference:** AMC uses a small packet template as the portable handoff.
- **does_not_prove:** Focused packets improve every task or every model.
- **adoption:** adopted
- **enforcement:** instruction_only (hosts still inject shared instructions, skills and permissions)
- **implementation:** `templates/context-packet.md`, `references/packets.md`
- **outcome_status:** not_verified
- **confidence:** medium
- **review_date:** 2026-09-19

## AMC-ISO-001 — writer isolation is host-enforced

- **mechanism:** writer_isolation
- **claim:** Independent writers need separate branches, worktrees, sandboxes or equivalent host isolation. A skill cannot create that isolation by itself.
- **sources:** Claude Code `isolation: "worktree"` (docs 2026-09-15: worktree from default branch, not parent HEAD); Codex worktrees/environments; Superpowers `using-git-worktrees` (fail-open if git/worktree missing)
- **source_supported_fact:** Isolation is a host/runtime feature. Superpowers documents the same gap: the skill asks, the host may or may not isolate.
- **architectural_inference:** AMC records isolation as required for parallel writers and serializes when the host cannot isolate.
- **does_not_prove:** Worktrees raise quality. They reduce overwrite risk when the host actually creates them.
- **adoption:** adopted
- **enforcement:** host_enforced when the host creates the worktree; validator_enforced `PARALLEL_WITHOUT_ISOLATION` only if a contract file is checked; otherwise instruction_only
- **implementation:** `evals/control_contract.py`, `SKILL.md`, `docs/hosts.md`
- **outcome_status:** not_verified (AMC). Host worktree behavior is documented by vendors, not attested for AMC runs
- **confidence:** high for the requirement; medium for host coverage
- **review_date:** 2026-09-19

## AMC-ART-001 — artifacts and evidence, not transcripts

- **mechanism:** artifact_handoff
- **claim:** Workers return files, checks and a short evidence packet. Raw transcripts are not acceptance.
- **sources:** Anthropic long-running / structured-note guidance; Karpathy autoresearch keep/discard of candidate artifacts; NVIDIA AVO commit-if-correct
- **source_supported_fact:** Research and vendor notes treat files and scores as the durable state. They do not prove AMC’s packet fields are optimal.
- **architectural_inference:** Mission View plus evidence packets are the portable state.
- **does_not_prove:** Agents will actually fill the packets without a host hook.
- **adoption:** adopted
- **enforcement:** instruction_only in live chats; validator_enforced for required keys when a contract/Mission View is checked
- **implementation:** `templates/evidence-packet.md`, `templates/mission-view.md`, `evals/control_contract.py`
- **outcome_status:** not_verified
- **confidence:** medium
- **review_date:** 2026-09-19

## AMC-ACC-001 — PASS requires evidence, not a command

- **mechanism:** acceptance_evidence
- **claim:** `PASS` needs an executed check, a current artifact, or a named review/attestation. A passing command is sufficient only when the claim is a command claim. Worker completion is `completed` + `NOT VERIFIED` until the lead accepts.
- **sources:** Superpowers `verification-before-completion` (instruction: fail the task if you did not run verification); AMC Truth Layer verdicts; Anthropic eval guidance (grade A process, not AMC outcomes)
- **source_supported_fact:** Superpowers states an iron law in a skill. Claude Code does not host-enforce it. AMC can schema-check a recorded verdict; it cannot force a host to run tests.
- **architectural_inference:** Split lifecycle (`completed`) from verdict (`NOT VERIFIED` / `PASS`).
- **does_not_prove:** Leads will refuse false PASS in production chats.
- **adoption:** adopted
- **enforcement:** validator_enforced for known verdict strings and missing observation receipts; instruction_only for actually running the check
- **implementation:** `evals/control_contract.py`, `references/verification.md`, `templates/mission-view.md`
- **outcome_status:** not_verified
- **confidence:** medium
- **review_date:** 2026-09-19

## AMC-OBS-001 — planned delegation must be observed

- **mechanism:** observation_receipts
- **claim:** If the plan says a child job exists, the contract must record an observed child id or an explicit `DELEGATION_NOT_OBSERVED` deviation. Planned-only graphs are not execution proof.
- **sources:** AMC local contract 2026-09-18; Microsoft AF checkpoints (host-side persistence, not AMC); Google ADK session state (SDK, not AMC)
- **source_supported_fact:** Vendor runtimes persist session/checkpoint state internally. A portable skill has no such store unless the repo keeps files.
- **architectural_inference:** Require planned vs observed child ids in the control contract when that file is used.
- **does_not_prove:** Hosts will write the contract without being asked.
- **adoption:** adopted
- **enforcement:** validator_enforced in `evals/control_contract.py`; instruction_only in the installed skill package (Python is not shipped in COPY_DIRS)
- **implementation:** `evals/control_contract.py`, `docs/control-contract.md`
- **outcome_status:** observed for the self-check suite; live host use `not_verified`
- **confidence:** high for the invariant; low for adoption in chats
- **review_date:** 2026-09-19

## AMC-AVO-001 — optimizer loops need a frozen evaluator

- **mechanism:** measurable_optimizer
- **claim:** Variation/repair loops are in-scope only when a real evaluator, bounded search surface and keep/discard rule exist. Ordinary software tasks usually lack that evaluator.
- **sources:** Karpathy `karpathy/autoresearch` (commit `228791f`, MIT, 2026-03-09): one file, frozen eval, one metric, keep/discard; NVIDIA Agentic Variation Operators (arXiv 2603.24517v1, 2026-03-31): Vary(P,K,f), commit if correct and not worse
- **source_supported_fact:** Both systems assume a frozen f. Autoresearch is a research loop, not a coding-agent swarm. AVO results do not transfer to tasks without f.
- **architectural_inference:** AMC route `measurable_optimizer` is eligible only with an evaluator. Otherwise reject the route.
- **does_not_prove:** AVO-style loops help product coding work.
- **adoption:** adopted with a hard eligibility gate
- **enforcement:** validator_enforced `OPTIMIZER_WITHOUT_EVALUATOR`; instruction_only for actually freezing f
- **implementation:** `evals/control_contract.py`, `references/optimization.md`
- **outcome_status:** not_verified for software-task payoff
- **confidence:** high for the gate; high that transfer to ordinary SE is invalid
- **review_date:** 2026-09-19

## AMC-COST-001 — no general cheaper/faster/better claim

- **mechanism:** outcome_hygiene
- **claim:** AMC does not claim that multi-agent work is generally cheaper, faster, or higher quality than direct work. Stronger-lead plus cheaper-worker remains optional.
- **sources:** METR (time-horizon tables, not AMC); SkillOpt (arXiv 2605.23904v2) skill-induced failure; AMC `docs/status.json` behavioral `NOT VERIFIED`
- **source_supported_fact:** Public evals measure models and some harnesses. None attest AMC production outcomes. Codex children inherit parent model/effort unless explicitly set.
- **architectural_inference:** Keep cheap-worker language as a routing option, never as a guarantee. Host spawn semantics can silently keep the parent model.
- **does_not_prove:** The option is useless. It proves the option is unverified.
- **adoption:** adopted (claim refused)
- **enforcement:** instruction_only plus review of docs; `docs/status.json` records behavioral `NOT VERIFIED`
- **implementation:** `SKILL.md`, `docs/status.json`, `docs/evidence.md`
- **outcome_status:** not_verified (intentionally)
- **confidence:** high that we must not claim it
- **review_date:** 2026-09-19

## AMC-HOST-001 — host owns the loop

- **mechanism:** host_runtime
- **claim:** Sandbox, traces, compaction, worktrees, permissions and actual subagent spawn are host services. AMC can instruct and, in-repo, validate files. It cannot execute the loop.
- **sources:** Claude Code subagents/hooks docs; Codex AGENTS.md and plugins; Google ADK runners; Microsoft AF workflow runtime
- **source_supported_fact:** Those products are runtimes or SDKs. AMC’s packaged skill copies `agents`, `references`, `templates`, `assets` — not `scripts/validate.py`.
- **architectural_inference:** Document host dependence instead of shipping a daemon.
- **does_not_prove:** Adding a daemon would improve outcomes.
- **adoption:** adopted
- **enforcement:** host_enforced for spawn/isolation; instruction_only for AMC policy in live chats
- **implementation:** `scripts/package_plugin.py` `COPY_DIRS`, `docs/control-contract.md`, `docs/hosts.md`
- **outcome_status:** observed for package contents; live spawn `not_verified`
- **confidence:** high
- **review_date:** 2026-09-19

## AMC-PROJ-001 — Claude Code Projects is out of class

- **mechanism:** hosted_coordinator
- **claim:** Claude Code Projects is a hosted coordinator with cloud threads, VM isolation, project memory and a 200-thread/day cap. AMC must not copy that runtime. Compare the architecture pattern, not the product.
- **sources:** Anthropic Claude Code Projects, https://code.claude.com/docs/en/claude-projects (fetched 2026-09-19). Public beta, Pro/Max, not Team/Enterprise yet.
- **source_supported_fact:** Coordinator conversation routes work to cloud Claude Code sessions. Threads get repos, project instructions and project memory. Each thread is a VM with its own branch. Soft: routing judgment, memory drafts. Hard: VM, branch, thread cap, plan availability, skip-permissions flag.
- **architectural_inference:** Keep AMC as the portable skill for hosts that are not that coordinator. Do not add cloud sessions to AMC.
- **does_not_prove:** Projects is “better than AMC” or the reverse. Different product class.
- **adoption:** rejected as AMC runtime; used as comparison only
- **enforcement:** not applicable in AMC (host product)
- **implementation:** none in AMC. See this ledger and [field-state.md](field-state.md)
- **outcome_status:** not_verified (no AMC vs Projects trial)
- **confidence:** high for class split
- **review_date:** 2026-09-19

## AMC-SP-001 — Superpowers is a host plugin, not a proof of AMC

- **mechanism:** sdd_plugin
- **claim:** Superpowers (`obra/superpowers`, plugin v6.1.1) is a Claude/Codex/Cursor plugin: session-start hook plus composable skills (brainstorm → spec → plan → subagent-driven TDD → review). Its “proven techniques” line is vendor language. AMC shares the skill-plugin class and rejects mandatory SDD, mandatory subagents, and verification as an iron law without a recorded check.
- **sources:** `obra/superpowers` README; `.claude-plugin/plugin.json` v6.1.1; `hooks/hooks.json` SessionStart `startup|clear|compact`; skills `using-superpowers`, `subagent-driven-development`, `verification-before-completion`, `using-git-worktrees` (local Cursor cache, 2026-09-19)
- **source_supported_fact:** SessionStart injects bootstrap. SDD spawns implementer then spec-reviewer, then a two-stage review (spec then code quality). Worktree skill fails open. Verification is a written rule, not a host gate.
- **architectural_inference:** AMC can reuse “fresh implementer + independent review” as an optional route, not a default pipeline.
- **does_not_prove:** Superpowers raises quality, or that AMC should copy SDD.
- **adoption:** adapted (optional review/isolation language); rejected (mandatory SDD pipeline)
- **enforcement:** Superpowers: mix of host hook (session-start) and instruction_only skills. AMC: instruction_only unless in-repo validators run
- **implementation:** comparison only; AMC `SKILL.md` is a router, not SDD
- **outcome_status:** not_verified
- **confidence:** high for mechanism description
- **review_date:** 2026-09-19

## AMC-SKILL-001 — progressive disclosure is host-provided

- **mechanism:** skill_loading
- **claim:** Name/description at start, then SKILL.md, then linked files, is the vendor skill protocol. AMC must keep a short router skill and put depth in `references/`.
- **sources:** Anthropic Skills; OpenAI Codex skills / AGENTS.md
- **source_supported_fact:** Hosts load skill metadata first. AMC cannot change that protocol.
- **architectural_inference:** Keep `SKILL.md` small. Do not put the claim ledger in the skill body.
- **does_not_prove:** Shorter skills always win.
- **adoption:** adopted
- **enforcement:** host_enforced loading; validator_enforced description length in `scripts/validate.py`
- **implementation:** `SKILL.md` frontmatter, `scripts/validate.py`
- **outcome_status:** observed for packaging; quality `not_verified`
- **confidence:** high
- **review_date:** 2026-09-19

## AMC-ADK-001 — workflows are explicit, routing is adaptive

- **mechanism:** workflow_boundary
- **claim:** Use Sequential/Parallel/Loop workflow agents, Microsoft graphs, or checkpoints only when ordering, isolation, gates or recovery require them. LLM-driven delegation stays the default router.
- **sources:** Google ADK 2.0 workflow agents; Microsoft Agent Framework workflows vs agents-as-tools; Anthropic workflow vs agent distinction
- **source_supported_fact:** SDKs provide graph runtimes. AMC is not those SDKs.
- **architectural_inference:** Encode six named routes in docs/contract. Do not ship a graph engine.
- **does_not_prove:** Named routes beat free-form lead judgment.
- **adoption:** adapted (route names); rejected (graph runtime)
- **enforcement:** validator_enforced route enum when a contract file exists; instruction_only otherwise
- **implementation:** `evals/control_contract.py` `ROUTES`
- **outcome_status:** not_verified
- **confidence:** medium
- **review_date:** 2026-09-19

## AMC-SKILLOPT-001 — skills can induce failure

- **mechanism:** skill_risk
- **claim:** Adding skills can reduce performance. AMC must not treat “more skills” as an upgrade.
- **sources:** SkillOpt arXiv 2605.23904v2
- **source_supported_fact:** The paper studies skill-induced failure and repair. It is not an AMC eval.
- **architectural_inference:** Keep the core skill small. Optional profiles stay opt-in.
- **does_not_prove:** AMC’s current skill is the right size.
- **adoption:** adopted as a limitation
- **enforcement:** instruction_only
- **implementation:** `docs/field-state.md`, this ledger
- **outcome_status:** not_verified for AMC
- **confidence:** medium that the warning applies; high that we must not ignore it
- **review_date:** 2026-09-19
