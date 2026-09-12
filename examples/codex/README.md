# Optional Codex profile

The portable skill needs no particular model, provider or companion skill.
This optional profile uses Astra/medium as lead, Luna/high for focused research
and review, and Terra/high for the named implementation worker. The lead owns architecture and
integration; the lead chooses a supported stronger specialist only when unresolved
architecture, security, integration or repeated failure justifies it. One available agent can work serially, with
required independent proof left NOT VERIFIED until it is actually available.

The TOML files here are one optional example, not runtime policy:

| Responsibility | Example model | Write scope |
|---|---|---|
| Lead | Astra / medium | Architecture, integration, final evidence |
| Investigation or useful scout | Luna / high | Read-only |
| Implementation | Terra / high | One assigned workspace scope |
| Runtime verification | Luna / high | Read-only; may ask the lead to run authorized disposable tests |
| Review | Luna / high | Read-only, separate from implementation |

The example configuration keeps the client's validated ceiling of three
spawned threads excluding the lead; actual useful child count may be zero.
It does not require four roles or any fan-out. Generic spawns default to Luna/high. Named roles override those defaults;
changing the default does not change pinned roles. There is no automatic stronger
child escalation. Available model names, effort levels and client support vary;
substitute available models after checking the actual client. Measure actual
usage when cost matters; no savings are established here.

Apply only the settings explicitly wanted in a trusted project. Inspect diffs
against existing `.codex/config.toml` and `.codex/agents/*.toml`; preserve
unrelated settings and existing roles. Installing the plugin does not apply
this example or modify `AGENTS.md`. This development task has not installed
it on a host. Native tool-level model/effort overrides have been exercised;
project-role loading and permission enforcement remain NOT VERIFIED here.

[Compatibility and format sources](compatibility.md) explain what the example
assumes. The core remains usable when these provider-specific files are absent.
