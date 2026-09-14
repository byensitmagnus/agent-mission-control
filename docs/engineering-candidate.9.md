# Candidate.9: installation-independent engineering evidence

Local engineering on 2026-09-14 from GitHub `main`
`c49dc1be2e334091f6c841047ff2ad778b7bde84` (`v0.2.0-candidate.8`).
Branch `codex/unified-amc-kernel`. No merge, release, installation or
publication. Push and a PR against `main` are the authorized next step.

AMC remains one skill/plugin. Companion projects are design sources only.

## Concrete changes

| Before | Candidate.9 | Check |
|---|---|---|
| `overall: PASS` with required jobs still queued | Required jobs must be completed PASS; unfinished, negative or required-superseded jobs fail | `python scripts/test_validate.py` |
| Plugin defaultPrompt pushed coordinated agents | One AMC workflow; smallest useful execution graph; verified evidence | `python scripts/test_package_plugin.py` |
| Templates shipped transport.py fiction | Blank templates; demonstrations under `examples/packets/` | `python scripts/validate.py` |
| `MISSION.md` mixed years of PASS history | Compact live mission; history in `docs/history/through-candidate.8.md` | live `MISSION.md` |
| Live mission could keep template placeholders | Instance records reject unresolved placeholders; templates may keep them | `scripts/test_validate.py` `live_placeholders` |
| Every substantive run wrote a learning observation | Signal only for reusable success, failure or surprise | `references/learning.md`; `evals/decision_kernel.py --self-check` |
| Codex example required Astra/Sol/Luna/Terra, four roles, 3 threads | Optional profile: valid model refs, sandbox limits, threads 1..32 | `scripts/test_validate.py` other-model positive |

## Limits

CI and local checks prove engineering integrity, not better agent behavior.
The [bounded comparison protocol](../evals/candidate.9/README.md) is frozen.
One Sol/medium pair on `c9-01` (commit `84a0fcb`) passed the public check and
failed the hidden False hyphen on **both** arms. AMC stayed direct and used
more time and input tokens. Cases 2–4 were not run. Comparative benefit remains
NOT VERIFIED.

Independent review first obtained overall PASS through optionalized required
jobs, `None.` plus a blocker, short/date identities, unverified gate evidence
(`no subject runs`, `not yet verified`), missing artifact identity in gate
evidence, and a blocker parked in Next action. Those paths now fail
`scripts/test_validate.py` (54 negative controls). Residual: unfinished work
can still be hidden as optional if a dummy required job is marked PASS. That
is a false record, not a closed semantic proof. The checker tests internal
consistency of the named artifact identity, not that it equals git HEAD.

Historical qualification FAIL and the Sol 18/18 pair are unchanged.
`evals/v3` still has no completed subject results on this SHA.
