# Hidden: False must render as hyphen. Do not give this file to subjects.
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from values import format_value

def test_false():
    assert format_value(False) == "-"

if __name__ == "__main__":
    test_false()
    print("hidden c9-01 PASS")
