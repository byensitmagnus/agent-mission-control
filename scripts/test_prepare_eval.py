#!/usr/bin/env python3
"""Check isolation, identical inputs and safe refusal; this is not an agent eval."""

import hashlib
import json
import os
import sys
from pathlib import Path
import subprocess
import tempfile

from unittest.mock import patch

from prepare_eval import ROOT, fixture_paths, git_environment, prepare, relative_path


def main():
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))["cases"]
        for case in cases:
            first = prepare(case["id"], root / case["id"] / "first", ROOT)
            second = prepare(case["id"], root / case["id"] / "second", ROOT)
            assert first["prompt_sha256"] == second["prompt_sha256"]
            assert first["fixture_sha256"] == second["fixture_sha256"]
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
            result = prepare("01-text", root / "filtered", ROOT)
        workspace = root / "filtered/workspace"
        committed = subprocess.check_output(["git", "show", "HEAD:README.md"],
                                            cwd=workspace, env=git_environment())
        actual = (workspace / "README.md").read_bytes()
        assert not sentinel.exists(), "inherited Git filter was executed"
        assert committed == actual
        assert hashlib.sha256(committed).hexdigest() == result["fixture_sha256"]["README.md"]
        assert not (root / "unrelated.git").exists()
        source = root / "source"
        (source / "assets").mkdir(parents=True)
        (source / "SKILL.md").write_text("test skill", encoding="utf-8")
        destination = source / "assets" / "recursive-eval"
        try:
            prepare("01-text", destination, source)
        except ValueError as error:
            assert "copied skill directory" in str(error)
        else:
            raise AssertionError("recursive eval destination was accepted")
        assert not destination.exists()
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
    print("PASS: 9 paired disposable fixture preparations; isolation/refusal checks (not behavioral evals)")


if __name__ == "__main__":
    main()
