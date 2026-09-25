# Results, versions and limits

AMC aims to make useful work easier to finish and verify. The records below show
what has actually been checked. They do not establish that AMC generally beats
another orchestration tool or an assistant working directly.

## Choose a version deliberately

| Version | Available as | What this means |
|---|---|---|
| **v0.2.0-candidate.4** | [Earlier release](https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.4), with skill/plugin ZIPs and checksums. | Historical first-use evidence concerns this prerelease. |
| **0.2.0-candidate.7** | Retained local experiment and runtime snapshot; no published release ZIP. | It adds verification guidance with a bounded review-ownership experiment. |
| **v0.2.0-candidate.8** | [Tagged ZIP](https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.8), with skill/plugin checksums. | Older runtime. Tagged source added five-host installation/checking/updating. [Engineering evidence](engineering-candidate.8.md). |
| **0.2.0-candidate.9** | Baseline `main` at `3f35485`, including [#6](https://github.com/byensitmagnus/agent-mission-control/pull/6) and [#10](https://github.com/byensitmagnus/agent-mission-control/pull/10). No tagged ZIP. | Unified kernel and three routes. Dated engineering checks concern specific source snapshots. Nine Codex runs remain a [closed postmortem](../evals/candidate.9/README.md), not current behavioral qualification. |
| **0.2.0-candidate.11** | Readiness work derived from `3f35485`; publication status is recorded in [MISSION.md](../MISSION.md). No tagged ZIP. | Repairs handoff consistency, installed links and first-use guidance. The [readiness record](reviews/readiness-2026-09-24.md) distinguishes completed checks and observed use from pending proof. |
| **v0.2.0-candidate.12** | [Latest tagged ZIP](https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.12) from `9084bc0`, with skill/plugin checksums. | Moves the verdict rules small models skip in reference files into `SKILL.md`. [Haiku smoke runs](../evals/haiku-smoke-2026-09-25.md): 7/10 → 9/10 on the shipped runtime (SHA-256 `e9cc02ad…7f586158`). |

The repository's CI badge describes current `main`, not every earlier release.
Keep the release tag's source identity and archive checksum together.
[Build instructions](development.md#build-both-formats) are for contributors;
normal use needs neither Python nor a custom model profile.

## What the evidence supports

| Observation | What passed | Practical limit |
|---|---|---|
| [Haiku smoke runs](../evals/haiku-smoke-2026-09-25.md) | Claude Haiku 4.5 on 10 repository cases, scored from files and transcripts: 7/10 on candidate.11, 9/10 on the shipped candidate.12. Stale resume passed in 3 of 3 runs; the release verdict held in 2 of 4 repeats (0 of 3 before). | One run per case in the main table, no run without AMC. Haiku still self-approved the release in 2 of 4 repeats. The fan-out case fails, and its check is stricter than the skill. |
| [Current readiness candidate](reviews/readiness-2026-09-24.md) | Full repository audit, targeted engineering checks, exact project install, explicit Codex skill input, checked review repairs and an actual three-file read. | Native read needed one approved command. No unassisted sandbox, desktop picker, other-host behavior or comparative improvement claim. Publication remains pending. |
| [Published skill first use](../examples/codex/compatibility.md#2026-09-13-standalone-skill-first-use-check) | A Windows Codex CLI session selected the exact project skill and returned supported README points. | A normal file-read approval was needed. Desktop/IDE discovery, plugin installation and role activation were not established. |
| [Direct versus AMC task](../evals/v0.2-fps-comparison.md) | Both completed the same bounded repair, 18/18 checks. | AMC did not improve the result in that pair and took more time. Cache/order and accounting limits prevent a general cost conclusion. |
| [candidate.6 versus candidate.7](../evals/acceptance-review/README.md) | Both repaired the gate correctly, 19/19 controller checks. Candidate.7 additionally obtained a fresh acceptance reviewer; a trivial control used no child. | One pair with shared host instructions. Both needed zero extra user process prompts. No general quality, user-effort or speed improvement is proven. |
| [Engineering validation](development.md#run-local-engineering-checks) | Checks cover structure, package integrity, fixtures, preservation, accounting and replay tooling. | Passing tooling tests is not proof of an agent's behavior on your project. |
| [Host portability](engineering-candidate.8.md#host-observations) | The real runtime installs identically in five isolated project directories; Grok's native inspector finds the exact project copy. | File placement is not native discovery. Other current client observations and end-to-end limits are stated individually. |
| [Read-only research follow-up](engineering-candidate.8.md#read-only-research-observation) | One Terra lead delegated to Luna, checked counterevidence and returned a supported refutation without further user coordination. The controller checked the retained claim and unchanged snapshot. | One development observation with newly supplied caller context; no causal comparison, runtime execution or measured savings. |

[Earlier qualification failures](../evals/v0.2-qualification.md) and
[real product observations](../evals/v0.2-fps-pilot.md) remain available.
The [research basis](research-basis.md) separates external findings from AMC's
own design decisions. [Field state](field-state.md) grades those findings A–E
and compares mechanisms across product classes. The workflow diagrams and sample
deliveries are illustrations.

## Judge the result on your own work

Start with a bounded task you already need, using the [task recipes](task-guide.md).
Inspect three things: did the requested behavior work, did existing behavior
survive, and did the lead complete integration and verification without making
you coordinate its workers? Save actual failures and corrections as well as wins.

If you compare approaches, keep the task, starting files, acceptance checks and
host comparable. Count setup, lead, workers, review, retries and user intervention.
Agent counts and test counts alone do not measure quality. Similar successful
runs are needed before making broad claims about speed or effort.

For normal feedback, one concrete experience is enough; no paid benchmark is
required. [Report what happened](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml)
without secrets, customer data or raw private conversations.

[Get started](getting-started.md) · [Compare approaches](choosing.md) ·
[Historical evaluation index](../evals/README.md)
