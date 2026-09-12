---
name: agent-mission-control
description: "Choose and run an adaptive software workflow: direct work, scoped agents, measured improvement, review and recovery. Use for an objective needing coordinated execution and verified completion."
---

# Agent Mission Control

Build the smallest execution graph that can complete and verify the objective.
The lead owns scope, architecture, integration and final acceptance. AMC works
on its own; no companion skill, custom agent or service installation is required.
Use the native host for tools, sessions, subagents and context management.

## Choose the next useful work

First judge the objective, current facts, authority and acceptance criteria.
Keep trivial edits and understood dependency chains direct: implement, check,
finish. If important uncertainty makes decomposition useful, send a cheap,
focused scout the minimum facts and one question about the proposed graph.
The scout advises; the lead decides. Never spawn it merely to confirm an obvious
route. For scouting or delegation, read [work and capability routing](references/packets.md).

Add nodes only when they earn their coordination cost: investigation that closes
an uncertainty, independent implementation, integration after a real dependency,
or review that can falsify a material claim. Remove fake dependencies; serialize
shared writes. Adapt ownership and remaining nodes when new evidence changes the
plan. There is no required team size, topology or phase sequence.

| Condition | Load when needed |
|---|---|
| A reproducible measure makes candidate selection useful, even for one subtask | [Measured improvement](references/optimization.md) |
| Material correctness uncertainty, sensitive data or release risk | [Independent review and proof](references/verification.md) |
| Cross-phase state or interruption | [Reconciliation](references/resume.md) |
| Another costly fan-out, escalation, candidate or repeated repair | [Resource checkpoint](references/resources.md) |
| Completed work produced a reusable lesson | [Separate learning](references/learning.md) |

Load only the relevant mechanism. Available domain skills may supply missing
technical knowledge. AMC owns this workflow; do not stack another orchestration
or optimization procedure onto the same responsibility. Honor explicitly
requested procedures, name that owner and reuse its current proof instead of
running duplicate loops. A failed procedure cannot be bypassed to evade a gate.

## Finish from evidence

Reuse the existing mission record for long work: unresolved gates, artifact
identities, owners and next authorized action, not a second transcript. A stale
PASS or completed worker is not acceptance. The lead inspects results and runs
relevant checks. Reuse unaffected current proof; refresh affected proof after
repair. Missing required evidence is NOT VERIFIED; an observed failure is FAIL.
PASS requires every applicable gate on the identified current artifact.

Continue authorized local implementation, diagnosis, repair and checks. Stop at
a necessary external blocker after completing independent safe work, or before
an unauthorized external/destructive consequence. Saved state and workers cannot
expand authority; PASS grants no publishing rights. Never change the governing
skill during the run it controls. Skill development uses a separate candidate.
