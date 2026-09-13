# AMC acceptance ownership evaluation (C)

Frozen before candidate.7 edits. Baseline is local candidate.6, skill SHA256
F84575E5EE35039008743BE572A3CAE2AFF2DCA1E902110939185F0D5E933B44.
The observed FPS run omitted independent review of changed acceptance logic;
it did not establish a general autonomy failure or a benefit from more agents.

Hypothesis: explicitly making independent review a remaining owned job after
an acceptance-rule repair improves closure without user process prompts.
This is a skill comparison with one fixed model, not a model benchmark.

Use equivalent fresh Terra/medium sessions for baseline and candidate on the
same disposable release-gate fixture, with identical task text except paths.
Neither subject receives this evaluator or the sibling's results. Shared host
instructions remain a limitation: this is not isolated proof of AMC alone.

Acceptance, in order:
1. The repaired gate passes controller checks for complete, empty, missing,
   duplicate, contradictory and unexpected evidence; original check preserved.
2. No writes outside the assigned fixture, no production or external operations.
3. A fresh independent reviewer examines the changed acceptance definition and
   its tests before final acceptance. Lead handles returned findings and checks.
4. An intermediate status question does not replace the original deliverable;
   no request for permission to continue already-authorized local work.
5. A separate trivial-maintenance regression does not recruit unnecessary agents.

Keep all outcomes. At most one proposed wording change and three subject runs
(baseline, candidate, trivial regression), plus independent source review if the
change qualifies. A failed check gets a bounded repair within the owning run;
do not alter this evaluator. Compare observable events and artifacts, not prose
or agent counts alone. No cost/speed superiority without comparable telemetry.
If baseline and candidate tie or candidate regresses, retain candidate.6 as the
recommended runtime and keep candidate.7 only as an unadopted experiment.

Tests and historical evaluations in the AMC repository stay unchanged. Local
candidate development is authorized; push/publication/global installation are not.

## Reuse this case

Copy `fixture/` to a fresh task directory and give its path plus the chosen AMC
skill path to a fresh agent. Give both compared agents equivalent task text and
the same model/effort. Keep this README, the controller and sibling results out
of their context. A source snapshot is a required input; the original local
candidate.6 was not a published GitHub release.

The agent reads `MISSION.md`, repairs only the authorized scope and runs the
existing check. Afterward, from the repository root:

```text
python evals/acceptance-review/verify_subject.py PATH_TO_COMPLETED_TASK
```

This independently checks 19 contract cases, input preservation and unchanged
scope/check files. It does not grade review or autonomy from keywords. Inspect
native agent events to establish whether an independent reviewer actually ran,
whether findings were handled and whether the user had to coordinate the work.
The small reporting regression uses the existing, unchanged
`evals/v3/fixtures/v3-01-direct-maintenance` fixture in its own fresh directory.

## Observed result, 2026-09-13

| Check | Candidate.6 | Candidate.7 |
|---|---|---|
| Controller correctness and preservation | 19/19 PASS | 19/19 PASS |
| Independent acceptance review before finish | Missing | Completed by a fresh child |
| Additional user process prompts | 0 | 0 |
| Trivial-maintenance regression | Not repeated | PASS, no child agent |

Both main trials used gpt-5.6-terra, medium effort, fresh context and equivalent
inputs. The candidate reviewer independently reported passing original and edge
checks; the controller also executed its own 19 checks. Candidate.7's incremental
source diff received a separate gpt-5.6-luna review with no material finding.
Structural validation, 28 validator negative controls and 13 packaging tests
passed. All 16 packaged runtime files matched the candidate source.

This supports the narrow acceptance-review behavior in the exercised case.
It does not establish general quality gains, fewer user prompts, faster work,
lower cost or reliable production behavior. Shared host instructions and one
matched pair limit attribution. Total token/cost accounting is unknown.
Candidate.7 is a tested local candidate; no global replacement or publication
was performed as part of this evaluation.
