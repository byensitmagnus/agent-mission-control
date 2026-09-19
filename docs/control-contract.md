# Control contract

Canonical machine semantics: [`scripts/amc_guard.py`](../scripts/amc_guard.py), schema_version `1`.
The installed CLI is [`scripts/amc-check.py`](../scripts/amc-check.py).
The blank form is [`templates/control-contract.json`](../templates/control-contract.json).
Product statuses live in [`status.json`](status.json).
Canonical claims: [`research/claims.json`](../research/claims.json).

This is an engineering contract for planning, observation and acceptance. It is
not a runtime, scheduler, database or proof that AMC is better, cheaper or faster.

Markdown [`MISSION.md`](../MISSION.md) and [`templates/mission-view.md`](../templates/mission-view.md)
remain human views. If the two disagree, the Python contract wins for machine
checks. Live chats stay instruction-only until the host runs the bundled checker
on a mission file. Trivial direct tasks do not need a mission file.

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
| Unique job IDs, cycles, overlapping writers, unknown enums | repository_ci_enforced |
| Installed `amc-check.py` on a mission file | bundled_checker_enforced |
| Live routing in a host chat | instruction_only |
| Parallel writers need host isolation | Validator claim when checked; isolation itself is host_enforced |
| Observed child/session IDs | host_enforced when the host reports them |
| Skill text telling the lead not to fake PASS | instruction_only |
| CI green on `main` | externally_attested engineering, not behavioral PASS |
| Package bytes and install rollback | repository_ci_enforced |

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

Field pins were last graded in [`field-state.md`](field-state.md). Claude Code
Projects was fetched 2026-09-19. Star counts remain popularity data, not quality.
Homemade subject-run farms stay closed
([candidate.9 postmortem](../evals/candidate.9/README.md)).
