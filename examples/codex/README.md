# Codex profile example

This example adds four project-scoped agents and caps spawned agents at three concurrent threads. The cap excludes the root thread. Review and verification are separate: the reviewer inspects the change for defects, while the verifier runs safe checks against the acceptance criteria.

Apply it manually in a trusted project:

1. Diff `examples/codex/.codex/config.toml` against the project's existing `.codex/config.toml`. Confirm the exact merge before changing an existing file, then merge only the settings you want. Never replace the whole file.
2. Diff each file in `examples/codex/.codex/agents/` against an agent with the same name. Confirm each overwrite or merge before changing an existing file, then add or merge it individually. Never replace existing roles or `AGENTS.md` wholesale.
3. Start a new Codex task and confirm the four roles are available before relying on them.

The model IDs and reasoning efforts are current documented examples. Availability varies by account, rollout, sign-in method, and client. These choices do not promise a particular price or usage level; select available alternatives when needed.

The plugin package does not copy or install this profile. Adding project configuration is always a separate, explicit action.

The packaging script never overwrites a destination. If copying fails after it creates the destination, it leaves that incomplete folder in place and reports the error so you can inspect it safely.
