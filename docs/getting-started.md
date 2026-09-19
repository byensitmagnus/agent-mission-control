# Get started with Agent Mission Control

[Install](#1-install-the-skill) · [Select](#2-select-the-installed-copy) ·
[First task](#3-try-a-small-first-task) · [Real work](task-guide.md) ·
[Troubleshooting](#troubleshooting)

You need a coding assistant with native Agent Skills and a project folder.
AMC is workflow instructions. Your existing account supplies models and tools.
No extra API key or server.

## 1. Install the skill

Install the **current `main` source**. That is the kernel this site describes.
The last tagged ZIP is [candidate.8](https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.8); it is an older runtime.

**Checked path** (Git and Python 3.11+). Clone this repository, then install
into an existing project:

```bash
git clone https://github.com/byensitmagnus/agent-mission-control.git
cd agent-mission-control
python scripts/install_skill.py --host claude-code --project "../my-app"
```

Replace `claude-code` with `codex`, `cursor`, `grok` or `kimi`. Details:
[hosts.md](hosts.md#install-the-current-source).

**Copy path** (no Python). Clone or download the default branch. Copy these
runtime files into the skill directory for your host, keeping the folder name
`agent-mission-control`:

`SKILL.md`, `LICENSE`, `references/`, `templates/`, `agents/`, `assets/`

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

Copy SKILL.md, LICENSE, references, templates, agents and assets into
.agents/skills/agent-mission-control/. Inspect first. Preserve any existing
installation or customizations; if one exists, show the difference before
replacing it. Do not change global settings, model defaults or permissions.
Confirm the installed SKILL.md path. Help me select that project copy,
especially if another skill has the same name.
```

[Version details](evidence.md#choose-a-version-deliberately).

## 2. Select the installed copy

Open the same project. Select `agent-mission-control` by path, not only by name:

- **Codex:** `/skills`, `$`, or the desktop picker
- **Claude Code:** `/agent-mission-control`
- **Cursor:** Customize → Skills, or `/` in chat
- **Grok:** `/agent-mission-control` after `grok inspect --json` from the project
- **Kimi:** `/skill:agent-mission-control` from the Git root

The path must end in `agent-mission-control/SKILL.md` **inside this project**.
A global or older copy with the same name is a different install. Restart the
client if a new folder does not appear. A file on disk is not proof the client
loaded it. If the skill loads but cannot read a file, fix that permission
before treating the first task as done.

## 3. Try a small first task

Start in a project that has `README.md`. Keep your current model and normal
permissions. Paste, using your host’s invocation if it is not `$agent-mission-control`:

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

**Done when:** the project copy was selected, each bullet is supported by the
README, no project files changed, and the answer says checks were not run.
Reading a README does not prove the application works.

## 4. Move on to your actual task

Use a [bug, feature, resume or research recipe](task-guide.md). Give the outcome
and what must stay working. The lead owns coordination. You do not assign a
team.

## Troubleshooting

| What you see | What to check |
|---|---|
| AMC is missing from the picker | Confirm `SKILL.md` is in this project’s host directory, not a doubled `agent-mission-control/agent-mission-control/` folder, then restart the client. |
| Two AMC entries appear | Select the project path. Global and project copies stay separate. |
| The agent cannot read the README | Resolve the host’s file-access prompt. A finished reply is not a successful read. Do not disable the sandbox. |
| No subagents appear | A small task may stay with the lead. Installation does not add a subagent API. |
| Output claims tests passed without evidence | Inspect the command output and the artifact. Missing proof is not PASS. |

To stop using this copy, deselect it and move
`<host-skills-dir>/agent-mission-control/` out of the discovery folder.
That does not change global model settings.

**Astra or extra models?** No. Keep your selected lead.
**Always spawn agents?** No. Direct work is the default. Sequential specialists are optional. Parallel fan-out needs independent jobs.
**Tagged plugin ZIP?** Last tag is candidate.8, an older runtime. Prefer current source.
**Update?** [Checked update with a retained backup](hosts.md#update-an-existing-project-installation).

[How it works](how-it-works.md) · [Hosts](hosts.md) ·
[Report an experience](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml)
