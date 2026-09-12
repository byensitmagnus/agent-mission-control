<p align="center">
  <img src="assets/mission-control.svg" alt="Agent Mission Control" width="100%" />
</p>

<p align="center"><strong>One lead. Focused agents. Measurable progress. Independent proof.</strong></p>

<p align="center">
  <a href="https://github.com/byensitmagnus/agent-mission-control/actions/workflows/validate.yml"><img src="https://github.com/byensitmagnus/agent-mission-control/actions/workflows/validate.yml/badge.svg" alt="Structural validation" /></a>
  <a href="https://github.com/byensitmagnus/agent-mission-control/releases"><img src="https://img.shields.io/github/v/release/byensitmagnus/agent-mission-control?color=8b5cf6" alt="Published release" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22d3ee" alt="MIT License" /></a>
</p>

Agent Mission Control turns one software objective into the smallest useful
workflow and verifies completion. The lead owns architecture and integration.
Clear edits stay direct; scouts, workers and loops are added only when useful.
The core works without companion skills or a custom runtime.

This is an **unreleased standalone candidate**. Current work and proof are in
[the standalone report](evals/v0.2-standalone-candidate.md) and [MISSION](MISSION.md). The following comparisons are retained history. The [previous qualification](evals/v0.2-qualification.md)
ended **FAIL** after 19 controlled subjects. [Iteration 2](evals/v0.2-control-candidate.md) narrowed activation
and removes competing execution ownership. It is staged for review; improved
engineering outcomes and token savings remain **NOT VERIFIED**.

[Design sources and license decisions](references/provenance.md) explains the adopted and
rejected mechanisms. Native sessions, tools and context management remain with
Codex or the host.

## One execution owner

| Need | Owner |
|---|---|
| Ordinary edit or understood dependency chain | Lead's normal implementation/check loop |
| One focused independent job | Native scoped worker when it adds useful value |
| Substantial independent workstreams | AMC work/context routing; native agents |
| Measured candidate optimization | AMC frozen evaluator, recoverable incumbent and bounded attempts |
| Cross-phase state, recovery and final acceptance | Lead with Mission Control |
| Offline learning | Separate completed-task workflow |

The entrypoint loads relevant references for work/capability routing, optimization,
review, recovery, resource checks or separate learning. Context Diamond, AVO and
SkillOpt are credited design sources, not required installations. Domain skills
remain optional technical help. Explicitly requested procedures retain one owner;
do not duplicate their loops or bypass their gates.

If optimization delegates jobs, the lead retains selection and workers own only
those bounded jobs. Reuse the existing tracker and adequate current review;
Mission Control does not create an additional team or verification cycle.
The lead still inspects artifacts and executes relevant acceptance checks.
Required independent proof is never invented when only one agent is available.

## Use the skill

```text
$agent-mission-control

Prepare this application for release. Preserve existing user data, delegate
independent work where useful, verify it, and stop before deploy.
```

A bounded handoff can be this short:

```text
Goal: Check deadline behavior in transport.py against requirements.md.
Why independent: Storage review does not need this result.
Base: The lead's recorded commit plus current transport.py snapshot.
Owner: Read-only transport.py and requirements.md; preserve others' work.
Authority: Local reads and non-mutating checks; no external changes.
Return: Boundary results, file anchors and risks; verify before/at/after expiry.
```

Use only relevant context. [Work and capability routing](references/packets.md) covers ownership
transfers; the [populated packet](templates/context-packet.md) gives a longer
example when needed.

## Resume from facts

For a long mission, reuse its existing tracker or the
[Mission View template](templates/mission-view.md). Record gates, owners,
commands, results and artifact identities. On resume, reconcile that record
with HEAD, uncommitted files, test output and still-running workers.
An old PASS cannot override a current failure. See
[reconciliation](references/resume.md).

Safe local edits, tests and repairs continue within existing authority.
Stop at an unauthorized external or destructive action. A local PASS grants
no deployment permission. The [release example](examples/fps-booster-release.md)
is illustrative, not measured proof.

## Build and install

The repository root is the only canonical skill source. Python 3.11+ builds
both formats into **new paths outside the source tree**:

```bash
python scripts/package_plugin.py ../amc-packages/skill/agent-mission-control --format skill --archive ../amc-packages/skill.zip
python scripts/package_plugin.py ../amc-packages/plugin/agent-mission-control --archive ../amc-packages/plugin.zip
```

| Format | Contents | Installation |
|---|---|---|
| Skill | SKILL.md, references, templates, UI metadata, assets and license | Place the built folder in a new `.agents/skills/agent-mission-control` directory in the intended project |
| Codex plugin | `.codex-plugin/plugin.json` and the same skill under `skills/agent-mission-control/` | Register the built plugin through a configured marketplace, then install with the host's Plugins browser |

See [OpenAI's plugin setup guide](https://developers.openai.com/codex/plugins)
for marketplace and installation support in the actual client. Start a new
session after installation. Plugin host installation and discovery are
**NOT VERIFIED** here; package validation is a separate check. No project
configuration or custom agents are installed by the builder.

Existing destinations and archives are refused. The builder rejects traversal,
linked paths and outputs inside the source. The default source must be this
repository with the expected origin; packaging an explicitly supplied trusted
snapshot is a Python API operation for tests and offline builds. Source bytes
are copied unchanged. Tracked text uses LF for portable Git snapshots; an
explicit external snapshot is copied without normalization. ZIP entry order,
timestamps and permissions are fixed.
Failures may leave a newly created partial output for inspection.

For updates, build a new version in a separate directory, compare it with the
installed files and preserve local customizations before an authorized switch.
Do not blindly overwrite. To uninstall a skill, remove only its confirmed
installation directory after preserving edits; uninstall a plugin through the
host's plugin manager. The builder performs neither action.

The [optional Codex profile](examples/codex/README.md) shows independently configured lead and child models/reasoning. It is not loaded by the
portable runtime. Actual cost, token savings and broad compatibility are
not established.

## Verification and development

```bash
python scripts/validate.py
python scripts/test_validate.py
python scripts/test_prepare_eval.py
python scripts/test_package_plugin.py
```

These check package structure and safety, including negative controls and
disposable fixture integrity. They do not prove agent behavior. The
[11-case behavioral suite](evals/README.md) covers discovery, direct work,
dependencies, ownership, resume, measurable variation, release risk and
authority. Compare all three sources under the same frozen rubric.

[Previous qualification](evals/v0.2-qualification.md) preserves the failed
comparison and its limitations. [Offline skill evolution](CONTRIBUTING.md)
uses completed-run failures and held-out replay; it never rewrites the skill
during the mission it governs. Read [security guidance](SECURITY.md) before
reporting vulnerabilities.

[MIT](LICENSE) Â© 2026 Byens IT. Independent project; no endorsement by OpenAI,
NVIDIA, Microsoft or the projects that inspired it.
