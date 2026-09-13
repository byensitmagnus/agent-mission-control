#!/usr/bin/env python3
"""Check isolation, identical inputs and safe refusal; this is not an agent eval."""

import hashlib
import os
import sys
from pathlib import Path
import subprocess
import tempfile

from unittest.mock import patch

from prepare_eval import ROOT, fixture_paths, git_environment, load_evaluator, prepare, relative_path


def main():
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        evaluator, evaluator_hash = load_evaluator()
        cases = evaluator["cases"]
        alternate_source = root / "alternate-source"
        alternate_source.mkdir()
        (alternate_source / "SKILL.md").write_text("---\nname: agent-mission-control\n---\nalternate\n", encoding="utf-8")
        for name in ("agents", "references", "templates", "assets"):
            (alternate_source / name).mkdir()
        for case in cases:
            first = prepare(case["id"], root / case["id"] / "first", ROOT)
            second = prepare(case["id"], root / case["id"] / "second", ROOT)
            alternate = prepare(case["id"], root / case["id"] / "alternate", alternate_source)
            assert first["prompt_sha256"] == second["prompt_sha256"]
            assert first["fixture_sha256"] == second["fixture_sha256"]
            assert first["prompt_sha256"] == alternate["prompt_sha256"]
            assert first["fixture_sha256"] == alternate["fixture_sha256"]
            assert first["case_definition_sha256"] == alternate["case_definition_sha256"]
            assert first["evaluator_sha256"] == alternate["evaluator_sha256"] == evaluator_hash
            assert first["skill_files_sha256"] != alternate["skill_files_sha256"]
            assert first["activation"] == case["activation"]
            prompt = (root / case["id"] / "first/prompt.txt").read_text(encoding="utf-8")
            names_skill = "$agent-mission-control" in prompt
            assert names_skill == (case["activation"] == "explicit")
            workspace = root / case["id"] / "first/workspace"
            assert not (workspace / "evals").exists()
            assert not (workspace / "manifest.json").exists()
            status = subprocess.check_output(["git", "status", "--porcelain"], cwd=workspace, env=git_environment())
            assert not status
            assert not subprocess.check_output(["git", "remote"], cwd=workspace, env=git_environment())
            assert first["behavioral_verdict"] == "NOT VERIFIED"
            before = (workspace / ".agents/skills/agent-mission-control/SKILL.md").read_bytes()
            try:
                prepare(case["id"], root / case["id"] / "first", ROOT)
            except FileExistsError:
                pass
            else:
                raise AssertionError("existing destination was overwritten")
            assert before == (workspace / ".agents/skills/agent-mission-control/SKILL.md").read_bytes()
        # A global clean filter would run arbitrary code and alter committed bytes.
        attributes = root / "attributes"
        attributes.write_text("*.md filter=amc\n", encoding="utf-8")
        sentinel = root / "filter-ran"
        script = root / "filter.py"
        script.write_text("from pathlib import Path; import sys; Path(sys.argv[1]).write_text('ran'); sys.stdout.write('FILTERED' + sys.stdin.read())", encoding="utf-8")
        config = root / "gitconfig"
        def configure(key, value):
            subprocess.run(["git", "config", "--file", str(config), key, value],
                           check=True, env=git_environment())
        configure("core.attributesFile", attributes.as_posix())
        configure("filter.amc.clean", f'"{Path(sys.executable).as_posix()}" "{script.as_posix()}" "{sentinel.as_posix()}"')
        configure("filter.amc.required", "true")
        poisoned = {"GIT_CONFIG_GLOBAL": str(config), "GIT_CONFIG_COUNT": "1",
                    "GIT_CONFIG_KEY_0": "core.attributesFile",
                    "GIT_CONFIG_VALUE_0": str(attributes), "GIT_DIR": str(root / "unrelated.git")}
        with patch.dict(os.environ, poisoned):
            result = prepare("01-small-linear", root / "filtered", ROOT)
        workspace = root / "filtered/workspace"
        committed = subprocess.check_output(["git", "show", "HEAD:README.md"],
                                            cwd=workspace, env=git_environment())
        actual = (workspace / "README.md").read_bytes()
        assert not sentinel.exists(), "inherited Git filter was executed"
        assert committed == actual
        assert hashlib.sha256(committed).hexdigest() == result["fixture_sha256"]["README.md"]
        assert not (root / "unrelated.git").exists()
        source = root / "source"
        for name in ("agents", "references", "templates", "assets"):
            (source / name).mkdir(parents=True)
        (source / "SKILL.md").write_text("test skill", encoding="utf-8")
        destination = source / "assets" / "recursive-eval"
        try:
            prepare("01-small-linear", destination, source)
        except ValueError as error:
            assert "copied skill directory" in str(error)
        else:
            raise AssertionError("recursive eval destination was accepted")
        assert not destination.exists()
        incomplete_source = root / "incomplete-source"
        incomplete_source.mkdir()
        (incomplete_source / "SKILL.md").write_text("test skill", encoding="utf-8")
        incomplete_destination = root / "incomplete-eval"
        try:
            prepare("01-small-linear", incomplete_destination, incomplete_source)
        except ValueError as error:
            assert "missing runtime directory" in str(error)
        else:
            raise AssertionError("incomplete skill source was accepted")
        assert not incomplete_destination.exists()
        outside = root / "outside"
        linked_source = outside / "source"
        linked_source.mkdir(parents=True)
        (linked_source / "SKILL.md").write_text("outside skill", encoding="utf-8")
        source_sentinel = linked_source / "sentinel"
        source_sentinel.write_text("untouched", encoding="utf-8")
        source_parent_link = root / "source-parent-link"
        source_parent_link.symlink_to(outside, target_is_directory=True)
        linked_destination = root / "linked-source-eval"
        try:
            prepare("01-small-linear", linked_destination, source_parent_link / "source")
        except ValueError as error:
            assert "skill source or ancestor" in str(error)
        else:
            raise AssertionError("linked skill-source ancestor was accepted")
        assert source_sentinel.read_text(encoding="utf-8") == "untouched"
        assert not linked_destination.exists()
        destination_outside = root / "destination-outside"
        destination_outside.mkdir()
        destination_sentinel = destination_outside / "sentinel"
        destination_sentinel.write_text("untouched", encoding="utf-8")
        destination_parent_link = root / "destination-parent-link"
        destination_parent_link.symlink_to(destination_outside, target_is_directory=True)
        try:
            prepare("01-small-linear", destination_parent_link / "eval", ROOT)
        except ValueError as error:
            assert "destination parent or ancestor" in str(error)
        else:
            raise AssertionError("linked destination ancestor was accepted")
        assert destination_sentinel.read_text(encoding="utf-8") == "untouched"
        assert not (destination_outside / "eval").exists()
        for value in ("../escape", "/absolute", "C:/escape", "a\\b", ".git/config", "a//b", ""):
            try:
                relative_path(value)
            except ValueError:
                pass
            else:
                raise AssertionError(f"unsafe path accepted: {value}")
        for fixture in ({"a": "file", "a/b.txt": "child"}, {"A": "one", "a": "two"}):
            try:
                fixture_paths(fixture)
            except ValueError:
                pass
            else:
                raise AssertionError("conflicting fixture paths were accepted")
        dangling_source = root / "dangling-source"
        dangling_source.mkdir()
        (dangling_source / "SKILL.md").write_text("test skill", encoding="utf-8")
        for name in ("agents", "templates", "assets"):
            (dangling_source / name).mkdir()
        (dangling_source / "references").symlink_to(root / "missing-runtime", target_is_directory=True)
        try:
            prepare("01-small-linear", root / "dangling-eval", dangling_source)
        except ValueError as error:
            assert "linked skill input" in str(error)
        else:
            raise AssertionError("dangling runtime symlink was accepted")
        assert not (root / "dangling-eval").exists()
        for fixture in (
            {"README.md": "one", "README.md.": "two"},
            {"data/x": "one", "data./x": "two"},
            {"NUL": "device"},
            {"COM1.txt": "device"},
            {"con .txt": "device"},
            {"COM\u00b9.txt": "device"},
            {"CONOUT$": "device"},
            {"bad\x00name": "invalid"},
            {"folder /file.txt": "space alias"},
        ):
            try:
                fixture_paths(fixture)
            except ValueError:
                pass
            else:
                raise AssertionError(f"Windows alias/device accepted: {fixture}")
        assert len(fixture_paths({"COM10.txt": "valid", "NUL-file.txt": "valid",
                                  "notes/my file.md": "valid"})) == 3
    print(f"PASS: {len(cases)} tripled disposable fixture preparations; identical evaluator inputs across skill snapshots; isolation/refusal checks (not behavioral evals)")


if __name__ == "__main__":
    main()
