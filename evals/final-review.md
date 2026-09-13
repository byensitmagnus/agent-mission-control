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
