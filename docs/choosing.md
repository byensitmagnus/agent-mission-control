# Choose the orchestration approach for your work

These projects solve related problems at different levels. This comparison is
based on the linked repository versions inspected on 2026-09-13. It describes
inspected implementation as well as documentation; it is not an execution benchmark.

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
The [optional profile](../examples/codex/README.md) is separate and opt-in.

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

The linked comparison repositories are forks of
[Untrivial-ai/agent-orchestrator](https://github.com/Untrivial-ai/agent-orchestrator)
and [donvito/codex-astra-luna-orchestrator](https://github.com/donvito/codex-astra-luna-orchestrator).
The pinned forks, rather than changing upstream heads, define this comparison.

## What to compare before adopting

The code comparison matters as much as the interface:

| Mechanism | AMC candidate.8 source | Agent Orchestrator | Codex Astra/Luna |
|---|---|---|---|
| Host integration | One skill payload, five project destinations, read-only byte check; native tools supply execution. | [Real adapter interface](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/ports/agent.go) with launch and restore behavior. | [Codex installation script](https://github.com/byensitmagnus/codex-astra-luna-orchestrator/blob/014b1d7c48c39087beec8aa4f1ca022053ac17b3/setup.ps1) and model/role profiles. |
| Existing user files | Refuses an existing skill; staged byte check before activation; no global/config changes. | Its service manages worker workspaces. | Copies project profiles with overwrite handling; this is a configuration change. |
| Recovery and isolation | Native host mechanisms plus lead reconciliation; no automatic recovery service. | [Implemented worktree lifecycle](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/adapters/workspace/gitworktree/workspace.go) and [session-switch recovery](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/session_manager/agent_switching.go). | Codex provides the runtime; profile instructions guide its use. |
| Review | Lead arranges material independent review, integrates fixes and executes acceptance. | [Idle auto-review coordinator](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/autoreview/coordinator.go) is actual service code. | Named reviewer roles and orchestration instructions. |

AMC's new installer and integrity regressions are practical improvements. They
do not reproduce AO's daemon features. [Inspect the code checks and host limits](engineering-candidate.8.md).

Check the result on a task you understand: preserved behavior, verified delivery,
necessary user intervention and total work required. AMC's
[results and limitations](evidence.md) are available for inspection. We have not
run an equivalent end-to-end task across all three products, so comparative
quality, completion rate, speed and cost remain unverified.

## What still needs to improve

Candidate.8 is worth adopting for its checked installation and repaired tooling.
That is an improvement over AMC's previous source, not evidence of an overall
lead over either alternative. The next useful work, in order, is:

1. **Complete native first use.** On each advertised host, demonstrate selection
   of the installed skill and one useful task through delivery and executed
   checks. Include delegation when the task benefits from it. Five identical
   folders and one discovery observation do not establish that journey.
2. **Demonstrate recovery without user coordination.** On work that actually
   needs it, show a stopped or failed worker being reconciled, unfinished work
   resumed safely and review findings integrated. AO already implements lifecycle
   mechanisms; AMC must demonstrate the result through its native host. Add code
   only where an observed failure cannot be solved by the existing mechanisms.
3. **Show repeatable user benefit.** Retain successful and failed deliveries,
   regressions, user corrections and total elapsed work on ordinary useful tasks.
   A fair comparative claim needs comparable scope and acceptance across the
   products. The existing direct-versus-AMC pair achieved the same result and
   AMC took longer; it is evidence to keep, not a win to reframe.

These are evidence gaps and product priorities, not extra gates for every user
task. A dashboard clone, more role files or a larger test count would not by
themselves demonstrate better delivered work.

[Install AMC](getting-started.md) · [Understand its workflow](how-it-works.md) ·
[Sources and attribution](sources.md)
