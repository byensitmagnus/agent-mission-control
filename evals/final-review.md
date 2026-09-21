# Fresh-context AI review: candidate e4d32b0 (AMC Product Contract v1.1 Hardening)

Reviewed candidate: `e4d32b021832a48ebcb86f9625a832c120f2eef7`  
Review date: 2026-09-20  
Reviewer identity: Fresh-context AI review (Security & Contract Reviewer)  
Category: Fresh-context AI review (internal verification artifact; not external human audit)  
Review and CI status:
- Fresh-context AI review covered `e4d32b021832a48ebcb86f9625a832c120f2eef7`.
- `5e509164b17ec668a552606c9cae24a1060f1a11` added the review artifact.
- Final-tip CI passed on `5e509164b17ec668a552606c9cae24a1060f1a11`.
- No GitHub review approval or independent human review exists yet.
- GitHub Actions pinning: `actions/checkout` and `actions/setup-python` are pinned by immutable commit SHA. `actions/setup-dotnet@v4` temporarily retains a mutable major tag; not all Actions are immutable-pinned while `setup-dotnet` remains `@v4`.
Supplied context: PR #7 branch diff against `df184ad`, AMC Product Contract v1.1 mandate, 30 adversarial attack vectors, and clean-slate fail-open audit.

## Verdict

Engineering: PASS for candidate `e4d32b021832a48ebcb86f9625a832c120f2eef7`  
Behavioral: NOT VERIFIED  
Release: NO-GO  
Merge: NOT AUTHORIZED  

## Context and Findings Disposition

1. **Schema-first and Status Model Separation (Mandate 1 & 2)**
   - *Finding*: Empty `{}` contract or missing `schema_version` could be accepted or return ambiguous `PASS`. Python truthiness allowed `"false"` strings to evaluate as True.
   - *Disposition*: Implemented strict validation order (parse -> require `schema_version: 1` -> strict type schema -> normalization -> semantics -> artifact/evidence -> outcome). Replaced ambiguous `status: PASS` with `contract_validity: VALID | INVALID`, `mission_outcome: PASS | FAIL | BLOCKED | NOT VERIFIED`, `behavioral_status: NOT VERIFIED`. Empty `{}` returns `INVALID`.

2. **Instruction-Only Bypass Neutralization (Mandate 3)**
   - *Finding*: `--instruction-only` returned `status: PASS` and `contract_required: false` as fact without task evidence. Missing CLI argument for `--mission-view` caused `IndexError`.
   - *Disposition*: `--instruction-only` without contract returns neutral `check_status: SKIPPED`, `decision_source: caller_asserted`, `enforcement_scope: instruction_only`, `mission_outcome: NOT VERIFIED`, with exit code 0. CLI arguments consume their parameter or exit with code 2 on missing values.

3. **Artifact Identity & Mission PASS Hardening (Mandate 4)**
   - *Finding*: Artifact digests allowed short 1-char strings; dirty trees used clean hashes; SHA-1 / SHA-256 formats were not enforced.
   - *Disposition*: SHA-1 enforced to 40 hex characters; SHA-256 enforced to 64 hex characters. Identity method and algorithm must match (`git-commit` with `sha1`/`sha256`, `dirty-manifest` with `sha256`). Dirty source identity canonically binds `base_commit`, `diff_digest` (`git diff --binary --full-index`), status/mode/renames, and recursive untracked manifest with per-file SHA-256 digests. `PASS` without artifact or with `none` is strictly rejected.

4. **Role & Route Semantics (Mandate 5)**
   - *Finding*: `simple_sequential` rejected legitimate lead-only jobs. Scope overlap rejected legitimate sequential transfers. Delegation break-even only applied to writers.
   - *Disposition*: `simple_sequential` only rejects delegated jobs. Overlap rejected only when concurrent; sequential handoff allowed with dependency ordering and explicit handoff. All delegated routes require typed `delegation_decision`. Reviewers/verifiers strictly enforced read-only.

5. **Host Observation Claims Separation (Mandate 6)**
   - *Finding*: Self-authored JSON receipts could claim host observation without external attestation.
   - *Disposition*: Separated `receipt_shape_valid`, `host_observation_claimed`, and `externally_attested`. Structured isolation receipt required.

6. **Orca Host Profile Scope Correction (Mandate 7)**
   - *Finding*: `AMC-ORCA-002` claimed `bundled_checker_enforced`, but only tested fixture text consistency without live production enforcement.
   - *Disposition*: Claim reclassified to `repository_ci_enforced` as source-backed design. Fixture renamed from `amc_contract` to `design_mapping`. Orca source pinned by full immutable commit SHA `ae1277cf5a5a22174c5cd92e55ba63a001539491`.

7. **Claim Integrity and Extended Validation (Mandate 8)**
   - *Finding*: `AMC-COST-001` cited harmful-skills paper for a local repository observation. Audit dates and source back-references were inconsistent.
   - *Disposition*: Corrected `AMC-COST-001` source to `AMC-REPO-AUDIT`. Updated all audit dates to 2026-09-20. Extended `render_claims.py` with strict enum checks, bidirectional source `supports` validation, and path existence validation.

8. **Removal of Stale Tracked Runtime Status (Mandate 9)**
   - *Finding*: `docs/status.json` and `MISSION.md` contained volatile state (dirty branch, actions not performed, stale test counts).
   - *Disposition*: Stripped transient runtime state from static repo files. External attestation anchored to GitHub Actions CI and `BUILD_RECORD.json`.

9. **Authoritative BUILD_RECORD Verification (Mandate 10)**
   - *Finding*: Installer ignored `BUILD_RECORD.json` during `--check`.
   - *Disposition*: Installer recomputes runtime content digest, parses and validates `BUILD_RECORD.json`, and reports `BUILD_RECORD_INVALID` (TAMPERED, STALE, MISSING) on mismatch.

10. **CI Hardening & Windows Job (Mandate 11)**
    - *Finding*: Actions were unpinned or used mutable tags; no Windows CI existed.
    - *Disposition*: Added Windows CI job in `.github/workflows/validate.yml` covering packaging, skill installation, checker execution, and path handling. Pinned GitHub Actions by immutable commit SHA (`actions/checkout@11bd7190`, `actions/setup-python@42375524`, `actions/setup-dotnet@v4` documented). Handled Windows 8.3 short paths via `os.path.samefile`.

11. **Comprehensive 30 Adversarial Cases (Section 13)**
    - *Finding*: Need systematic adversarial test coverage proving fail-closed rejection.
    - *Disposition*: Created `scripts/test_adversarial_guard.py` implementing all 30 adversarial cases. All 30 cases pass.

# Adaptive candidate 2: independent review

The historical review below belongs to `358680d`; its old test counts and
behavioral limitations are not results for the current candidate.

Current reviewer: separate read-only Luna agent with fresh product context
(no implementation-worker conversations), following its earlier source-only
research. It inspected actual files/diff, ran the structural validator, 25
negative controls, packaging tests and fixture tests, and exercised hostile Git
environment, archive/source parity, source links and the official plugin
validator. Final code/eval reinspection completed on both Python versions;
no material runtime, packaging or evaluator defect remained. Its status-record
findings are resolved in the current Mission View and this review record.

Verdict: PASS for the independent local artifact review. The reviewer
confirmed the final status-record corrections; no material findings remain.
Behavioral acceptance remains NOT VERIFIED.

Findings repaired by the lead/workers:
- Eval README case count and command IDs were stale; updated to eleven/v2.
- Historical review and current review were not distinguished; marked here.
- Result template used an obsolete case ID; updated for schema v2.
- Final archive proof exposed host-dependent text line endings; tracked text
  now uses LF and opposite autocrlf archive builds preserve every file byte.

Root independently found and repaired inherited Git environment/provenance
ambiguity in the builder and linked-ancestor gaps in fixture preparation.
Both changes have executable negative controls. Full current proof is recorded
in [the candidate log](v0.2-candidate-log.md).

# Historical review: candidate 1 / rubric v1 — 2026-09-11

Reviewer: fresh read-only Sol agent, reasoning high, with requirements and
current artifacts but no worker conversations or proposed acceptance verdict.
Root retained authority and reran relevant commands itself.

## Verdict

PASS for the local/static review gate. No unresolved material findings after
repair and independent reinspection. This is not behavioral acceptance.

## Reproduced findings and repairs

- Direct-task instructions conflicted with unconditional independent review.
  Simple edits and understood dependency chains now return after root's
  proportionate check, before the mission-only workflow.
- Mission View accepted overall PASS with unverified gates, incomplete sections
  and malformed status/header values. Packet validation accepted an empty field
  by consuming the next line. Current checks reject these mutations and accept
  documented queued/completed/PASS/BLOCKED examples.
- A missing verifier role, conflicting fixture paths and external SVG style
  imports were accepted. Exact role set, shared fixture path preflight and a
  documented restricted SVG subset now reject them.
- Git fixture creation inherited user configuration/attributes. A disposable
  clean filter ran and changed committed bytes. Every Git subprocess now uses
  a scrubbed Git environment with global/system config and attributes disabled.
  The fresh hostile-config probe observed sentinel=false, decoy=false and
  committed bytes identical to workspace bytes, without filter output.
- Root also repaired packager cleanup ownership, missing output parents and
  self-copy destinations; existing output is refused without deletion, linked
  inputs are rejected and post-creation failures leave inspectable partial output.

## Evidence

Independent review and root execution both observed:

- `python scripts/validate.py`: PASS.
- `python scripts/test_validate.py`: valid-state positives and 24 reason-checked
  negative controls PASS.
- `python scripts/test_prepare_eval.py`: nine paired disposable preparations,
  identical prompts/fixtures, path/refusal/Git-contamination controls PASS.
- `python scripts/test_package_plugin.py`: four tests PASS.
- Generated plugin accepted by the installed official OpenAI plugin validator.
- `git diff --check`: PASS; Windows line-ending conversion warnings only.
- Public GitHub vulnerability-reporting endpoint returned enabled=false.

Root runs use Python 3.11.9 and 3.14.3, Git 2.47.0.windows.2. The installed
skill-creator quick validator also passes on Python 3.11 with its existing
PyYAML dependency; repository checks require only the standard library.

## Limits

Zero controlled subject-agent runs were completed. The nine-case behavioral
comparison and host installation/discovery remain NOT VERIFIED. Model cost,
tokens and comparative runtime are NOT MEASURED. Updated hosted CI has not run
because this candidate must remain local. Review made no repository edits or
external mutations; these notes are root's concise evidence record.
