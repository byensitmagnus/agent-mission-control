# Evaluation index

**Status of `main`:** runtime candidate.15, tagged `v0.2.0-candidate.15`.
Candidate.16 is on a branch, not yet released.
Latest runs: [Haiku smoke runs](haiku-smoke-2026-09-25.md), labelled smoke, not proof.
The [nine Codex runs](candidate.9/README.md) are a **closed postmortem**. Behavior, price and speed remain **NOT VERIFIED**.
Do not add cases or rerun them as product proof. AMC does
not run an owned behavioral research program; design cites host docs, published
research, other public repos and known practitioner guidance.
`evals/decision_kernel.py` is a deterministic regression test; it does not
launch agents. New kernel cases only falsify local contracts (break-even,
artifact handoff, budget ceilings). They do not prove AMC is the best workflow.

[Candidate.7 acceptance-review case](acceptance-review/README.md) records a
bounded comparison with candidate.6 and supplies a runnable 19-case controller.
Both repairs passed; only candidate.7 obtained independent acceptance review.
This is narrow behavior evidence with shared-host limitations, not general
quality, autonomy or cost qualification. Historical results below are unchanged.

The [whole-project research review](../docs/research-basis.md) and
[field state](../docs/field-state.md) are the basis for
the current local candidate. Routine acceptance uses deterministic tooling,
source review and observed real-task defects. No new behavioral benchmark is
required or reported for that update. Historical scores and their frozen cases
below remain unchanged and do not score the current candidate. Performance,
cost advantage and automatic host activation remain unverified.

[Completed Sol comparison and measurements](v0.2-fps-comparison.md): both task outcomes pass; incumbent retained.

# Public executable development cases

[Run the FPS-derived replays and accounting controls](fps-replays.md). These
checks are reproducible locally and included in the validation workflow. They
verify the test tooling, not a claim of agent superiority.

# Latest real-task evidence

[The FPS Booster pilot](v0.2-fps-pilot.md) records two real application tasks,
including an initial false reviewer PASS, exact-byte repair, model/context
observations and incomplete cost attribution. Final bounded repairs pass;
comparative AMC benefit remains NOT VERIFIED. Historical sections follow.

# Historical standalone experiment

[Iteration 3](v0.2-standalone-candidate.md) implements the standalone candidate and
records six actual Luna tasks, two narrow source refinements and an independent
review. Replacement qualification remains NOT VERIFIED; observed regressions and
host contamination are preserved. The sections below are historical results.

# Historical candidate recommendation

[Iteration 2](v0.2-control-candidate.md) passes its local simplification/review gate:
one ownership change, existing checks, ten Luna source-decision probes, zero new
Astra subjects. Real engineering superiority remains NOT VERIFIED. The historical
qualification below remains FAIL; its results and frozen evaluator are unchanged.

# Historical qualification, 2026-09-12

**2026-09-12: FAIL as an improvement candidate.** This FAIL does not score
current `main`. Nineteen authenticated matched-host
subjects completed the bounded evaluation (one timed out after a verified artifact).
Authentication is no longer the blocker. See [qualification](v0.2-qualification.md)
and [all results](results/2026-09-12-behavioral.json). The sections below preserve the
historical schema-2 clean-profile investigation; v3 used a different matched-host contract.

# Behavioral evals

Eleven realistic cases, one [frozen rubric](rubric.md), and disposable local
fixtures in [cases.json](cases.json) cover direct work, dependent chains,
independent fan-out, writer collisions, stale resume, measured optimization,
ordinary features, migration safety, missing evidence, autonomous repair and
external authority. Python 3.11+ and Git prepare the fixtures.

The v2 evaluator was frozen on 2026-09-11 before candidate instruction edits.
Its digest is SHA-256 of the exact `cases.json` bytes followed by the exact
`rubric.md` bytes:

```text
2c4f07976eef82371c10029e17e985a4d515c95c246b5c02aae386440f3060ac
```

## Prepare a controlled comparison

Use three immutable skill-source directories:

- v0.1.0: `fdbf07fa3443ca454509ca36ace6e2651b9fc2e6`
- v0.2 baseline: `358680dd4fedb3faf38a4599d1e20ed9a376c0fd`
- candidate: its recorded commit or content digest

For every case and subject, run the same generator into a new destination:

```bash
python scripts/prepare_eval.py 01-small-linear work/v01-01 --skill-source path/to/v0.1.0
python scripts/prepare_eval.py 01-small-linear work/v02-01 --skill-source path/to/v0.2-baseline
python scripts/prepare_eval.py 01-small-linear work/candidate-01 --skill-source path/to/candidate
```

Each destination contains `workspace/`, `prompt.txt` and an evaluator-only
`manifest.json`. The workspace has a local Git baseline, no remote and only the
selected skill snapshot. Existing destinations, linked/reparse sources and
linked/reparse destination ancestors are refused. The manifest binds the run to
the evaluator, case, prompt, fixture and copied skill hashes.

An `explicit` case names the skill. A `description` case deliberately does not,
so normal runtime discovery is part of the observation. Expected routing,
checks, rubric and previous verdicts stay outside subject context.

Before running subjects, prove that the runtime supplies all of these at once:

1. Fresh independent session and disposable workspace.
2. Identical explicit model, reasoning, tools, sandbox and approval policy.
3. The local target skill is visible, while user/global instructions and
   unrelated skills are absent.
4. Native command, file-change and agent events are captured for an independent
   evaluator.
5. Approval failures are fail-closed; no bypass, unrestricted sandbox or
   credential copying is used.

Do not run a batch until those controls pass. The fixture generator does not
execute or grade subjects. Run its structural checks with:

```bash
python scripts/test_prepare_eval.py
```

The test prepares all eleven cases against two copies of the current skill and
an alternate skill snapshot. It proves identical evaluator inputs across skill
versions, explicit/description prompt behavior, clean local Git fixtures,
no-overwrite behavior, Git-config isolation, path safety and linked-ancestor
refusal. It is not behavioral proof.

## Historical feasibility evidence

Codex CLI 0.153.3 can start an authenticated `--ephemeral` subject with
`--ignore-user-config`, `--approve-for-me`, explicit model/reasoning and native
JSONL events. A pilot completed the small linear edit in a disposable workspace
and emitted command and file-change events. CLI help defines
`--approve-for-me` as automatic review using the workspace-write sandbox; it
cannot be combined with the redundant `--sandbox` option.

That pilot is not a controlled result. Default-profile `codex debug
prompt-input` inspection still showed shared home instructions and unrelated
skill context with `project_doc_max_bytes=0`. The debug command has no
`--ignore-user-config` option, so it does not establish the exact context seen
by the exec pilot; `exec --ignore-user-config` alone also does not prove that
the shared instructions are absent. Context equivalence is unestablished.

A fresh temporary `CODEX_HOME` removed the observed shared context and retained
the project-local target skill, but the supported client then had no
authentication and the subject failed with HTTP 401. No credential was read,
copied or linked. The clean-home attempt also tried provider/plugin startup
traffic, so it was not repeated.

The prompt-isolation probe used this shape and printed only the byte-count and
marker booleans, never the prompt payload:

```powershell
$inputJson = codex debug prompt-input -c project_doc_max_bytes=0 'catalog probe' | Out-String
[pscustomobject]@{
  chars = $inputJson.Length
  shared_home_instructions = $inputJson.Contains('AI-MEMORY:INSTRUCTIONS:START')
  target_skill = $inputJson.Contains('agent-mission-control')
  unrelated_skill = $inputJson.Contains('Ponytail')
} | ConvertTo-Json
```

The independently repeated default-home probe returned 48,604 characters and
identified the shared-instruction and unrelated-skill references without
printing their contents. Because JSON escaping makes literal path matching
unreliable, the probe records content-reference markers rather than an exact
path-string assertion.
With `CODEX_HOME` set to the fresh directory
`C:\Users\Usmo1\AppData\Local\Temp\amc-codex-home-01a09218`, the same probe
returned 31,692 characters with the global and unrelated markers false and the
target marker true. An actual clean-home subject started thread
`01a09228-ad65-75f0-baee-8f3236013774`, then failed authentication. The retained
command-output anchor is `2026-09-11T20:28:54.665815Z` with HTTP 401; no stderr
file or session transcript was persisted.

The ephemeral authenticated pilot also warned that Guardian could not fork its
review session because persistence was disabled. This is a limitation of that
pilot, not proof that every safe approval configuration is unusable. Its
in-workspace commands completed, but approval behavior for a command needing
review was not established. A shared-context native subagent cannot prove the
missing clean authenticated context.

Therefore the three-version behavioral comparison is **NOT VERIFIED**. The
exact blocker is that a clean, authenticated and isolated subject context has
not been established without host auth/config setup. No behavior runner is
included because it would automate an unproved context. Model cost, comparative
time, tokens and superiority are `NOT MEASURED` or `NOT VERIFIED` as defined by
the rubric.

The fixture prompts contain deliberate faults and stale status. They are test
inputs, never authority to modify real projects or bypass gates.

## Matched-host qualification follow-up

The earlier clean-profile authentication failure is historical. A fresh
matched-host CLI session now authenticated through the existing ChatGPT login
without transferring credentials. The installed same-name Mission Control was
disabled per invocation; a local target skill was discovered instead.

A native preflight reproduced the original Python failure, repaired the fixture,
and reran the original Python check successfully. This establishes execution
feasibility, not comparative product improvement. Earlier pilots that failed
sandbox startup or substituted another language's assertions remain excluded.

The [v3 comparison](v3/README.md) tests incremental Mission Control behavior in
a locked shared host environment against the existing orchestration approach.
It is distinct from clean-room standalone qualification. Exact source loading,
fixture identity, runtime configuration and original command evidence remain
required for every scored run. No credentials were transferred or installed skills edited. Codex automatically added experiment workspace trust entries; only those exact paths were normalized.
