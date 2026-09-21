#!/usr/bin/env python3
"""Render docs/claim-ledger.md from research/claims.json. No network."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "research" / "claims.json"
LEDGER = ROOT / "docs" / "claim-ledger.md"
REQUIRED_CLAIM = (
    "claim_id", "claim_type", "mechanism", "claim", "evidence_origin",
    "source_ids", "source_supported_fact", "architectural_inference",
    "does_not_prove", "adoption", "enforcement_scope", "outcome_status",
    "audited_date", "implementation",
)
REQUIRED_SOURCE = (
    "source_id", "author", "title", "source_type", "url", "retrieved_at",
)
ALLOWED_EVIDENCE_ORIGIN = {"primary_source", "reasoned_inference", "local_observation", "replicated_eval"}
ALLOWED_ENFORCEMENT_SCOPE = {"instruction_only", "bundled_checker_enforced", "host_enforced", "repository_ci_enforced"}
ALLOWED_OUTCOME_STATUS = {"observed", "not_verified", "verified"}
ALLOWED_ADOPTION = {"adopted", "adapted", "rejected_as_runtime", "rejected", "recorded"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load() -> dict:
    data = json.loads(CANONICAL.read_text(encoding="utf-8"))
    top_audited_date = str(data.get("audited_date") or "")
    if not DATE_RE.match(top_audited_date):
        raise ValueError(f"top-level audited_date must be YYYY-MM-DD: {top_audited_date!r}")

    claims = data.get("claims") or []
    sources = {item["source_id"]: item for item in data.get("sources") or []}
    if len(sources) != len(data.get("sources") or []):
        raise ValueError("duplicate source_id")
    ids = [item["claim_id"] for item in claims]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate claim_id")

    claim_map = {item["claim_id"]: item for item in claims}

    for source in sources.values():
        missing = [key for key in REQUIRED_SOURCE if key not in source]
        if missing:
            raise ValueError(f"{source.get('source_id')}: missing {missing}")
        if str(source.get("version") or "").strip().lower() == "latest":
            raise ValueError(f"{source['source_id']}: version must not be latest")
        retrieved_at = str(source.get("retrieved_at") or "")
        if not DATE_RE.match(retrieved_at):
            raise ValueError(f"{source['source_id']}: retrieved_at must be YYYY-MM-DD: {retrieved_at!r}")
        for supported_claim_id in source.get("supports") or []:
            if supported_claim_id not in claim_map:
                raise ValueError(f"{source['source_id']}: supports non-existent claim {supported_claim_id}")
            if source["source_id"] not in claim_map[supported_claim_id].get("source_ids", []):
                raise ValueError(
                    f"{source['source_id']} supports {supported_claim_id}, but claim does not list it in source_ids"
                )

    for item in claims:
        missing = [key for key in REQUIRED_CLAIM if key not in item]
        if missing:
            raise ValueError(f"{item.get('claim_id')}: missing {missing}")
        if item.get("evidence_origin") not in ALLOWED_EVIDENCE_ORIGIN:
            raise ValueError(f"{item['claim_id']}: invalid evidence_origin: {item.get('evidence_origin')}")
        if item.get("enforcement_scope") not in ALLOWED_ENFORCEMENT_SCOPE:
            raise ValueError(f"{item['claim_id']}: invalid enforcement_scope: {item.get('enforcement_scope')}")
        if item.get("outcome_status") not in ALLOWED_OUTCOME_STATUS:
            raise ValueError(f"{item['claim_id']}: invalid outcome_status: {item.get('outcome_status')}")
        if item.get("adoption") not in ALLOWED_ADOPTION:
            raise ValueError(f"{item['claim_id']}: invalid adoption: {item.get('adoption')}")

        claim_date = str(item.get("audited_date") or "")
        if not DATE_RE.match(claim_date):
            raise ValueError(f"{item['claim_id']}: audited_date must be YYYY-MM-DD: {claim_date!r}")
        if claim_date > top_audited_date:
            raise ValueError(f"{item['claim_id']}: audited_date {claim_date} exceeds top-level audited_date {top_audited_date}")

        for source_id in item["source_ids"]:
            if source_id not in sources:
                raise ValueError(f"{item['claim_id']}: unknown source {source_id}")
            if item["claim_id"] not in sources[source_id].get("supports", []):
                raise ValueError(
                    f"{item['claim_id']} cites {source_id}, but source supports back-reference does not list it"
                )

        impl = item.get("implementation") or ""
        for raw_path in [p.strip() for p in impl.split(",") if p.strip()]:
            file_path = raw_path.split()[0]
            if not (ROOT / file_path).exists():
                raise ValueError(f"{item['claim_id']}: implementation path does not exist: {file_path}")

        if "latest" in json.dumps(item).lower():
            raise ValueError(f"{item['claim_id']}: durable claims must not say latest")

    skillopt = [item["claim_id"] for item in claims if "SKILLOPT" in item["claim_id"]]
    harmful = [item["claim_id"] for item in claims if "HARMFUL" in item["claim_id"]]
    if not skillopt or not harmful:
        raise ValueError("SkillOpt and harmful-skills claims must both exist")
    skillopt_sources = set()
    harmful_sources = set()
    for item in claims:
        if item["claim_id"] in skillopt:
            skillopt_sources.update(item["source_ids"])
        if item["claim_id"] in harmful:
            harmful_sources.update(item["source_ids"])
    if skillopt_sources & harmful_sources:
        raise ValueError("SkillOpt and harmful-skills claims must use different sources")
    local = [item for item in sources.values() if item["source_id"] == "SUPERPOWERS-LOCAL"]
    upstream = [item for item in sources.values() if item["source_id"] == "SUPERPOWERS-641"]
    if not local or not upstream:
        raise ValueError("Superpowers local and upstream sources must both exist")
    if local[0].get("audited_ref") == upstream[0].get("audited_ref"):
        raise ValueError("Superpowers local and upstream refs must stay distinct")
    return data


def render(data: dict) -> str:
    lines = [
        "# Claim ledger",
        "",
        "Generated from [`research/claims.json`](../research/claims.json). "
        f"Do not edit this file by hand. Regenerated {data.get('generated_note', 'by scripts/render_claims.py')}.",
        "",
        "Three independent axes: evidence origin, enforcement scope, outcome status.",
        "A green checker is not behavioral PASS.",
        "",
        "## Sources",
        "",
        "| ID | Author | Title | Type | Audited ref | Retrieved |",
        "|---|---|---|---|---|---|",
    ]
    for source in data["sources"]:
        lines.append(
            "| {source_id} | {author} | {title} | {source_type} | {ref} | {retrieved_at} |".format(
                ref=source.get("audited_ref") or source.get("version") or source.get("commit") or "n/a",
                **source,
            )
        )
    lines.extend(["", "## Claims", ""])
    for item in data["claims"]:
        lines.extend([
            f"## {item['claim_id']} — {item['mechanism']}",
            "",
            f"- **claim_type:** {item['claim_type']}",
            f"- **claim:** {item['claim']}",
            f"- **evidence_origin:** {item['evidence_origin']}",
            f"- **source_ids:** {', '.join(item['source_ids'])}",
            f"- **source_supported_fact:** {item['source_supported_fact']}",
            f"- **architectural_inference:** {item['architectural_inference']}",
            f"- **does_not_prove:** {item['does_not_prove']}",
            f"- **adoption:** {item['adoption']}",
            f"- **enforcement_scope:** {item['enforcement_scope']}",
            f"- **outcome_status:** {item['outcome_status']}",
            f"- **implementation:** {item['implementation']}",
            f"- **audited_date:** {item['audited_date']}",
            f"- **superseded:** {item.get('superseded') or 'no'}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        data = load()
        text = render(data)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    if args.check:
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.is_file() else ""
        if current != text:
            print("FAIL: docs/claim-ledger.md is stale; run python scripts/render_claims.py", file=sys.stderr)
            return 1
        print("PASS: claim ledger matches research/claims.json")
        return 0
    LEDGER.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {LEDGER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
