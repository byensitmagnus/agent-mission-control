#!/usr/bin/env python3
"""Non-skipping Windows junction controls for packaging and installation."""
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from install_skill import install
from package_plugin import (
    FILE_ATTRIBUTE_REPARSE_POINT,
    PLUGIN_NAME,
    package,
)
from test_package_plugin import make_source


def create_junction(link: Path, target: Path) -> None:
    result = subprocess.run(
        ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(
            f"junction fixture creation failed ({result.returncode}): "
            f"{result.stdout}{result.stderr}"
        )
    attributes = getattr(link.lstat(), "st_file_attributes", 0)
    if not attributes & FILE_ATTRIBUTE_REPARSE_POINT:
        raise AssertionError(f"fixture is not a reparse point: {link}")


def remove_junction(link: Path) -> None:
    if link.exists() or link.is_symlink():
        os.rmdir(link)


class WindowsReparseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertEqual(os.name, "nt", "junction controls must run on Windows")
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = make_source(self.root)

    def junction(self, name: str, target: Path) -> Path:
        link = self.root / name
        create_junction(link, target)
        self.addCleanup(remove_junction, link)
        return link

    def test_package_rejects_junction_destination_ancestor(self) -> None:
        outside = self.root / "outside-package"
        outside.mkdir()
        junction = self.junction("package-junction", outside)

        with self.assertRaisesRegex(ValueError, "destination contains a linked ancestor"):
            package(junction / PLUGIN_NAME, source=self.source, package_format="skill")

        self.assertFalse((outside / PLUGIN_NAME).exists())

    def test_install_rejects_junction_host_directory(self) -> None:
        project = self.root / "project"
        project.mkdir()
        outside = self.root / "outside-host"
        outside.mkdir()
        sentinel = outside / "sentinel.txt"
        sentinel.write_text("untouched", encoding="utf-8")
        junction = project / ".agents"
        create_junction(junction, outside)
        self.addCleanup(remove_junction, junction)

        with self.assertRaisesRegex(ValueError, "installation contains a linked ancestor"):
            install(project, "codex", source=self.source)

        self.assertEqual(sentinel.read_text(encoding="utf-8"), "untouched")
        self.assertFalse((outside / "skills").exists())


if __name__ == "__main__":
    unittest.main()
