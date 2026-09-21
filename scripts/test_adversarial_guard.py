#!/usr/bin/env python3
"""30 Required Adversarial Cases for AMC Product Contract V1.1 Guard Hardening."""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import amc_guard
import install_skill
import package_plugin


class AdversarialGuardHardeningTests(unittest.TestCase):
    """Systematic verification of all 30 required adversarial cases."""

    # 1. empty object
    def test_case_01_empty_object_fails_closed(self) -> None:
        result = amc_guard.check_contract({})
        self.assertEqual(result["contract_validity"], "INVALID")
        self.assertEqual(result["mission_outcome"], "NOT VERIFIED")
        codes = [i["code"] for i in result["issues"]]
        self.assertIn("MISSING_SCHEMA_VERSION", codes)

    # 2. missing schema_version
    def test_case_02_missing_schema_version_fails_closed(self) -> None:
        result = amc_guard.check_contract({"planned_route": "direct", "overall": "NOT VERIFIED"})
        self.assertEqual(result["contract_validity"], "INVALID")
        codes = [i["code"] for i in result["issues"]]
        self.assertIn("MISSING_SCHEMA_VERSION", codes)

    # 3. unknown schema_version
    def test_case_03_unknown_schema_version(self) -> None:
        result = amc_guard.check_contract({"schema_version": 999, "planned_route": "direct"})
        self.assertEqual(result["contract_validity"], "INVALID")
        codes = [i["code"] for i in result["issues"]]
        self.assertIn("UNSUPPORTED_SCHEMA_VERSION", codes)

    # 4. string false for delegation_authority
    def test_case_04_string_false_for_delegation_authority(self) -> None:
        plan = {
            "schema_version": 1,
            "jobs": [
                {
                    "id": "w1",
                    "capability": "focused-general-worker",
                    "delegation_authority": "false",
                    "write_scope": ["src/app.py"],
                    "accept_check": {"declared": True, "kind": "executable"},
                }
            ],
            "break_even": True,
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("INVALID_TYPE", codes)
        self.assertTrue(any("delegation_authority" in i.path for i in issues))

    # 5. string false for trivial
    def test_case_05_string_false_for_trivial(self) -> None:
        plan = {"schema_version": 1, "trivial": "false", "planned_route": "direct"}
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("INVALID_TYPE", codes)
        self.assertTrue(any("trivial" in i.path for i in issues))

    # 6. non-integer budget
    def test_case_06_non_integer_budget(self) -> None:
        plan = {"schema_version": 1, "budget": "100", "planned_route": "direct"}
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("INVALID_TYPE", codes)

    # 7. negative budget
    def test_case_07_negative_budget(self) -> None:
        plan = {"schema_version": 1, "budget": -50, "planned_route": "direct"}
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertTrue("NEGATIVE_CEILING" in codes or "INVALID_TYPE" in codes)

    # 8. non-list scope
    def test_case_08_non_list_scope(self) -> None:
        plan = {
            "schema_version": 1,
            "break_even": True,
            "jobs": [
                {
                    "id": "w1",
                    "capability": "focused-general-worker",
                    "write_scope": "src/app.py",
                    "accept_check": {"declared": True, "kind": "executable"},
                }
            ],
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("INVALID_TYPE", codes)
        self.assertTrue(any("write_scope" in i.path for i in issues))

    # 9. mixed-type scope list
    def test_case_09_mixed_type_scope_list(self) -> None:
        plan = {
            "schema_version": 1,
            "break_even": True,
            "jobs": [
                {
                    "id": "w1",
                    "capability": "focused-general-worker",
                    "write_scope": ["src/app.py", 1234],
                    "accept_check": {"declared": True, "kind": "executable"},
                }
            ],
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("INVALID_TYPE", codes)

    # 10. unbound required job
    def test_case_10_unbound_required_job(self) -> None:
        plan = {
            "schema_version": 1,
            "overall": "PASS",
            "jobs": [{"id": "real-job", "required": True}],
            "gates": [{"id": "g1", "status": "PASS"}],
            "mission": {
                "overall": "PASS",
                "artifact": "a" * 40,
                "required_jobs": [
                    {"id": "unbound-ghost-job", "lifecycle": "completed", "verdict": "PASS"}
                ],
                "required_gates": [{"id": "g1", "status": "PASS"}],
                "blockers": [],
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("PASS_WITH_INCOMPLETE_JOB", codes)

    # 11. unbound required gate
    def test_case_11_unbound_required_gate(self) -> None:
        plan = {
            "schema_version": 1,
            "overall": "PASS",
            "jobs": [{"id": "j1", "required": True}],
            "gates": [{"id": "real-gate", "status": "PASS"}],
            "mission": {
                "overall": "PASS",
                "artifact": "a" * 40,
                "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
                "required_gates": [{"id": "unbound-ghost-gate", "status": "PASS"}],
                "blockers": [],
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("PASS_WITH_INCOMPLETE_GATE", codes)

    # 12. one-character artifact
    def test_case_12_one_character_artifact(self) -> None:
        plan = {
            "schema_version": 1,
            "overall": "PASS",
            "jobs": [{"id": "j1", "required": True}],
            "gates": [{"id": "g1", "status": "PASS"}],
            "mission": {
                "overall": "PASS",
                "artifact": "x",
                "identity_method": "content-digest",
                "digest_algorithm": "sha256",
                "evidence_identity": "x",
                "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
                "required_gates": [{"id": "g1", "status": "PASS"}],
                "blockers": [],
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertTrue("MALFORMED_ARTIFACT_DIGEST" in codes or "INVALID_ARTIFACT_DIGEST" in codes)

    # 13. malformed SHA-1
    def test_case_13_malformed_sha1(self) -> None:
        plan = {
            "schema_version": 1,
            "overall": "PASS",
            "jobs": [{"id": "j1", "required": True}],
            "gates": [{"id": "g1", "status": "PASS"}],
            "mission": {
                "overall": "PASS",
                "artifact": "a" * 39,  # 39 chars instead of 40
                "identity_method": "git-commit",
                "digest_algorithm": "sha1",
                "evidence_identity": "a" * 39,
                "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
                "required_gates": [{"id": "g1", "status": "PASS"}],
                "blockers": [],
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertTrue("MALFORMED_ARTIFACT_DIGEST" in codes or "INVALID_ARTIFACT_DIGEST" in codes)

    # 14. malformed SHA-256
    def test_case_14_malformed_sha256(self) -> None:
        plan = {
            "schema_version": 1,
            "overall": "PASS",
            "jobs": [{"id": "j1", "required": True}],
            "gates": [{"id": "g1", "status": "PASS"}],
            "mission": {
                "overall": "PASS",
                "artifact": "f" * 63 + "z",  # invalid hex and wrong format
                "identity_method": "content-digest",
                "digest_algorithm": "sha256",
                "evidence_identity": "f" * 63 + "z",
                "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
                "required_gates": [{"id": "g1", "status": "PASS"}],
                "blockers": [],
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertTrue("MALFORMED_ARTIFACT_DIGEST" in codes or "INVALID_ARTIFACT_DIGEST" in codes)

    # 15. identity-method/algorithm mismatch
    def test_case_15_identity_method_algorithm_mismatch(self) -> None:
        plan = {
            "schema_version": 1,
            "overall": "PASS",
            "jobs": [{"id": "j1", "required": True}],
            "gates": [{"id": "g1", "status": "PASS"}],
            "mission": {
                "overall": "PASS",
                "artifact": "a" * 40,
                "identity_method": "content-digest",
                "digest_algorithm": "sha1",  # mismatch: content-digest requires sha256
                "evidence_identity": "a" * 40,
                "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
                "required_gates": [{"id": "g1", "status": "PASS"}],
                "blockers": [],
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertTrue("ARTIFACT_METHOD_MISMATCH" in codes or "ARTIFACT_METHOD_ALGORITHM_MISMATCH" in codes)

    # 16. PASS with method none
    def test_case_16_pass_with_method_none_rejected(self) -> None:
        plan = {
            "schema_version": 1,
            "overall": "PASS",
            "jobs": [{"id": "j1", "required": True}],
            "gates": [{"id": "g1", "status": "PASS"}],
            "mission": {
                "overall": "PASS",
                "artifact": "a" * 40,
                "identity_method": "none",
                "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
                "required_gates": [{"id": "g1", "status": "PASS"}],
                "blockers": [],
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("PASS_WITHOUT_ARTIFACT", codes)

    # 17. instruction-only without evidence
    def test_case_17_instruction_only_without_evidence_is_skipped(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "amc-check.py"), "--instruction-only", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(data["check_status"], "SKIPPED")
        self.assertEqual(data["decision_source"], "caller_asserted")
        self.assertEqual(data["enforcement_scope"], "instruction_only")
        self.assertEqual(data["mission_outcome"], "NOT VERIFIED")
        self.assertEqual(data["status"], "SKIPPED")
        self.assertNotEqual(data["status"], "PASS")

    # 18. CLI flag missing its value
    def test_case_18_cli_flag_missing_value_exits_2(self) -> None:
        for flag in ("--mission-view", "--write-report"):
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "amc-check.py"), flag],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 2, f"{flag} should exit 2 on missing value")
            self.assertIn("usage error", proc.stderr.lower())

    # 19. nested sensitive receipt key
    def test_case_19_nested_sensitive_receipt_key(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "direct",
            "observed_route": "direct",
            "route_receipt": {
                "metadata": {
                    "connection": {
                        "api_token": "sk-1234567890abcdef"
                    }
                }
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("SENSITIVE_DATA_EXPOSED", codes)

    # 20. self-authored isolation prose
    def test_case_20_self_authored_isolation_prose(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "direct",
            "observed_route": "direct",
            "route_receipt": {
                "observed_isolation": "Container isolation fully guaranteed by developer"
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("INVALID_TYPE", codes)

    # 21. lead-only simple sequential job
    def test_case_21_lead_only_simple_sequential_job_allowed(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "direct",
            "observed_route": "direct",
            "simple_sequential": True,
            "jobs": [
                {
                    "id": "lead-step",
                    "role": "lead",
                    "write_scope": ["src/main.py"],
                }
            ],
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertNotIn("SIMPLE_SEQUENTIAL_DELEGATION", codes)

    # 22. sequential scope handoff
    def test_case_22_sequential_scope_handoff_allowed(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "sequential_delegated",
            "observed_route": "sequential_delegated",
            "break_even": True,
            "jobs": [
                {
                    "id": "step-1",
                    "capability": "focused-general-worker",
                    "write_scope": ["src/db.py"],
                    "accept_check": {"declared": True, "kind": "executable"},
                },
                {
                    "id": "step-2",
                    "capability": "focused-general-worker",
                    "write_scope": ["src/db.py"],
                    "depends_on": ["step-1"],
                    "scope_handoff": True,
                    "accept_check": {"declared": True, "kind": "executable"},
                },
            ],
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertNotIn("CONCURRENT_SCOPE_COLLISION", codes)

    # 23. concurrent scope collision
    def test_case_23_concurrent_scope_collision_rejected(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "isolated_parallel",
            "observed_route": "isolated_parallel",
            "break_even": True,
            "jobs": [
                {
                    "id": "p1",
                    "capability": "focused-general-worker",
                    "write_scope": ["src/db.py"],
                    "accept_check": {"declared": True, "kind": "executable"},
                },
                {
                    "id": "p2",
                    "capability": "focused-general-worker",
                    "write_scope": ["src/db.py"],
                    "accept_check": {"declared": True, "kind": "executable"},
                },
            ],
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertTrue("CONCURRENT_SCOPE_COLLISION" in codes or "WRITER_SCOPE_OVERLAP" in codes)

    # 24. completed dependencies followed by parallel ready wave
    def test_case_24_completed_dependencies_parallel_wave(self) -> None:
        plan = {
            "schema_version": 1,
            "planned_route": "isolated_parallel",
            "observed_route": "isolated_parallel",
            "break_even": True,
            "jobs": [
                {
                    "id": "dep-a",
                    "capability": "focused-general-worker",
                    "write_scope": ["src/a.py"],
                    "lifecycle": "completed",
                    "verdict": "PASS",
                    "accept_check": {"declared": True, "kind": "executable"},
                },
                {
                    "id": "worker-1",
                    "capability": "focused-general-worker",
                    "write_scope": ["src/b.py"],
                    "parallel": True,
                    "depends_on": ["dep-a"],
                    "accept_check": {"declared": True, "kind": "executable"},
                },
                {
                    "id": "worker-2",
                    "capability": "focused-general-worker",
                    "write_scope": ["src/c.py"],
                    "parallel": True,
                    "depends_on": ["dep-a"],
                    "accept_check": {"declared": True, "kind": "executable"},
                },
            ],
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertNotIn("DEPENDENT_PARALLEL", codes)

    # 25. Orca fixture passed through the real contract or clearly renamed design-only
    def test_case_25_orca_fixture_renamed_design_mapping(self) -> None:
        fixture_path = ROOT / "templates" / "fixtures" / "orca-mapping.json"
        if not fixture_path.is_file():
            self.skipTest("orca fixture not in core slice")
        self.assertTrue(fixture_path.is_file())
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        self.assertIn("design_mapping", fixture)
        self.assertNotIn("amc_contract", fixture)

    # 26. tampered BUILD_RECORD
    def test_case_26_tampered_build_record_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "proj"
            proj.mkdir()
            install_skill.install(proj, "cursor")
            record_path = proj / ".cursor" / "skills" / "agent-mission-control" / "BUILD_RECORD.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["runtime_content_digest"] = "0" * 64
            record_path.write_text(json.dumps(record), encoding="utf-8")
            res = install_skill.install(proj, "cursor", check=True)
            self.assertEqual(res["status"], "BUILD_RECORD_INVALID")
            self.assertEqual(res["build_record_status"], "TAMPERED")
            self.assertEqual(res["attestation"], "INVALID")

    # 27. stale BUILD_RECORD
    def test_case_27_stale_build_record_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "proj"
            proj.mkdir()
            install_skill.install(proj, "cursor")
            record_path = proj / ".cursor" / "skills" / "agent-mission-control" / "BUILD_RECORD.json"
            record = json.loads(record_path.read_text(encoding="utf-8"))
            record["version"] = "0.0.1-ancient"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            res = install_skill.install(proj, "cursor", check=True)
            self.assertEqual(res["status"], "BUILD_RECORD_INVALID")
            self.assertEqual(res["build_record_status"], "STALE")
            self.assertEqual(res["attestation"], "INVALID")

    # 28. untracked nested file identity
    def test_case_28_untracked_nested_file_changes_identity(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_commit = "1" * 40
            diff = b"sample diff"
            status1 = "?? file.txt\n"
            file1 = root / "file.txt"
            file1.write_text("hello", encoding="utf-8")
            h1, id1 = amc_guard.compute_dirty_source_identity(root, base_commit, status1, diff, [file1])

            # Add nested untracked file
            nested_dir = root / "nested" / "sub"
            nested_dir.mkdir(parents=True)
            file2 = nested_dir / "child.txt"
            file2.write_text("world", encoding="utf-8")
            status2 = "?? file.txt\n?? nested/sub/child.txt\n"
            h2, id2 = amc_guard.compute_dirty_source_identity(root, base_commit, status2, diff, [file1, file2])

            self.assertNotEqual(h1, h2)
            self.assertNotEqual(id1["untracked_manifest_digest"], id2["untracked_manifest_digest"])

    # 29. rename/mode/deletion identity
    def test_case_29_rename_mode_deletion_changes_identity(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_commit = "2" * 40
            file1 = root / "src.py"
            file1.write_text("code", encoding="utf-8")

            # Normal diff
            h_orig, _ = amc_guard.compute_dirty_source_identity(root, base_commit, " M src.py\n", b"diff_content_1", [file1])

            # Mode change diff
            h_mode, _ = amc_guard.compute_dirty_source_identity(root, base_commit, " M src.py\n", b"diff_content_1_mode_change", [file1])
            self.assertNotEqual(h_orig, h_mode)

            # Deletion diff
            h_del, _ = amc_guard.compute_dirty_source_identity(root, base_commit, " D src.py\n", b"diff_content_deleted", [])
            self.assertNotEqual(h_orig, h_del)

            # Rename diff
            h_rename, _ = amc_guard.compute_dirty_source_identity(root, base_commit, " R src.py -> dest.py\n", b"diff_rename", [file1])
            self.assertNotEqual(h_orig, h_rename)

    # 30. current truth files contradicting performed external actions
    def test_case_30_current_truth_files_contradiction(self) -> None:
        status_path = ROOT / "docs" / "status.json"
        self.assertTrue(status_path.is_file())
        status = json.loads(status_path.read_text(encoding="utf-8"))
        # Must not state push is not performed when PR is published
        not_auth = status.get("not_authorized", [])
        self.assertNotIn("push", not_auth)
        self.assertIn("merge", not_auth)
        self.assertIn("tag", not_auth)
        self.assertIn("release", not_auth)
        # Must not have stale static dirty boolean
        art = status.get("artifact_identity", {})
        self.assertNotIn("dirty", art)


class EvidenceBindingTests(unittest.TestCase):
    def _base_contract(self) -> dict:
        sha1 = "a" * 40
        return {
            "schema_version": 1,
            "overall": "PASS",
            "blockers": [],
            "candidate_artifact": {
                "type": "git-commit",
                "identity_method": "git-commit",
                "digest_algorithm": "sha1",
                "digest": sha1,
                "dirty": False,
            },
            "jobs": [
                {
                    "id": "j1",
                    "role": "lead",
                    "capability": "lead-capable",
                    "write_scope": ["a.py"],
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
                        "command": "pytest",
                        "evidence_digest": sha1,
                    },
                }
            ],
            "mission": {
                "overall": "PASS",
                "artifact": {
                    "type": "git-commit",
                    "identity_method": "git-commit",
                    "digest_algorithm": "sha1",
                    "digest": sha1,
                    "dirty": False,
                },
                "required_jobs": ["j1"],
                "required_gates": ["g1"],
                "evidence_digest": sha1,
            },
        }

    def test_matching_evidence_identity(self) -> None:
        plan = self._base_contract()
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertNotIn("PASS_WITHOUT_EVIDENCE", codes)
        self.assertNotIn("PASS_STALE_EVIDENCE", codes)
        self.assertEqual(codes, [])

    def test_missing_evidence_identity(self) -> None:
        plan = self._base_contract()
        del plan["mission"]["evidence_digest"]
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("PASS_WITHOUT_EVIDENCE", codes)

    def test_mismatching_evidence_identity(self) -> None:
        plan = self._base_contract()
        plan["mission"]["evidence_digest"] = "b" * 40
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertTrue("PASS_STALE_EVIDENCE" in codes or "PASS_WITHOUT_EVIDENCE" in codes)

    def test_gate_evidence_absent(self) -> None:
        plan = self._base_contract()
        del plan["gates"][0]["evidence"]
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("GATE_WITHOUT_EVIDENCE", codes)

    def test_gate_evidence_placeholder(self) -> None:
        plan = self._base_contract()
        plan["gates"][0]["evidence"] = "none"
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("GATE_WITHOUT_EVIDENCE", codes)

    def test_gate_evidence_bound_to_stale_artifact(self) -> None:
        plan = self._base_contract()
        plan["gates"][0]["evidence"] = {
            "command": "pytest",
            "target_artifact": {
                "type": "git-commit",
                "identity_method": "git-commit",
                "digest_algorithm": "sha1",
                "digest": "b" * 40,
                "dirty": False,
            },
        }
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("PASS_STALE_EVIDENCE", codes)

    def test_negative_plain_string_artifact_deadbeef(self) -> None:
        plan = self._base_contract()
        plan["mission"]["artifact"] = "deadbeef"
        issues = amc_guard.validate(plan)
        codes = [i.code for i in issues]
        self.assertIn("PASS_WITHOUT_ARTIFACT", codes)

    def test_regression_false_pass_contract_rejected(self) -> None:
        contract = {
            "schema_version": 1,
            "overall": "PASS",
            "blockers": [],
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
                    "status": "NOT VERIFIED",
                    "evidence": "none",
                }
            ],
            "mission": {
                "overall": "PASS",
                "artifact": "deadbeef",
                "required_jobs": ["j1"],
                "required_gates": [{"id": "g1", "status": "PASS"}],
            },
        }
        res = amc_guard.check_contract(contract)
        self.assertEqual(res["contract_validity"], "INVALID")
        self.assertEqual(res["mission_outcome"], "FAIL")
        codes = [i["code"] for i in res["issues"]]
        self.assertIn("PASS_WITHOUT_ARTIFACT", codes)
        self.assertIn("PASS_WITHOUT_EVIDENCE", codes)
        self.assertIn("PASS_WITH_INCOMPLETE_GATE", codes)


if __name__ == "__main__":
    unittest.main()
