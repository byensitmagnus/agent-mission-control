#!/usr/bin/env python3
"""Self-checks for package_plugin.py."""

import json
import os
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from package_plugin import COPY_DIRS, EXPECTED_ORIGIN, PLUGIN_NAME, VERSION, package


SKILL_BYTES = b"---\r\nname: agent-mission-control\r\ndescription: Test\r\n---\r\n"
FIXTURE_BYTES = b"fixture\x00\r\n\xff"


def make_source(root: Path) -> Path:
    source = root / "source"
    source.mkdir(parents=True)
    (source / "SKILL.md").write_bytes(SKILL_BYTES)
    (source / "LICENSE").write_bytes(b"MIT\r\n")
    for name in COPY_DIRS:
        directory = source / name
        (directory / "nested").mkdir(parents=True)
        (directory / "nested" / "fixture.bin").write_bytes(FIXTURE_BYTES + name.encode())
    return source


def assert_skill_bytes(test: unittest.TestCase, source: Path, skill: Path) -> None:
    test.assertEqual((skill / "SKILL.md").read_bytes(), (source / "SKILL.md").read_bytes())
    test.assertEqual((skill / "LICENSE").read_bytes(), (source / "LICENSE").read_bytes())
    for name in COPY_DIRS:
        expected = source / name / "nested" / "fixture.bin"
        actual = skill / name / "nested" / "fixture.bin"
        test.assertEqual(actual.read_bytes(), expected.read_bytes())


def init_repo(path: Path, origin: str | None = None) -> None:
    subprocess.run(("git", "init", "-q", str(path)), check=True)
    if origin is not None:
        subprocess.run(("git", "-C", str(path), "remote", "add", "origin", origin), check=True)


class PackagePluginTests(unittest.TestCase):
    def test_default_packages_genuine_plugin_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "new" / "nested" / PLUGIN_NAME
            package(destination)
            manifest = json.loads(
                (destination / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["name"], PLUGIN_NAME)
            self.assertEqual(manifest["version"], VERSION)
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertTrue((destination / "skills" / PLUGIN_NAME / "SKILL.md").is_file())
            self.assertTrue((destination / "assets" / "icon-small.svg").is_file())
            self.assertFalse((destination / ".codex").exists())
            self.assertNotRegex(json.dumps(manifest), r"coordinated agents|multi-agent software missions")
            self.assertIn("smallest useful execution graph", manifest["description"])
            self.assertIn("verified evidence", manifest["interface"]["defaultPrompt"][0])
            self.assertIn("one workflow", manifest["interface"]["defaultPrompt"][0])
            self.assertNotIn("MISSION.md", {p.relative_to(destination / "skills" / PLUGIN_NAME).as_posix() for p in (destination / "skills" / PLUGIN_NAME).rglob("*") if p.is_file()})

            sentinel = destination / "sentinel.txt"
            sentinel.write_text("keep", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                package(destination)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_skill_and_plugin_runtime_bytes_match(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "skill" / PLUGIN_NAME
            plugin = Path(temporary) / "plugin" / PLUGIN_NAME
            package(skill, package_format="skill")
            package(plugin, package_format="plugin")
            plugin_skill = plugin / "skills" / PLUGIN_NAME
            skill_files = {
                path.relative_to(skill).as_posix()
                for path in skill.rglob("*")
                if path.is_file()
            }
            plugin_files = {
                path.relative_to(plugin_skill).as_posix()
                for path in plugin_skill.rglob("*")
                if path.is_file()
            }
            self.assertEqual(skill_files, plugin_files)
            for name in sorted(skill_files):
                self.assertEqual((skill / name).read_bytes(), (plugin_skill / name).read_bytes(), name)

    def test_explicit_trusted_snapshot_preserves_source_and_fixture_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = make_source(root)
            destination = root / "output" / PLUGIN_NAME
            package(destination, source, package_format="skill")
            assert_skill_bytes(self, source, destination)
            self.assertFalse((destination / ".codex-plugin").exists())

    def test_plugin_package_preserves_nested_source_and_fixture_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = make_source(root)
            destination = root / "output" / PLUGIN_NAME
            package(destination, source)
            assert_skill_bytes(self, source, destination / "skills" / PLUGIN_NAME)
            self.assertEqual(
                (destination / "assets" / "nested" / "fixture.bin").read_bytes(),
                (source / "assets" / "nested" / "fixture.bin").read_bytes(),
            )

    def test_zip_archives_are_byte_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = make_source(root)
            first = root / "first" / PLUGIN_NAME
            second = root / "second" / PLUGIN_NAME
            first_zip = root / "first.zip"
            second_zip = root / "second.zip"
            package(first, source, package_format="skill", archive=first_zip)
            package(second, source, package_format="skill", archive=second_zip)
            self.assertEqual(first_zip.read_bytes(), second_zip.read_bytes())
            with zipfile.ZipFile(first_zip) as bundle:
                self.assertEqual(
                    bundle.read(f"{PLUGIN_NAME}/SKILL.md"),
                    SKILL_BYTES,
                )
                self.assertTrue(all(item.date_time == (1980, 1, 1, 0, 0, 0) for item in bundle.infolist()))
                self.assertTrue(all(item.compress_type == zipfile.ZIP_STORED for item in bundle.infolist()))

    def test_existing_archive_is_refused_before_destination_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = make_source(root)
            destination = root / "output" / PLUGIN_NAME
            archive = root / "existing.zip"
            archive.write_bytes(b"keep")
            with self.assertRaises(FileExistsError):
                package(destination, source, archive=archive)
            self.assertFalse(destination.exists())
            self.assertEqual(archive.read_bytes(), b"keep")

    def test_rejects_linked_source_descendant_before_destination_creation(self) -> None:
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
            with self.assertRaises(ValueError):
                package(destination, source)
            self.assertFalse(destination.exists())

    def test_rejects_linked_source_and_destination_ancestors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = make_source(root)
            source_link = root / "source-link"
            output = root / "real-output"
            output.mkdir()
            output_link = root / "output-link"
            try:
                os.symlink(source, source_link, target_is_directory=True)
                os.symlink(output, output_link, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"this host cannot create directory symlinks: {error}")

            destination = root / "safe" / PLUGIN_NAME
            with self.assertRaises(ValueError):
                package(destination, source_link)
            self.assertFalse(destination.exists())

            linked_destination = output_link / PLUGIN_NAME
            with self.assertRaises(ValueError):
                package(linked_destination, source)
            self.assertFalse(linked_destination.exists())

            archive_destination = root / "archive-safe" / PLUGIN_NAME
            linked_archive = output_link / "package.zip"
            with self.assertRaises(ValueError):
                package(archive_destination, source, archive=linked_archive)
            self.assertFalse(archive_destination.exists())
            self.assertFalse(linked_archive.exists())

    def test_default_source_without_git_is_refused_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = make_source(root)
            destination = root / "output" / PLUGIN_NAME
            with patch("package_plugin.SOURCE_ROOT", source):
                with self.assertRaises(ValueError):
                    package(destination)
            self.assertFalse(destination.exists())

    def test_default_source_must_be_exact_git_root_with_expected_raw_origin(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            repository.mkdir()
            init_repo(repository, EXPECTED_ORIGIN)
            nested_source = make_source(repository)
            nested_destination = root / "nested-output" / PLUGIN_NAME
            with patch("package_plugin.SOURCE_ROOT", nested_source):
                with self.assertRaisesRegex(ValueError, "repository root"):
                    package(nested_destination)
            self.assertFalse(nested_destination.exists())

            wrong_source = make_source(root / "wrong")
            init_repo(wrong_source, "alias:agent-mission-control.git")
            wrong_destination = root / "wrong-output" / PLUGIN_NAME
            injected = {
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "url.https://github.com/byensitmagnus/.insteadof",
                "GIT_CONFIG_VALUE_0": "alias:",
            }
            with patch.dict(os.environ, injected):
                with patch("package_plugin.SOURCE_ROOT", wrong_source):
                    with self.assertRaisesRegex(ValueError, "unexpected default source origin"):
                        package(wrong_destination)
            self.assertFalse(wrong_destination.exists())

    def test_default_source_accepts_canonical_https_spellings_only(self) -> None:
        origins = (
            (EXPECTED_ORIGIN, True),
            (EXPECTED_ORIGIN.removesuffix(".git"), True),
            (EXPECTED_ORIGIN + ".evil", False),
            (EXPECTED_ORIGIN.replace("github.com", "github.com.example.invalid"), False),
            (EXPECTED_ORIGIN.replace("byensitmagnus", "another-owner"), False),
            (EXPECTED_ORIGIN.replace("https://", "http://"), False),
        )
        for origin, accepted in origins:
            with self.subTest(origin=origin), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source = make_source(root)
                init_repo(source, origin)
                destination = root / "output" / PLUGIN_NAME
                with patch("package_plugin.SOURCE_ROOT", source):
                    if accepted:
                        package(destination, package_format="skill")
                        assert_skill_bytes(self, source, destination)
                    else:
                        with self.assertRaisesRegex(ValueError, "unexpected default source origin"):
                            package(destination, package_format="skill")
                        self.assertFalse(destination.exists())

    def test_default_source_ignores_injected_git_repository_environment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = make_source(root)
            init_repo(source, EXPECTED_ORIGIN)
            unrelated = root / "unrelated"
            unrelated.mkdir()
            init_repo(unrelated, "https://example.invalid/wrong.git")
            destination = root / "output" / PLUGIN_NAME
            injected = {
                "GIT_DIR": str(unrelated / ".git"),
                "GIT_WORK_TREE": str(unrelated),
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "remote.origin.url",
                "GIT_CONFIG_VALUE_0": "https://example.invalid/injected.git",
            }
            with patch.dict(os.environ, injected):
                with patch("package_plugin.SOURCE_ROOT", source):
                    package(destination, package_format="skill")
            assert_skill_bytes(self, source, destination)

    def test_refuses_any_destination_inside_source_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = make_source(Path(temporary))
            destination = source / "not-copied" / PLUGIN_NAME
            with self.assertRaises(ValueError):
                package(destination, source)
            self.assertFalse(destination.exists())

    def test_leaves_owned_partial_destination_after_copy_failure(self) -> None:
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
