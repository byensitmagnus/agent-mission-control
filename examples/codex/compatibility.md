# Codex format and compatibility notes

The core skill has no Codex configuration dependency. These are references
for the optional profile and package format, not a host compatibility matrix.

- [Skills](https://developers.openai.com/codex/skills) use name/description
  discovery followed by loading the skill and relevant references.
- The installed OpenAI plugin-creator specification on 2026-09-11 describes
  `.codex-plugin/plugin.json`, a `skills/<name>/SKILL.md` tree and
  `"skills": "./skills/"`. The generated plugin is also checked with its
  official local validator; host installation is a separate unverified gate.
  [Specification source](https://github.com/openai/skills/blob/main/skills/.system/plugin-creator/references/plugin-json-spec.md).
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
