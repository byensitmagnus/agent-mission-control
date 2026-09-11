# Contributing

Keep changes small and tied to an observed workflow failure or a reproducible improvement. Never overwrite an existing user file or host configuration during setup or packaging.

1. Explain the task that exposed the problem.
2. Show the existing behavior and the desired behavior.
3. Change the fewest instructions needed.
4. Run `python scripts/validate.py` and `python scripts/test_validate.py` for structural checks.
5. For behavioral claims, run the scenarios documented in [`evals/README.md`](evals/README.md) and record evidence in the relevant candidate log.
Include evidence that the change improves the target case without weakening scope, safety, or verification gates.

Structural checks prove package shape and metadata. Evaluation runs prove the behavior they actually exercise; keep those claims separate.

Do not add provider-specific policy, speculative roles, or mandatory agents for work that a single agent can complete directly. Fixed evaluation rubrics are changed separately from candidate implementations, with the reason and expected effect documented.