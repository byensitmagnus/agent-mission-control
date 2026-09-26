# Choose the orchestration approach for your work

These projects solve related problems at different levels. This comparison is
based on the linked repository versions inspected on 2026-09-13. It describes
inspected implementation as well as documentation; it is not an execution benchmark.

Install current GitHub `main`, or choose an exact tag from
[Releases](https://github.com/byensitmagnus/agent-mission-control/releases).
Candidate.16's original R4 claim was rejected after a false PASS on a migration
smoke case; its report-format beta has advisory PASS only.
The mechanism table below records an older inspection.

## Start with what you need

| Your need | A good fit | Why |
|---|---|---|
| Give a coding agent a goal and let it choose, coordinate and verify the work. | **Agent Mission Control** | A portable workflow skill using your current host, selected lead and available tools. |
| Follow many worker sessions, branches, pull requests and reviews in a separate live desktop interface. | **Agent Orchestrator** | A desktop platform with a local daemon, Kanban and worker workspaces. |
| Install explicit Codex model/effort assignments for named agent roles. | **Codex Astra/Luna Orchestrator** | Project installers, Pro/Plus profiles, role files and tuning guides. |

## What you get with AMC

AMC brings adaptive routing, focused handoffs, integration, verification and
recoverable progress into a skill. Its standard installation adds a project
skill folder. It does not install a daemon or replace your model settings.
The [optional intent profiles](../examples/profiles.md) and the
[optional Codex mapping](../examples/codex/README.md) are separate and opt-in.

Choose AMC when you want the lead to own the execution route and produce a
deliverable with inspectable checks. Begin with [one useful task](task-guide.md).
Actual delegation and isolation depend on your host's capabilities and the work.

## Where the alternatives fit better

**Agent Orchestrator** makes concurrent work visible through real product
screens: worker sessions, isolated Git worktrees, native terminals, previews,
PRs and CI. Its [README](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/README.md)
and [quickstart](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/frontend/src/landing/content/docs/quickstart.mdx)
describe that complete workspace. AMC does not supply its own board, terminal,
browser or worktree manager. If that interface is your main need, evaluate AO.

**Codex Astra/Luna Orchestrator** makes role/model choices explicit and offers
shell and PowerShell installers. Its
[README](https://github.com/byensitmagnus/codex-astra-luna-orchestrator/blob/014b1d7c48c39087beec8aa4f1ca022053ac17b3/README.md)
documents overwrite handling, role overrides, example tasks and token accounting.
If you want those specific presets, evaluate that setup. AMC's core skill keeps
your selected lead and routes work to available capabilities; it does not require
Astra/Luna or promise that another model pairing will be cheaper.

The pinned forks inspected for the comparison were
[Untrivial-ai/agent-orchestrator](https://github.com/Untrivial-ai/agent-orchestrator)
and [donvito/codex-astra-luna-orchestrator](https://github.com/donvito/codex-astra-luna-orchestrator).
The read-only 2026-09-24 source refresh also inspected upstream pins AO
`15e9ea971f1711ec8b50e157d6eb300db6cbe0d6` and CALO
`575e74ebcf9b199513151a8996665a71cf64ce50`, alongside fork pins AO
`63a04f08fc5a5804a2306e96d1c59fc4a7f68c03` and CALO
`014b1d7c48c39087beec8aa4f1ca022053ac17b3`. Current upstream heads observed
that day were AO `96f2b39` and CALO `30b7d0b`; those heads were not inspected
and support no claims in this comparison.

## What to compare before adopting

The code comparison matters as much as the interface:

| Mechanism | AMC source on 2026-09-13 | Agent Orchestrator | Codex Astra/Luna |
|---|---|---|---|
| Host integration | One skill payload, five project destinations, read-only byte check; native tools supply execution. | [Real adapter interface](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/ports/agent.go) with launch and restore behavior. | [Codex installation script](https://github.com/byensitmagnus/codex-astra-luna-orchestrator/blob/014b1d7c48c39087beec8aa4f1ca022053ac17b3/setup.ps1) and model/role profiles. |
| Existing user files | Default install refuses replacement; explicit updates check the reviewed fingerprint and retain the complete old copy. No global/config changes. | Its service manages worker workspaces. | Copies project profiles with overwrite handling; this is a configuration change. |
| Recovery and isolation | Native host mechanisms plus lead reconciliation; no automatic recovery service. | [Implemented worktree lifecycle](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/adapters/workspace/gitworktree/workspace.go) and [session-switch recovery](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/session_manager/agent_switching.go). | Codex provides the runtime; profile instructions guide its use. |
| Review | Lead arranges material independent review, integrates fixes and executes acceptance. | [Idle auto-review coordinator](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/autoreview/coordinator.go) is actual service code. | Named reviewer roles and orchestration instructions. |

The candidate.8 installer and integrity checks were practical improvements over
AMC's previous source. They do not reproduce AO's daemon features.
[That record](engineering-candidate.8.md) is not a reason to install the tag.

Check the result on a task you understand: preserved behavior, verified delivery,
necessary user intervention and total work required. AMC's
[results and limitations](evidence.md) are available for inspection. We have not
run an equivalent end-to-end task across all three products, so comparative
quality, completion rate, speed and cost remain unverified.

## What to install

Install current GitHub `main`, using [getting started](getting-started.md).
For an exact tagged ZIP, check [Releases](https://github.com/byensitmagnus/agent-mission-control/releases);
`main` can advance before a new tag. The 2026-09-13 inspection is not evidence
of an overall lead over either alternative.

Other branches are not this kernel. A product-contract draft adds a JSON
contract and a Python checker. An Orca draft maps jobs onto another product's
CLI. Neither is required here. This skill keeps direct work, a specialist when
focused expertise or fresh context helps, and parallel work only when the jobs
are independent. Real dependencies name the upstream artifact they need.

AMC does not run an owned behavioral research program. Further kernel changes
must cite host docs, published research, other public repositories or known
practitioner guidance. Engineering checks and defects on real commissioned work
remain allowed. Do not add subject-run farms to close the gaps below.

The source-aligned product priority is a cautious sequential default for
ordinary coding, plus coordination where it fits: use expertise or fresh context
for a bounded specialist task, fan out only independent jobs, and name a required
upstream artifact only when the work actually depends on it. Keep durable
progress and host isolation for parallel writers. A dashboard clone, more role
files or a larger homemade test count would not by themselves demonstrate better
delivered work. [Field state](field-state.md) maps these mechanisms to graded
sources and compares AMC with hosts, SDKs, frameworks, AO, CALO, Superpowers and
Spec Kit by mechanism, not by brand.

ADK, Microsoft Agent Framework and LangGraph are **frameworks**. They are not
the same product class as this skill.

[Reviewed code research priorities](research-priorities.md) add exact source
anchors, counterevidence and the smallest next investigations. They distinguish
possible improvements from accepted implementation work.

[Install AMC](getting-started.md) · [Understand its workflow](how-it-works.md) ·
[Sources and attribution](sources.md)
