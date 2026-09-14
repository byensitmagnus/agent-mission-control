schema_version: 1
overall: NOT VERIFIED

# Unified AMC kernel

## Goal / Definition of Done

Ship Agent Mission Control as one workflow skill/plugin on a PR against `main`.
Engineering checks must pass. Improved agent behavior, cost and speed versus
direct work remain NOT VERIFIED.

## Base and candidate

Current artifact: branch `codex/unified-amc-kernel` on base `c49dc1be2e334091f6c841047ff2ad778b7bde84`
Base: GitHub `main` / published `v0.2.0-candidate.8`.
Candidate: `0.2.0-candidate.9`; one decision kernel; no companion runtime.

## Hard gates

| Gate | Status | Evidence |
|---|---|---|
| False overall PASS rejected | PASS | `scripts/test_validate.py` negative controls, including superseded and live placeholders |
| Plugin copy is one AMC workflow | PASS | `scripts/package_plugin.py`; `agents/openai.yaml`; `SKILL.md` |
| Blank templates vs examples | PASS | `templates/`; demonstrations in `examples/packets/` |
| Optional profiles not frozen to named models | PASS | `scripts/validate.py` Codex rules; other-model positive control |
| Compact live mission | PASS | this file; history in `docs/history/through-candidate.8.md` |
| Behavioral superiority vs direct work | NOT VERIFIED | `evals/v3` has no subject runs on this SHA; `c9-01` both arms fail the hidden False case |

## Authority

Authorized: local edits, tests, offline packages, one read-only review, push and
PR against `main`.
Forbidden: merge, release, installation, publication, global skills, host
configuration, daemons and new services.

## Jobs

| Job | Agent | Required | Lifecycle | Verdict | Owned scope |
|---|---|---|---|---|---|
| Validator, plugin and PASS rules | Lead | yes | completed | PASS | `scripts/validate.py`, `package_plugin.py`, tests |
| Runtime kernel and templates | Lead | yes | completed | PASS | `SKILL.md`, `references/`, `templates/`, `MISSION.md` |
| Docs, history and research claims | Lead | yes | completed | PASS | `docs/`, `README.md`, `docs/history/` |
| Independent falsification review | Reviewer | yes | completed | PASS | PASS rules; reviewer 2d743209 holes closed in `scripts/validate.py` |
| Open PR against main | Lead | yes | queued | NOT VERIFIED | branch `codex/unified-amc-kernel` |
| Bounded behavioral comparison | Lead | no | queued | NOT VERIFIED | `evals/candidate.9/`; `evals/v3/` |

## Decisions and evidence

Engineering integrity is checked by local tests, not by agent quality. Skill and
plugin runtime bytes must match. Historical qualification FAIL and the Sol 18/18
pair are unchanged. Structural validator PASS is not product PASS. Candidate.9 is
not claimed better than direct work. Residual: a dummy required PASS job can still
hide unfinished work as optional queued; that remains a false record.

## Blockers

None.

## Next action

After checks and review, push this branch and open a PR against `main`. Do not
merge or release.

## Last verified

Commit/snapshot: branch `codex/unified-amc-kernel` on base `c49dc1be2e334091f6c841047ff2ad778b7bde84`. UTC timestamp: 2026-09-14T11:52:51Z.
