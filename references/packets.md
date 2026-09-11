# Packet schemas, version 1

These headings are the required fields. Each field contains concrete task
data, an explicit `None` with a reason, or a declared uncertainty. A field's
presence alone does not prove its claim. Omitted evidence means NOT VERIFIED.

## Context Packet

```text
Objective:
Reason for delegation:
Base commit or snapshot:
Owned scope:
Relevant paths, symbols and inputs:
Dependencies already satisfied:
Constraints and invariants:
Authorized actions:
Required deliverable:
Acceptance check:
```

Root supplies the complete packet. Owned scope names paths, generated outputs,
fixtures and shared surfaces; mark read-only jobs explicitly. A worker may ask
for a missing input but cannot expand ownership, goals or permission itself.
If a base or dependency changes, root refreshes the affected packet before
work continues. Identify shared-workspace collaborators; workers preserve
their changes. Use [this populated example](../templates/context-packet.md).

Send paths or small relevant excerpts, not full thread history. Prefer fresh
worker context when the runtime supports it. Root assigns any nested work
explicitly; nesting counts against the same concurrency and ownership limits.

## Evidence Packet

```text
Verdict:
Claims:
Files and symbols inspected or changed:
Commands run and observed results:
Acceptance-check result:
Risks and uncertainties:
Blocking decision, if any:
```

Verdict is `PASS`, `FAIL`, `BLOCKED` or `NOT VERIFIED` for the bounded job only.
Commands include exit codes and the base/snapshot they apply to. Link artifacts
without dumping sensitive logs. Distinguish inspection, execution and inference.
Use [this populated example](../templates/evidence-packet.md).

Root reconciles expected packets and maps evidence to gates. A PASS assertion
without an executed required check is NOT VERIFIED. Incompatible evidence is
NOT VERIFIED until independently resolved; an observed failing check remains
FAIL. Reviewers receive the requirements and current artifacts without the
implementer's proposed verdict. Runtime verification is a separate activity.
