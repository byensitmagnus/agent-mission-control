# Candidate.9 historical postmortem

Closed homemade comparison. **Do not extend. Do not launch subject runs.**

Raw JSONL, prompts, stderr, launch files and per-arm result folders were removed
from this tree on 2026-09-15. The numbers below are the recorded conclusion.
They are not product proof that AMC is better, cheaper or faster.

## Nine Codex arms (2026-09-14/15)

Host: Codex CLI 0.153.3, `gpt-5.6-sol`, medium,
`--ignore-user-config --ephemeral --approve-for-me`.

Contamination: every arm loaded the user Superpowers plugin from
`~/.codex/plugins`. Direct did **not** install AMC. This was not a naked
single-agent isolation.

Hidden checkers were not in the workspace. `user_interventions` was recorded as
0 by protocol, not parsed from host events.

| Case | Arm | Hidden | Claimed | False PASS | Time s | Input | Cached | Uncached | Output | Children |
|---|---|---|---|---|---|---|---|---|---|---|
| audit | direct | FAIL | PASS | yes | 85.5 | 225863 | 199296 | 26567 | 1899 | 0 |
| audit | candidate.8 | FAIL | PASS | yes | 81.4 | 129104 | 101120 | 27984 | 1873 | 0 |
| audit | candidate.9 | FAIL | PASS | yes | 72.6 | 127595 | 99968 | 27627 | 1569 | 0 |
| false-pass | direct | PASS | PASS | no | 57.9 | 147352 | 121600 | 25752 | 945 | 0 |
| false-pass | candidate.8 | PASS | PASS | no | 37.7 | 101190 | 74624 | 26566 | 783 | 0 |
| false-pass | candidate.9 | PASS | PASS | no | 55.4 | 151703 | 130944 | 20759 | 1012 | 0 |
| holdout | direct | PASS | PASS | no | 69.7 | 148288 | 125952 | 22336 | 1245 | 0 |
| holdout | candidate.8 | PASS | PASS | no | 60.4 | 126722 | 103680 | 23042 | 1064 | 0 |
| holdout | candidate.9 | PASS | PASS | no | 107.6 | 263187 | 240000 | 23187 | 2138 | 0 |

Audit hidden required HTTP `429`; the visible prompt did not name 429. All three
arms still FAIL audit. Do not use that miss as product proof. Candidate.8/9 also
wrote Danish `to gange` for a double-discount the English checker first missed;
that string was added **after** the audit runs.

Audit-direct originally stored `children: 7`; reparsed spawn items to `0`.
Direct `skill_read_mentioned: true` was a Superpowers false-positive.

## Observation

Candidate.9 had **no holdout correctness regression** and **no unique
correctness or safety win**. On holdout it used more wall time and more total
input than direct and candidate.8; uncached input was similar. n=9, one host,
contaminated arms: not a statistical comparison.

## Historical c9-01 (earlier the same day)

Source commit `84a0fcb`. Both arms public PASS, hidden FAIL
(`False` → `"False"` not `"-"`). The visible prompt did not state the False
hyphen. Launch prompt was not preserved. AMC 75.0 s / 188346 input vs control
52.6 s / 99814 input. Zero children both. Cases 2–4 were not run.

## Why the farm closed

A trustworthy behavioral answer needs many issues and many runs. That budget is
not available. Kernel changes cite host docs, published research, other public
repositories or practitioner guidance. Engineering checks and defects on real
commissioned work remain allowed.
