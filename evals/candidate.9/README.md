# Candidate.9 bounded comparison protocol

The nine-run comparison is
[comparison/README.md](comparison/README.md). **Closed.** Do not launch
`run_subject.py` as product proof. Hidden checks for `false-pass` and `holdout`
were stated in the visible prompts. The audit notify `429` check was not; that
case is development data.

## Historical c9-01 (not product evidence)

Frozen 2026-09-14 before an earlier launch. **Do not use as product proof.**

Subject runs: **c9-01 executed 2026-09-14** on source commit `84a0fcb`. Both
arms public PASS, hidden FAIL (`False` → `"False"` not `"-"`). The visible
prompt did not state the False hyphen. Launch prompt and exact command were not
preserved. AMC 75.0 s / 188 346 input vs control 52.6 s / 99 814 input. Zero
children both. Cases 2–4 were not run.
See [results-2026-09-14.json](results-2026-09-14.json).
