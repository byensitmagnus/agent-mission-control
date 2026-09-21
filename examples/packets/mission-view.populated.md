schema_version: 1
overall: NOT VERIFIED

# Mission View — populated demonstration, not live evidence

## Goal / Definition of Done

Fix the disposable transport deadline check; preserve retry semantics. Done
means before/equal/after boundary checks pass with independent review.

## Base and candidate

Current artifact: NOT VERIFIED
Base: NOT VERIFIED; root must capture HEAD and workspace snapshot before edits.
Candidate: 1, parent is the captured baseline; hypothesis: strict deadline
comparison rejects expired work without changing retry behavior. Maximum: 2.

## Route

Planned route: sequential_delegated
Observed route: sequential_delegated
Deviation: none
Observed agents/threads: none
Observed isolation: none

## Hard gates

| Gate | Status | Evidence |
|---|---|---|
| Deadline behavior | NOT VERIFIED | No executed boundary check |
| Retry behavior preserved | NOT VERIFIED | No executed regression check |
| Independent review | NOT VERIFIED | No packet received |
| Root runtime verification | NOT VERIFIED | No current artifact |

## Authority

Authorized: read and edit disposable fixture files; run local checks.
Forbidden: external mutations, credentials, push, deploy and destructive work.
Evaluator and authority belong to root; workers cannot change them.

## Jobs

| Job | Role | Agent | Required | Lifecycle | Verdict | Owned scope |
|---|---|---|---|---|---|---|
| Deadline investigation | worker | Unassigned | yes | queued | NOT VERIFIED | Read-only transport.py |
| Retry investigation | worker | Unassigned | no | queued | NOT VERIFIED | Read-only retry.py |
| Implementation and integration | lead | Root | yes | queued | NOT VERIFIED | transport.py and local checks, after architecture decision |
| Independent review | reviewer | Unassigned | yes | queued | NOT VERIFIED | Read-only candidate |

## Decisions and evidence

No implementation decision yet. Root must inspect the source and freeze the
baseline before starting jobs. This populated demonstration makes no live claims.

## Blockers

None established. Missing evidence must be gathered; it is not a user blocker.

## Next action

Root captures git status, HEAD and fixture digest, then reads the deadline rule.

## Last verified

Commit/snapshot: NOT VERIFIED. UTC timestamp: NOT VERIFIED.
External actions not performed: push, merge, tag, release.
