# Optional host intent profiles

These are examples of how a host may map AMC capability classes. They are not
AMC's identity, not a required model pairing, and not evidence that one graph is
cheaper or better. Validator rules stay format and sandbox limits; they do not
require named models.

Apply a profile only when the user asks, or when the host already exposes the
mapping. Keep the selected lead. See the cost-aware preflight in
[resources](../references/resources.md#cost-aware-delegation) before any fan-out.

| Profile | Intent | Typical graph |
|---|---|---|
| `quality` | Prefer correctness over calendar time | More work stays with the lead. Review when the claim is material. Concurrency 1 unless the user asked for isolated independent jobs. |
| `balanced` | Current AMC default | Direct for sequential work. Sequential specialists only for bounded isolation. Parallel cheaper workers only for independent jobs with host isolation and compact artifacts. Review by risk, not by habit. |
| `throughput` | Prefer verifiable capacity inside the budget | More fan-out on ready independent jobs, still under the worker/retry/reviewer ceilings. Isolation and artifact handoff remain required. Review is still not automatic. |

Example class mappings the host may already provide. Substitute what the host
actually exposes; do not invent IDs.

| Class | Optional examples |
|---|---|
| Lead-capable | Astra, Sol, Opus, Fable, or the user's selected lead |
| Focused / cheap worker | Luna, Sonnet, Thea, or the host default child |
| Material reviewer | A strong available model, only when risk warrants it |

The [optional Codex TOML](codex/README.md) is one possible `balanced` mapping
(Sol lead, Luna generic children, ceiling 3). It does not freeze those names
into AMC and it does not prove savings.

Do not install three parallel TOML trees. Do not treat concurrency as a target.
Do not activate reviewer-by-default in `throughput`.
