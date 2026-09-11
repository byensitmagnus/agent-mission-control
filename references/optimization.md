# Measurable candidate loops

Load only when a reproducible evaluator or observable score makes comparing
candidates useful. Do ordinary feature implementation directly; a test suite
alone does not justify searching alternatives.

Before changing candidate 1, freeze the workload, correctness checks,
environment, metric priority and attempt/time budget. Execute the baseline.
Record its source identity and score, and keep a recoverable incumbent.
An unrepeatable baseline or missing evaluator leaves improvement NOT VERIFIED.

Choose a bounded hypothesis using the task and previous candidates, including
rejection evidence. Implement, evaluate, diagnose and repair autonomously within
scope. The agent chooses how to investigate and edit; no fixed variation
operator or agent topology is required.

Record each candidate's parent, hypothesis, source snapshot, commands,
correctness result, score and acceptance or rejection reason. Accept only
when correctness passes and the frozen selection rule matches or improves
the incumbent without regressing a higher-priority metric. Keep the incumbent
when a candidate loses; an equal score may be retained only if the frozen rule
allows it, and is not an improvement claim.

Workers may supply bounded changes or evidence; they cannot change the
evaluator, goal, selection rule or incumbent. A changed evaluator starts a
separate comparison with the baseline rerun, never a retroactive pass.

When attempts repeat or stall, inspect lineage and raw failure evidence before
choosing a different hypothesis. Exhausting the budget ends the experiment
with the best verified candidate or an exact unresolved gate. Do not expand
the budget or hide failed correctness to manufacture a winner.

Report unavailable cost, tokens or time as NOT MEASURED. This loop optimizes
the task artifact; it never changes the skill governing the current mission.
