schema_version: 1
overall: NOT VERIFIED

# Truth Layer v1

## Goal / Definition of Done

Canonical fail-closed control contract for intent, route, observation, artifact
identity and acceptance. Engineering checks on this branch. Behavioral
superiority remains NOT VERIFIED. No push, merge, tag or release.

## Base and candidate

Current artifact: dirty working tree on `codex/truth-layer-v1` over base tree
`9a347734ba8e2e4974160a8e1a3f77c1b0b8dc28`. Candidate commit SHA is not stored
in this file.
Previous published ZIP: `v0.2.0-candidate.8` (older runtime).
Candidate.9: `main` source, no tagged ZIP.

## Hard gates

| Gate | Status | Evidence |
|---|---|---|
| False overall PASS rejected | PASS | `scripts/test_validate.py`; queued/running jobs forbidden under overall PASS |
| Plugin copy is one AMC workflow | PASS | `scripts/package_plugin.py`; `agents/openai.yaml`; `SKILL.md` |
| Blank templates vs examples | PASS | `templates/`; `examples/packets/` |
| Optional profiles not frozen to named models | PASS | `scripts/validate.py` Codex rules |
| Compact live mission | PASS | this file; `docs/history/through-candidate.8.md` |
| Same-lead engineering notes | PASS | `docs/reviews/`; not independent public review |
| Homemade subject-farm closed | PASS | [postmortem](evals/candidate.9/README.md); raw JSONL removed |
| Field-state evidence model | PASS | [field-state.md](docs/field-state.md) grades A–E |
| Install matches current source | PASS | `docs/getting-started.md` installs `main`, not the candidate.8 ZIP |
| Truth Layer contract self-check | PASS | `python evals/control_contract.py --self-check` 58 cases, extra-error harness; engineering only |
| Behavioral superiority vs direct work | NOT VERIFIED | nine Codex runs: no unique win; contaminated Superpowers plugin |

## Authority

Authorized: local engineering and docs on `codex/truth-layer-v1`.
Forbidden: push, merge, GitHub release, global install, host-config change, daemons,
new services, new AMC subject-run batches and GitHub settings changes.

## Jobs

| Job | Agent | Required | Lifecycle | Verdict | Owned scope |
|---|---|---|---|---|---|
| Validator, plugin and PASS rules | Lead | yes | completed | PASS | `scripts/validate.py`, tests |
| Runtime kernel and templates | Lead | yes | completed | PASS | `SKILL.md`, `references/`, `templates/` |
| Docs, field state and postmortem | Lead | yes | completed | PASS | `docs/`, `README.md`, `evals/candidate.9/README.md` |
| Cost-aware delegation, profiles and D-grade field table | Lead | yes | completed | PASS | `references/resources.md`, `examples/profiles.md`, `evals/decision_kernel.py` |
| Repo front door, docs map and agent instructions | Lead | yes | completed | PASS | `README.md`, `docs/README.md`, `AGENTS.md`, `.claude/GOAL.md` |
| User path install → first task | Lead | yes | completed | PASS | `docs/getting-started.md` |
| Open PR against main | Lead | yes | completed | PASS | https://github.com/byensitmagnus/agent-mission-control/pull/6 |
| Merge PR #6 | Lead | yes | completed | PASS | `main` `1f4b676` |
| Truth Layer v1 contract | Lead | yes | completed | PASS | `evals/control_contract.py`, docs, governance templates |
| Three-arm comparison | Lead | no | superseded | NOT VERIFIED | superseded: farm closed; conclusion in postmortem |

## Decisions and evidence

Engineering integrity is separate from agent quality. Machine semantics for the
control contract live in `evals/control_contract.py`. Markdown mission views
remain human projections. `SKILL.md` is unchanged in this round. The nine Codex
runs stay a closed postmortem. Kernel changes cite graded sources in
`docs/field-state.md` (pins dated 2026-09-15, not revalidated 2026-09-18).
Install from `main`. The candidate.8 ZIP remains the last tagged package.

## Blockers

None.

## Next action

Finish nothing further in this local slice. Do not push, merge or cut a GitHub release.

## Last verified

Commit/snapshot: base tree `9a347734ba8e2e4974160a8e1a3f77c1b0b8dc28` on `main` `df184ad`. UTC timestamp: 2026-09-18T08:40:00Z.
This file does not pin the candidate commit SHA.
