#!/usr/bin/env python3
"""Project installation, preservation and failure controls; no host launches."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from install_skill import HOST_DIRS, install
from package_plugin import package
from test_package_plugin import assert_skill_bytes, make_source


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = make_source(self.root)
        self.project = self.root / "project with spaces"
        self.project.mkdir()

    def run_install(self, host="codex", **kwargs):
        return install(self.project, host, source=self.source, **kwargs)

    def test_five_hosts_preserve_files_and_have_identical_checked_bytes(self):
        for name in ("AGENTS.md", "CLAUDE.md", "config.toml"):
            (self.project / name).write_bytes(b"user settings\r\n")
        identities = set()
        for host, directory in HOST_DIRS.items():
            result = self.run_install(host)
            destination = self.project / directory / "skills" / "agent-mission-control"
            self.assertEqual(result["path"], str(destination))
            self.assertEqual(result["status"], "INSTALLED")
            self.assertIn("builder_version", result)
            self.assertNotIn("source_version", result)
            self.assertEqual(result["host_discovery"], "NOT VERIFIED")
            assert_skill_bytes(self, self.source, destination)
            checked = self.run_install(host, check=True)
            self.assertEqual(checked["status"], "MATCH")
            self.assertEqual(checked["source_sha256"], checked["installed_sha256"])
            identities.add(checked["installed_sha256"])
        self.assertEqual(len(identities), 1)
        for name in ("AGENTS.md", "CLAUDE.md", "config.toml"):
            self.assertEqual((self.project / name).read_bytes(), b"user settings\r\n")
        self.assertFalse(list(self.project.glob(".amc-install-*")))

    def test_read_only_check_detects_missing_changed_removed_and_extra_files(self):
        self.assertEqual(self.run_install(check=True)["status"], "MISSING")
        self.assertEqual(list(self.project.iterdir()), [])
        destination = Path(self.run_install()["path"])
        (destination / "SKILL.md").write_bytes(b"custom instructions")
        (destination / "LICENSE").unlink()
        (destination / "extra.txt").write_bytes(b"keep")
        checked = self.run_install(check=True)
        self.assertEqual(checked["status"], "DIFFERENT")
        self.assertEqual(checked["differences"], ["LICENSE", "SKILL.md", "extra.txt"])
        with self.assertRaises(FileExistsError): self.run_install()
        self.assertEqual((destination / "SKILL.md").read_bytes(), b"custom instructions")
        self.assertEqual((destination / "extra.txt").read_bytes(), b"keep")

    def test_invalid_inputs_and_unverified_default_source_do_not_write(self):
        for project, host in ((self.project, "invented"), (self.root / "absent", "kimi"), (self.source, "codex")):
            with self.subTest(project=project, host=host), self.assertRaises(ValueError):
                install(project, host, source=self.source)
        with patch("install_skill.SOURCE_ROOT", self.source):
            for check in (False, True):
                with self.assertRaises(ValueError): install(self.project, "grok", check=check)
        self.assertFalse((self.source / ".agents").exists())
        self.assertFalse((self.root / "absent").exists())
        self.assertEqual(list(self.project.iterdir()), [])

    def test_copy_failure_does_not_expose_skill(self):
        with patch("package_plugin.shutil.copy2", side_effect=OSError("disk full")):
            with self.assertRaises(OSError): self.run_install("claude-code")
        self.assertEqual(list(self.project.iterdir()), [])

    def test_move_failure_leaves_non_invocable_partial_and_refuses_overwrite(self):
        with patch.object(Path, "rename", side_effect=OSError("move failed")):
            with self.assertRaises(OSError): self.run_install("cursor")
        destination = self.project / ".cursor/skills/agent-mission-control"
        self.assertTrue(destination.is_dir())
        self.assertFalse((destination / "SKILL.md").exists())
        self.assertEqual(self.run_install("cursor", check=True)["status"], "DIFFERENT")
        with self.assertRaises(FileExistsError): self.run_install("cursor")

    def test_changed_staged_bytes_are_not_activated(self):
        def changed(destination, **kwargs):
            package(destination, **kwargs)
            (destination / "SKILL.md").write_bytes(b"raced")
        with patch("install_skill.package", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "source changed"): self.run_install("kimi")
        self.assertEqual(list(self.project.iterdir()), [])

    def test_destination_created_during_staging_is_preserved(self):
        destination = self.project / ".agents/skills/agent-mission-control"
        def competing(staged, **kwargs):
            package(staged, **kwargs)
            destination.mkdir(parents=True)
            (destination / "SKILL.md").write_bytes(b"other owner")
        with patch("install_skill.package", side_effect=competing):
            with self.assertRaises(FileExistsError): self.run_install()
        self.assertEqual((destination / "SKILL.md").read_bytes(), b"other owner")

    def test_linked_project_installation_and_extra_file_are_rejected(self):
        link = self.root / "project-link"
        try: os.symlink(self.project, link, target_is_directory=True)
        except OSError as error: self.skipTest(f"cannot create symlink: {error}")
        with self.assertRaises(ValueError): install(link, "codex", source=self.source)
        os.symlink(self.root / "outside", self.project / ".kimi", target_is_directory=True)
        with self.assertRaises(ValueError): self.run_install("kimi")
        destination = Path(self.run_install("grok")["path"])
        os.symlink(self.source / "SKILL.md", destination / "extra.md")
        with self.assertRaises(ValueError): self.run_install("grok", check=True)


if __name__ == "__main__": unittest.main()
