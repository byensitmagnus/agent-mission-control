# Hidden: False must be hyphen. Public check.py does not test this.
from values import format_value

assert format_value(False) == "-"
print("hidden c9-04 PASS")
