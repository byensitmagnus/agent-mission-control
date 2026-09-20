#!/usr/bin/env python3
"""Product-contract tests for the bundled checker, claims and package identity."""
from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import amc_guard  # noqa: E402
from package_plugin import COPY_FILES, PLUGIN_NAME, VERSION, package  # noqa: E402


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=str(cwd or ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


class GuardContractTests(unittest.TestCase):
    def test_trivial_direct_does_not_require_contract(self) -> None:
        self.assertFalse(amc_guard.contract_required({"trivial": True, "simple_sequential": True, "planned_route": "direct"}))
        self.assertFalse(amc_guard.contract_required({"trivial": True, "planned_route": "direct"}))
        self.assertFalse(amc_guard.contract_required({"planned_route": "direct", "simple_sequential": True}))

    def test_high_risk_direct_requires_contract(self) -> None:
        self.assertTrue(amc_guard.contract_required({"planned_route": "direct", "release_sensitive": True}))
        self.assertTrue(amc_guard.contract_required({"planned_route": "direct", "risk_level": "material"}))
        self.assertTrue(amc_guard.contract_required({"planned_route": "direct", "risk_level": "critical"}))
        self.assertTrue(amc_guard.contract_required({"planned_route": "direct", "false_pass_cost": "high"}))
        self.assertTrue(amc_guard.contract_required({"planned_route": "direct", "acceptance_logic_changed": True}))
        self.assertTrue(amc_guard.contract_required({"planned_route": "direct", "acceptance_logic_changes": True}))
        # High risk flags override trivial / simple_sequential exemption
        self.assertTrue(amc_guard.contract_required({"planned_route": "direct", "trivial": True, "release_sensitive": True}))
        self.assertTrue(amc_guard.contract_required({"planned_route": "direct", "trivial": True, "simple_sequential": True, "risk_level": "material"}))
        self.assertTrue(amc_guard.contract_required({"planned_route": "direct", "trivial": True, "false_pass_cost": "high"}))
        self.assertTrue(amc_guard.contract_required({"planned_route": "direct", "trivial": True, "acceptance_logic_changed": True}))

    def test_delegated_work_requires_contract(self) -> None:
        plan = {"planned_route": "sequential_delegated"}
        self.assertTrue(amc_guard.contract_required(plan))

    def test_instruction_only_path_without_file(self) -> None:
        result = run(str(ROOT / "scripts" / "amc-check.py"), "--instruction-only", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["enforcement_scope"], "instruction_only")
        self.assertEqual(payload["behavioral"], "NOT VERIFIED")

    def test_worker_defaults_to_no_delegation(self) -> None:
        job = {"id": "w", "capability": "focused-general-worker"}
        self.assertEqual(amc_guard._job_role(job), "worker")
        self.assertFalse(amc_guard._may_delegate(job))

    def test_unauthorized_nested_delegation(self) -> None:
        plan = {
            "schema_version": 1,
            "break_even": True,
            "planned_route": "sequential_delegated",
            "observed_route": "sequential_delegated",
            "observed_child_ids": [{"id": "c", "source": "host-reported"}],
            "jobs": [
                {
                    "id": "w",
                    "role": "worker",
                    "capability": "cheap-bounded-worker",
                    "write_scope": ["a.py"],
                    "accept_check": {"declared": True, "kind": "executable"},
                    "return": "artifact",
                    "observed_child_jobs": ["n"],
                },
                {
                    "id": "n",
                    "parent_job": "w",
                    "capability": "cheap-bounded-worker",
                    "write_scope": ["b.py"],
                    "accept_check": {"declared": True, "kind": "executable"},
                    "return": "artifact",
                },
            ],
        }
        codes = [item.code for item in amc_guard.validate(plan)]
        self.assertIn("UNAUTHORIZED_NESTED_DELEGATION", codes)

    def test_reviewer_write_rejected(self) -> None:
        plan = {"schema_version": 1, "jobs": [{"id": "r", "role": "reviewer", "capability": "material-reviewer", "write_scope": ["fix.py"]}]}
        codes = [item.code for item in amc_guard.validate(plan)]
        self.assertIn("REVIEWER_WRITE_FORBIDDEN", codes)

    def test_route_mismatch_visible(self) -> None:
        plan = {
            "schema_version": 1,
            "break_even": True,
            "planned_route": "direct",
            "observed_route": "sequential_delegated",
            "jobs": [{
                "id": "w",
                "capability": "cheap-bounded-worker",
                "write_scope": ["a.py"],
                "accept_check": {"declared": True, "kind": "executable"},
                "return": "artifact",
            }],
        }
        codes = [item.code for item in amc_guard.validate(plan)]
        self.assertIn("ROUTE_MISMATCH", codes)

    def test_mission_view_cannot_drift(self) -> None:
        plan = {"schema_version": 1, "planned_route": "direct", "observed_route": "review", "overall": "NOT VERIFIED"}
        markdown = "overall: NOT VERIFIED\nPlanned route: direct\nObserved route: direct\n"
        codes = [item.code for item in amc_guard.compare_mission_view(plan, markdown)]
        self.assertIn("MISSION_VIEW_DRIFT", codes)

    def test_stale_artifact_rejected(self) -> None:
        plan = {
            "schema_version": 1,
            "overall": "PASS",
            "jobs": [{"id": "j1", "required": True}],
            "gates": [{"id": "g1", "status": "PASS"}],
            "mission": {
                "overall": "PASS",
                "artifact": "a" * 40,
                "stale_pass_artifact": "b" * 40,
                "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
                "required_gates": [{"id": "g1", "status": "PASS", "evidence": f"check on {'a' * 40}"}],
            },
        }
        codes = [item.code for item in amc_guard.validate(plan)]
        self.assertIn("PASS_STALE_EVIDENCE", codes)


class PackageAndClaimsTests(unittest.TestCase):
    def test_version_from_canonical_file(self) -> None:
        self.assertEqual(VERSION, (ROOT / "VERSION").read_text(encoding="utf-8").strip())
        self.assertNotEqual(VERSION, "0.2.0-candidate.9")

    def test_claims_skillopt_and_harmful_use_different_sources(self) -> None:
        result = run(str(ROOT / "scripts" / "render_claims.py"), "--check")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        data = json.loads((ROOT / "research" / "claims.json").read_text(encoding="utf-8"))
        skillopt = {sid for item in data["claims"] if "SKILLOPT" in item["claim_id"] for sid in item["source_ids"]}
        harmful = {sid for item in data["claims"] if "HARMFUL" in item["claim_id"] for sid in item["source_ids"]}
        self.assertTrue(skillopt)
        self.assertTrue(harmful)
        self.assertFalse(skillopt & harmful)

    def test_superpowers_local_and_upstream_distinct(self) -> None:
        data = json.loads((ROOT / "research" / "claims.json").read_text(encoding="utf-8"))
        sources = {item["source_id"]: item for item in data["sources"]}
        self.assertEqual(sources["SUPERPOWERS-LOCAL"]["audited_ref"], "v6.1.1")
        self.assertEqual(sources["SUPERPOWERS-641"]["audited_ref"], "v6.4.1")

    def test_user_copy_docs_list_bundled_checker(self) -> None:
        paths = (
            ROOT / "docs" / "getting-started.md",
            ROOT / "docs" / "development.md",
            ROOT / "CLAUDE.md",
            ROOT / "AGENTS.md",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertIn("VERSION", text, path)
            for relative in COPY_FILES:
                self.assertIn(relative.replace("\\", "/"), text, path)

    def test_no_superiority_claim_in_docs_or_tests(self) -> None:
        banned = ("generally better", "generally cheaper", "generally faster", "behavioral superiority PASS")
        for path in (ROOT / "SKILL.md", ROOT / "README.md", ROOT / "docs" / "status.json"):
            text = path.read_text(encoding="utf-8").lower()
            for phrase in banned:
                self.assertNotIn(phrase, text, path)

    def test_packaged_checker_runs_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "pkg" / PLUGIN_NAME
            package(destination, package_format="skill")
            self.assertTrue((destination / "scripts" / "amc-check.py").is_file())
            self.assertTrue((destination / "scripts" / "amc_guard.py").is_file())
            contract = Path(temporary) / "mission.json"
            contract.write_text(
                (ROOT / "templates" / "control-contract.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            isolated = Path(temporary) / "isolated"
            isolated.mkdir()
            checker = destination / "scripts" / "amc-check.py"
            result = run(str(checker), "--json", str(contract), cwd=isolated)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["contract_validity"], "VALID")
            self.assertEqual(payload["mission_outcome"], "NOT VERIFIED")
            self.assertEqual(payload["behavioral_status"], "NOT VERIFIED")

    def test_checker_does_not_modify_project_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "proj"
            project.mkdir()
            sentinel = project / "keep.txt"
            sentinel.write_text("untouched", encoding="utf-8")
            contract = project / "mission.json"
            contract.write_text(
                (ROOT / "templates" / "control-contract.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            before = {path.relative_to(project).as_posix(): path.read_bytes() for path in project.rglob("*") if path.is_file()}
            result = run(str(ROOT / "scripts" / "amc-check.py"), "--json", str(contract), cwd=project)
            self.assertEqual(result.returncode, 0, result.stderr)
            after = {path.relative_to(project).as_posix(): path.read_bytes() for path in project.rglob("*") if path.is_file()}
            self.assertEqual(before, after)

    def test_checker_uses_no_network(self) -> None:
        def blocked(*_args, **_kwargs):
            raise AssertionError("network")
        with patch.object(socket, "create_connection", blocked), patch.object(socket, "socket", blocked):
            result = amc_guard.check_contract({"schema_version": 1, "planned_route": "direct", "observed_route": "direct", "overall": "NOT VERIFIED"})
            self.assertEqual(result["contract_validity"], "VALID")
            self.assertEqual(result["mission_outcome"], "NOT VERIFIED")

    def test_two_builds_same_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "a" / PLUGIN_NAME
            second = root / "b" / PLUGIN_NAME
            first_zip = root / "a.zip"
            second_zip = root / "b.zip"
            package(first, package_format="skill", archive=first_zip)
            package(second, package_format="skill", archive=second_zip)
            self.assertEqual(first_zip.read_bytes(), second_zip.read_bytes())
            digest = hashlib.sha256(first_zip.read_bytes()).hexdigest()
            self.assertEqual(len(digest), 64)


if __name__ == "__main__":
    unittest.main()
