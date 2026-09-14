# Candidate.9 three-arm results

Host: Codex CLI 0.153.3, `gpt-5.6-sol`, medium, `--ignore-user-config --ephemeral --approve-for-me`.
Shared contamination: Codex still loaded the user Superpowers plugin from
`~/.codex/plugins` on every arm. This is not a naked single-agent isolation.
No user interventions. Hidden checkers were not in the workspace.
`user_interventions` is protocol-recorded as 0, not parsed from host events.

Audit hidden originally required English `twice`; candidate.8/9 wrote Danish
`to gange`. That string was added to the checker after the audit runs. Frozen
launch `hidden_hash` for all three audit arms is
`bbe2a1a30da0e1f280f28060e80edecb72b148bf22cde1d87b3cf223bdc9276b`. Current
`hidden/audit_check.py` is `a88545fa2c00387324e0c2e8f70a14f6f2aa323969dcf97db555d52e46f2b863`.
All three arms still FAIL audit because none named HTTP 429. The visible audit
prompt did not name 429. Do not use the audit notify miss as product proof.

`false-pass` and `holdout` were not used to change `SKILL.md`. Holdout ran
after those development cases with the same runtime.

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

Bound files per run: `prompt.txt`, `launch.json`, `result.json`, `final.md`,
`codex.jsonl`. JSONL SHA-256 values are in [matrix.json](matrix.json).
Audit-direct originally stored `children: 7`; reparsed from `codex.jsonl` with
the spawn-item parser to `0`. Direct `skill_read_mentioned: true` is a
false-positive on Superpowers text, not AMC installation.

Candidate.9 holdout runtime hash at launch:
`3ce8b8ae4c78ace99b2f6699d1aa6adb41409ecc2b45ed0bee184b1c66bdaf2d`.

## Observation

Candidate.9 had **no holdout correctness regression** and **no unique
correctness or safety win**. On holdout it used more wall time and more total
input tokens than direct and candidate.8; uncached input was similar. General
price/speed superiority remains NOT VERIFIED. These nine runs are not a
statistical comparison. Audit notify-429 is not a valid hidden contract.
