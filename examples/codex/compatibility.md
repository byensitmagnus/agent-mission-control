# Codex format and compatibility notes

The core skill has no Codex configuration dependency. These are references
for the optional profile and package format, not a host compatibility matrix.

- [Skills](https://developers.openai.com/codex/skills) use name/description
  discovery followed by loading the skill and relevant references.
- The installed OpenAI plugin-creator specification on 2026-09-11 describes
  `.codex-plugin/plugin.json`, a `skills/<name>/SKILL.md` tree and
  `"skills": "./skills/"`. The generated plugin is also checked with its
  official local validator during manual package acceptance; this is not a CI
  or host-installation claim. Plugin installation remains unverified; the
  standalone skill has the dated discovery/invocation check below.
  The former [OpenAI skills catalog](https://github.com/openai/skills) is now
  deprecated; use the [current build guide](https://learn.chatgpt.com/docs/build-plugins)
  and [OpenAI plugin examples](https://github.com/openai/plugins) for new work.
- [Project configuration](https://developers.openai.com/codex/config-reference)
  and [custom agents](https://developers.openai.com/codex/subagents) describe
  `.codex/config.toml` and `.codex/agents/*.toml`. Confirm supported keys in
  the actual client before applying the profile.
- `agents/openai.yaml` supplies skill UI metadata; it is not a custom-agent
  declaration. [Models](https://developers.openai.com/codex/models) and effort
  availability are environment-dependent.
- [Plugins](https://developers.openai.com/codex/plugins) distribute components.
  This builder deliberately excludes project configuration and custom agents.

Structural validation checks the supplied example; it does not prove that a
host loaded its models, permissions, roles or concurrency settings.

## 2026-09-12 source check

Current official documentation describes trusted project role discovery from
`.codex/agents/*.toml`, where `name` identifies the role. Project config is ignored
for untrusted projects. Generic `agents.default_subagent_model` and
`agents.default_subagent_reasoning_effort` defaults are independent of root;
explicit role fields override defaults. The example uses documented `medium`
and `high`, not a guessed `max` TOML value. The current app tool also exposes
additional effort values; tool availability does not establish config syntax.

`max_concurrent_threads_per_session` caps spawned threads, excluding primary.
It grants neither exclusive file ownership nor separate worktrees. Research and
review roles are read-only, while the worker permits workspace writes. Requested
scope remains separate from enforced permissions. No global config or AGENTS
file is written by these examples or by the package builder.

A local CLI 0.153.3 prompt-renderer probe left global config unchanged, but did
not expose custom-role markers or reject the invalid project-effort control.
Therefore project-role loading and enforcement remain NOT VERIFIED. This is not
evidence that the profile is active. The source validator tests the example's
shape, not execution. Keep it opt-in until a real host run verifies the settings.


## 2026-09-13 profile guidance update

[Current subagent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents)
supports separate model/effort choices: Luna for narrow repeatable work, Terra for
bounded exploration, and stronger models for ambiguous multi-step work; medium is
a balanced effort, while high serves complex logic and review. The example now
uses Sol/medium lead, Luna/medium generic children, Terra/medium research and
implementation, Terra/high review and Luna/medium verification. The source
validator accepts the supported model set rather than forcing Astra. This checks
the example's structure, not host activation or comparative model quality.


## 2026-09-13 standalone skill first-use check

The published `v0.2.0-candidate.4` skill ZIP was extracted into a new Git
project at `.agents/skills/agent-mission-control/`. Codex CLI 0.153.3 on
Windows returned that exact path from `skills/list`, enabled with repo scope.
A pre-existing user skill had the same name; it remained separate. The test
selected the project copy explicitly through the app-server skill input.

Three bounded Luna/low invocations exercised the README first task:

| Attempt | Result | Adjustment |
|---|---|---|
| Initial read | NOT VERIFIED: Windows sandbox process startup failed with `apply deny-read ACLs`. The agent did not claim to have read the file. | Permit a normal, one-command approval for the README reader. |
| Approved read | File reading worked, but the answer gave incorrect line numbers. | Ask for section headings instead of guessed line numbers. |
| Final task | PASS: three supported points, correct section headings, no project checks claimed and no file changes. | No further model runs. |

The final run kept read-only sandbox configuration and used one normal approval
for `Get-Content -LiteralPath 'README.md'` in the disposable project.
No persistent approval or global configuration change was made. This verifies
discovery and the bounded task on this host **with that approval**; it does not
certify unassisted Windows sandbox startup, desktop/IDE UI discovery, plugin
installation, custom-agent roles or general model quality.

The test README came from AMC commit
`86382362ba7c0baf0260832e5476a925694a35b2`.
The final response's headings and claims were checked against that file.
[Sanitized results and usage counters](../../evals/results/2026-09-13-first-use.json).
[App-server skill selection](https://learn.chatgpt.com/docs/app-server#skills).
