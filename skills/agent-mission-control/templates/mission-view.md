schema_version: 1
overall: NOT VERIFIED

# Mission View — blank template. Copy and fill. No live claims.

## Goal / Definition of Done

State the objective and the checks that would make it done. This file starts as
NOT VERIFIED and contains no case facts.

## Base and candidate

Current artifact: NOT VERIFIED
Record commit or snapshot plus dirty-tree/artifact digest when relevant.
Base: NOT VERIFIED until a recoverable snapshot exists.
Candidate: none.

## Hard gates

| Gate | Status | Evidence |
|---|---|---|
| Required acceptance check | NOT VERIFIED | No executed check yet |

## Authority

Authorized: only the user's current task scope.
Forbidden: actions outside that scope, including unauthorized credential access,
push, deploy or destructive work. Record any explicit publication mandate here;
the mission record cannot grant new authority.

## Jobs

| Job | Agent | Required | Lifecycle | Verdict | Writable owned scope |
|---|---|---|---|---|---|
| Required work | Lead | yes | queued | NOT VERIFIED | Named writable paths |

Lifecycle is queued, running, completed or superseded. Verdict is PASS, FAIL,
BLOCKED or NOT VERIFIED. Required is yes or no. Completion is not acceptance.
A dropped job is superseded, optional, NOT VERIFIED, and names a superseded: reason.
Writable owned scope lists exclusive write paths; read-only jobs use `none`.
When a job needs an earlier output, name the upstream job and exact artifact
under Decisions and evidence.

## Decisions and evidence

NOT VERIFIED. Copying this template makes no live claims.

## Blockers

None.

## Next action

Fill the objective, freeze the current artifact identity, then do the next authorized check.

## Last verified

Commit/snapshot: NOT VERIFIED. UTC timestamp: NOT VERIFIED.
