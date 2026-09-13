# Give AMC a useful task

[Install and select the skill](getting-started.md) first. Then choose a prompt
below and replace the bracketed text. Describe the outcome and what must stay
working. The lead owns task decomposition, worker handoffs, integration and
verification; you do not need to assign a sequence of agent roles.

These are task recipes, not claims that a particular task has already passed.
Use normal host permissions. Each recipe stops before external publication.
The examples use Codex's `$agent-mission-control`; substitute your
[host's invocation](hosts.md#install-the-current-source) in another assistant.

## Fix a bug

```text
$agent-mission-control

Fix this bug: [what happens, what should happen, and how to reproduce it].
Preserve [the existing behavior or data that must not change].

Find the cause, make the smallest complete repair and verify the affected
behavior using the project's existing checks. Add a focused regression
check when needed. Reuse valid unaffected evidence.

Own any useful delegation and follow-up. Finish the authorized local work;
show the changed files, checks actually run and remaining limitations.
Stop before push, deployment or other external changes.
```

**Inspect the delivery:** the original failure is addressed, nearby behavior is
preserved and the reported check actually covers the bug. A green unrelated
suite is insufficient. A small fix may need only the lead.

## Build a feature

```text
$agent-mission-control

Implement [feature] for [who needs it and why].
Acceptance: [two or three observable behaviors].
Preserve: [existing workflows, data and compatibility].
Out of scope: [adjacent changes you do not want].

Choose and carry out the work, including useful independent help.
Coordinate ownership, integrate the result and verify every acceptance
criterion. Keep a brief record if the task spans several stages.
Show the finished behavior, relevant checks and any remaining blocker.
Stop before push, deployment, purchases or other external changes.
```

**Inspect the delivery:** try each acceptance behavior and open the relevant
evidence. If a UI changed, inspect the rendered result. Delegation is useful when
jobs can proceed independently or a fresh review can uncover a material error.
Two workers editing the same files are not independent just because they have
different role names. The lead must reconcile their work.

## Resume unfinished work

```text
$agent-mission-control

Continue this objective: [the full original outcome].
Read the existing progress record at [path] and inspect current files
before trusting its status. Preserve other contributors' work.

Identify what is complete, what still needs proof and the next authorized
action. Reuse valid evidence for unchanged artifacts. Resolve stale
ownership before writing and continue through the remaining local work.

Keep the progress record current. Finish with the verified result or the
exact external blocker. Existing scope and permissions still apply;
stop before push, deployment or other external changes.
```

**Inspect the delivery:** it advances the original objective, reconciles changed
files with saved state and identifies current artifacts. A new plan alone is
not the requested completion. If another agent is still writing, ownership needs
resolution before a new writer takes over.

## Research code without changing it

Use this when another task owns implementation, or when you want evidence before
deciding to change code. Pin a commit or disposable source snapshot; starting
file paths are entry points, not a reason to omit a necessary caller or guard.

```text
$agent-mission-control

Investigate [one concrete question] in [read-only snapshot and identity].
Start at [paths/symbols]. Follow relevant callers, guards and existing tests
inside this snapshot. Do not edit or execute product code, run builds/tests,
change the live workspace, or send its owner new instructions.
Write the report only to [separate output path].

Own useful delegation and verification within [small effort/agent budget].
Give each worker the question, source identity, permitted read scope and
required evidence. If a necessary dependency is missing, identify it and
resolve it within authorized read access; do not guess or widen write scope.

For each material finding, give the trigger, source anchors, impact and
counterevidence you checked. Distinguish what the code establishes from
runtime behavior that was not tested. Missing caller context is a missing
source dependency, not automatically a need to execute the application.
Check version-sensitive API assumptions against primary documentation when
external reading is authorized; otherwise name that unresolved assumption.

The lead must challenge worker findings before retaining them. Zero
confirmed defects is valid. Return findings or reasoned refutations,
existing test coverage, proposed next checks and remaining uncertainties.
Do not implement the proposed repairs.
```

**Inspect the delivery:** citations support the precise claim and the relevant
call path is covered. A helper accepting an argument does not establish that a
user can supply it through the application. Neither a worker's confidence nor
reviewer agreement substitutes for tracing that boundary. This recipe
uses AMC's existing [packet](../references/packets.md) and
[verification](../references/verification.md) guidance; it adds no mandatory
research stage to ordinary implementation.

## What a completed delivery looks like

**Illustration:** a CSV export writes an empty cell for a legitimate zero value.
The goal is to retain zero while preserving the representation of a missing
value. The following paths and results are invented to demonstrate the format.

| Part of the delivery | Illustrative content | What you can inspect |
|---|---|---|
| Result | Zero now exports as `0`; missing values remain blank. | Both cases in the generated CSV. |
| Change | Updated `src/export.py`; added a focused regression in `tests/test_export.py`. | The actual diff in those files. |
| Verification | `python -m unittest tests.test_export` passed on the changed source. | Command output and the cases it covers. |
| Limits | External spreadsheet import was not tested. No deployment occurred. | The scope and any remaining requirement. |

AMC uses explicit outcomes:

| Status | Meaning for your task |
|---|---|
| **PASS** | Every applicable acceptance gate has evidence for the current artifact. |
| **FAIL** | An applicable check found an actual failure. |
| **NOT VERIFIED** | Required evidence is missing, incomplete or not current. |
| **BLOCKED** | A necessary external input, permission or resource prevents continuation. |

The lead should handle authorized repairs and affected checks before concluding.
A blocker should explain exactly what is needed, with independent work already
completed. A status label does not replace the underlying evidence.

## Keep communication useful

Expect updates when a finding changes the approach, a useful milestone finishes
or a necessary decision arises. You should not need to relay worker results
between agents or repeatedly authorize the same local work. Required host
approvals and real product decisions still need the appropriate person.

If AMC stalls, a useful correction is: “Return to the original outcome, inspect
the current evidence and finish the remaining authorized work.” For a report,
record the correction and what caused it; [share a sanitized experience](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml).

[How routing works](how-it-works.md) · [Measured results and limits](evidence.md) ·
[Setup and troubleshooting](getting-started.md#troubleshooting)
