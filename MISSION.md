schema_version: 1
overall: NOT VERIFIED

# Adaptive v0.2 candidate

## Goal / Definition of Done

A portable selective runtime, conditional references, safe same-source packages,
realistic behavioral evals and independent proof. The local implementation is
complete. Behavioral superiority requires controlled subject runs and remains
NOT VERIFIED; no static test is substituted for that gate.

## Base and candidate

Public v0.1.0/main: `fdbf07fa3443ca454509ca36ace6e2651b9fc2e6`.
Local parent: `358680dd4fedb3faf38a4599d1e20ed9a376c0fd`, initially clean.
Branch: `codex/v0.2-adaptive`. The enclosing commit identifies this candidate.
The exact final commit/clean-worktree/scan proof is recorded externally after
commit creation to avoid self-referential hashes in this file.
Earlier candidate-1 results are explicitly historical.

## Hard gates

| Gate | Status | Evidence |
|---|---|---|
| Repository identity and intact baseline | PASS | Root HEAD/status/remote and baseline archive checks |
| Selective portable runtime and conditional references | PASS | Current files, structural checks, independent inspection |
| Same-source skill/plugin packages and integrity | PASS | 12 package tests, both official validators, cross-Python byte equality |
| Fixture isolation and structural safety | PASS | 25 negative controls and 11 tripled fixture preparations on Python 3.11/3.14 |
| Controlled behavior and superiority | NOT VERIFIED | Clean authenticated context unavailable; evals/README.md |
| Independent final review | PASS | Executed final code/eval review; status corrections in evals/final-review.md |
| Enclosing commit and clean delivery | NOT VERIFIED | Read actual enclosing Git state and external delivery report |

## Authority

Local edits, one safe branch, disposable fixtures, tests, repairs, read-only
sources, bounded agents and one local commit are authorized. No push, merge,
release, GitHub settings changes, live host installation, destructive cleanup
or permission bypass. Existing installed governing skills were not changed:
this repository is the explicitly requested offline product candidate.

## Jobs

| Job | Agent | Status | Owned scope |
|---|---|---|---|
| Primary source verification | source_review | completed | Five primary design sources, read-only |
| Packaging | packaging | completed | Builder and package tests |
| Eval design and feasibility | evals | completed | Cases/rubric/preparer/tests/eval README |
| Integration and proof | Lead | completed | Runtime, docs, validator, actual final checks |
| Independent final review | source_review | completed | Read-only final diff and executable checks |

All implementation scopes are returned to the lead. No worker is left writing.
The reviewer received requirements and artifacts, not implementation dialogue.
Missing controlled runs are not counted as completed agent jobs.

## Decisions and evidence

Evaluator SHA256(cases bytes || rubric bytes), frozen before runtime writes:
`2c4f07976eef82371c10029e17e985a4d515c95c246b5c02aae386440f3060ac`.

Candidate hypothesis: phase-specific references reduce irrelevant routing
constraints while retaining ownership and evidence. Correctness/safety take
precedence, then completed cases with no regressions. The new candidate is
retained for review, not accepted as a demonstrated optimization winner.

[The candidate log](evals/v0.2-candidate-log.md) records sources, comparison,
commands and package hashes. [The 33 records](evals/results/2026-09-11-adaptive.json)
bind identical inputs across three runtime snapshots. Zero controlled runs.
One noncontrolled CLI pilot completed a fixture heading; root verified its diff
and excluded it from comparative scoring. Model savings are not measured.

Root repaired Git-source/environment ambiguity, linked-ancestor escapes in
fixture preparation, and invalid activation JSON-type handling. All have
negative controls. A final Git archive byte check also caught host-dependent
line endings; .gitattributes now fixes text to LF and both autocrlf settings
produce identical source bytes. The original visual asset Git blobs are unchanged.

## Blockers

Default-profile prompt inspection still contains shared home instructions.
A clean temporary profile retains the target skill but its client request
failed HTTP 401 without authentication. The authenticated ephemeral pilot's
approval-review path also was not fully observed. A clean authenticated isolated
subject context has not been established without host auth/config setup.
These limits block behavioral acceptance, not completed local implementation.

## Next action

Read the enclosing commit and external delivery evidence for the final local
commit, clean-tree and secret-scan checks. The remaining behavioral gate needs
a clean authenticated isolated runtime.
Push, merge and release remain outside the current mandate.

## Last verified

2026-09-11: root executed relevant checks on Python 3.11.9 and 3.14.3.
Current runtime and evaluator hashes are in the linked comparison record.
Reconcile actual HEAD, dirty state and external delivery evidence on resume.
