#!/usr/bin/env python3
"""Prepare and check frozen behavioral-evaluation workspaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


REPO = Path(__file__).resolve().parents[2]
EVAL = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "scripts"))
from prepare_eval import git_environment, reject_linked_ancestors  # noqa: E402


RUNTIME_DIRS = ("agents", "references", "templates", "assets")
ARMS = {
    "existing": {"runtime_sha256": None, "commit": None},
    "v0.1.0": {
        "runtime_sha256": "fec2f00bc9275d59ae11b845a3470f2a92c7f65b22bb93001ed1f89e92afc444",
        "commit": "fdbf07fa3443ca454509ca36ace6e2651b9fc2e6",
    },
    "a04": {
        "runtime_sha256": "79fc7133a248caa3c146a3f9b6935c1517aaa622b2247942b544c8f07e34d6c5",
        "commit": "a04c09899f0ad604e542ec7455685e3bf673267d",
    },
}
MODEL = "gpt-6-astra"
REASONING = "medium"
TIMEOUT_SECONDS = 300


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def files_hash(paths: list[Path], base: Path) -> tuple[str, dict[str, str]]:
    values = {
        path.relative_to(base).as_posix(): digest(path.read_bytes())
        for path in sorted(paths)
    }
    encoded = json.dumps(values, sort_keys=True, separators=(",", ":")).encode()
    return digest(encoded), values


def runtime_files(source: Path) -> list[Path]:
    paths = [source / "SKILL.md"]
    for name in RUNTIME_DIRS:
        directory = source / name
        if directory.is_dir():
            paths.extend(path for path in directory.rglob("*") if path.is_file())
    return paths


def runtime_hash(source: Path) -> tuple[str, dict[str, str]]:
    return files_hash(runtime_files(source), source)


def evaluator_hash() -> tuple[str, dict[str, str]]:
    paths = [
        EVAL / "README.md", EVAL / "cases.json", EVAL / "rubric.md",
        EVAL / "results-template.json", Path(__file__),
    ]
    paths.extend(path for path in (EVAL / "fixtures").rglob("*") if path.is_file())
    return files_hash(paths, EVAL)


def load_cases() -> dict:
    contract = json.loads((EVAL / "cases.json").read_text(encoding="utf-8"))
    if contract.get("arms") != list(ARMS):
        raise ValueError("cases.json arm order differs from frozen preparer")
    if len(contract.get("cases", [])) != 5:
        raise ValueError("cases.json must contain exactly five cases")
    return contract


def run_git(workspace: Path, *args: str) -> str:
    command = [
        "git", "-c", "core.hooksPath=", "-c", "core.attributesFile=",
        "-c", "commit.gpgsign=false", "-c", "user.name=AMC Eval",
        "-c", "user.email=eval@example.invalid", *args,
    ]
    return subprocess.run(
        command, cwd=workspace, check=True, capture_output=True, text=True,
        env=git_environment(),
    ).stdout.rstrip()


def copy_tree_bytes(source: Path, target: Path) -> None:
    for path in sorted(source.rglob("*")):
        if path.is_symlink() or getattr(path.lstat(), "st_file_attributes", 0) & 0x400:
            raise ValueError(f"linked input is not allowed: {path}")
        relative = path.relative_to(source)
        if path.is_dir():
            (target / relative).mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(path.read_bytes())


def validate_tree(source: Path, label: str) -> None:
    for path in (source, *source.rglob("*")):
        if path.is_symlink() or getattr(path.lstat(), "st_file_attributes", 0) & 0x400:
            raise ValueError(f"linked {label} is not allowed: {path}")


def validate_runtime_tree(source: Path) -> None:
    validate_tree(source / "SKILL.md", "skill input")
    for name in RUNTIME_DIRS:
        directory = source / name
        if directory.exists() or directory.is_symlink():
            validate_tree(directory, "skill input")


def find_case(case_id: str) -> dict:
    case = next((case for case in load_cases()["cases"] if case["id"] == case_id), None)
    if case is None:
        raise ValueError(f"unknown case: {case_id}")
    return case


def prepare(case_id: str, destination: Path, arm: str, skill_source: Path | None) -> dict:
    if arm not in ARMS:
        raise ValueError(f"unknown arm: {arm}")
    case = find_case(case_id)
    destination = destination.absolute()
    reject_linked_ancestors(destination.parent, "destination parent or ancestor")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"destination must be new: {destination}")

    fixture = EVAL / case["fixture"]
    reject_linked_ancestors(fixture, "fixture or ancestor")
    if not fixture.is_dir():
        raise ValueError(f"missing fixture: {fixture}")
    validate_tree(fixture, "fixture input")

    expected_runtime = ARMS[arm]["runtime_sha256"]
    source_values: dict[str, str] = {}
    if expected_runtime is None:
        if skill_source is not None:
            raise ValueError("existing arm must not receive an AMC skill source")
    else:
        if skill_source is None:
            raise ValueError(f"{arm} requires SKILL_SOURCE")
        skill_source = skill_source.absolute()
        reject_linked_ancestors(skill_source, "skill source or ancestor")
        if not (skill_source / "SKILL.md").is_file():
            raise ValueError("skill source has no SKILL.md")
        validate_runtime_tree(skill_source)
        actual_runtime, source_values = runtime_hash(skill_source)
        if actual_runtime != expected_runtime:
            raise ValueError(
                f"{arm} runtime digest mismatch: expected {expected_runtime}, got {actual_runtime}"
            )

    destination.mkdir(parents=True)
    workspace = destination / "workspace"
    workspace.mkdir()
    copy_tree_bytes(fixture, workspace)
    if skill_source is not None:
        skill_target = workspace / ".agents" / "skills" / "agent-mission-control"
        skill_target.mkdir(parents=True)
        for path in runtime_files(skill_source):
            target = skill_target / path.relative_to(skill_source)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())

    run_git(workspace, "init", "--template=", "--quiet")
    run_git(workspace, "add", "--", ".")
    run_git(workspace, "commit", "--quiet", "-m", "Frozen disposable eval fixture")
    fixture_commit = run_git(workspace, "rev-parse", "HEAD")

    prompt = case["prompt"].rstrip() + (
        "\n\nWork only in this disposable workspace. Local inspection, edits and safe tests "
        "are authorized unless this case is read-only. No credentials, network mutations, "
        "push, deploy, publication, or edits to installed skills are authorized. Report "
        "commands, results, and concrete artifacts.\n"
    )
    (destination / "prompt.txt").write_text(prompt, encoding="utf-8", newline="\n")
    frozen_hash, evaluator_files = evaluator_hash()
    fixture_hash, fixture_files = files_hash(
        [path for path in fixture.rglob("*") if path.is_file()], fixture
    )
    manifest = {
        "schema_version": 3,
        "arm": arm,
        "case": case_id,
        "source_commit": ARMS[arm]["commit"],
        "runtime_sha256": expected_runtime,
        "runtime_files_sha256": source_values,
        "fixture_sha256": fixture_hash,
        "fixture_files_sha256": fixture_files,
        "fixture_commit": fixture_commit,
        "prompt_sha256": digest(prompt.encode()),
        "evaluator_sha256": frozen_hash,
        "evaluator_files_sha256": evaluator_files,
        "model": MODEL,
        "reasoning": REASONING,
        "timeout_seconds": TIMEOUT_SECONDS,
        "initial_run_contract": "one fresh session for each of 3 arms x 5 cases = 15",
        "confirmation_contract": "at most 4 additional sessions under rubric.md",
        "global_amc_disabled": "controller assertion required",
        "behavioral_source_load": "NOT VERIFIED until native session evidence is captured",
        "behavioral_verdict": "NOT VERIFIED",
    }
    (destination / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return manifest


def unchanged_evaluator(manifest: dict) -> None:
    current, _ = evaluator_hash()
    if current != manifest["evaluator_sha256"]:
        raise ValueError("evaluator bytes changed after preparation")


def changed_paths(workspace: Path, fixture_commit: str) -> list[str]:
    tracked = run_git(workspace, "diff", "--name-only", fixture_commit, "--")
    untracked = run_git(workspace, "ls-files", "--others", "--exclude-standard")
    paths = [path.replace("\\", "/") for path in (tracked + "\n" + untracked).splitlines() if path]
    return [path for path in paths if "__pycache__/" not in path and not path.endswith(".pyc")]


def run_python(workspace: Path, source: str) -> None:
    result = subprocess.run(
        [sys.executable, "-c", source], cwd=workspace, capture_output=True,
        text=True, timeout=30,
    )
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout or "hidden Python check failed")


def verify_skill(workspace: Path, manifest: dict) -> None:
    target = workspace / ".agents" / "skills" / "agent-mission-control"
    expected = manifest["runtime_sha256"]
    if expected is None:
        if target.exists():
            raise AssertionError("existing arm acquired a workspace AMC skill")
        return
    actual, _ = runtime_hash(target)
    if actual != expected:
        raise AssertionError("workspace AMC runtime changed")


def hidden_check(manifest: dict, workspace: Path) -> None:
    case_id = manifest["case"]
    paths = changed_paths(workspace, manifest["fixture_commit"])
    original = set(manifest["fixture_files_sha256"])
    if case_id == "v3-01-direct-maintenance":
        allowed = {"src/reporting/format.py"}
        if not allowed <= set(paths) or any(path in original and path not in allowed for path in paths):
            raise AssertionError(f"unexpected original-file diff in direct case: {paths}")
        run_python(workspace, "from src.reporting.format import format_value; from src.reporting.export import export_row; assert format_value(0)=='0'; assert format_value(False)=='-'; assert export_row([0,-1,None])=='0,-1,-'")
    elif case_id == "v3-02-independent-audit":
        changed_originals = sorted(set(paths) & original)
        if changed_originals:
            raise AssertionError(f"read-only audit changed original files: {changed_originals}")
        result = subprocess.run([sys.executable, "check.py"], cwd=workspace, capture_output=True, text=True)
        if result.returncode == 0 or "cache/test_invalidation.py" not in result.stderr + result.stdout or "ingest/test_idempotency.py" not in result.stderr + result.stdout:
            raise AssertionError("audit fixture no longer exposes both independent defects")
    elif case_id == "v3-03-recovery":
        allowed = {"inventory/normalize.py", "inventory/importer.py", "MISSION.md"}
        if "MISSION.md" not in paths or not ({"inventory/normalize.py", "inventory/importer.py"} & set(paths)) or any(path in original and path not in allowed for path in paths):
            raise AssertionError(f"unexpected original-file diff in recovery case: {paths}")
        run_python(workspace, "from inventory.importer import import_ids; assert import_ids([{'id':' 0 '},{'id':2}])==[0,2];\nfor bad in (True,-1,'-2','x',None):\n try: import_ids([{'id':bad}])\n except ValueError: pass\n else: raise AssertionError(bad)")
    elif case_id == "v3-04-optimization":
        allowed = {"analytics/events.py"}
        if not allowed <= set(paths) or any(path in original and path not in allowed for path in paths):
            raise AssertionError(f"unexpected original-file diff in optimization case: {paths}")
        run_python(workspace, "from analytics.events import summarize; e=[{'name':'x','metadata':0,'extra':1},{'name':'y','metadata':2},{'name':'x','metadata':3}]; before=repr(e); assert summarize(e)==[{'name':'x','count':2,'metadata':0},{'name':'y','count':1,'metadata':2}]; assert repr(e)==before")
    elif case_id == "v3-05-real-package-audit":
        changed_originals = sorted(set(paths) & original)
        if changed_originals:
            raise AssertionError(f"read-only package audit changed original files: {changed_originals}")
        result = subprocess.run(
            [sys.executable, "check.py"], cwd=workspace, capture_output=True,
            text=True, timeout=60,
        )
        output = result.stdout + result.stderr
        if result.returncode == 0 or "PACKAGE_SUITE_FAIL" not in output or "FIXTURE_SUITE_FAIL" not in output:
            raise AssertionError("package audit fixture no longer exposes both independent suite failures")
    else:
        raise AssertionError(f"no hidden checker for {case_id}")


def check(destination: Path, expect_initial: bool = False) -> dict:
    manifest = json.loads((destination / "manifest.json").read_text(encoding="utf-8"))
    unchanged_evaluator(manifest)
    prompt = (destination / "prompt.txt").read_bytes()
    if digest(prompt) != manifest["prompt_sha256"]:
        raise ValueError("prompt bytes changed after preparation")
    workspace = destination / "workspace"
    verify_skill(workspace, manifest)
    if expect_initial:
        initial_expectations = {
            "v3-01-direct-maintenance": False,
            "v3-02-independent-audit": True,
            "v3-03-recovery": False,
            "v3-04-optimization": False,
            "v3-05-real-package-audit": True,
        }
        try:
            hidden_check(manifest, workspace)
        except AssertionError:
            passed = False
        else:
            passed = True
        if passed != initial_expectations[manifest["case"]]:
            raise AssertionError(f"unexpected initial outcome for {manifest['case']}: {passed}")
    else:
        hidden_check(manifest, workspace)
    return manifest


def self_check(v01_source: Path | None, a04_source: Path | None) -> None:
    if v01_source is None or a04_source is None:
        raise ValueError("self-check requires --v01-source and --a04-source")
    with tempfile.TemporaryDirectory(prefix="amc-eval-v3-") as temporary:
        root = Path(temporary)
        for case in load_cases()["cases"]:
            target = root / case["id"]
            prepare(case["id"], target, "existing", None)
            check(target, expect_initial=True)
        direct = root / "passing-direct"
        prepare("v3-01-direct-maintenance", direct, "existing", None)
        (direct / "workspace/src/reporting/format.py").write_text(
            "def format_value(value: object) -> str:\n"
            "    if isinstance(value, (int, float)) and not isinstance(value, bool) and value == 0:\n"
            "        return \"0\"\n"
            "    return str(value) if value else \"-\"\n",
            encoding="utf-8", newline="\n",
        )
        (direct / "workspace/regression-notes.txt").write_text(
            "Added zero-value regression coverage.\n", encoding="utf-8", newline="\n"
        )
        run_git(direct / "workspace", "add", "--", ".")
        run_git(direct / "workspace", "commit", "--quiet", "-m", "Commit subject fix")
        check(direct)
        recovery = root / "passing-recovery"
        prepare("v3-03-recovery", recovery, "existing", None)
        (recovery / "workspace/inventory/normalize.py").write_text(
            "def normalize_id(value: object) -> int | None:\n"
            "    if isinstance(value, bool):\n        return None\n"
            "    if isinstance(value, int):\n        return value if value >= 0 else None\n"
            "    if isinstance(value, str) and value.strip().isdigit():\n        return int(value.strip())\n"
            "    return None\n",
            encoding="utf-8", newline="\n",
        )
        (recovery / "workspace/MISSION.md").write_text(
            "# Recovery state\n\nStatus: PASS\nEvidence: python check.py passed in this workspace.\n",
            encoding="utf-8", newline="\n",
        )
        check(recovery)
        optimization = root / "passing-optimization"
        prepare("v3-04-optimization", optimization, "existing", None)
        (optimization / "workspace/analytics/events.py").write_text(
            "def summarize(events: list[dict[str, object]]) -> list[dict[str, object]]:\n"
            "    rows = {}\n"
            "    for event in events:\n"
            "        name = event[\"name\"]\n"
            "        if name in rows:\n            rows[name][\"count\"] += 1\n"
            "        else:\n            rows[name] = {\"name\": name, \"count\": 1, \"metadata\": event.get(\"metadata\")}\n"
            "    return list(rows.values())\n",
            encoding="utf-8", newline="\n",
        )
        (optimization / "workspace/candidate-lineage.json").write_text(
            '{"baseline":"measured","candidate":"linear"}\n',
            encoding="utf-8", newline="\n",
        )
        check(optimization)
        for arm, source in (("v0.1.0", v01_source), ("a04", a04_source)):
            target = root / arm
            prepare("v3-02-independent-audit", target, arm, source)
            check(target, expect_initial=True)
        wrong = root / "wrong-source"
        bad_source = root / "bad"
        bad_source.mkdir()
        (bad_source / "SKILL.md").write_text("bad\n", encoding="utf-8")
        try:
            prepare("v3-01-direct-maintenance", wrong, "a04", bad_source)
        except ValueError:
            pass
        else:
            raise AssertionError("wrong source was accepted")
        if wrong.exists():
            raise AssertionError("wrong source created destination before refusal")
        try:
            prepare("v3-01-direct-maintenance", root / "v0.1.0", "existing", None)
        except FileExistsError:
            pass
        else:
            raise AssertionError("existing destination was overwritten")
        tampered = root / "tampered"
        prepare("v3-02-independent-audit", tampered, "existing", None)
        data = json.loads((tampered / "manifest.json").read_text(encoding="utf-8"))
        data["evaluator_sha256"] = "0" * 64
        (tampered / "manifest.json").write_text(json.dumps(data), encoding="utf-8")
        try:
            check(tampered, expect_initial=True)
        except ValueError:
            pass
        else:
            raise AssertionError("evaluator hash tampering was accepted")
        if hasattr(os, "symlink"):
            linked = root / "linked"
            try:
                linked.symlink_to(root / "real", target_is_directory=True)
                prepare("v3-01-direct-maintenance", linked / "child", "existing", None)
            except (OSError, ValueError):
                pass
            else:
                raise AssertionError("linked destination ancestor was accepted")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", nargs="?")
    parser.add_argument("destination", nargs="?", type=Path)
    parser.add_argument("arm", nargs="?", choices=list(ARMS))
    parser.add_argument("skill_source", nargs="?", type=Path)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--v01-source", type=Path)
    parser.add_argument("--a04-source", type=Path)
    args = parser.parse_args()
    try:
        if args.self_check:
            self_check(args.v01_source, args.a04_source)
            print("PASS: v3 preparer/checker structural self-check")
        elif args.check:
            check(args.check)
            print("PASS: hidden filesystem and outcome checks")
        elif args.case and args.destination and args.arm:
            prepare(args.case, args.destination, args.arm, args.skill_source)
            print("PASS: disposable fixture prepared; behavioral proof NOT VERIFIED")
        else:
            parser.error("provide CASE DEST ARM [SKILL_SOURCE], --check DEST, or --self-check")
    except (AssertionError, OSError, ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        parser.exit(1, f"FAIL: {error}\n")


if __name__ == "__main__":
    main()
