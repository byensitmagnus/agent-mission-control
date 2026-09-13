# Risk and independent proof

Load for material correctness uncertainty, migrations or risky releases. Define the
affected surfaces, correctness gates, authorized consequences and recovery
plan before changing them.

## Execution preflight

Before a costly suite, inspect the existing build/test entrypoint and its nested
checks. Choose one route that supplies the required evidence without running the
same suite immediately before an entrypoint that already runs it. Preserve
explicit repeatability requirements; reuse proof only when source, relevant
environment and acceptance coverage still match.

Check known prerequisites cheaply in the same execution environment as the suite:
the pinned toolchain, working directory and any previously failing browser or
permission prerequisite. Stop dependent execution when preflight fails. Do not
assume environment changes survive separate shell calls, and do not bypass a
toolchain pin to report a required check as passing.

Classify failures before repair: product behavior, test expectation, environment,
or missing evidence. Repair the responsible layer, rerun the affected check, then
refresh required broader proof when justified. An environment failure before test
execution is not an app defect or a PASS. Another expensive run needs a changed
prerequisite, relevant repair, new hypothesis or explicit repeatability purpose.

For release work, distinguish the requested channel's working user journeys and
recovery requirements from broader product coverage and optional improvements.
Trace blocking criteria to current authority; a maturity counter is not a bug
count. Do not promise zero bugs, silently lower requirements or invent stricter
ones. Code checks cannot substitute for required packaged-app behavior or a live
error-reporting receipt. Complete executable work before naming external blockers.

## Review and preservation

A repair to acceptance logic is material review work even if the diff is small:
release gates, evidence aggregators and other rules that authorize acceptance.
After focused implementation checks pass, assign a fresh reviewer who did not
author the repair. Give the reviewer the requirement, changed rule, test oracle
and raw results; ask whether incomplete or contradictory evidence can still pass.
Keep this review as an unresolved job in the existing mission. The lead handles
findings, repair and affected verification before accepting the result. Passing
the author's tests does not replace this review. If independence is unavailable,
name the missing review and finish other authorized work. Ordinary text edits
and test maintenance that do not change acceptance meaning need no extra role.

Capture the actual baseline data and relevant rendered or executable behavior.
For migrations, use disposable copies first. Compare IDs, counts and complete
values, including false, zero, unknown keys and supported settings. Verify
rollback restores the original bytes or an explicitly equivalent recoverable
state. A deliberately corrupted output must fail the preservation check.

Keep valid existing data and rendering accessible until migration is complete.
Changes to product data, images, prices, CTAs or purchase flows require scope
that covers them. Verify each affected surface against its own baseline; do
not let a passing build stand in for data or visual parity.

Obtain fresh independent review for material work whose acceptance or risk needs
it. Give the reviewer requirements, current diff/artifacts, relevant callers,
executed evidence and specific risks, without the implementer's argument for PASS.
Ask it to falsify completion and return reproducible findings. Start with the
least costly capable reviewer; escalate unresolved high-value uncertainty using
[capability routing](packets.md). A trivial edit needs no review team. Reuse review
when it covers the gates and current candidate; collect only missing proof.
A verifier executes the required checks against the identified candidate;
reviewer agreement is not runtime evidence. Fresh history reduces inherited
argumentation; it does not guarantee independent errors or reviewer competence.
Require a relevant source, reproducible counterexample or executed check for a
material claim; treat an unconfirmed finding as uncertainty rather than a defect. The lead inspects those artifacts
and runs the relevant checks itself. Read-only verifiers can use disposable
write scopes for test outputs when authorized; inability to execute a required
check remains NOT VERIFIED, never an inferred PASS.

Return material findings to the responsible owner with the failing reproduction.
Repair, rerun affected checks and refresh affected review on the repaired artifact. Keep unrelated
current passing evidence. If a required reviewer, runtime, external state or
recovery test is unavailable, name that gate and the concrete missing input.
Finish all safe preparation, then stop at the exact unauthorized consequence.
