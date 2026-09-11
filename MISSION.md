schema_version: 1
overall: NOT VERIFIED

# v0.2 local candidate mission

## Goal / Definition of Done

Produce one local v0.2 candidate from the actual baseline, with portable core,
optional documented Codex profile, durable context/evidence/state contracts,
nine fixed evalcases, structural tooling, accurate public docs and independent
review. The frozen contract is [the candidate log](evals/v0.2-candidate-log.md).

## Base and candidate

Base and candidate-1 parent: `fdbf07fa3443ca454509ca36ace6e2651b9fc2e6`.
Branch: `feat/local-v0.2-candidate`. Candidate 1 is the current working tree;
candidate 2 has not been started. Snapshot is recorded in final proof artifacts.

## Hard gates

| Gate | Status | Evidence |
|---|---|---|
| Baseline identity/public/CI | PASS | Root public API GETs, 2026-09-11T18:59:03Z; public, one successful workflow |
| Portable core and durable contracts | PASS | Fresh independent review, evals/final-review.md |
| Safe profile/plugin package | PASS | Root four package tests and official plugin validation |
| Structural and negative controls | PASS | Root 24 negative controls plus valid states on Python 3.11/3.14 |
| Nine-case behavioral comparison | NOT VERIFIED | Isolated agent sessions unavailable; see evals/README.md |
| Independent final review | PASS | evals/final-review.md, no material residual findings |
| Delivery provenance | NOT VERIFIED | Enclosing Git commit and external delivery report record final clean-tree proof |

## Authority

Authorized: one local feature branch, repository edits, bounded subagents,
safe local tests/disposable fixtures, repairs and one local candidate commit.
Forbidden: push, merge, release, GitHub settings/security changes, credentials,
external or destructive actions. Disposable fixture history has no remote and
is separate from the one candidate commit. No user configuration is installed.

## Jobs

| Job | Agent | Status | Owned scope |
|---|---|---|---|
| Orchestration audit | audit_orchestration / Sol | completed | Read-only core |
| Codex compatibility audit | audit_codex / Sol | completed | Official public sources |
| Public repo audit | audit_public / Luna | completed | Read-only public GitHub and docs |
| Validation tooling | audit_orchestration / Sol | completed | Validator, negative tests, workflow |
| Profile and packaging | audit_codex / Sol | completed | Codex example, UI metadata/icons, packager/tests |
| Public docs | audit_public / Luna | completed | README, SECURITY, CONTRIBUTING, release example |
| Integration and proof | Root / Astra | completed | Core, references, templates, evals, final integration |

Three audit packets expected and received. Three implementation packets expected
and received; root verification and fresh independent final review are complete. No worker owns active
writes now. Root has reclaimed completed scopes for integration fixes.

## Decisions and evidence

- Keep canonical skill at repository root; plugin builder copies it into the
  documented `skills/agent-mission-control/` layout. Plugin installation does not
  install `.codex/config.toml` or `.codex/agents/`; official docs do not promise it.
- Four distinct optional roles: research, implementation, review, runtime
  verification; concurrency three excludes root. No daemon or extra dependency.
- Private vulnerability reporting is disabled (`enabled: false`, public API);
  security docs use a contact-only public issue until maintainer enables it.
- Root review found a destructive error-cleanup race in the first packager;
  repair atomically claims the destination and never deletes on failure.
- The user permits an honest NOT VERIFIED behavioral result if clean isolated
  agent runs are unavailable. Structural proof is separately reported.

## Blockers

Controlled behavioral comparison: Windows sandbox initialization fails with
`apply deny-read ACLs`; native workers share filesystem/config context, and
separate authenticated CLI sessions would require prohibited credential use.
No technical blocker prevents remaining package verification and local commit.

## Next action

Retain this local candidate. The next unpassed functional gate is controlled
behavioral evaluation in a working isolated agent environment. No further local
implementation step remains; delivery provenance is read from the enclosing Git
commit and final report, never inferred from an embedded commit hash.

## Last verified

Baseline commit: `fdbf07fa3443ca454509ca36ace6e2651b9fc2e6`.
UTC: `2026-09-11T18:59:03Z` for public baseline checks. The candidate working-tree
snapshot and record timestamps are in evals/results/2026-09-11.json; the final
delivery report names the exact committed source and its verification time.
