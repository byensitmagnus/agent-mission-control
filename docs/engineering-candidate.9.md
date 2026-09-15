# Candidate.9: installation-independent engineering evidence

Local engineering from GitHub `main`
`c49dc1be2e334091f6c841047ff2ad778b7bde84` (`v0.2.0-candidate.8`).
Branch `codex/unified-amc-kernel`. Open PR
https://github.com/byensitmagnus/agent-mission-control/pull/6
Candidate.9 is PR source, not merged, not released, not installed.

AMC remains one skill/plugin. Companion projects are design sources only.
`evals/decision_kernel.py` is a regression test. It does not launch agents.

## Concrete changes

| Before | Candidate.9 | Check |
|---|---|---|
| `overall: PASS` with required jobs still queued | Required jobs must be completed PASS | `python scripts/test_validate.py` |
| Dummy required PASS + optional queued real work | Overall PASS forbids queued and running jobs | `pass_optional_queued` / `pass_optional_running` |
| Plugin defaultPrompt pushed coordinated agents | One AMC workflow; smallest useful execution graph; verified evidence | `python scripts/test_package_plugin.py` |
| Templates shipped transport.py fiction | Blank templates; demonstrations under `examples/packets/` | `python scripts/validate.py` |
| `MISSION.md` mixed years of PASS history | Compact live mission; history in `docs/history/through-candidate.8.md` | live `MISSION.md` |
| Live mission could keep template placeholders | Instance records reject unresolved placeholders | `live_placeholders` |
| Reviewer id not openable on GitHub | Public review notes and source audit | `docs/reviews/candidate.9-falsification.md`; `docs/reviews/candidate.9-working-tree.md`; `docs/source-audit-2026-09-15.md` |
| Codex example required named models, four roles, 3 threads | Format, sandbox limits, threads 1..32 | other-model positive control |

The 16 common AMC runtime files are byte-identical in the skill and plugin
packages. The ZIP archives have different structure and SHA256 hashes.

## Limits

CI and local checks prove engineering integrity, not better agent behavior.
The [nine Codex runs](../evals/candidate.9/comparison/results/README.md) are a
closed record. Do not extend that protocol. Historical `c9-01` on `84a0fcb`
remains development evidence: both arms failed a hidden False hyphen that the
visible prompt did not state. Do not treat that pair as product proof.
Further kernel changes cite host docs, published research, other public
repositories or known practitioner guidance. The
[source audit](source-audit-2026-09-15.md) records that check.

The validator tests Markdown contract consistency. It cannot prove that
natural-language evidence is true or that the named artifact equals git HEAD.
A dummy required PASS job can still exist if unfinished work is omitted from
the Jobs table or superseded with a reason.

Historical qualification FAIL and the Sol 18/18 pair are unchanged.
`evals/v3` still has no completed subject results on this PR.

Nine Codex comparison runs are bound in
[comparison results](../evals/candidate.9/comparison/results/README.md).
Candidate.9 had no holdout correctness regression and no unique win. The audit
notify-429 hidden check was not named in the visible prompt; it is development
data, not product proof. The method is closed: no new subject-run batches.
