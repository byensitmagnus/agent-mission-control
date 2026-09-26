<p align="center">
  <picture>
    <source media="(max-width: 600px)" srcset="docs/assets/mission-path-mobile.svg" />
    <img src="docs/assets/mission-path.svg" alt="Illustration, not a recorded run: a lead takes a goal, chooses direct work or a specialist or parallel help, then integrates and verifies." width="100%" />
  </picture>
</p>

<h1 align="center">Agent Mission Control</h1>
<p align="center"><strong>Stop babysitting your coding agent.</strong><br />
One skill that helps the agent choose the right amount of help,<br />and show which checks actually ran before it says “done”.</p>

<p align="center">
  <a href="https://github.com/byensitmagnus/agent-mission-control/actions/workflows/validate.yml"><img src="https://github.com/byensitmagnus/agent-mission-control/actions/workflows/validate.yml/badge.svg?branch=main" alt="Public main engineering checks" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2c568c" alt="MIT license" /></a>
  <img src="https://img.shields.io/badge/Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor%20%C2%B7%20Grok%20%C2%B7%20Kimi-skill-6d4aff" alt="Agent Skill for Claude Code, Codex, Cursor, Grok and Kimi" />
</p>

**Agent Mission Control (AMC)** is an open-source agent orchestration skill for
AI coding agents. In Claude Code, Codex, Cursor, Grok or Kimi, it helps one lead
choose direct work, a scoped specialist or independent parallel jobs, then
check the current artifact and report what remains uncertain.

```bash
npx skills add byensitmagnus/agent-mission-control
```

<p align="center">16 small files (about 60 KB). No server, no API key, no extra model.<br />
<a href="docs/getting-started.md"><strong>Get started →</strong></a> ·
<a href="docs/task-guide.md">Task recipes</a> ·
<a href="#the-workflow-at-a-glance">See the workflow ↓</a> ·
<a href="docs/evidence.md">Results &amp; limits</a></p>

## Why

Coding agents tend to fail in three familiar ways. AMC gives the lead agent one
rule set for each:

| What goes wrong | What AMC tells the lead to do |
|---|---|
| **A swarm for a one-line fix.** Five subagents, five context dumps, one tiny change. | Keep small work direct. Delegate only when a job earns its coordination cost. |
| **“All tests pass”** when no test ran. | Report only checks that actually ran on the current artifact. Missing proof stays **NOT VERIFIED**. |
| **Lost after a long session.** The context fills up and work starts over. | Keep a compact mission record and reconcile it with the files before trusting it. |

## The workflow at a glance

AMC helps the lead pick the smallest useful route, integrate the work, check
the current artifact and report an evidence-based status. Review is added when
risk or an unresolved finding calls for it; confirmed fixes go through the
checks again.

```mermaid
flowchart TD
  A["Coding task<br/>goal · limits · done when"] --> B{"Which route adds value?"}
  B -->|small or sequential| C["Lead works directly"]
  B -->|focused gap| D["One scoped specialist"]
  B -->|independent jobs| E["Parallel help<br/>isolate writers"]
  C --> F["Lead integrates current artifact"]
  D --> F
  E --> F
  F --> G["Run relevant checks"]
  G -->|failed check: repair| F
  G --> H{"Risk or missing proof?"}
  H -->|yes| I["Fresh independent review"]
  H -->|no| J["Report evidence and limits"]
  I -->|confirmed finding: repair| F
  I --> J
  J --> K["PASS · FAIL · NOT VERIFIED · BLOCKED"]
```

The diagram shows possible routes, not a mandatory pipeline or a measured
outcome. A reported PASS is advisory; your host and reviewer control risky
actions such as release or migration. [Detailed workflow →](docs/how-it-works.md)

## Three routes, one lead

The lead picks the smallest route that can finish the job and changes route
when new evidence says so:

1. **Direct.** The lead edits, checks and finishes. This is the default.
2. **One specialist.** A bounded job gets focused expertise or a fresh context.
   The handoff names inputs, write scope and the acceptance check.
3. **Parallel.** Only for jobs that do not need each other's output. Parallel
   writers need host isolation such as worktrees.

The lead owns integration and the final verdict: **PASS**, **FAIL**,
**NOT VERIFIED** or **BLOCKED**. A worker saying “done” is input, not acceptance.

## Start in 30 seconds

1. **Install** in your project: `npx skills add byensitmagnus/agent-mission-control`.
   As a Claude Code plugin instead: `/plugin marketplace add https://github.com/byensitmagnus/agent-mission-control`,
   then `/plugin install agent-mission-control@amc`.
   Prefer Git + Python or plain copy? See [other install paths](docs/getting-started.md#1-install-the-skill).
2. **Select it:** `/agent-mission-control` in Claude Code (`/agent-mission-control:agent-mission-control`
   if installed as a plugin), `$agent-mission-control` in Codex, `/` in Cursor. [All hosts](docs/getting-started.md#2-select-the-installed-copy).
3. **Give it work you already need** (`$` is Codex syntax; use your host's command from step 2):

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

## What “done” looked like in one smoke run

In a disposable migration case, the first independent reviewer rejected a
parity check: Python treats `0 == False` as true, so a wrong-type value could
pass. The agent repaired the check, reran it and got approval on the changed
artifact. Condensed from the [candidate.15 Sonnet run](evals/haiku-smoke-2026-09-25.md#candidate15-smoke-2026-09-26):

```text
Result: preserve false and zero settings through migration
Changed files: migrate.py, verify_migration.py
Checks run: python verify_migration.py -> parity, rollback and corruption controls passed
Not verified: record fields outside the fixture's ID and settings; no production release
Delegation: independent review for migration risk
Review: first REJECT (0 == False); after repair, APPROVE on the changed files
Status: PASS
```

PASS here is for the disposable fixture only. This is one smoke observation,
not a production run or proof that AMC improves
quality generally. The run also started a second reviewer beyond the intended
one-review ceiling.

If someone will run a generated script or installer, that file is what gets
checked. A green check on the source alone leaves the package NOT VERIFIED.
[Full delivery example →](docs/task-guide.md#what-a-completed-delivery-looks-like)

## Built with itself

AMC is developed with AMC. The
[readiness review](docs/reviews/readiness-2026-09-24.md#product-outcome-and-workflow-trace)
traces one real delivery: scoped jobs in separate worktrees, a review that
returned four findings (three confirmed and repaired, one rejected against the
actual code), then merge after green CI. It is an observed trace, not a benchmark.

## Honest limits

- AMC's `PASS` is an agent's evidence claim, not permission to release or run a
  migration. For high-risk work, check the actual independent review of the
  current artifact and use host permissions and CI for the consequential step.
  Candidate.16 smoke produced false high-risk PASS reports from Haiku and
  Sonnet. In the Sonnet run, an approved parity checker accepted `false` changed
  to numeric `0` as unchanged. Treat every model's release verdict as advisory.
  [Supported use](docs/prd.md#supported-operating-envelope).
- General gains in cost, speed or quality are **not established**. We do not
  claim them. [What was actually checked](docs/evidence.md).
- AMC is instructions. Your host decides which tools, subagents and permissions exist.
- Small models need the rules in plain sight. With Claude Haiku 4.5, 9 of 10
  repository cases passed after the verdict rules moved into `SKILL.md` (7 of 10
  before). One run per case. Haiku still approved a risky migration on its own
  tests in 5 of 7 runs across candidate.12 and .13. On candidate.15 the whole
  migration case passed in 1 of 3 runs; one started an independent reviewer.
  Candidate.16's fixed report template was used in all seven final smoke runs.
  The migration case passed in 2 of 3, but one still reported PASS without
  independent review. The delegation reason appeared in 2 of 3 case 03 runs,
  versus 0 of 3 on candidate.15. These are smoke results, not a reliability
  claim. [Haiku results](evals/haiku-smoke-2026-09-25.md)
  In the candidate.16 Sonnet case 08 run, the final report also said
  `Delegation: none` despite using a reviewer agent.
- The CI badge covers engineering checks on `main`, not agent behavior.

## Pick the right tool

AMC fits when you want adaptive execution **inside the coding assistant you
already use**. A desktop coordination platform fits when you want a separate
live board. A model profile fits when you want fixed role/model presets.
[Compare by need →](docs/choosing.md)

| I want to… | Go to… |
|---|---|
| Install, select or troubleshoot | [Getting started](docs/getting-started.md) · [Hosts](docs/hosts.md) |
| Do useful work | [Task recipes](docs/task-guide.md) |
| Understand the workflow | [How it works](docs/how-it-works.md) · [The skill itself](skills/agent-mission-control/SKILL.md) |
| Inspect evidence and sources | [Evidence](docs/evidence.md) · [Field state](docs/field-state.md) · [Sources](docs/sources.md) |
| See where AMC is going | [Product requirements and plan](docs/prd.md) |
| Contribute | [Development](docs/development.md) · [Contributing](CONTRIBUTING.md) |

**Versions:** the installs above use `main`. For a tagged ZIP, use the
[latest release](https://github.com/byensitmagnus/agent-mission-control/releases/latest)
and verify its checksums. Candidate.16's report template has a documented
false high-risk PASS; any release of it is a report-format/workflow beta with
advisory PASS, not an enforced release gate.
The docs map is [docs/README.md](docs/README.md).

## Help it get better

Tried it on real work? [Share what happened](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml):
the goal, what the agent did, the result you checked and where you had to step
in. Remove private information first. If AMC saved you a babysitting session,
a ⭐ helps other developers find it.

[Security](SECURITY.md) · [MIT license](LICENSE) ·
[Development history](docs/history/through-candidate.8.md)

Made by **[Byens IT](https://byens-it.dk)** for people building with AI.
