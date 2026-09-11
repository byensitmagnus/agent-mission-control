# Candidate and risk gates

Read this for measurable optimization, migrations or data-sensitive releases.

## Measured candidates

Before candidate 1, freeze the workload, correctness checks, environment and
selection order. Record baseline commit/snapshot, candidate parent, hypothesis,
expected change, attempt/time budget and observed result. Keep an immutable
baseline and a recoverable incumbent. Test each candidate on the same inputs;
workers cannot edit the evaluator to pass. Root rejects regressions and selects
on hard gates before improvements. Label unavailable cost/timing/token data
`NOT MEASURED`; do not infer savings from a cheaper model's name.

Repairs within one hypothesis belong to that candidate. A changed hypothesis
uses the next candidate and its remaining budget. Record rejection evidence;
budget exhaustion stops the experiment without turning it into PASS. A changed
evaluator requires a new separately identified comparison, never retroactive
acceptance of a failing candidate.

## Migration or customer-facing change

Capture baseline data and relevant rendered/executable behavior before edits.
Use disposable copies for migration. Compare IDs, counts and full values,
including false, zero, unknown fields and supported settings. Prove rollback
restores original bytes or an explicitly equivalent recoverable state. Include
a negative control that deliberately corrupts output and must fail parity.
Do not let a new gate hide an existing valid source before migration is complete.
Preserve images, product data, prices, CTA and flows unless changes are in scope.

## Independent review and runtime verification

Review looks for broken invariants and omitted paths. Verification executes
the frozen acceptance checks against the candidate. Neither an implementer's
own review nor reviewer agreement replaces execution. Root reproduces relevant
checks and maps artifacts to gates. Missing independent review or verification
keeps the relevant gate NOT VERIFIED. Root repairs material findings within
scope, then repeats affected checks and obtains fresh review of that repair.

A local PASS grants no additional authority. Stop at the exact boundary of an
unapproved consequential action; finish all independent authorized preparation.
External state that cannot be read is NOT VERIFIED, never assumed safe.
