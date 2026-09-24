# Practical-use gate evidence, 2026-09-24

Milestone: PR #10 merged as `main` `7b72be5`. This note does not close the
daily-use goal. Gate 2 stays NOT VERIFIED.

## README before and after

Before, `df184ad` `README.md`: "Give your coding agent an outcome. It chooses
the smallest graph that can finish and prove the work." The first action was a
read-only README quiz. The diagram said "Focused help."

After, `7b72be5`: "For a hard coding job inside the assistant you already use."
The first useful action is the filled bug prompt. The diagram says "One
specialist or parallel" and is labeled illustrative.

Rendered check 2026-09-23, local HTTP preview of the SVG files: the navy card
stayed readable on a white page and on `#0d1117`. At about 390px the mobile
SVG showed Lead, Direct work, Specialist or parallel, and Integrate & verify.
The wide capture frame cut the right edge of the desktop SVG; the file itself
contains that box.

About text set 2026-09-23: "Portable workflow skill for coding agents. One lead
chooses direct work, one specialist, or parallel help, then shows what was
checked." Topics: `agent-skills`, `coding-agents`, `claude-code`, `codex`,
`cursor`, `markdown`.

## One task

2026-09-23, temp project `amc-export-bug`. `cell(0)` returned `''`.
`python3 -m unittest tests.test_export` failed with `'' != '0'`. A Cursor
agent read the installed skill, stayed one lead, changed `src/export.py`, and
the same command then passed 2 tests. No commit and no push.

Friction: Windows `python` was a Store stub, so the check ran with `python3`.
The agent was given the skill path. The IDE picker was not used. Resume was
not required.

## Backlog

Not this gate: PR #8 JSON contract and checker. PR #9 Orca CLI. Quality, price,
and speed remain NOT VERIFIED.
