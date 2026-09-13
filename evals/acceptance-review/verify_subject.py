"""Controller check for the frozen release-evidence contract; no subject repairs."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
root = Path(sys.argv[1]).resolve()
fixture = Path(__file__).parent / "fixture"
spec = importlib.util.spec_from_file_location("subject_gate", root / "release_gate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def row(name="a", **updates):
    return {"name": name, "status": "PASS", "assertions": [True], **updates}


cases = [
    ("complete", ["a"], [row()], True),
    ("reordered", ["a", "b"], [row("b"), row()], True),
    ("metadata", ["a"], [row(extra={"keep": 0})], True),
    ("empty required", [], [], False),
    ("missing required", None, [row()], False),
    ("empty name", [""], [row("")], False),
    ("duplicate required", ["a", "a"], [row(), row()], False),
    ("empty results", ["a"], [], False),
    ("missing case", ["a", "b"], [row()], False),
    ("extra case", ["a"], [row(), row("b")], False),
    ("duplicate result", ["a", "b"], [row(), row()], False),
    ("wrong case", ["a"], [row("b")], False),
    ("unhashable name", ["a"], [row([])], False),
    ("missing assertions", ["a"], [{"name": "a", "status": "PASS"}], False),
    ("empty assertions", ["a"], [row(assertions=[])], False),
    ("integer assertion", ["a"], [row(assertions=[1])], False),
    ("failed assertion", ["a"], [row(assertions=[True, False])], False),
    ("failed row", ["a"], [row(status="FAIL")], False),
    ("malformed row", ["a"], [None], False),
]
observed = []
for name, required, results, expected in cases:
    before = copy.deepcopy((required, results))
    actual = module.release_ready(required, results)
    assert actual is expected, (name, expected, actual)
    assert (required, results) == before, (name, "input mutation")
    observed.append(name)
for name in ("MISSION.md", "check.py"):
    assert (root / name).read_bytes() == (fixture / name).read_bytes(), name
print(json.dumps({"status": "PASS", "cases": len(observed), "inputPreservation": True,
                  "scopeFilesPreserved": True, "sourceSha256": hashlib.sha256(
                      (root / "release_gate.py").read_bytes()).hexdigest()}))
