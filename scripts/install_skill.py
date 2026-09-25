#!/usr/bin/env python3
"""Install or check the current AMC source in one existing project. No host config edits."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path

from package_plugin import (
    COPY_DIRS, PLUGIN_NAME, REQUIRED_FILES, SKILL_DIR, SOURCE_ROOT, VERSION,
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
SHA256 = re.compile(r"[0-9a-f]{64}$", re.IGNORECASE)


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


def update_backup(project: Path) -> Path:
    parent = project / ".amc-skill-backups"
    _reject_linked_chain(parent, "backup")
    parent.mkdir(exist_ok=True)
    _reject_linked_chain(parent, "backup")
    return Path(tempfile.mkdtemp(prefix=f"{PLUGIN_NAME}-", dir=parent))


def activate_update(destination: Path, staged: Path, project: Path,
                    previous_sha256: str) -> dict:
    backup = update_backup(project)
    backup.rmdir()
    destination.rename(backup)
    if destination.exists() or destination.is_symlink():
        return {
            "status": "RECOVERY_REQUIRED", "path": str(destination),
            "backup_path": str(backup), "previous_installed_sha256": previous_sha256,
            "error": "destination was claimed before activation",
        }
    try:
        staged.rename(destination)
    except OSError as error:
        result = {
            "status": "RECOVERY_REQUIRED", "path": str(destination),
            "backup_path": str(backup), "previous_installed_sha256": previous_sha256,
            "error": f"activation failed: {error}",
        }
        if not destination.exists() and not destination.is_symlink():
            try:
                backup.rename(destination)
            except OSError as restore_error:
                result["error"] += f"; restore failed: {restore_error}"
            else:
                result["status"] = "ROLLED_BACK"
                result["backup_path"] = str(destination)
                result["restored_path"] = str(destination)
        return result
    return {
        "status": "UPDATED", "path": str(destination),
        "backup_path": str(backup), "previous_installed_sha256": previous_sha256,
    }


def install(project: Path, host: str, *, check: bool = False,
            update: bool = False, expected_installed_sha256: str | None = None,
            source: Path | None = None) -> dict:
    if host not in HOST_DIRS:
        raise ValueError(f"unsupported host: {host}")
    if check and update:
        raise ValueError("--check and --update cannot be used together")
    if expected_installed_sha256 is not None and not update:
        raise ValueError("--expected-installed-sha256 requires --update")
    if update and (expected_installed_sha256 is None or not SHA256.fullmatch(expected_installed_sha256)):
        raise ValueError("--update requires a 64-character SHA-256 digest")
    if expected_installed_sha256 is not None:
        expected_installed_sha256 = expected_installed_sha256.lower()
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
    expected = file_hashes(origin / SKILL_DIR, selected=True)
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

    if update:
        if not destination.is_dir():
            raise ValueError(f"installation is missing or not a directory: {destination}")
        actual = file_hashes(destination)
        previous_sha256 = fingerprint(actual)
        if previous_sha256 != expected_installed_sha256:
            raise ValueError("installed SHA-256 does not match --expected-installed-sha256")
        if actual == expected:
            result.update(status="MATCH", installed_sha256=previous_sha256, differences=[])
            return result
        # Stage outside discovery directories, then re-read both mutable inputs
        # before moving the original installation.
        with tempfile.TemporaryDirectory(prefix=".amc-update-", dir=project) as temporary:
            staged = Path(temporary) / PLUGIN_NAME
            package(staged, source=source, package_format="skill")
            _validate_source(origin)
            if file_hashes(origin / SKILL_DIR, selected=True) != expected or file_hashes(staged) != expected:
                raise ValueError("source changed while staging; installation was not activated")
            _reject_linked_chain(destination, "installation")
            if fingerprint(file_hashes(destination)) != previous_sha256:
                raise ValueError("installation changed while staging; update was not activated")
            activated = activate_update(destination, staged, project, previous_sha256)
        result.update(activated, source_sha256=fingerprint(expected))
        if activated["status"] == "UPDATED":
            result["installed_sha256"] = fingerprint(expected)
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
    parser.add_argument("--update", action="store_true", help="replace the reviewed existing installation")
    parser.add_argument("--expected-installed-sha256", metavar="DIGEST")
    parser.add_argument(
        "--source",
        type=Path,
        help="trusted local source snapshot; omitted uses the canonical repository check",
    )
    args = parser.parse_args()
    try:
        result = install(args.project, args.host, check=args.check, update=args.update,
                         expected_installed_sha256=args.expected_installed_sha256,
                         source=args.source)
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"MATCH", "INSTALLED", "UPDATED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
