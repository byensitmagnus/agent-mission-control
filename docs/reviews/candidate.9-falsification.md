# Candidate.9 PASS-rule falsification review

This is a public engineering review of the mission validator. It is not a
product-quality claim and not an independent human review.

- Reviewer: AI agent (Grok 4.6), read-only pass then lead repair
- Scope: `overall: PASS` rules, plugin copy, packaging identity, research claims
- Inspected commit: `76e62b1bfbbf01cd5032cb8bd6fc36ddcc09dc11` on
  `codex/unified-amc-kernel`, PR https://github.com/byensitmagnus/agent-mission-control/pull/6
- Base: `c49dc1be2e334091f6c841047ff2ad778b7bde84`

An internal session id `2d743209-53f4-45f0-97d1-390d848244ae` is not a GitHub
object. This file in the PR tree is the reopenable record.

## Findings on `76e62b1`

| Id | Severity | Finding | Reproduction | Repair |
|---|---|---|---|---|
| F1 | Critical | Live `MISSION.md` could be flipped to overall PASS while a superiority gate still said `evals/v3 has no subject runs` | Copy repo; set `overall: PASS`; set that gate Status to PASS without changing evidence; mark queued required jobs completed | `UNVERIFIED_EVIDENCE` rejects `no subject runs` / `not yet verified` / `no executed` on PASS gates |
| F2 | High | Artifact identity `2026` matched a timestamp substring | Pass-ready mission with Current artifact `2026` | PASS identities need length ≥ 16, a letter and a digit, and must not be a date prefix |
| F3 | High | `Blockers: None.` plus `Next action: Blocked: …` was accepted | Pass-ready template Next action replaced with `Blocked:` | PASS forbids `\bblocked\b` in Next action |
| F4 | High | Dummy required PASS + optional queued unfinished work was accepted | Pass-ready plus optional queued row | Closed after `76e62b1` on this PR: PASS forbids all queued/running jobs |
| F5 | Medium | Plugin synonym scan is narrow | Not exploited in the shipped copy | Current SKILL/plugin text already requires smallest useful execution graph |

F1–F3 were closed on `76e62b1` and re-probed (`ATTACK_RC 1`: missing hard-gate
evidence). F4 remained on that commit. Later commits on this PR, not `76e62b1`
itself, forbid queued and running jobs under overall PASS and add negative
controls. Do not treat this file as proof of a SHA that had not been created
when the finding was written.

## Re-run checks after F4 repair

Recorded with the PR tree that contains this file:

- `python scripts/validate.py`
- `python scripts/test_validate.py`

The checker tests Markdown contract consistency. It cannot prove that
natural-language evidence is true or that the named artifact equals git HEAD.

## Remaining limits

- A dummy required PASS job can still exist if unfinished work is omitted from
  the Jobs table or superseded with a reason. Completeness of the *real* work
  is not a schema property.
- `evals/decision_kernel.py` is a JSON regression fixture, not runtime
  enforcement of agent behavior.
- Bound comparison results are summarized in
  [candidate.9 postmortem](../../evals/candidate.9/README.md).
  They are not a general quality, cost or speed claim. Raw JSONL was removed.
