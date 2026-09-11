# Delegation and handoffs

Load when independent work merits a worker, or ownership changes.

Before assigning writers, compare their paths, generated outputs, fixtures,
services and mutable state. Freeze shared interfaces first. Resolve overlap
by narrowing scopes or finishing and handing off one job before the next.
Isolation protects edits; it does not make dependent tasks independent.

Give the worker only enough context to act:
- objective, why it is independent and the base commit or file snapshot;
- one owned scope, relevant inputs and satisfied dependencies;
- constraints, allowed actions, deliverable and an acceptance check.

These are information requirements, not mandatory headings. Use a short
paragraph when sufficient; the [Context Packet](../templates/context-packet.md)
is a populated example. Link paths and small excerpts instead of sending the
full conversation. State when collaborators share the workspace and require
preservation of their edits. Nested delegation must fit the same ownership
and permission boundaries and have an independent reason.

Use a strong available lead for architecture and integration; focused or
cheaper workers suit bounded work. Escalate a job when its uncertainty or risk
exceeds the worker's capabilities. If cost is an objective, measure actual
usage; a model name is not cost evidence.

On return, require artifact locations, changed/inspected paths, commands with
observed results, acceptance status and unresolved risks. The
[Evidence Packet](../templates/evidence-packet.md) illustrates missing proof.
Do not promote a bounded worker verdict into the mission verdict.

Reconcile expected and received deliverables. Inspect differences and run
affected checks before integration; keep missing, stale or conflicting claims
unverified. Record the old owner as stopped and the transfer as accepted before
the next writer starts. If a worker might still be running, inspect native
state or stay read-only until exclusive ownership is established.

Give a separate reviewer the requirements and current artifacts without the
implementer's intended conclusion. Review is evidence about defects, while
runtime verification requires actual execution.
