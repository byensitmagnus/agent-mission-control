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
Confirm the installed SKILL.md path and explain how I can select the skill.
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

## 2. Select it

Open the intended project in Codex. Select the skill in the skill picker or
mention `$agent-mission-control` in your request. If it does not appear,
restart Codex and check that the folder is not nested twice.

Discovery controls can differ between the desktop app, CLI and IDE extension.
The package is validated; each client's discovery behavior still depends on its
version and configuration.

## 3. Give it a real task

```text
$agent-mission-control

Prepare this app for release.
Preserve user data and existing features.
Use independent help where useful, fix confirmed problems,
and show the checks and any remaining blockers. Stop before deployment.
```

You can also start much smaller: fix a bug, complete a feature, or investigate
why a test fails. AMC is intended to keep simple work simple.

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
[OpenAI's plugin guide](https://developers.openai.com/codex/plugins).
Use the skill package if you want the simpler project-local route.

**How do I update or remove it?** Compare a new version in a separate folder,
preserve local edits, then replace only the confirmed project installation.
Remove that same installation folder to uninstall, after saving any changes.
Neither action requires changing your global Codex configuration.

[See the workflow scenarios](how-it-works.md) · [Explore the sources](sources.md) ·
[Report an experience](https://github.com/byensitmagnus/agent-mission-control/issues/new?template=experience.yml)
