#!/usr/bin/env python3
"""Self-checks for package_plugin.py."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from package_plugin import COPY_DIRS, PLUGIN_NAME, package


def make_source(root: Path) -> Path:
    source = root / "source"
    source.mkdir()
    (source / "SKILL.md").write_text("---\nname: agent-mission-control\ndescription: Test\n---\n", encoding="utf-8")
    (source / "LICENSE").write_text("MIT\n", encoding="utf-8")
    for name in COPY_DIRS:
        (source / name).mkdir()
    return source


class PackagePluginTests(unittest.TestCase):
    def test_packages_allowlist_and_refuses_existing_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "new" / "nested" / PLUGIN_NAME
            package(destination)
            manifest = json.loads(
                (destination / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertTrue((destination / "skills" / PLUGIN_NAME / "SKILL.md").is_file())
            self.assertTrue((destination / "LICENSE").is_file())
            self.assertFalse((destination / ".codex").exists())

            sentinel = destination / "sentinel.txt"
            sentinel.write_text("keep", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                package(destination)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_rejects_linked_source_before_destination_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = make_source(root)
            external = root / "external.txt"
            external.write_text("external", encoding="utf-8")
            link = source / "assets" / "external-link"
            try:
                os.symlink(external, link)
            except OSError as error:
                self.skipTest(f"this host cannot create a test symlink: {error}")

            destination = root / "output" / PLUGIN_NAME
            destination.parent.mkdir()
            with self.assertRaises(ValueError):
                package(destination, source)
            self.assertFalse(destination.exists())

    def test_refuses_recursive_destination_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = make_source(Path(temporary))
            destination = source / "assets" / PLUGIN_NAME
            with self.assertRaises(ValueError):
                package(destination, source)
            self.assertFalse(destination.exists())

    def test_leaves_partial_destination_after_copy_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = make_source(root)
            destination = root / PLUGIN_NAME
            with patch("package_plugin.shutil.copy2", side_effect=OSError("copy failed")):
                with self.assertRaises(OSError):
                    package(destination, source)
            self.assertTrue(destination.is_dir())


if __name__ == "__main__":
    unittest.main()
