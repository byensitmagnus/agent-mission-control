# Codex compatibility

Verified against official OpenAI documentation and source on 2026-09-11.

- Skills use progressive disclosure: Codex initially loads the name, description, and path, then reads the full `SKILL.md` when selected. Keep the description short and put detailed workflow material in the skill body and references. Source: <https://developers.openai.com/codex/skills>
- A plugin manifest lives at `.codex-plugin/plugin.json`. The documented skill layout is `skills/<skill-name>/SKILL.md`, referenced by `"skills": "./skills/"`. Source: <https://github.com/openai/skills/blob/main/skills/.system/plugin-creator/references/plugin-json-spec.md>
- Project overrides live in trusted-project `.codex/config.toml`. Project custom agents live in `.codex/agents/*.toml` and require `name`, `description`, and `developer_instructions`; normal config keys such as `model`, `model_reasoning_effort`, and `sandbox_mode` are supported. Sources: <https://developers.openai.com/codex/config-reference> and <https://developers.openai.com/codex/subagents>
- The downloadable current config schema is <https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/config.schema.json>.
- Current public Codex model IDs include `gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`, and `gpt-5.6-luna`. Model and effort availability varies by account, rollout, sign-in method, and client; there is no universal per-model effort guarantee. Source: <https://developers.openai.com/codex/models>
- Plugins distribute skills and may bundle MCP servers, browser extensions, and hooks. Official documentation does not establish that installing a plugin copies project `.codex/config.toml` or `.codex/agents/*.toml`; this package therefore exposes the Codex profile only as a manual example. Source: <https://developers.openai.com/codex/plugins>

`agents/openai.yaml` is skill UI metadata, not a custom-agent declaration. The profile example keeps research and review read-only, and keeps implementation in a separate workspace-write role.
