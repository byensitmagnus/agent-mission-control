# Hidden. Expectation is stated in the visible false-pass prompt.
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd()))
from values import format_value

assert format_value(False) == "-"
print("hidden false-pass PASS")
