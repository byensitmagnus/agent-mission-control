# Execution feedback and measured improvement

Use for difficult work that needs repeated investigation, implementation and
repair, or for a subtask with a reproducible optimization measure. Duration alone
needs durable progress, not a candidate search. The lead owns the outer objective;
delegated jobs cannot run a competing outer loop.

## Long work with observable progress

Keep the acceptance criteria and authority explicit. Choose the next unresolved
milestone or uncertainty, inspect relevant code and domain documentation, form a
bounded hypothesis, then implement or probe and inspect actual results. Let new
evidence change the remaining route. A failing input, compiler diagnostic,
behavioral check or observed environment transition can guide the next action;
a numerical performance score is not required for ordinary engineering progress.

Leave a recoverable working checkpoint and update the existing mission record
with the current artifact, completed checks, failed approaches and next useful
action before a handoff or context loss. Resume from [current facts](resume.md).
Completing one milestone does not complete the original objective. Continue its
remaining authorized work; avoid making a separate supervisor or scout for every
step. A researcher may help resolve a concrete uncertainty, not approve routine
progress. Explicit independent acceptance requirements still apply.

## Candidate selection needs a stable evaluator

Before an optimization comparison, freeze workload, correctness gates,
environment, metric priority and attempt/time/resource budget. Execute the
baseline and keep its source recoverable. An unrepeatable baseline leaves the
improvement NOT VERIFIED. Record each bounded hypothesis, parent/source, commands,
correctness, score and diagnosis in the existing record, including failed attempts.
Accept a strict improvement under the frozen rule with no higher-priority
regression; a predeclared FAIL-to-PASS repair can be an improvement. Ties keep the
incumbent. This conservative selection rule is AMC's policy, not NVIDIA's exact
algorithm. Workers cannot change the evaluator or acceptance. A changed evaluator
starts a separate baseline comparison; never weaken it to make a candidate pass.

Identify accepted inputs and observable behavior outside the visible benchmark.
Use the recoverable incumbent for a small differential check of relevant cases
such as types, equality, ordering, first-value retention and mutation. A faster
benchmark cannot justify narrowing that contract. Reject or repair preservation
mismatches. New diagnostics are development evidence and must not silently alter
a frozen evaluation. Account for measurement noise before declaring a gain.

## Stagnation and stopping

Repeated failures, unchanged hypotheses or evaluator drift trigger a review of
raw evidence and lineage. Two consecutive non-improvements is a practical default
for an optimization checkpoint, not a research-established universal threshold.
The lead first revisits assumptions and the failing reproduction. Use a focused
fresh review when it can resolve the impasse; give a less capable worker a clearer
contract or escalate only the unresolved part. The next attempt needs new evidence
or a materially different hypothesis.

Apply the [resource checkpoint](resources.md) before another costly attempt.
At the agreed limit retain the best verified candidate and identify unresolved
gates. Do not expand the budget to manufacture a winner. This loop changes the
task artifact; changing its governing skill belongs to separate development.
