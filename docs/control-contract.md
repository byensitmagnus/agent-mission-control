# Control contract

Canonical machine semantics: [`evals/control_contract.py`](../evals/control_contract.py), schema_version `1`.
The blank form is [`templates/control-contract.json`](../templates/control-contract.json).
Product statuses live in [`status.json`](status.json).

This is an engineering contract for planning, observation and acceptance. It is
not a runtime, scheduler, database or proof that AMC is better, cheaper or faster.

Markdown [`MISSION.md`](../MISSION.md) and [`templates/mission-view.md`](../templates/mission-view.md)
remain human views. If the two disagree, the Python contract wins for machine
checks. The installed skill package does not execute this Python; host behavior
is still instruction-only unless this repository's checks are run.

## Status split

| Status | Meaning | Must not be inferred from |
|---|---|---|
| Engineering | Structural, package, contract and replay tooling on an identified tree | Agent quality on a user's project |
| Behavioral | Measured agent benefit versus a comparable direct path | A green engineering validator |
| Release | Explicit GO / NO-GO to publish or tag | A merge to `main` |

Unknown stays unknown. `PASS` in engineering never writes behavioral `PASS`.

## Route receipt

Record planned route, reason, expected information value, coordination-cost
assumption, worker/reviewer ceilings, expected host capabilities, observed
child/session IDs, observed roles, observed isolation, deviations, fallback and
result status. Do not store prompts, transcripts, secrets, source code or file
contents by default.

If a delegated route was planned and no native child/session was observed, record
`DELEGATION_NOT_OBSERVED`, do not claim delegation happened, fall back to authorized
direct work, and keep behavioral benefit NOT VERIFIED.

Observed child IDs are objects `{id, source}` where `source` is one of
`host-reported`, `worktree`, `sandbox`, `session`. Bare strings do not count as
observation. Isolation evidence must be a host-observed record, not `claimed`,
`yes`, `true` or `prompt`. An `isolated_parallel` route with two writers needs
that isolation even if job `parallel` flags are missing.

Required jobs and gates for schema_version `1` PASS bind to `plan.jobs` /
`plan.gates`. Ghost completed IDs do not mint PASS. After acceptance-logic
change, a reviewer must be completed, PASS, and explicitly independent.
`queued` or `same-lead` does not count. Dirty bytes with `git-tree` or
`git-commit` identity fail even if `evidence_assumes_clean` is omitted.

## Artifact identity

Do not embed the candidate commit SHA in a tracked file that is part of that
same commit.

| Tree state | Identity |
|---|---|
| Clean committed source | Git tree plus package/content digest |
| Dirty candidate | Base commit, dirty flag, changed-file manifest **and per-file SHA-256** |

Stale evidence cannot accept changed bytes. Dirty bytes cannot be accepted by
clean-commit evidence.

## Guarantee class

| Rule | Class |
|---|---|
| Unique job IDs, cycles, overlapping writers, unknown enums | Validator-enforced in this repo |
| Delegation needs explicit positive break-even | Validator-enforced on the contract document |
| Parallel writers need host isolation | Validator-enforced claim; isolation itself is host-enforced |
| Observed child/session IDs | Directly observed when the host reports them |
| Skill text telling the lead not to fake PASS | Instruction-only at runtime |
| CI green on `main` | Externally attested engineering, not behavioral PASS |
| Package bytes and install rollback | Validator-enforced in packaging/install tests |

## AVO / offline learning eligibility

Do not run candidate search on ordinary software work. An AVO-like optimizer is
allowed only when all are true: scalar or totally ordered metric; frozen
evaluator; deterministic or sufficiently repeated environment; bounded edit
surface; baseline; fixed budget; recoverable lineage; ties keep the incumbent;
evaluator changes start a new baseline; preservation or holdout checks; rollback.

Offline skill learning stays a separate process: observation → bounded rule delta
→ train cases → validation cases → untouched holdout → strict improvement →
explicit adoption. Never auto-adopt from a normal successful task.

## Future opt-in telemetry

No telemetry backend ships in this branch. A future local JSONL schema may use
the keys in `TELEMETRY_EVENT_KEYS` inside `evals/control_contract.py`: opt-in
append-only events, locally salted HMAC identifiers, no prompts or file
contents, and unknown money unless a versioned price source and date exist.
Cached and uncached tokens must not be priced the same.

## Sources for this slice

Field pins were last graded in [`field-state.md`](field-state.md) on 2026-09-15.
They were **not freshly revalidated** on 2026-09-18. Star counts remain popularity
data, not quality. Homemade subject-run farms stay closed
([candidate.9 postmortem](../evals/candidate.9/README.md)).
