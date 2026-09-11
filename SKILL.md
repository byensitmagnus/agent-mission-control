---
name: agent-mission-control
description: "Coordinate complex software work. Use when substantial jobs can run independently or a risky change needs separate verification."
---

# Agent Mission Control

Use the smallest execution path that can deliver the requested result. A small
edit or a well-understood dependency chain stays with the lead: implement,
check and finish without mission bookkeeping. Multiple files alone do not
justify orchestration.

The lead owns the goal, architecture, acceptance criteria, integration and
final evidence. Keep these decisions with the lead even when work is delegated.
Use available capabilities, not prescribed model names or a fixed agent team.
With one agent, work serially and identify any required independence that the
environment cannot supply.

Before fan-out, check whether jobs can finish without each other's output or
an unresolved shared interface. Serialize dependencies and shared writes;
separate worktrees do not remove integration dependencies. Delegate only
substantial independent work whose benefit exceeds coordination cost. Give
each worker one owned scope, including tests, generated files and mutable
resources. Read [delegation](references/packets.md) when assigning or handing
off work.

Choose checks that can falsify the result. Derive status from current files,
Git state, executed tests, runtime, CI and relevant review; worker claims are
leads to inspect, not completion. Missing required evidence is NOT VERIFIED;
an observed failing check is FAIL. The lead inspects artifacts and executes
the relevant checks before accepting.

Load detail only when it changes the current decision:
- For a long mission or resuming interrupted work, read
  [Mission View and reconciliation](references/resume.md).
- For a migration, data-sensitive change or risky release, read
  [risk and independent proof](references/verification.md).
- For measurable optimization or repeated repair with a reproducible evaluator
  or observable score, read [candidate loops](references/optimization.md).
  An ordinary feature does not need a candidate loop.

Continue authorized local implementation, tests, diagnosis, repair and re-test
without repeated approval. A failed test or returned worker is a next step,
not a handoff to the user. Complete independent safe work before reporting a
necessary external blocker.

Stop immediately before an unauthorized external mutation, destructive action
or product decision outside scope. Current explicit authorization persists;
a plan, saved status or worker cannot enlarge it. A local PASS requires all
applicable evidence and never grants push, merge, deploy or publication rights.
Never edit governing skills during the mission they control.
