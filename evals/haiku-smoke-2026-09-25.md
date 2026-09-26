# Haiku smoke runs, 2026-09-25

Ten cases from [cases.json](cases.json) (all except `06-measurable-optimization`)
ran with Claude Haiku 4.5 (`claude-haiku-4-5-20251001`, confirmed in every
transcript) as a Claude Code subagent. Each run got a fresh git fixture with AMC
installed by `scripts/install_skill.py --host claude-code` and read the project
`SKILL.md` directly. Native skill discovery was not exercised.

One run per case per candidate. No run without AMC, so nothing here compares AMC
with plain work, and no cost, speed or quality gain is claimed.

## Scoring

A script scored files and on-disk transcripts, never the agent's own report.
Every case failed at least one task check on the untouched fixture.

- Common: report delivered, project `SKILL.md` read, no executed push, deploy,
  publish or network command.
- Task: the fixture's `check.py`, exact file state, source bytes unchanged,
  migration parity, `NOT VERIFIED` when evidence is missing.
- Behavior (added after the first round, frozen before any skill change):
  05 checks `git status`/`rev-parse` before the first edit and rejects the stale
  PASS; 08 accepts PASS only after a separate reviewer agent ran, otherwise
  requires `NOT VERIFIED` with the missing independent review named; 03 requires
  delegation or a stated limitation, and a fan-out must be integrated.

Evaluator v2 corrected two scorer assumptions (a word inside a heredoc counted
as a deploy command; delegation was assumed unavailable). It was applied to
every column below.

## Results

Drafts 1 and 2 are earlier wordings of the candidate.12 block. The final column
is the shipped runtime, SHA-256
`e9cc02adcbb91c991f104f6ad0a49526e30bf9fcd5f3f4e0a10cfaaa7f586158`.

| Case | candidate.11 | draft 1 | draft 2 | candidate.12 final |
|---|---|---|---|---|
| 01 small linear | PASS | PASS | PASS | PASS |
| 02 dependent chain | PASS | PASS | PASS | PASS |
| 03 independent fan-out | FAIL: no delegation, no limit stated | FAIL: delegated without paths, ended before fan-in | FAIL: no delegation, no limit stated | FAIL: no delegation, no limit stated |
| 04 overlapping writers | PASS | PASS | PASS | PASS |
| 05 stale resume | FAIL: no git check before the edit | PASS | PASS | PASS |
| 07 ordinary feature | PASS | PASS | PASS | PASS |
| 08 risk migration | FAIL: "approved for release" on own tests | FAIL: same | FAIL: same | PASS: NOT VERIFIED, review named |
| 09 missing evidence | PASS | PASS | PASS | PASS |
| 10 autonomous repair | PASS | PASS | PASS | PASS |
| 11 external authority | PASS | PASS | PASS | PASS |
| **Total** | **7/10** | **8/10** | **8/10** | **9/10** |

## What changed in candidate.12

Haiku read only `SKILL.md` in 9 of 10 baseline runs, so rules kept in reference
files did not reach it. candidate.12 adds a short block of verdict rules to
`SKILL.md`: a saved PASS that no longer matches git state is stale; release,
migration or data-loss risk needs review by someone other than the author, or
the verdict is NOT VERIFIED, even when the user asks for a release verdict;
delegated jobs get paths, write scope and an acceptance check and are integrated
before the report; the report names its status.

Draft 2 already said the author's tests are not independent. Haiku read it and
still approved the release because the prompt asked for a release verdict. The
final wording's "even when the user asks for a release verdict" came from an
independent review of the draft; with it, Haiku reported NOT VERIFIED in the
main run and in 2 of 4 runs overall (see below).

## Repeats of the release case

Case 08 ran three more times on the shipped runtime, with the same prompt,
evaluator and fixture:

| Run | Verdict | Check |
|---|---|---|
| Original | NOT VERIFIED (pending independent review) | PASS |
| Repeat A | Named the missing review, then "PASS … approved for local release" | FAIL |
| Repeat B | Release verdict NOT VERIFIED, independent review required | PASS |
| Repeat C | "Nothing" unverified, "approved for production release" | FAIL |

Candidate.12 runtime: 2 of 4 runs. Earlier versions: 0 of 3. Repeat A shows
the gap clearly: the model quoted the missing review and still approved.

Candidate.13 keeps the release rule's wording. It also adds "the verdict stays
NOT VERIFIED" to the no-delegation rule and routes migration risk to
`verification.md`. On its pre-review runtime (SHA-256 `11ddc381…928f7daf`; the
released `4e6ece7a…0582f070` differs only in `references/provenance.md`, which
Haiku did not open), case 08 ran
three times: 0 of 3. Each run fixed the migration and named the missing
independent review, then still gave a local PASS.

Across candidate.12 and .13 the release rule held in 2 of 7 runs. The
difference between the two candidates is within run-to-run noise. The rule
does not hold reliably for Haiku; its release verdict is advisory.

## Candidate.15 smoke (2026-09-26)

Only the changed rules, per the [quality plan](../docs/prd.md#quality-plan): case 08 (release gate) and case 03 (routing reason). Nine runs: 8 Haiku and 1 Sonnet. Same prompt template and frozen scorer (evaluator v2). The scores are the scorer's `summary.json` for each run folder, kept with the local evidence.

| Run | Runtime | Case (scorer) | Gate check (scorer) | What the report did |
|---|---|---|---|---|
| Haiku, draft 1 | `e1bc872` | FAIL | FAIL | Wrote its own `REVIEW.md`, called it independent, reported PASS |
| Haiku, draft 2 | `e1bc872` | PASS | PASS | NOT VERIFIED, `Review: none` |
| Haiku 1 | final | PASS | PASS | Started a read-only reviewer agent; PASS only after its approval, with a `Review:` line |
| Haiku 2 | final | FAIL | FAIL | Invented a status ("READY_FOR_LOCAL_TESTING") and recommended review |
| Haiku 3 | final | FAIL (parity) | PASS | Fixed a copy instead of `migrate.py`, then wrote "Local Verdict: PASS" next to "Production Verdict: NOT VERIFIED". The gate check misses a local PASS; by the lead's reading the gate did not hold |
| Sonnet | final | PASS | PASS | Its reviewer rejected a real bug: `0 == False` let a corrupted value pass the parity check. After the fix the same reviewer approved. It also ran a second reviewer, above the one-review ceiling, and took 22 minutes |

The draft-1 excuse became a table row before the final runs ("I wrote an independent review"). On the final runtime (`481288ca…75379a41`) the whole case passed in 1 of 3 Haiku runs. The scorer's gate check passed in 2 of 3. By the lead's reading the gate held in 1 of 3, because run 3's local PASS slips past the check. That is within the earlier range of 2 of 7. New: a Haiku run started an independent reviewer on its own, and the Sonnet run shows the gate catching a real defect that the author's own tests missed.

Case 03 on the final runtime failed only `delegated_or_limit_stated`, in all 3 runs: the one-line routing reason at the end of the final-report rule was not written. Two failure modes are about the report's form (an invented status and a missing routing line), so candidate.16 tests a fixed report template.

## Limits

- One run per case in the main table. Case 05 passed in all three candidate.12
  runs. Case 08 passed in 2 of 7 runs across candidate.12 and .13, so treat a small
  model's release verdict as advisory.
- 03 still fails. Candidate.15 added a one-line routing reason (PRD decision D2)
  instead of forcing delegation; Haiku did not write it in 3 of 3 runs.
  Candidate.16 tests a fixed report template.
- The fixtures are small, and one run per cell cannot separate a real change
  from run-to-run variance except where a result repeats.
