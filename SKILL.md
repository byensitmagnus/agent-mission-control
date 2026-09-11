---
name: agent-mission-control
description: "Run complex, high-risk, or release-critical software work through scoped orchestration, isolated agents, measurable optimization, independent proof, and validation-gated learning. Use for major refactors, performance work, migrations, or multi-surface releases; skip routine one-pass changes."
---

# Agent Mission Control

This skill works standalone. When `context-diamond`, `avo`,
`skillopt-sleep-learned`, or `skillopt-sleep` are installed, load only the one
needed for the current phase and let its detailed procedure override overlapping
guidance here.

## Qualify the run

Use Mission Control when at least one is true:

- two or more substantial independent jobs can run concurrently;
- architecture, migration, security, data integrity, or release risk needs a
  separate decision and verification layer;
- success requires measurable candidate iteration rather than a one-pass fix;
- several customer-facing surfaces must remain consistent through a release.

Otherwise use the normal single-agent workflow. Multiple files alone do not
make a task complex.

## Freeze the control contract

Before implementation, record:

```markdown
Goal / Definition of Done:
Source of truth and baseline:
Hard correctness and release gates:
Frozen evaluator or acceptance checks:
Authorized scope and control gates:
Attempt / time budget:
Open risks and unknowns:
```

For work likely to cross context boundaries, update the project's existing
durable tracker; create `MISSION.md` only when none exists. Store observable
facts—current commit, changed paths, commands, scores, failures, approvals—not
agent confidence or raw transcripts.

## Route work

The lead owns the contract, architecture, task graph, integration decisions,
release conclusion, and final evidence. Keep the user's selected lead; in Codex
prefer Astra for this role when available.

1. Run a fake-edge test: for each proposed job, ask whether it truly needs the
   previous job's output. Fan out only when at least two substantial jobs are
   independent or the user explicitly requests parallel work.
2. Give each worker one contract: objective, owned paths or surface, inputs,
   constraints, required artifact and evidence, and acceptance check. Prefer
   read-only research; concurrent writers need separate worktrees or disjoint
   ownership. Never let two agents mutate the same candidate or integration
   surface.
3. Use direct implementation for a linear, well-understood change. Do not add
   workers just to fill roles.
4. Use a candidate loop only for measurable optimization or iterative repair.
   Freeze the evaluator before candidate 1. Delegated work may supply evidence
   or a bounded change, but it may not change the evaluator, goal, or incumbent.

When available, use `context-diamond` for steps 1–2 and `avo` for step 4. Their
current model-routing and candidate-selection rules are authoritative.

Workers report claims with file or symbol references, commands and observed
results, unresolved risks, and dependencies. Missing output is missing—not a
pass. Derive status from the workspace, tests, runtime, CI, review, and approval
state rather than narrative updates.

## Execute the graph

```text
contract -> explore -> lead decision -> isolated build
         -> evaluate/repair -> independent review -> lead verification
         -> release gate -> post-run learning
```

- Exploration may fan out. Architecture choice, integration, shared-file edits,
  and release decisions serialize through the lead.
- In a candidate run, keep the incumbent recoverable, change one bounded
  hypothesis per candidate, record rejection diagnoses, and stop at the fixed
  budget or a verified winner.
- A fresh verifier tries to disprove the result from the frozen contract and
  current artifacts. Agent agreement, a handoff summary, or a self-reported
  green test is not proof.
- For customer-facing or installer releases, compare the candidate with a
  rendered or executable baseline on every affected surface. Preserve existing
  data, images, prices, settings, CTAs, and flows unless their change is
  explicitly in scope. Include a negative control for data-loss protections.
- Stop immediately before merge, push, deploy, publication, destructive action,
  credential use, or an unapproved product decision unless the current request
  already authorizes that exact consequence.

## Close and learn

Finish with one release verdict: `PASS`, `FAIL`, or `NOT VERIFIED`, mapped to
every frozen gate and backed by concrete evidence. A plan, worker return,
candidate, review, or build alone is not completion.

Keep runtime learning separate from runtime authority:

1. After the verified run, retain only short reusable lessons with their task,
   outcome, evaluator, and evidence. Never retain secrets, customer data, raw
   prompts, transcripts, or provider payloads.
2. Do not rewrite this or another governing skill during the run.
3. When repeated tasks justify skill optimization, use a held-out evaluation:
   harvest evidence, replay representative tasks, propose bounded edits, reject
   regressions, and stage the winner before adoption. Use `skillopt-sleep` when
   installed; never auto-adopt without current user authorization.
4. Without a held-out evaluator, leave the lesson as a proposal. A plausible
   reflection is not learned guidance.

## Non-goals

- Do not recreate a daemon, database, Kanban, provider adapters, or a generic
  DAG engine inside a skill.
- Do not promise cost savings from model routing; measure token and time use on
  the actual task when cost is an objective.
- Do not generalize published benchmark gains to a project without a local
  baseline and evaluator.
