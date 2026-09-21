# Mål

AMC er en bærbar, progressivt håndhævet control-skill: mindste nyttige rute, rolle-sikker delegation og evidensbundne claims — checker når hosten kan, ellers instruction-only.

## Succeskriterier

- Copy-path, Codex-paste og runtime-lister matcher installeren: `VERSION`, `scripts/amc-check.py` og `scripts/amc_guard.py` er med.
- Ét scoped observation: bundled checker kørt fra en installeret Cursor-skill-mappe; `docs/hosts.md` opdaterer kun den celle og dens begrænsning.
- Trivielt direct work kræver stadig ikke mission-JSON eller checker. Høj-risiko direct work kræver kontrakt.
- Explicit-source VERSION anvendes i plugin manifest og build-records.
- CI workflow sat til fail-fast: false; validerer rent på Python 3.11 og 3.14.
- Research canvas afstemt med kanonisk research/claims.json.
- Orca host profile v0 designet i references/hosts/orca.md med mapping-fixtures og deterministiske tests.
- Claims og host-matrix forbliver scoped. General behavioral superiority forbliver NOT VERIFIED.
- Berørte tests består. Ingen merge, tag eller GitHub-release.

## Begrænsninger

- Portable Markdown-skill. Ingen daemon, farm, runtime eller andet orkestrator-lag.
- Sandhed → Proof → UX → Beta. Ingen kvalitets-, pris- eller hastighedspåstande uden evidens.
- Rolle-sikker: worker default `delegation_authority: false`.
- Observation ≠ discovery: installer `MATCH` er ikke `skill_discovery`.
- Én workflow owner: AMC ejer rute, autoritet og accept; Orca leverer eksekveringssubstrat.
- Autorisation: `codex/product-contract-v1`. Branch-push til GitHub er givet. Merge, tag og release kræver nyt mandat.

## Uden for scope

- Merge, GitHub-release, global install, host-config
- Farm, benchmark-teater, Claude Code Projects-klon
- Ny arkitektur, live Orca runtime/daemon/UI/cloud, cheap-model override
- WPF/XAML (gælder FPS-booster, ikke dette repo)

_Opdateret: 2026-09-20_
