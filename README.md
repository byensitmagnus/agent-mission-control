<p align="center">
  <picture>
    <source media="(max-width: 600px)" srcset="docs/assets/mission-path-mobile.svg" />
    <img src="docs/assets/mission-path.svg" alt="Illustration, not a recorded run: a lead takes a goal, chooses direct work or a specialist or parallel help, then integrates and verifies." width="100%" />
  </picture>
</p>

<h1 align="center">Agent Mission Control</h1>
<p align="center"><strong>Turn a demanding AI coding task into a checked delivery.</strong><br />One lead manages context, useful specialist help and the work still left to finish.</p>
<p align="center">One portable skill. Codex · Claude Code · Cursor · Grok · Kimi.<br />No extra server. Delegate only when a job earns its cost.</p>

<p align="center">
  <a href="docs/getting-started.md"><strong>Get started →</strong></a> ·
  <a href="docs/task-guide.md">Pick a task</a> ·
  <a href="docs/how-it-works.md">How it works</a> ·
  <a href="docs/evidence.md">Results &amp; limits</a>
</p>

<p align="center">
  <a href="https://github.com/byensitmagnus/agent-mission-control/actions/workflows/validate.yml"><img src="https://github.com/byensitmagnus/agent-mission-control/actions/workflows/validate.yml/badge.svg?branch=main" alt="Public main engineering checks" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2c568c" alt="MIT license" /></a>
</p>

## Start in your project

1. **Install the project skill** from
   [current `main`](docs/getting-started.md#1-install-the-skill). Five-host
   checked install and update live in
   [hosts.md](docs/hosts.md#install-the-current-source).
2. **Select the project copy** with your
   [host command](docs/getting-started.md#2-select-the-installed-copy). Keep your
   current model and normal permissions.
3. **Give it work you already need.** Replace the brackets below with one
   concrete outcome. The lead chooses the work and manages handoffs.

```text
$agent-mission-control

Deliver: [the outcome I need].
Done when: [two observable criteria].
Preserve: [behavior, data, constraints].

Inspect the project. Choose useful help.
Finish the authorized local work.
Run relevant checks. Show the result,
evidence and remaining limits.
Stop before push or external changes.
```

For a read-only first task: “Map how this project's main user action reaches its
implementation. Cite the real files and flag missing context. Do not edit or run
code.” A supported answer shows the task was done; confirm skill loading through
your host's selected path or invocation record, not the answer alone.

[Fix a bug](docs/task-guide.md#fix-a-bug) ·
[Investigate with a specialist](docs/task-guide.md#one-specialist-for-a-bounded-investigation) ·
[Resume saved work](docs/task-guide.md#resume-unfinished-work)

**A useful result** names the changed files or the report, the checks that
actually ran, and what is still open. [Share that experience](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml)
after you remove private information.

## Your goal stays with one lead

AMC is a reusable set of instructions that helps your coding assistant choose
the work, give useful jobs to focused agents, integrate their results and check
the finished deliverable. The lead coordinates the handoffs. You supply the goal,
constraints and decisions that need your authority.

| When you need… | AMC is designed to… | You should receive… |
|---|---|---|
| A bug fixed | Reproduce it, make the repair and check affected behavior. | The change, checks and remaining limitations. |
| A feature built | Split genuinely independent work, then integrate and verify it. | One coherent result, with evidence for its acceptance criteria. |
| Interrupted work finished | Reconcile the saved mission with current files and valid proof. | Progress from the remaining work and a clear final status. |
| Code investigated before a change | Trace callers and guards in a read-only snapshot, then challenge findings. | Supported findings or reasoned refutations, with untested behavior clearly identified. |

Small tasks stay with the lead. The route is one of three:

1. **Direct.** The lead edits, checks, and finishes.
2. **One specialist.** Focused expertise or a fresh context helps a bounded job. The handoff names the required inputs, write scope and acceptance check; upstream work must be ready when needed.
3. **Parallel.** Only jobs that do not need each other's output. Parallel writers need host isolation.

A stronger lead may give a bounded job to a cheaper worker. That pairing is
optional, not AMC's identity. Host tools and permissions determine what can
actually run.

## Know what “done” means

The lead should show **what changed, which checks actually ran, and what remains**.
A worker finishing is one input to that decision. Confirmed failures need repair;
missing evidence must stay visible. Long tasks keep a recoverable mission record.

An illustrative delivery can be as short as:

> **Fixed:** zero is retained in the exported total.<br>
> **Checked:** regression and existing export checks passed.<br>
> **Scope:** export formatting changed; no deployment performed.

This is an output example, not a measured run.
If someone will run a generated script or installer, that file is the artifact.
A passing check on the source leaves the package NOT VERIFIED.
[Follow a complete task and delivery example →](docs/task-guide.md#what-a-completed-delivery-looks-like)

## Context and dependencies, handled for you

**Context engineering:** load the relevant files and decisions when needed, give
specialists enough context to work, and keep compact findings with source paths.
**Workflow graphs:** start independent work together, wait for real dependencies,
and pass the specific output the next step needs. The lead keeps this structure
in its plan; you do not configure a graph database or assign an agent hierarchy.

[See a concrete handoff and dependency example →](docs/how-it-works.md#context-and-dependencies)

## Versions

**Use now:** GitHub `main` — current kernel, no tagged ZIP yet.
**Last tagged package:** [candidate.8](https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.8)
skill and plugin ZIPs (older runtime).

What each check actually covers is in the [evidence guide](docs/evidence.md).
General gains in cost, speed or quality are **not established**. The CI badge
reports public `main`.

## Choose the right tool

AMC fits when you want adaptive execution **inside your coding assistant**.
A desktop coordination platform fits when you need a separate live board and
workspace UI. A model profile fits when you want explicit role/model presets.

[Compare AMC, Agent Orchestrator and Codex Astra/Luna by user need →](docs/choosing.md)

## Find your next answer

| I want to… | Go to… |
|---|---|
| Install, select or troubleshoot | [Getting started](docs/getting-started.md) · [Hosts](docs/hosts.md) |
| Do useful work | [Task recipes](docs/task-guide.md) |
| Understand the workflow | [How it works](docs/how-it-works.md) |
| Compare tools or inspect evidence | [Choosing](docs/choosing.md) · [Evidence](docs/evidence.md) · [Field state](docs/field-state.md) |
| Contribute | [Development](docs/development.md) · [Contributing](CONTRIBUTING.md) |

The full folder map is [docs/README.md](docs/README.md). Optional host mappings:
[intent profiles](examples/profiles.md) · [Codex example](examples/codex/README.md).

## Built in the open

AMC draws on Context Diamond, AVO, SkillOpt, practical orchestrators and lab
research. The current map is [field state](docs/field-state.md).
[Sources](docs/sources.md) list what we adapt;
[research-basis](docs/research-basis.md) is the longer archived review.
These sources are not extra installations or endorsements.

Try a useful task and [share what happened](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml).
One concrete example helps: the goal, what the agent did, the result you checked
and where you had to intervene. Remove private information before sharing.

[Development history](docs/history/through-candidate.8.md) · [Historical evaluations](evals/README.md) ·
[Security](SECURITY.md) · [MIT license](LICENSE)

Made by **[Byens IT](https://byens-it.dk)** for people building with AI.
