schema_version: 1
overall: NOT VERIFIED

# Host observations

## Goal / Definition of Done

Copy-path matches installer. Scoped host observations only where a native
command actually ran. Behavioral superiority remains NOT VERIFIED.
Branch push is authorized for machine handoff; merge, tag and release are not.

## Base and candidate

Current artifact: branch `codex/product-contract-v1` (candidate.10). Commit attestation provided externally by GitHub Actions `GITHUB_SHA`; package runtime identity by `BUILD_RECORD.json`.
Base commit: `df184ad03da0f333f9525a7706f7aa664e09de47` (main PR #6 merge).
Package identity: `0.2.0-candidate.10` (not a release).

## Route

Planned route: direct
Observed route: direct
Deviation: none
Observed agents/threads: none
Observed isolation: none

## Hard gates

| Gate | Status | Evidence |
|---|---|---|
| Copy-path lists checker scripts | PASS | `docs/getting-started.md`; `scripts/test_amc_check.py` 19/19 |
| Cursor bundled checker from installed folder | PASS | scoped 2026-09-19 observation: Cursor 3.21.13; checker PASS, behavioral NOT VERIFIED |
| Grok project skill discovery | PASS | scoped 2026-09-19 observation: Grok 1.0.3 `inspect --json`; `source.type=project`; exact SKILL.md path |
| Orca host profile mapping | PASS | `references/hosts/orca.md`; `scripts/test_orca_mapping.py` 10/10 |
| Cursor / Codex / Claude / Kimi skill_discovery | NOT VERIFIED | no native loader listing in this slice |
| Behavioral superiority vs direct work | NOT VERIFIED | no production outcome study |

## Authority

Authorized: local engineering and docs on `codex/product-contract-v1`, plus
publishing this branch to GitHub for machine handoff.
Forbidden: merge, GitHub release, global install, host-config change, daemons,
new services, new AMC subject-run batches and GitHub settings changes.

## Jobs

| Job | Role | Agent | Required | Lifecycle | Verdict | Owned scope |
|---|---|---|---|---|---|---|
| Copy-path + host observations | lead | Lead | yes | completed | NOT VERIFIED | getting-started, hosts.md |
| Farm comparison | worker | Lead | no | superseded | NOT VERIFIED | superseded: farm closed; conclusion in postmortem |

## Decisions and evidence

Grok inspect is discovery, not a completed task. Cursor checker execution is
Python from an installer-placed folder, not skill-picker discovery. Codex,
Claude Code and Kimi have no equivalent no-model inspect used here.
Orca host profile v0 designed in `references/hosts/orca.md` with capability schema
in `templates/host-capability-schema.json`, mapping fixture in `templates/fixtures/orca-mapping.json`,
and deterministic tests in `scripts/test_orca_mapping.py`. Single workflow owner preserved:
AMC owns route, authority and acceptance; Orca supplies execution and observation.
Behavioral superiority remains NOT VERIFIED.
Commit attestation is external via GitHub Actions GITHUB_SHA; runtime identity is generated BUILD_RECORD.json.

## Blockers

None that block remaining local docs. Native discovery on Codex/Claude/Kimi
needs those clients' own listing path without a model run.

## Next action

Continue on `codex/product-contract-v1` from GitHub. Leave other host cells
NOT VERIFIED until similarly scoped. Do not merge, tag or release.

## Last verified

Date: 2026-09-20.
Candidate commit attestation is provided externally by GitHub Actions `GITHUB_SHA`.
Package runtime content identity is verified authoritatively via `BUILD_RECORD.json`.
Forbidden actions: merge, tag, release, GitHub settings change, global install.
