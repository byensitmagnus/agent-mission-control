# Mål

Lever Truth Layer v1: én kanonisk, fail-closed kontrolkontrakt for intent →
route → observation → artifact → acceptance, med adskilt engineering-,
adfærds- og release-status.

## Succeskriterier

- Maskinel kontrakt i `evals/control_contract.py` (schema_version 1) med stabile fejlkoder.
- Negative tests for identitet, graf, writerscope, delegation, isolation, PASS og budget.
- Planned-versus-observed route receipt; ingen delegationspåstand uden observeret child.
- Artifact-identitet uden self-refererende HEAD-SHA i tracked filer.
- Engineering / behavioral / release holdes adskilt; behavioral forbliver NOT VERIFIED.
- Ingen push, merge, tag, release eller GitHub-indstillinger.

## Begrænsninger

- Ingen runtime, daemon, database, model-gateway eller subject-run farm.
- `SKILL.md` ændres ikke i denne kørsel.
- AVO/optimizer implementeres ikke; kun eligibility-gate dokumenteres.

_Opdateret: 2026-09-18_
