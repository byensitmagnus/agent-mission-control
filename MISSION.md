schema_version: 1
overall: NOT VERIFIED

# Daily-use readiness

## Goal / Definition of Done

Deliver the practical exit gate in [.claude/GOAL.md](.claude/GOAL.md): an
approachable portable skill that takes a requested outcome through appropriate
work, useful handoffs, integration and inspectable evidence. One usable host
path and one real commissioned task are sufficient; comparative performance
research is outside this delivery.

## Base and candidate

Baseline: `main` `3f35485679ad906fd900faaba9c1d1f2786b80a3`, read on 2026-09-24.
Current artifact: candidate.11 runtime SHA-256 `4301eefdf4768522cd7d924bcbdc3f88c424f270eb14042ade5ceb6e0b6a52f8`.
Source work is on `codex/usage-readiness`, based on `3f35485`.
Runtime identity: `0.2.0-candidate.11`; candidate.10 belongs to an older
contract draft. Last tagged ZIP remains candidate.8.

## Hard gates

Priority order: preserve user work and authority; correct installed behavior;
coherent workflow; usable first task; clear presentation. No score for extra
agents, files, rules or research. Keep a candidate only when a declared failure
becomes PASS without regressing a higher-priority gate.

| Gate | Status | Evidence |
|---|---|---|
| Preserve work and product boundary | PASS | Six original dirty files preserved; isolated worktrees; portable runtime; no global changes |
| Coherent core and package | PASS | Routing and handoffs reconciled; independent review; Windows/Linux checks and both built-package link checks pass |
| GitHub and first-use path | PASS | Useful outcome prompt, corrected discovery guidance, retained artwork and rendered wide/390-pixel local previews; published view belongs to final delivery |
| Current host use | PASS | Exact project install MATCH; explicit native skill input; Codex 0.156.1 read the installed skill and two current docs with one approved read command; lead checked the returned contents and report |
| Real deliverable and publication | NOT VERIFIED | Real acceptance review and repairs completed; authorized publication, remote CI and final main-based project install remain open |

## Frozen evaluator and candidate lineage

Frozen baseline: preservation PASS (separate worktree and six dirty files
retained); coherence FAIL (conflicting specialist prerequisites and two broken
packaged links); first use FAIL (README quiz called selection proof); native
task loading and final delivery NOT VERIFIED. This is a five-gate acceptance
rubric, not an agent-quality score.

Baseline engineering rerun: Python 3.12.8 under WSL, byte-identical clone of
`3f35485`: validator PASS, package 14/14, installer 13/13, decision kernel 36/36.
These checks do not validate agent behavior. Baseline Codex native discovery
lists the project skill separately from an older personal copy. Baseline runtime
SHA-256: `6708acc7c6a1bc1b62e5aea7711e5e04804aef5cb05fbbfeb1a1f741f61f69b3`.

Attempt budget: one integrated readiness candidate, followed by at most two
evidence-directed repair passes per unresolved defect. Repeated failure triggers
diagnosis and a new bounded hypothesis, not abandonment of executable work.

| Candidate | Parent | Hypothesis/change | Correctness | Score | Evidence | Verdict/diagnosis |
|---|---|---|---|---|---|---|
| Baseline | `3f35485` | Existing daily-use goal | Structural checks pass; two known product gaps | 1/5 gates established | Baseline observations above | Retain as recoverable baseline |
| Readiness | Baseline | Repair routing, package links, Windows path identity and first use | Relevant engineering checks and approved native read PASS | 4/5 gates established | [Dated review](docs/reviews/readiness-2026-09-24.md) | Retain repairs; publication pending; no overall PASS or performance claim |

## Authority

Authorized: complete local audit, goal, implementation, targeted checks and a
project-scoped native-use observation. On 2026-09-24 the user accepted the
recommended publication flow: push the reviewed branch, open a PR and merge
after green GitHub checks and review. Tagged release, global installation,
host configuration changes and a subject-run farm are outside this mandate.

## Jobs

| Job | Agent | Required | Lifecycle | Verdict | Writable owned scope |
|---|---|---|---|---|---|
| Full repository and source audit | Lead + three auditors | yes | completed | PASS | none; audit covered 159 files, history, PR #7–10 and six local edits |
| Runtime and handoffs | Runtime specialist; lead integration | yes | completed | PASS | SKILL.md, references/, templates/, agents/, examples/ |
| Packaging and checks | Engineering specialist; lead verification | yes | completed | PASS | scripts/, evals/decision_kernel.py, .github/workflows/validate.yml |
| Source decisions | Source specialist | yes | completed | PASS | docs/field-state.md, docs/sources.md, docs/choosing.md |
| Presentation, native use and acceptance | Lead | yes | running | NOT VERIFIED | README.md, remaining docs/, .claude/GOAL.md, MISSION.md |

## Decisions and evidence

Keep one lead and the three routes. Specialists may help through expertise or
fresh context; real dependencies carry a named artifact. Concurrent writers use
host isolation. Templates preserve writable ownership and current evidence
identity. The host owns execution, permission enforcement and discovery.

Adapt bounded mechanisms from OpenAI, Anthropic, Google ADK, NVIDIA AVO, Agent
Orchestrator and CALO. Source guidance is not proof of AMC outcome gains.
PR #8's Guard and PR #9's Orca/claim runtime are not core dependencies. Preserve
historical negative findings in [evidence](docs/evidence.md) and the
[candidate.9 postmortem](evals/candidate.9/README.md).

The [dated review](docs/reviews/readiness-2026-09-24.md) records the full audit,
source decisions, checks, package identities and native-use limits. All delegated
writers finished in separate worktrees before integration. Final reviewers are
read-only; they have no write ownership. Review findings were checked by the
lead, including rejection of the alleged `None.` validator failure because the
actual contract accepts a trailing period.

## Blockers

No external authorization blocker remains for the reviewed publication flow.
Remote checks, merge and the final main-based project installation are pending.
The native file-read issue was resolved through a normal one-command approval
within the already authorized audit scope, after removing stale inherited
Desktop identity hints from the child process. No persistent permission, ACL or
host configuration changed. Unassisted Windows sandbox reads and desktop/IDE
picker interaction were not established and are not claimed.

## Next action

Open the PR for the pushed branch and merge after remote checks and review.
Then inspect the published rendering and install
the accepted main source in the agreed project. A draft PR alone is not the exit
gate; preserve the pending final-delivery job until these steps are complete.

## Last verified

Baseline source `3f35485`; candidate runtime
`4301eefdf4768522cd7d924bcbdc3f88c424f270eb14042ade5ceb6e0b6a52f8`.
Local engineering checks, exact install/package hashes, rendered preview and
native explicit invocation and approved file read observed 2026-09-24.
UTC checkpoint: 2026-09-24 09:25:34.
Publication and the final main-based project installation are not verified.
