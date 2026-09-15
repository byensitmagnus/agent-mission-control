# Working-tree review after F4 repair (not independent)

This is a second read-only review by the same AI lead that implemented the
queued-PASS repair and comparison runs. It is not an independent review.

- Date: 2026-09-14
- Tree: dirty `codex/unified-amc-kernel` on parent `76e62b1bfbbf01cd5032cb8bd6fc36ddcc09dc11`
- PR: https://github.com/byensitmagnus/agent-mission-control/pull/6 (open, not merged)
- Base: `c49dc1be2e334091f6c841047ff2ad778b7bde84`

## Verdict at inspection: FAIL

The working tree already forbade queued/running jobs under overall PASS, but
the public GitHub artifact was still `76e62b1`, the review note was untracked,
and the audit hidden check was not derivable from the visible prompt.

| Id | Severity | Finding | Reproduction | Repair in this PR tree |
|---|---|---|---|---|
| W1 | Critical | `docs/reviews/candidate.9-falsification.md` was untracked and claimed a follow-up commit SHA that did not exist | `git ls-files docs/reviews` empty; PR #6 had one commit | Track the review files; describe F4 as closed by later PR commits, not by a pre-existing SHA |
| W2 | High | Live GitHub HEAD still accepted optional queued under overall PASS | `76e62b1` `scripts/validate.py` | Later PR commits ship the queued/running prohibition and `pass_optional_queued` |
| W3 | High | Audit hidden required `429`, which the visible prompt did not name | `cases/audit.txt` vs `hidden/audit_check.py` | Document as development data of the same class as historical `c9-01` for notify; do not treat audit as product proof |
| W4 | High | Dummy overall PASS still possible with omitted unfinished jobs, or gate text `no completed subject results` / Authority `Unfinished work remains queued` | `make_pass_ready()` plus those strings | Reject those evidence/narrative phrases; remaining dummy PASS without listing the real work is still a schema limit |

## Checks re-run after repair

Lead-executed after the table above was repaired. Same agent, not independent.

- `python scripts/validate.py`
- `python scripts/test_validate.py`

## Remaining limits

- Validator contract-consistency only. Natural-language lies and omitted jobs
  can still produce overall PASS.
- Superpowers plugin loaded on every comparison arm (see
  [postmortem](../../evals/candidate.9/README.md)).
- `user_interventions` was recorded as 0 by protocol, not by a host event parser.
- Audit hidden originally required `429`, which the visible prompt did not name.
  Frozen launch `hidden_hash` was `bbe2a1a3…`. The checker was later edited for
  Danish `to gange`. Raw launch files were removed with the rest of the farm.
- Audit-direct originally stored `children: 7` from an older parser that counted
  Superpowers docs. Reparsed spawn items to `0`.
