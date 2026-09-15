# Code research priorities

Reviewed 2026-09-13. These are research conclusions from inspected public
sources, not an AMC-owned eval farm and not claims of overall superiority.
Do not turn the “next check” notes into subject-run batches. Recheck the source
and obtain task authority before implementing a proposal.
Use this alongside the broader [implementation comparison](choosing.md)
and the [15 September 2026 source audit](source-audit-2026-09-15.md).
Superpowers, Spec Kit, mini-SWE-agent and host worktrees/VMs are contrast
sources in that audit, not AMC dependencies.

Two independent Luna researchers inspected AMC tooling and competitor mechanisms.
The controller checked retained anchors, counterevidence and priorities. No
competitor code or product application was executed, and this research changed
no runtime or tooling code. The only executable research probe used Python's
standard JSON decoder and read the two existing evaluator definitions.

| Source | Inspected identity |
|---|---|
| AMC tooling | [b6d6294](https://github.com/byensitmagnus/agent-mission-control/tree/b6d6294e6f6bda574c5f7fbaefd787ee231c3f30); subsequent changes in this pass are documentation only. |
| Agent Orchestrator (AO) | [63a04f0](https://github.com/byensitmagnus/agent-orchestrator/tree/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03) in the requested fork. |
| Codex Astra/Luna Orchestrator (CALO) | [014b1d7](https://github.com/byensitmagnus/codex-astra-luna-orchestrator/tree/014b1d7c48c39087beec8aa4f1ca022053ac17b3) in the requested fork. |

The existing local upstream clones had different heads. The exact fork commits
were fetched and inspected without changing their working-tree checkouts.
Static mechanisms below are not claims that upstream tests or host journeys ran.

## R1 — Investigate stricter evaluator input validation

**Observed:** AMC's [fixture loader](https://github.com/byensitmagnus/agent-mission-control/blob/b6d6294e6f6bda574c5f7fbaefd787ee231c3f30/scripts/prepare_eval.py#L24-L27)
and [structural validator](https://github.com/byensitmagnus/agent-mission-control/blob/b6d6294e6f6bda574c5f7fbaefd787ee231c3f30/scripts/validate.py#L212-L226)
use ordinary JSON decoding. Repeating a member such as `prompt` keeps its last
value. This behavior was confirmed in a standard-library probe and is
[documented by Python](https://docs.python.org/3/library/json.html#repeated-names-within-an-object).
A visually reviewed definition could therefore contain a misleading earlier value.

**Counterevidence:** both current evaluator JSON files have no repeated members.
The preparer also records [effective case and prompt hashes](https://github.com/byensitmagnus/agent-mission-control/blob/b6d6294e6f6bda574c5f7fbaefd787ee231c3f30/scripts/prepare_eval.py#L150-L159).
No existing result was shown to be corrupt or nondeterministic. The controller
therefore narrowed the researcher's reproducibility claim to a low-priority
defensive validation opportunity. It is separate from the already repaired
duplicate **session ID** accounting bug.

**Next check:** in a disposable copy, supply one duplicate-member case to both
supported entrypoints and record the outcome. If rejecting ambiguous input is
accepted, use a small standard-library decoding hook and one focused negative
control; preserve valid input behavior. The historical
[v3 loader](https://github.com/byensitmagnus/agent-mission-control/blob/b6d6294e6f6bda574c5f7fbaefd787ee231c3f30/evals/v3/prepare.py#L75-L81)
has the same decoding pattern, but frozen evaluation artifacts must remain intact.
No parser change was implemented in this research pass.

## R2 — Observe uncertain worker creation before adding recovery fields

AO's switch coordinator [matches an idempotency key to the request](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/session_manager/agent_switching.go#L175-L204)
and [reads back durable identities after an ambiguous store result](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/session_manager/agent_switching.go#L315-L365).
That is concrete recovery machinery for a harness switch, not a generic promise
about every delegated task. It suggests a useful scenario for AMC: the host may
have created a worker even when the lead lost the response.

AMC already [requires native-state reconciliation and forbids a replacement
while the old writer remains uncertain](../references/resume.md#reconciliation).
The controller deferred the researcher's proposal to add mandatory admission
keys: a Markdown field cannot supply atomic deduplication, and the host may
already provide the needed operation identity.

**Next evidence:** during a bounded disposable recovery task, record the real
host's operation/session identity, ambiguous outcome, read-back and final owner.
Confirm that the lead resumes without an overlapping writer or user relaying
messages. Only an observed gap justifies a host-specific example or implementation.
A simulated ledger can test ledger logic; it cannot prove native recovery.

## R3 — Defer a portable session-stop feature

AO defines an [optional native-session termination contract](https://github.com/byensitmagnus/agent-orchestrator/blob/63a04f08fc5a5804a2306e96d1c59fc4a7f68c03/backend/internal/ports/agent.go#L92-L98):
stop the specified session before destroying its terminal/worktree, preserving
the resumable transcript. This pass verified that interface, not every adapter's
implementation or runtime guarantee.

**Next evidence:** if ordinary AMC work exposes an interrupted worker that can
still write, reproduce it in a disposable project. Inspect the actual host's
stop/status tools and preservation behavior before documenting a remedy.
AMC has no universal process controller; do not invent one or add a daemon to
match a competitor's feature list. The user benefit would be preventing orphan
writers, but no new host leak was established here.

## R4 — Keep adaptive routing and optional model profiles

CALO's [Pro configuration](https://github.com/byensitmagnus/codex-astra-luna-orchestrator/blob/014b1d7c48c39087beec8aa4f1ca022053ac17b3/profiles/pro/codex/config.toml#L15-L33)
makes the Astra lead, Luna children and concurrency explicit. This is useful
setup convenience. AMC already offers an [optional Codex profile](../examples/codex/README.md)
while keeping the runtime portable and using available host capabilities.
Keep that separation; no measured comparison supports making this topology
mandatory or adding more roles. Clear installation and role ownership are useful
patterns already incorporated into AMC's [host guide](hosts.md).

## What this changes in the priorities

The smallest new code investigation is R1. The larger user-benefit question is
R2 combined with native first use: can the lead deliver and recover without
making the user coordinate agents? Observe those on useful work within the
available budget. The [Terra-to-Luna research observation](engineering-candidate.8.md#read-only-research-observation)
supports one successful delegation/review outcome; it does not answer recovery,
cross-host activation, comparative cost or general quality.

Keep documented partial-output behavior as it is unless real failed retries
show material user friction. Automatic cleanup would need preservation proof,
not merely fewer files. No dashboard, new service, compulsory workflow stage or
model benchmark follows from this research.
