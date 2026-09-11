#!/usr/bin/env python3
"""Baseline plus table-driven negative controls for validate.py."""
from __future__ import annotations
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate.py"

def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(VALIDATOR), "--root", str(root)], capture_output=True, text=True, check=False)

def replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text: raise AssertionError(f"missing mutation source in {path}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

def empty_section(root: Path, heading: str) -> None:
    path = root / "templates/mission-view.md"; text = path.read_text(encoding="utf-8")
    changed, count = re.subn(rf"(^## {re.escape(heading)}\s*$\n).*?(?=^## )", r"\1\n", text, count=1, flags=re.M | re.S)
    if count != 1: raise AssertionError(f"section not found: {heading}")
    path.write_text(changed, encoding="utf-8")

def missing_icon(root): (root / "assets/icon-small.svg").unlink()
def duplicate_yaml(root):
    path = root / "agents/openai.yaml"; path.write_text(path.read_text(encoding="utf-8") + '  display_name: "duplicate"\n', encoding="utf-8")
def duplicate_toml(root):
    path = next((root / "examples/codex/.codex/agents").glob("*.toml")); path.write_text(path.read_text(encoding="utf-8") + '\nname = "duplicate"\n', encoding="utf-8")
def missing_packet_field(root): replace(root / "templates/evidence-packet.md", "Blocking decision, if any:", "Removed field:")
def empty_claims(root): replace(root / "templates/evidence-packet.md", "Claims: The required deadline boundary check has not been executed.", "Claims:")
def bad_mission_status(root): replace(root / "templates/mission-view.md", "overall: NOT VERIFIED", "overall: MAYBE")
def bad_evidence_status(root): replace(root / "templates/evidence-packet.md", "Verdict: NOT VERIFIED", "Verdict: MAYBE")
def bad_gate_status(root): replace(root / "templates/mission-view.md", "| Deadline behavior | NOT VERIFIED |", "| Deadline behavior | MAYBE |")
def bad_gate_header(root): replace(root / "templates/mission-view.md", "| Gate | Status | Evidence |", "| Check | Status | Evidence |")
def false_pass(root): replace(root / "templates/mission-view.md", "overall: NOT VERIFIED", "overall: PASS")
def empty_jobs(root): empty_section(root, "Jobs")
def empty_authority(root): empty_section(root, "Authority")
def ready_job(root): replace(root / "templates/mission-view.md", "| Deadline investigation | Unassigned | queued |", "| Deadline investigation | Unassigned | ready |")
def complete_job(root): replace(root / "templates/mission-view.md", "| Deadline investigation | Unassigned | queued |", "| Deadline investigation | Unassigned | complete |")
def unsafe_profile(root): replace(root / "examples/codex/.codex/agents/mission_reviewer.toml", 'sandbox_mode = "read-only"', 'sandbox_mode = "workspace-write"')
def missing_role(root): (root / "examples/codex/.codex/agents/mission_verifier.toml").unlink()
def invalid_eval_path(root):
    path = root / "evals/cases.json"; data = json.loads(path.read_text(encoding="utf-8")); data["cases"][0]["fixture"] = {"../escape.txt": "x"}; path.write_text(json.dumps(data), encoding="utf-8")
def invalid_activation(root):
    path = root / "evals/cases.json"; data = json.loads(path.read_text(encoding="utf-8")); data["cases"][0]["activation"] = []; path.write_text(json.dumps(data), encoding="utf-8")
def drive_eval_path(root):
    path = root / "evals/cases.json"; data = json.loads(path.read_text(encoding="utf-8")); data["cases"][0]["fixture"] = {"C:/escape.txt": "x"}; path.write_text(json.dumps(data), encoding="utf-8")
def eval_ancestor_collision(root):
    path = root / "evals/cases.json"; data = json.loads(path.read_text(encoding="utf-8")); data["cases"][0]["fixture"] = {"a": "file", "a/b.txt": "child"}; path.write_text(json.dumps(data), encoding="utf-8")
def broken_link(root):
    path = root / "README.md"; path.write_text(path.read_text(encoding="utf-8") + "\n[broken](missing-file.md)\n", encoding="utf-8")
def malformed_svg(root): (root / "assets/mission-control.svg").write_text("<svg>", encoding="utf-8")
def svg_event(root): replace(root / "assets/icon-small.svg", "<svg ", '<svg onload="alert(1)" ')
def svg_style_import(root): replace(root / "assets/icon-small.svg", "</svg>", "<style>@import url(https://example.test/x.css);</style></svg>")
def placeholder(root):
    path = root / "README.md"; path.write_text(path.read_text(encoding="utf-8") + "\nTODO unfinished\n", encoding="utf-8")

def main() -> int:
    baseline = run(ROOT)
    if baseline.returncode:
        print(baseline.stdout + baseline.stderr, end="", file=sys.stderr); print("FAIL: baseline must validate", file=sys.stderr); return 1
    controls = {
        missing_icon: "missing icon_small", duplicate_yaml: "duplicate key",
        duplicate_toml: "duplicate TOML", missing_packet_field: "fields must be exactly", empty_claims: "Claims needs content",
        bad_mission_status: "invalid overall", bad_evidence_status: "invalid Verdict", bad_gate_status: "invalid hard-gate status", bad_gate_header: "Hard gates header must be",
        false_pass: "overall PASS requires every hard gate PASS", empty_jobs: "empty section Jobs", empty_authority: "empty section Authority",
        ready_job: "invalid job lifecycle status", complete_job: "invalid job lifecycle status",
        unsafe_profile: "unsafe sandbox mode", missing_role: "must be exactly",
        invalid_eval_path: "unsafe fixture path", invalid_activation: "invalid activation", drive_eval_path: "unsafe fixture path", eval_ancestor_collision: "conflicting fixture file and directory",
        broken_link: "broken local link", malformed_svg: "malformed SVG", svg_event: "event handler forbidden",
        svg_style_import: "unsafe SVG element style", placeholder: "unfinished placeholder",
    }
    for mutation, expected in controls.items():
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "repo"; shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__")); mutation(copy)
            result = run(copy); output = result.stdout + result.stderr
            if result.returncode == 0 or expected not in output: print(f"FAIL: negative control {mutation.__name__}: {output}", file=sys.stderr); return 1
    with tempfile.TemporaryDirectory() as directory:
        copy = Path(directory) / "repo"; shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        replace(copy / "templates/mission-view.md", "overall: NOT VERIFIED", "overall: BLOCKED")
        replace(copy / "templates/mission-view.md", "None established. Missing evidence must be gathered; it is not a user blocker.", "Required signing credential is unavailable.")
        if run(copy).returncode: print("FAIL: legitimate BLOCKED mission rejected", file=sys.stderr); return 1
    with tempfile.TemporaryDirectory() as directory:
        copy = Path(directory) / "repo"; shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        replace(copy / "templates/mission-view.md", "| Deadline investigation | Unassigned | queued |", "| Deadline investigation | Unassigned | completed |")
        replace(copy / "templates/mission-view.md", "| Retry investigation | Unassigned | queued |", "| Retry investigation | Unassigned | PASS |")
        if run(copy).returncode: print("FAIL: legitimate completed/PASS jobs rejected", file=sys.stderr); return 1
    print(f"PASS: queued, completed/PASS and BLOCKED positives; {len(controls)} negative controls"); return 0

if __name__ == "__main__": raise SystemExit(main())
