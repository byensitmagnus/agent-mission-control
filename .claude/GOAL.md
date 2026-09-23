# Mål

Få den færdige kerne på `main`: tre ruter, tjek af den fil brugeren kører, og en første nyttig opgave. Ingen ny runtime.

## Succeskriterier

- PR #10 er merget til `main`.
- En Cursor-projektinstall af den merget kilde er `MATCH`.
- `python3 scripts/validate.py` og `python3 scripts/test_package_plugin.py` er grønne på den commit.
- Kvalitet, pris og hastighed forbliver NOT VERIFIED.

## Begrænsninger

- Portabel Markdown-skill. Værten ejer agenter, værktøjer og isolation.
- Ingen release, tagged ZIP, daemon eller checker-runtime.
- PR #8’s JSON-kontrakt og PR #9’s Orca-CLI følger ikke med.

## Uden for scope

- At bevise at AMC er hurtigere, billigere eller bedre.
- At Cursor 3.20.21’s skill-vælger kan køres headless. Den CLI viser `agent`, men parseren kører kun `tunnel`.

_Opdateret: 2026-09-23_
