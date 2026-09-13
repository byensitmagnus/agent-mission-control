#!/usr/bin/env python3
"""Bounded public replays for two sanitized FPS Booster regressions.

Candidate C# is trusted input and executes unsandboxed in a temporary evaluator directory.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "scripts"))
from prepare_eval import reject_linked_ancestors

FIXTURES = ROOT / "fps-fixtures"
TIMEOUT = 45
SCORED = {"json": ["Classifier.cs"], "encoding": ["release.ps1"]}
JSON_EXPECTED = {
    "zero": "APPLIED", "positive": "FAIL", "negative": "FAIL", "decimal": "FAIL",
    "fraction": "FAIL", "overflow": "FAIL", "string": "FAIL", "null": "FAIL",
    "boolean": "FAIL", "object": "FAIL", "array": "FAIL", "missing": "FAIL",
    "badStatus": "FAIL", "numberStatus": "FAIL", "nullStatus": "FAIL",
    "missingStatus": "FAIL", "rootArray": "FAIL", "malformed": "FAIL",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture_files(case: str) -> dict[str, str]:
    source = FIXTURES / case
    return {p.relative_to(source).as_posix(): digest(p) for p in source.rglob("*") if p.is_file()}


def fixture_scored_bytes(case: str) -> dict[str, str]:
    source = FIXTURES / case
    return {name: base64.b64encode((source / name).read_bytes()).decode("ascii") for name in SCORED[case]}


def manifest_path(destination: Path) -> Path:
    return destination.parent / ("." + destination.name + ".fps-replay-manifest.json")


def emit(payload: dict) -> None:
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def prepare(case: str, destination: Path) -> int:
    source = FIXTURES / case
    try:
        reject_linked_ancestors(destination, "destination or ancestor")
        reject_linked_ancestors(manifest_path(destination), "manifest or ancestor")
    except ValueError:
        emit({"case": case, "status": "REFUSED", "reason": "linked-output-path"})
        return 2
    destination = destination.resolve()
    manifest = manifest_path(destination)
    if destination.exists() or manifest.exists():
        emit({"case": case, "status": "REFUSED", "reason": "destination-or-manifest-exists"})
        return 2
    shutil.copytree(source, destination)
    manifest.write_text(json.dumps({"case": case, "destination": str(destination), "files": fixture_files(case), "scored_bytes": fixture_scored_bytes(case)}, sort_keys=True), encoding="utf-8")
    emit({"case": case, "status": "PREPARED", "manifest": str(manifest)})
    return 0


def load_manifest(destination: Path) -> tuple[dict | None, str | None]:
    path = manifest_path(destination.resolve())
    if not path.is_file():
        return None, "manifest-missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "manifest-invalid"
    if not isinstance(data, dict):
        return None, "manifest-invalid"
    case = data.get("case")
    if not isinstance(case, str) or case not in SCORED or data.get("destination") != str(destination.resolve()):
        return None, "manifest-binding-invalid"
    if data.get("files") != fixture_files(case) or data.get("scored_bytes") != fixture_scored_bytes(case):
        return None, "manifest-fixture-binding-invalid"
    return data, None


def preserved(destination: Path, manifest: dict) -> list[str]:
    changed = []
    allowed = set(SCORED[manifest["case"]])
    for name, expected in manifest["files"].items():
        if name in allowed:
            continue
        path = destination / name
        if not path.is_file() or digest(path) != expected:
            changed.append(name)
    return changed


PROGRAM = r'''using System;
using System.Collections.Generic;
using System.Text.Json;
var cases = new Dictionary<string, string> {
    ["zero"] = "{\"status\":\"ok\",\"failedCount\":0}",
    ["positive"] = "{\"status\":\"ok\",\"failedCount\":1}",
    ["negative"] = "{\"status\":\"ok\",\"failedCount\":-1}",
    ["decimal"] = "{\"status\":\"ok\",\"failedCount\":0.0}",
    ["fraction"] = "{\"status\":\"ok\",\"failedCount\":0.5}",
    ["overflow"] = "{\"status\":\"ok\",\"failedCount\":2147483648}",
    ["string"] = "{\"status\":\"ok\",\"failedCount\":\"0\"}",
    ["null"] = "{\"status\":\"ok\",\"failedCount\":null}",
    ["boolean"] = "{\"status\":\"ok\",\"failedCount\":false}",
    ["object"] = "{\"status\":\"ok\",\"failedCount\":{}}",
    ["array"] = "{\"status\":\"ok\",\"failedCount\":[]}",
    ["missing"] = "{\"status\":\"ok\"}",
    ["badStatus"] = "{\"status\":\"error\",\"failedCount\":0}",
    ["numberStatus"] = "{\"status\":0,\"failedCount\":0}",
    ["nullStatus"] = "{\"status\":null,\"failedCount\":0}",
    ["missingStatus"] = "{\"failedCount\":0}",
    ["rootArray"] = "[]",
    ["malformed"] = "{"
};
var results = new Dictionary<string, string>();
foreach (var item in cases) {
    try { results[item.Key] = Classifier.Classify(item.Value); }
    catch (Exception exception) { results[item.Key] = "EXCEPTION:" + exception.GetType().Name; }
}
Console.WriteLine(JsonSerializer.Serialize(results));
'''


def grade_json_output(actual: object) -> tuple[str, dict]:
    if not isinstance(actual, dict):
        return "FAIL", {"reason": "runner-output-not-object"}
    if set(actual) != set(JSON_EXPECTED):
        return "FAIL", {"reason": "runner-output-keys-invalid", "missing": sorted(set(JSON_EXPECTED) - set(actual)), "extra": sorted(set(actual) - set(JSON_EXPECTED))}
    failures = {name: value for name, value in actual.items() if value != JSON_EXPECTED[name]}
    return ("PASS" if not failures else "FAIL"), {"failures": failures, "cases": actual}


def run_json(destination: Path, dotnet: str) -> tuple[str, dict]:
    candidate = destination / "Classifier.cs"
    if not candidate.is_file():
        return "FAIL", {"reason": "Classifier.cs-missing"}
    with tempfile.TemporaryDirectory(prefix="fps-replay-") as temporary:
        work = Path(temporary)
        (work / "Classifier.cs").write_bytes(candidate.read_bytes())
        (work / "Program.cs").write_text(PROGRAM, encoding="utf-8")
        (work / "Replay.csproj").write_text('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net8.0</TargetFramework><OutputType>Exe</OutputType><ImplicitUsings>enable</ImplicitUsings></PropertyGroup></Project>', encoding="utf-8")
        try:
            build = subprocess.run([dotnet, "build", "Replay.csproj", "-nologo", "-v:q", "-o", "out"], cwd=work, text=True, capture_output=True, timeout=TIMEOUT)
        except FileNotFoundError:
            return "NOT_VERIFIED", {"reason": "dotnet-not-found"}
        except subprocess.TimeoutExpired:
            return "NOT_VERIFIED", {"reason": "dotnet-timeout"}
        if build.returncode:
            return "FAIL", {"reason": "compile-failed", "detail": build.stdout[-400:] + build.stderr[-400:]}
        try:
            run = subprocess.run([dotnet, str(work / "out" / "Replay.dll")], cwd=work, text=True, capture_output=True, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            return "FAIL", {"reason": "runtime-timeout"}
        if run.returncode:
            return "FAIL", {"reason": "runtime-failed", "detail": run.stderr[-400:]}
        try:
            actual = json.loads(run.stdout)
        except json.JSONDecodeError:
            return "FAIL", {"reason": "invalid-runner-output", "detail": run.stdout[-400:]}
    return grade_json_output(actual)


def run_encoding(destination: Path, manifest: dict) -> tuple[str, dict]:
    source = destination / "release.ps1"
    baseline = base64.b64decode(manifest["scored_bytes"]["release.ps1"])
    if not source.is_file():
        return "FAIL", {"reason": "release.ps1-missing"}
    data = source.read_bytes()
    exact = data == b"\xef\xbb\xbf" + baseline
    return ("PASS" if exact else "FAIL"), {"bom": data[:3].hex(), "exact": exact}


def check(destination: Path, dotnet: str) -> tuple[int, dict]:
    destination = destination.resolve()
    manifest, error = load_manifest(destination)
    if error:
        return 2, {"status": "FAIL", "reason": error}
    changed = preserved(destination, manifest)
    if changed:
        return 1, {"case": manifest["case"], "status": "FAIL", "reason": "preservation-failed", "changed": changed}
    if manifest["case"] == "json":
        status, detail = run_json(destination, dotnet)
    else:
        status, detail = run_encoding(destination, manifest)
    return (0 if status == "PASS" else 3 if status == "NOT_VERIFIED" else 1), {"case": manifest["case"], "status": status, **detail}


GOOD_CLASSIFIER = '''using System.Text.Json;
public static class Classifier {
 public static string Classify(string json) {
  try { using var document = JsonDocument.Parse(json); var root = document.RootElement;
   if (root.ValueKind != JsonValueKind.Object || !root.TryGetProperty("status", out var status) || status.ValueKind != JsonValueKind.String || status.GetString() != "ok" || !root.TryGetProperty("failedCount", out var failed) || failed.ValueKind != JsonValueKind.Number || !failed.TryGetInt32(out var count) || count != 0) return "FAIL";
   return "APPLIED";
  } catch (JsonException) { return "FAIL"; }
 }
}'''


def check_prepare_paths() -> dict[str, bool]:
    with tempfile.TemporaryDirectory(prefix="fps-path-controls-") as temporary:
        base = Path(temporary)
        outside = base / "outside"
        outside.mkdir()
        link = base / "linked-parent"
        link.symlink_to(outside, target_is_directory=True)
        try:
            refused = prepare("encoding", link / "run") == 2
            ancestor_safe = refused and not list(outside.iterdir())
        finally:
            link.unlink()
        destination = base / "manifest-run"
        manifest = manifest_path(destination)
        escaped = outside / "escaped.json"
        manifest.symlink_to(escaped)
        try:
            refused = prepare("encoding", destination) == 2
            manifest_safe = refused and not escaped.exists() and not destination.exists()
        finally:
            manifest.unlink()
        return {"prepare_linked_parent": ancestor_safe, "prepare_linked_manifest": manifest_safe}


def self_check(dotnet: str) -> int:
    results = check_prepare_paths()
    results["json_forged_empty_output"] = grade_json_output({})[0] == "FAIL"
    with tempfile.TemporaryDirectory(prefix="fps-replay-self-check-") as temporary:
        base = Path(temporary)
        for case in ("json", "encoding"):
            destination = base / case
            prepare(case, destination)
            if case == "json":
                path = manifest_path(destination)
                forged_manifest = json.loads(path.read_text(encoding="utf-8"))
                forged_manifest["files"]["user-state.txt"] = "forged"
                path.write_text(json.dumps(forged_manifest), encoding="utf-8")
                _, binding = check(destination, dotnet)
                results["json_manifest_binding"] = binding["status"] == "FAIL"
                path.write_text(json.dumps({"case": case, "destination": str(destination.resolve()), "files": fixture_files(case), "scored_bytes": fixture_scored_bytes(case)}), encoding="utf-8")
                _, broken = check(destination, dotnet)
                results["json_broken"] = broken["status"] == "FAIL"
                (destination / "Classifier.cs").write_text(GOOD_CLASSIFIER, encoding="utf-8")
                _, repaired = check(destination, dotnet)
                results["json_repaired"] = repaired["status"] == "PASS"
                (destination / "Classifier.cs").write_text('public static class Classifier { public static string Classify(string json) => "APPLIED"; }', encoding="utf-8")
                _, regression = check(destination, dotnet)
                results["json_behavior_regression"] = regression["status"] == "FAIL"
                (destination / "user-state.txt").write_text("changed", encoding="utf-8")
                _, preserve = check(destination, dotnet)
                results["json_preservation"] = preserve["status"] == "FAIL"
            else:
                _, baseline = check(destination, dotnet)
                results["encoding_broken"] = baseline["status"] == "FAIL"
                baseline_bytes = (FIXTURES / "encoding" / "release.ps1").read_bytes()
                (destination / "release.ps1").write_bytes(b"\xef\xbb\xbf" + baseline_bytes)
                _, repaired = check(destination, dotnet)
                results["encoding_repaired"] = repaired["status"] == "PASS"
                (destination / "release.ps1").write_bytes(b"\xff\xfe" + baseline_bytes)
                _, wrong = check(destination, dotnet)
                results["encoding_wrong_prefix"] = wrong["status"] == "FAIL"
                (destination / "user-state.txt").write_text("changed", encoding="utf-8")
                _, preserve = check(destination, dotnet)
                results["encoding_preservation"] = preserve["status"] == "FAIL"
    status = "PASS" if all(results.values()) else "FAIL"
    emit({"status": status, "checks": results})
    return 0 if status == "PASS" else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--dotnet", default="dotnet")
    sub = parser.add_subparsers(dest="command")
    prepare_parser = sub.add_parser("prepare")
    prepare_parser.add_argument("case", choices=("json", "encoding"))
    prepare_parser.add_argument("destination", type=Path)
    check_parser = sub.add_parser("check")
    check_parser.add_argument("destination", type=Path)
    check_parser.add_argument("--dotnet", default="dotnet")
    args = parser.parse_args()
    if args.self_check:
        return self_check(args.dotnet)
    if args.command == "prepare":
        return prepare(args.case, args.destination)
    if args.command == "check":
        code, report = check(args.destination, args.dotnet)
        emit(report)
        return code
    parser.error("use prepare, check, or --self-check")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())