#!/usr/bin/env python3
"""Baseline plus table-driven negative controls for validate.py."""
from __future__ import annotations
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate.py"
TEMPLATE = Path("templates/mission-view.md")
REQUIRED_JOB = "| Required work | Lead | yes | queued | NOT VERIFIED | Named owned paths |"

def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(VALIDATOR), "--root", str(root)], capture_output=True, text=True, check=False)

def replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text: raise AssertionError(f"missing mutation source in {path}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")

def empty_section(root: Path, heading: str) -> None:
    path = root / TEMPLATE; text = path.read_text(encoding="utf-8")
    changed, count = re.subn(rf"(^## {re.escape(heading)}\s*$\n).*?(?=^## )", r"\1\n", text, count=1, flags=re.M | re.S)
    if count != 1: raise AssertionError(f"section not found: {heading}")
    path.write_text(changed, encoding="utf-8")

def make_pass_ready(root: Path) -> None:
    path = root / TEMPLATE
    text = path.read_text(encoding="utf-8")
    text = text.replace("overall: NOT VERIFIED", "overall: PASS", 1)
    text = text.replace("Current artifact: NOT VERIFIED", "Current artifact: abcdef0123456789deadbeef", 1)
    text = text.replace(
        "| Required acceptance check | NOT VERIFIED | No executed check yet |",
        "| Required acceptance check | PASS | python check.py on abcdef0123456789deadbeef |",
        1,
    )
    text = text.replace(
        REQUIRED_JOB,
        "| Required work | Lead | yes | completed | PASS | Named owned paths |",
        1,
    )
    text = text.replace(
        "NOT VERIFIED. Copying this template makes no live claims.",
        "Lead ran python check.py on artifact abcdef0123456789deadbeef; the gate matched.",
        1,
    )
    text = text.replace(
        "Commit/snapshot: NOT VERIFIED. UTC timestamp: NOT VERIFIED.",
        "Commit/snapshot: abcdef0123456789deadbeef. UTC timestamp: 2026-09-14T08:00:00Z.",
        1,
    )
    path.write_text(text, encoding="utf-8")

def missing_icon(root): (root / "assets/icon-small.svg").unlink()
def duplicate_yaml(root):
    path = root / "agents/openai.yaml"; path.write_text(path.read_text(encoding="utf-8") + '  display_name: "duplicate"\n', encoding="utf-8")
def duplicate_toml(root):
    path = next((root / "examples/codex/.codex/agents").glob("*.toml")); path.write_text(path.read_text(encoding="utf-8") + '\nname = "duplicate"\n', encoding="utf-8")
def missing_packet_field(root): replace(root / "templates/evidence-packet.md", "Blocking decision, if any:", "Removed field:")
def empty_claims(root): replace(root / "templates/evidence-packet.md", "Claims: No live claims until sources are inspected.", "Claims:")
def bad_mission_status(root): replace(root / TEMPLATE, "overall: NOT VERIFIED", "overall: MAYBE")
def bad_evidence_status(root): replace(root / "templates/evidence-packet.md", "Verdict: NOT VERIFIED", "Verdict: MAYBE")
def bad_gate_status(root): replace(root / TEMPLATE, "| Required acceptance check | NOT VERIFIED |", "| Required acceptance check | MAYBE |")
def bad_gate_header(root): replace(root / TEMPLATE, "| Gate | Status | Evidence |", "| Check | Status | Evidence |")
def false_pass(root): replace(root / TEMPLATE, "overall: NOT VERIFIED", "overall: PASS")
def empty_jobs(root): empty_section(root, "Jobs")
def empty_authority(root): empty_section(root, "Authority")
def ready_job(root): replace(root / TEMPLATE, REQUIRED_JOB, "| Required work | Lead | yes | ready | NOT VERIFIED | Named owned paths |")
def complete_job(root): replace(root / TEMPLATE, REQUIRED_JOB, "| Required work | Lead | yes | complete | NOT VERIFIED | Named owned paths |")
def unsafe_profile(root): replace(root / "examples/codex/.codex/agents/mission_reviewer.toml", 'sandbox_mode = "read-only"', 'sandbox_mode = "workspace-write"')
def empty_lead_model(root): replace(root / "examples/codex/.codex/config.toml", 'model = "gpt-5.6-sol"', 'model = ""')
def bad_lead_model(root): replace(root / "examples/codex/.codex/config.toml", 'model = "gpt-5.6-sol"', 'model = "not a model!"')
def bad_child_model(root): replace(root / "examples/codex/.codex/config.toml", 'default_subagent_model = "gpt-5.6-luna"', 'default_subagent_model = "not a model!"')
def bad_child_effort(root): replace(root / "examples/codex/.codex/config.toml", 'default_subagent_reasoning_effort = "medium"', 'default_subagent_reasoning_effort = "invented-effort"')
def zero_threads(root): replace(root / "examples/codex/.codex/config.toml", "max_concurrent_threads_per_session = 3", "max_concurrent_threads_per_session = 0")
def fiction_template(root): replace(root / "templates/context-packet.md", "State the bounded job. Start as NOT VERIFIED.", "Inspect transport.py::should_send.")
def plugin_push(root): replace(root / "scripts/package_plugin.py", "smallest useful workflow and finish with verified evidence", "coordinated agents in multi-agent software missions")
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
def broken_srcset(root):
    path = root / "README.md"; path.write_text(path.read_text(encoding="utf-8") + '\n<source srcset="assets/icon-small.svg 1x, missing-mobile.svg 2x" />\n', encoding="utf-8")
def malformed_svg(root): (root / "assets/mission-control.svg").write_text("<svg>", encoding="utf-8")
def svg_event(root): replace(root / "assets/icon-small.svg", "<svg ", '<svg onload="alert(1)" ')
def svg_style_import(root): replace(root / "assets/icon-small.svg", "</svg>", "<style>@import url(https://example.test/x.css);</style></svg>")
def placeholder(root):
    path = root / "README.md"; path.write_text(path.read_text(encoding="utf-8") + "\nTODO unfinished\n", encoding="utf-8")

def pass_required_queued(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required work | Lead | yes | completed | PASS | Named owned paths |", REQUIRED_JOB)

def pass_required_running(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required work | Lead | yes | completed | PASS | Named owned paths |", "| Required work | Lead | yes | running | NOT VERIFIED | Named owned paths |")

def pass_required_fail(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required work | Lead | yes | completed | PASS | Named owned paths |", "| Required work | Lead | yes | completed | FAIL | Named owned paths |")

def pass_required_blocked(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required work | Lead | yes | completed | PASS | Named owned paths |", "| Required work | Lead | yes | completed | BLOCKED | Named owned paths |")

def pass_required_not_verified(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required work | Lead | yes | completed | PASS | Named owned paths |", "| Required work | Lead | yes | completed | NOT VERIFIED | Named owned paths |")

def pass_optional_running(root):
    make_pass_ready(root)
    replace(
        root / TEMPLATE,
        "| Required work | Lead | yes | completed | PASS | Named owned paths |",
        "| Required work | Lead | yes | completed | PASS | Named owned paths |\n| Optional scout | Unassigned | no | running | NOT VERIFIED | Read-only notes |",
    )

def pass_optional_queued(root):
    make_pass_ready(root)
    replace(
        root / TEMPLATE,
        "| Required work | Lead | yes | completed | PASS | Named owned paths |",
        "| Required work | Lead | yes | completed | PASS | Named owned paths |\n| Real remaining work | Unassigned | no | queued | NOT VERIFIED | the actual unfinished audit |",
    )

def pass_optional_completed_fail(root):
    make_pass_ready(root)
    replace(
        root / TEMPLATE,
        "| Required work | Lead | yes | completed | PASS | Named owned paths |",
        "| Required work | Lead | yes | completed | PASS | Named owned paths |\n| Optional scout | Unassigned | no | completed | FAIL | Read-only notes |",
    )

def pass_missing_artifact(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "Current artifact: abcdef0123456789deadbeef", "Current artifact: NOT VERIFIED")

def pass_no_required_job(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required work | Lead | yes | completed | PASS | Named owned paths |", "| Required work | Lead | no | completed | PASS | Named owned paths |")

def pass_blocker_after_none(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "None.", "None. Signing credential is unavailable.")

def pass_artifact_none(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "Current artifact: abcdef0123456789deadbeef", "Current artifact: None")

def pass_last_verified_lower(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "Commit/snapshot: abcdef0123456789deadbeef. UTC timestamp: 2026-09-14T08:00:00Z.", "Commit/snapshot: abcdef0123456789deadbeef. UTC timestamp: not verified.")

def pass_gate_evidence_unverified(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required acceptance check | PASS | python check.py on abcdef0123456789deadbeef |", "| Required acceptance check | PASS | NOT VERIFIED |")

def pass_required_superseded(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required work | Lead | yes | completed | PASS | Named owned paths |", "| Required work | Lead | yes | superseded | NOT VERIFIED | superseded: dropped |")

def pass_superseded_no_reason(root):
    make_pass_ready(root)
    replace(
        root / TEMPLATE,
        "| Required work | Lead | yes | completed | PASS | Named owned paths |",
        "| Required work | Lead | yes | completed | PASS | Named owned paths |\n| Old scout | Unassigned | no | superseded | NOT VERIFIED | leftover notes |",
    )

def live_placeholders(root):
    make_pass_ready(root)
    (root / "MISSION.md").write_text((root / TEMPLATE).read_text(encoding="utf-8"), encoding="utf-8")

def pass_gate_no_executed(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required acceptance check | PASS | python check.py on abcdef0123456789deadbeef |", "| Required acceptance check | PASS | No executed check yet |")

def pass_gate_not_yet(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required acceptance check | PASS | python check.py on abcdef0123456789deadbeef |", "| Required acceptance check | PASS | checked, not yet verified |")

def pass_gate_no_subject_runs(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required acceptance check | PASS | python check.py on abcdef0123456789deadbeef |", "| Required acceptance check | PASS | evals/v3 has no subject runs on abcdef0123456789deadbeef |")

def pass_gate_without_artifact(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required acceptance check | PASS | python check.py on abcdef0123456789deadbeef |", "| Required acceptance check | PASS | python check.py passed |")

def pass_short_artifact(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "Current artifact: abcdef0123456789deadbeef", "Current artifact: 2026")
    replace(root / TEMPLATE, "python check.py on abcdef0123456789deadbeef", "python check.py on 2026")
    replace(root / TEMPLATE, "artifact abcdef0123456789deadbeef", "artifact 2026")
    replace(root / TEMPLATE, "Commit/snapshot: abcdef0123456789deadbeef", "Commit/snapshot: 2026")

def pass_next_blocked(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "Fill the objective, freeze the current artifact identity, then do the next authorized check.", "Blocked: signing credential is unavailable.")

def pass_unfinished_narrative(root):
    make_pass_ready(root)
    replace(
        root / TEMPLATE,
        "Lead ran python check.py on artifact abcdef0123456789deadbeef; the gate matched.",
        "Lead ran python check.py on artifact abcdef0123456789deadbeef; unfinished work remains queued in notes.",
    )

def pass_authority_unfinished(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "Forbidden: credentials, push, deploy, destructive work and new authority.", "Forbidden: none. Unfinished work remains queued.")

def pass_gate_not_executed(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required acceptance check | PASS | python check.py on abcdef0123456789deadbeef |", "| Required acceptance check | PASS | check not executed on abcdef0123456789deadbeef |")

def pass_gate_zero_subject_runs(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required acceptance check | PASS | python check.py on abcdef0123456789deadbeef |", "| Required acceptance check | PASS | zero subject runs on abcdef0123456789deadbeef |")

def pass_gate_no_completed_subject(root):
    make_pass_ready(root)
    replace(root / TEMPLATE, "| Required acceptance check | PASS | python check.py on abcdef0123456789deadbeef |", "| Required acceptance check | PASS | evals/v3 has no completed subject results on abcdef0123456789deadbeef |")

def pass_optional_completed_not_verified(root):
    make_pass_ready(root)
    replace(
        root / TEMPLATE,
        "| Required work | Lead | yes | completed | PASS | Named owned paths |",
        "| Required work | Lead | yes | completed | PASS | Named owned paths |\n| Optional scout | Unassigned | no | completed | NOT VERIFIED | Read-only notes |",
    )

def main() -> int:
    from validate import srcset_urls
    assert list(srcset_urls('a.svg 1x,b.svg 2x')) == ['a.svg', 'b.svg']
    assert list(srcset_urls('data:image/png;base64,AAAA 1x, b.svg 2x')) == ['data:image/png;base64,AAAA', 'b.svg']
    assert list(srcset_urls('a.svg,b.svg 2x')) == ['a.svg,b.svg']
    baseline = run(ROOT)
    if baseline.returncode:
        print(baseline.stdout + baseline.stderr, end="", file=sys.stderr); print("FAIL: baseline must validate", file=sys.stderr); return 1
    controls = {
        missing_icon: "missing icon_small", duplicate_yaml: "duplicate key",
        duplicate_toml: "duplicate TOML", missing_packet_field: "fields must be exactly", empty_claims: "Claims needs content",
        bad_mission_status: "invalid overall", bad_evidence_status: "invalid Verdict", bad_gate_status: "invalid hard-gate status", bad_gate_header: "Hard gates header must be",
        false_pass: "overall PASS requires every hard gate PASS", empty_jobs: "empty section Jobs", empty_authority: "empty section Authority",
        ready_job: "invalid job lifecycle status", complete_job: "invalid job lifecycle status",
        unsafe_profile: "unsafe sandbox mode", empty_lead_model: "model reference required",
        bad_lead_model: "invalid model reference", bad_child_model: "invalid model reference", bad_child_effort: "bad default subagent reasoning effort",
        zero_threads: "max_concurrent_threads_per_session must be 1..32",
        fiction_template: "blank templates must not contain case fiction",
        plugin_push: "plugin copy must not push multi-agent defaults",
        pass_required_queued: "overall PASS forbids unfinished jobs",
        pass_required_running: "overall PASS forbids unfinished jobs",
        pass_required_fail: "overall PASS requires required jobs completed with PASS",
        pass_required_blocked: "overall PASS requires required jobs completed with PASS",
        pass_required_not_verified: "overall PASS requires required jobs completed with PASS",
        pass_optional_queued: "overall PASS forbids unfinished jobs",
        pass_optional_running: "overall PASS forbids unfinished jobs",
        pass_optional_completed_fail: "overall PASS forbids completed jobs with a negative verdict",
        pass_missing_artifact: "overall PASS requires a current artifact identity",
        pass_no_required_job: "at least one required job",
        pass_blocker_after_none: "overall PASS requires no blockers",
        pass_artifact_none: "overall PASS requires a current artifact identity",
        pass_last_verified_lower: "overall PASS requires current last-verified identity",
        pass_gate_evidence_unverified: "overall PASS forbids missing hard-gate evidence",
        pass_required_superseded: "superseded jobs must be optional",
        pass_superseded_no_reason: "superseded jobs need a superseded: reason",
        live_placeholders: "unresolved template placeholders",
        pass_gate_no_executed: "overall PASS forbids missing hard-gate evidence",
        pass_gate_not_yet: "overall PASS forbids missing hard-gate evidence",
        pass_gate_no_subject_runs: "overall PASS forbids missing hard-gate evidence",
        pass_gate_without_artifact: "overall PASS requires current artifact identity in hard-gate evidence",
        pass_short_artifact: "overall PASS requires a current artifact identity",
        pass_next_blocked: "overall PASS forbids a blocker in Next action",
        pass_unfinished_narrative: "overall PASS forbids unfinished work in narrative fields",
        pass_authority_unfinished: "overall PASS forbids unfinished work in narrative fields",
        pass_gate_not_executed: "overall PASS forbids missing hard-gate evidence",
        pass_gate_zero_subject_runs: "overall PASS forbids missing hard-gate evidence",
        pass_gate_no_completed_subject: "overall PASS forbids missing hard-gate evidence",
        pass_optional_completed_not_verified: "overall PASS forbids completed jobs with a negative verdict",
        invalid_eval_path: "unsafe fixture path", invalid_activation: "invalid activation", drive_eval_path: "unsafe fixture path", eval_ancestor_collision: "conflicting fixture file and directory",
        broken_link: "broken local link", broken_srcset: "broken local link", malformed_svg: "malformed SVG", svg_event: "event handler forbidden",
        svg_style_import: "unsafe SVG element style", placeholder: "unfinished placeholder",
    }
    for mutation, expected in controls.items():
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "repo"; shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__")); mutation(copy)
            result = run(copy); output = result.stdout + result.stderr
            if result.returncode == 0 or expected not in output: print(f"FAIL: negative control {mutation.__name__}: {output}", file=sys.stderr); return 1
    with tempfile.TemporaryDirectory() as directory:
        copy = Path(directory) / "repo"; shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        replace(copy / TEMPLATE, "overall: NOT VERIFIED", "overall: BLOCKED")
        replace(copy / TEMPLATE, "None.", "Required signing credential is unavailable.")
        if run(copy).returncode: print("FAIL: legitimate BLOCKED mission rejected", file=sys.stderr); return 1
    with tempfile.TemporaryDirectory() as directory:
        copy = Path(directory) / "repo"; shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        make_pass_ready(copy)
        replace(
            copy / TEMPLATE,
            "| Required work | Lead | yes | completed | PASS | Named owned paths |",
            "| Required work | Lead | yes | completed | PASS | Named owned paths |\n| Old scout | Unassigned | no | superseded | NOT VERIFIED | superseded: replaced by lead inspection |",
        )
        if run(copy).returncode:
            print("FAIL: legitimate PASS with superseded optional job rejected", file=sys.stderr); return 1
    with tempfile.TemporaryDirectory() as directory:
        copy = Path(directory) / "repo"; shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        replace(copy / "examples/codex/.codex/config.toml", 'model = "gpt-5.6-sol"', 'model = "claude-opus-4"')
        replace(copy / "examples/codex/.codex/config.toml", 'default_subagent_model = "gpt-5.6-luna"', 'default_subagent_model = "gpt-oss-20b"')
        replace(copy / "examples/codex/.codex/config.toml", "max_concurrent_threads_per_session = 3", "max_concurrent_threads_per_session = 5")
        (copy / "examples/codex/.codex/agents/mission_verifier.toml").unlink()
        if run(copy).returncode:
            print("FAIL: optional profile with other models, 5 threads and three roles rejected", file=sys.stderr); return 1
    print(f"PASS: queued/PASS/BLOCKED positives; {len(controls)} negative controls"); return 0

if __name__ == "__main__": raise SystemExit(main())
