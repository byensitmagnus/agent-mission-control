<p align="center">
  <picture>
    <source media="(max-width: 600px)" srcset="docs/assets/mission-path-mobile.svg" />
    <img src="docs/assets/mission-path.svg" alt="AMC workflow illustration: give the lead a goal; it chooses direct work or focused help, then integrates and verifies the result." width="100%" />
  </picture>
</p>

<h1 align="center">Agent Mission Control</h1>
<p align="center"><strong>Give your coding agent an outcome. Let it own the work through verification.</strong></p>
<p align="center">One workflow skill. Codex · Claude Code · Cursor · Grok · Kimi.<br />Use the models and tools your host actually provides.</p>

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
add value. There is no fixed team size or required model pairing, and no AMC
server to operate. Host tools and permissions determine what can actually run.

## Start in your project

1. **Install the project skill.** The [setup guide](docs/getting-started.md#1-install-the-skill)
   provides a copyable installation prompt and checksum check for the
   [published skill ZIP](https://github.com/byensitmagnus/agent-mission-control/releases/download/v0.2.0-candidate.8/agent-mission-control-skill.zip).
   This installs **candidate.8**. The [source installer](docs/hosts.md#install-the-current-source)
   adds checked installation for five hosts and
   [reviewed updates with a retained backup](docs/hosts.md#update-an-existing-project-installation).
2. **Select your project copy** of `agent-mission-control` using your
   [host's skill command](docs/hosts.md). The example below uses Codex. Keep your
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

## What is available and what is proven?

| Version | Status | Evidence |
|---|---|---|
| **candidate.4** | Earlier published skill and plugin ZIPs. | Package checks and a bounded Windows CLI skill-selection/first-use check for that version. |
| **candidate.7** | Retained review-ownership experiment; not a release download. | One controlled repair comparison: both versions passed 19 checks; candidate.7 also arranged independent acceptance review. |
| **candidate.8** | Current prerelease skill/plugin ZIPs; tagged source adds five-host install/check/update CLI and repaired evaluation/accounting tools. Runtime instructions match candidate.7. | [Engineering checks and native host observations](docs/engineering-candidate.8.md); complete cross-host work remains unverified. |
| **candidate.9** | Open PR source ([#6](https://github.com/byensitmagnus/agent-mission-control/pull/6)); not merged; no release ZIP. | Engineering checks PASS. Nine matched Codex runs: no unique correctness win; holdout slower/heavier. Audit notify-429 is not product evidence. Quality, time and price remain NOT VERIFIED. [Comparison results](evals/candidate.9/comparison/results/README.md). |

**General improvements in cost, speed, quality or user effort are not established.**
The [evidence guide](docs/evidence.md) explains what each check covers, host
limitations, earlier failures and how to evaluate AMC on your own work.
The CI badge reports public `main`. The release tag identifies the packaged
source; its `SHA256SUMS.txt` identifies the download bytes.

## Choose the right tool

AMC fits when you want adaptive execution **inside your coding assistant**.
A desktop coordination platform fits when you need a separate live board and
workspace UI. A model profile fits when you want explicit role/model presets.

[Compare AMC, Agent Orchestrator and Codex Astra/Luna by user need →](docs/choosing.md)

## Find your next answer

| I want to… | Go to… |
|---|---|
| Install, select or troubleshoot the skill | [Getting started](docs/getting-started.md) |
| Use Claude Code, Cursor, Grok, Kimi or Codex | [Host installation and real support limits](docs/hosts.md) |
| Give the agent a useful task | [Task recipes and expected delivery](docs/task-guide.md) |
| Understand delegation, review and recovery | [How it works](docs/how-it-works.md) |
| Choose optional role/model settings | [Advanced Codex profile](examples/codex/README.md) |
| Inspect results or contribute a change | [Evidence](docs/evidence.md) · [Development](docs/development.md) · [Contributing](CONTRIBUTING.md) |
| Continue evidence-led improvement work | [Reviewed code research and next checks](docs/research-priorities.md) |

## Built in the open

AMC draws on Context Diamond, AVO, SkillOpt, practical orchestrators and lab
research. [Source attribution and pinned references](docs/sources.md) explain
what we adapt; the [research review](docs/research-basis.md) records the reasoning.
These sources are not extra installations or endorsements.

Try a useful task and [share what happened](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml).
One concrete example helps: the goal, what the agent did, the result you checked
and where you had to intervene. Remove private information before sharing.

[Development history](docs/history/through-candidate.8.md) · [Historical evaluations](evals/README.md) ·
[Security](SECURITY.md) · [MIT license](LICENSE)

Made by **[Byens IT](https://byens-it.dk)** for people building with AI.
