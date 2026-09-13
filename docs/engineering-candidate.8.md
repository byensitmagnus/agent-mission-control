# Candidate.8: installation and engineering evidence

Local engineering check, 2026-09-13, followed by development-branch publication.
The published release download is still candidate.4. Runtime instructions are byte-identical
to the retained candidate.7 runtime; this iteration changes tooling and guidance,
not the rules of an ongoing product task.

## Concrete changes and user benefit

| Before | Candidate.8 | Executable check |
|---|---|---|
| Users manually choose and copy a host-specific directory. | One project installer targets Codex, Claude Code, Cursor, Grok or Kimi, preserves existing files and checks installed bytes. | `python scripts/test_install_skill.py` |
| An evaluation source containing only `SKILL.md` could be prepared successfully. | All required runtime directories must exist and pass link checks before creating output. | `python scripts/test_prepare_eval.py` |
| Two usage files with the same session ID could silently collapse to one apparently complete result. | Duplicate IDs fail with a clear error; no misleading aggregate is returned. | `python scripts/test_usage_snapshot.py` |
| A missing mobile `srcset` asset passed structural validation. | HTML image/source candidates are checked along with existing links. | `python scripts/test_validate.py` |

The optional Codex verifier is now described as read-only evidence inspection.
Builds/tests that write artifacts remain the authorized lead's responsibility;
the example has not silently gained write permissions.

## Host observations

The real candidate runtime was installed into five separate disposable Windows
projects. All five byte checks matched the source and each other. This verifies
the installer and path mapping, not five completed native workflows.

| Host | Native observation in this iteration | Limit |
|---|---|---|
| Grok CLI 1.0.3 (1a29d5bc12) | `grok inspect --json` returned AMC with `source.type=project` and the exact new `.grok/skills/agent-mission-control/SKILL.md` path. | Discovery only; no model request or delegated task was run. |
| Codex CLI | The generated local protocol schema was inspected; an isolated `skills/list` probe failed before initialization with `Could not find home directory`. | Current discovery NOT VERIFIED. The earlier candidate.4 first-use record remains separate. |
| Claude Code | CLI available; native directory/invocation checked against its official documentation. | Current discovery and completed work NOT VERIFIED. |
| Cursor 3.20.17 | Editor CLI reports its version; directory/invocation checked against official documentation. | No native skill-selection or delegated-task check. A generic `agent` executable on this machine belongs to Grok, so it was not used as Cursor. |
| Kimi CLI | Installed launcher exits with `uv trampoline failed to canonicalize script path`. | Current discovery and task execution NOT VERIFIED; documentation alone is not a successful client run. |

No host settings, authentication, model choices or permissions were changed to
turn a failed probe into a success. [Host setup and sources](hosts.md) explain
selection, shadowing, required capabilities and normal recovery.

## Verification scope

The targeted installer controls cover five-host byte identity, existing-file
preservation, read-only mismatch reporting, invalid/provenance/linked paths,
copy failure, interrupted activation, changing package bytes and competing
destination creation. Regression checks cover the two reproduced integrity
bugs. The existing package builder still supplies provenance, deterministic
archives and source/output guards.

The lead executed all five affected check groups: **PASS**. This includes eight
installer tests, 11 tripled fixture preparations, usage integrity controls,
13 package tests and structural validation with 29 negative controls. The new
duplicate-ID fixture is removed before the existing invalid-timestamp controls,
so one expected failure cannot mask another. A separate documentation check
validated 114 local links and 21 anchors across 12 pages.

Both generated packages contain the same 16 runtime files as the source and
retained candidate.7. All 136 pre-existing repository files remain present;
all 83 existing evaluation files are byte-identical. Unaffected historical
replays were retained, not rerun. The installer check was added to GitHub CI;
remote CI had not run at that local checkpoint. For current branch validation,
inspect the pull request's Checks tab and the
[branch CI runs](https://github.com/byensitmagnus/agent-mission-control/actions?query=branch%3Acodex%2Famc-autonomy-proof).

Independent source review found no remaining material issue. It resolved the
installer's misleading `source_version` field by naming it `builder_version`;
fingerprints identify actual source bytes. A proposed comma-splitting change
was rejected after checking the HTML standard, because it would misparse URL
commas. These checks do not replace native-client execution evidence.

Local candidate.8 package SHA-256 values:

```text
7cde9319329f9a6ad793180dbb18434cf81df688bd8e6c7080d47771baf325be  agent-mission-control-skill.zip
33689433f3d24ed0b01655044e272c46b4efcc6806240fb530ae48246c78722e  agent-mission-control-plugin.zip
```

The ZIPs are built from the current development checkout, whose Git base is
`08e828a1aff0686dcbd6781364b40cc3239066cf` plus the recorded local changes.
The separate installed governing runtime and FPS product workspace were not
modified. Python packaging uses only the standard library.

These are engineering checks, not model benchmarks. No comparable complete
mission has been executed across all three projects and five clients. General
superiority, lower cost, faster completion and fewer user interventions remain
unverified. The [implementation comparison](choosing.md) preserves AO's actual
daemon/worktree/recovery strengths and the other project's Codex-profile scope.

[Install for your host](hosts.md) · [All evidence](evidence.md) ·
[Development checks](development.md)

## Follow-up: safe updates of existing installations

The same development branch now closes a concrete first-use gap: existing
installations previously required manual replacement. The explicit
`--update --expected-installed-sha256` operation replaces only the reviewed
file contents and retains the entire old directory outside skill discovery.
`--check` supplies the differences and fingerprint without writing files.
Stale confirmation, changing inputs and linked backup paths are refused.
A handled activation error restores the old directory if its destination is
free; a competing owner is preserved with a reported recovery location.
Power-loss recovery remains manual. No daemon, dependency or host/model config
change was added. [Use the update flow](hosts.md#update-an-existing-project-installation).

The lead executed 13 installer tests and 13 package tests, with no skips, and
structural/diff checks. A separate command-line journey installed the actual
candidate.4 runtime plus a local customization into each of five disposable
projects, then updated to this branch. All five retained the exact old bytes,
matched the new runtime, preserved project instructions, refused stale
confirmation without writes and made a repeated matching update a no-op.
These are filesystem/CLI checks, not native host activation or productivity
measurements. Runtime instruction bytes remain unchanged.

During lead review, an incorrect preservation-test expectation was corrected
and the competing-owner control was changed to exercise a real directory rename.
Source review also required checking an observed destination claim before
activation. The implementation does not claim cross-process locking against
hostile filesystem races.

A fresh Luna reviewer independently ran the installer controls and a disposable
CLI status check; no material finding remained. The updater research observation
in the mission record is separate read-only product work. It did not run or
change the product and is not a cross-model benchmark.
