# Risk and independent proof

Load for migrations, data-sensitive changes or risky releases. Define the
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

Obtain fresh independent review of the invariants and relevant callers.
A verifier executes the required checks against the identified candidate;
reviewer agreement is not runtime evidence. The lead inspects those artifacts
and runs the relevant checks itself. Read-only verifiers can use disposable
write scopes for test outputs when authorized; inability to execute a required
check remains NOT VERIFIED, never an inferred PASS.

Repair material findings and refresh affected proof and review. Keep unrelated
current passing evidence. If a required reviewer, runtime, external state or
recovery test is unavailable, name that gate and the concrete missing input.
Finish all safe preparation, then stop at the exact unauthorized consequence.
