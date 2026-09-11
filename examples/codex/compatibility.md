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
