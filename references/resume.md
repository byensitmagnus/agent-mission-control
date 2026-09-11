# Mission View schema and resume

The [version 1 template](../templates/mission-view.md) is a plain Markdown
record, not a scheduler or dashboard. Its first two lines declare
`schema_version: 1` and `overall: PASS|FAIL|BLOCKED|NOT VERIFIED`. The required
sections are Goal / Definition of Done, Base and candidate, Hard gates,
Authority, Jobs, Decisions and evidence, Blockers, Next action, Last verified.
Every gate has a status and evidence reference; every job has an agent, status
and owned scope. Only root updates the aggregate record.

Allowed gate/job verdicts are PASS, FAIL, BLOCKED and NOT VERIFIED; job lifecycle
may additionally be queued, running or completed. Lifecycle completion is not
acceptance. Overall PASS requires all hard gates PASS on current evidence and
no unresolved material blocker. Use FAIL for an observed gate failure, BLOCKED
for an external prerequisite, NOT VERIFIED for missing/stale/conflicting proof.
If both failure and missing evidence exist, report both; never collapse them to
PASS. `Last verified` names the commit plus dirty-tree/artifact digest when
needed and a UTC timestamp. A commit alone cannot identify uncommitted changes.

## Reconciliation

1. Read the durable record and inspect `git status --short`, `git rev-parse HEAD`
   and the artifacts cited by its next gate. If there is no Git repository,
   verify the recorded file snapshot/digest and explicitly record that limit.
2. Compare base, candidate and owned paths with current files. A mismatch
   invalidates affected claims. Keep unrelated user changes; do not reset the
   workspace to fit an old claim. Record which checks need fresh execution.
3. Query native agent state when available. An interrupted/session-lost worker
   is not automatically completed. Reconcile its files and packet before
   reclaiming ownership. Never spawn a replacement writer while the previous
   one might still mutate the same scope; confirm stopped or use read-only
   inspection until the conflict is resolved.
4. Continue the next failed or unverified gate. Update status only with current
   evidence, including failed checks. If the record version is unknown, preserve
   it and reconstruct a supported record from workspace proof before proceeding.

Secrets and raw conversation logs do not belong in Mission View. Keep concise
decisions with the artifact or command that supports them. Existing mission
trackers may use another format if they retain the same information and gates.
