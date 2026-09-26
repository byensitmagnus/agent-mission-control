# Get started with Agent Mission Control

[Install](#1-install-the-skill) · [Select](#2-select-the-installed-copy) ·
[Confirm the copy](#3-confirm-the-selected-copy) · [Useful task](#4-do-one-useful-task) ·
[Troubleshooting](#troubleshooting)

You need a coding assistant with native Agent Skills and a project folder.
AMC is workflow instructions. Your existing account supplies models and tools.
No extra API key or server.

## 1. Install the skill

Install the **current `main` source**. That is the kernel this site describes.
The latest tagged ZIP, [candidate.14](https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.14), contains the same runtime with checksums.

**Fastest path** (Node.js). From your project folder, the open
[skills CLI](https://github.com/vercel-labs/skills) copies only the skill folder:

```bash
npx skills add byensitmagnus/agent-mission-control
```

It asks which agents to install for; `-a claude-code` (or `codex`, `cursor`, …)
chooses directly. The result is the same 16 runtime files as the checked path.

**Claude Code plugin.** The repository is also a plugin marketplace. In Claude Code:

```text
/plugin marketplace add https://github.com/byensitmagnus/agent-mission-control
/plugin install agent-mission-control@amc
```

Use the HTTPS URL: the `owner/repo` shorthand clones over SSH and fails without a
GitHub SSH key. The plugin route downloads the repository into Claude Code's plugin cache and loads one skill: no agents, hooks or MCP servers. Invoke it as
`/agent-mission-control:agent-mission-control`. A plugin installs for your user
by default; from a shell, `claude plugin install agent-mission-control@amc --scope project`
limits it to the current project.

**Checked path** (Git and Python 3.11+). Byte-checked install, update with a
retained backup, and no overwrite of an existing copy. Clone this repository,
then install into an existing project:

```bash
git clone https://github.com/byensitmagnus/agent-mission-control.git
cd agent-mission-control
python scripts/install_skill.py --host claude-code --project "../my-app"
```

Replace `claude-code` with `codex`, `cursor`, `grok` or `kimi`. Details:
[hosts.md](hosts.md#install-the-current-source).

**Copy path** (no tools). Clone or download the default branch. Copy the whole
folder `skills/agent-mission-control/` into the skill directory for your host,
keeping the folder name `agent-mission-control`. It contains `SKILL.md`,
`LICENSE`, `references/`, `templates/`, `agents/` and `assets/`.

| Host | Project directory |
|---|---|
| Codex | `.agents/skills/` |
| Claude Code | `.claude/skills/` |
| Cursor | `.cursor/skills/` |
| Grok | `.grok/skills/` |
| Kimi | `.kimi/skills/` |

The file that must exist:

```text
your-project/<host-skills-dir>/agent-mission-control/SKILL.md
```

Copying only `SKILL.md` breaks the skill. Dot-folders may be hidden.

**Codex can do the files.** Open the target project and paste:

```text
Install Agent Mission Control from
https://github.com/byensitmagnus/agent-mission-control
into this project only. Use the default branch, not a tagged ZIP.

Copy the repository folder skills/agent-mission-control/ into
.agents/skills/agent-mission-control/. Inspect first. Preserve any existing
installation or customizations; if one exists, show the difference before
replacing it. Do not change global settings, model defaults or permissions.
Confirm the installed SKILL.md path. Help me select that project copy,
especially if another skill has the same name.
```

[Version details](evidence.md#choose-a-version-deliberately).

## 2. Select the installed copy

Open the same project. Invoke `agent-mission-control`, then verify which path
the host selected; not every host offers selection by path:

- **Codex:** `/skills`, `$`, or the desktop picker
- **Claude Code:** `/agent-mission-control`
- **Cursor:** Customize → Skills, or `/` in chat
- **Grok:** `/agent-mission-control` after `grok inspect --json` from the project
- **Kimi:** `/skill:agent-mission-control` from the Git root

In Claude Code, a same-named personal copy wins over the project copy. Resolve
that conflict with the [duplicate-copy instructions](hosts.md#resolve-a-claude-code-name-conflict)
before trusting the project installation.

The path must end in `agent-mission-control/SKILL.md` **inside this project**.
A global or older copy with the same name is a different install. Restart the
client if a new folder does not appear. A file on disk is not proof the client
loaded it. If the skill loads but cannot read a file, fix that permission
before treating the first task as done.

## 3. Confirm the selected copy

Inspect the host's selection or invocation record for the exact project path.
An installation check proves bytes; a discovery list proves visibility; an
explicit skill invocation or loaded-instruction record establishes which copy
was supplied to a task. An agent saying “I used AMC” is insufficient.

For an optional read-only smoke task, start in a project that has `README.md`.
Keep your current model and normal permissions. Use your host's invocation:

```text
$agent-mission-control

Read README.md in this project. In at most three bullets:
- Explain what the project does.
- Give one example of a task it helps with.
- Name one limitation or unanswered question.

Cite the README.md section heading for each bullet; do not guess line numbers.
Do not change files, install anything, run project checks, or delegate.
Say explicitly that no checks were run.
```

**Task complete when:** each bullet is supported by the README, no project files
changed, and the answer says checks were not run. This checks a bounded reading
task. The answer alone proves neither skill loading nor application behavior.

## 4. Do one useful task

Describe one outcome you already need and two observable acceptance criteria.
You can use [the bug prompt](task-guide.md#fix-a-bug), a
[bounded investigation](task-guide.md#one-specialist-for-a-bounded-investigation),
or [resume saved work](task-guide.md#resume-unfinished-work). Example file names
are placeholders; use your project's actual paths.

You should get back the files or report, the checks that actually ran, and what
is still open. A worker finishing is not that result.
[Share what happened](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml)
after you remove private information. One example is enough: the goal, what the
agent did, the result you checked, and where you stepped in.

## Troubleshooting

| What you see | What to check |
|---|---|
| AMC is missing from the picker | Confirm `SKILL.md` is in this project’s host directory, not a doubled `agent-mission-control/agent-mission-control/` folder, then restart the client. |
| Two AMC entries appear or an older copy loads | Select the project path where supported. For Claude Code, follow the [name-conflict instructions](hosts.md#resolve-a-claude-code-name-conflict). |
| The agent cannot read the README | Resolve the host’s file-access prompt. A finished reply is not a successful read. Do not disable the sandbox. |
| No subagents appear | A small task may stay with the lead. Installation does not add a subagent API. |
| Output claims tests passed without evidence | Inspect the command output and the artifact. Missing proof is not PASS. |

To stop using this copy, deselect it and move
`<host-skills-dir>/agent-mission-control/` out of the discovery folder.
That does not change global model settings.

**Astra or extra models?** No. Keep your selected lead.
**Always spawn agents?** No. A specialist needs a useful bounded job; only
parallel jobs must be independent of each other's output.
**Tagged ZIPs?** [candidate.14](https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.14) has a skill ZIP and a Codex-plugin ZIP; check them against `SHA256SUMS.txt`. Claude Code uses the plugin marketplace above.
**Update?** [Checked update with a retained backup](hosts.md#update-an-existing-project-installation).

[How it works](how-it-works.md) · [Hosts](hosts.md) ·
[Report an experience](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml)
