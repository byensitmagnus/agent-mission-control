# Measured improvement

Use for the portion of a mission with a reproducible evaluator or observable
objective measure. Ordinary implementation does not need candidate search.
The lead owns selection; delegated jobs cannot run a competing outer loop.

Before editing, freeze workload, correctness gates, environment, metric priority
and attempt/time/resource budget. Execute the baseline and keep its source recoverable.
An unrepeatable baseline leaves improvement NOT VERIFIED. Try one bounded
hypothesis; record parent/source, commands, correctness, score and diagnosis in
the existing record. Accept only a strict improvement under the frozen rule with
no higher-priority regression; ties keep the incumbent. Workers cannot change the
evaluator or acceptance. A changed evaluator starts a separate baseline comparison.

Repair from observed failures. After two consecutive non-improvements or evaluator
drift, inspect raw evidence and lineage before changing the hypothesis. Before
another candidate, apply the [resource checkpoint](resources.md); do not repeat
a strategy without new information. At the budget limit retain the best verified
candidate and disclose unresolved gates. Do not expand the budget to manufacture
a winner. Report unobserved resources as NOT MEASURED, including missing child
usage. This loop changes the task artifact, not its governing skills.
