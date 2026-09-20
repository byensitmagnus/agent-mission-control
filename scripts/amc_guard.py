#!/usr/bin/env python3
"""AMC Guard: canonical mission/receipt checker. No agent is launched.

Machine semantics for planning, observation and acceptance live here.
Markdown views are projections. A passing check is not behavioral PASS
and not a release decision. Stdlib only. No network.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA_VERSION = 1
CAPABILITIES = {
    "lead-capable",
    "focused-general-worker",
    "cheap-bounded-worker",
    "material-reviewer",
    "narrow-verifier",
}
DELEGATED_WRITERS = {"focused-general-worker", "cheap-bounded-worker"}
ROLES = {"lead", "worker", "reviewer", "verifier"}
LIFECYCLES = {"queued", "running", "completed", "superseded"}
VERDICTS = {"PASS", "FAIL", "BLOCKED", "NOT VERIFIED"}
GATE_STATUSES = VERDICTS
ROUTES = {
    "direct",
    "scout",
    "sequential_delegated",
    "isolated_parallel",
    "review",
    "measurable_optimizer",
}
DELEGATED_ROUTES = {"scout", "sequential_delegated", "isolated_parallel"}
ISOLATION_VERIFIED = {"worktree", "sandbox", "vm", "permissions"}
ISOLATION_NONE = {"none", "unverified"}
ARTIFACT_METHODS = {
    "none",
    "git-commit",
    "git-tree",
    "package-digest",
    "content-digest",
    "dirty-manifest",
    "diff-digest",
}
DIGEST_ALGORITHMS = {"none", "sha1", "sha256"}
ENGINEERING = VERDICTS
BEHAVIORAL = VERDICTS
RELEASE = {"GO", "NO-GO", "NOT DECIDED"}
SLEEP_MARKERS = ("skillopt-sleep", "nightly sleep", "auto-adopt", "transcript harvest")
PLACEHOLDER = {"", "none", "n/a", "unknown", "not verified", "-", "null"}
WEAK_ISOLATION_EVIDENCE = PLACEHOLDER | {"claimed", "yes", "true", "prompt", "asserted"}
CHILD_SOURCES = {"host-reported", "worktree", "sandbox", "session"}
SENSITIVE_RECEIPT_KEYS = {
    "prompt", "full_prompt", "raw_output", "stdout", "stderr",
    "transcript", "source_code", "file_contents", "secrets", "secret",
    "contents", "api_key", "token", "password", "credentials", "auth",
}

JOB_KEYS = {
    "id", "depends_on", "parallel", "write_scope", "read_scope", "capability",
    "accept_check", "attempts", "return", "lifecycle", "verdict", "required",
    "independent", "isolation", "role", "delegation_authority", "parent_job",
    "observed_child_jobs", "delegation_ceiling", "permitted_actions",
    "required_artifact", "ownership_handoff", "scope_handoff",
}
PLAN_KEYS = {
    "schema_version", "task_id", "objective", "non_goals", "authority",
    "prohibited_actions", "base_artifact", "candidate_artifact", "dirty",
    "planned_route", "observed_route", "route_reason", "break_even",
    "break_even_evidence", "delegation_decision", "host_capabilities",
    "host_capability_confidence", "jobs", "gates", "blockers",
    "reviewer_requirement", "reviewer_independence", "budget", "timestamps",
    "overall", "limitations", "simple_sequential", "work_kind",
    "host_isolation", "isolation_evidence", "isolation_workspace",
    "optimization", "mission", "learning", "lead_repeats_worker",
    "concurrency_as_goal", "worker_budget", "review_budget", "retry_budget",
    "trivial", "acceptance_logic_changed", "route_receipt", "product_status",
    "release_sensitive", "risk_level", "false_pass_cost", "acceptance_logic_changes",
    "observed_child_ids", "observed_agent_roles", "expected_information_value",
    "coordination_cost_assumption", "fallback_route", "deviations",
    "independent_behavioral_evidence", "release_decision",
}
TELEMETRY_EVENT_KEYS = (
    "schema_version", "task_id_hmac", "host_version", "skill_version",
    "planned_route", "observed_route", "job_count", "isolation", "packet_size",
    "tokens", "tool_calls", "wall_time_ms", "attempts", "repairs",
    "user_interventions", "acceptance_result", "reviewer_catches", "rollback",
    "artifact_before", "artifact_after", "final_outcome",
)
AVO_GATES = (
    "scalar_or_ordered_metric", "evaluator_frozen", "deterministic_or_repeated",
    "bounded_edit_surface", "baseline_exists", "fixed_budget",
    "recoverable_lineage", "ties_keep_incumbent", "evaluator_change_new_baseline",
    "preservation_or_holdout", "rollback_possible",
)


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    path: str = ""


def _unknown(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip().casefold() in PLACEHOLDER:
        return True
    return False


def _norm_enum(value: object) -> str:
    return str(value or "").strip()


def _is_bool(value: object) -> bool:
    return type(value) is bool


def _is_non_neg_int(value: object) -> bool:
    return type(value) is int and type(value) is not bool and value >= 0


def _find_sensitive_receipt_keys(data: Any, path: str = "route_receipt") -> list[str]:
    found: list[str] = []
    if isinstance(data, dict):
        for k, v in data.items():
            curr = f"{path}.{k}"
            k_lower = str(k).lower()
            if any(s in k_lower for s in SENSITIVE_RECEIPT_KEYS):
                found.append(curr)
            found.extend(_find_sensitive_receipt_keys(v, curr))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            found.extend(_find_sensitive_receipt_keys(v, f"{path}[{i}]"))
    return found


def _validate_top_level_types(plan: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    # Booleans
    for key in (
        "trivial", "simple_sequential", "break_even", "dirty",
        "concurrency_as_goal", "lead_repeats_worker", "release_sensitive",
        "acceptance_logic_changed", "acceptance_logic_changes",
        "independent_behavioral_evidence", "release_decision",
    ):
        if key in plan and not _is_bool(plan[key]):
            issues.append(Issue("INVALID_TYPE", f"field {key} must be a boolean", key))

    # Budgets
    for key in ("worker_budget", "review_budget", "retry_budget"):
        if key in plan:
            val = plan[key]
            if type(val) is int and type(val) is not bool:
                if val < 0:
                    issues.append(Issue("NEGATIVE_CEILING", f"field {key} must not be negative", key))
            else:
                issues.append(Issue("INVALID_TYPE", f"field {key} must be a non-negative integer", key))

    if "budget" in plan:
        val = plan["budget"]
        if type(val) is int and type(val) is not bool:
            if val < 0:
                issues.append(Issue("NEGATIVE_CEILING", "field budget must not be negative", "budget"))
        elif isinstance(val, dict):
            for b_k, b_v in val.items():
                if type(b_v) is int and type(b_v) is not bool:
                    if b_v < 0:
                        issues.append(Issue("NEGATIVE_CEILING", f"budget.{b_k} must not be negative", f"budget.{b_k}"))
                else:
                    issues.append(Issue("INVALID_TYPE", f"budget.{b_k} must be a non-negative integer", f"budget.{b_k}"))
        else:
            issues.append(Issue("INVALID_TYPE", "field budget must be a non-negative integer or object", "budget"))

    # String lists
    for key in ("non_goals", "prohibited_actions", "deviations", "limitations", "observed_agent_roles"):
        if key in plan:
            val = plan[key]
            if not isinstance(val, list):
                issues.append(Issue("INVALID_TYPE", f"field {key} must be a list", key))
            elif not all(isinstance(x, str) for x in val):
                issues.append(Issue("INVALID_TYPE", f"field {key} entries must be strings", key))

    # Objects / Dicts
    for key in ("base_artifact", "candidate_artifact", "route_receipt", "optimization", "mission", "learning", "product_status", "delegation_decision"):
        if key in plan and not isinstance(plan[key], dict):
            issues.append(Issue("INVALID_TYPE", f"field {key} must be an object", key))

    # Strings
    for key in (
        "task_id", "objective", "authority", "planned_route", "observed_route",
        "route_reason", "fallback_route", "work_kind", "host_isolation",
        "isolation_workspace", "overall", "risk_level", "false_pass_cost",
        "expected_information_value", "coordination_cost_assumption",
    ):
        if key in plan and not isinstance(plan[key], str):
            issues.append(Issue("INVALID_TYPE", f"field {key} must be a string", key))

    # Blockers
    if "blockers" in plan:
        val = plan["blockers"]
        if not isinstance(val, list):
            issues.append(Issue("INVALID_TYPE", "field blockers must be a list", "blockers"))

    # Observed children
    if "observed_child_ids" in plan:
        val = plan["observed_child_ids"]
        if not isinstance(val, list):
            issues.append(Issue("INVALID_TYPE", "field observed_child_ids must be a list", "observed_child_ids"))

    # Gates
    if "gates" in plan:
        val = plan["gates"]
        if not isinstance(val, list):
            issues.append(Issue("INVALID_TYPE", "field gates must be a list", "gates"))
        else:
            for idx, g in enumerate(val):
                if not isinstance(g, dict):
                    issues.append(Issue("INVALID_TYPE", f"gates[{idx}] must be an object", f"gates[{idx}]"))

    # Jobs
    if "jobs" in plan:
        val = plan["jobs"]
        if not isinstance(val, list):
            issues.append(Issue("INVALID_TYPE", "field jobs must be a list", "jobs"))
        else:
            for idx, j in enumerate(val):
                if not isinstance(j, dict):
                    issues.append(Issue("INVALID_TYPE", f"jobs[{idx}] must be an object", f"jobs[{idx}]"))

    return issues


def validate(plan: Any) -> list[Issue]:
    if not isinstance(plan, dict):
        return [Issue("MALFORMED_INPUT", "malformed contract: plan must be an object")]

    # 1. Require schema_version
    if "schema_version" not in plan:
        return [Issue("MISSING_SCHEMA_VERSION", "missing schema_version")]
    version = plan.get("schema_version")
    if type(version) is not int or version != SCHEMA_VERSION:
        return [Issue("UNSUPPORTED_SCHEMA_VERSION", f"unsupported schema_version {version}")]

    # 2. Strict structural schema
    issues: list[Issue] = []
    extra = set(plan) - PLAN_KEYS
    if extra:
        issues.append(Issue("UNSUPPORTED_KEY", f"unsupported keys {sorted(extra)}"))

    type_issues = _validate_top_level_types(plan)
    issues.extend(type_issues)
    if any(issue.code in {"INVALID_TYPE", "NEGATIVE_CEILING"} for issue in type_issues):
        return issues

    receipt = plan.get("route_receipt")
    if receipt is not None:
        issues.extend(_route_receipt(receipt, plan))
    issues.extend(_jobs(plan))
    issues.extend(_authority(plan))
    issues.extend(_delegation(plan))
    issues.extend(_optimization(plan))
    issues.extend(_mission(plan))
    issues.extend(_learning(plan))
    status = plan.get("product_status")
    if isinstance(status, dict):
        issues.extend(validate_product_status(status))
    return issues


def _is_ordered_dependency(job_a_id: str, job_b_id: str, by_id: dict[str, dict[str, Any]]) -> bool:
    """Return True if job_b depends directly or transitively on job_a."""
    visited: set[str] = set()
    queue = list(by_id.get(job_b_id, {}).get("depends_on") or [])
    while queue:
        dep = queue.pop(0)
        if dep == job_a_id:
            return True
        if dep in by_id and dep not in visited:
            visited.add(dep)
            queue.extend(by_id[dep].get("depends_on") or [])
    return False


def _jobs(plan: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    jobs = plan.get("jobs")
    if jobs is None:
        jobs = []
    if not isinstance(jobs, list):
        return [Issue("MALFORMED_INPUT", "malformed contract: jobs must be a list", "jobs")]

    if plan.get("simple_sequential") is True:
        delegated_jobs = [
            j for j in jobs
            if isinstance(j, dict) and (_job_role(j) != "lead" or j.get("capability") in DELEGATED_WRITERS or j.get("delegation_authority") is True)
        ]
        if delegated_jobs:
            issues.append(Issue("SIMPLE_SEQUENTIAL_DELEGATION", "simple sequential work must not delegate"))

    ids: list[str] = []
    seen: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    for index, job in enumerate(jobs):
        loc = f"jobs[{index}]"
        if not isinstance(job, dict):
            issues.append(Issue("MALFORMED_INPUT", f"malformed contract: {loc} must be an object", loc))
            continue
        extra = set(job) - JOB_KEYS
        if extra:
            issues.append(Issue("UNSUPPORTED_KEY", f"{loc}: unsupported keys {sorted(extra)}", loc))
        raw_id = job.get("id")
        if not isinstance(raw_id, str) or not raw_id.strip():
            issues.append(Issue("MISSING_JOB_ID", f"{loc}: missing job ID", loc))
            continue
        job_id = raw_id.strip()
        if job_id in seen:
            issues.append(Issue("DUPLICATE_JOB_ID", f"{job_id}: duplicate job ID", loc))
            continue
        seen.add(job_id)
        ids.append(job_id)
        by_id[job_id] = job

        # Job field types
        for b_field in ("delegation_authority", "parallel", "independent", "required", "scope_handoff"):
            if b_field in job and not _is_bool(job[b_field]):
                issues.append(Issue("INVALID_TYPE", f"{job_id}: {b_field} must be a boolean", f"{loc}.{b_field}"))

        if "write_scope" in job:
            ws = job["write_scope"]
            if not isinstance(ws, list):
                issues.append(Issue("INVALID_TYPE", f"{job_id}: write_scope must be a list", f"{loc}.write_scope"))
            elif not all(isinstance(x, str) for x in ws):
                issues.append(Issue("INVALID_TYPE", f"{job_id}: write_scope entries must be strings", f"{loc}.write_scope"))

        if "read_scope" in job:
            rs = job["read_scope"]
            if not isinstance(rs, list):
                issues.append(Issue("INVALID_TYPE", f"{job_id}: read_scope must be a list", f"{loc}.read_scope"))
            elif not all(isinstance(x, str) for x in rs):
                issues.append(Issue("INVALID_TYPE", f"{job_id}: read_scope entries must be strings", f"{loc}.read_scope"))

        if "permitted_actions" in job:
            pa = job["permitted_actions"]
            if not isinstance(pa, list):
                issues.append(Issue("INVALID_TYPE", f"{job_id}: permitted_actions must be a list", f"{loc}.permitted_actions"))
            elif not all(isinstance(x, str) for x in pa):
                issues.append(Issue("INVALID_TYPE", f"{job_id}: permitted_actions entries must be strings", f"{loc}.permitted_actions"))

        if "delegation_ceiling" in job:
            dc = job["delegation_ceiling"]
            if type(dc) is int and type(dc) is not bool:
                if dc < 0:
                    issues.append(Issue("NEGATIVE_CEILING", f"{job_id}: delegation_ceiling must not be negative", f"{loc}.delegation_ceiling"))
            else:
                issues.append(Issue("INVALID_TYPE", f"{job_id}: delegation_ceiling must be a non-negative integer", f"{loc}.delegation_ceiling"))

        capability = job.get("capability")
        if capability and capability not in CAPABILITIES:
            issues.append(Issue("UNKNOWN_CAPABILITY", f"{job_id}: unknown capability {capability}", loc))
        lifecycle = job.get("lifecycle")
        if lifecycle is not None and str(lifecycle) not in LIFECYCLES:
            issues.append(Issue("UNKNOWN_LIFECYCLE", f"{job_id}: unknown lifecycle {lifecycle}", loc))
        verdict = job.get("verdict")
        if verdict is not None and str(verdict).upper() not in VERDICTS:
            issues.append(Issue("UNKNOWN_VERDICT", f"{job_id}: unknown verdict {verdict}", loc))

        depends = job.get("depends_on") or []
        if not isinstance(depends, list):
            issues.append(Issue("MALFORMED_INPUT", f"{job_id}: depends_on must be a list", loc))
            depends = []

        accept = job.get("accept_check") or {}
        if accept and not isinstance(accept, dict):
            issues.append(Issue("MALFORMED_INPUT", f"{job_id}: accept_check must be an object", loc))
            accept = {}

        scopes = _scope_values(job.get("write_scope"))
        missing_capability = not capability
        if scopes and missing_capability:
            issues.append(Issue("UNKNOWN_CAPABILITY", f"{job_id}: writer capability is unknown", loc))
        writing = bool(scopes) and (capability in DELEGATED_WRITERS or missing_capability)
        if writing and not accept.get("declared"):
            if capability == "cheap-bounded-worker":
                issues.append(Issue("WRITER_NO_ACCEPT_CHECK", f"{job_id}: cheap writing worker needs a predeclared accept check", loc))
            else:
                issues.append(Issue("WRITER_NO_ACCEPT_CHECK", f"{job_id}: writer needs a predeclared accept check", loc))
        elif writing and plan.get("work_kind") == "code" and accept.get("kind") != "executable" and not accept.get("exception"):
            issues.append(Issue("CODE_WRITE_NO_EXECUTABLE_CHECK", f"{job_id}: code writes need an executable accept check", loc))
        if plan.get("work_kind") == "research" and capability in {"cheap-bounded-worker", "material-reviewer", "narrow-verifier"}:
            if accept.get("declared") and accept.get("kind") not in {"source-anchors", "counterevidence", None}:
                issues.append(Issue("UNSUPPORTED_KEY", f"{job_id}: research accept check must be source anchors or counterevidence", loc))
        if capability in DELEGATED_WRITERS and job.get("return") == "transcript":
            issues.append(Issue("TRANSCRIPT_HANDOFF", f"{job_id}: workers return artifacts, not transcripts", loc))
        elif missing_capability and job.get("return") == "transcript":
            issues.append(Issue("TRANSCRIPT_HANDOFF", f"{job_id}: workers return artifacts, not transcripts", loc))

        attempts = job.get("attempts") or []
        if not isinstance(attempts, list):
            issues.append(Issue("MALFORMED_INPUT", f"{job_id}: attempts must be a list", loc))
            attempts = []
        failures = [item for item in attempts if isinstance(item, dict) and item.get("failed")]
        if len(failures) > 1:
            last = failures[-1]
            if not last.get("contract_changed") and not last.get("escalated"):
                issues.append(Issue("REPAIR_WITHOUT_ESCALATION", f"{job_id}: after one failed attempt, change the contract or escalate", loc))
        if len(failures) > 2:
            issues.append(Issue("REPAIR_WITHOUT_ESCALATION", f"{job_id}: more than one retry is forbidden", loc))
        for raw_scope in scopes:
            path_issue = _unsafe_path(raw_scope, job_id)
            if path_issue:
                issues.append(path_issue)

    # Validate dependencies and parallel waves
    for job_id, job in by_id.items():
        depends = job.get("depends_on") or []
        if not isinstance(depends, list):
            continue
        absent = [name for name in depends if name not in by_id]
        if absent:
            issues.append(Issue("UNKNOWN_DEPENDENCY", f"{job_id}: unknown dependency {absent}", job_id))

        if job.get("parallel") is True and depends:
            # Dependent jobs may enter a later parallel wave after dependencies complete.
            # Reject if running parallel alongside uncompleted dependencies in same wave.
            for dep in depends:
                if dep in by_id:
                    dep_job = by_id[dep]
                    dep_lifecycle = str(dep_job.get("lifecycle") or "").lower()
                    if dep_lifecycle != "completed":
                        issues.append(Issue("DEPENDENT_PARALLEL", f"{job_id}: dependent jobs must not run in parallel wave with uncompleted dependency {dep}", job_id))

    if _has_cycle(by_id):
        issues.append(Issue("DEPENDENCY_CYCLE", "dependency cycle"))

    issues.extend(_scope_collisions(by_id))

    workers = [
        job for job in by_id.values()
        if job.get("capability") in DELEGATED_WRITERS
        or (_scope_values(job.get("write_scope")) and not job.get("capability"))
    ]
    reviewers = [job for job in by_id.values() if job.get("capability") == "material-reviewer"]
    if workers:
        if plan.get("break_even") is False:
            issues.append(Issue("DELEGATION_WITHOUT_BREAKEVEN", "failed break-even must not delegate"))
        elif plan.get("break_even") is not True:
            issues.append(Issue("DELEGATION_WITHOUT_BREAKEVEN", "delegation requires explicit positive break-even"))
    if plan.get("lead_repeats_worker") is True:
        issues.append(Issue("LEAD_REPEATS_WORKER", "lead must not redo the worker job"))
    if plan.get("concurrency_as_goal") is True:
        issues.append(Issue("CONCURRENCY_AS_GOAL", "concurrency is a ceiling, not a target"))
    worker_budget = plan.get("worker_budget")
    if worker_budget is not None and len(workers) > worker_budget:
        issues.append(Issue("BUDGET_EXCEEDED", "worker budget exceeded"))
    review_budget = plan.get("review_budget")
    if review_budget is not None and len(reviewers) > review_budget:
        issues.append(Issue("BUDGET_EXCEEDED", "reviewer budget exceeded"))
    retry_budget = plan.get("retry_budget")
    if retry_budget is not None:
        retries = 0
        for job in by_id.values():
            failures = [item for item in (job.get("attempts") or []) if isinstance(item, dict) and item.get("failed")]
            retries += max(0, len(failures) - 1)
        if retries > retry_budget:
            issues.append(Issue("BUDGET_EXCEEDED", "retry budget exceeded"))
    if plan.get("trivial") is True and reviewers:
        issues.append(Issue("TRIVIAL_REVIEWER", "trivial work must not spawn a reviewer"))
    issues.extend(_parallel_isolation(plan, by_id))
    return issues


def _scope_values(value: object) -> list[str]:
    if value is None or value is False:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item.strip()]
    return []


def _unsafe_path(value: str, job_id: str) -> Issue | None:
    if "\\" in value or ":" in value:
        return Issue("UNSAFE_PATH", f"{job_id}: unsafe relative path: {value}", job_id)
    path = PurePosixPath(value)
    if not value.strip() or path.is_absolute() or ".." in path.parts or ".git" in path.parts:
        return Issue("UNSAFE_PATH", f"{job_id}: unsafe relative path: {value}", job_id)
    return None


def _normalize_scope(value: str) -> str:
    parts = [part for part in PurePosixPath(value).parts if part not in {".", ""}]
    return "/".join(parts) if parts else "."


def _has_glob(value: str) -> bool:
    return any(char in value for char in "*?[]")


def _scopes_overlap(left: str, right: str) -> str | None:
    a, b = _normalize_scope(left), _normalize_scope(right)
    if a == b:
        return "exact"
    if _has_glob(left) or _has_glob(right):
        if _has_glob(left) and (fnmatch(b, a) or fnmatch(right, left)):
            return "glob"
        if _has_glob(right) and (fnmatch(a, b) or fnmatch(left, right)):
            return "glob"
        a_lit = left.split("*")[0].split("?")[0]
        b_lit = right.split("*")[0].split("?")[0]
        if a_lit and b_lit and (a_lit.startswith(b_lit) or b_lit.startswith(a_lit)):
            return "glob"
        return None
    a_parts, b_parts = PurePosixPath(a).parts, PurePosixPath(b).parts
    if a_parts == b_parts[: len(a_parts)] or b_parts == a_parts[: len(b_parts)]:
        return "ancestor"
    return None


def _scope_collisions(by_id: dict[str, dict[str, Any]]) -> list[Issue]:
    issues: list[Issue] = []
    owned: list[tuple[str, str]] = []
    for job_id, job in by_id.items():
        for raw in _scope_values(job.get("write_scope")):
            if _unsafe_path(raw, job_id):
                continue
            owned.append((job_id, raw))
    for index, (left_id, left) in enumerate(owned):
        for right_id, right in owned[index + 1 :]:
            if left_id == right_id:
                continue
            kind = _scopes_overlap(left, right)
            if not kind:
                continue

            # Sequential handoff: if jobs are ordered by dependency and predecessor is settled or handed off
            left_job = by_id.get(left_id, {})
            right_job = by_id.get(right_id, {})
            if _is_ordered_dependency(left_id, right_id, by_id):
                left_settled = str(left_job.get("lifecycle") or "").lower() in {"completed", "superseded"}
                is_handoff = right_job.get("ownership_handoff") == left_id or right_job.get("scope_handoff") is True
                if left_settled or is_handoff:
                    continue
            elif _is_ordered_dependency(right_id, left_id, by_id):
                right_settled = str(right_job.get("lifecycle") or "").lower() in {"completed", "superseded"}
                is_handoff = left_job.get("ownership_handoff") == right_id or left_job.get("scope_handoff") is True
                if right_settled or is_handoff:
                    continue

            # Concurrent collision
            if kind == "exact":
                scope = _normalize_scope(left)
                issues.append(Issue("WRITER_SCOPE_OVERLAP", f"shared write-scope {scope} owned by concurrent {left_id} and {right_id}"))
            else:
                issues.append(Issue("WRITER_SCOPE_OVERLAP", f"overlapping writer scopes {left} and {right} owned by concurrent {left_id} and {right_id}"))
    return issues


def _has_cycle(by_id: dict[str, dict[str, Any]]) -> bool:
    graph = {job_id: [] for job_id in by_id}
    indeg = {job_id: 0 for job_id in by_id}
    for job_id, job in by_id.items():
        for dep in job.get("depends_on") or []:
            if dep in by_id:
                graph[dep].append(job_id)
                indeg[job_id] += 1
    ready = [job_id for job_id, count in indeg.items() if count == 0]
    seen = 0
    while ready:
        node = ready.pop()
        seen += 1
        for child in graph[node]:
            indeg[child] -= 1
            if indeg[child] == 0:
                ready.append(child)
    return bool(by_id) and seen < len(by_id)


def _observed_children(value: object) -> list[str]:
    found: list[str] = []
    for item in value or []:
        if isinstance(item, dict):
            ident = item.get("id")
            source = item.get("source")
            if _unknown(ident) or source not in CHILD_SOURCES:
                continue
            found.append(str(ident).strip())
    return found


def _parallel_isolation(plan: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> list[Issue]:
    parallel_writers = [
        job_id
        for job_id, job in by_id.items()
        if job.get("parallel") is True and _scope_values(job.get("write_scope"))
    ]
    scoped = [job_id for job_id, job in by_id.items() if _scope_values(job.get("write_scope"))]
    routes = {_norm_enum(plan.get("planned_route")), _norm_enum(plan.get("observed_route"))}
    if len(parallel_writers) < 2 and not ("isolated_parallel" in routes and len(scoped) >= 2):
        return []
    isolation = plan.get("host_isolation")
    evidence = plan.get("isolation_evidence")
    if isolation in (None, False, ""):
        return [Issue("PARALLEL_WITHOUT_ISOLATION", "parallel writers need host isolation")]
    if isolation is True or str(isolation) not in ISOLATION_VERIFIED | ISOLATION_NONE:
        return [Issue("UNKNOWN_ISOLATION", f"unknown isolation value {isolation}")]
    if str(isolation) in ISOLATION_NONE:
        return [Issue("PARALLEL_WITHOUT_ISOLATION", "parallel writers need host isolation")]

    # Structured isolation receipt validation: prose is rejected
    if isinstance(evidence, str) or _unknown(evidence):
        return [Issue("CLAIMED_ISOLATION_WITHOUT_EVIDENCE", "claimed isolation requires structured host receipt, not prose string")]
    if isinstance(evidence, dict):
        required_keys = {"host", "workspace", "mechanism", "identity"}
        missing_keys = required_keys - set(evidence.keys())
        if missing_keys:
            return [Issue("CLAIMED_ISOLATION_WITHOUT_EVIDENCE", f"isolation receipt missing {sorted(missing_keys)}")]
        if any(_unknown(evidence.get(k)) for k in required_keys):
            return [Issue("CLAIMED_ISOLATION_WITHOUT_EVIDENCE", "isolation receipt has unknown or placeholder fields")]
    else:
        receipt = plan.get("route_receipt")
        obs_iso = receipt.get("observed_isolation") if isinstance(receipt, dict) else None
        if not isinstance(obs_iso, dict) or any(_unknown(obs_iso.get(k)) for k in ("host", "workspace", "mechanism", "identity")):
            return [Issue("CLAIMED_ISOLATION_WITHOUT_EVIDENCE", "claimed isolation without observed structured host evidence")]

    return []


def _delegation_gaps(planned: str, observed: str, children_raw: object, plan: dict[str, Any]) -> list[Issue]:
    child_ids = _observed_children(children_raw)
    if observed in DELEGATED_ROUTES and not child_ids:
        return [Issue("DELEGATION_NOT_OBSERVED", "planned delegation was not observed")]
    if planned in DELEGATED_ROUTES and not child_ids:
        if observed in DELEGATED_ROUTES or not observed:
            return [Issue("DELEGATION_NOT_OBSERVED", "planned delegation was not observed")]
        deviations = list(plan.get("deviations") or [])
        receipt = plan.get("route_receipt") if isinstance(plan.get("route_receipt"), dict) else {}
        deviations.extend(receipt.get("deviations") or [])
        if "DELEGATION_NOT_OBSERVED" not in deviations:
            return [Issue("DELEGATION_NOT_OBSERVED", "planned delegation was not observed")]
    return []


def _job_role(job: dict[str, Any]) -> str:
    explicit = job.get("role")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip()
    capability = job.get("capability")
    if capability == "lead-capable":
        return "lead"
    if capability == "material-reviewer":
        return "reviewer"
    if capability == "narrow-verifier":
        return "verifier"
    return "worker"


def _may_delegate(job: dict[str, Any]) -> bool:
    if "delegation_authority" in job:
        return job.get("delegation_authority") is True
    return _job_role(job) == "lead"


def contract_required(plan: dict[str, Any]) -> bool:
    """Trivial direct work does not need a mission file. Material routes and high-risk direct work do."""
    if not isinstance(plan, dict):
        return True
    risk_level = str(plan.get("risk_level") or "").strip().lower()
    false_pass_cost = str(plan.get("false_pass_cost") or "").strip().lower()
    high_risk_direct = (
        plan.get("release_sensitive") is True
        or risk_level in {"material", "critical"}
        or false_pass_cost in {"high", "critical"}
        or plan.get("acceptance_logic_changed") is True
        or plan.get("acceptance_logic_changes") is True
    )
    if high_risk_direct:
        return True
    if plan.get("trivial") is True and plan.get("simple_sequential") is True:
        return False
    if plan.get("trivial") is True and not high_risk_direct:
        return False
    planned = _norm_enum(plan.get("planned_route")) or "direct"
    if planned == "direct" and plan.get("simple_sequential") is True:
        jobs = [job for job in (plan.get("jobs") or []) if isinstance(job, dict)]
        writers = [job for job in jobs if _job_role(job) != "lead" or _scope_values(job.get("write_scope"))]
        if not writers and planned == "direct":
            return False
    return planned in DELEGATED_ROUTES | {"review", "measurable_optimizer"} or bool(
        _norm_enum(plan.get("observed_route")) in DELEGATED_ROUTES
    )


def _authority(plan: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    jobs = [job for job in (plan.get("jobs") or []) if isinstance(job, dict)]
    by_id = {str(job.get("id")).strip(): job for job in jobs if isinstance(job.get("id"), str) and str(job.get("id")).strip()}
    for job_id, job in by_id.items():
        role = _job_role(job)
        if role not in ROLES:
            issues.append(Issue("UNKNOWN_ROLE", f"{job_id}: unknown role {role}", job_id))
            continue
        parent = job.get("parent_job")
        if parent and parent not in by_id:
            issues.append(Issue("UNKNOWN_DEPENDENCY", f"{job_id}: unknown parent job {parent}", job_id))

        if role in {"reviewer", "verifier"}:
            if _scope_values(job.get("write_scope")):
                code = "REVIEWER_WRITE_FORBIDDEN" if role == "reviewer" else "VERIFIER_WRITE_FORBIDDEN"
                issues.append(Issue(code, f"{job_id}: {role} must be read-only (write_scope forbidden)", job_id))
            pa = job.get("permitted_actions")
            if isinstance(pa, list):
                write_ops = {"write", "edit", "modify", "delete", "create", "patch"}
                if any(str(act).lower() in write_ops for act in pa):
                    code = "REVIEWER_WRITE_FORBIDDEN" if role == "reviewer" else "VERIFIER_WRITE_FORBIDDEN"
                    issues.append(Issue(code, f"{job_id}: {role} permitted_actions cannot include write operations", job_id))
            if job.get("delegation_authority") is True:
                issues.append(Issue("REVIEWER_DELEGATION_FORBIDDEN", f"{job_id}: {role} may not delegate", job_id))

        children = job.get("observed_child_jobs") or []
        nested = [child for child in by_id.values() if child.get("parent_job") == job_id]
        if (children or nested) and not _may_delegate(job):
            issues.append(Issue(
                "UNAUTHORIZED_NESTED_DELEGATION",
                f"{job_id}: {role} created children without delegation_authority",
                job_id,
            ))
    return issues


def _delegation(plan: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    planned = _norm_enum(plan.get("planned_route"))
    observed = _norm_enum(plan.get("observed_route"))
    if planned and planned not in ROUTES:
        issues.append(Issue("UNKNOWN_ROUTE", f"unknown planned route {planned}"))
    if observed and observed not in ROUTES:
        issues.append(Issue("UNKNOWN_ROUTE", f"unknown observed route {observed}"))
    deviations = list(plan.get("deviations") or [])
    receipt = plan.get("route_receipt") if isinstance(plan.get("route_receipt"), dict) else {}
    deviations.extend(receipt.get("deviations") or [])
    if planned and observed and planned != observed:
        labeled = {"ROUTE_MISMATCH", "DELEGATION_NOT_OBSERVED"} & {str(item) for item in deviations}
        if not labeled:
            issues.append(Issue("ROUTE_MISMATCH", f"planned route {planned} differs from observed {observed}"))
    children = plan.get("observed_child_ids")
    if children is None and isinstance(plan.get("route_receipt"), dict):
        children = plan["route_receipt"].get("observed_child_session_ids")
    issues.extend(_delegation_gaps(planned, observed, children, plan))

    jobs = [job for job in (plan.get("jobs") or []) if isinstance(job, dict)]
    workers = [
        job for job in jobs
        if job.get("capability") in DELEGATED_WRITERS
        or (_scope_values(job.get("write_scope")) and not job.get("capability"))
    ]
    is_delegated = (
        planned in DELEGATED_ROUTES
        or observed in DELEGATED_ROUTES
    )
    if is_delegated and not workers:
        dd = plan.get("delegation_decision")
        if plan.get("break_even") is False:
            issues.append(Issue("DELEGATION_WITHOUT_BREAKEVEN", "failed break-even must not delegate"))
        elif plan.get("break_even") is not True:
            if not (isinstance(dd, dict) and dd.get("decision") == "approved"):
                issues.append(Issue("DELEGATION_WITHOUT_BREAKEVEN", "delegation requires explicit positive break-even or approved delegation_decision"))
        elif _unknown(plan.get("break_even_evidence")) and not dd:
            issues.append(Issue("DELEGATION_WITHOUT_BREAKEVEN", "delegated route requires non-empty break_even_evidence or delegation_decision"))

    if "delegation_decision" in plan:
        dd = plan["delegation_decision"]
        if isinstance(dd, dict):
            if dd.get("decision") not in {"approved", "rejected"}:
                issues.append(Issue("INVALID_TYPE", "delegation_decision.decision must be 'approved' or 'rejected'", "delegation_decision.decision"))
            for field in ("reason", "expected_value", "coordination_cost", "confidence"):
                if field not in dd or _unknown(dd[field]):
                    issues.append(Issue("MALFORMED_INPUT", f"delegation_decision missing {field}", f"delegation_decision.{field}"))
            if dd.get("decision") == "rejected" and is_delegated:
                issues.append(Issue("DELEGATION_WITHOUT_BREAKEVEN", "delegation decision rejected"))

    return issues


def _route_receipt(receipt: Any, plan: dict[str, Any]) -> list[Issue]:
    if not isinstance(receipt, dict):
        return [Issue("MALFORMED_INPUT", "route_receipt must be an object")]
    issues: list[Issue] = []
    sensitive_paths = _find_sensitive_receipt_keys(receipt, "route_receipt")
    if sensitive_paths:
        issues.append(Issue("SENSITIVE_DATA_EXPOSED", f"route_receipt forbids sensitive fields {sensitive_paths}"))

    planned = _norm_enum(receipt.get("planned_route") or plan.get("planned_route"))
    observed = _norm_enum(receipt.get("observed_route") or plan.get("observed_route"))
    if planned and planned not in ROUTES:
        issues.append(Issue("UNKNOWN_ROUTE", f"unknown planned route {planned}"))
    if observed and observed not in ROUTES:
        issues.append(Issue("UNKNOWN_ROUTE", f"unknown observed route {observed}"))

    for ceil in ("worker_ceiling", "reviewer_ceiling"):
        if ceil in receipt:
            cval = receipt[ceil]
            if type(cval) is int and type(cval) is not bool:
                if cval < 0:
                    issues.append(Issue("NEGATIVE_CEILING", f"route_receipt.{ceil} must not be negative", f"route_receipt.{ceil}"))
            else:
                issues.append(Issue("INVALID_TYPE", f"route_receipt.{ceil} must be a non-negative integer", f"route_receipt.{ceil}"))

    if "observed_isolation" in receipt:
        obs = receipt["observed_isolation"]
        if not isinstance(obs, dict):
            issues.append(Issue("INVALID_TYPE", "route_receipt.observed_isolation must be an object", "route_receipt.observed_isolation"))
        else:
            extra_obs = set(obs) - {"mechanism", "host", "workspace", "identity", "source", "evidence"}
            if extra_obs:
                issues.append(Issue("UNSUPPORTED_KEY", f"observed_isolation unsupported keys {sorted(extra_obs)}"))

    issues.extend(_delegation_gaps(planned, observed, receipt.get("observed_child_session_ids"), plan))
    return issues


def _optimization(plan: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    optimization = plan.get("optimization")
    planned = _norm_enum(plan.get("planned_route"))
    if planned == "measurable_optimizer" or optimization:
        data = optimization if isinstance(optimization, dict) else {}
        if not data.get("evaluator_frozen"):
            issues.append(Issue("OPTIMIZER_NO_FROZEN_EVALUATOR", "optimizer route requires a frozen evaluator"))
        if data.get("tie") and data.get("keep") != "incumbent":
            issues.append(Issue("OPTIMIZER_TIE_REPLACES_INCUMBENT", "measurable optimization ties keep the incumbent"))
        if data.get("evaluator_changed") and not data.get("new_baseline"):
            issues.append(Issue("EVALUATOR_CHANGE_NO_BASELINE", "a changed evaluator starts a new baseline"))
    return issues


def _artifact_identity(value: object) -> tuple[str, dict[str, Any] | None]:
    if isinstance(value, dict):
        digest = str(value.get("digest") or "").strip()
        return digest, value
    return str(value or "").strip(), None


def _mission(plan: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    mission = plan.get("mission") or {}
    if mission and not isinstance(mission, dict):
        return [Issue("MALFORMED_INPUT", "mission must be an object")]
    overall = str((mission.get("overall") if mission else plan.get("overall")) or "").upper()
    if overall and overall not in VERDICTS:
        issues.append(Issue("UNKNOWN_VERDICT", f"unknown overall verdict {overall}"))

    jobs = [job for job in (plan.get("jobs") or []) if isinstance(job, dict)]
    by_id = {job.get("id"): job for job in jobs if job.get("id")}
    plan_gates = {
        gate.get("id"): gate
        for gate in (plan.get("gates") or [])
        if isinstance(gate, dict) and gate.get("id")
    }

    acceptance_changed = (
        plan.get("acceptance_logic_changed") is True
        or plan.get("acceptance_logic_changes") is True
        or (isinstance(mission, dict) and mission.get("acceptance_logic_changed") is True)
    )
    material_risk = str(plan.get("risk_level") or "").lower() in {"material", "critical"}

    if acceptance_changed or material_risk:
        independence = plan.get("reviewer_independence")
        independent = []
        if independence not in {False, "same-lead", "not-independent", "unknown"}:
            for job in jobs:
                if job.get("capability") != "material-reviewer":
                    continue
                flag = job.get("independent", independence)
                if flag not in {True, "independent"}:
                    continue
                if str(job.get("lifecycle") or "").lower() != "completed":
                    continue
                if str(job.get("verdict") or "").upper() != "PASS":
                    continue
                independent.append(job)
        if overall == "PASS" and not independent:
            issues.append(Issue("PASS_WITHOUT_REVIEW", "overall PASS requires independent review after acceptance-logic change or material risk"))

    if overall != "PASS":
        return issues

    # Overall PASS checks:
    artifact_value = mission.get("artifact", plan.get("candidate_artifact"))
    artifact, artifact_obj = _artifact_identity(artifact_value)
    if not artifact or artifact.casefold() in PLACEHOLDER or artifact == "none":
        issues.append(Issue("PASS_WITHOUT_ARTIFACT", "overall PASS requires a current artifact identity"))
    else:
        stale = mission.get("stale_pass_artifact")
        if stale and artifact and str(stale) != artifact:
            issues.append(Issue("PASS_STALE_EVIDENCE", "stale mission PASS cannot accept a new artifact"))

        method = (artifact_obj.get("identity_method") if artifact_obj else None) or mission.get("identity_method") or plan.get("identity_method")
        algorithm = (artifact_obj.get("digest_algorithm") if artifact_obj else None) or mission.get("digest_algorithm") or plan.get("digest_algorithm")
        digest = (artifact_obj.get("digest") if artifact_obj else None) or artifact

        if method == "none" or algorithm == "none" or digest in PLACEHOLDER or digest == "none":
            issues.append(Issue("PASS_WITHOUT_ARTIFACT", "overall PASS forbids identity_method none or placeholder digest"))

        # Strict SHA formats and method-algorithm compatibility
        if method in {"git-commit", "git-tree"}:
            if algorithm not in {"sha1", "sha256"}:
                issues.append(Issue("ARTIFACT_METHOD_MISMATCH", f"git object method {method} requires sha1 or sha256 algorithm"))
            elif algorithm == "sha1" and not re.fullmatch(r"[0-9a-f]{40}", str(digest).lower()):
                issues.append(Issue("MALFORMED_ARTIFACT_DIGEST", f"git SHA-1 digest {digest} must be exactly 40 hexadecimal characters"))
            elif algorithm == "sha256" and not re.fullmatch(r"[0-9a-f]{64}", str(digest).lower()):
                issues.append(Issue("MALFORMED_ARTIFACT_DIGEST", f"git SHA-256 digest {digest} must be exactly 64 hexadecimal characters"))
        elif method in {"dirty-manifest", "content-digest", "package-digest", "diff-digest"}:
            if algorithm != "sha256":
                issues.append(Issue("ARTIFACT_METHOD_MISMATCH", f"{method} requires sha256 digest algorithm"))
            elif not re.fullmatch(r"[0-9a-f]{64}", str(digest).lower()):
                issues.append(Issue("MALFORMED_ARTIFACT_DIGEST", f"{method} digest {digest} must be exactly 64 hexadecimal characters"))
        elif not artifact_obj:
            if len(str(digest)) < 8 or not re.fullmatch(r"[0-9a-f]+", str(digest).lower()):
                issues.append(Issue("MALFORMED_ARTIFACT_DIGEST", f"artifact identity {digest} is malformed or too short"))

    is_dirty = plan.get("dirty") is True or (artifact_obj and artifact_obj.get("dirty") is True) or mission.get("dirty") is True
    if is_dirty and (method in {"git-commit", "git-tree"} or mission.get("evidence_assumes_clean")):
        issues.append(Issue("PASS_DIRTY_WITH_CLEAN_EVIDENCE", "dirty candidate accepted by clean-artifact evidence"))

    evidence_digest = mission.get("evidence_digest") or (mission.get("evidence_artifact") or {}).get("digest")
    if evidence_digest and digest and str(evidence_digest).strip() != str(digest).strip():
        issues.append(Issue("PASS_STALE_EVIDENCE", f"evidence digest {evidence_digest} does not match artifact digest {digest}"))

    # Required jobs must be bound to plan.jobs
    required_jobs = list(mission.get("required_jobs") or [])
    if not required_jobs:
        required_jobs = [job for job in jobs if job.get("required") is True]
    if not required_jobs:
        issues.append(Issue("PASS_WITH_INCOMPLETE_JOB", "overall PASS requires required jobs"))

    for rjob in required_jobs:
        if not isinstance(rjob, dict):
            issues.append(Issue("MALFORMED_INPUT", "required job must be an object"))
            continue
        job_id = rjob.get("id")
        if not job_id or job_id not in by_id:
            issues.append(Issue("PASS_WITH_INCOMPLETE_JOB", f"overall PASS rejected: required job {job_id} is not bound to plan.jobs"))
            continue
        record = by_id[job_id]
        lifecycle = str(rjob.get("lifecycle") or record.get("lifecycle") or "").lower()
        if lifecycle and lifecycle not in LIFECYCLES:
            issues.append(Issue("UNKNOWN_LIFECYCLE", f"unknown lifecycle {lifecycle}"))
        verdict = str(rjob.get("verdict") or record.get("verdict") or "").upper()
        if verdict and verdict not in VERDICTS:
            issues.append(Issue("UNKNOWN_VERDICT", f"unknown verdict {verdict}"))
        if lifecycle != "completed" or verdict != "PASS":
            issues.append(Issue("PASS_WITH_INCOMPLETE_JOB", f"overall PASS rejected: required job unfinished or negative: {job_id} (not PASS)"))

    # Required gates must be bound to plan.gates
    gates = list(mission.get("required_gates") or mission.get("gates") or plan.get("gates") or [])
    if not gates:
        issues.append(Issue("PASS_WITH_INCOMPLETE_GATE", "overall PASS requires required gates"))
    for gate in gates:
        if not isinstance(gate, dict):
            issues.append(Issue("MALFORMED_INPUT", "gate must be an object"))
            continue
        gate_id = gate.get("id")
        if not gate_id or gate_id not in plan_gates:
            issues.append(Issue("PASS_WITH_INCOMPLETE_GATE", f"overall PASS rejected: required gate {gate_id} is not bound to plan.gates"))
            continue
        record = plan_gates[gate_id]
        status = str(gate.get("status") or record.get("status") or "").upper()
        if status not in GATE_STATUSES:
            issues.append(Issue("UNKNOWN_GATE_STATUS", f"unknown gate status {status}"))
        if status != "PASS":
            issues.append(Issue("PASS_WITH_INCOMPLETE_GATE", f"overall PASS rejected: required gate {gate_id} unfinished or not PASS"))

    # Explicit empty blockers required
    blockers = mission.get("blockers") if "blockers" in mission else plan.get("blockers")
    if blockers is None:
        issues.append(Issue("PASS_WITH_BLOCKER", "overall PASS requires explicit empty blockers"))
    elif len(blockers) > 0:
        issues.append(Issue("PASS_WITH_BLOCKER", "overall PASS with active blockers"))

    return issues


def _learning(plan: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    learning = plan.get("learning") or {}
    if learning and not isinstance(learning, dict):
        return [Issue("MALFORMED_INPUT", "learning must be an object")]
    ordinary = bool(learning.get("ordinary_success"))
    if ordinary and learning.get("started_sleep"):
        issues.append(Issue("ORDINARY_SUCCESS_STARTED_LEARNING", "normal completion must not start Sleep"))
    if ordinary and learning.get("auto_adopted"):
        issues.append(Issue("ORDINARY_SUCCESS_STARTED_LEARNING", "normal completion must not auto-adopt a skill"))
    if ordinary and learning.get("wrote_observation") and not learning.get("reusable_signal"):
        issues.append(Issue("ORDINARY_SUCCESS_STARTED_LEARNING", "ordinary success must not write a learning observation"))
    blob = json.dumps(plan).lower()
    if ordinary and any(marker in blob for marker in SLEEP_MARKERS):
        issues.append(Issue("ORDINARY_SUCCESS_STARTED_LEARNING", "normal completion must not invoke Sleep or harvest"))
    return issues


def validate_product_status(status: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    extra = set(status) - {
        "schema_version", "engineering", "behavioral", "release",
        "independent_behavioral_evidence", "release_decision", "limitations",
        "evidence_run", "evidence_not_run", "artifact_identity",
        "external_actions_not_performed", "not_authorized",
    }
    if extra:
        issues.append(Issue("UNSUPPORTED_KEY", f"unsupported status keys {sorted(extra)}"))
    engineering = str(status.get("engineering") or "").upper()
    behavioral = str(status.get("behavioral") or "").upper()
    release = str(status.get("release") or "")
    if engineering and engineering not in ENGINEERING:
        issues.append(Issue("UNKNOWN_VERDICT", f"unknown engineering status {status.get('engineering')}"))
    if behavioral and behavioral not in BEHAVIORAL:
        issues.append(Issue("UNKNOWN_VERDICT", f"unknown behavioral status {status.get('behavioral')}"))
    if release and release not in RELEASE:
        issues.append(Issue("UNKNOWN_VERDICT", f"unknown release status {status.get('release')}"))
    if behavioral == "PASS" and not status.get("independent_behavioral_evidence"):
        issues.append(Issue("BEHAVIORAL_FROM_ENGINEERING", "behavioral PASS cannot be derived from engineering validation alone"))
    if release == "GO" and not status.get("release_decision"):
        issues.append(Issue("RELEASE_WITHOUT_DECISION", "release GO requires an explicit release decision"))
    return issues


def changed_paths(porcelain: str) -> list[str]:
    changed: list[str] = []
    for line in porcelain.splitlines():
        if len(line) < 3:
            continue
        path = line[2:].lstrip()
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        changed.append(path.replace("\\", "/"))
    return changed


def compute_dirty_source_identity(
    root: Path,
    base_commit: str,
    status_porcelain: str,
    binary_diff_bytes: bytes,
    untracked_files: list[Path] | None = None,
) -> tuple[str, dict[str, Any]]:
    """Compute a canonical SHA-256 bound to base commit, diff, status, modes, renames, and untracked files."""
    diff_hash = hashlib.sha256(binary_diff_bytes).hexdigest()

    untracked_entries: list[dict[str, Any]] = []
    if untracked_files is None:
        untracked_files = []
        for line in status_porcelain.splitlines():
            if line.startswith("??"):
                p = line[3:].strip()
                if p.startswith('"') and p.endswith('"'):
                    p = p[1:-1]
                full = root / p
                if full.is_file():
                    untracked_files.append(full)
                elif full.is_dir():
                    untracked_files.extend(f for f in full.rglob("*") if f.is_file())

    for full_path in sorted(set(untracked_files), key=lambda p: str(p.relative_to(root).as_posix())):
        try:
            rel = full_path.relative_to(root).as_posix()
        except ValueError:
            rel = str(full_path).replace("\\", "/")
        try:
            content = full_path.read_bytes()
            untracked_entries.append({"path": rel, "sha256": hashlib.sha256(content).hexdigest()})
        except OSError:
            untracked_entries.append({"path": rel, "sha256": "unreadable"})

    norm_status = "\n".join(sorted(line.strip().replace("\\", "/") for line in status_porcelain.splitlines() if line.strip()))

    untracked_digest = hashlib.sha256(json.dumps(untracked_entries, sort_keys=True).encode("utf-8")).hexdigest()
    payload = {
        "base_commit": str(base_commit or "unknown").strip(),
        "binary_diff_sha256": diff_hash,
        "dirty": True,
        "status_porcelain": norm_status,
        "untracked_files": untracked_entries,
        "untracked_manifest_digest": untracked_digest,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    return digest, payload


def dirty_manifest_digest(root: Path, changed: list[str], dirty: bool, base_commit: str = "base-commit") -> str:
    """Compute dirty manifest digest bound to files and base commit."""
    status_lines = [f" M {p}" for p in changed]
    diff_parts = []
    untracked = []
    for p in changed:
        full = root / p
        if full.is_file():
            b = full.read_bytes()
            diff_parts.append(f"{p}:{hashlib.sha256(b).hexdigest()}".encode("utf-8"))
            untracked.append(full)
        else:
            diff_parts.append(f"{p}:missing".encode("utf-8"))
    binary_diff_bytes = b"".join(diff_parts)
    digest, _ = compute_dirty_source_identity(
        root=root,
        base_commit=base_commit,
        status_porcelain="\n".join(status_lines),
        binary_diff_bytes=binary_diff_bytes,
        untracked_files=untracked,
    )
    return digest


def inspect_worktree(root: Path | None = None) -> dict[str, Any]:
    root = (root or Path.cwd()).resolve()

    def git(*args: str, text: bool = True) -> Any:
        try:
            result = subprocess.run(("git", "-C", str(root), *args), capture_output=True, text=text, check=False)
        except OSError:
            return None if text else b""
        if result.returncode != 0:
            return None if text else b""
        return result.stdout.strip() if text else result.stdout

    commit = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    porcelain = git("status", "--porcelain=v1", "-uall")
    dirty = bool(porcelain)
    if dirty:
        binary_diff = git("diff", "--binary", "--full-index", "HEAD", text=False) or b""
        digest, _ = compute_dirty_source_identity(
            root=root,
            base_commit=commit or "unknown",
            status_porcelain=porcelain or "",
            binary_diff_bytes=binary_diff,
        )
        changed = changed_paths(porcelain or "")
    else:
        digest = tree or "unknown"
        changed = ["."]

    return {
        "schema_version": SCHEMA_VERSION,
        "type": "source-tree",
        "identity_method": "dirty-manifest" if dirty else "git-tree",
        "digest_algorithm": "sha256" if dirty else "sha1",
        "digest": digest,
        "base_commit": commit or "unknown",
        "git_tree": tree or "unknown",
        "dirty": dirty,
        "included_paths": changed,
        "excluded_paths": [".git"],
        "generation_command": "git rev-parse HEAD^{tree} && git status --porcelain=v1 -uall; binary diff & untracked sha256",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verification": "NOT VERIFIED",
        "note": "commit SHA is observational; do not embed it in a tracked self-hash",
    }


def validate_host_attempt(
    active_attempt: dict[str, Any],
    incoming_task_id: str,
    incoming_dispatch_id: str,
    message_type: str = "worker_done",
    outcome: str | None = None,
) -> dict[str, Any]:
    """Pure host-neutral lifecycle decision for dispatches/attempts."""
    task_id = active_attempt.get("task_id")
    active_dispatch_id = active_attempt.get("active_dispatch_id") or active_attempt.get("dispatch_id")
    status = active_attempt.get("status", "active")

    if not incoming_dispatch_id:
        return {
            "decision": "REJECTED",
            "reason": "MISSING_DISPATCH_ID",
            "message": "incoming completion message is missing dispatch_id",
            "active_dispatch_id": active_dispatch_id,
        }

    if incoming_task_id != task_id:
        return {
            "decision": "REJECTED",
            "reason": "TASK_ID_MISMATCH",
            "message": f"incoming task_id {incoming_task_id} does not match active task {task_id}",
            "active_task_id": task_id,
        }

    if status != "active":
        return {
            "decision": "REJECTED",
            "reason": "ATTEMPT_NOT_ACTIVE",
            "message": f"active attempt status is {status}, not active",
            "status": status,
        }

    if incoming_dispatch_id != active_dispatch_id:
        return {
            "decision": "REJECTED",
            "reason": "STALE_DISPATCH_REJECTED",
            "message": f"stale dispatch {incoming_dispatch_id} cannot complete active dispatch {active_dispatch_id}",
            "active_dispatch_id": active_dispatch_id,
        }

    return {
        "decision": "ACCEPTED",
        "reason": "DISPATCH_MATCH",
        "message": "incoming dispatch matches active attempt",
        "active_dispatch_id": active_dispatch_id,
        "outcome": outcome or "PASS",
    }


def seeded_adversary(seed: int = 20260918) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    cases: list[dict[str, Any]] = []
    count = rng.randint(2, 4)
    cases.append({
        "id": "gen-duplicate-ids",
        "schema_version": 1,
        "jobs": [{"id": "dup", "depends_on": []} for _ in range(count)],
        "expect_codes": ["DUPLICATE_JOB_ID"],
    })
    length = rng.choice((2, 3, 4, 5))
    cases.append({
        "id": f"gen-cycle-{length}",
        "schema_version": 1,
        "jobs": [{"id": f"n{index}", "depends_on": [f"n{(index + 1) % length}"]} for index in range(length)],
        "expect_codes": ["DEPENDENCY_CYCLE"],
    })
    pairs = (("src/a.py", "src/a.py"), ("src", "src/x.py"), ("./lib/x.py", "lib/x.py"), ("lib/*", "lib/x.py"))
    for index, (left, right) in enumerate(pairs):
        cases.append({
            "id": f"gen-scope-{index}",
            "schema_version": 1,
            "break_even": True,
            "jobs": [
                {"id": "w1", "write_scope": [left], "capability": "focused-general-worker", "accept_check": {"declared": True, "kind": "executable"}},
                {"id": "w2", "write_scope": [right], "capability": "focused-general-worker", "accept_check": {"declared": True, "kind": "executable"}},
            ],
            "expect_codes": ["WRITER_SCOPE_OVERLAP"],
        })
    for state in ("ready", "complete", "done"):
        cases.append({
            "id": f"gen-lifecycle-{state}",
            "schema_version": 1,
            "jobs": [{"id": "x", "lifecycle": state}],
            "expect_codes": ["UNKNOWN_LIFECYCLE"],
        })
    return cases


def _writer(job_id: str, scope: str | list[str], **extra: Any) -> dict[str, Any]:
    job = {
        "id": job_id,
        "write_scope": [scope] if isinstance(scope, str) else list(scope),
        "capability": "focused-general-worker",
        "accept_check": {"declared": True, "kind": "executable"},
        "return": "artifact",
    }
    job.update(extra)
    return job


def _pass_mission(**extra: Any) -> dict[str, Any]:
    valid_sha1 = "a" * 40
    mission = {
        "overall": "PASS",
        "artifact": {
            "identity_method": "git-commit",
            "digest_algorithm": "sha1",
            "digest": valid_sha1,
            "dirty": False,
        },
        "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
        "required_gates": [{"id": "g1", "status": "PASS", "evidence": f"check on {valid_sha1}"}],
        "blockers": [],
    }
    mission.update(extra)
    return mission


TRUTH_CASES: list[dict[str, Any]] = [
    {"id": "01-missing-job-id", "schema_version": 1, "jobs": [{"depends_on": []}], "expect_codes": ["MISSING_JOB_ID"]},
    {"id": "02-duplicate-job-ids", "schema_version": 1, "jobs": [{"id": "a"}, {"id": "a"}], "expect_codes": ["DUPLICATE_JOB_ID"]},
    {"id": "03-unknown-dependency", "schema_version": 1, "jobs": [{"id": "b", "depends_on": ["z"]}], "expect_codes": ["UNKNOWN_DEPENDENCY"]},
    {"id": "04-direct-cycle", "schema_version": 1, "jobs": [{"id": "a", "depends_on": ["b"]}, {"id": "b", "depends_on": ["a"]}], "expect_codes": ["DEPENDENCY_CYCLE"]},
    {"id": "05-long-cycle", "schema_version": 1, "jobs": [{"id": "a", "depends_on": ["b"]}, {"id": "b", "depends_on": ["c"]}, {"id": "c", "depends_on": ["a"]}], "expect_codes": ["DEPENDENCY_CYCLE"]},
    {"id": "06-exact-scope", "schema_version": 1, "break_even": True, "jobs": [_writer("a", "app.py"), _writer("b", "app.py")], "expect_codes": ["WRITER_SCOPE_OVERLAP"]},
    {"id": "07-parent-child-scope", "schema_version": 1, "break_even": True, "jobs": [_writer("a", "src"), _writer("b", "src/a.py")], "expect_codes": ["WRITER_SCOPE_OVERLAP"]},
    {"id": "08-normalized-scope", "schema_version": 1, "break_even": True, "jobs": [_writer("a", "./src/a.py"), _writer("b", "src/a.py")], "expect_codes": ["WRITER_SCOPE_OVERLAP"]},
    {"id": "09-glob-scope", "schema_version": 1, "break_even": True, "jobs": [_writer("a", "src/*"), _writer("b", "src/a.py")], "expect_codes": ["WRITER_SCOPE_OVERLAP"]},
    {
        "id": "10-writer-no-accept",
        "schema_version": 1,
        "break_even": True,
        "work_kind": "code",
        "jobs": [{"id": "patch", "capability": "cheap-bounded-worker", "write_scope": ["mod.py"], "accept_check": {"declared": False}}],
        "expect_codes": ["WRITER_NO_ACCEPT_CHECK"],
    },
    {
        "id": "10b-code-write-non-executable",
        "schema_version": 1,
        "break_even": True,
        "work_kind": "code",
        "jobs": [{"id": "patch", "capability": "cheap-bounded-worker", "write_scope": ["mod.py"], "accept_check": {"declared": True, "kind": "manual"}}],
        "expect_codes": ["CODE_WRITE_NO_EXECUTABLE_CHECK"],
    },
    {
        "id": "11-focused-no-accept",
        "schema_version": 1,
        "break_even": True,
        "jobs": [{"id": "w", "capability": "focused-general-worker", "write_scope": ["a.py"], "accept_check": {"declared": False}}],
        "expect_codes": ["WRITER_NO_ACCEPT_CHECK"],
    },
    {
        "id": "11b-writer-no-capability",
        "schema_version": 1,
        "jobs": [{"id": "w", "write_scope": ["a.py"]}],
        "expect_codes": ["UNKNOWN_CAPABILITY", "WRITER_NO_ACCEPT_CHECK", "DELEGATION_WITHOUT_BREAKEVEN"],
    },
    {
        "id": "12-missing-breakeven",
        "schema_version": 1,
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_WITHOUT_BREAKEVEN"],
    },
    {
        "id": "13-failed-breakeven",
        "schema_version": 1,
        "break_even": False,
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_WITHOUT_BREAKEVEN"],
    },
    {
        "id": "14-unknown-isolation",
        "schema_version": 1,
        "break_even": True,
        "host_isolation": "maybe",
        "jobs": [_writer("a", "a.py", parallel=True), _writer("b", "b.py", parallel=True)],
        "expect_codes": ["UNKNOWN_ISOLATION"],
    },
    {
        "id": "15-claimed-isolation",
        "schema_version": 1,
        "break_even": True,
        "host_isolation": "worktree",
        "jobs": [_writer("a", "a.py", parallel=True), _writer("b", "b.py", parallel=True)],
        "expect_codes": ["CLAIMED_ISOLATION_WITHOUT_EVIDENCE"],
    },
    {
        "id": "15b-weak-isolation-evidence",
        "schema_version": 1,
        "break_even": True,
        "host_isolation": "worktree",
        "isolation_evidence": "claimed",
        "jobs": [_writer("a", "a.py", parallel=True), _writer("b", "b.py", parallel=True)],
        "expect_codes": ["CLAIMED_ISOLATION_WITHOUT_EVIDENCE"],
    },
    {
        "id": "15c-isolated-parallel-route",
        "schema_version": 1,
        "break_even": True,
        "planned_route": "isolated_parallel",
        "jobs": [_writer("a", "a.py"), _writer("b", "b.py")],
        "expect_codes": ["PARALLEL_WITHOUT_ISOLATION", "DELEGATION_NOT_OBSERVED"],
    },
    {
        "id": "16-planned-no-child",
        "schema_version": 1,
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "sequential_delegated",
        "observed_child_ids": [],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_NOT_OBSERVED"],
    },
    {
        "id": "16b-observed-delegated-no-child",
        "schema_version": 1,
        "break_even": True,
        "planned_route": "direct",
        "observed_route": "sequential_delegated",
        "observed_child_ids": [],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_NOT_OBSERVED", "ROUTE_MISMATCH"],
    },
    {
        "id": "16c-bare-string-child",
        "schema_version": 1,
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "sequential_delegated",
        "observed_child_ids": ["session-abc"],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_NOT_OBSERVED"],
    },
    {
        "id": "16d-fallback-unlabeled",
        "schema_version": 1,
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "direct",
        "fallback_route": "direct",
        "observed_child_ids": [],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_NOT_OBSERVED", "ROUTE_MISMATCH"],
    },
    {
        "id": "16e-structured-child-ok",
        "schema_version": 1,
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "sequential_delegated",
        "observed_child_ids": [{"id": "sess-1", "source": "host-reported"}],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": [],
    },
    {
        "id": "17-unknown-lifecycle",
        "schema_version": 1,
        "jobs": [{"id": "j1", "required": True}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(required_jobs=[{"id": "j1", "lifecycle": "ready", "verdict": "PASS"}]),
        "expect_codes": ["UNKNOWN_LIFECYCLE", "PASS_WITH_INCOMPLETE_JOB"],
    },
    {
        "id": "18-pass-queued",
        "schema_version": 1,
        "jobs": [{"id": "j1", "required": True, "lifecycle": "queued", "verdict": "NOT VERIFIED"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(required_jobs=[{"id": "j1", "lifecycle": "queued", "verdict": "NOT VERIFIED"}]),
        "expect_codes": ["PASS_WITH_INCOMPLETE_JOB"],
    },
    {
        "id": "18b-ghost-required-job",
        "schema_version": 1,
        "jobs": [{"id": "real", "lifecycle": "queued", "verdict": "NOT VERIFIED", "required": True}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(required_jobs=[{"id": "ghost", "lifecycle": "completed", "verdict": "PASS"}]),
        "expect_codes": ["PASS_WITH_INCOMPLETE_JOB"],
    },
    {
        "id": "19-pass-gate-unknown",
        "schema_version": 1,
        "jobs": [{"id": "j1", "required": True, "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "UNKNOWN"}],
        "mission": _pass_mission(required_gates=[{"id": "g1", "status": "UNKNOWN"}]),
        "expect_codes": ["UNKNOWN_GATE_STATUS", "PASS_WITH_INCOMPLETE_GATE"],
    },
    {
        "id": "19b-pass-missing-gates",
        "schema_version": 1,
        "jobs": [{"id": "j1", "required": True, "lifecycle": "completed", "verdict": "PASS"}],
        "mission": {
            "overall": "PASS",
            "artifact": {
                "identity_method": "git-commit",
                "digest_algorithm": "sha1",
                "digest": "a" * 40,
                "dirty": False,
            },
            "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
            "blockers": [],
        },
        "expect_codes": ["PASS_WITH_INCOMPLETE_GATE"],
    },
    {
        "id": "20-pass-blocker",
        "schema_version": 1,
        "jobs": [{"id": "j1", "required": True, "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(blockers=["signing credential unavailable"]),
        "expect_codes": ["PASS_WITH_BLOCKER"],
    },
    {
        "id": "21-stale-artifact",
        "schema_version": 1,
        "jobs": [{"id": "j1", "required": True, "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(
            artifact={"type": "source-tree", "identity_method": "git-tree", "digest_algorithm": "sha1", "digest": "b" * 40, "dirty": False},
            evidence_digest="a" * 40,
        ),
        "expect_codes": ["PASS_STALE_EVIDENCE"],
    },
    {
        "id": "22-dirty-clean-evidence",
        "schema_version": 1,
        "jobs": [{"id": "j1", "required": True, "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(dirty=True, evidence_assumes_clean=True),
        "expect_codes": ["PASS_DIRTY_WITH_CLEAN_EVIDENCE"],
    },
    {
        "id": "22b-dirty-git-tree",
        "schema_version": 1,
        "jobs": [{"id": "j1", "required": True, "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(
            artifact={"type": "source-tree", "identity_method": "git-tree", "digest_algorithm": "sha1", "digest": "b" * 40, "dirty": True},
            evidence_assumes_clean=False,
        ),
        "expect_codes": ["PASS_DIRTY_WITH_CLEAN_EVIDENCE"],
    },
    {
        "id": "23-accept-change-no-review",
        "schema_version": 1,
        "acceptance_logic_changed": True,
        "jobs": [{"id": "j1", "required": True, "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(),
        "expect_codes": ["PASS_WITHOUT_REVIEW"],
    },
    {
        "id": "23b-queued-reviewer",
        "schema_version": 1,
        "acceptance_logic_changed": True,
        "jobs": [
            {"id": "j1", "required": True, "lifecycle": "completed", "verdict": "PASS"},
            {"id": "review", "capability": "material-reviewer", "independent": True, "lifecycle": "queued", "verdict": "NOT VERIFIED"},
        ],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(),
        "expect_codes": ["PASS_WITHOUT_REVIEW"],
    },
    {
        "id": "23c-same-lead-reviewer",
        "schema_version": 1,
        "acceptance_logic_changed": True,
        "reviewer_independence": "same-lead",
        "jobs": [
            {"id": "j1", "required": True, "lifecycle": "completed", "verdict": "PASS"},
            {"id": "review", "capability": "material-reviewer", "lifecycle": "completed", "verdict": "PASS"},
        ],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(),
        "expect_codes": ["PASS_WITHOUT_REVIEW"],
    },
    {
        "id": "25-optimizer-no-frozen",
        "schema_version": 1,
        "planned_route": "measurable_optimizer",
        "optimization": {"tie": False, "keep": "incumbent"},
        "expect_codes": ["OPTIMIZER_NO_FROZEN_EVALUATOR"],
    },
    {
        "id": "26-optimizer-tie",
        "schema_version": 1,
        "optimization": {"evaluator_frozen": True, "tie": True, "keep": "candidate"},
        "expect_codes": ["OPTIMIZER_TIE_REPLACES_INCUMBENT"],
    },
    {
        "id": "27-evaluator-change",
        "schema_version": 1,
        "optimization": {"evaluator_frozen": True, "evaluator_changed": True, "new_baseline": False},
        "expect_codes": ["EVALUATOR_CHANGE_NO_BASELINE"],
    },
    {
        "id": "28-ordinary-learning",
        "schema_version": 1,
        "learning": {"ordinary_success": True, "started_sleep": True, "auto_adopted": True},
        "expect_codes": ["ORDINARY_SUCCESS_STARTED_LEARNING"],
    },
    {
        "id": "29-transcript",
        "schema_version": 1,
        "break_even": True,
        "jobs": [_writer("w", "a.py", **{"return": "transcript"})],
        "expect_codes": ["TRANSCRIPT_HANDOFF"],
    },
    {
        "id": "30-budget-overflow",
        "schema_version": 1,
        "break_even": True,
        "worker_budget": 0,
        "review_budget": 0,
        "retry_budget": 0,
        "jobs": [
            {
                **_writer("w", "a.py", capability="cheap-bounded-worker"),
                "attempts": [{"failed": True, "escalated": True}, {"failed": True, "escalated": True}],
            },
            {"id": "r", "capability": "material-reviewer"},
        ],
        "expect_codes": ["BUDGET_EXCEEDED"],
    },
    {
        "id": "unsafe-path",
        "schema_version": 1,
        "break_even": True,
        "jobs": [_writer("a", "../secret")],
        "expect_codes": ["UNSAFE_PATH"],
    },
    {
        "id": "honest-fallback",
        "schema_version": 1,
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "direct",
        "fallback_route": "direct",
        "deviations": ["DELEGATION_NOT_OBSERVED"],
        "observed_child_ids": [],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": [],
    },
    {
        "id": "isolated-parallel-ok",
        "schema_version": 1,
        "break_even": True,
        "host_isolation": "worktree",
        "isolation_evidence": {
            "host": "cursor",
            "workspace": "worktree",
            "mechanism": "git-worktree",
            "identity": "wt-a,wt-b",
            "source": "host-reported",
        },
        "isolation_workspace": "worktree",
        "jobs": [_writer("a", "a.py", parallel=True), _writer("b", "b.py", parallel=True)],
        "expect_codes": [],
    },
    {
        "id": "status-behavioral-from-eng",
        "schema_version": 1,
        "product_status": {"engineering": "PASS", "behavioral": "PASS", "release": "NO-GO"},
        "expect_codes": ["BEHAVIORAL_FROM_ENGINEERING"],
    },
    {
        "id": "role-worker-nested",
        "schema_version": 1,
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "sequential_delegated",
        "observed_child_ids": [{"id": "child-1", "source": "host-reported"}],
        "jobs": [
            _writer("w", "a.py", capability="cheap-bounded-worker", role="worker", observed_child_jobs=["nested"]),
            {"id": "nested", "parent_job": "w", "capability": "cheap-bounded-worker", "write_scope": ["b.py"], "accept_check": {"declared": True, "kind": "executable"}, "return": "artifact"},
        ],
        "expect_codes": ["UNAUTHORIZED_NESTED_DELEGATION"],
    },
    {
        "id": "role-reviewer-write",
        "schema_version": 1,
        "jobs": [{"id": "r", "role": "reviewer", "capability": "material-reviewer", "write_scope": ["src/fix.py"]}],
        "expect_codes": ["REVIEWER_WRITE_FORBIDDEN"],
    },
    {
        "id": "role-worker-default-ok",
        "schema_version": 1,
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "sequential_delegated",
        "observed_child_ids": [{"id": "sess-1", "source": "host-reported"}],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker", role="worker", delegation_authority=False)],
        "expect_codes": [],
    },
    # New strict-schema and adversarial truth cases
    {"id": "strict-missing-schema-version", "jobs": [], "expect_codes": ["MISSING_SCHEMA_VERSION"]},
    {"id": "strict-unsupported-schema-version-str", "schema_version": "1", "jobs": [], "expect_codes": ["UNSUPPORTED_SCHEMA_VERSION"]},
    {"id": "strict-unsupported-schema-version-num", "schema_version": 2, "jobs": [], "expect_codes": ["UNSUPPORTED_SCHEMA_VERSION"]},
    {"id": "strict-string-bool-delegation", "schema_version": 1, "jobs": [{"id": "w", "delegation_authority": "false"}], "expect_codes": ["INVALID_TYPE"]},
    {"id": "strict-string-bool-trivial", "schema_version": 1, "trivial": "false", "expect_codes": ["INVALID_TYPE"]},
    {"id": "strict-non-int-budget", "schema_version": 1, "worker_budget": "1", "expect_codes": ["INVALID_TYPE"]},
    {"id": "strict-negative-budget", "schema_version": 1, "worker_budget": -1, "expect_codes": ["NEGATIVE_CEILING"]},
    {"id": "strict-non-list-scope", "schema_version": 1, "jobs": [{"id": "w", "write_scope": 123}], "expect_codes": ["INVALID_TYPE"]},
    {
        "id": "strict-mixed-scope-list",
        "schema_version": 1,
        "break_even": True,
        "jobs": [
            {
                "id": "w",
                "capability": "focused-general-worker",
                "write_scope": ["src", 123],
                "accept_check": {"declared": True, "kind": "executable"},
                "return": "artifact",
            }
        ],
        "expect_codes": ["INVALID_TYPE"],
    },
    {
        "id": "strict-unbound-required-job",
        "schema_version": 1,
        "jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(required_jobs=[{"id": "unbound_job", "lifecycle": "completed", "verdict": "PASS"}]),
        "expect_codes": ["PASS_WITH_INCOMPLETE_JOB"],
    },
    {
        "id": "strict-unbound-required-gate",
        "schema_version": 1,
        "jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(required_gates=[{"id": "unbound_gate", "status": "PASS"}]),
        "expect_codes": ["PASS_WITH_INCOMPLETE_GATE"],
    },
    {
        "id": "strict-one-char-artifact",
        "schema_version": 1,
        "jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(artifact="x"),
        "expect_codes": ["MALFORMED_ARTIFACT_DIGEST"],
    },
    {
        "id": "strict-malformed-sha1",
        "schema_version": 1,
        "jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(artifact={"identity_method": "git-commit", "digest_algorithm": "sha1", "digest": "not-a-valid-sha1", "dirty": False}),
        "expect_codes": ["MALFORMED_ARTIFACT_DIGEST"],
    },
    {
        "id": "strict-malformed-sha256",
        "schema_version": 1,
        "jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(artifact={"identity_method": "dirty-manifest", "digest_algorithm": "sha256", "digest": "deadbeef", "dirty": True}),
        "expect_codes": ["MALFORMED_ARTIFACT_DIGEST"],
    },
    {
        "id": "strict-method-algorithm-mismatch",
        "schema_version": 1,
        "jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(artifact={"identity_method": "dirty-manifest", "digest_algorithm": "sha1", "digest": "a" * 40, "dirty": True}),
        "expect_codes": ["ARTIFACT_METHOD_MISMATCH"],
    },
    {
        "id": "strict-pass-method-none",
        "schema_version": 1,
        "jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
        "gates": [{"id": "g1", "status": "PASS"}],
        "mission": _pass_mission(artifact={"identity_method": "none", "digest_algorithm": "none", "digest": "none", "dirty": False}),
        "expect_codes": ["PASS_WITHOUT_ARTIFACT"],
    },
    {
        "id": "strict-nested-sensitive-receipt",
        "schema_version": 1,
        "route_receipt": {"details": {"prompt": "secret instructions"}},
        "expect_codes": ["SENSITIVE_DATA_EXPOSED"],
    },
    {
        "id": "strict-self-authored-isolation-prose",
        "schema_version": 1,
        "break_even": True,
        "host_isolation": "worktree",
        "isolation_evidence": "I ran this in a temporary worktree securely",
        "jobs": [_writer("a", "a.py", parallel=True), _writer("b", "b.py", parallel=True)],
        "expect_codes": ["CLAIMED_ISOLATION_WITHOUT_EVIDENCE"],
    },
    {
        "id": "strict-lead-only-simple-sequential",
        "schema_version": 1,
        "simple_sequential": True,
        "jobs": [{"id": "lead-job", "role": "lead", "capability": "lead-capable"}],
        "expect_codes": [],
    },
    {
        "id": "strict-sequential-scope-handoff",
        "schema_version": 1,
        "break_even": True,
        "jobs": [
            _writer("job1", "auth.py", lifecycle="completed", verdict="PASS"),
            _writer("job2", "auth.py", depends_on=["job1"], ownership_handoff="job1"),
        ],
        "expect_codes": [],
    },
]


def _codes(plan: dict[str, Any]) -> list[str]:
    return [issue.code for issue in validate(plan)]


def _exact(found: list[str], expected: list[str]) -> tuple[list[str], list[str]]:
    missing = [code for code in expected if code not in found]
    extra = [code for code in found if code not in expected]
    return missing, extra


def self_check() -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    cases = list(TRUTH_CASES) + seeded_adversary()
    for case in cases:
        expected = list(case["expect_codes"])
        test_payload = {key: value for key, value in case.items() if key not in {"id", "expect_codes"}}
        found = _codes(test_payload)
        miss, extra_codes = _exact(found, expected)
        if miss or extra_codes:
            failures.append({"id": case["id"], "missing": miss, "extra": extra_codes, "found": found})
    malformed = validate("not-an-object")
    if [item.code for item in malformed] != ["MALFORMED_INPUT"]:
        failures.append({"id": "malformed-root", "found": [item.code for item in malformed]})
    empty_res = validate({})
    if [item.code for item in empty_res] != ["MISSING_SCHEMA_VERSION"]:
        failures.append({"id": "empty-root-missing-schema-version", "found": [item.code for item in empty_res]})
    parsed = changed_paths(" M .claude/GOAL.md\n?? templates/control-contract.json\n")
    if parsed != [".claude/GOAL.md", "templates/control-contract.json"]:
        failures.append({"id": "dotfile-dirty-manifest", "found": parsed})
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        sample = root / "a.py"
        sample.write_text("one", encoding="utf-8")
        first = dirty_manifest_digest(root, ["a.py"], True)
        sample.write_text("two", encoding="utf-8")
        second = dirty_manifest_digest(root, ["a.py"], True)
        if first == second:
            failures.append({"id": "dirty-manifest-same-paths-different-bytes", "found": [first]})
    return {
        "status": "PASS" if not failures else "FAIL",
        "cases": len(cases) + 4,
        "failures": failures,
        "note": "truth-layer contract self-check; not agent behavior",
    }


def parse_mission_view(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    overall = re.search(r"^overall:\s*(.+)\s*$", text, re.M)
    if overall:
        fields["overall"] = overall.group(1).strip()
    for key, label in (
        ("planned_route", "Planned route"),
        ("observed_route", "Observed route"),
        ("deviation", "Deviation"),
        ("artifact", "Current artifact"),
    ):
        match = re.search(rf"^{label}:\s*(.+)\s*$", text, re.M)
        if match:
            fields[key] = match.group(1).strip()
    return fields


def compare_mission_view(plan: dict[str, Any], markdown: str) -> list[Issue]:
    fields = parse_mission_view(markdown)
    issues: list[Issue] = []
    planned = _norm_enum(plan.get("planned_route"))
    observed = _norm_enum(plan.get("observed_route"))
    overall = str(plan.get("overall") or (plan.get("mission") or {}).get("overall") or "").strip()
    if planned and fields.get("planned_route") and fields["planned_route"] != planned:
        issues.append(Issue("MISSION_VIEW_DRIFT", f"mission view planned_route {fields['planned_route']!r} != {planned!r}"))
    if observed and fields.get("observed_route") and fields["observed_route"] != observed:
        issues.append(Issue("MISSION_VIEW_DRIFT", f"mission view observed_route {fields['observed_route']!r} != {observed!r}"))
    if overall and fields.get("overall") and fields["overall"] != overall:
        issues.append(Issue("MISSION_VIEW_DRIFT", f"mission view overall {fields['overall']!r} != {overall!r}"))
    if planned and "planned_route" not in fields:
        issues.append(Issue("MISSION_VIEW_DRIFT", "mission view missing Planned route"))
    if observed and "observed_route" not in fields:
        issues.append(Issue("MISSION_VIEW_DRIFT", "mission view missing Observed route"))
    return issues


def render_mission_view(plan: dict[str, Any]) -> str:
    planned = _norm_enum(plan.get("planned_route")) or "direct"
    observed = _norm_enum(plan.get("observed_route")) or planned
    overall = str(plan.get("overall") or "NOT VERIFIED")
    deviations = plan.get("deviations") or ["none"]
    children = _observed_children(plan.get("observed_child_ids") or [])
    isolation = plan.get("host_isolation") or "none"
    artifact = plan.get("candidate_artifact") or {}
    digest = artifact.get("digest") if isinstance(artifact, dict) else artifact
    jobs = plan.get("jobs") or []
    job_rows = []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        job_rows.append(
            "| {id} | {role} | {agent} | {required} | {lifecycle} | {verdict} | {scope} |".format(
                id=job.get("id") or "job",
                role=_job_role(job),
                agent=job.get("capability") or "unassigned",
                required="yes" if job.get("required", True) else "no",
                lifecycle=job.get("lifecycle") or "queued",
                verdict=job.get("verdict") or "NOT VERIFIED",
                scope=", ".join(_scope_values(job.get("write_scope"))) or "Named owned paths",
            )
        )
    if not job_rows:
        job_rows.append("| required-work | lead | lead-capable | yes | queued | NOT VERIFIED | Named owned paths |")
    return (
        f"schema_version: 1\n"
        f"overall: {overall}\n\n"
        "# Mission View\n\n"
        "## Goal / Definition of Done\n\n"
        f"{plan.get('objective') or 'State the objective.'}\n\n"
        "## Base and candidate\n\n"
        f"Current artifact: {digest or 'NOT VERIFIED'}\n"
        "Base: NOT VERIFIED until a recoverable snapshot exists.\n"
        "Candidate: none.\n\n"
        "## Route\n\n"
        f"Planned route: {planned}\n"
        f"Observed route: {observed}\n"
        f"Deviation: {', '.join(str(item) for item in deviations)}\n"
        f"Observed agents/threads: {', '.join(children) or 'none'}\n"
        f"Observed isolation: {isolation}\n\n"
        "## Hard gates\n\n"
        "| Gate | Status | Evidence |\n"
        "|---|---|---|\n"
        "| Required acceptance check | NOT VERIFIED | No executed check yet |\n\n"
        "## Authority\n\n"
        f"Authorized: {plan.get('authority') or 'only the user current task scope'}.\n"
        "Forbidden: credentials, push, deploy, destructive work and new authority.\n\n"
        "## Jobs\n\n"
        "| Job | Role | Agent | Required | Lifecycle | Verdict | Owned scope |\n"
        "|---|---|---|---|---|---|---|\n"
        + "\n".join(job_rows) + "\n\n"
        "## Decisions and evidence\n\n"
        "NOT VERIFIED until checks run.\n\n"
        "## Blockers\n\n"
        "None.\n\n"
        "## Next action\n\n"
        "Run the named acceptance check on the current artifact.\n\n"
        "## Last verified\n\n"
        "Commit/snapshot: NOT VERIFIED. UTC timestamp: NOT VERIFIED.\n"
        "External actions not performed: push, merge, tag, release.\n"
    )


def check_contract(data: Any, markdown: str | None = None) -> dict[str, Any]:
    if not isinstance(data, dict):
        issues = [Issue("MALFORMED_INPUT", "malformed contract: plan must be an object")]
    else:
        issues = validate(data)
        if markdown:
            issues.extend(compare_mission_view(data, markdown))

    valid = not issues
    contract_validity = "VALID" if valid else "INVALID"

    overall = None
    if isinstance(data, dict):
        mission = data.get("mission")
        if isinstance(mission, dict) and mission.get("overall"):
            overall = mission.get("overall")
        elif data.get("overall"):
            overall = data.get("overall")

    norm_overall = str(overall or "").strip().upper()
    if norm_overall in VERDICTS:
        mission_outcome = norm_overall
    else:
        mission_outcome = "NOT VERIFIED"

    if not valid and mission_outcome == "PASS":
        mission_outcome = "FAIL"

    payload = {
        "contract_validity": contract_validity,
        "mission_outcome": mission_outcome,
        "behavioral_status": "NOT VERIFIED",
        "enforcement_scope": "bundled_checker_enforced",
        "status": contract_validity,
        "contract_required": contract_required(data) if isinstance(data, dict) else True,
        "behavioral": "NOT VERIFIED",
        "issues": [{"code": item.code, "message": item.message, "path": item.path} for item in issues],
        "note": "A valid contract is not behavioral PASS and does not prove outcome truth.",
    }
    return payload


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--self-check":
        result = self_check()
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "PASS" else 1
    if argv and argv[0] == "--inspect":
        print(json.dumps(inspect_worktree(), indent=2))
        return 0
    json_out = False
    instruction_only = False
    mission_view: Path | None = None
    report: Path | None = None
    contract: Path | None = None
    rest: list[str] = []
    index = 0
    while index < len(argv):
        item = argv[index]
        if item == "--json":
            json_out = True
        elif item == "--instruction-only":
            instruction_only = True
        elif item == "--mission-view":
            if index + 1 >= len(argv) or argv[index + 1].startswith("-"):
                print("usage error: --mission-view requires a file argument", file=sys.stderr)
                return 2
            index += 1
            mission_view = Path(argv[index])
        elif item == "--write-report":
            if index + 1 >= len(argv) or argv[index + 1].startswith("-"):
                print("usage error: --write-report requires a file argument", file=sys.stderr)
                return 2
            index += 1
            report = Path(argv[index])
        elif item == "--render-mission-view":
            rest.append(item)
        elif not item.startswith("-"):
            contract = Path(item)
        else:
            print(f"unknown option: {item}", file=sys.stderr)
            return 2
        index += 1
    if instruction_only and contract is None:
        payload = {
            "check_status": "SKIPPED",
            "decision_source": "caller_asserted",
            "enforcement_scope": "instruction_only",
            "mission_outcome": "NOT VERIFIED",
            "behavioral_status": "NOT VERIFIED",
            "behavioral": "NOT VERIFIED",
            "contract_required": "caller_asserted",
            "contract_validity": "SKIPPED",
            "status": "SKIPPED",
            "issues": [],
            "note": "No mission contract supplied. Caller asserted instruction-only route without checker evaluation.",
        }
        print(json.dumps(payload, indent=2) if json_out else "instruction-only: SKIPPED (caller asserted)")
        return 0
    if contract is None:
        print(
            "usage: amc-check.py [--json] [--instruction-only] [--mission-view FILE] "
            "[--write-report FILE] CONTRACT.json",
            file=sys.stderr,
        )
        return 2
    try:
        data = json.loads(contract.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: cannot read contract: {error}", file=sys.stderr)
        return 1
    markdown = mission_view.read_text(encoding="utf-8") if mission_view else None
    if rest and "--render-mission-view" in rest:
        text = render_mission_view(data)
        if report:
            report.write_text(text, encoding="utf-8", newline="\n")
        else:
            print(text)
        return 0
    payload = check_contract(data, markdown)
    text = json.dumps(payload, indent=2) if json_out else (
        payload["contract_validity"] + "".join(f"\n{item['code']}: {item['message']}" for item in payload["issues"])
    )
    if report:
        report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(text)
    if payload["contract_validity"] != "VALID":
        return 1
    if payload["mission_outcome"] == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
