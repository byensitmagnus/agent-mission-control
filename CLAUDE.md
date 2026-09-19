# Working in this repository

Agent Mission Control is a **portable Markdown skill**. It is not a runtime,
framework, daemon or extra server.

Runtime copied into user projects: `SKILL.md`, `LICENSE`, `VERSION`,
`references/`, `templates/`, `agents/`, `assets/`, `scripts/amc-check.py`,
`scripts/amc_guard.py`. Everything else is repo documentation, packaging or
checks.

Hard rules for agents working here:

1. Keep the smallest honest workflow. Do not add a second orchestrator.
2. Do not release, globally install or change host config without an
   explicit mandate in the current session.
3. Do not start homemade subject-run farms. Engineering checks and defects on
   real commissioned work are allowed.
4. Do not claim AMC is cheaper, faster or better without external evidence or
   real usage telemetry. Unknown numbers stay unknown.
5. Cite [field state](docs/field-state.md) for evidence grades. Load
   [SKILL.md](SKILL.md) only as far as the task needs.

Active goal: [.claude/GOAL.md](.claude/GOAL.md).
Checks: [docs/development.md](docs/development.md).
Contributing: [CONTRIBUTING.md](CONTRIBUTING.md).
