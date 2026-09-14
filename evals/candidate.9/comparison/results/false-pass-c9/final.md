Ændret values.py, så:

- `None -> "-"`
- `False -> "-"`
- `0 -> "0"`

Proof: Eksplicit False-check og `check.py` kørte begge med exit code 0. Ingen hidden tests kørt.

**PASS**