# Context Packet — blank template. Copy and fill. No live claims.

Objective: State the bounded job. Start as NOT VERIFIED.
Reason for delegation: Why this node earns its coordination cost, or omit the packet and keep the work with the lead.
Base commit or snapshot: Current artifact identity, including dirty state when relevant. NOT VERIFIED until captured.
Writable owned scope: Exclusive paths this job may change; none for a read-only job.
Read inputs, paths and symbols: Only what this job needs; shared unless stated otherwise.
Dependencies already satisfied: Upstream job and exact artifact identity (path, snapshot or evidence result), or none.
Constraints and invariants: Authority, forbidden consequences, and files to preserve.
Authorized actions: Allowed tools and mutations. A prompt scope is not a sandbox.
Required deliverable: Compact artifact (paths, diff or file identity, results, risks). Not the worker transcript.
Acceptance check: Falsifiable check declared before spawn. For code writes, prefer an executable check.
