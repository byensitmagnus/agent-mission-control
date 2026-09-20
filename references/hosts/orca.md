# Orca host profile design (v0)

Accessed: 2026-09-20. Pinned source: [`stablyai/orca`](https://github.com/stablyai/orca)
(Stably Inc. / Lovecast Inc., MIT license, `main` branch snapshot 2026-09-20;
specifically `skill-guides/orchestration.md` and CLI documentation).
Popularity is developer interest, not performance proof.

## Classification

Orca is classified as:
- **Desktop/remote Agent Development Environment (ADE):** runs multiple CLI
  coding agents side-by-side with worktree, terminal and browser integration.
- **Execution substrate:** supplies processes, isolated worktrees, pseudo-terminals
  (PTYs) and environment routing.
- **Structured orchestration runtime:** provides Run inboxes, Task DAGs,
  Dispatches, worker mail and decision gates via CLI/RPC.
- **Optional AMC host:** AMC can run inside an Orca terminal as a skill, or
  direct Orca Dispatches for execution.
- **Not AMC's portable core:** AMC remains a portable Markdown skill without
  daemons, runtime dependencies, databases, cloud accounts or UI dependencies.

General behavioral superiority of multi-agent or Orca-managed workflows versus
direct single-agent work remains **NOT VERIFIED**.

## Single workflow owner

AMC and Orca must never act as competing orchestrators for the same task:

- **AMC owns:** workflow policy, smallest-useful-route choice, authority boundaries,
  break-even calculation, artifact reconciliation, verification rules and final
  acceptance.
- **Orca supplies:** execution substrate, PTY/terminal handles, git worktree
  creation/teardown, message delivery, and child process status.

When using AMC within Orca:
1. AMC lead formulates the contract and chooses whether to delegate.
2. If delegated, AMC emits an Orca Task and Dispatch.
3. The worker executes under Orca's PTY and reports `worker_done`.
4. AMC lead inspects artifacts, runs verification checks and decides acceptance.

## Design mapping: AMC to Orca

| AMC semantic entity | Orca orchestration entity | Mapping & command mechanism |
|---|---|---|
| **Mission** | **Run** | `orca orchestration run-create --objective "<objective>" --json` |
| **Job** | **Task** | `orca orchestration task-create --spec "<spec>" [--deps <ids>] --json` |
| **Attempt** | **Dispatch** | `orca orchestration worker-start --task <id>` or `dispatch --task <id> --inject` |
| **Observed child** | **Dispatch ID + Terminal/Worktree** | `dispatchId` bound to `agentTerminalHandle` and worktree path |
| **Isolation evidence** | **Worktree + Branch + Host** | Verified git worktree directory, branch name, and PTY process identity |
| **Blocker** | **Decision gate / Blocked task** | `orca orchestration ask` or task status set to `blocked` |
| **Completion** | **worker_done** | Message of type `worker_done` explicitly bound to both `taskId` and `dispatchId` |
| **Retry** | **New Dispatch** | Fresh Dispatch on existing Task; previous Dispatch marked superseded/failed |
| **Cleanup** | **Explicit lifecycle** | `reuse` (existing terminal), `retain` (debug/re-inspection), or `release` |

## Adopted Orca-inspired principles

1. **Task identity separate from attempt identity:**
   A Task represents the unit of work and its acceptance contract. A Dispatch
   represents one concrete attempt on a terminal. Retries create a new Dispatch
   under the same Task, preserving failure history without mutating task requirements.

2. **Stale attempts cannot complete the active task:**
   A `worker_done` signal from an earlier, superseded Dispatch (e.g. from an
   interrupted or timed-out attempt) is rejected. Only the active, attested
   `dispatchId` can complete a Task.

3. **Separate requested versus effective execution profile:**
   The requested model/effort/capability (from AMC Context Packet) is recorded
   separately from the effective host/model/runtime that actually executed the
   job (from Orca terminal inspection).

4. **Missing observation is not proof of termination:**
   A polling timeout or missing message is a checkpoint, not a confirmation that
   the worker has failed or exited. Workers must be inspected or explicitly
   heartbeat-monitored before declaring abandonment.

5. **Explicit cleanup ownership:**
   Worktrees and terminals must have an explicit disposal policy: `retain` on
   unresolved failure or review, `release` on verified acceptance, `reuse` for
   sequential iterations with unchanged dependencies.

6. **Version-matched host guidance:**
   Use the exact CLI grammar and RPC conventions supported by the observed Orca
   version rather than hardcoding legacy or speculative flags.

## Explicitly rejected patterns

- **Parallel racing as default:**
  Racing multiple agents on the same problem consumes tokens and attention
  without established expected-value gain. AMC requires explicit break-even and
  independent tasks for concurrency.

- **Worktree as a complete security sandbox:**
  Git worktrees isolate filesystem writes from the main working directory. They
  do not sandbox network access, system processes, IPC, environment secrets or
  shared operating system resources.

- **Full-autonomy flags as requirement:**
  AMC enforces authority boundaries. Tools must not bypass permission models or
  circumvent user consent rules.

- **Copying Orca's UI, runtime, cloud, mobile or database into AMC:**
  AMC has zero native runtime footprint. It must not bundle webviews, desktop
  shells, background servers, sync engines or database layers.

- **Orca as a mandatory AMC dependency:**
  AMC remains completely functional on standard terminal hosts (Codex, Claude
  Code, Cursor, Grok, Kimi) without Orca installed.

- **Behavioral superiority claims:**
  No claim that Orca integration makes coding faster, cheaper or higher quality.
  All outcome claims remain `not_verified`.
