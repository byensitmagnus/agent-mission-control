# Build and check AMC

For using the skill, start with [the setup guide](getting-started.md).
The folder map is [README.md](README.md).
The repository root is the canonical skill source. The Python utilities below
are development tools; users of a ready-made skill ZIP do not need Python.

## Build both formats

Python 3.11+ can build into **new paths outside the source tree**:

```bash
python scripts/package_plugin.py ../amc-packages/skill/agent-mission-control --format skill --archive ../amc-packages/skill.zip
python scripts/package_plugin.py ../amc-packages/plugin/agent-mission-control --archive ../amc-packages/plugin.zip
```

Both ZIPs contain a top-level `agent-mission-control/` folder. The skill format
contains the runtime directly; the plugin format adds `.codex-plugin/plugin.json`
and places the same runtime under `skills/agent-mission-control/`.
The builder installs neither project configuration nor custom agents.

Existing destinations/archives, linked paths, traversal and outputs inside the
source are refused. The default source must be this repository with its expected
GitHub origin. An explicit trusted snapshot can be supplied through the Python
API for tests or offline builds. Source bytes are copied unchanged; ZIP order,
timestamps and permissions are fixed. Failures may leave a new partial output
for inspection. Preserve existing outputs rather than overwriting them.

Record the source identity, runtime hashes and archive SHA-256 values when
distributing. Validate the actual generated packages with the official
skill/plugin validators available in your development environment. Their local
results are separate from host installation/discovery proof.

## Run local engineering checks

```bash
python scripts/validate.py
python scripts/test_validate.py
python scripts/test_prepare_eval.py
python evals/decision_kernel.py --self-check
python scripts/test_package_plugin.py
python scripts/test_install_skill.py
python scripts/test_usage_snapshot.py
python evals/preservation_check.py --self-check
python evals/fps_replay.py --self-check
```

The JSON replay requires .NET 8; see [replay setup](../evals/fps-replays.md) for
an explicit SDK path. These commands do not launch agents. CI runs the local
checks on Python 3.11 and 3.14 with .NET 8. Passing them is not product PASS.

The current local engineering record is
[candidate.9](engineering-candidate.9.md). Historical candidate.8 evidence stays
in [its record](engineering-candidate.8.md).

Root `MISSION.md` and `docs/` are repository status. Packaging copies only
`SKILL.md`, `LICENSE`, `agents/`, `references/`, `templates/` and `assets/`.
The live mission record is not part of the runtime skill or plugin.

The fixtures intentionally contain broken examples for regression controls.
They are not production implementations. Replay C# executes as trusted local
code; the runner is not a sandbox for untrusted submissions.

## Improve the project

Follow [CONTRIBUTING](../CONTRIBUTING.md). Justify a change with a reproducible bug,
a product/compatibility need or a documented source principle. Review it and run
the affected engineering checks. Design from host docs, published research,
other public repositories and known practitioner guidance. Do not add homemade
subject-run farms. Expensive model comparisons are not a contribution
requirement.

[Research review](research-basis.md) · [Field state](field-state.md) ·
[Historical evaluations](../evals/README.md) ·
[Security](../SECURITY.md)
