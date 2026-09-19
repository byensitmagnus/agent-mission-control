schema_version: 1
overall: NOT VERIFIED

# Product contract v1

## Goal / Definition of Done

Portable skill with a bundled optional checker, role-safe receipts, one
canonical claim file, and honest package identity. Behavioral superiority
remains NOT VERIFIED. No push, merge, tag or release.

## Base and candidate

Current artifact: dirty working tree on `codex/product-contract-v1` over
`3cc23250383f4178d1f4d3e55ee5acbc4ec98771`. Candidate commit SHA is not stored
in this file.
Previous published ZIP: `v0.2.0-candidate.8`.
Package identity for this slice: `0.2.0-candidate.10` (not a release).

## Route

Planned route: direct
Observed route: direct
Deviation: none
Observed agents/threads: none
Observed isolation: none

## Hard gates

| Gate | Status | Evidence |
|---|---|---|
| False overall PASS rejected | PASS | `scripts/test_validate.py` |
| Bundled checker ships | NOT VERIFIED | `scripts/amc-check.py` until package tests run |
| Claims SkillOpt vs harmful-skills split | NOT VERIFIED | `research/claims.json` until renderer check runs |
| Superpowers local vs upstream distinct | NOT VERIFIED | v6.1.1 vs v6.4.1 in `research/claims.json` |
| Behavioral superiority vs direct work | NOT VERIFIED | no production outcome study |

## Authority

Authorized: local engineering and docs on `codex/product-contract-v1`.
Forbidden: push, merge, GitHub release, global install, host-config change, daemons,
new services, new AMC subject-run batches and GitHub settings changes.

## Jobs

| Job | Role | Agent | Required | Lifecycle | Verdict | Owned scope |
|---|---|---|---|---|---|---|
| Product contract v1 | lead | Lead | yes | running | NOT VERIFIED | `scripts/amc_guard.py`, packaging, claims, docs |
| Farm comparison | worker | Lead | no | superseded | NOT VERIFIED | superseded: farm closed; conclusion in postmortem |

## Decisions and evidence

Engineering integrity is separate from agent quality. Canonical checker:
`scripts/amc_guard.py`. Installed CLI: `scripts/amc-check.py`. Claims:
`research/claims.json`. Markdown ledgers are generated views.

## Blockers

None.

## Next action

Finish local tests. Do not push, merge or cut a GitHub release.

## Last verified

Commit/snapshot: parent `3cc23250383f4178d1f4d3e55ee5acbc4ec98771`. UTC timestamp: 2026-09-19T10:00:00Z.
This file does not pin the candidate commit SHA.
External actions not performed: push, merge, tag, release.
