schema_version: 1
overall: NOT VERIFIED

# Unified AMC kernel

## Goal / Definition of Done

North star: `.claude/GOAL.md`. Public `main` holds the current kernel. Install
matches that kernel. Engineering checks pass. No homemade subject-run farms.
Behavior, price and speed remain NOT VERIFIED. No new GitHub release in this round.

## Base and candidate

Current artifact: GitHub `main` after PR https://github.com/byensitmagnus/agent-mission-control/pull/6
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
| Behavioral superiority vs direct work | NOT VERIFIED | nine Codex runs: no unique win; contaminated Superpowers plugin |

## Authority

Authorized: local engineering and docs on `main`.
Forbidden: new GitHub release, global install, host-config change, daemons,
new services and new AMC subject-run batches.

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
| Three-arm comparison | Lead | no | superseded | NOT VERIFIED | superseded: farm closed; conclusion in postmortem |

## Decisions and evidence

Engineering integrity is separate from agent quality. The 16 common AMC runtime
files are byte-identical in skill and plugin packages; ZIP archives are not.
The nine Codex runs are summarized in `evals/candidate.9/README.md`. Raw
transcripts were removed; the negative conclusion is kept. Kernel changes cite
graded sources in `docs/field-state.md`. Historical `c9-01` remains a failed
hidden False pair. Direct-first is a cautious sequential default, not a natural
law. Skills and MCP are complementary. Strong-lead plus cheaper-worker is an
optional graph under the cost-aware preflight, not AMC's identity.
Install from `main`. The candidate.8 ZIP remains the last tagged package.

## Blockers

None.

## Next action

Do not cut a GitHub release. Use AMC on commissioned work.

## Last verified

Commit/snapshot: `main` `1f4b676423608af44bf14c0b13f8e8c5ba776baa`. UTC timestamp: 2026-09-15T13:30:22Z.
