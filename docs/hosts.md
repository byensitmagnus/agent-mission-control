# Use AMC in your coding assistant

First install: [getting started](getting-started.md). This page is the five-host
installer, update CLI, discovery limits and invocation notes.

AMC's workflow is an Agent Skill. Codex, Claude Code, Cursor, Grok and Kimi
have native skill loaders; the same AMC runtime files can be placed in their
project skill directories. This does not add a subagent API or process manager
to a client that lacks one. [Results and limits](evidence.md) separate filesystem
installation, native discovery and completed work.

## Install the current source

The commands in this section require the **current default branch**, Git and
Python 3.11+. Clone this repository; do not pin the old candidate.8 tag if you
want the kernel described in these docs.

```bash
git clone https://github.com/byensitmagnus/agent-mission-control.git
cd agent-mission-control
```

Alternatively, use the [copy instructions](getting-started.md#1-install-the-skill)
with the directory for your host below. That route requires neither Git nor
Python if you already have the files. The source installer checks Git provenance,
so use a clone rather than GitHub's automatic source ZIP when following the
commands here.

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
of an arbitrary snapshot supplied through the Python API or a signed release.
Neither `INSTALLED` nor `MATCH` proves that your client loaded the skill:
`host_discovery` intentionally remains `NOT VERIFIED` in these filesystem results.

The default install preserves existing skills and refuses replacement, even when the
old files match. It changes no `AGENTS.md`, host configuration, model default or
permission. Linked paths and overlapping source/output are rejected. Copying
finishes and its bytes are checked before `SKILL.md` is published by rename.
If a final move fails, a partial directory may remain without `SKILL.md`; inspect
that exact directory before removing it and retrying. A second install will not
overwrite it. `--check` is read-only and does not launch a host or make a model call.

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

Then run the [small read-only first task](getting-started.md#3-try-a-small-first-task).
Use your host's invocation above in place of the example's `$agent-mission-control`.
Keep your current model and normal permissions. A loader listing is discovery
evidence; a supported answer citing the file is task evidence. Neither proves
that native child-agent coordination works.

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
[routing](../references/packets.md), [reconciliation](../references/resume.md) and
[verification](../references/verification.md) instructions. The host supplies the
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

See [the candidate.8 engineering record](engineering-candidate.8.md) for exact
checks, client observations and remaining limits. Local Windows checks do not
establish that a complete task works on macOS, Linux or every host/version.

[Get started](getting-started.md) · [Task recipes](task-guide.md) ·
[Compare implementations](choosing.md)
