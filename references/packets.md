# Work, context and capability routing

Delegate when a bounded job buys useful information or execution after context,
coordination and integration cost. Focused expertise or a fresh context can
justify a specialist without an earlier job output. When a job does need
another's output, name that exact dependency artifact. Freeze shared interfaces
first; parallelize ready independent work;
serialize dependent work and shared mutable resources. A worktree alone does not
make jobs independent. Each writer owns one exclusive scope, including tests,
generated files and resources. Confirm the old owner stopped before transferring
writes; if uncertain, inspect read-only. Preserve collaborators' edits.

Parallel writers need **host-enforced** isolation: a worktree, sandbox, VM or
exclusive permissions. A prompt that names exclusive files is not a sandbox.
If the host cannot isolate writers, serialize the writes and say so. Shared
read-only research may still fan out without a worktree.

## Scout and capability choice

A scout is useful when scope, dependencies or needed expertise remain unclear.
Give it the objective, authority, relevant paths/current facts and one bounded
triage question. Ask for a compact proposed graph: nodes/owners, real dependencies,
uncertainties, appropriate capability and necessary proof. Include optimization,
recovery or learning only if the facts justify them. It does not execute the whole
mission or recruit a team. Skip scouting when the lead already knows the route.

Choose among models and tools the host actually exposes. AMC names capability
classes, not product models:

| Class | Use for |
|---|---|
| Lead-capable | Scope, architecture, integration, budget and final acceptance |
| Focused general worker | Routine bounded implementation |
| Cheap bounded worker | Narrow discovery, mechanical edits, or a predeclared check |
| Material reviewer | Independent falsification of a risky claim |
| Narrow verifier | Executing a declared check against an identified artifact |

Host profiles ([quality / balanced / throughput](https://github.com/byensitmagnus/agent-mission-control/blob/main/examples/profiles.md)) may
map these classes to concrete models. Keep the selected lead.
Do not default every child to the lead model or force difficult work onto the
cheapest class. If the requested capability is unavailable, report the limit and
choose a supported alternative; do not silently upgrade cost or invent IDs.

A cheap bounded worker may receive a job only when all of the following hold:

1. The job is bounded.
2. Inputs and write-scope are known.
3. A falsifiable acceptance check is declared before spawn.
4. The lead can check the result without repeating the whole job.
5. Expected gain exceeds coordination cost.

For code writes, that check should be executable when behavior can be tested.
Research may use source anchors, counterevidence and the lead reopening sources.
UI work may need rendering or visual inspection. Allow at most one retry with a
tighter contract for the same bounded hypothesis; then diagnose and escalate
only the unresolved slice or use a materially different hypothesis. Do not loop
the same attempt.
Run the break-even preflight in [resources](resources.md#cost-aware-delegation)
before spawn. If it rejects delegation, keep the work with the lead. If only
parallel readiness fails, serialize a still-useful specialist handoff.

Set child model and reasoning independently of the lead when native tools allow.
Match effort to the unresolved work: low for straightforward mechanical tasks,
medium for routine work, high for complex logic or material review. Short context
does not require high effort; no effort label guarantees quality. Use native
read-only roles for research/review and bounded write permissions for
implementation; a prompt scope is not a sandbox. Host concurrency is a ceiling,
not a target. With no delegation API, work serially and disclose any required
independence that cannot be provided.

## Handoff and integration

Send goal, current source identity, necessary inputs, exclusive writable scope,
constraints/authority and acceptance check. When a job needs an earlier output,
name the upstream job and exact artifact as a path, snapshot or evidence result.
Reporting to the lead is not a dependency. When no earlier output exists, write
none. Shared read inputs do not imply writable ownership. Compaction may drop
raw tool output and still keep
the identity the next check uses. Start new workers with fresh context
and a task-specific packet, without the parent's or siblings' conversations.
Pass only necessary outputs from dependency jobs through the lead. A researcher
needs its question and sources; an implementer needs the agreed interfaces and
relevant findings. The lead keeps the overall state and evidence, not every raw
transcript. Shared host rules/tools can still be present; fresh history is not
full prompt isolation. Ask for missing task context instead of guessing. Load
available domain
skills by the actual subtask, without forwarding the whole daily skill library.
[Context Packet](../templates/context-packet.md) is optional
formatting. Nested delegation needs its own value, scope and resource room.

Workers return a compact artifact: owned paths, diff or file identity, commands
actually run, results and unresolved risks — not the worker conversation. The
lead must be able to accept or reject from that artifact without repeating the
job. The [Evidence Packet](../templates/evidence-packet.md) is optional
formatting. Reconcile expected against received results, inspect artifacts and
execute acceptance checks.
Route a finding to its responsible owner with a reproducible failure; integrate
its repair after prerequisites, then refresh only affected evidence. Missing or
failed workers stay visible. Independent review follows
[verification](verification.md) when risk or acceptance warrants it.
