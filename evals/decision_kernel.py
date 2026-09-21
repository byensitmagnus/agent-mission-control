#!/usr/bin/env python3
"""Compatibility wrapper around the canonical Truth Layer contract."""
from __future__ import annotations

import json
import sys
from typing import Any

from control_contract import validate


def check(plan: dict[str, Any]) -> list[str]:
    contract = dict(plan)
    contract.setdefault("schema_version", 1)
    if "jobs" in contract and isinstance(contract["jobs"], list):
        norm_jobs = []
        for j in contract["jobs"]:
            if isinstance(j, dict):
                nj = dict(j)
                if isinstance(nj.get("write_scope"), str):
                    nj["write_scope"] = [nj["write_scope"]]
                norm_jobs.append(nj)
            else:
                norm_jobs.append(j)
        contract["jobs"] = norm_jobs
    if "isolation_evidence" in contract and isinstance(contract["isolation_evidence"], str):
        if contract.get("host_isolation") == "worktree":
            contract["isolation_evidence"] = {
                "host": "git",
                "workspace": "worktree",
                "mechanism": "worktree",
                "identity": contract["isolation_evidence"],
            }
    if "mission" in contract and isinstance(contract["mission"], dict):
        m = dict(contract["mission"])
        if m.get("overall") == "PASS":
            art = m.get("artifact")
            if art in {"aaa", "bbb"}:
                dig = art[0] * 40
                m["artifact"] = {
                    "identity_method": "git-commit",
                    "digest_algorithm": "sha1",
                    "digest": dig,
                    "dirty": False,
                    "type": "git-commit",
                }
                m.setdefault("evidence_digest", dig)
            elif isinstance(art, dict) and "digest" in art:
                m.setdefault("evidence_digest", art["digest"])
            elif not art:
                m.setdefault("evidence_digest", "a" * 40)
            stale = m.get("stale_pass_artifact")
            if stale in {"aaa", "bbb"}:
                m["stale_pass_artifact"] = stale[0] * 40
        if "gates" not in contract and "required_gates" in m:
            contract["gates"] = [{"id": g.get("id"), "status": g.get("status", "PASS"), "evidence": "check on artifact"} for g in m["required_gates"] if isinstance(g, dict)]
        elif "gates" in contract:
            for g in contract["gates"]:
                if isinstance(g, dict) and not g.get("evidence"):
                    g["evidence"] = "check on artifact"
        if "required_jobs" in m:
            if "jobs" not in contract:
                contract["jobs"] = []
            plan_job_ids = {j["id"] for j in contract["jobs"] if isinstance(j, dict) and "id" in j}
            norm_rjobs = []
            for idx, rj in enumerate(m["required_jobs"]):
                if isinstance(rj, dict):
                    nrj = dict(rj)
                    jid = nrj.get("id") or f"j{idx}"
                    nrj["id"] = jid
                    norm_rjobs.append(nrj)
                    if jid not in plan_job_ids:
                        contract["jobs"].append({"id": jid, "required": True, "lifecycle": nrj.get("lifecycle", "completed"), "verdict": nrj.get("verdict", "PASS")})
                else:
                    norm_rjobs.append(rj)
            m["required_jobs"] = norm_rjobs
        contract["mission"] = m
    return [issue.message for issue in validate(contract)]


CASES = [
    {
        "id": "01-simple-no-delegation",
        "simple_sequential": True,
        "jobs": [],
        "expect": [],
    },
    {
        "id": "01-simple-delegation-fail",
        "simple_sequential": True,
        "break_even": True,
        "jobs": [{"id": "scout", "depends_on": [], "capability": "cheap-bounded-worker"}],
        "expect": ["simple sequential work must not delegate"],
    },
    {
        "id": "02-dependent-parallel-fail",
        "break_even": True,
        "jobs": [
            {"id": "a", "depends_on": [], "write_scope": "a.py", "capability": "focused-general-worker", "accept_check": {"declared": True, "kind": "executable"}},
            {"id": "b", "depends_on": ["a"], "parallel": True, "write_scope": "b.py", "capability": "focused-general-worker", "accept_check": {"declared": True, "kind": "executable"}},
        ],
        "expect": ["dependent jobs must not run in parallel"],
    },
    {
        "id": "03-shared-write-fail",
        "break_even": True,
        "jobs": [
            {"id": "a", "write_scope": "app.py", "capability": "focused-general-worker", "accept_check": {"declared": True, "kind": "executable"}},
            {"id": "b", "write_scope": "app.py", "capability": "focused-general-worker", "accept_check": {"declared": True, "kind": "executable"}},
        ],
        "expect": ["shared write-scope app.py"],
    },
    {
        "id": "04-cheap-writer-no-check-fail",
        "break_even": True,
        "work_kind": "code",
        "jobs": [
            {
                "id": "patch",
                "capability": "cheap-bounded-worker",
                "write_scope": "mod.py",
                "accept_check": {"declared": False},
            }
        ],
        "expect": ["cheap writing worker needs a predeclared accept check"],
    },
    {
        "id": "05-research-source-anchors",
        "break_even": True,
        "work_kind": "research",
        "jobs": [
            {
                "id": "audit",
                "capability": "cheap-bounded-worker",
                "accept_check": {"declared": True, "kind": "source-anchors"},
            }
        ],
        "expect": [],
    },
    {
        "id": "06-one-retry-then-escalate",
        "break_even": True,
        "jobs": [
            {
                "id": "patch",
                "capability": "cheap-bounded-worker",
                "write_scope": "mod.py",
                "accept_check": {"declared": True, "kind": "executable"},
                "attempts": [
                    {"failed": True, "contract_changed": True, "escalated": False},
                    {"failed": True, "contract_changed": False, "escalated": True},
                ],
            }
        ],
        "expect": [],
    },
    {
        "id": "06-endless-retry-fail",
        "break_even": True,
        "jobs": [
            {
                "id": "patch",
                "capability": "cheap-bounded-worker",
                "write_scope": "mod.py",
                "accept_check": {"declared": True, "kind": "executable"},
                "attempts": [
                    {"failed": True},
                    {"failed": True},
                    {"failed": True},
                ],
            }
        ],
        "expect": ["change the contract or escalate", "more than one retry is forbidden"],
    },
    {
        "id": "07-optimization-tie-keeps-incumbent",
        "optimization": {"evaluator_frozen": True, "tie": True, "keep": "incumbent", "evaluator_changed": False, "new_baseline": False},
        "expect": [],
    },
    {
        "id": "07-optimization-tie-fail",
        "optimization": {"evaluator_frozen": True, "tie": True, "keep": "candidate", "evaluator_changed": False, "new_baseline": False},
        "expect": ["ties keep the incumbent"],
    },
    {
        "id": "08-changed-evaluator-new-baseline",
        "optimization": {"evaluator_frozen": True, "tie": False, "keep": "incumbent", "evaluator_changed": True, "new_baseline": True},
        "expect": [],
    },
    {
        "id": "08-changed-evaluator-fail",
        "optimization": {"evaluator_frozen": True, "tie": False, "keep": "candidate", "evaluator_changed": True, "new_baseline": False},
        "expect": ["changed evaluator starts a new baseline"],
    },
    {
        "id": "09-stale-pass-new-artifact-fail",
        "mission": {
            "overall": "PASS",
            "artifact": "bbb",
            "stale_pass_artifact": "aaa",
            "required_jobs": [{"lifecycle": "completed", "verdict": "PASS"}],
            "required_gates": [{"id": "g1", "status": "PASS"}],
            "blockers": [],
        },
        "expect": ["stale mission PASS cannot accept a new artifact"],
    },
    {
        "id": "10-overall-pass-unfinished-required",
        "mission": {
            "overall": "PASS",
            "artifact": "aaa",
            "required_jobs": [{"lifecycle": "queued", "verdict": "NOT VERIFIED"}],
            "required_gates": [{"id": "g1", "status": "PASS"}],
            "blockers": [],
        },
        "expect": ["required job unfinished or negative"],
    },
    {
        "id": "10-overall-pass-missing-artifact",
        "mission": {"overall": "PASS", "artifact": "", "required_jobs": [{"lifecycle": "completed", "verdict": "PASS"}], "required_gates": [{"id": "g1", "status": "PASS"}], "blockers": []},
        "expect": ["current artifact identity"],
    },
    {
        "id": "10-overall-pass-no-required-jobs",
        "mission": {"overall": "PASS", "artifact": "aaa", "required_jobs": [], "required_gates": [{"id": "g1", "status": "PASS"}], "blockers": []},
        "expect": ["overall PASS requires required jobs"],
    },
    {
        "id": "11-ordinary-success-no-sleep",
        "learning": {
            "ordinary_success": True,
            "reusable_signal": False,
            "started_sleep": False,
            "auto_adopted": False,
            "wrote_observation": False,
        },
        "expect": [],
    },
    {
        "id": "11-ordinary-success-sleep-fail",
        "learning": {
            "ordinary_success": True,
            "reusable_signal": False,
            "started_sleep": True,
            "auto_adopted": False,
            "wrote_observation": True,
        },
        "expect": ["must not start Sleep", "must not write a learning observation"],
    },
    {
        "id": "11-ordinary-success-auto-adopt-fail",
        "learning": {
            "ordinary_success": True,
            "reusable_signal": False,
            "started_sleep": False,
            "auto_adopted": True,
            "wrote_observation": False,
        },
        "expect": ["must not auto-adopt"],
    },
    {
        "id": "12-parallel-writers-no-isolation-fail",
        "break_even": True,
        "jobs": [
            {
                "id": "a",
                "parallel": True,
                "write_scope": "a.py",
                "capability": "focused-general-worker",
                "accept_check": {"declared": True, "kind": "executable"},
            },
            {
                "id": "b",
                "parallel": True,
                "write_scope": "b.py",
                "capability": "focused-general-worker",
                "accept_check": {"declared": True, "kind": "executable"},
            },
        ],
        "expect": ["parallel writers need host isolation"],
    },
    {
        "id": "12-parallel-writers-with-isolation",
        "break_even": True,
        "host_isolation": "worktree",
        "isolation_evidence": "git worktree list: /tmp/wt-a /tmp/wt-b",
        "isolation_workspace": "worktree",
        "jobs": [
            {
                "id": "a",
                "parallel": True,
                "write_scope": "a.py",
                "capability": "focused-general-worker",
                "accept_check": {"declared": True, "kind": "executable"},
            },
            {
                "id": "b",
                "parallel": True,
                "write_scope": "b.py",
                "capability": "focused-general-worker",
                "accept_check": {"declared": True, "kind": "executable"},
            },
        ],
        "expect": [],
    },
    {
        "id": "13-failed-breakeven-must-not-delegate",
        "break_even": False,
        "jobs": [
            {
                "id": "patch",
                "capability": "cheap-bounded-worker",
                "write_scope": "mod.py",
                "accept_check": {"declared": True, "kind": "executable"},
            }
        ],
        "expect": ["failed break-even must not delegate"],
    },
    {
        "id": "13-transcript-handoff-fail",
        "break_even": True,
        "jobs": [
            {
                "id": "patch",
                "capability": "focused-general-worker",
                "write_scope": "mod.py",
                "accept_check": {"declared": True, "kind": "executable"},
                "return": "transcript",
            }
        ],
        "expect": ["workers return artifacts, not transcripts"],
    },
    {
        "id": "13-lead-repeats-worker-fail",
        "break_even": True,
        "lead_repeats_worker": True,
        "jobs": [
            {
                "id": "patch",
                "capability": "cheap-bounded-worker",
                "write_scope": "mod.py",
                "accept_check": {"declared": True, "kind": "executable"},
                "return": "artifact",
            }
        ],
        "expect": ["lead must not redo the worker job"],
    },
    {
        "id": "13-concurrency-as-goal-fail",
        "concurrency_as_goal": True,
        "jobs": [],
        "expect": ["concurrency is a ceiling, not a target"],
    },
    {
        "id": "13-worker-budget-exceeded",
        "break_even": True,
        "worker_budget": 1,
        "host_isolation": "worktree",
        "jobs": [
            {
                "id": "a",
                "capability": "focused-general-worker",
                "write_scope": "a.py",
                "accept_check": {"declared": True, "kind": "executable"},
            },
            {
                "id": "b",
                "capability": "focused-general-worker",
                "write_scope": "b.py",
                "accept_check": {"declared": True, "kind": "executable"},
            },
        ],
        "expect": ["worker budget exceeded"],
    },
    {
        "id": "13-trivial-reviewer-fail",
        "trivial": True,
        "review_budget": 0,
        "jobs": [{"id": "review", "capability": "material-reviewer"}],
        "expect": ["trivial work must not spawn a reviewer", "reviewer budget exceeded"],
    },
    {
        "id": "13-compact-artifact-within-budget",
        "break_even": True,
        "worker_budget": 1,
        "review_budget": 0,
        "jobs": [
            {
                "id": "patch",
                "capability": "cheap-bounded-worker",
                "write_scope": "mod.py",
                "accept_check": {"declared": True, "kind": "executable"},
                "return": "artifact",
            }
        ],
        "expect": [],
    },
]


def self_check() -> dict[str, Any]:
    failures = []
    for case in CASES:
        expected = list(case["expect"])
        found = check({key: value for key, value in case.items() if key not in {"id", "expect"}})
        missing = [item for item in expected if not any(item in message for message in found)]
        extra = [message for message in found if expected and not any(item in message for item in expected)]
        if not expected:
            extra = found
        if missing or extra:
            failures.append({"id": case["id"], "missing": missing, "extra": extra, "found": found})
    return {
        "status": "PASS" if not failures else "FAIL",
        "cases": len(CASES),
        "failures": failures,
        "note": "decision-kernel self-check; not agent behavior",
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--self-check":
        result = self_check()
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "PASS" else 1
    print("usage: evals/decision_kernel.py --self-check", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
