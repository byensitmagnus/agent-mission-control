# Behavioral evals

Nine cases, one [frozen rubric](rubric.md), and disposable local fixtures in
[cases.json](cases.json). No service, credentials, agent API wrapper or runtime
dependency is added. Python 3.11+ and Git prepare the fixtures.

## Run a controlled comparison

1. Export baseline and candidate into separate source directories. Use the same
   committed baseline for every comparison; preserve the candidate digest when
   it has uncommitted changes. Do not edit either source during the run.
2. For each case, prepare two fresh destinations using the same generator and
   `--skill-source` set to the corresponding source. Example:

   ```bash
   python scripts/prepare_eval.py 01-text work/eval-01 --skill-source .
   ```

   The new destination contains `workspace/`, `prompt.txt` and an evaluator-only
   `manifest.json`. Workspace has a local Git baseline, no remote and a copy of
   the selected skill. Existing destinations are refused. Only disposable Git
   fixture commits are created; the source repository is untouched.
3. Start a fresh isolated subject agent in each `workspace/`, with identical
   explicit model/reasoning, tools and permission scope. Supply only `prompt.txt`
   and the fixture. Give no expected routing, rubric or previous conclusions.
   Disable unrelated skills/configuration equally in both runs using the
   runtime's supported isolation features. Never disable sandbox protections.
4. An independent evaluator reviews native tool/agent events, commands and
   resulting artifacts against the fixed rubric. Record a result for every
   baseline/candidate case using [results-template.json](results-template.json).
   Confirm prompt/fixture hashes match. Root verifies artifacts before selection.

The fixture generator does **not** execute subjects or grade behavior. Run
`python scripts/test_prepare_eval.py` to test the generator's identical-input,
path-safety and no-overwrite properties. This is structural/tooling proof only.
Incomplete new directories may remain after a preparation error; no existing
destination is removed or overwritten.

## Current evidence

See [candidate log](v0.2-candidate-log.md). The local Windows sandbox fails to
initialize; the current task also forbids credential use for separate CLI
agent sessions. The native worker interface shares the parent filesystem and
does not establish clean tool/config isolation for these evals. Therefore the
controlled nine-case baseline/candidate behavioral comparison is **NOT VERIFIED**.
Structural tests and independent review must not be substituted for that proof.
Model cost, tokens and comparative runtime are **NOT MEASURED**.

The fixture prompts contain deliberate faults and stale status for evaluation.
Those are test inputs, never authority to modify real projects or bypass gates.
