#!/usr/bin/env python3
"""Install or check the current AMC source in one existing project. No host config edits."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from package_plugin import (
    COPY_DIRS, PLUGIN_NAME, REQUIRED_FILES, SOURCE_ROOT, VERSION,
    _absolute, _is_link, _is_within, _reject_linked_chain,
    _validate_default_source, _validate_source, package,
)

HOST_DIRS = {
    "codex": ".agents",
    "claude-code": ".claude",
    "cursor": ".cursor",
    "grok": ".grok",
    "kimi": ".kimi",
}


def file_hashes(root: Path, selected: bool = False) -> dict[str, str]:
    paths = [root / name for name in REQUIRED_FILES] if selected else []
    trees = [root / name for name in COPY_DIRS] if selected else [root]
    for tree in trees:
        for path in tree.rglob("*"):
            if _is_link(path):
                raise ValueError(f"linked file or directory: {path}")
            if path.is_file():
                paths.append(path)
            elif not path.is_dir():
                raise ValueError(f"unsupported file: {path}")
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(paths)}


def fingerprint(files: dict[str, str]) -> str:
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


def install(project: Path, host: str, *, check: bool = False,
            source: Path | None = None) -> dict:
    if host not in HOST_DIRS:
        raise ValueError(f"unsupported host: {host}")
    project = _absolute(project)
    origin = _absolute(source or SOURCE_ROOT)
    if not project.is_dir():
        raise ValueError(f"project directory is missing: {project}")
    _reject_linked_chain(project, "project")
    destination = project / HOST_DIRS[host] / "skills" / PLUGIN_NAME
    _reject_linked_chain(destination, "installation")
    _validate_source(origin)
    if source is None:
        _validate_default_source(origin)
    if _is_within(project, origin) or _is_within(origin, destination):
        raise ValueError("installation project and source must not overlap the installed skill")
    expected = file_hashes(origin, selected=True)
    result = {
        "status": "MISSING", "host": host, "path": str(destination),
        "builder_version": VERSION, "source_sha256": fingerprint(expected),
        "host_discovery": "NOT VERIFIED",
    }
    if check:
        if not destination.exists():
            return result
        if not destination.is_dir():
            raise ValueError(f"installation is not a directory: {destination}")
        actual = file_hashes(destination)
        changed = sorted(key for key in expected.keys() | actual.keys()
                         if expected.get(key) != actual.get(key))
        result.update(status="DIFFERENT" if changed else "MATCH",
                      installed_sha256=fingerprint(actual), differences=changed)
        return result

    if destination.exists():
        raise FileExistsError(f"installation already exists; use --check: {destination}")
    # Stage outside discovery directories. Publish SKILL.md last, by rename, so
    # interrupted copying cannot advertise an incomplete workflow to the host.
    with tempfile.TemporaryDirectory(prefix=".amc-install-", dir=project) as temporary:
        staged = Path(temporary) / PLUGIN_NAME
        package(staged, source=source, package_format="skill")
        if file_hashes(staged) != expected:
            raise ValueError("source changed while packaging; installation was not activated")
        _reject_linked_chain(destination, "installation")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.mkdir(exist_ok=False)
        # ponytail: a move failure leaves an owned, non-invocable partial folder.
        # Inspect/remove that folder before retry; never overwrite a prior install.
        for path in sorted(staged.iterdir()):
            if path.name != "SKILL.md":
                path.rename(destination / path.name)
        (staged / "SKILL.md").rename(destination / "SKILL.md")
    result.update(status="INSTALLED", installed_sha256=fingerprint(expected))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--host", required=True, choices=HOST_DIRS)
    parser.add_argument("--check", action="store_true", help="read-only byte comparison with this source")
    args = parser.parse_args()
    try:
        result = install(args.project, args.host, check=args.check)
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"MATCH", "INSTALLED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
