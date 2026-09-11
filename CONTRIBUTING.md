# Contributing

Keep changes small and tied to an observed workflow failure or a reproducible
improvement.

1. Explain the task that exposed the problem.
2. Show the existing behavior and the desired behavior.
3. Change the fewest instructions needed.
4. Run `python scripts/validate.py`.
5. Include evidence that the change improves the target case without weakening
   scope, safety, or verification gates.

Do not add provider-specific policy, speculative roles, or mandatory agents for
work that a single agent can complete directly.
