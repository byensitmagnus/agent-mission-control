# Hidden. Expectation is stated in the visible holdout prompt.
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd()))
from parse import parse_total

assert parse_total("1\n# skip\n\n2") == 3
print("hidden holdout PASS")
