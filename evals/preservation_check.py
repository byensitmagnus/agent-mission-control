#!/usr/bin/env python3
"""Development diagnostic for a trusted local summarize implementation.

Compare supported builtin examples with the unchanged v3 baseline. This is not
a frozen v3 score, a held-out test, or proof for arbitrary Python objects.
Candidate code executes locally: only supply a trusted source file.
"""

import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import runpy


BASELINE = Path(__file__).parent / "v3/fixtures/v3-04-optimization/analytics/events.py"
NAMES = ("x", "y", "", None, False, 0, 1, ["x"], {"x": [1]}, ("x",))
CASES = [[]]
for size in (1, 2):
    for names in product(NAMES, repeat=size):
        CASES.append([
            {"name": name, "metadata": {"first": index, "nested": [False, 0]}}
            for index, name in enumerate(names)
        ])
CASES.extend([
    [{"name": "x", "metadata": value}, {"name": "y"}, {"name": "x", "metadata": 99}]
    for value in (None, False, 0, "", [], {})
])
REFERENCE = runpy.run_path(str(BASELINE))["summarize"]


def compare(candidate):
    failures = []
    for index, events in enumerate(CASES):
        expected = REFERENCE(deepcopy(events))
        supplied = deepcopy(events)
        before = repr(supplied)
        try:
            actual = candidate(supplied)
            # Builtin corpus only: repr also distinguishes False/0 and container types.
            if actual != expected or repr(actual) != repr(expected):
                failures.append({"case": index, "reason": "output differs from baseline"})
        except Exception as error:
            failures.append({"case": index, "reason": type(error).__name__})
        if repr(supplied) != before:
            failures.append({"case": index, "reason": "input mutated"})
    return {"verdict": "FAIL" if failures else "PASS", "cases": len(CASES), "failures": failures}


def self_check():
    def hash_only(events):
        rows = {}
        for event in events:
            name = event["name"]
            if name in rows:
                rows[name]["count"] += 1
            else:
                rows[name] = {"name": name, "count": 1, "metadata": event.get("metadata")}
        return list(rows.values())

    def lossy(events):
        result = REFERENCE(events)
        for row in result:
            row["metadata"] = row["metadata"] or None
        return result

    def mutating(events):
        result = REFERENCE(events)
        events.clear()
        return result

    controls = {"baseline": REFERENCE, "hash_only": hash_only, "lossy_metadata": lossy,
                "mutating": mutating, "reordered": lambda events: list(reversed(REFERENCE(events)))}
    results = {name: compare(function)["verdict"] for name, function in controls.items()}
    passed = results == {name: "PASS" if name == "baseline" else "FAIL" for name in controls}
    return {"verdict": "PASS" if passed else "FAIL", "cases": len(CASES), "controls": results}


def identity(path):
    return {"file": path.name, "sha256": sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--candidate", type=Path)
    mode.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        result = self_check()
    else:
        result = compare(runpy.run_path(str(args.candidate))["summarize"])
        result["candidate"] = identity(args.candidate)
    result.update(evaluator=identity(Path(__file__)), baseline=identity(BASELINE),
                  scope="development diagnostic; builtin corpus; not frozen v3 or held-out evidence")
    print(json.dumps(result, indent=2))
    return int(result["verdict"] != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
