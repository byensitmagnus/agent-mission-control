# Daily-use readiness review — 2026-09-24

## Scope and source identity

The user requested a complete repository review and practical improvements,
grounded in the referenced projects and official AI documentation. Baseline:
`main` `3f35485679ad906fd900faaba9c1d1f2786b80a3`. Work is isolated on
`codex/usage-readiness`; [MISSION.md](../../MISSION.md) owns live status and
[the goal](../../.claude/GOAL.md) owns the exit gate.

The review covered all **159 tracked files**, with an exact Git-blob match for
every coverage entry, and **264 paths across the reachable history**. All 44
non-merge commits were covered by scoped full-diff reading. Eight merge commits
had empty combined diffs: no additional merge resolution was omitted. Identical
blobs/patches were read once after identity checks; three raster assets were
visually inspected. Historical evaluation fixtures include deliberate defects.

Three independent audit scopes covered runtime, engineering and sources; the
lead read user documentation, integrated findings and checked the coverage
inventory. Six pre-existing local edits in the user's other checkout were read
and preserved. Local audit manifests retain paths, hashes and coverage; raw
private session transcripts are not part of this review.

| Repository surface | Role | Decision |
|---|---|---|
| `SKILL.md`, `references/`, `templates/`, `agents/`, `assets/`, `LICENSE` | Installed portable runtime | Keep one lead; repair route, handoff and evidence consistency |
| `README.md`, `docs/`, `examples/` | Public presentation, setup, recipes and provenance | Lead with a useful outcome; distinguish discovery, loading and task evidence |
| `scripts/`, `.github/workflows/` | Build, install and engineering checks | Check actual packaged links; expose existing trusted-source API; add Windows coverage |
| `evals/` and archived reviews | Local contract controls and historical observations | Preserve limits and negative findings; no new subject-run farm |
| `.claude/GOAL.md`, `MISSION.md`, contributor instructions | Product goal and current work | Finite daily-use exit gate, current artifact and explicit publication authority |

### Open changes were inspected, not blanket-merged

GitHub PR identity was read directly on 2026-09-24:

| PR | Verified head / state | Disposition for this work |
|---|---|---|
| [#7](https://github.com/byensitmagnus/agent-mission-control/pull/7) | `f5fa9c86c067827610f354a019ed6b108c5e20ef`, open | Superseded contract draft; do not revive |
| [#8](https://github.com/byensitmagnus/agent-mission-control/pull/8) | `6613960540c5f062e8ccb2df7ab9568fa26c7b9e`, open | Reuse focused ideas; 2,211-line Guard and JSON contract stay out of core |
| [#9](https://github.com/byensitmagnus/agent-mission-control/pull/9) | `fb121bbdaf0162cd9ce971557bdf880840742ae9`, stacked on #8 | Orca and generated claims remain optional research, not installation prerequisites |
| [#10](https://github.com/byensitmagnus/agent-mission-control/pull/10) | `072e52df7c77e035b83b919a0cb1af9c6063dfa8`, merged as `7b72be5` | Existing milestone included in baseline; not the complete daily-use gate |

No PR was closed or merged by this review. The repository was already public;
its existing About description and topics matched a portable coding-agent skill.

## Why these changes

| Observed problem | Repair | User-facing result |
|---|---|---|
| Specialist route required a preceding artifact even when expertise or fresh context was sufficient | Treat real upstream dependencies conditionally | A useful investigator can start from existing source without an artificial prerequisite |
| Read inputs and exclusive write ownership were conflated | Separate shared read context from owned changes | Specialists can inspect the same facts while writers avoid collisions |
| Self-acceptance and retry rules could block useful continuation | Require adequate acceptance evidence; diagnose repeated failures per job/hypothesis | The lead remains accountable and continues other authorized work |
| Evidence packets lacked current artifact identity | Carry snapshot/digest and local edit state | A result can be matched to the version actually checked |
| Three runtime links targeted excluded `examples/` or `docs/` files | Use public reference links and validate packaged links | Installed navigation works, not just navigation in the full repo |
| Windows short and long names for the same path failed provenance/containment checks | Compare physical paths after rejecting linked ancestors | Normal Windows temporary paths work without allowing source/output overlap |
| README quiz was described as proof of skill selection | Separate byte match, discovery, invocation and task outcome | Setup guidance makes the actual proof boundary clear |
| First useful example assumed fictional export files | Start with the user's outcome and actual project paths | A new user can begin work without constructing a demo project |

The existing responsive SVG artwork is retained. GitHub-rendered Markdown was
saved before and after; the candidate was inspected in a local preview at wide
and 390-pixel widths, with light and dark styling. The preview approximates
GitHub CSS; final published rendering remains a publication check. Existing
public GitHub rendering was inspected as the baseline. Images loaded and the
narrow page had no horizontal page overflow.

## External grounding

The detailed mechanism/source/limit map belongs in [field state](../field-state.md)
and [sources](../sources.md), not in ordinary task context. This review used the
official OpenAI skills/subagents/App Server documentation, Anthropic context
engineering and Claude Code guidance, Google ADK graph documentation, NVIDIA
AVO, and pinned sources for Agent Orchestrator and Codex Astra/Luna.

The transferable choices are selective context, useful specialist isolation,
actual input/output dependencies, lead-owned integration, recoverable state and
evaluator-backed optimization where an objective evaluator exists. Framework
APIs and orchestrator services remain host facilities. Newer upstream AO/CALO
heads differed from inspected pins; they were not represented as fully audited.

## Engineering and actual use

Baseline checks were rerun from a byte-identical independent clone because a
Windows-created Git worktree's metadata was not usable by WSL Git. Python was
3.12.8 under WSL; native Windows `python` was a Store alias. No shared Git metadata
or global Python/host settings were changed.

| Check | Baseline `3f35485` | Readiness candidate |
|---|---|---|
| Structural validator | PASS | PASS on Windows and Linux; validator regression controls also pass, including 62 negative controls |
| Package tests | 14 passed | Windows: 15 passed, 2 symlink controls skipped. Linux: 16 passed, 1 Windows-only control skipped |
| Installer tests | 13 passed | Windows: 12 passed, 2 symlink controls skipped. Linux: 14 passed |
| Windows junction controls | Not present | 2 passed, no skips; short/long path regression also ran and passed locally |
| Decision kernel | 36 cases passed; policy self-check only | 39 cases passed; still policy self-check only |
| Native Codex discovery | Exact project copy listed alongside old personal copy | Exact updated project copy listed; guarded update and byte check MATCH |
| Explicit skill use on commissioned work | Not established by discovery | Explicit project skill input, reviewed repair findings and approved native three-file read; lead accepted the bounded report |

Baseline installed runtime SHA-256:
`6708acc7c6a1bc1b62e5aea7711e5e04804aef5cb05fbbfeb1a1f741f61f69b3`.
Candidate.11 runtime SHA-256:
`4301eefdf4768522cd7d924bcbdc3f88c424f270eb14042ade5ceb6e0b6a52f8`.
The skill and plugin ZIPs were built through the public CLI, their runtime
hashes match this identity, and their packaged links pass. ZIP SHA-256 values:

- Skill: `38b25a821a5758b39095b31b220642b6250420578f942cae49abbe5dca3f2f9c`.
- Plugin: `4b44e4809ead81b60da192b457daaf86e57ae3fc7ab16d8ce95c192345363567`.

These are local review artifacts, not a published release. The prior project
installation was preserved in the installer's reported backup directory.

Native Windows used a scratch-only official PSF Python 3.14.7 embeddable
distribution; global Python, PATH and host settings were unchanged. Linux used
Python 3.12.8 and an independent Git clone with 161 candidate files verified
byte-for-byte. Linux fixture preparation, usage-snapshot controls and the
117-case preservation self-check also passed. Fixture preparation failed on
Windows at its unguarded symlink setup (WinError 1314); it passed on Linux.
The unchanged .NET FPS replay was not rerun. Remote CI for this unpublished
candidate remains pending.

An independent reviewer read the complete engineering diff and relevant
callers and reported no material findings; the lead separately executed the
checks above. Windows CI exercises junction rejection, but a runner without
distinct short/long aliases can skip that alias-specific regression. There is
no claim that every filesystem variant was exercised.

### Native task observation

The useful task is an acceptance review of this commissioned change. Codex
0.156.1 App Server discovered the exact project skill and received its absolute
path as an explicit skill input, using the existing default model and normal
read-only permissions. The first attempt failed before shell execution with
`registered Core process has no package identity`. No escalation was granted
and no security or host configuration was changed.

A second attempt completed the same real review task with 13 full,
line-numbered source files supplied as a frozen snapshot. It returned four
findings. The lead confirmed and repaired three: an unresolved superseded
writer must not mutate an accepted artifact; Claude Code's personal/project
name conflict needs an actionable resolution; and the blank mission template
must respect an explicit publication mandate. The fourth alleged a validator
failure on `None.`. Actual code already accepts that form, so no validator
change was warranted; the prose now states the optional period explicitly.
The existing 62 negative controls were rerun after updating their changed
template mutation target and passed.

The corrected skill was installed with a guarded update and checked as MATCH.
A narrow follow-up reviewed only those repairs against the updated source and
reported all four findings resolved, with no material new contradiction.
This exercises skill loading and text review; it cannot establish native
filesystem tools or writer isolation. The local record retains file hashes
and invocation evidence. Raw private session transcripts are not published.
No user intervention was required for the review itself, but the lead supplied
the snapshot because the host could not read files at that stage.

A bounded file-read attempt removed two inherited Desktop Core identity
hints from the standalone child process only. The shell then started, but
Windows denied access to the installed `SKILL.md`. The reviewer stopped on that
error. Read-only sandboxing and on-request approvals remained enabled; there
were no global environment, ACL or host configuration changes. This narrows
the remaining issue to the native file-access path, not skill discovery.

The existing [compatibility record](../../examples/codex/compatibility.md#2026-09-13-standalone-skill-first-use-check)
already documented a normal one-command read approval for this Windows path.
The lead inspected and approved exactly one `Get-Content -LiteralPath` command
for the installed skill, current README and getting-started guide through the
host's ordinary approval API. It returned exit 0. The lead compared the returned
contents against all three current files, then checked the report's section
references and route-to-deliverable explanation. No material first-use
contradiction remained in that bounded review. The audit client was restarted
once to restore its closed approval-input channel; that incomplete attempt
was terminated and never accepted as proof.

Native loading and this approved reading task are established for Codex 0.156.1
with the current runtime. No session-wide approval, execution-policy amendment,
ACL change or global setting was granted. The lead handled the one read approval
within the user's existing audit mandate. Unassisted Windows sandbox reads,
desktop/IDE picker interaction, other hosts and native child-agent isolation
remain outside this observation. This is one real acceptance workflow with
setup failures and checked repairs, not a comparative benchmark.

## Remaining boundary

Local candidate review is complete. Publication and the final main-based project
installation await publication authority and the remote checks. Comparative quality,
cost and speed remain unmeasured; these are separate research questions, not
prerequisites for the finite practical exit gate.
