Opdateret `parse_total` til at:

- summere heltal
- ignorere blanke linjer
- ignorere linjer, der efter whitespace starter med `#`

Kørte:

- Offentlig happy-path-check: PASS
- Egen check med blanke linjer og kommentarer: PASS
- Ingen hidden tests kørt

PASS