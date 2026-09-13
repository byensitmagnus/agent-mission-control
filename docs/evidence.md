# Results, versions and limits

AMC aims to make useful work easier to finish and verify. The records below show
what has actually been checked. They do not establish that AMC generally beats
another orchestration tool or an assistant working directly.

## Choose a version deliberately

| Version | Available as | What this means |
|---|---|---|
| **v0.2.0-candidate.4** | [Published early-use release](https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.4), with skill/plugin ZIPs and checksums. | This is the version used by the public installation guide. It is a prerelease. |
| **0.2.0-candidate.7** | Retained local experiment and runtime snapshot; no published release ZIP. | It adds verification guidance with a bounded review-ownership experiment. |
| **0.2.0-candidate.8** | Development source in this branch; no published release ZIP. | Same runtime as candidate.7, with five-host installation/checking and repaired evaluation/accounting utilities. [Engineering evidence](engineering-candidate.8.md). Downloading candidate.4 does not install these changes. |

The repository's public-main CI badge does not describe this development branch;
check the pull request's Checks tab for its current source.
For a development package, keep its source identity and archive checksum together.
[Build instructions](development.md#build-both-formats) are for contributors;
normal use needs neither Python nor a custom model profile.

## What the evidence supports

| Observation | What passed | Practical limit |
|---|---|---|
| [Published skill first use](../examples/codex/compatibility.md#2026-09-13-standalone-skill-first-use-check) | A Windows Codex CLI session selected the exact project skill and returned supported README points. | A normal file-read approval was needed. Desktop/IDE discovery, plugin installation and role activation were not established. |
| [Direct versus AMC task](../evals/v0.2-fps-comparison.md) | Both completed the same bounded repair, 18/18 checks. | AMC did not improve the result in that pair and took more time. Cache/order and accounting limits prevent a general cost conclusion. |
| [candidate.6 versus candidate.7](../evals/acceptance-review/README.md) | Both repaired the gate correctly, 19/19 controller checks. Candidate.7 additionally obtained a fresh acceptance reviewer; a trivial control used no child. | One pair with shared host instructions. Both needed zero extra user process prompts. No general quality, user-effort or speed improvement is proven. |
| [Engineering validation](development.md#run-local-engineering-checks) | Checks cover structure, package integrity, fixtures, preservation, accounting and replay tooling. | Passing tooling tests is not proof of an agent's behavior on your project. |
| [Host portability](engineering-candidate.8.md#host-observations) | The real runtime installs identically in five isolated project directories; Grok's native inspector finds the exact project copy. | File placement is not native discovery. Other current client observations and end-to-end limits are stated individually. |

[Earlier qualification failures](../evals/v0.2-qualification.md) and
[real product observations](../evals/v0.2-fps-pilot.md) remain available.
The [research basis](research-basis.md) separates external findings from AMC's
own design decisions. The workflow diagrams and sample deliveries are illustrations.

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
