#!/usr/bin/env python3
"""Deterministic decision-kernel contracts. No agent is launched."""
from __future__ import annotations

import json
import sys
from typing import Any

CAPABILITIES = {
    "lead-capable",
    "focused-general-worker",
    "cheap-bounded-worker",
    "material-reviewer",
    "narrow-verifier",
}
SLEEP_MARKERS = ("skillopt-sleep", "nightly sleep", "auto-adopt", "transcript harvest")


def _err(errors: list[str], message: str) -> None:
    errors.append(message)


def check(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    jobs = list(plan.get("jobs") or [])
    if plan.get("simple_sequential") and jobs:
        _err(errors, "simple sequential work must not delegate")

    scopes: dict[str, str] = {}
    ids = {job["id"] for job in jobs}
    for job in jobs:
        depends = list(job.get("depends_on") or [])
        if job.get("parallel") and depends:
            _err(errors, f"{job['id']}: dependent jobs must not run in parallel")
        missing = [name for name in depends if name not in ids]
        if missing:
            _err(errors, f"{job['id']}: unknown dependency {missing}")
        scope = job.get("write_scope")
        if scope:
            owner = scopes.get(scope)
            if owner and owner != job["id"]:
                _err(errors, f"shared write-scope {scope} owned by {owner} and {job['id']}")
            scopes[scope] = job["id"]
        capability = job.get("capability")
        if capability and capability not in CAPABILITIES:
            _err(errors, f"{job['id']}: unknown capability {capability}")
        accept = job.get("accept_check") or {}
        writing = bool(scope) and capability in {"cheap-bounded-worker", "focused-general-worker"}
        if capability == "cheap-bounded-worker":
            if writing and not accept.get("declared"):
                _err(errors, f"{job['id']}: cheap writing worker needs a predeclared accept check")
            if writing and accept.get("kind") != "executable" and plan.get("work_kind") == "code":
                _err(errors, f"{job['id']}: code writes need an executable accept check")
        if plan.get("work_kind") == "research" and capability in {"cheap-bounded-worker", "material-reviewer", "narrow-verifier"}:
            if accept.get("kind") not in {"source-anchors", None} and accept.get("declared"):
                if accept.get("kind") not in {"source-anchors", "counterevidence"}:
                    _err(errors, f"{job['id']}: research accept check must be source anchors or counterevidence")
        attempts = list(job.get("attempts") or [])
        failures = [item for item in attempts if item.get("failed")]
        retry_count = max(0, len(failures) - 1)
        for retry in failures[1:]:
            if not (
                retry.get("contract_changed")
                or retry.get("hypothesis_changed")
                or retry.get("escalated")
            ):
                _err(
                    errors,
                    f"{job['id']}: after one failed attempt, change the contract or hypothesis, or escalate",
                )
        retry_budget = int(job.get("retry_budget", 1))
        if retry_count > retry_budget:
            _err(errors, f"{job['id']}: retry budget exceeded")
        if job.get("capability") in {"cheap-bounded-worker", "focused-general-worker"} and job.get("return") == "transcript":
            _err(errors, f"{job['id']}: workers return artifacts, not transcripts")

    workers = [job for job in jobs if job.get("capability") in {"cheap-bounded-worker", "focused-general-worker"}]
    reviewers = [job for job in jobs if job.get("capability") == "material-reviewer"]
    if workers and plan.get("break_even") is False:
        _err(errors, "failed break-even must not delegate")
    if plan.get("lead_repeats_worker"):
        _err(errors, "lead must not redo the worker job")
    if plan.get("concurrency_as_goal"):
        _err(errors, "concurrency is a ceiling, not a target")
    worker_budget = plan.get("worker_budget")
    if worker_budget is not None and len(workers) > worker_budget:
        _err(errors, "worker budget exceeded")
    review_budget = plan.get("review_budget")
    if review_budget is not None and len(reviewers) > review_budget:
        _err(errors, "reviewer budget exceeded")
    if plan.get("trivial") and reviewers:
        _err(errors, "trivial work must not spawn a reviewer")
    if plan.get("complex_slice"):
        independent_proof = any(
            job.get("capability") in {"material-reviewer", "narrow-verifier"}
            and job.get("independent") is True
            and job.get("lifecycle") == "completed"
            and str(job.get("verdict") or "").upper() == "PASS"
            and (job.get("accept_check") or {}).get("artifact_identity_checked") is True
            for job in jobs
        )
        if plan.get("author_accepts") and not independent_proof:
            _err(errors, "complex slice author acceptance requires independent proof")
        repaired = [item for item in list(plan.get("findings") or []) if item.get("repaired")]
        if repaired and not any(item.get("blocking") for item in repaired):
            _err(errors, "complex slice repairs must target blocking findings")
        same_hypothesis = int(plan.get("same_hypothesis_repairs") or 0)
        continued = plan.get("new_evidence") or plan.get("hypothesis_changed") or plan.get("escalated")
        if same_hypothesis > 1 and not continued:
            _err(errors, "complex slice stops after one same-hypothesis repair")
        if plan.get("standing_pipeline"):
            _err(errors, "complex slice must not start a standing review pipeline")

    parallel_writers = [
        job["id"]
        for job in jobs
        if job.get("parallel") and job.get("write_scope")
    ]
    if len(parallel_writers) >= 2 and not plan.get("host_isolation"):
        _err(errors, "parallel writers need host isolation")

    optimization = plan.get("optimization")
    if optimization:
        if optimization.get("tie") and optimization.get("keep") != "incumbent":
            _err(errors, "measurable optimization ties keep the incumbent")
        if optimization.get("evaluator_changed") and not optimization.get("new_baseline"):
            _err(errors, "a changed evaluator starts a new baseline")

    mission = plan.get("mission") or {}
    overall = str(mission.get("overall") or "").upper()
    if overall == "PASS":
        artifact = str(mission.get("artifact") or "").strip()
        if not artifact or artifact.casefold() in {"none", "not verified", "n/a", "unknown", "-"}:
            _err(errors, "overall PASS requires a current artifact identity")
        stale = mission.get("stale_pass_artifact")
        if stale and artifact and str(stale) != artifact:
            _err(errors, "stale mission PASS cannot accept a new artifact")
        required = list(mission.get("required_jobs") or [])
        if not required:
            _err(errors, "overall PASS requires required jobs")
        for job in required:
            lifecycle = str(job.get("lifecycle") or "").lower()
            verdict = str(job.get("verdict") or "").upper()
            if lifecycle in {"queued", "running", "complete"} or verdict in {"FAIL", "BLOCKED", "NOT VERIFIED", ""}:
                _err(errors, "overall PASS rejected: required job unfinished or negative")
        if plan.get("release_delivery"):
            shipped = str(plan.get("shipped_artifact") or "").strip()
            checked = str(plan.get("checked_artifact") or "").strip()
            if not shipped or shipped != checked:
                _err(errors, "release PASS must check the shipped artifact")

    learning = plan.get("learning") or {}
    ordinary = bool(learning.get("ordinary_success"))
    if ordinary and learning.get("started_sleep"):
        _err(errors, "normal completion must not start Sleep")
    if ordinary and learning.get("auto_adopted"):
        _err(errors, "normal completion must not auto-adopt a skill")
    if ordinary and learning.get("wrote_observation") and not learning.get("reusable_signal"):
        _err(errors, "ordinary success must not write a learning observation")
    blob = json.dumps(plan).lower()
    if ordinary and any(marker in blob for marker in SLEEP_MARKERS):
        _err(errors, "normal completion must not invoke Sleep or harvest")
    return errors


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
        "jobs": [{"id": "scout", "depends_on": [], "capability": "cheap-bounded-worker"}],
        "expect": ["simple sequential work must not delegate"],
    },
    {
        "id": "02-dependent-parallel-fail",
        "jobs": [
            {"id": "a", "depends_on": [], "write_scope": "a.py"},
            {"id": "b", "depends_on": ["a"], "parallel": True, "write_scope": "b.py"},
        ],
        "expect": ["dependent jobs must not run in parallel"],
    },
    {
        "id": "03-shared-write-fail",
        "jobs": [
            {"id": "a", "write_scope": "app.py", "capability": "focused-general-worker", "accept_check": {"declared": True, "kind": "executable"}},
            {"id": "b", "write_scope": "app.py", "capability": "focused-general-worker", "accept_check": {"declared": True, "kind": "executable"}},
        ],
        "expect": ["shared write-scope app.py"],
    },
    {
        "id": "04-cheap-writer-no-check-fail",
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
        "id": "06-repeated-unchanged-retry-fail",
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
        "expect": ["change the contract or hypothesis, or escalate", "retry budget exceeded"],
    },
    {
        "id": "06-new-hypothesis-and-escalation-within-budget",
        "jobs": [
            {
                "id": "patch",
                "capability": "cheap-bounded-worker",
                "write_scope": "mod.py",
                "retry_budget": 2,
                "accept_check": {"declared": True, "kind": "executable"},
                "attempts": [
                    {"failed": True},
                    {"failed": True, "hypothesis_changed": True},
                    {"failed": True, "escalated": True},
                ],
            }
        ],
        "expect": [],
    },
    {
        "id": "06-one-retry-per-job-is-not-a-global-budget",
        "jobs": [
            {
                "id": job_id,
                "capability": "focused-general-worker",
                "attempts": [
                    {"failed": True},
                    {"failed": True, "hypothesis_changed": True},
                ],
            }
            for job_id in ("first", "second")
        ],
        "expect": [],
    },
    {
        "id": "07-optimization-tie-keeps-incumbent",
        "optimization": {"tie": True, "keep": "incumbent", "evaluator_changed": False, "new_baseline": False},
        "expect": [],
    },
    {
        "id": "07-optimization-tie-fail",
        "optimization": {"tie": True, "keep": "candidate", "evaluator_changed": False, "new_baseline": False},
        "expect": ["ties keep the incumbent"],
    },
    {
        "id": "08-changed-evaluator-new-baseline",
        "optimization": {"tie": False, "keep": "incumbent", "evaluator_changed": True, "new_baseline": True},
        "expect": [],
    },
    {
        "id": "08-changed-evaluator-fail",
        "optimization": {"tie": False, "keep": "candidate", "evaluator_changed": True, "new_baseline": False},
        "expect": ["changed evaluator starts a new baseline"],
    },
    {
        "id": "09-stale-pass-new-artifact-fail",
        "mission": {
            "overall": "PASS",
            "artifact": "bbb",
            "stale_pass_artifact": "aaa",
            "required_jobs": [{"lifecycle": "completed", "verdict": "PASS"}],
        },
        "expect": ["stale mission PASS cannot accept a new artifact"],
    },
    {
        "id": "10-overall-pass-unfinished-required",
        "mission": {
            "overall": "PASS",
            "artifact": "aaa",
            "required_jobs": [{"lifecycle": "queued", "verdict": "NOT VERIFIED"}],
        },
        "expect": ["required job unfinished or negative"],
    },
    {
        "id": "10-overall-pass-missing-artifact",
        "mission": {"overall": "PASS", "artifact": "", "required_jobs": [{"lifecycle": "completed", "verdict": "PASS"}]},
        "expect": ["current artifact identity"],
    },
    {
        "id": "10-overall-pass-no-required-jobs",
        "mission": {"overall": "PASS", "artifact": "aaa", "required_jobs": []},
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
        "host_isolation": "worktree",
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
    {
        "id": "14-complex-author-accept-fail",
        "complex_slice": True,
        "author_accepts": True,
        "findings": [{"blocking": True, "repaired": True}],
        "same_hypothesis_repairs": 1,
        "expect": ["complex slice author acceptance requires independent proof"],
    },
    {
        "id": "14-complex-lead-accepts-after-independent-proof",
        "complex_slice": True,
        "author_accepts": True,
        "jobs": [
            {
                "id": "review",
                "capability": "material-reviewer",
                "independent": True,
                "lifecycle": "completed",
                "verdict": "PASS",
                "accept_check": {
                    "declared": True,
                    "artifact_identity_checked": True,
                },
            }
        ],
        "findings": [{"blocking": True, "repaired": True}],
        "same_hypothesis_repairs": 1,
        "expect": [],
    },
    {
        "id": "14-complex-deferred-repair-fail",
        "complex_slice": True,
        "author_accepts": False,
        "findings": [{"blocking": False, "repaired": True}],
        "same_hypothesis_repairs": 1,
        "expect": ["complex slice repairs must target blocking findings"],
    },
    {
        "id": "14-complex-second-repair-fail",
        "complex_slice": True,
        "author_accepts": False,
        "findings": [{"blocking": True, "repaired": True}],
        "same_hypothesis_repairs": 2,
        "expect": ["complex slice stops after one same-hypothesis repair"],
    },
    {
        "id": "14-complex-standing-pipeline-fail",
        "complex_slice": True,
        "author_accepts": False,
        "standing_pipeline": True,
        "same_hypothesis_repairs": 1,
        "findings": [{"blocking": True, "repaired": True}],
        "expect": ["complex slice must not start a standing review pipeline"],
    },
    {
        "id": "14-complex-new-evidence-continues",
        "complex_slice": True,
        "author_accepts": False,
        "new_evidence": True,
        "findings": [{"blocking": True, "repaired": True}],
        "same_hypothesis_repairs": 2,
        "expect": [],
    },
    {
        "id": "14-complex-blocking-then-stop",
        "complex_slice": True,
        "author_accepts": False,
        "escalated": True,
        "findings": [
            {"blocking": True, "repaired": True},
            {"blocking": False, "repaired": False},
        ],
        "same_hypothesis_repairs": 1,
        "expect": [],
    },
    {
        "id": "15-release-source-pass-fail",
        "release_delivery": True,
        "checked_artifact": "scripts/main.ps1",
        "shipped_artifact": "FPSBooster.ps1",
        "mission": {
            "overall": "PASS",
            "artifact": "scripts/main.ps1",
            "required_jobs": [{"lifecycle": "completed", "verdict": "PASS"}],
        },
        "expect": ["release PASS must check the shipped artifact"],
    },
    {
        "id": "15-release-package-checked",
        "release_delivery": True,
        "checked_artifact": "FPSBooster.ps1",
        "shipped_artifact": "FPSBooster.ps1",
        "mission": {
            "overall": "PASS",
            "artifact": "FPSBooster.ps1",
            "required_jobs": [{"lifecycle": "completed", "verdict": "PASS"}],
        },
        "expect": [],
    },
]


def self_check() -> dict[str, Any]:
    failures = []
    for case in CASES:
        expected = list(case["expect"])
        found = check({key: value for key, value in case.items() if key not in {"id", "expect"}})
        missing = [item for item in expected if not any(item in message for message in found)]
        extra = [] if expected else found
        if missing or extra:
            failures.append({"id": case["id"], "missing": missing, "found": found})
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
