# Public replays derived from the FPS pilot

These anonymous development fixtures reproduce two observed failure modes:
unsafe JSON classification accepted by a mistaken review, and an encoding repair
that must preserve all original file bytes. They contain no FPS application source
or customer data. They are development cases, not held-out evidence or a benchmark
showing AMC superiority.

## Run the checks

Python 3.11+ and a .NET 8 SDK are required for the JSON fixture. One command runs
both replay cases and their positive/negative evaluator controls:

```sh
python evals/fps_replay.py --self-check
```

If the SDK is outside PATH, append `--dotnet /path/to/dotnet` (or `dotnet.exe`).
No packages beyond the SDK are required. The checker compiles and runs **trusted
candidate C#** in a temporary directory; it is not an untrusted-code sandbox.
The encoding checker compares bytes and never executes PowerShell.

## Give an agent a small task

```sh
python evals/fps_replay.py prepare json /new/task-directory
python evals/fps_replay.py check /new/task-directory
```

Use `encoding` instead of `json` for the second task. Preparation refuses an
existing destination or manifest, including linked output paths and ancestors. The task, source, quoted review data and
preserved user-state are in the directory; the baseline manifest is outside it.
Only the source named in `task.txt` may change. Invoke the evaluator but do not
edit it or the manifest. Additional files are permitted and need proportional
human review; the checker does not sandbox agent writes.

JSON requires all 18 fixed outcomes, including malformed types, missing fields,
overflow and invalid JSON. An empty or incomplete output cannot earn PASS.
Encoding requires exactly EF BB BF plus the original bytes. Both cases reject
changes to preserved fixture files and invalid baseline bindings. Missing dotnet
is NOT_VERIFIED rather than a successful check.

The control suite deliberately runs broken baselines, known-good repairs,
behavior regressions, forged empty results and corrupted preservation/bindings.
These controls verify the evaluator, not an agent's behavior.

## Account for the whole run

The read-only native counter collector follows a controller and its descendants,
subtracts pre-window counters, handles resets and includes failed attempts:

```sh
python scripts/test_usage_snapshot.py
python scripts/usage_snapshot.py --sessions /local/codex/sessions --root-id CONTROLLER_ID --since 2026-09-12T22:08:25.813Z --expected-agent /root/subject --out /local/proof/usage.json
```

Use the timezone-aware ISO 8601 timestamp of the initial user request or a
preregistered arm start. Z and equivalent UTC offsets identify the same instant;
invalid or timezone-free timestamps are refused.
Expected agent names expose missing records. Missing usage/baselines remain
unknown, never zero. Complete malformed records fail closed; an unflushed final
line is omitted. Output contains counters, model/effort and visible initial
message character counts/marker flags, not raw conversations.

Every snapshot ends at each session's last observed counter. Unflushed work and
the final response can be missing, so this is not final billing. Cached input is
already included in input. Visible message characters exclude parts of the host
and tool input and cannot identify their individual token costs. Native IDs and
local paths in private snapshots should be removed before public sharing.

## Controlled comparison contract

The first comparison uses one JSON task twice: Sol/medium direct and Sol/medium
with an explicit frozen AMC source. Both receive fresh histories and the same
checker, runtime and host. Shared instructions remain, so this is a matched-host
workflow comparison, not an isolated skill-only causal experiment.

Two initial subjects maximum; no retry replaces a failed outcome. Each has a
180-second monitored stop and a 600000 observed-input stop for its subject tree.
Counter lag and in-flight calls can overshoot; record the actual interruption and
usage. Controller, preparation and review usage are recorded separately and stay
in the total cost coverage. AMC may request one bounded Luna/medium reviewer;
direct work stays single-agent. No topology earns points.

Correctness and preservation are hard gates. Report interventions, tokens by
actual model and elapsed time separately; do not invent a dollar score or
conclude broad savings from a single pair. Encoding is withheld from these
subjects for a different-case check if an attributable rule change is justified.
Retain the incumbent when evidence does not justify a rule change.

[Historical real-task pilot](v0.2-fps-pilot.md) preserves the observations that
motivated these development fixtures. Frozen historical evaluations remain unchanged.
[First completed direct-versus-AMC pair](v0.2-fps-comparison.md): both pass; no rule change or price-saving claim.
