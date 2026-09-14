#!/usr/bin/env python3
"""Launch one frozen comparison subject. Does not score product superiority."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
C8 = "c49dc1be2e334091f6c841047ff2ad778b7bde84"
RUNTIME = ("SKILL.md", "LICENSE", "agents", "references", "templates", "assets")
CASES = {
    "audit": {"sandbox": "workspace-write", "hidden": "audit_check.py"},
    "false-pass": {"sandbox": "workspace-write", "hidden": "false_pass_check.py"},
    "holdout": {"sandbox": "workspace-write", "hidden": "holdout_check.py"},
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_tree(root: Path) -> dict[str, str]:
    files = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            files[path.relative_to(root).as_posix()] = digest_bytes(path.read_bytes())
    return files


def fingerprint(files: dict[str, str]) -> str:
    return digest_bytes(json.dumps(files, sort_keys=True).encode())


def copy_runtime(source: Path, dest: Path) -> None:
    dest.mkdir(parents=True)
    shutil.copy2(source / "SKILL.md", dest / "SKILL.md")
    shutil.copy2(source / "LICENSE", dest / "LICENSE")
    for name in ("agents", "references", "templates", "assets"):
        shutil.copytree(source / name, dest / name)


def extract_c8(dest: Path) -> None:
    dest.mkdir(parents=True)
    archive = subprocess.run(
        ["git", "-C", str(ROOT), "archive", C8, *RUNTIME],
        check=True,
        capture_output=True,
    )
    subprocess.run(["tar", "-xf", "-", "-C", str(dest)], check=True, input=archive.stdout)


def claimed_verdict(text: str) -> str:
    tail = "\n".join(text.strip().splitlines()[-30:])
    match = re.search(r"(?im)\b(NOT VERIFIED|BLOCKED|FAIL|PASS)\b", tail)
    return match.group(1).upper() if match else "NOT VERIFIED"


def codex_bin() -> str:
    found = shutil.which("codex") or shutil.which("codex.cmd")
    if not found:
        raise FileNotFoundError("codex executable not found on PATH")
    return found


def parse_usage(jsonl: str) -> dict:
    usage = {"input_tokens": None, "cached_input_tokens": None, "output_tokens": None, "children": 0}
    for line in jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event.get("item"), dict) and event["item"].get("type") in {"agent_spawn", "subagent", "thread_spawn"}:
            usage["children"] += 1
        command = ""
        if isinstance(event.get("item"), dict):
            command = str(event["item"].get("command") or "")
        if "spawn_agent" in command:
            usage["children"] += 1
        payload = event.get("usage") or event.get("token_usage") or {}
        if isinstance(payload, dict):
            for key, dest in (
                ("input_tokens", "input_tokens"),
                ("cached_input_tokens", "cached_input_tokens"),
                ("output_tokens", "output_tokens"),
                ("input", "input_tokens"),
                ("cached_input", "cached_input_tokens"),
                ("output", "output_tokens"),
            ):
                if payload.get(key) is not None:
                    usage[dest] = payload[key]
    return usage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arm", required=True, choices=("direct", "candidate.8", "candidate.9"))
    parser.add_argument("--case", required=True, choices=tuple(CASES))
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    if ROOT == out or ROOT in out.parents:
        print("error: --out must be outside the source repository", file=sys.stderr)
        return 1
    if out.exists():
        print(f"error: destination exists: {out}", file=sys.stderr)
        return 1

    spec = CASES[args.case]
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    prompt = (HERE / "cases" / f"{args.case}.txt").read_text(encoding="utf-8")
    if args.arm != "direct":
        prompt = "$agent-mission-control\n\n" + prompt

    workspace = out / "workspace"
    workspace.mkdir(parents=True)
    shutil.copytree(HERE / "fixtures" / args.case, workspace, dirs_exist_ok=True)
    (workspace / "prompt.txt").write_text(prompt, encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(workspace)], check=True)

    skill_hash = None
    skill_dir = workspace / ".agents" / "skills" / "agent-mission-control"
    if args.arm == "candidate.8":
        extract_c8(skill_dir)
        skill_hash = fingerprint(digest_tree(skill_dir))
    elif args.arm == "candidate.9":
        copy_runtime(ROOT, skill_dir)
        skill_hash = fingerprint(digest_tree(skill_dir))

    fixture_hash = fingerprint(digest_tree(HERE / "fixtures" / args.case))
    hidden_path = HERE / "hidden" / spec["hidden"]
    hidden_hash = digest_bytes(hidden_path.read_bytes())
    candidate_hash = None
    if args.arm == "candidate.9":
        files = {}
        for name in RUNTIME:
            path = ROOT / name
            if path.is_file():
                files[name] = digest_bytes(path.read_bytes())
            else:
                files.update({f"{name}/{rel}": digest for rel, digest in digest_tree(path).items()})
        candidate_hash = fingerprint(files)

    launch = [
        codex_bin(),
        "exec",
        "--ignore-user-config",
        "--ephemeral",
        "--approve-for-me",
        "--json",
        "--skip-git-repo-check",
        "-m",
        protocol["model"],
        "-c",
        f'model_reasoning_effort="{protocol["reasoning"]}"',
        "-C",
        str(workspace),
        "-o",
        str(out / "final.md"),
        "-",
    ]
    (out / "launch.json").write_text(
        json.dumps(
            {
                "arm": args.arm,
                "case": args.case,
                "command": launch,
                "sandbox": spec["sandbox"],
                "timeout_s": protocol["timeout_s"],
                "host": protocol["host"],
                "host_version": protocol["host_version"],
                "model": protocol["model"],
                "reasoning": protocol["reasoning"],
                "fixture_hash": fixture_hash,
                "hidden_hash": hidden_hash,
                "skill_hash": skill_hash,
                "candidate9_runtime_hash": candidate_hash,
                "skill_present": skill_dir.joinpath("SKILL.md").is_file(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    started = time.perf_counter()
    try:
        result = subprocess.run(
            launch,
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=protocol["timeout_s"] + 30,
            check=False,
        )
        timed_out = False
    except subprocess.TimeoutExpired as error:
        result = error
        timed_out = True
    elapsed = time.perf_counter() - started

    stdout = result.stdout if not timed_out else (result.stdout or b"")
    stderr = result.stderr if not timed_out else (result.stderr or b"")
    (out / "codex.jsonl").write_bytes(stdout)
    (out / "codex.stderr.txt").write_bytes(stderr)
    final_path = out / "final.md"
    final = final_path.read_text(encoding="utf-8") if final_path.is_file() else ""
    if not final:
        final = stdout.decode("utf-8", errors="replace")[-8000:]
        (out / "final.md").write_text(final, encoding="utf-8")

    hidden = {"status": "NOT RUN", "output": ""}
    if not timed_out:
        hidden_run = subprocess.run(
            [sys.executable, str(hidden_path)],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        hidden = {
            "status": "PASS" if hidden_run.returncode == 0 else "FAIL",
            "output": (hidden_run.stdout + hidden_run.stderr)[-4000:],
            "returncode": hidden_run.returncode,
        }

    usage = parse_usage(stdout.decode("utf-8", errors="replace"))
    claimed = claimed_verdict(final)
    skill_read = "agent-mission-control" in stdout.decode("utf-8", errors="replace").lower() and ".agents" in stdout.decode("utf-8", errors="replace").lower()
    record = {
        "arm": args.arm,
        "case": args.case,
        "timed_out": timed_out,
        "exit_code": None if timed_out else result.returncode,
        "elapsed_s": round(elapsed, 1),
        "claimed_verdict": claimed,
        "hidden": hidden,
        "false_pass": claimed == "PASS" and hidden.get("status") != "PASS",
        "usage": usage,
        "skill_read_mentioned": skill_read,
        "user_interventions": 0,
    }
    (out / "result.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    return 0 if not timed_out else 2


if __name__ == "__main__":
    raise SystemExit(main())
