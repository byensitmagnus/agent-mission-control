<p align="center">
  <picture>
    <source media="(max-width: 600px)" srcset="docs/assets/mission-path-mobile.svg" />
    <img src="docs/assets/mission-path.svg" alt="AMC workflow illustration: give the lead a goal; it chooses direct work or focused help, then integrates and verifies the result." width="100%" />
  </picture>
</p>

<h1 align="center">Agent Mission Control</h1>
<p align="center"><strong>Give your coding agent an outcome. It chooses the smallest graph that can finish and prove the work.</strong></p>
<p align="center">One portable skill. Codex · Claude Code · Cursor · Grok · Kimi.<br />No extra server. Delegate only when a job earns its cost.</p>

<p align="center">
  <a href="docs/getting-started.md"><strong>Get started →</strong></a> ·
  <a href="docs/task-guide.md">Pick a task</a> ·
  <a href="docs/how-it-works.md">How it works</a> ·
  <a href="docs/evidence.md">Results &amp; limits</a>
</p>

<p align="center">
  <a href="https://github.com/byensitmagnus/agent-mission-control/actions/workflows/validate.yml"><img src="https://github.com/byensitmagnus/agent-mission-control/actions/workflows/validate.yml/badge.svg?branch=main" alt="Public main engineering checks" /></a>
  <a href="https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.8"><img src="https://img.shields.io/badge/download-candidate.8-2c568c" alt="Published download: candidate.8" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2c568c" alt="MIT license" /></a>
</p>

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

Small tasks stay with the lead. Larger tasks can use native subagents when they
add value. A stronger lead may delegate bounded jobs to cheaper workers only
when the work is independent, isolated and cheap to verify. That pairing is
optional, not AMC's identity. Host tools and permissions determine what can
actually run.

## Start in your project

1. **Install the project skill** from the
   [published ZIP](https://github.com/byensitmagnus/agent-mission-control/releases/download/v0.2.0-candidate.8/agent-mission-control-skill.zip)
   using the [setup guide](docs/getting-started.md#1-install-the-skill). That is
   **candidate.8**. Five-host checked install and update live in
   [hosts.md](docs/hosts.md#install-the-current-source).
2. **Select the project copy** with your
   [host command](docs/getting-started.md#2-select-the-installed-copy). Keep your
   current model and normal permissions.
3. **Try this read-only task** in a project with a README:

```text
$agent-mission-control

Read README.md. In at most three bullets, explain its purpose,
one useful task and one limitation. Cite the section heading for each.
Do not change files, install anything, run project checks or delegate.
Say explicitly that no checks were run.
```

**A successful first result:** three supported points, references you can find,
no changed files and an explicit “no checks run.” This checks basic use;
your project's working behavior needs its own tests.

**Then use it on work you need done:** [fix a bug](docs/task-guide.md#fix-a-bug),
[build a feature](docs/task-guide.md#build-a-feature),
[resume unfinished work](docs/task-guide.md#resume-unfinished-work) or
[research code without changing it](docs/task-guide.md#research-code-without-changing-it).
Each recipe includes a prompt and what to inspect when it finishes.

## Know what “done” means

The lead should show **what changed, which checks actually ran, and what remains**.
A worker finishing is one input to that decision. Confirmed failures need repair;
missing evidence must stay visible. Long tasks keep a recoverable mission record.

An illustrative delivery can be as short as:

> **Fixed:** zero is retained in the exported total.<br>
> **Checked:** regression and existing export checks passed.<br>
> **Scope:** export formatting changed; no deployment performed.

This is an output example, not a measured run.
[Follow a complete task and delivery example →](docs/task-guide.md#what-a-completed-delivery-looks-like)

## Versions

**Use now:** [candidate.8](https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.8)
skill and plugin ZIPs, with checksums.
**Next source:** [PR #6](https://github.com/byensitmagnus/agent-mission-control/pull/6)
unified kernel — not merged, not a quality or price claim.

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
