# Get started with Agent Mission Control

You need Codex with access to the project you want to work on. AMC supplies the
workflow instructions; your existing Codex account supplies models and tools.
The skill does not need its own API key or a separate server.

## 1. Install the skill

The simplest package is
[agent-mission-control-skill.zip](https://github.com/byensitmagnus/agent-mission-control/releases/download/v0.2.0-candidate.4/agent-mission-control-skill.zip)
from the [candidate release](https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.4).
Choose that asset rather than GitHub's automatic “Source code” download.

**Let Codex handle the files.** Open your intended project and paste:

```text
Install Agent Mission Control v0.2.0-candidate.4 in this project only.

Use the skill ZIP and SHA256SUMS.txt from:
https://github.com/byensitmagnus/agent-mission-control/releases/tag/v0.2.0-candidate.4

Check the ZIP against the listed SHA-256 checksum. Extract the
agent-mission-control folder into .agents/skills/ in this project.
Inspect the package first. Preserve any existing installation or customizations;
if one exists, show the difference before replacing it.
Do not change global settings, model defaults or permissions.
Confirm the installed SKILL.md path. Help me select that project copy,
especially if another skill has the same name.
```

Alternatively, download and unzip the asset yourself. Move its
`agent-mission-control` folder into `.agents/skills/` inside your project.
The final path must be:

```text
your-project/
  .agents/
    skills/
      agent-mission-control/
        SKILL.md
        references/
        templates/
        agents/
        assets/
        LICENSE
```

The dot-prefixed `.agents` folder may be hidden in your file manager. Keep all
the packaged folders together; copying only `SKILL.md` breaks its references.
[OpenAI documents this project-scoped skill location](https://learn.chatgpt.com/docs/build-skills).

## 2. Select the installed copy

Open the intended project in Codex. In the CLI or IDE extension, use
`/skills` or type `$` to find `agent-mission-control`. In the desktop
client, use its skill picker. Select the copy whose path is inside **this
project**, ending in `.agents/skills/agent-mission-control/SKILL.md`.

**Already have AMC installed elsewhere?** Two skills can have the same name.
Codex does not merge them. Check the path before selecting: a global or older
copy is not proof that this project's package was loaded.

If the project copy does not appear, check for a doubled folder such as
`agent-mission-control/agent-mission-control/SKILL.md`, then restart Codex.
A file existing on disk is only the installation check; finding and selecting
it in the client is the discovery check.
If the skill loads but Codex cannot read a file, that is a separate permissions
problem. Keep the task unfinished until reading works; do not treat a completed
agent response as a successful check.
[OpenAI's current skill guide](https://learn.chatgpt.com/docs/build-skills)
explains discovery and invocation.

## 3. Try a small first task

Start in a project that has a `README.md`. Use your current model and normal
permissions; this first task only reads a file. With the project copy of AMC
selected, paste:

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

You should receive a short answer with references you can open. Compare it
with the README: are the purpose, example and limitation actually supported?
The answer should say that project checks were **not run**. Reading a README
does not establish that an application works or is ready to release.

For example, in AMC's own repository the answer can explain that AMC is a
Codex orchestration skill, name feature work as an example, and note that
host capabilities vary. This is an illustration of the expected content,
not a prescribed answer for your project.

**Finished:** the project skill was selected, the answer matches the README,
and no project files changed. No extra agent or paid model comparison is needed.
[See the dated installation check and its host limits](../examples/codex/compatibility.md#2026-09-13-standalone-skill-first-use-check).

## 4. Move on to your actual task

Once the small task works, give AMC a bug, feature or investigation you already
need. For a larger release task, you can use:

```text
$agent-mission-control

Prepare this app for release.
Preserve user data and existing features.
Use independent help where useful, fix confirmed problems,
and show the checks and any remaining blockers. Stop before deployment.
```

Expect a clear objective, a useful route, relevant changes or findings, and
checks you can inspect. On longer work, expect a progress record that can be
resumed. You do not need to ask for AVO, Context Diamond and learning separately.

## Common questions

**Do I need Astra or several models?** No. Keep your selected lead. AMC uses
available capabilities; additional agents and models are optional. The
[Sol/Terra/Luna example](../examples/codex/README.md) is an editable advanced
profile, not something installed with the skill.

**Will it always create agents?** No. Delegation must add useful independent work.
If native subagents are unavailable, work can stay with the lead; required
independent review must be reported as unavailable.

**Will it deploy, buy services or rewrite its own rules?** Installing the skill
does not grant permissions. Your request and the host's permission controls
remain authoritative. Learning proposals are separate from the active run.

**Can I use the plugin instead?** The release includes
`agent-mission-control-plugin.zip` with the same skill. Plugin distribution
requires a marketplace/install route supported by your client; this repository
is not a published universal-directory listing. See
[OpenAI's current plugin build guide](https://learn.chatgpt.com/docs/build-plugins)
and [plugin examples](https://github.com/openai/plugins).
Use the skill package if you want the simpler project-local route.

**What if Windows blocks the README reader?** If Codex reports
`apply deny-read ACLs`, the local sandbox could not start the reader. Inspect
and approve only the requested read of your README if your client offers normal
per-command approval. Do not disable the sandbox or grant a permanent blanket
permission. If reading remains unavailable, the first task is not complete.

**How do I update or remove it?** Compare a new version in a separate folder,
preserve local edits, then replace only the confirmed project installation.
Remove that same installation folder to uninstall, after saving any changes.
Neither action requires changing your global Codex configuration.

[See the workflow scenarios](how-it-works.md) · [Explore the sources](sources.md) ·
[Report an experience](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml)
