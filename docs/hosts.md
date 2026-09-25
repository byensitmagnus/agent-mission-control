# Use AMC in your coding assistant

First install: [getting started](getting-started.md), which also covers the
[Claude Code plugin](getting-started.md#1-install-the-skill). This page is the five-host
installer, update CLI, discovery limits and invocation notes.

AMC's workflow is an Agent Skill. Codex, Claude Code, Cursor, Grok and Kimi
have native skill loaders; the same AMC runtime files can be placed in their
project skill directories. This does not add a subagent API or process manager
to a client that lacks one. [Results and limits](evidence.md) separate filesystem
installation, native discovery and completed work.

## Install the current source

The commands in this section require the **current default branch**, Git and
Python 3.11+. Clone this repository, or check out the `v0.2.0-candidate.12` tag
for the latest tagged runtime; older tags carry older kernels.

```bash
git clone https://github.com/byensitmagnus/agent-mission-control.git
cd agent-mission-control
```

Alternatively, `npx skills add byensitmagnus/agent-mission-control` or the
[copy instructions](getting-started.md#1-install-the-skill) place the same
`skills/agent-mission-control/` folder in the directory for your host below.
Those routes need neither this clone nor Python; `--check` below can still
compare such a copy byte-for-byte. By default, the installer screens the
Git root and canonical origin. This is a provenance screen, not a signed-source
attestation. Use a clone for the default commands below.

From the AMC source checkout, choose one host and an existing target project:

```bash
python scripts/install_skill.py --host claude-code --project "../my-app"
python scripts/install_skill.py --host claude-code --project "../my-app" --check
```

The same commands work in PowerShell. Replace `claude-code` with `codex`,
`cursor`, `grok` or `kimi`. Keep the source checkout outside the target skill.
Install only for the host you intend to use; several hosts also discover one
another's directories, so installing five copies in one project is unnecessary.

Each destination below contains `agent-mission-control/SKILL.md`:

| Host flag | Project skill directory |
|---|---|
| `codex` | `.agents/skills/` |
| `claude-code` | `.claude/skills/` |
| `cursor` | `.cursor/skills/` |
| `grok` | `.grok/skills/` |
| `kimi` | `.kimi/skills/` |

Select the installed copy with the host's native command:

- **Codex:** use `/skills`, `$`, or the desktop skill picker; inspect the path.
- **Claude Code:** use `/agent-mission-control`; a same-named personal skill
  can take precedence over the project copy.
- **Cursor:** find AMC in Customize → Skills or type `/` and select it in chat.
- **Grok:** check `grok inspect --json` from the project, then invoke
  `/agent-mission-control`.
- **Kimi:** invoke `/skill:agent-mission-control`; check any configured skills
  directory override. Set `--project` to the Git repository root, because Kimi
  discovers project skills there when started in a repository subdirectory.

`INSTALLED` means the complete package was copied to the reported path.
`MATCH` from `--check` means its file names and bytes equal this source's runtime;
`DIFFERENT` lists missing, edited or extra files; `MISSING` means no installation
exists. Failed checks exit with code 1. A SHA-256 fingerprint identifies the
runtime contents; `builder_version` identifies the installer, not the version
of an arbitrary snapshot supplied through `--source` or a signed release.
Neither `INSTALLED` nor `MATCH` proves that your client loaded the skill:
`host_discovery` intentionally remains `NOT VERIFIED` in these filesystem results.

The default install preserves existing skills and refuses replacement, even when the
old files match. It changes no `AGENTS.md`, host configuration, model default or
permission. Linked paths and overlapping source/output are rejected. Copying
finishes and its bytes are checked before `SKILL.md` is published by rename.
If a final move fails, a partial directory may remain without `SKILL.md`; inspect
that exact directory before removing it and retrying. A second install will not
overwrite it. `--check` is read-only and does not launch a host or make a model call.

For a fork, downloaded source or independently inspected local snapshot, both
the installer and package builder accept `--source PATH`. That explicitly trusts
the selected source rather than requiring the canonical Git origin; structural,
path and copy checks still apply. Inspect the source before running its scripts.

```bash
python scripts/install_skill.py --host codex --project "../my-app" --source "." --check
```

Use the same `--source` for install, check and update. The returned runtime
digest identifies the actual bytes, including local edits.

## Update an existing project installation

Update from a trusted AMC source checkout after work using the old copy has
stopped. The source installer provides a separate, explicit update operation.
It does not change your selected model or host settings.

First inspect the existing installation against the new source:

```bash
python scripts/install_skill.py --host claude-code --project "../my-app" --check
```

`DIFFERENT` and exit code 1 mean the copies differ. Inspect the reported file
names and compare any customized files with the new source. Keep the returned
`installed_sha256`; it identifies the installation you just inspected. `MATCH`
means this source is already installed and no update is needed.

After reviewing the differences, use that exact digest:

```bash
python scripts/install_skill.py --host claude-code --project "../my-app" --update --expected-installed-sha256 "PASTE_INSTALLED_SHA256_HERE"
```

The installer verifies the new package before replacing the old copy. It refuses
a stale fingerprint if installed files changed after inspection. An update
activates the source as supplied; it does not silently merge local customizations.
The complete old directory is retained outside skill discovery, including your
custom files. The result reports `backup_path` and `previous_installed_sha256`.
Keep that backup until you have selected and checked the new copy in your host.
The same commands support all five host flags above.

On a handled activation failure, the installer restores the old copy when its
destination is free. If another owner occupies that destination, it preserves
both owners' data and reports where the backup remains. A killed process or
power loss can also leave the old copy in the backup directory: automatic
restart recovery is not provided.

For recovery, stop work using that copy and inspect the exact reported paths.
Preserve any current installation outside discovery before moving the retained
backup back to its original location; never overwrite another owner's directory.
Compare restored bytes with the old fingerprint. A byte match verifies recovery
of the files; select that copy in the host before resuming work.

## Confirm discovery before trusting a result

Open the target project in your assistant. Check the selected skill's **actual
path**, not only its displayed name. Personal skills can shadow project copies
in Claude Code; Codex can show multiple same-named entries; Kimi's configured
directories affect which copy wins. Restart the client if a newly added skill
is absent. A plugin's Codex manifest is not a universal plugin installer.

Then follow [confirm the selected copy](getting-started.md#3-confirm-the-selected-copy).
Use your host's invocation above in place of the example's `$agent-mission-control`.
Keep your current model and normal permissions. A loader listing is discovery
evidence. An explicit invocation or loaded-instruction record ties the selected
path to the task. A supported answer citing a file is task evidence only; it
does not identify which skill was loaded. None of these alone proves native
child-agent coordination.

## Resolve a Claude Code name conflict

Claude Code gives enterprise and personal skills precedence over a project
skill with the same name. `/agent-mission-control` therefore cannot select the
project copy while a higher-priority copy shadows it. This follows the official
[name resolution rules](https://code.claude.com/docs/en/skills#resolve-skills-that-share-a-name),
rechecked on 2026-09-24.

If the conflicting copy is your personal installation, stop sessions using it
and preserve its complete folder in a backup outside all skill discovery
directories. Moving it affects other projects, so an agent needs your explicit
approval for that personal-install change. Do not delete customizations or
rename only the folder: the declared skill name can still conflict. Start a
fresh session in the project, invoke AMC and inspect the loaded path. Retain
the backup so you can restore the personal copy later. Enterprise-managed
copies require the organization's owner; do not bypass their policy.

## Match the workflow to actual host capabilities

For a task that benefits from delegation, let the lead inspect the native tools
it actually has: create a child, receive its result, inspect status and stop it.
Use real exposed model choices and permissions. Do not substitute a guessed
command or assume that an unrelated executable named `agent` belongs to Cursor.
No provider-specific model profile is installed by AMC.

The lead owns integration and checks on every host. Assign exclusive write
scopes; use native worktree/isolation support where it is available and useful.
A shared working directory and a role description are not filesystem isolation.
Read-only reviewers inspect evidence; checks that write build/cache artifacts
belong with the authorized lead or an appropriately scoped verifier.

When resuming, match the recorded artifact with current files and confirm an old
writer has stopped before reassigning its scope. If native status is unavailable,
inspect read-only until ownership is resolved. Continue independent authorized
work; do not manufacture a new writer or ask the user to coordinate routine
handoffs. Required independent review remains unverified when the host cannot
provide it. Keep relevant evidence in the existing mission record; a small task
does not need a separate capability checklist.

These behaviors are already defined in AMC's
[routing](../skills/agent-mission-control/references/packets.md), [reconciliation](../skills/agent-mission-control/references/resume.md) and
[verification](../skills/agent-mission-control/references/verification.md) instructions. The host supplies the
runtime mechanisms. AMC does not implement a daemon or automatic recovery service.

## Sources and observed support

Directory and invocation mappings were checked on 2026-09-13 against
[OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills),
[Claude Code's skills guide](https://code.claude.com/docs/en/skills),
[Cursor's skills guide](https://cursor.com/docs/skills), and
[Kimi CLI's skills guide](https://moonshotai.github.io/kimi-cli/en/customization/skills.html).
Grok's mapping was checked against the installed Grok **1.0.3 (1a29d5bc12)**
`docs/user-guide/08-skills.md` and its `inspect --help` command. This is evidence
for that CLI build; the Grok model name alone does not identify a compatible host.

On 2026-09-23 the current [OpenAI skills guide](https://developers.openai.com/codex/skills)
still documents repository `.agents/skills`, and [Cursor's skills guide](https://cursor.com/docs/skills)
still documents project `.cursor/skills/` and `.agents/skills/`. Cursor also loads
`.claude/skills/` and `.codex/skills/` for compatibility. Claude Code's
[skills guide](https://code.claude.com/docs/en/skills) still documents project
`.claude/skills/`. That recheck did not rerun the five-host installer. Kimi and
Grok were not rechecked on that date.

See [the candidate.8 engineering record](engineering-candidate.8.md) for exact
checks, client observations and remaining limits. Local Windows checks do not
establish that a complete task works on macOS, Linux or every host/version.

The [2026-09-24 readiness observation](reviews/readiness-2026-09-24.md#native-task-observation)
ties the current project-installed runtime to an explicit Codex 0.156.1 skill
input and a completed reading task with one normal command approval. It records
the earlier setup failures; it does not establish desktop picker interaction or
automatic Windows sandbox access.

[Get started](getting-started.md) · [Task recipes](task-guide.md) ·
[Compare implementations](choosing.md)
