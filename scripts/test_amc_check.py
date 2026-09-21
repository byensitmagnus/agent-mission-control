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
        valid_sha1 = "a" * 40
        plan = {
            "schema_version": 1,
            "overall": "PASS",
            "blockers": [],
            "candidate_artifact": {
                "type": "git-commit",
                "identity_method": "git-commit",
                "digest_algorithm": "sha1",
                "digest": valid_sha1,
                "dirty": False,
            },
            "jobs": [{"id": "j1", "required": True, "lifecycle": "completed", "verdict": "PASS"}],
            "gates": [{"id": "g1", "status": "PASS", "evidence": {"command": "pytest", "evidence_digest": valid_sha1}}],
            "mission": {
                "overall": "PASS",
                "artifact": {
                    "type": "git-commit",
                    "identity_method": "git-commit",
                    "digest_algorithm": "sha1",
                    "digest": valid_sha1,
                    "dirty": False,
                },
                "stale_pass_artifact": "b" * 40,
                "evidence_digest": valid_sha1,
                "required_jobs": ["j1"],
                "required_gates": ["g1"],
            },
        }
        codes = [item.code for item in amc_guard.validate(plan)]
        self.assertIn("PASS_STALE_EVIDENCE", codes)


class PackageAndClaimsTests(unittest.TestCase):
    def test_version_from_canonical_file(self) -> None:
        self.assertEqual(VERSION, (ROOT / "VERSION").read_text(encoding="utf-8").strip())
        self.assertNotEqual(VERSION, "0.2.0-candidate.9")

    def test_claims_skillopt_and_harmful_use_different_sources(self) -> None:
        claims_file = ROOT / "research" / "claims.json"
        if not claims_file.is_file():
            self.skipTest("research/claims.json not present in core slice")
        result = run(str(ROOT / "scripts" / "render_claims.py"), "--check")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        data = json.loads(claims_file.read_text(encoding="utf-8"))
        skillopt = {sid for item in data["claims"] if "SKILLOPT" in item["claim_id"] for sid in item["source_ids"]}
        harmful = {sid for item in data["claims"] if "HARMFUL" in item["claim_id"] for sid in item["source_ids"]}
        self.assertTrue(skillopt)
        self.assertTrue(harmful)
        self.assertFalse(skillopt & harmful)

    def test_superpowers_local_and_upstream_distinct(self) -> None:
        claims_file = ROOT / "research" / "claims.json"
        if not claims_file.is_file():
            self.skipTest("research/claims.json not present in core slice")
        data = json.loads(claims_file.read_text(encoding="utf-8"))
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


class RequirePassCliTests(unittest.TestCase):
    def _run_cli(self, contract_data: dict | str, *flags: str) -> tuple[int, dict | str]:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "contract.json"
            if isinstance(contract_data, str):
                p.write_text(contract_data, encoding="utf-8")
            else:
                p.write_text(json.dumps(contract_data), encoding="utf-8")
            res = run(str(ROOT / "scripts" / "amc-check.py"), *flags, "--json", str(p))
            try:
                payload = json.loads(res.stdout)
            except Exception:
                payload = res.stdout
            return res.returncode, payload

    def test_invalid_contract_fails_both_modes(self) -> None:
        invalid = {"not_a_valid_contract": True}
        code, out = self._run_cli(invalid)
        self.assertEqual(code, 1)
        self.assertEqual(out["contract_validity"], "INVALID")

        code_rp, out_rp = self._run_cli(invalid, "--require-pass")
        self.assertEqual(code_rp, 1)
        self.assertEqual(out_rp["contract_validity"], "INVALID")

    def test_mission_fail_behavior(self) -> None:
        contract = {
            "schema_version": 1,
            "planned_route": "direct",
            "observed_route": "direct",
            "overall": "FAIL",
            "mission": {"overall": "FAIL"},
        }
        # Default mode returns 0, but notes that no outcome was accepted
        code, out = self._run_cli(contract)
        self.assertEqual(code, 0)
        self.assertEqual(out["contract_validity"], "VALID")
        self.assertEqual(out["mission_outcome"], "FAIL")
        self.assertIn("no mission outcome was accepted", out["note"])

        # --require-pass returns non-zero (1)
        code_rp, out_rp = self._run_cli(contract, "--require-pass")
        self.assertEqual(code_rp, 1)
        self.assertEqual(out_rp["contract_validity"], "VALID")
        self.assertEqual(out_rp["mission_outcome"], "FAIL")

    def test_mission_blocked_behavior(self) -> None:
        contract = {
            "schema_version": 1,
            "planned_route": "direct",
            "observed_route": "direct",
            "overall": "BLOCKED",
            "mission": {"overall": "BLOCKED"},
        }
        # Default mode returns 0
        code, out = self._run_cli(contract)
        self.assertEqual(code, 0)
        self.assertEqual(out["contract_validity"], "VALID")
        self.assertEqual(out["mission_outcome"], "BLOCKED")
        self.assertIn("no mission outcome was accepted", out["note"])

        # --require-pass returns non-zero (1)
        code_rp, out_rp = self._run_cli(contract, "--require-pass")
        self.assertEqual(code_rp, 1)
        self.assertEqual(out_rp["contract_validity"], "VALID")
        self.assertEqual(out_rp["mission_outcome"], "BLOCKED")

    def test_mission_not_verified_behavior(self) -> None:
        contract = {
            "schema_version": 1,
            "planned_route": "direct",
            "observed_route": "direct",
            "overall": "NOT VERIFIED",
            "mission": {"overall": "NOT VERIFIED"},
        }
        # Default mode returns 0
        code, out = self._run_cli(contract)
        self.assertEqual(code, 0)
        self.assertEqual(out["contract_validity"], "VALID")
        self.assertEqual(out["mission_outcome"], "NOT VERIFIED")
        self.assertIn("no mission outcome was accepted", out["note"])

        # --require-pass returns non-zero (1)
        code_rp, out_rp = self._run_cli(contract, "--require-pass")
        self.assertEqual(code_rp, 1)
        self.assertEqual(out_rp["contract_validity"], "VALID")
        self.assertEqual(out_rp["mission_outcome"], "NOT VERIFIED")

    def test_mission_pass_behavior(self) -> None:
        contract = {
            "schema_version": 1,
            "planned_route": "direct",
            "observed_route": "direct",
            "overall": "PASS",
            "blockers": [],
            "candidate_artifact": {
                "type": "git-commit",
                "identity_method": "git-commit",
                "digest_algorithm": "sha1",
                "digest": "a" * 40,
                "dirty": False,
            },
            "mission": {
                "overall": "PASS",
                "artifact": {
                    "type": "git-commit",
                    "identity_method": "git-commit",
                    "digest_algorithm": "sha1",
                    "digest": "a" * 40,
                    "dirty": False,
                },
                "evidence_digest": "a" * 40,
                "required_jobs": ["j1"],
                "required_gates": ["g1"],
            },
            "jobs": [
                {
                    "id": "j1",
                    "role": "lead",
                    "capability": "lead-capable",
                    "write_scope": ["src/lib.py"],
                    "accept_check": {"declared": True, "command": "pytest"},
                    "lifecycle": "completed",
                    "verdict": "PASS",
                }
            ],
            "gates": [
                {
                    "id": "g1",
                    "status": "PASS",
                    "evidence": {
                        "test_command": "pytest",
                        "evidence_digest": "a" * 40,
                        "target_artifact": {
                            "type": "git-commit",
                            "identity_method": "git-commit",
                            "digest_algorithm": "sha1",
                            "digest": "a" * 40,
                            "dirty": False,
                        },
                    },
                }
            ],
        }
        # Default mode returns 0
        code, out = self._run_cli(contract)
        self.assertEqual(code, 0)
        self.assertEqual(out["contract_validity"], "VALID")
        self.assertEqual(out["mission_outcome"], "PASS")

        # --require-pass returns 0
        code_rp, out_rp = self._run_cli(contract, "--require-pass")
        self.assertEqual(code_rp, 0)
        self.assertEqual(out_rp["contract_validity"], "VALID")
        self.assertEqual(out_rp["mission_outcome"], "PASS")


class CanonicalDelegationTests(unittest.TestCase):
    def test_scout_route_decision(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "scout",
            "observed_route": "scout",
            "delegation_decision": {
                "decision": "delegate",
                "reason": "explore potential solutions",
                "basis": "information_value",
                "expected_value": 0.8,
                "coordination_cost": 0.2,
                "confidence": 0.9,
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertNotIn("MISSING_DELEGATION_DECISION", codes)
        self.assertNotIn("INVALID_DELEGATION_DECISION", codes)

    def test_sequential_worker_route_decision(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "sequential_delegated",
            "observed_route": "sequential_delegated",
            "delegation_decision": {
                "decision": "delegate",
                "reason": "specialized implementation task",
                "basis": "specialization",
                "expected_value": 0.9,
                "coordination_cost": 0.3,
                "confidence": 0.85,
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertNotIn("MISSING_DELEGATION_DECISION", codes)

    def test_isolated_parallel_route_decision(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "isolated_parallel",
            "observed_route": "isolated_parallel",
            "observed_isolation": {"method": "git_worktree", "evidence": "created worktree wt1"},
            "delegation_decision": {
                "decision": "delegate",
                "reason": "parallel speedup on separate subtrees",
                "basis": "parallel_speedup",
                "expected_value": 1.2,
                "coordination_cost": 0.4,
                "confidence": 0.8,
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertNotIn("MISSING_DELEGATION_DECISION", codes)

    def test_review_route_decision_risk_override(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "reviewer_delegated",
            "observed_route": "reviewer_delegated",
            "delegation_decision": {
                "decision": "delegate",
                "reason": "high-risk acceptance logic requires fresh reviewer",
                "basis": "risk_override",
                "expected_value": 1.0,
                "coordination_cost": 0.5,
                "confidence": 0.95,
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertNotIn("MISSING_DELEGATION_DECISION", codes)
        self.assertNotIn("INVALID_DELEGATION_DECISION", codes)

    def test_missing_delegation_decision_rejected(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "sequential_delegated",
            "observed_route": "sequential_delegated",
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("MISSING_DELEGATION_DECISION", codes)


if __name__ == "__main__":
    unittest.main()
