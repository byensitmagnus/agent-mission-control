# Optional Codex profile

The portable skill keeps the selected lead and needs no particular provider or
model. This opt-in example uses Sol/medium for scope, architecture, integration
and final evidence. Generic children use Luna/medium for narrow, repeatable jobs;
named roles use the capability and effort shown below. These are starting points
from current host guidance, not a benchmark-proven optimum.

| Responsibility | Example model | Scope |
|---|---|---|
| Lead | Sol / medium | Architecture, integration, final evidence |
| Investigation or useful scout | Terra / medium | Read-only, one bounded question |
| Implementation | Terra / medium | One assigned workspace scope |
| Runtime verification | Luna / medium | Narrow checks; lead can execute disposable builds |
| Material review | Terra / high | Read-only, separate from implementation |

Use Luna for a clear mechanical question, or a stronger supported model for a
specific unresolved risk. High effort is for difficult reasoning, not a blanket
setting on every cheap worker. Preserve a user's explicit model selection.
A single agent can work serially; required independent proof stays NOT VERIFIED
until supplied. The profile does not require all roles or an initial scout.

The example ceiling is three spawned threads excluding the lead; actual useful
child count may be zero. Named roles override generic defaults, so changing a
default does not change those pins. Check actual client/model/effort support
before applying the [TOML examples](compatibility.md). Model names and prices are
not stable portable interfaces. No cost savings are established by this profile.

Apply only wanted settings in a trusted project after comparing with existing
`.codex/config.toml` and `.codex/agents/*.toml`. Preserve unrelated settings and
roles. Installing the plugin does not apply this example or modify `AGENTS.md`.
No active/global configuration is changed by the builder. Native tool-level
model/effort overrides were exercised previously; automatic project-role loading
and permission enforcement remain NOT VERIFIED. Inspect the actual selected
model and permissions on a necessary real task before claiming activation.
