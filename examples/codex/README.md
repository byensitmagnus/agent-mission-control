# Optional Codex profile

The portable skill needs no particular model, provider or companion skill.
Choose capabilities first: a strong lead owns architecture and integration;
focused workers handle bounded work; escalate when uncertainty or risk demands
it. One available agent can work serially, with required independent proof
left NOT VERIFIED until it is actually available.

The TOML files here are one optional example, not runtime policy:

| Responsibility | Example model | Write scope |
|---|---|---|
| Lead | Astra | Architecture, integration, final evidence |
| Investigation | Luna | Read-only |
| Implementation | Terra | One assigned workspace scope |
| Runtime verification | Terra | Read-only; authorized disposable test outputs as needed |
| Review | Sol | Read-only, separate from implementation |

The example caps subagents at three concurrent threads. It does not require
four roles or any fan-out. Available model names, effort levels and client
support vary; substitute available models after checking the actual client.
Measure actual usage when cost matters; no savings are established here.

Apply only the settings explicitly wanted in a trusted project. Inspect diffs
against existing `.codex/config.toml` and `.codex/agents/*.toml`; preserve
unrelated settings and existing roles. Installing the plugin does not apply
this example or modify `AGENTS.md`. This development task has not installed
it on a host or verified live discovery.

[Compatibility and format sources](compatibility.md) explain what the example
assumes. The core remains usable when these provider-specific files are absent.
