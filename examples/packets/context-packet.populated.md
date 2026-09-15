# Context Packet — populated demonstration, not live evidence

Objective: Determine whether the transport deadline check matches its contract.
Reason for delegation: Retry policy can be investigated independently in parallel.
Base commit or snapshot: Fixture snapshot transport.py and requirements.md, captured by root in the run manifest.
Owned scope: Read-only transport.py and requirements.md; no writable paths.
Relevant paths, symbols and inputs: transport.py::remaining and should_send; requirements.md deadline rule.
Dependencies already satisfied: The deadline contract is fixed; no architecture decision is pending.
Constraints and invariants: Preserve files; do not change goals, evaluator or authority; other agents share this workspace and their edits must be preserved; no nested delegation.
Authorized actions: Read the two inputs and run a non-mutating local expression check; no credentials or external mutations.
Required deliverable: Evidence Packet with current source anchors and observed boundary behavior.
Acceptance check: Compare deadline-before, equality and deadline-after behavior against the written rule.
