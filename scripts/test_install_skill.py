#!/usr/bin/env python3
"""Project installation, preservation and failure controls; no host launches."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from install_skill import HOST_DIRS, file_hashes, fingerprint, install
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

    def test_update_replaces_all_hosts_and_retains_complete_customized_backup(self):
        before = {}
        for host, directory in HOST_DIRS.items():
            destination = self.project / directory / "skills" / "agent-mission-control"
            self.run_install(host)
            (destination / "local-note.txt").write_bytes(f"keep-{host}".encode())
            before[host] = self.run_install(host, check=True)["installed_sha256"]
        (self.project / "AGENTS.md").write_bytes(b"project setting")
        (self.source / "SKILL.md").write_bytes(b"updated skill\r\n")

        backups = set()
        for host, directory in HOST_DIRS.items():
            result = self.run_install(host, update=True, expected_installed_sha256=before[host])
            destination = self.project / directory / "skills" / "agent-mission-control"
            backup = Path(result["backup_path"])
            self.assertEqual(result["status"], "UPDATED")
            self.assertEqual(result["previous_installed_sha256"], before[host])
            self.assertTrue(backup.is_dir())
            self.assertEqual((backup / "local-note.txt").read_bytes(), f"keep-{host}".encode())
            assert_skill_bytes(self, self.source, destination)
            self.assertEqual(self.run_install(host, check=True)["status"], "MATCH")
            backups.add(result["installed_sha256"])
        self.assertEqual(len(backups), 1)
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), b"project setting")

    def test_update_rejects_invalid_or_stale_confirmation_before_writing(self):
        installed = self.run_install()
        destination = Path(installed["path"])
        for digest in (None, "not-a-hash", "0" * 64):
            with self.subTest(digest=digest), self.assertRaises(ValueError):
                self.run_install(update=True, expected_installed_sha256=digest)
            self.assertFalse((self.project / ".amc-skill-backups").exists())
            self.assertTrue(destination.is_dir())
        with self.assertRaises(ValueError):
            self.run_install(check=True, update=True, expected_installed_sha256="0" * 64)
        with self.assertRaises(ValueError):
            self.run_install(expected_installed_sha256=installed["installed_sha256"])
        self.assertEqual(self.run_install(check=True)["installed_sha256"], installed["installed_sha256"])

    def test_update_refuses_source_or_destination_change_while_staging(self):
        installed = self.run_install()
        digest = installed["installed_sha256"]
        destination = Path(installed["path"])
        (self.source / "SKILL.md").write_bytes(b"candidate")

        def source_changes(staged, **kwargs):
            package(staged, **kwargs)
            (self.source / "SKILL.md").write_bytes(b"changed after staging")
        with patch("install_skill.package", side_effect=source_changes):
            with self.assertRaisesRegex(ValueError, "source changed while staging"):
                self.run_install(update=True, expected_installed_sha256=digest)
        self.assertTrue(destination.is_dir())
        self.assertFalse((self.project / ".amc-skill-backups").exists())

        (self.source / "SKILL.md").write_bytes(b"candidate two")
        def destination_changes(staged, **kwargs):
            package(staged, **kwargs)
            (destination / "race.txt").write_bytes(b"other owner")
        with patch("install_skill.package", side_effect=destination_changes):
            with self.assertRaisesRegex(ValueError, "installation changed while staging"):
                self.run_install(update=True, expected_installed_sha256=digest)
        self.assertEqual((destination / "race.txt").read_bytes(), b"other owner")
        self.assertFalse((self.project / ".amc-skill-backups").exists())

    def test_update_activation_failure_rolls_back_or_retains_both_owners(self):
        installed = self.run_install()
        destination = Path(installed["path"])
        old_skill = (destination / "SKILL.md").read_bytes()
        (destination / "local-note.txt").write_bytes(b"keep this too")
        digest = self.run_install(check=True)["installed_sha256"]
        (self.source / "SKILL.md").write_bytes(b"candidate")
        original_rename = Path.rename

        def fail_activation(path, target):
            if path.name == "agent-mission-control" and path.parent.name.startswith(".amc-update-"):
                raise OSError("activation blocked")
            return original_rename(path, target)
        with patch.object(Path, "rename", fail_activation):
            result = self.run_install(update=True, expected_installed_sha256=digest)
        self.assertEqual(result["status"], "ROLLED_BACK")
        self.assertTrue(Path(result["backup_path"]).is_dir())
        self.assertEqual((destination / "SKILL.md").read_bytes(), old_skill)
        self.assertEqual((destination / "local-note.txt").read_bytes(), b"keep this too")

        (self.source / "SKILL.md").write_bytes(b"candidate two")
        def competing_owner(path, target):
            result = original_rename(path, target)
            if path == destination:
                destination.mkdir()
                (destination / "SKILL.md").write_bytes(b"new owner")
            return result
        with patch.object(Path, "rename", competing_owner):
            result = self.run_install(update=True, expected_installed_sha256=digest)
        self.assertEqual(result["status"], "RECOVERY_REQUIRED")
        self.assertTrue(Path(result["backup_path"]).is_dir())
        self.assertEqual((Path(result["backup_path"]) / "SKILL.md").read_bytes(), old_skill)
        self.assertEqual((Path(result["backup_path"]) / "local-note.txt").read_bytes(), b"keep this too")
        self.assertEqual((destination / "SKILL.md").read_bytes(), b"new owner")

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

    def test_update_refuses_linked_backup_directory(self):
        installed = self.run_install()
        original_skill = Path(installed["path"]).joinpath("SKILL.md").read_bytes()
        (self.source / "SKILL.md").write_bytes(b"candidate")
        external = self.root / "external-backups"
        external.mkdir()
        try: os.symlink(external, self.project / ".amc-skill-backups", target_is_directory=True)
        except OSError as error: self.skipTest(f"cannot create symlink: {error}")
        with self.assertRaises(ValueError):
            self.run_install(update=True, expected_installed_sha256=installed["installed_sha256"])
        self.assertEqual(Path(installed["path"]).joinpath("SKILL.md").read_bytes(), original_skill)

    def test_update_refuses_match_if_build_record_missing_or_tampered(self):
        installed = self.run_install()
        destination = Path(installed["path"])
        checked = self.run_install(check=True)
        self.assertEqual(checked["status"], "MATCH")
        self.assertTrue(checked["content_match"])
        self.assertTrue(checked["build_record_self_consistent"])
        self.assertTrue(checked["trusted_source_match"])

        # Case 1: Runtime files match, but BUILD_RECORD.json missing during update
        (destination / "BUILD_RECORD.json").unlink()
        digest = fingerprint(file_hashes(destination))
        res = self.run_install(update=True, expected_installed_sha256=digest)
        self.assertNotEqual(res["status"], "MATCH")
        self.assertEqual(res["status"], "BUILD_RECORD_INVALID")
        self.assertEqual(res["build_record_status"], "MISSING")
        self.assertTrue(res["content_match"])
        self.assertFalse(res["build_record_self_consistent"])

        # Re-install cleanly
        import shutil
        shutil.rmtree(destination)
        installed = self.run_install()

        # Case 2: Runtime files match, but BUILD_RECORD.json tampered during update
        br_path = destination / "BUILD_RECORD.json"
        data = json.loads(br_path.read_text(encoding="utf-8"))
        data["runtime_content_digest"] = "0" * 64
        br_path.write_text(json.dumps(data), encoding="utf-8")
        digest_tampered = fingerprint(file_hashes(destination))
        res2 = self.run_install(update=True, expected_installed_sha256=digest_tampered)
        self.assertNotEqual(res2["status"], "MATCH")
        self.assertEqual(res2["status"], "BUILD_RECORD_INVALID")
        self.assertEqual(res2["build_record_status"], "TAMPERED")
        self.assertTrue(res2["content_match"])
        self.assertFalse(res2["build_record_self_consistent"])


if __name__ == "__main__": unittest.main()
