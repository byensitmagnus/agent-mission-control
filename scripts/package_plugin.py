#!/usr/bin/env python3
"""Build Agent Mission Control skill or Codex plugin packages."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import zipfile
from pathlib import Path


PLUGIN_NAME = "agent-mission-control"
VERSION = "0.2.0-candidate.12"
EXPECTED_ORIGIN = "https://github.com/byensitmagnus/agent-mission-control.git"
SOURCE_ROOT = Path(os.path.abspath(__file__)).parent.parent
# Runtime lives in its own folder so `npx skills add` copies only the skill.
SKILL_DIR = Path("skills") / PLUGIN_NAME
COPY_DIRS = ("agents", "references", "templates", "assets")
REQUIRED_FILES = ("SKILL.md", "LICENSE")
PACKAGE_FORMATS = ("skill", "plugin")
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ROUTE_DESCRIPTION = (
    "One lead works directly. Use a specialist for focused expertise or a fresh context. "
    "Fan out only independent jobs. Isolate parallel writers."
)
PRODUCT_DESCRIPTION = (
    "Use for a coding bug, feature, resume, or investigation that must show which checks ran. "
    + ROUTE_DESCRIPTION
)
DEFAULT_PROMPT = (
    "Use Agent Mission Control as one workflow for a bug, feature, resume, or investigation. "
    "Choose the smallest useful workflow and finish with verified evidence. "
    + ROUTE_DESCRIPTION
)


def _absolute(path: Path) -> Path:
    return Path(os.path.abspath(path))


def _is_link(path: Path) -> bool:
    attributes = getattr(path.lstat(), "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & FILE_ATTRIBUTE_REPARSE_POINT)


def _reject_linked_chain(path: Path, label: str) -> None:
    for candidate in (path, *path.parents):
        if (candidate.exists() or candidate.is_symlink()) and _is_link(candidate):
            raise ValueError(f"{label} contains a linked ancestor: {candidate}")


def _is_within(path: Path, root: Path) -> bool:
    path = path.resolve(strict=False)
    root = root.resolve(strict=False)
    return path == root or root in path.parents


def _validate_source(source: Path) -> None:
    if not source.is_dir():
        raise ValueError(f"source directory is missing: {source}")
    _reject_linked_chain(source, "source")
    skill = source / SKILL_DIR
    if not skill.is_dir() or _is_link(skill) or _is_link(skill.parent):
        raise ValueError(f"required skill directory is missing or linked: {skill}")
    for name in REQUIRED_FILES:
        path = skill / name
        if not path.is_file() or _is_link(path):
            raise ValueError(f"required source file is missing or linked: {path}")
    for name in COPY_DIRS:
        root = skill / name
        if not root.is_dir() or _is_link(root):
            raise ValueError(f"required source directory is missing or linked: {root}")
        for path in root.rglob("*"):
            if _is_link(path):
                raise ValueError(f"linked source path is not allowed: {path}")
            if not path.is_dir() and not path.is_file():
                raise ValueError(f"unsupported source path is not allowed: {path}")


def _git(source: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ("git", "-C", str(source), *args),
            capture_output=True,
            check=False,
            text=True,
            env=_git_environment(),
        )
    except OSError as error:
        raise ValueError(f"cannot verify default source provenance: {error}") from error
    if result.returncode:
        detail = result.stderr.strip() or "git command failed"
        raise ValueError(f"cannot verify default source provenance: {detail}")
    return result.stdout.strip()


def _git_environment() -> dict[str, str]:
    environment = {
        key: value for key, value in os.environ.items() if not key.upper().startswith("GIT_")
    }
    environment.update(
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_ATTR_NOSYSTEM="1",
    )
    return environment


def _validate_default_source(source: Path) -> None:
    top_level = _absolute(Path(_git(source, "rev-parse", "--show-toplevel")))
    try:
        same_root = source.samefile(top_level)
    except OSError:
        same_root = False
    if not same_root:
        raise ValueError(f"default source is not the repository root: {source}")
    origin = _git(source, "config", "--local", "--no-includes", "--get", "remote.origin.url")
    if origin not in {EXPECTED_ORIGIN, EXPECTED_ORIGIN.removesuffix(".git")}:
        raise ValueError(f"unexpected default source origin: {origin!r}")


def _copy_skill(source: Path, destination: Path) -> None:
    skill = source / SKILL_DIR
    shutil.copy2(skill / "SKILL.md", destination / "SKILL.md")
    for name in COPY_DIRS:
        shutil.copytree(skill / name, destination / name)
    shutil.copy2(skill / "LICENSE", destination / "LICENSE")


def _write_manifest(destination: Path) -> None:
    manifest = {
        "name": PLUGIN_NAME,
        "version": VERSION,
        "description": PRODUCT_DESCRIPTION,
        "author": {"name": "Byens IT"},
        "license": "MIT",
        "repository": "https://github.com/byensitmagnus/agent-mission-control",
        "skills": "./skills/",
        "interface": {
            "displayName": "Agent Mission Control",
            "shortDescription": "Direct coding, focused specialists and checked evidence",
            "longDescription": PRODUCT_DESCRIPTION,
            "developerName": "Byens IT",
            "category": "Developer Tools",
            "capabilities": ["Interactive", "Read", "Write"],
            "defaultPrompt": [DEFAULT_PROMPT],
            "brandColor": "#8b5cf6",
            "composerIcon": "./assets/icon-small.svg",
            "logo": "./assets/icon-large.svg",
            "screenshots": [],
        },
    }
    (destination / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def _zip_info(name: str, directory: bool) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, ZIP_TIMESTAMP)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_STORED
    mode = stat.S_IFDIR | 0o755 if directory else stat.S_IFREG | 0o644
    info.external_attr = mode << 16
    if directory:
        info.external_attr |= 0x10
    return info


def _write_archive(destination: Path, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    with archive.open("xb") as output:
        with zipfile.ZipFile(output, "w") as bundle:
            root_name = f"{destination.name}/"
            bundle.writestr(_zip_info(root_name, True), b"")
            paths = sorted(destination.rglob("*"), key=lambda path: path.relative_to(destination).as_posix())
            for path in paths:
                name = root_name + path.relative_to(destination).as_posix()
                if path.is_dir():
                    bundle.writestr(_zip_info(name + "/", True), b"")
                else:
                    bundle.writestr(_zip_info(name, False), path.read_bytes())


def package(
    destination: Path,
    source: Path | None = None,
    package_format: str = "plugin",
    archive: Path | None = None,
) -> None:
    explicit_source = source is not None
    source = _absolute(source or SOURCE_ROOT)
    destination = _absolute(destination)
    archive = _absolute(archive) if archive is not None else None

    if package_format not in PACKAGE_FORMATS:
        raise ValueError(f"unsupported package format: {package_format!r}")
    if destination.name != PLUGIN_NAME:
        raise ValueError(f"destination basename must be {PLUGIN_NAME!r}")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"destination already exists: {destination}")
    _reject_linked_chain(destination.parent, "destination")
    _validate_source(source)
    if not explicit_source:
        _validate_default_source(source)
    if _is_within(destination, source):
        raise ValueError("destination cannot be inside the source directory")

    if archive is not None:
        if archive.suffix.lower() != ".zip":
            raise ValueError("archive must use the .zip extension")
        if archive.exists() or archive.is_symlink():
            raise FileExistsError(f"archive already exists: {archive}")
        _reject_linked_chain(archive.parent, "archive destination")
        if _is_within(archive, source) or _is_within(archive, destination):
            raise ValueError("archive cannot be inside the source or package destination")

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir(exist_ok=False)
    if package_format == "skill":
        _copy_skill(source, destination)
    else:
        (destination / ".codex-plugin").mkdir()
        skill = destination / "skills" / PLUGIN_NAME
        skill.mkdir(parents=True)
        _copy_skill(source, skill)
        shutil.copytree(source / SKILL_DIR / "assets", destination / "assets")
        shutil.copy2(source / SKILL_DIR / "LICENSE", destination / "LICENSE")
        _write_manifest(destination)

    if archive is not None:
        _write_archive(destination, archive)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog=Path(argv[0]).name, description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--format", choices=PACKAGE_FORMATS, default="plugin", dest="package_format")
    parser.add_argument("--archive", type=Path, metavar="NEW.zip")
    parser.add_argument(
        "--source",
        type=Path,
        help="trusted local source snapshot; omitted uses the canonical repository check",
    )
    try:
        args = parser.parse_args(argv[1:])
    except SystemExit as error:
        return int(error.code)
    try:
        package(
            args.destination,
            source=args.source,
            package_format=args.package_format,
            archive=args.archive,
        )
    except (ValueError, FileExistsError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
