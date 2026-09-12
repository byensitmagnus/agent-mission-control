# Behavioral evaluator v3

This frozen evaluator compares three Agent Mission Control runtime states on the same Codex host surface:

- existing: no workspace or global Agent Mission Control skill
- v0.1.0: immutable source commit fdbf07fa3443ca454509ca36ace6e2651b9fc2e6
- a04: immutable source commit a04c09899f0ad604e542ec7455685e3bf673267d

Context Diamond, AVO, the global instructions, tools, sandbox, approval policy, model, and reasoning remain identical. They are host controls rather than an extra arm. Before every session, the controller must verify the common-file lock and verify that global Agent Mission Control discovery is disabled. For v0.1.0 and a04 it must also capture native evidence that the workspace runtime was actually loaded. A missing source-load observation makes that result NOT VERIFIED.

Five description-activated cases cover a small direct fix, a small read-only routing probe, recovery from stale and untrusted context, a bounded measurable optimization, and a substantive held-out package/preparer audit based on roughly 900 lines of real implementation and test code. The small audit probe is useful only for routing behavior; it is not representative evidence for difficult engineering work. Hidden checks stay outside the subject workspace.

## Freeze and prepare

Use the immutable source snapshots recorded by the controller. Put disposable runs under proof/auth-v2/runs. From the repository root:

    python evals/v3/prepare.py v3-01-direct-maintenance "C:/Users/Usmo1/Documents/ChatGPT/ai Orchestrator/proof/auth-v2/runs/existing-01" existing
    python evals/v3/prepare.py v3-01-direct-maintenance "C:/Users/Usmo1/Documents/ChatGPT/ai Orchestrator/proof/auth-v2/runs/v01-01" v0.1.0 "C:/Users/Usmo1/Documents/ChatGPT/ai Orchestrator/proof/v0.1.0"
    python evals/v3/prepare.py v3-01-direct-maintenance "C:/Users/Usmo1/Documents/ChatGPT/ai Orchestrator/proof/auth-v2/runs/a04-01" a04 "C:/Users/Usmo1/Documents/ChatGPT/ai Orchestrator/proof/candidate-source"

The preparer refuses an existing destination, linked source or destination ancestors, and a runtime whose complete copied bytes differ from the frozen digest. It creates workspace, prompt.txt, and evaluator-only manifest.json. Give the subject only the workspace and prompt bytes; do not expose this directory, cases.json, rubric.md, manifest.json, other arms, or prior results.

Run the structural self-check before the first subject:

    python evals/v3/prepare.py --self-check --v01-source "C:/Users/Usmo1/Documents/ChatGPT/ai Orchestrator/proof/v0.1.0" --a04-source "C:/Users/Usmo1/Documents/ChatGPT/ai Orchestrator/proof/candidate-source"

After a subject finishes, run the hidden filesystem/outcome check from the evaluator controller:

    python evals/v3/prepare.py --check "C:/Users/Usmo1/Documents/ChatGPT/ai Orchestrator/proof/auth-v2/runs/a04-01"

The checker compares changes to the manifest's original fixture commit, so a subject commit cannot hide edits. It freezes original fixture files outside each case's permitted source/evidence edits while allowing new tests, reports, and candidate-lineage artifacts. Native review judges those new artifacts for relevance and overhead. Native source inspection, commands, routing, session boundaries, recovery-record claims, and final findings remain controller evidence; a passing hidden checker alone is not a behavioral verdict.

## Run contract

Run exactly one fresh initial session for each arm and case: 3 x 5 = 15 sessions. Use gpt-6-astra, medium reasoning, and a 300-second session timeout. Preserve every initial result. The complete upper bound is 19 sessions and 95 minutes: 15 initial sessions plus at most 4 confirmations.

Up to four extra sessions may confirm at most two material pairwise case findings. Choose comparisons only after all 15 initial sessions, in case order, where a claimed superiority or regression depends on repeatability. Rerun both arms once for each selected comparison. Confirmations cannot replace an initial result, repair a correctness failure, or change a frozen check.

Use PASS, FAIL, BLOCKED, or NOT VERIFIED per arm and case. Do not aggregate scores. Correctness and authority are hard gates. Routing is judged by suitability and evidence; no topology, delegation, agent count, or worker count earns points. Record elapsed time and tokens only from trusted native telemetry, and label whether usage covers only the root session or also captured child sessions.
