# Risk and independent proof

Load for material correctness uncertainty, migrations or risky releases. Define the
affected surfaces, correctness gates, authorized consequences and recovery
plan before changing them.

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
reviewer agreement is not runtime evidence. The lead inspects those artifacts
and runs the relevant checks itself. Read-only verifiers can use disposable
write scopes for test outputs when authorized; inability to execute a required
check remains NOT VERIFIED, never an inferred PASS.

Return material findings to the responsible owner with the failing reproduction.
Repair, rerun affected checks and refresh affected review on the repaired artifact. Keep unrelated
current passing evidence. If a required reviewer, runtime, external state or
recovery test is unavailable, name that gate and the concrete missing input.
Finish all safe preparation, then stop at the exact unauthorized consequence.
