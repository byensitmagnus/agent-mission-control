# Candidate.9 three-arm comparison

**Closed.** Do not add cases, rerun arms or treat this protocol as product
proof. A trustworthy AMC behavior claim would need many runs across many
issues; that budget is not available. Keep these files as a frozen record.

Historical `c9-01` on commit `84a0fcb` stays in
[../results-2026-09-14.json](../results-2026-09-14.json). Both arms failed a
hidden False hyphen that the visible task did not state. Do not use that pair
as product evidence.

`evals/decision_kernel.py` is a deterministic regression test. It does not
launch agents and does not enforce runtime behavior.

## Arms

Same host, model, reasoning, tools, timeout and approvals on every arm.
Sandbox is identical across arms *within a case*.

| Arm | Skill | Source |
|---|---|---|
| `direct` | None | empty `.agents/skills/` |
| `candidate.8` | Published runtime from `c49dc1be2e334091f6c841047ff2ad778b7bde84` | `git archive` of `SKILL.md`, `LICENSE`, `agents/`, `references/`, `templates/`, `assets/` |
| `candidate.9` | Branch runtime at launch | same path set from the worktree used for the run |

Host freeze: Codex CLI `0.153.3`, model `gpt-5.6-sol`, reasoning `medium`,
`--ignore-user-config --ephemeral --approve-for-me --json`. Timeout 180 s.
One attempt per arm per case. No retries. `--approve-for-me` selects
workspace-write; do not also pass `--sandbox`. Audit still forbids editing the
two source files; the hidden checker verifies the planted defects remain.

Shared contamination: every arm still loaded the user Superpowers plugin from
`~/.codex/plugins`. This is not naked single-agent isolation. Direct did not
install AMC.

## Cases

Hidden checkers live in `hidden/` and are **not** copied into the subject
workspace. A hidden check may stay unpublished, but its expected behavior must
be derivable from the visible contract. It must not test guessing an unnamed
product requirement.

| Id | Role | Visible contract | Hidden | Derivable? |
|---|---|---|---|---|
| `audit` | Development | Read-only. Name the concrete defect in `billing.py` and in `notify.py`. Write `AUDIT.md`. Do not edit code. | Report names `apply_discount` double discount and `should_retry` missing 429 | Billing yes. Notify `429` **no** — same class as `c9-01`. Not product evidence |
| `false-pass` | Development | `format_value(None)` and `format_value(False)` must be `-`. Bundled `check.py` omits False. Do not claim PASS until False is evidenced | `format_value(False) == "-"` | Yes |
| `holdout` | Held-out after freeze | `parse_total` skips blank lines and `#` comments. Bundled `check.py` is the happy path only. Do not claim PASS until comments and blanks are evidenced | `#` and blank lines ignored; numeric lines summed | Yes |

`SKILL.md` was not changed after these cases or after holdout. Audit and
false-pass are development/selection data. Holdout is the unused case.

Budget: the nine runs are spent. Do not add a tenth.

## Launch (historical)

The command below is how the bound results were produced. Do not rerun it as
product proof.

```bash
python evals/candidate.9/comparison/run_subject.py --arm direct --case audit --out ../amc-eval-runs/audit-direct
```

Bound copies are under [results/](results/).

## Ranking (historical)

Used only to read the nine frozen runs. Not a method to extend.
