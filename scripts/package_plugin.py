#!/usr/bin/env python3
"""Build a local Agent Mission Control plugin bundle at a new destination."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


PLUGIN_NAME = "agent-mission-control"
VERSION = "0.2.0-candidate.1"
COPY_DIRS = ("agents", "references", "templates", "assets")
REQUIRED_FILES = ("SKILL.md", "LICENSE")
FILE_ATTRIBUTE_REPARSE_POINT = 0x400


def _is_link(path: Path) -> bool:
    attributes = getattr(path.lstat(), "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & FILE_ATTRIBUTE_REPARSE_POINT)


def _validate_source(source: Path) -> None:
    for name in REQUIRED_FILES:
        path = source / name
        if not path.is_file() or _is_link(path):
            raise ValueError(f"required source file is missing or linked: {path}")
    for name in COPY_DIRS:
        root = source / name
        if not root.is_dir() or _is_link(root):
            raise ValueError(f"required source directory is missing or linked: {root}")
        for path in root.rglob("*"):
            if _is_link(path):
                raise ValueError(f"linked source path is not allowed: {path}")


def package(destination: Path, source: Path | None = None) -> None:
    source = (source or Path(__file__).resolve().parent.parent).absolute()
    destination = destination.absolute()
    if destination.name != PLUGIN_NAME:
        raise ValueError(f"destination basename must be {PLUGIN_NAME!r}")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"destination already exists: {destination}")

    _validate_source(source)
    target = destination.resolve()
    for name in COPY_DIRS:
        copied = (source / name).resolve()
        if target == copied or copied in target.parents:
            raise ValueError("destination cannot be inside a copied source directory")
    skill = destination / "skills" / PLUGIN_NAME
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir(exist_ok=False)
    (destination / ".codex-plugin").mkdir()
    skill.mkdir(parents=True)
    shutil.copy2(source / "SKILL.md", skill / "SKILL.md")
    for name in COPY_DIRS:
        shutil.copytree(source / name, skill / name)
    shutil.copytree(source / "assets", destination / "assets")
    shutil.copy2(source / "LICENSE", destination / "LICENSE")

    manifest = {
        "name": PLUGIN_NAME,
        "version": VERSION,
        "description": "Coordinate bounded multi-agent software missions with evidence-backed completion.",
        "author": {"name": "Byens IT"},
        "skills": "./skills/",
        "interface": {
            "displayName": "Agent Mission Control",
            "shortDescription": "Coordinate bounded software missions",
            "longDescription": "Plan, delegate, verify, and consolidate bounded software missions.",
            "developerName": "Byens IT",
            "category": "Developer Tools",
            "capabilities": ["Interactive", "Read", "Write"],
            "defaultPrompt": ["Run this software mission with coordinated agents."],
            "brandColor": "#8b5cf6",
            "composerIcon": "./assets/icon-small.svg",
            "logo": "./assets/icon-large.svg",
            "screenshots": [],
        },
    }
    (destination / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {Path(argv[0]).name} DESTINATION", file=sys.stderr)
        return 2
    try:
        package(Path(argv[1]))
    except (ValueError, FileExistsError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
