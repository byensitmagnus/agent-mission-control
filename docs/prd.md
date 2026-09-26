# Product requirements and plan

Owner: Byens IT. Updated 2026-09-26. This is the current product definition. It
replaces the Danish [goal](../.claude/GOAL.md), whose exit gate is closed.

## Summary

AMC is one small Agent Skill that makes a coding agent's "done" trustworthy:

- **Right-sized work.** The agent picks the smallest workflow that fits.
- **Clean handoffs.** It hands off work completely when it delegates.
- **Independent approval.** It gets independent approval before it passes risky changes.
- **Proof at the end.** It finishes with the checks that actually ran.

It is Markdown that the host already understands. There is no server, no
runtime and no extra model.

## Problem

- **Unverified success.** Agents report success without running the checks, and users re-check by hand. Users of the most popular skill library ask for completion status after plan execution ([obra/superpowers#1075](https://github.com/obra/superpowers/issues/1075)).
- **Small models skip rules they must load.** In our smoke runs, Claude Haiku 4.5 opened only `SKILL.md` in 9 of 10 baseline runs. It approved a risky migration on its own tests in 5 of 7 runs across candidate.12 and .13 ([results](../evals/haiku-smoke-2026-09-25.md)).
- **Skills get skipped or cost context.** Skills that overlap trained behavior are skipped ([anthropics/claude-code#30387](https://github.com/anthropics/claude-code/issues/30387)), and large skills cost context ([anthropics/skills#1486](https://github.com/anthropics/skills/issues/1486)).
- **Delegation fails both ways.** It is either absent or a swarm. Extra agents cost tokens and coordination, and handoffs drop file paths.
- **No shared definition of done.** Hosts now ship strong loops: Claude Code's `/goal` and Stop hooks, and subagents on several hosts. What they lack is a portable definition of done, and of when a helper earns its cost.

## Users

| User | Job | Needs from AMC |
|---|---|---|
| Developer using Claude Code, Codex or Cursor daily | Finish real repository tasks without babysitting | A report they can trust, and no false "tests pass" |
| Team lead or skill author | One definition of done across hosts and models | Portable rules, a small footprint and honest limits |

## Principles

1. **Smallest workflow first.** Anthropic ([effective agents](https://www.anthropic.com/engineering/building-effective-agents)), [OpenAI](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) and [Google ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) all start simple.
2. **Evidence over claims.** Report what ran ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)).
3. **The author does not approve its own risky work.** A reviewer or a person does ([sources](sources.md)).
4. **Specific, falsifiable rules.** No generic "double-check" rituals: Anthropic's `/claude-api prompt-audit` flags them for current models.
5. **Verdict rules live in `SKILL.md`,** in plain words that small models follow ([skill authoring](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).
6. **Portable and small.** Follow the [Agent Skills spec](https://agentskills.io/specification). Host-native gates are optional add-ons.

## Requirements

The smoke case numbers refer to the [Haiku smoke cases](../evals/haiku-smoke-2026-09-25.md).

| ID | Requirement | Acceptance | Smoke case |
|---|---|---|---|
| R1 Honest report | Every task ends with the result, changed files, the checks that ran (command and outcome), what stays unverified, and one status: PASS, FAIL, BLOCKED or NOT VERIFIED | Every check the report claims appears as an executed command. Missing evidence is NOT VERIFIED; an observed failure is FAIL | 01, 02, 07, 09 |
| R2 Smallest workflow | Understood sequential work stays with the lead. Helpers are for fresh context, expertise or independent jobs. Parallel writers are isolated | Small cases stay direct. Independent jobs are delegated, or the lead says in one line why not | 01, 02, 04; 03 (failing) |
| R3 Complete handoff | Each delegated job gets the working folder, exact input paths, a write scope and an acceptance check. The lead waits for every result | No worker reports missing inputs. The final report integrates or names every result | 03 (failing) |
| R4 Independent approval | Release, migration or data-loss risk needs an approval of the current artifact, by a reviewer agent or a person, before PASS | No PASS or "approved for release" without that approval | 08 |
| R5 Safe resume | Before trusting a saved record, compare it with Git (or file digests) and rerun stale checks | A stale PASS is reported as NOT VERIFIED and rechecked | 05 |
| R6 Authority | Continue authorized local work. Stop before unauthorized external or destructive steps | No push, publish or deploy without a mandate | 10, 11 |
| R7 Footprint | `SKILL.md` has at most 200 lines and 12 KB (about 3,000 tokens). The description has at most 240 characters, and there are at most 20 installed files. One-line install through `npx skills` and the Claude Code plugin marketplace. No runtime dependency | `validate.py` enforces the limits. Public install checks pass for each release | validator |
| R8 Honest claims | Public text claims only measured results, and smoke is labelled smoke | An independent review of each release text | review |

## Non-goals

- A runtime, daemon, dashboard, scheduler or graph engine.
- A swarm by default, or fixed role and model presets as identity.
- Claims of lower cost, higher speed or better quality without external evidence.
- Large evaluation campaigns. The quality plan below is the whole proof budget.
- Mandatory hooks. Any host gate is opt-in.
- Replacing host loops such as `/goal`. AMC defines done; the host runs the loop.

## Quality plan

Proof has to fit a small team, so AMC relies on published practice, logic and small checks:

- **Every runtime change:**
  - `validate.py`, the unit tests and CI must pass;
  - one independent read-only review of the diff, by a cheaper reviewer model or a person;
  - release only after that approval (R4 applies to AMC itself).
- **Smoke:** for each changed rule, run 3 Haiku runs on the mapped case and 1 Sonnet run, scored with the frozen scorer. Record the result as smoke, never as proof, and never as a headline based on one run.
- **Prompt audit:** when rules change, run Anthropic's prompt audit on `SKILL.md`. Keep the explicit rules that small models need.
- **Public install check for each release:**
  - checksums and the fingerprint of the extracted skill;
  - skill discovery through `npx skills add --list`;
  - an isolated plugin install.

## Metrics

- **Adoption:** GitHub stars, skills.sh installs, a plugin-directory listing, and experience reports.
- **Behavior smoke:** passes per case and model, for each release.
- **Footprint:** `SKILL.md` lines and bytes, and the number of installed files.

## Research basis

Checked on 2026-09-26 with the GitHub API and the linked pages. Star counts are rounded and move over time. Pins for the sources AMC adapts are in [sources](sources.md).

| Source | Signal | Reuse | Reject |
|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers/tree/8ca22dba9a94f28898bbce59f2537ff4d87c747d) | ~292k★, MIT | An excuses table. A reviewer briefed with the requirement and commit range, never the session history | Its full brainstorm-to-TDD methodology; AMC stays one skill |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | ~99k★, MIT | Install breadth: `npx skills` plus a marketplace | A lifecycle command set |
| [anthropics/skills](https://github.com/anthropics/skills) and the [Agent Skills spec](https://agentskills.io/specification) | ~178k★; the spec | Frontmatter limits and progressive disclosure | — |
| [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | ~27k★, MIT | An opt-in Stop-hook completion gate that reads a file and never runs commands from Markdown. Input for M6 | Always-on hooks |
| [vercel-labs/skills](https://github.com/vercel-labs/skills), [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | ~33k★, ~37k★ | Distribution: `npx skills` and the official plugin directory | — |
| Anthropic docs: best practices, skill authoring, effective agents, hooks | official | A verification subagent, shown evidence, simplicity, visible planning steps, Stop hooks | — |
| OpenAI practical guide; Codex skills and hooks | official | A single agent first, and human oversight for high-risk actions | — |
| Google ADK multi-agent patterns | official | Generator and critic. A human authorizes irreversible actions | A graph runtime as a dependency |
| [NVIDIA AVO](https://arxiv.org/abs/2603.24517) | paper | Execution feedback as the judge in optimization work | It does not cover release approval |
| X: a Claude Code `/goal` and Stop-hook guide (38K views); `/claude-api prompt-audit` (194K views on a quote) | community | Pair AMC with host loops, and avoid verification rituals | — |

## Where AMC stands

**Working:**
- Both install paths are checked for each release.
- 70 validator negative controls, and CI on Linux and Windows.
- Checksummed releases, recorded sources and honest limits.
- Anthropic's prompt audit (2026-09-26) found no stale or duplicated rules. It flagged three idioms in the release gate (the IMPORTANT marker, the numbered steps and the excuses table); all three stay as scoped fixes for a measured small-model failure ([record](evidence.md)).

**Gaps:**
1. **R4 on small models:** 2 of 7 across candidates .12 and .13; on candidate.15 the whole case passed in 1 of 3, and on candidate.16 in 2 of 3 (smoke). One candidate.16 run still reported PASS without independent review. A candidate.15 Sonnet run held, and its reviewer caught a real bug. R4 remains open.
2. **R2 and case 03:** the delegation reason was written in 0 of 3 candidate.15 Haiku runs and 2 of 3 candidate.16 runs.
3. **Report form:** candidate.16's fixed template appeared in all seven final smoke runs, mostly fixing the missing-field problem. A filled template can still contain a false PASS.
4. **No demo:** the README shows no real report.
5. **Front door:** about 40 Markdown files, roughly half of them history or development material.

## Plan

| Milestone | Deliverable | Owner | Done when |
|---|---|---|---|
| M1 | Candidate.14 release gate | Lead | Released 2026-09-26 |
| M2 | This PRD | Lead; cheaper-model review | Merged 2026-09-26 |
| M3 | Candidate.15, with three parts:<br>• the four deferred points;<br>• a one-line reason when independent jobs stay with the lead (R2);<br>• an R7 budget in `validate.py` | Lead; independent reviewer | The review approves. Smoke: 3 Haiku runs each on cases 08 and 03, plus 1 Sonnet run on 08. Released |
| M3b | Candidate.16: a fixed final-report template. The status is limited to the four values, with `Review:` and `Delegation:` fields | Lead; independent reviewer | Smoke on cases 08 and 03 shows the template followed. Released |
| M4 | Front door: the README leads with the pain and a real report excerpt from an M3 smoke run, plus footprint numbers. The docs map separates current docs from the archive | Lead drafts; review | Merged |
| M5 | Distribution: plugin-directory submission, one X post per concrete lesson, an r/ClaudeCode tip, a dev.to article, and Show HN once a demo exists | Magnus submits and posts to Reddit and HN; the lead drafts. X posts go out only after Magnus approves the text | Submitted or posted |
| M6 | Optional completion gate on hosts with Stop hooks | Lead evaluates | Considered only if the M3b template leaves R1 or R4 failures on Haiku, and the gate fits in about 50 lines, is opt-in and runs no commands |

M3b implementation and smoke are complete on `claude/candidate-16`; its
independent review and release remain open.

## Exit gate: routine use, then maintenance

AMC is ready to leave active development when all four checks below pass on
one identified release. Closing the project means maintaining that release,
not claiming AMC is generally faster, cheaper or more accurate than direct work.

1. **One current artifact.** The reviewed commit, tagged skill/plugin ZIPs,
   checksums, documented version and selected daily-use installation agree.
   Installation and rollback checks pass. No page links to a nonexistent tag.
2. **Risk stays controlled.** Engineering checks and an independent review pass
   on the release artifact. Decide M6 against the known false-PASS case: an
   opt-in host check must reject unsupported high-risk PASS without blocking
   honest NOT VERIFIED or ordinary direct work. A Stop hook alone is not the
   release authority; host permissions, CI and review protect actual release.
   If the check cannot meet this contract, keep R4 open and narrow the public
   claim instead of calling the project complete.
3. **Real work succeeds.** Use the same installed release on three naturally
   occurring commissioned tasks: one small direct task, one multi-step or
   resumed task, and one with release, migration or data-loss risk. Inspect the
   delivered artifacts and recorded checks. Require no known false PASS or
   lost authorized work; record user intervention, elapsed time and reviewer
   effort. These observations establish owner readiness, not a general gain.
4. **A usable front door.** README shows one real report and a short install
   path; evidence and host limitations are accurate. One outside reader can
   install the release and understand what PASS does and does not mean.

After these checks, record the accepted version and proof in project status,
switch to maintenance, and change AMC only for a reproducible defect, a host
compatibility change or a concrete user need. M5 promotion is separate from
this product exit gate.

## Operating model

- **The lead** makes decisions, integrates work, verifies results and releases.
- **Cheaper models do the bulk work:**
  - Sonnet does research, drafts and independent review;
  - Haiku does inventory and serves as the smoke subject.
- At most three workers run at once. Workers never approve their own output.
- **Authority:**
  - Merges and releases need an explicit mandate in the current session ([AGENTS.md](../AGENTS.md) rule 2) and must pass the quality plan.
  - Reddit, HN and directory submissions are Magnus's.
  - X posts need his approval of the text.

## Decisions

1. **D1:** this PRD replaces the Danish goal as the product definition.
2. **D2:** case 03 stays. Candidate.15 makes the lead state a one-line routing reason instead of forcing delegation (Anthropic: make planning steps visible).
3. **D3:** the core skill has no hooks. M6 decides on an opt-in gate from evidence.
4. **D4:** the four statuses stay: PASS, FAIL, BLOCKED and NOT VERIFIED.
5. **D5:** proof means engineering checks, one independent review and small smoke runs. No campaigns.
