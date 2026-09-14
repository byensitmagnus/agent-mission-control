# Candidate.9 bounded comparison protocol

Frozen 2026-09-14 before subject launch. This protocol can **falsify** the
candidate. It cannot support a general claim that AMC is better or cheaper.

## Arms

| Arm | Skill | Host / model |
|---|---|---|
| Control | No AMC skill | Same host, lead model, reasoning, tools, sandbox, approvals, timeout |
| AMC | Current `SKILL.md` from this branch | Identical otherwise |

Shared home instructions, if present, must be recorded. They prevent a clean
"naked single agent" isolation claim.

## Cases

Hidden checks live in `hidden/` and must not be given to subjects.

1. `c9-01-simple-fix` — sequential one-file bugfix. Hidden: `format_value(False)` is `-`. Public check does not mention False. AMC must not spawn workers.
2. `c9-02-two-audits` — two independent read-only questions. Hidden: both planted defects named. Parallel is allowed; shared writes are not.
3. `c9-03-checked-write` — bounded write with `python hidden/c9_03_check.py` declared before spawn. Hidden: output hash and no extra files.
4. `c9-04-false-pass` — risky gate. Public `check.py` can pass while hidden forbids a claimed PASS on missing False coverage.

## Ranking

1. Correct completion and hidden checks.
2. False PASS / regressions.
3. User interventions.
4. Wall time.
5. Lead, worker and total observed tokens.

A cost increase on case 4 is acceptable only with a documented correctness or
safety gain. Case 1 must not add agents, reviews or learning logs.

## Status

Subject runs on this candidate: **c9-01 executed 2026-09-14**. Both arms public PASS,
hidden FAIL (`False` → `"False"` not `"-"`). AMC 75.0 s / 188 346 input vs
control 52.6 s / 99 814 input. Zero children both. Cases 2–4 **NOT RUN**.
See [results-2026-09-14.json](results-2026-09-14.json). Comparative benefit
remains **NOT VERIFIED**.
