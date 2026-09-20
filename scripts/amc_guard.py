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
SENSITIVE_RECEIPT_KEYS = {"prompt", "transcript", "source_code", "file_contents", "secrets", "contents"}
JOB_KEYS = {
    "id", "depends_on", "parallel", "write_scope", "read_scope", "capability",
    "accept_check", "attempts", "return", "lifecycle", "verdict", "required",
    "independent", "isolation", "role", "delegation_authority", "parent_job",
    "observed_child_jobs", "delegation_ceiling", "permitted_actions",
    "required_artifact",
}
PLAN_KEYS = {
    "schema_version", "task_id", "objective", "non_goals", "authority",
    "prohibited_actions", "base_artifact", "candidate_artifact", "dirty",
    "planned_route", "observed_route", "route_reason", "break_even",
    "break_even_evidence", "host_capabilities", "host_capability_confidence",
    "jobs", "gates", "blockers", "reviewer_requirement", "reviewer_independence",
    "budget", "timestamps", "overall", "limitations", "simple_sequential",
    "work_kind", "host_isolation", "isolation_evidence", "isolation_workspace",
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


def validate(plan: Any) -> list[Issue]:
    if not isinstance(plan, dict):
        return [Issue("MALFORMED_INPUT", "malformed contract: plan must be an object")]
    issues: list[Issue] = []
    extra = set(plan) - PLAN_KEYS
    if extra:
        issues.append(Issue("UNSUPPORTED_KEY", f"unsupported keys {sorted(extra)}"))
    version = plan.get("schema_version")
    if version is not None and version not in {SCHEMA_VERSION, str(SCHEMA_VERSION)}:
        issues.append(Issue("UNSUPPORTED_KEY", f"unsupported schema_version {version}"))
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


def _jobs(plan: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    jobs = plan.get("jobs")
    if jobs is None:
        jobs = []
    if not isinstance(jobs, list):
        return [Issue("MALFORMED_INPUT", "malformed contract: jobs must be a list", "jobs")]
    if plan.get("simple_sequential") and jobs:
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
        if job.get("parallel") and depends:
            issues.append(Issue("DEPENDENT_PARALLEL", f"{job_id}: dependent jobs must not run in parallel", loc))
        missing = [name for name in depends if name not in seen and name not in {item.get("id") for item in jobs if isinstance(item, dict)}]
        # defer unknown deps until all ids collected
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

    missing_deps = []
    for job_id, job in by_id.items():
        depends = job.get("depends_on") or []
        if not isinstance(depends, list):
            continue
        absent = [name for name in depends if name not in by_id]
        if absent:
            missing_deps.append((job_id, absent))
            issues.append(Issue("UNKNOWN_DEPENDENCY", f"{job_id}: unknown dependency {absent}", job_id))
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
    if plan.get("lead_repeats_worker"):
        issues.append(Issue("LEAD_REPEATS_WORKER", "lead must not redo the worker job"))
    if plan.get("concurrency_as_goal"):
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
    if plan.get("trivial") and reviewers:
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
            if kind == "exact":
                scope = _normalize_scope(left)
                issues.append(Issue("WRITER_SCOPE_OVERLAP", f"shared write-scope {scope} owned by {left_id} and {right_id}"))
            else:
                issues.append(Issue("WRITER_SCOPE_OVERLAP", f"overlapping writer scopes {left} and {right} owned by {left_id} and {right_id}"))
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
        if job.get("parallel") and _scope_values(job.get("write_scope"))
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
    if _unknown(evidence) or str(evidence).strip().casefold() in WEAK_ISOLATION_EVIDENCE:
        return [Issue("CLAIMED_ISOLATION_WITHOUT_EVIDENCE", "claimed isolation without observed host evidence")]
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
        return bool(job.get("delegation_authority"))
    return _job_role(job) == "lead"


def contract_required(plan: dict[str, Any]) -> bool:
    """Trivial direct work does not need a mission file. Material routes and high-risk direct work do."""
    if not isinstance(plan, dict):
        return True
    risk_level = str(plan.get("risk_level") or "").strip().lower()
    false_pass_cost = str(plan.get("false_pass_cost") or "").strip().lower()
    high_risk_direct = (
        bool(plan.get("release_sensitive"))
        or risk_level in {"material", "critical"}
        or false_pass_cost in {"high", "critical"}
        or bool(plan.get("acceptance_logic_changed") or plan.get("acceptance_logic_changes"))
    )
    if high_risk_direct:
        return True
    if plan.get("trivial") and plan.get("simple_sequential"):
        return False
    if plan.get("trivial") and not high_risk_direct:
        return False
    planned = _norm_enum(plan.get("planned_route")) or "direct"
    if planned == "direct" and plan.get("simple_sequential"):
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
        if role in {"reviewer", "verifier"} and _scope_values(job.get("write_scope")):
            code = "REVIEWER_WRITE_FORBIDDEN" if role == "reviewer" else "VERIFIER_WRITE_FORBIDDEN"
            issues.append(Issue(code, f"{job_id}: {role} must be read-only", job_id))
        if role in {"reviewer", "verifier"} and job.get("delegation_authority") is True:
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
    return issues


def _route_receipt(receipt: Any, plan: dict[str, Any]) -> list[Issue]:
    if not isinstance(receipt, dict):
        return [Issue("MALFORMED_INPUT", "route_receipt must be an object")]
    issues: list[Issue] = []
    sensitive = SENSITIVE_RECEIPT_KEYS & set(receipt)
    if sensitive:
        issues.append(Issue("UNSUPPORTED_KEY", f"route_receipt forbids {sorted(sensitive)}"))
    planned = _norm_enum(receipt.get("planned_route") or plan.get("planned_route"))
    observed = _norm_enum(receipt.get("observed_route") or plan.get("observed_route"))
    if planned and planned not in ROUTES:
        issues.append(Issue("UNKNOWN_ROUTE", f"unknown planned route {planned}"))
    if observed and observed not in ROUTES:
        issues.append(Issue("UNKNOWN_ROUTE", f"unknown observed route {observed}"))
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
    if plan.get("acceptance_logic_changed") or (isinstance(mission, dict) and mission.get("acceptance_logic_changed")):
        independence = plan.get("reviewer_independence")
        independent = []
        if independence not in {False, "same-lead", "not-independent", "unknown"}:
            for job in jobs:
                if job.get("capability") != "material-reviewer":
                    continue
                flag = job.get("independent", independence)
                if flag not in {True, "independent"}:
                    continue
                if str(job.get("lifecycle") or "") != "completed":
                    continue
                if str(job.get("verdict") or "").upper() != "PASS":
                    continue
                independent.append(job)
        if overall == "PASS" and not independent:
            issues.append(Issue("PASS_WITHOUT_REVIEW", "overall PASS requires independent review after acceptance-logic change"))
    if overall != "PASS":
        return issues
    artifact_value = mission.get("artifact", plan.get("candidate_artifact"))
    artifact, artifact_obj = _artifact_identity(artifact_value)
    if not artifact or artifact.casefold() in PLACEHOLDER:
        issues.append(Issue("PASS_WITHOUT_ARTIFACT", "overall PASS requires a current artifact identity"))
    stale = mission.get("stale_pass_artifact")
    if stale and artifact and str(stale) != artifact:
        issues.append(Issue("PASS_STALE_EVIDENCE", "stale mission PASS cannot accept a new artifact"))
    method = artifact_obj.get("identity_method") if artifact_obj else None
    if artifact_obj:
        if method and method not in ARTIFACT_METHODS:
            issues.append(Issue("UNSUPPORTED_KEY", f"unknown artifact identity method {method}"))
        algorithm = artifact_obj.get("digest_algorithm")
        if algorithm and algorithm not in DIGEST_ALGORITHMS:
            issues.append(Issue("UNSUPPORTED_KEY", f"unknown digest algorithm {algorithm}"))
        evidence_digest = mission.get("evidence_digest") or (mission.get("evidence_artifact") or {}).get("digest")
        if evidence_digest and artifact_obj.get("digest") and str(evidence_digest) != str(artifact_obj.get("digest")):
            issues.append(Issue("PASS_STALE_EVIDENCE", "stale evidence cannot accept changed bytes"))
        if artifact_obj.get("dirty") and method in {"git-commit", "git-tree"}:
            issues.append(Issue("PASS_DIRTY_WITH_CLEAN_EVIDENCE", "dirty candidate accepted by clean-artifact evidence"))
    if mission.get("dirty") and mission.get("evidence_assumes_clean"):
        issues.append(Issue("PASS_DIRTY_WITH_CLEAN_EVIDENCE", "dirty candidate accepted by clean-artifact evidence"))
    schema1 = plan.get("schema_version") in {SCHEMA_VERSION, str(SCHEMA_VERSION)}
    required = list(mission.get("required_jobs") or [])
    if not required:
        required = [job for job in jobs if job.get("required") in {True, "yes"}]
    if not required:
        issues.append(Issue("PASS_WITH_INCOMPLETE_JOB", "overall PASS requires required jobs"))
    by_id = {job.get("id"): job for job in jobs if job.get("id")}
    for job in required:
        if not isinstance(job, dict):
            issues.append(Issue("MALFORMED_INPUT", "required job must be an object"))
            continue
        record = job
        if schema1:
            job_id = job.get("id")
            if not job_id or job_id not in by_id:
                issues.append(Issue("PASS_WITH_INCOMPLETE_JOB", "overall PASS rejected: required job is not bound to plan.jobs"))
                continue
            record = by_id[job_id]
        lifecycle = str(record.get("lifecycle") or "").lower()
        verdict = str(record.get("verdict") or "").upper()
        if lifecycle and lifecycle not in LIFECYCLES:
            issues.append(Issue("UNKNOWN_LIFECYCLE", f"unknown lifecycle {lifecycle}"))
        if lifecycle != "completed" or verdict != "PASS":
            issues.append(Issue("PASS_WITH_INCOMPLETE_JOB", "overall PASS rejected: required job unfinished or negative"))
    gates = list(mission.get("required_gates") or mission.get("gates") or plan.get("gates") or [])
    gates_declared = "required_gates" in mission or "gates" in mission or "gates" in plan
    if not gates_declared and schema1:
        issues.append(Issue("PASS_WITH_INCOMPLETE_GATE", "overall PASS requires required gates"))
    elif gates_declared:
        if not gates:
            issues.append(Issue("PASS_WITH_INCOMPLETE_GATE", "overall PASS requires required gates"))
        plan_gates = {
            gate.get("id"): gate
            for gate in (plan.get("gates") or [])
            if isinstance(gate, dict) and gate.get("id")
        }
        for gate in gates:
            if not isinstance(gate, dict):
                issues.append(Issue("MALFORMED_INPUT", "gate must be an object"))
                continue
            record = gate
            if schema1 and plan_gates:
                gate_id = gate.get("id")
                if not gate_id or gate_id not in plan_gates:
                    issues.append(Issue("PASS_WITH_INCOMPLETE_GATE", "overall PASS rejected: required gate is not bound to plan.gates"))
                    continue
                record = plan_gates[gate_id]
            status = str(record.get("status") or "").upper()
            if status not in GATE_STATUSES:
                issues.append(Issue("UNKNOWN_GATE_STATUS", f"unknown gate status {record.get('status')}"))
            if status != "PASS":
                issues.append(Issue("PASS_WITH_INCOMPLETE_GATE", "overall PASS rejected: required gate unfinished or negative"))
    blockers = mission.get("blockers", plan.get("blockers", None))
    if "blockers" in mission or "blockers" in plan:
        if blockers:
            issues.append(Issue("PASS_WITH_BLOCKER", "overall PASS with an active blocker"))
    elif schema1:
        issues.append(Issue("PASS_WITH_BLOCKER", "overall PASS requires explicit empty blockers"))
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
        "external_actions_not_performed",
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


def dirty_manifest_digest(root: Path, changed: list[str], dirty: bool) -> str:
    entries = []
    for path in changed:
        full = root / path
        if full.is_file():
            entries.append({"path": path, "sha256": hashlib.sha256(full.read_bytes()).hexdigest()})
        else:
            entries.append({"path": path, "sha256": None, "missing": True})
    payload = json.dumps({"changed": entries, "dirty": dirty}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def inspect_worktree(root: Path | None = None) -> dict[str, Any]:
    root = (root or Path.cwd()).resolve()
    def git(*args: str) -> str | None:
        try:
            result = subprocess.run(("git", "-C", str(root), *args), capture_output=True, text=True, check=False)
        except OSError:
            return None
        if result.returncode:
            return None
        return result.stdout.strip()
    commit = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    porcelain = git("status", "--porcelain=v1")
    dirty = bool(porcelain)
    changed = changed_paths(porcelain or "")
    digest = dirty_manifest_digest(root, changed, dirty) if dirty else (tree or "unknown")
    return {
        "schema_version": SCHEMA_VERSION,
        "type": "source-tree",
        "identity_method": "dirty-manifest" if dirty else "git-tree",
        "digest_algorithm": "sha256" if dirty else "sha1",
        "digest": digest,
        "base_commit": commit or "unknown",
        "git_tree": tree or "unknown",
        "dirty": dirty,
        "included_paths": changed if dirty else ["."],
        "excluded_paths": [".git"],
        "generation_command": "git rev-parse HEAD^{tree} && git status --porcelain=v1; sha256 changed files",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verification": "NOT VERIFIED",
        "note": "commit SHA is observational; do not embed it in a tracked self-hash",
    }


def seeded_adversary(seed: int = 20260918) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    cases: list[dict[str, Any]] = []
    count = rng.randint(2, 4)
    cases.append({
        "id": "gen-duplicate-ids",
        "jobs": [{"id": "dup", "depends_on": []} for _ in range(count)],
        "expect_codes": ["DUPLICATE_JOB_ID"],
    })
    length = rng.choice((2, 3, 4, 5))
    cases.append({
        "id": f"gen-cycle-{length}",
        "jobs": [{"id": f"n{index}", "depends_on": [f"n{(index + 1) % length}"]} for index in range(length)],
        "expect_codes": ["DEPENDENCY_CYCLE"],
    })
    pairs = (("src/a.py", "src/a.py"), ("src", "src/x.py"), ("./lib/x.py", "lib/x.py"), ("lib/*", "lib/x.py"))
    for index, (left, right) in enumerate(pairs):
        cases.append({
            "id": f"gen-scope-{index}",
            "break_even": True,
            "jobs": [
                {"id": "w1", "write_scope": left, "capability": "focused-general-worker", "accept_check": {"declared": True, "kind": "executable"}},
                {"id": "w2", "write_scope": right, "capability": "focused-general-worker", "accept_check": {"declared": True, "kind": "executable"}},
            ],
            "expect_codes": ["WRITER_SCOPE_OVERLAP"],
        })
    for state in ("ready", "complete", "done"):
        cases.append({
            "id": f"gen-lifecycle-{state}",
            "jobs": [{"id": "x", "lifecycle": state}],
            "expect_codes": ["UNKNOWN_LIFECYCLE"],
        })
    return cases


def _writer(job_id: str, scope: str, **extra: Any) -> dict[str, Any]:
    job = {
        "id": job_id,
        "write_scope": scope,
        "capability": "focused-general-worker",
        "accept_check": {"declared": True, "kind": "executable"},
        "return": "artifact",
    }
    job.update(extra)
    return job


def _pass_mission(**extra: Any) -> dict[str, Any]:
    mission = {
        "overall": "PASS",
        "artifact": "abcdef0123456789deadbeef",
        "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
        "required_gates": [{"id": "g1", "status": "PASS", "evidence": "check on abcdef0123456789deadbeef"}],
        "blockers": [],
    }
    mission.update(extra)
    return mission


TRUTH_CASES: list[dict[str, Any]] = [
    {"id": "01-missing-job-id", "jobs": [{"depends_on": []}], "expect_codes": ["MISSING_JOB_ID"]},
    {"id": "02-duplicate-job-ids", "jobs": [{"id": "a"}, {"id": "a"}], "expect_codes": ["DUPLICATE_JOB_ID"]},
    {"id": "03-unknown-dependency", "jobs": [{"id": "b", "depends_on": ["z"]}], "expect_codes": ["UNKNOWN_DEPENDENCY"]},
    {"id": "04-direct-cycle", "jobs": [{"id": "a", "depends_on": ["b"]}, {"id": "b", "depends_on": ["a"]}], "expect_codes": ["DEPENDENCY_CYCLE"]},
    {"id": "05-long-cycle", "jobs": [{"id": "a", "depends_on": ["b"]}, {"id": "b", "depends_on": ["c"]}, {"id": "c", "depends_on": ["a"]}], "expect_codes": ["DEPENDENCY_CYCLE"]},
    {"id": "06-exact-scope", "break_even": True, "jobs": [_writer("a", "app.py"), _writer("b", "app.py")], "expect_codes": ["WRITER_SCOPE_OVERLAP"]},
    {"id": "07-parent-child-scope", "break_even": True, "jobs": [_writer("a", "src"), _writer("b", "src/a.py")], "expect_codes": ["WRITER_SCOPE_OVERLAP"]},
    {"id": "08-normalized-scope", "break_even": True, "jobs": [_writer("a", "./src/a.py"), _writer("b", "src/a.py")], "expect_codes": ["WRITER_SCOPE_OVERLAP"]},
    {"id": "09-glob-scope", "break_even": True, "jobs": [_writer("a", "src/*"), _writer("b", "src/a.py")], "expect_codes": ["WRITER_SCOPE_OVERLAP"]},
    {
        "id": "10-writer-no-accept",
        "break_even": True,
        "work_kind": "code",
        "jobs": [{"id": "patch", "capability": "cheap-bounded-worker", "write_scope": "mod.py", "accept_check": {"declared": False}}],
        "expect_codes": ["WRITER_NO_ACCEPT_CHECK"],
    },
    {
        "id": "10b-code-write-non-executable",
        "break_even": True,
        "work_kind": "code",
        "jobs": [{"id": "patch", "capability": "cheap-bounded-worker", "write_scope": "mod.py", "accept_check": {"declared": True, "kind": "manual"}}],
        "expect_codes": ["CODE_WRITE_NO_EXECUTABLE_CHECK"],
    },
    {
        "id": "11-focused-no-accept",
        "break_even": True,
        "jobs": [{"id": "w", "capability": "focused-general-worker", "write_scope": "a.py", "accept_check": {"declared": False}}],
        "expect_codes": ["WRITER_NO_ACCEPT_CHECK"],
    },
    {
        "id": "11b-writer-no-capability",
        "jobs": [{"id": "w", "write_scope": "a.py"}],
        "expect_codes": ["UNKNOWN_CAPABILITY", "WRITER_NO_ACCEPT_CHECK", "DELEGATION_WITHOUT_BREAKEVEN"],
    },
    {
        "id": "12-missing-breakeven",
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_WITHOUT_BREAKEVEN"],
    },
    {
        "id": "13-failed-breakeven",
        "break_even": False,
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_WITHOUT_BREAKEVEN"],
    },
    {
        "id": "14-unknown-isolation",
        "break_even": True,
        "host_isolation": "maybe",
        "jobs": [_writer("a", "a.py", parallel=True), _writer("b", "b.py", parallel=True)],
        "expect_codes": ["UNKNOWN_ISOLATION"],
    },
    {
        "id": "15-claimed-isolation",
        "break_even": True,
        "host_isolation": "worktree",
        "jobs": [_writer("a", "a.py", parallel=True), _writer("b", "b.py", parallel=True)],
        "expect_codes": ["CLAIMED_ISOLATION_WITHOUT_EVIDENCE"],
    },
    {
        "id": "15b-weak-isolation-evidence",
        "break_even": True,
        "host_isolation": "worktree",
        "isolation_evidence": "claimed",
        "jobs": [_writer("a", "a.py", parallel=True), _writer("b", "b.py", parallel=True)],
        "expect_codes": ["CLAIMED_ISOLATION_WITHOUT_EVIDENCE"],
    },
    {
        "id": "15c-isolated-parallel-route",
        "break_even": True,
        "planned_route": "isolated_parallel",
        "jobs": [_writer("a", "a.py"), _writer("b", "b.py")],
        "expect_codes": ["PARALLEL_WITHOUT_ISOLATION", "DELEGATION_NOT_OBSERVED"],
    },
    {
        "id": "16-planned-no-child",
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "sequential_delegated",
        "observed_child_ids": [],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_NOT_OBSERVED"],
    },
    {
        "id": "16b-observed-delegated-no-child",
        "break_even": True,
        "planned_route": "direct",
        "observed_route": "sequential_delegated",
        "observed_child_ids": [],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_NOT_OBSERVED", "ROUTE_MISMATCH"],
    },
    {
        "id": "16c-bare-string-child",
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "sequential_delegated",
        "observed_child_ids": ["session-abc"],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": ["DELEGATION_NOT_OBSERVED"],
    },
    {
        "id": "16d-fallback-unlabeled",
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
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "sequential_delegated",
        "observed_child_ids": [{"id": "sess-1", "source": "host-reported"}],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker")],
        "expect_codes": [],
    },
    {
        "id": "17-unknown-lifecycle",
        "mission": _pass_mission(required_jobs=[{"lifecycle": "ready", "verdict": "PASS"}]),
        "expect_codes": ["UNKNOWN_LIFECYCLE", "PASS_WITH_INCOMPLETE_JOB"],
    },
    {
        "id": "18-pass-queued",
        "mission": _pass_mission(required_jobs=[{"lifecycle": "queued", "verdict": "NOT VERIFIED"}]),
        "expect_codes": ["PASS_WITH_INCOMPLETE_JOB"],
    },
    {
        "id": "18b-ghost-required-job",
        "schema_version": 1,
        "jobs": [{"id": "real", "lifecycle": "queued", "verdict": "NOT VERIFIED", "required": True}],
        "mission": _pass_mission(required_jobs=[{"id": "ghost", "lifecycle": "completed", "verdict": "PASS"}]),
        "expect_codes": ["PASS_WITH_INCOMPLETE_JOB"],
    },
    {
        "id": "19-pass-gate-unknown",
        "mission": _pass_mission(required_gates=[{"id": "g1", "status": "UNKNOWN"}]),
        "expect_codes": ["UNKNOWN_GATE_STATUS", "PASS_WITH_INCOMPLETE_GATE"],
    },
    {
        "id": "19b-pass-missing-gates",
        "schema_version": 1,
        "mission": {
            "overall": "PASS",
            "artifact": "abcdef0123456789deadbeef",
            "required_jobs": [{"id": "j1", "lifecycle": "completed", "verdict": "PASS"}],
            "blockers": [],
        },
        "expect_codes": ["PASS_WITH_INCOMPLETE_JOB", "PASS_WITH_INCOMPLETE_GATE"],
    },
    {
        "id": "20-pass-blocker",
        "mission": _pass_mission(blockers=["signing credential unavailable"]),
        "expect_codes": ["PASS_WITH_BLOCKER"],
    },
    {
        "id": "21-stale-artifact",
        "mission": _pass_mission(
            artifact={"type": "source-tree", "identity_method": "git-tree", "digest_algorithm": "sha1", "digest": "bbb", "dirty": False},
            evidence_digest="aaa",
        ),
        "expect_codes": ["PASS_STALE_EVIDENCE"],
    },
    {
        "id": "22-dirty-clean-evidence",
        "mission": _pass_mission(dirty=True, evidence_assumes_clean=True),
        "expect_codes": ["PASS_DIRTY_WITH_CLEAN_EVIDENCE"],
    },
    {
        "id": "22b-dirty-git-tree",
        "mission": _pass_mission(
            artifact={"type": "source-tree", "identity_method": "git-tree", "digest_algorithm": "sha1", "digest": "bbb", "dirty": True},
            evidence_assumes_clean=False,
        ),
        "expect_codes": ["PASS_DIRTY_WITH_CLEAN_EVIDENCE"],
    },
    {
        "id": "23-accept-change-no-review",
        "acceptance_logic_changed": True,
        "mission": _pass_mission(),
        "expect_codes": ["PASS_WITHOUT_REVIEW"],
    },
    {
        "id": "23b-queued-reviewer",
        "acceptance_logic_changed": True,
        "jobs": [{"id": "review", "capability": "material-reviewer", "independent": True, "lifecycle": "queued", "verdict": "NOT VERIFIED"}],
        "mission": _pass_mission(),
        "expect_codes": ["PASS_WITHOUT_REVIEW"],
    },
    {
        "id": "23c-same-lead-reviewer",
        "acceptance_logic_changed": True,
        "reviewer_independence": "same-lead",
        "jobs": [{"id": "review", "capability": "material-reviewer", "lifecycle": "completed", "verdict": "PASS"}],
        "mission": _pass_mission(),
        "expect_codes": ["PASS_WITHOUT_REVIEW"],
    },
    {
        "id": "25-optimizer-no-frozen",
        "planned_route": "measurable_optimizer",
        "optimization": {"tie": False, "keep": "incumbent"},
        "expect_codes": ["OPTIMIZER_NO_FROZEN_EVALUATOR"],
    },
    {
        "id": "26-optimizer-tie",
        "optimization": {"evaluator_frozen": True, "tie": True, "keep": "candidate"},
        "expect_codes": ["OPTIMIZER_TIE_REPLACES_INCUMBENT"],
    },
    {
        "id": "27-evaluator-change",
        "optimization": {"evaluator_frozen": True, "evaluator_changed": True, "new_baseline": False},
        "expect_codes": ["EVALUATOR_CHANGE_NO_BASELINE"],
    },
    {
        "id": "28-ordinary-learning",
        "learning": {"ordinary_success": True, "started_sleep": True, "auto_adopted": True},
        "expect_codes": ["ORDINARY_SUCCESS_STARTED_LEARNING"],
    },
    {
        "id": "29-transcript",
        "break_even": True,
        "jobs": [_writer("w", "a.py", **{"return": "transcript"})],
        "expect_codes": ["TRANSCRIPT_HANDOFF"],
    },
    {
        "id": "30-budget-overflow",
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
        "break_even": True,
        "jobs": [_writer("a", "../secret")],
        "expect_codes": ["UNSAFE_PATH"],
    },
    {
        "id": "honest-fallback",
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
        "break_even": True,
        "host_isolation": "worktree",
        "isolation_evidence": "git worktree list: /tmp/wt-a /tmp/wt-b",
        "isolation_workspace": "worktree",
        "jobs": [_writer("a", "a.py", parallel=True), _writer("b", "b.py", parallel=True)],
        "expect_codes": [],
    },
    {
        "id": "status-behavioral-from-eng",
        "product_status": {"engineering": "PASS", "behavioral": "PASS", "release": "NO-GO"},
        "expect_codes": ["BEHAVIORAL_FROM_ENGINEERING"],
    },
    {
        "id": "role-worker-nested",
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "sequential_delegated",
        "observed_child_ids": [{"id": "child-1", "source": "host-reported"}],
        "jobs": [
            _writer("w", "a.py", capability="cheap-bounded-worker", role="worker", observed_child_jobs=["nested"]),
            {"id": "nested", "parent_job": "w", "capability": "cheap-bounded-worker", "write_scope": "b.py", "accept_check": {"declared": True, "kind": "executable"}, "return": "artifact"},
        ],
        "expect_codes": ["UNAUTHORIZED_NESTED_DELEGATION"],
    },
    {
        "id": "role-reviewer-write",
        "jobs": [{"id": "r", "role": "reviewer", "capability": "material-reviewer", "write_scope": "src/fix.py"}],
        "expect_codes": ["REVIEWER_WRITE_FORBIDDEN"],
    },
    {
        "id": "role-worker-default-ok",
        "break_even": True,
        "planned_route": "sequential_delegated",
        "observed_route": "sequential_delegated",
        "observed_child_ids": [{"id": "sess-1", "source": "host-reported"}],
        "jobs": [_writer("w", "a.py", capability="cheap-bounded-worker", role="worker", delegation_authority=False)],
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
    missing, extra = _exact(["DUPLICATE_JOB_ID", "DEPENDENCY_CYCLE"], ["DUPLICATE_JOB_ID"])
    if extra != ["DEPENDENCY_CYCLE"] or missing:
        failures.append({"id": "24-unexpected-extra-harness", "missing": missing, "extra": extra})
    cases = list(TRUTH_CASES) + seeded_adversary()
    for case in cases:
        expected = list(case["expect_codes"])
        found = _codes({key: value for key, value in case.items() if key not in {"id", "expect_codes"}})
        miss, extra_codes = _exact(found, expected)
        if miss or extra_codes:
            failures.append({"id": case["id"], "missing": miss, "extra": extra_codes, "found": found})
    malformed = validate("not-an-object")
    if [item.code for item in malformed] != ["MALFORMED_INPUT"]:
        failures.append({"id": "malformed-root", "found": [item.code for item in malformed]})
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
    payload = {
        "status": "PASS" if not issues else "FAIL",
        "issues": [{"code": item.code, "message": item.message, "path": item.path} for item in issues],
        "contract_required": contract_required(data) if isinstance(data, dict) else True,
        "enforcement_scope": "bundled_checker_enforced",
        "behavioral": "NOT VERIFIED",
        "note": "A passing check is not behavioral PASS.",
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
            index += 1
            mission_view = Path(argv[index])
        elif item == "--write-report":
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
            "status": "PASS",
            "issues": [],
            "contract_required": False,
            "enforcement_scope": "instruction_only",
            "behavioral": "NOT VERIFIED",
            "note": "No mission file. Trivial direct path is instruction-only.",
        }
        print(json.dumps(payload, indent=2) if json_out else "instruction-only: no contract required")
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
        payload["status"] + "".join(f"\n{item['code']}: {item['message']}" for item in payload["issues"])
    )
    if report:
        report.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(text)
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
