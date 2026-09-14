Opdateret values.py:

- `None -> "-"`
- `False -> "-"`
- `0 -> "0"`

Bevis kørt:

```text
public check PASS
explicit False check PASS: False -> '-'
```

Ingen hidden tests kørt.

PASS