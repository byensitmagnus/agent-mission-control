# Contributing

Keep changes tied to an observed failure or a reproducible improvement. Run
the structural and safety checks documented in [README](README.md), and use
[behavioral evals](evals/README.md) for claims about agent decisions. Package
shape does not establish behavior.

## Offline skill evolution

Skill development is a separate task, after the source missions have ended.
Never change the controlling skill during the mission it governs.

1. Harvest observed failures from completed runs. Remove secrets, personal
   data, raw transcripts and unrelated context; reduce each failure to a small
   synthetic evalcase with inspectable inputs and outcomes.
2. Freeze the affected and held-out cases before proposing a small skill edit.
   Separate training/development examples from held-out checks.
3. Replay both sets in fresh comparable sessions. Inspect task artifacts and
   tool events; reject correctness, safety or routing regressions.
4. Retain the previous skill and rejection evidence. Stage a versioned candidate
   and its diff/results for human approval; do not auto-adopt it.

Without runnable behavioral evidence, the change remains a proposal with
NOT VERIFIED gates. Changing the evaluator requires an identified new
comparison. Do not optimize to exact wording, headings or agent counts.

This is an adaptation of validation-gated text optimization described in
[Microsoft SkillOpt](https://github.com/microsoft/SkillOpt), not a claim to
reproduce its reported benchmark gains. Nothing in the installed skill starts
a learning service or rewrites its own instructions.
