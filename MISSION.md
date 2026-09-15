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
| Same-lead engineering notes | PASS | `docs/reviews/`; not independent public review |
| Homemade subject-farm closed | PASS | [postmortem](evals/candidate.9/README.md); raw JSONL removed |
| Field-state evidence model | PASS | [field-state.md](docs/field-state.md) grades A–E |
| Behavioral superiority vs direct work | NOT VERIFIED | nine Codex runs: no unique win; contaminated Superpowers plugin |

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
| Docs, field state and postmortem | Lead | yes | completed | PASS | `docs/`, `README.md`, `evals/candidate.9/README.md` |
| Open PR against main | Lead | yes | completed | PASS | https://github.com/byensitmagnus/agent-mission-control/pull/6 |
| Three-arm comparison | Lead | no | superseded | NOT VERIFIED | superseded: farm closed; conclusion in postmortem |

## Decisions and evidence

Engineering integrity is separate from agent quality. The 16 common AMC runtime
files are byte-identical in skill and plugin packages; ZIP archives are not.
The nine Codex runs are summarized in `evals/candidate.9/README.md`. Raw
transcripts were removed; the negative conclusion is kept. Kernel changes cite
graded sources in `docs/field-state.md`. Historical `c9-01` remains a failed
hidden False pair. Direct-first is a cautious sequential default, not a natural
law. Skills and MCP are complementary.

## Blockers

None.

## Next action

Do not add subject-run batches. Do not merge or release.

## Last verified

Commit/snapshot: PR #6 `codex/unified-amc-kernel` on base `c49dc1be2e334091f6c841047ff2ad778b7bde84`. UTC timestamp: 2026-09-15T07:39:35Z.
