# Mission View schema and resume

The [version 1 template](../templates/mission-view.md) is a plain Markdown
record, not a scheduler or dashboard. Its first two lines declare
`schema_version: 1` and `overall: PASS|FAIL|BLOCKED|NOT VERIFIED`. The required
sections are Goal / Definition of Done, Base and candidate, Hard gates,
Authority, Jobs, Decisions and evidence, Blockers, Next action, Last verified.
`Base and candidate` includes `Current artifact:`. Every gate has a status and
evidence reference. Only the lead responsible for this mission updates its
aggregate record. A delegated agent explicitly assigned a separate mission owns
that mission's record; it does not update the parent mission's tracker.

Job **lifecycle** is queued, running, completed or superseded. Job **verdict** is PASS, FAIL,
BLOCKED or NOT VERIFIED. **Required** is yes or no. Lifecycle completion is not
acceptance. Unfinished jobs stay `NOT VERIFIED`. Overall PASS forbids queued or running
jobs. A dropped job is `superseded` with Required `no` and `superseded:` plus a
reason in writable owned scope. Optional work that is not finished must be removed or
superseded; it may not remain queued to obtain PASS.

When a job is retried, keep its job identity and distinguish each attempt in
Decisions and evidence. Only the current attempt may complete the job. A timeout
or missing observation does not prove an older attempt stopped; late results
from a superseded attempt cannot complete the job. Do not transfer its writable
scope until the host confirms termination.
Marking an attempt superseded does not revoke its tools. Before overall PASS,
record host evidence that every unfinished or superseded writer is stopped or
isolated from the accepted artifact. Otherwise keep acceptance unverified;
continue independent safe work without reassigning its live writable scope.

Overall PASS requires all of: every hard gate PASS with current evidence that is
not an unverified placeholder; the current artifact identity in hard-gate
evidence, decisions and last verified; every required job completed with verdict
PASS; at least one required job; no queued or running jobs; no completed job
with a negative verdict; no unresolved writer able to mutate the accepted
artifact; Blockers `None` (an optional trailing period is accepted); Next action
not itself blocked.
Narrative fields must not hide unfinished work as still queued. The checker tests
Markdown contract consistency; it cannot prove that natural-language evidence is
true or that the named identity equals git HEAD. Use FAIL for an observed gate failure, BLOCKED for an
external prerequisite, NOT VERIFIED for missing, stale or conflicting proof.
A stale mission PASS cannot accept a new artifact. If both failure and missing
evidence exist, report both; never collapse them to PASS. `Last verified` names
the commit plus dirty-tree/artifact digest when needed and a UTC timestamp.

Keep the live mission compact: current artifact, open gates, blockers and next
authorized action. Move finished iteration narrative to a dated history file.
A resuming agent must not need old iterations to learn current status.

Before a long-task handoff or context loss, refresh the current milestone,
working artifact, important decisions, failed approaches and next hypothesis in
the existing record. Keep durable evidence paths and brief diagnoses instead of
copying raw conversations. Compression must not drop facts later gates need, including the artifact
identity a later job uses.
A clean checkpoint means recoverable scoped work; never discard another owner's
uncommitted changes to manufacture a clean tree.

## Reconciliation

1. Read the durable record and inspect `git status --short`, `git rev-parse HEAD`
   and the artifacts cited by its next gate. If there is no Git repository,
   verify the recorded file snapshot/digest and explicitly record that limit.
2. Compare base, candidate and owned paths with current files. A mismatch
   invalidates affected claims. Keep unrelated user changes; do not reset the
   workspace to fit an old claim. Record which checks need fresh execution.
3. Query native agent state when available. An interrupted/session-lost worker
   is not automatically completed. Reconcile its files and packet before
   reclaiming ownership. A packet from a superseded attempt cannot complete the
   job, and a packet whose artifact identity no longer matches the current bytes
   is stale. Never spawn a replacement writer while the previous
   one might still mutate the same scope; confirm stopped or use read-only
   inspection until the conflict is resolved.
4. Continue the next failed or unverified gate. Update status only with current
   evidence, including failed checks. If the record version is unknown, preserve
   it and reconstruct a supported record from workspace proof before proceeding.

Secrets and raw conversation logs do not belong in Mission View. Keep concise
decisions with the artifact or command that supports them. Existing mission
trackers may use another format if they retain the same information and gates.
