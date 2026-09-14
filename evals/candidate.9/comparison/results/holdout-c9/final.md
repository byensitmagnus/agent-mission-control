Opdateret parse.py:

- Summerer heltal.
- Springer tomme og whitespace-only linjer over.
- Springer linjer, der starter med `#`, over.

Kørt kontrol dækkede happy path, blanke linjer, whitespace-linjer og kommentarer. Resultat: `public + blank + comment checks PASS`.

Ingen hidden tests kørt.

PASS