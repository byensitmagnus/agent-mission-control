schema_version: 1
overall: NOT VERIFIED

# Unified AMC kernel

## Goal / Definition of Done

Keep PR https://github.com/byensitmagnus/agent-mission-control/pull/6 consistent.
Engineering checks must pass. Do not start homemade subject-run farms.
Behavior, price and speed remain NOT VERIFIED. Do not merge or release.

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
| Public review record | PASS | `docs/reviews/candidate.9-falsification.md`; `docs/reviews/candidate.9-working-tree.md`; `docs/source-audit-2026-09-15.md` |
| Homemade subject-farm closed | PASS | [CONTRIBUTING](CONTRIBUTING.md); comparison marked closed |
| Behavioral superiority vs direct work | NOT VERIFIED | in-house farms rejected; nine Codex runs are a closed record, not a program |

## Authority

Authorized: local docs/policy edits, engineering tests, offline packages, push to
PR #6.
Forbidden: merge, release, installation, publication, global skills, host
configuration, daemons, new services and new AMC subject-run batches.

## Jobs

| Job | Agent | Required | Lifecycle | Verdict | Owned scope |
|---|---|---|---|---|---|
| Validator, plugin and PASS rules | Lead | yes | completed | PASS | `scripts/validate.py`, tests |
| Runtime kernel and templates | Lead | yes | completed | PASS | `SKILL.md`, `references/`, `templates/` |
| Docs and public review record | Lead | yes | completed | PASS | `docs/`, `README.md`, `docs/source-audit-2026-09-15.md` |
| Open PR against main | Lead | yes | completed | PASS | https://github.com/byensitmagnus/agent-mission-control/pull/6 |
| Three-arm comparison | Lead | no | superseded | NOT VERIFIED | superseded: homemade farm closed; nine runs kept as a record only |

## Decisions and evidence

Engineering integrity is separate from agent quality. The 16 common AMC runtime
files are byte-identical in skill and plugin packages; ZIP archives are not.
Nine Codex runs remain in `evals/candidate.9/comparison/results/` as a closed
record. They are not a research program to extend. Further kernel changes cite
host docs, published research, other public repos or known practitioner
guidance. Historical `c9-01` remains a failed hidden False pair.

## Blockers

None.

## Next action

Do not add subject-run batches. Do not merge or release. Source audit is in
`docs/source-audit-2026-09-15.md`.

## Last verified

Commit/snapshot: PR #6 `codex/unified-amc-kernel` on base `c49dc1be2e334091f6c841047ff2ad778b7bde84`. UTC timestamp: 2026-09-15T07:20:00Z.
