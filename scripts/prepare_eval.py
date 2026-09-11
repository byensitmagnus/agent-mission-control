#!/usr/bin/env python3
"""Prepare one fresh disposable fixture; never launch an agent or contact a service."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIRS = ("agents", "references", "templates", "assets")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_evaluator():
    cases_bytes = (ROOT / "evals/cases.json").read_bytes()
    rubric_bytes = (ROOT / "evals/rubric.md").read_bytes()
    return json.loads(cases_bytes), digest(cases_bytes + rubric_bytes)


def relative_path(value):
    path = PurePosixPath(value)
    if (not value or path.is_absolute() or ".." in path.parts
            or ":" in value or "\\" in value or str(path) != value
            or any(part.startswith(".") for part in path.parts)):
        raise ValueError(f"unsafe fixture path: {value}")
    return path


def fixture_paths(fixture):
    if not isinstance(fixture, dict) or not fixture:
        raise ValueError("fixture must be a nonempty object")
    paths = []
    seen = set()
    for name, text in fixture.items():
        if not isinstance(name, str) or not isinstance(text, str):
            raise ValueError("fixture paths and contents must be strings")
        path = relative_path(name)
        portable = name.casefold()
        if portable in seen:
            raise ValueError(f"conflicting fixture paths: {name}")
        seen.add(portable)
        paths.append((path, text))
    for path, _ in paths:
        if any(parent.as_posix().casefold() in seen for parent in path.parents):
            raise ValueError(f"conflicting fixture file and directory: {path}")
    return paths


def git_environment():
    # Isolate fixtures from user filters, external repo paths and injected config.
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_ATTR_NOSYSTEM="1")
    return env


def reject_linked_ancestors(path, label):
    for current in (path.absolute(), *path.absolute().parents):
        if not current.exists() and not current.is_symlink():
            continue
        attributes = getattr(current.lstat(), "st_file_attributes", 0)
        if current.is_symlink() or attributes & 0x400:
            raise ValueError(f"linked {label} is not allowed: {current}")


def prepare(case_id, destination, skill_source):
    evaluator, evaluator_hash = load_evaluator()
    cases = evaluator["cases"]
    case = next((item for item in cases if item["id"] == case_id), None)
    if case is None:
        raise ValueError(f"unknown case: {case_id}")
    paths = fixture_paths(case["fixture"])
    reject_linked_ancestors(skill_source, "skill source or ancestor")
    reject_linked_ancestors(destination.parent, "destination parent or ancestor")
    if not (skill_source / "SKILL.md").is_file():
        raise ValueError("skill source has no SKILL.md")
    # Fixtures and copied skill files are data, not arbitrary filesystem imports.
    sources = [skill_source / "SKILL.md"]
    for name in RUNTIME_DIRS:
        directory = skill_source / name
        if directory.exists():
            sources.extend([directory, *directory.rglob("*")])
    for source in sources:
        if source.is_symlink() or getattr(source.lstat(), "st_file_attributes", 0) & 0x400:
            raise ValueError(f"linked skill input is not allowed: {source}")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"destination must be new: {destination}")
    target = destination.resolve()
    for name in RUNTIME_DIRS:
        copied = (skill_source / name).resolve()
        if target == copied or copied in target.parents:
            raise ValueError("destination cannot be inside a copied skill directory")
    destination.mkdir(parents=True, exist_ok=False)
    workspace = destination / "workspace"
    workspace.mkdir()
    for relative, text in paths:
        target = workspace.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")

    skill = workspace / ".agents/skills/agent-mission-control"
    skill.mkdir(parents=True)
    shutil.copy2(skill_source / "SKILL.md", skill / "SKILL.md")
    for name in RUNTIME_DIRS:
        if (skill_source / name).is_dir():
            shutil.copytree(skill_source / name, skill / name)

    # Local fixture history only: no remote, credentials, user hooks or signing.
    git = ["git", "-c", "core.hooksPath=", "-c", "core.attributesFile=",
           "-c", "commit.gpgsign=false",
           "-c", "user.name=AMC Eval", "-c", "user.email=eval@example.invalid"]
    def run(*args):
        return subprocess.run(git + list(args), cwd=workspace, check=True,
                              capture_output=True, text=True, env=git_environment()).stdout.strip()
    run("init", "--template=", "--quiet")
    run("add", "--", ".")
    run("commit", "--quiet", "-m", "Disposable eval fixture")
    fixture_commit = run("rev-parse", "HEAD")
    activation = case["activation"]
    skill_instruction = ("Use $agent-mission-control from "
                         ".agents/skills/agent-mission-control.\n\n"
                         if activation == "explicit" else "")
    prompt = (skill_instruction + case["prompt"] + "\n\n"
              "Work only in this disposable workspace. Local inspection, edits and "
              "safe tests are authorized unless the task is read-only. No credentials, "
              "network mutations, push, deploy or publication. Do not edit the installed "
              "skill. Report commands and concrete artifacts.\n")
    (destination / "prompt.txt").write_text(prompt, encoding="utf-8", newline="\n")
    skill_hashes = {path.relative_to(skill).as_posix(): digest(path.read_bytes())
                    for path in sorted(skill.rglob("*")) if path.is_file()}
    manifest = {
        "schema_version": 2, "case": case_id, "activation": activation,
        "fixture_commit": fixture_commit,
        "evaluator_sha256": evaluator_hash,
        "case_definition_sha256": digest(json.dumps(
            case, sort_keys=True, separators=(",", ":")
        ).encode()),
        "prompt_sha256": digest(prompt.encode()),
        "fixture_sha256": {name: digest(text.encode()) for name, text in case["fixture"].items()},
        "skill_files_sha256": skill_hashes,
        "behavioral_verdict": "NOT VERIFIED",
        "note": "Preparation only. No agent has run. Keep this manifest outside subject context."
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case")
    parser.add_argument("destination", type=Path)
    parser.add_argument("--skill-source", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        prepare(args.case, args.destination, args.skill_source)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"FAIL: {error}\nAn incomplete new destination may remain; existing files were not overwritten.\n")
    print("PASS: disposable fixture prepared; behavioral proof NOT VERIFIED")


if __name__ == "__main__":
    main()
