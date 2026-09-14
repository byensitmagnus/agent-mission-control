schema_version: 1
overall: NOT VERIFIED

# Unified AMC kernel

## Goal / Definition of Done

Keep PR https://github.com/byensitmagnus/agent-mission-control/pull/6 consistent.
Engineering checks must pass. Behavior, price and speed remain NOT VERIFIED.
Do not merge or release.

## Base and candidate

Current artifact: PR #6 `codex/unified-amc-kernel` on base `c49dc1be2e334091f6c841047ff2ad778b7bde84`
Base: GitHub `main` / published `v0.2.0-candidate.8`.
Candidate: `0.2.0-candidate.9`, PR source, not merged, no release ZIP.

## Hard gates

| Gate | Status | Evidence |
|---|---|---|
| False overall PASS rejected | PASS | `scripts/test_validate.py`; queued/running jobs forbidden under overall PASS |
| Plugin copy is one AMC workflow | PASS | `scripts/package_plugin.py`; `agents/openai.yaml`; `SKILL.md` |
| Blank templates vs examples | PASS | `templates/`; `examples/packets/` |
| Optional profiles not frozen to named models | PASS | `scripts/validate.py` Codex rules |
| Compact live mission | PASS | this file; `docs/history/through-candidate.8.md` |
| Public review record | PASS | `docs/reviews/candidate.9-falsification.md`; `docs/reviews/candidate.9-working-tree.md` |
| Holdout correctness vs direct | PASS | all three arms hidden PASS; [results](evals/candidate.9/comparison/results/README.md) |
| Behavioral superiority vs direct work | NOT VERIFIED | nine Codex runs; candidate.9 had no unique win and used more holdout time/tokens |

## Authority

Authorized: local edits, tests, offline packages, one read-only review, push to
PR #6.
Forbidden: merge, release, installation, publication, global skills, host
configuration, daemons and new services.

## Jobs

| Job | Agent | Required | Lifecycle | Verdict | Owned scope |
|---|---|---|---|---|---|
| Validator, plugin and PASS rules | Lead | yes | completed | PASS | `scripts/validate.py`, tests |
| Runtime kernel and templates | Lead | yes | completed | PASS | `SKILL.md`, `references/`, `templates/` |
| Docs and public review record | Lead | yes | completed | PASS | `docs/`, `README.md` |
| Open PR against main | Lead | yes | completed | PASS | https://github.com/byensitmagnus/agent-mission-control/pull/6 |
| Three-arm comparison | Lead | yes | completed | PASS | `evals/candidate.9/comparison/`; nine subject runs |

## Decisions and evidence

Engineering integrity is separate from agent quality. The 16 common AMC runtime
files are byte-identical in skill and plugin packages; ZIP archives are not.
Nine Codex 0.153.3 / Sol / medium runs are bound in
`evals/candidate.9/comparison/results/`. Superpowers plugin contamination was
present on every arm. Candidate.9 is not claimed better than direct work.
Historical `c9-01` remains a failed hidden False pair from another commit.

## Blockers

None.

## Next action

Do not merge or release. Keep overall NOT VERIFIED for product behavior.

## Last verified

Commit/snapshot: PR #6 `codex/unified-amc-kernel` on base `c49dc1be2e334091f6c841047ff2ad778b7bde84`. UTC timestamp: 2026-09-14T16:10:00Z.
