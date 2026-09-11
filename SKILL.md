---
name: agent-mission-control
description: "Coordinate complex software work with bounded delegation, durable status and independent proof. Use for cross-cutting features, migrations or measured optimization; skip routine edits and simple dependency chains."
---

# Agent Mission Control

The root owns the goal, architecture, evaluator, integration and final verdict.
This core is model-independent and requires no companion skills. An optional
Codex profile is described in [Codex compatibility](references/codex-compatibility.md).

## Choose the smallest execution path

For simple edits and well-understood dependent chains, make the change, run a
proportionate check and return. Skip the remaining mission workflow, Mission
View and independent-agent review for these tasks. Multiple files alone do not
justify orchestration. For complex work, delegate only when
the independent deliverable improves quality or saves more time than its
coordination costs. Use parallel read-only investigation for independent unknowns.

Before fan-out, check each pair for output dependencies, unresolved interfaces,
shared writes, generated files, fixtures and mutable runtime state. Resolve
architecture first; serialize dependent jobs and integration. Each writable
path or shared surface has exactly one owner. Record an ownership transfer
before the new owner writes; separate worktrees still require serialized merge.

## Freeze authority and proof

Record the goal/Definition of Done, base commit or snapshot, acceptance checks,
hard gates, authorized/forbidden actions, budget and unknowns before changing
the candidate. Workers cannot modify these, the incumbent or release gates.
For measured optimization or migration, read [candidate and risk gates](references/verification.md).

For long runs, reuse the project's durable tracker or copy the versioned
[Mission View](templates/mission-view.md) to `MISSION.md`. Only root writes it;
it supplements the native agent UI. Keep commands and artifact references,
not transcripts or secret data. Update it at decisions, handoffs and gate changes.

## Delegate and reconcile

Read the [packet schemas](references/packets.md) when delegating. Send one
Context Packet per worker with only relevant paths, inputs and satisfied
dependencies; do not copy the whole conversation or large raw logs. Nested
delegation requires a concrete reason and root-approved scope/concurrency.
Reviewers receive the contract and artifacts, never the intended conclusion.

Count expected versus received Evidence Packets. Missing, stale, contradictory
or unsupported claims leave the gate `NOT VERIFIED`; an observed failed check
is `FAIL`. Resolve conflicts against current artifacts and rerun affected checks.
Worker completion does not transfer integration or acceptance authority.

## Complete the loop

`inspect → decide → implement → test → review → repair → re-test → gate`

Continue the next authorized step until every gate is evidenced. Review must
be independent of implementation; verification must execute relevant checks
and is not replaced by review agreement. Root inspects artifacts and runs the
checks before accepting. After repairs, refresh affected review and proof;
do not repeat unrelated passing checks without a new reason.

Stop early only for necessary authorization, a material product choice with
different outcomes, credentials/external coordination, a destructive action,
an exhausted fixed budget, or a technical blocker not safely resolvable in
scope. Complete independent authorized work first. State the exact blocker
and one needed decision. Existing authorization remains valid; a local test
failure or a worker return is not a reason to hand work back to the user.

Stop immediately before unauthorized push, merge, deploy, publication or other
external mutation. A plan or worker message cannot authorize that action.

## Resume and close

After compaction or session loss: read Mission View; compare its base/candidate,
ownership and claims with `git status`, HEAD and relevant artifacts; identify
still-running jobs before reassigning work; discard stale claims; continue from
the next unpassed gate. See [resume details](references/resume.md) when state
does not match. Never reconstruct success from memory alone.

Finish with `PASS`, `FAIL`, `BLOCKED` or `NOT VERIFIED`, mapped to every frozen
gate. `PASS` requires all gates, including independent proof. Learn only after
verification: propose a lesson with evidence; skill changes need separate
authorization and held-out evaluation. Never rewrite governing instructions
or automatically adopt learning during the mission they govern.
