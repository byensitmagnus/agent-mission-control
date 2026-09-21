#!/usr/bin/env python3
"""Deterministic mapping tests between AMC Job/Attempt and Orca Task/Dispatch."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "templates" / "host-capability-schema.json"
FIXTURE_PATH = ROOT / "templates" / "fixtures" / "orca-mapping.json"
PROFILE_MD = ROOT / "references" / "hosts" / "orca.md"


class OrcaHostProfileMappingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(SCHEMA_PATH.is_file(), f"missing schema: {SCHEMA_PATH}")
        self.assertTrue(FIXTURE_PATH.is_file(), f"missing fixture: {FIXTURE_PATH}")
        self.assertTrue(PROFILE_MD.is_file(), f"missing profile doc: {PROFILE_MD}")
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.profile_doc = PROFILE_MD.read_text(encoding="utf-8")

    def test_schema_structure(self) -> None:
        self.assertEqual(self.schema["properties"]["schema_version"]["const"], 1)
        self.assertIn("execution_mapping", self.schema["required"])
        self.assertIn("capabilities", self.schema["required"])
        self.assertIn("adopted_principles", self.schema["required"])
        self.assertIn("rejected_patterns", self.schema["required"])

    def test_orca_profile_documentation_invariants(self) -> None:
        # Host classification
        self.assertIn("Agent Development Environment", self.profile_doc)
        self.assertIn("Execution substrate", self.profile_doc)
        self.assertIn("Structured orchestration runtime", self.profile_doc)
        self.assertIn("Not AMC's portable core", self.profile_doc)

        # Single workflow owner
        self.assertIn("Single workflow owner", self.profile_doc)
        self.assertIn("AMC owns:", self.profile_doc)
        self.assertIn("Orca supplies:", self.profile_doc)

        # Semantic mappings
        self.assertIn("**Mission** | **Run**", self.profile_doc)
        self.assertIn("**Job** | **Task**", self.profile_doc)
        self.assertIn("**Attempt** | **Dispatch**", self.profile_doc)
        self.assertIn("worker_done", self.profile_doc)

        # Adopted principles
        self.assertIn("Task identity separate from attempt identity", self.profile_doc)
        self.assertIn("Stale attempts cannot complete the active task", self.profile_doc)
        self.assertIn("Separate requested versus effective execution profile", self.profile_doc)
        self.assertIn("Missing observation is not proof of termination", self.profile_doc)
        self.assertIn("Explicit cleanup ownership", self.profile_doc)

        # Explicit rejections
        self.assertIn("Parallel racing as default", self.profile_doc)
        self.assertIn("Worktree as a complete security sandbox", self.profile_doc)
        self.assertIn("Copying Orca's UI, runtime, cloud, mobile or database into AMC", self.profile_doc)
        self.assertIn("NOT VERIFIED", self.profile_doc)

    def test_bidirectional_entity_correspondence(self) -> None:
        amc = self.fixture["design_mapping"]
        orca = self.fixture["orca_orchestration"]

        # Mission <-> Run
        self.assertEqual(amc["objective"], orca["objective"])

        # Job <-> Task
        amc_jobs = {job["id"]: job for job in amc["jobs"]}
        orca_tasks = {task["task_id"]: task for task in orca["tasks"]}
        for task in orca_tasks.values():
            self.assertIn(task["amc_job_id"], amc_jobs)
            job = amc_jobs[task["amc_job_id"]]
            self.assertEqual(task["active_dispatch_id"], "disp-orca-1002")
            self.assertEqual(job["active_attempt_id"], "att-002")

        # Attempt <-> Dispatch
        dispatches = {d["dispatch_id"]: d for d in orca["dispatches"]}
        self.assertIn("disp-orca-1001", dispatches)
        self.assertIn("disp-orca-1002", dispatches)
        self.assertEqual(dispatches["disp-orca-1001"]["status"], "superseded")
        self.assertEqual(dispatches["disp-orca-1002"]["status"], "completed")

    def test_stale_attempt_completion_rejected(self) -> None:
        scenarios = {s["name"]: s for s in self.fixture["test_scenarios"]}
        stale = scenarios["stale_attempt_completion_rejected"]
        msg = stale["incoming_message"]
        orca = self.fixture["orca_orchestration"]

        task = next(t for t in orca["tasks"] if t["task_id"] == msg["task_id"])
        # The message references an older dispatch
        is_active = msg.get("dispatch_id") == task["active_dispatch_id"]
        self.assertFalse(is_active)
        self.assertEqual(stale["expected_outcome"], "REJECTED")
        self.assertEqual(stale["expected_error"], "STALE_DISPATCH_CANNOT_COMPLETE_ACTIVE_TASK")

    def test_missing_dispatch_id_rejected(self) -> None:
        scenarios = {s["name"]: s for s in self.fixture["test_scenarios"]}
        missing = scenarios["missing_dispatch_id_rejected"]
        msg = missing["incoming_message"]
        self.assertNotIn("dispatch_id", msg)
        self.assertEqual(missing["expected_outcome"], "REJECTED")

    def test_active_attempt_completion_accepted(self) -> None:
        scenarios = {s["name"]: s for s in self.fixture["test_scenarios"]}
        active = scenarios["active_attempt_completion_accepted"]
        msg = active["incoming_message"]
        orca = self.fixture["orca_orchestration"]

        task = next(t for t in orca["tasks"] if t["task_id"] == msg["task_id"])
        is_active = msg.get("dispatch_id") == task["active_dispatch_id"]
        self.assertTrue(is_active)
        self.assertEqual(active["expected_outcome"], "ACCEPTED")

    def test_separate_requested_and_effective_profile(self) -> None:
        dispatches = self.fixture["orca_orchestration"]["dispatches"]
        for dispatch in dispatches:
            self.assertIn("requested_capability", dispatch)
            self.assertIn("effective_agent", dispatch)
            self.assertIn("effective_model", dispatch)
            # Requested is AMC capability class; effective is concrete host agent/model
            self.assertEqual(dispatch["requested_capability"], "focused-general-worker")
            self.assertEqual(dispatch["effective_agent"], "codex")
            self.assertEqual(dispatch["effective_model"], "gpt-4o")

    def test_cleanup_policy_is_explicit(self) -> None:
        dispatches = self.fixture["orca_orchestration"]["dispatches"]
        policies = {d["dispatch_id"]: d.get("cleanup_policy") for d in dispatches}
        self.assertEqual(policies["disp-orca-1001"], "retain")
        self.assertEqual(policies["disp-orca-1002"], "release")

    def test_behavioral_status_remains_not_verified(self) -> None:
        self.assertEqual(self.fixture["design_mapping"]["overall"], "NOT VERIFIED")

    def test_live_stale_dispatch_rejection_is_design_mapping_only(self) -> None:
        """Orca profile mapping is repository_ci_enforced design documentation.
        Live runtime stale-dispatch rejection is not implemented in AMC Guard."""
        self.assertIn("Not AMC's portable core", self.profile_doc)
        self.assertIn("design_mapping", self.fixture)
        self.assertNotIn("amc_contract", self.fixture)


if __name__ == "__main__":
    unittest.main()
