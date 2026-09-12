from src.reporting.export import export_row
from src.reporting.format import format_value


assert format_value(0) == "0"
assert format_value(-2) == "-2"
assert format_value(None) == "-"
assert export_row([0, 3, None]) == "0,3,-"
print("PASS")
