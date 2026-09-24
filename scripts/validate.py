#!/usr/bin/env python3
"""Standard-library structural validation for the skill package.

A passing run proves packaging and Markdown schema contracts. It cannot prove
that natural-language evidence is true, that an agent followed AMC, or that the
named artifact equals git HEAD.
"""
from __future__ import annotations
import argparse, json, re, sys, tomllib
from pathlib import Path, PurePosixPath
import xml.etree.ElementTree as ET
from prepare_eval import fixture_paths

NAME = "agent-mission-control"
CONTEXT = ("Objective", "Reason for delegation", "Base commit or snapshot", "Writable owned scope", "Read inputs, paths and symbols", "Dependencies already satisfied", "Constraints and invariants", "Authorized actions", "Required deliverable", "Acceptance check")
EVIDENCE = ("Verdict", "Artifact identity checked", "Claims", "Files and symbols inspected or changed", "Commands run and observed results", "Acceptance-check result", "Risks and uncertainties", "Blocking decision, if any")
MISSION = ("Goal / Definition of Done", "Base and candidate", "Hard gates", "Authority", "Jobs", "Decisions and evidence", "Blockers", "Next action", "Last verified")
AGENT_KEYS = {"name", "description", "developer_instructions", "model", "model_reasoning_effort", "sandbox_mode"}
STATUSES = {"PASS", "FAIL", "BLOCKED", "NOT VERIFIED"}
JOB_LIFECYCLE = {"queued", "running", "completed", "superseded"}
JOB_REQUIRED = {"yes", "no"}
JOB_COLUMNS = ["Job", "Agent", "Required", "Lifecycle", "Verdict", "Writable owned scope"]
LEGACY_JOB_COLUMNS = ["Job", "Agent", "Required", "Lifecycle", "Verdict", "Owned scope"]
PLACEHOLDERS = re.compile(r"Named (?:owned|writable) paths|Copy and fill|Copying this template makes no live claims|State the objective|State the bounded job|Fill the objective", re.I)
UNVERIFIED_EVIDENCE = re.compile(
    r"(?is)\b(?:none|n/?a|unknown|unverified|not(?:[ -]| yet )?verified|"
    r"no executed|not executed|not run|no (?:completed )?subject runs?|"
    r"zero subject runs|no completed subject)\b"
)
PASS_UNFINISHED_TEXT = re.compile(
    r"(?is)\b(?:still queued|still running|unfinished work|work remains queued|"
    r"remains queued|optional queued|dummy required|not executed)\b"
)
EFFORTS = {"low", "medium", "high", "xhigh"}
SANDBOXES = {"read-only", "workspace-write"}
READ_ONLY_HINTS = ("researcher", "reviewer", "verifier")
MODEL_REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:+/-]{0,127}$")
TEMPLATE_FICTION = re.compile(r"\b(?:transport\.py|retry\.py|should_send)\b", re.I)
PLUGIN_PUSH = re.compile(r"coordinated agents?|multi-agent software missions", re.I)
PLUGIN_SMALLEST = re.compile(r"smallest useful (?:workflow|execution graph)", re.I)
PLUGIN_EVIDENCE = re.compile(r"verified (?:evidence|completion)", re.I)
MISSING_VALUE = re.compile(r"(?is)(?:none|not[ -]?verified|n/?a|unknown|-)\.?\s*")

def need(ok: bool, message: str) -> None:
    if not ok: raise ValueError(message)

def read(path: Path) -> str:
    need(path.is_file(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")

def relative(value: str, label: str) -> PurePosixPath:
    need("\\" not in value and ":" not in value, f"{label}: unsafe relative path: {value}")
    path = PurePosixPath(value)
    need(bool(value) and not path.is_absolute() and ".." not in path.parts and ".git" not in path.parts, f"{label}: unsafe relative path: {value}")
    return path

def resolve(root: Path, value: str, label: str, base: Path | None = None) -> Path:
    root = root.resolve()
    path = ((base or root) / Path(*relative(value, label).parts)).resolve()
    need(path == root or root in path.parents, f"{label}: path escapes package: {value}")
    return path

def resolve_link(root: Path, value: str, source: Path) -> Path:
    root = root.resolve()
    need(not Path(value).is_absolute(), f"link in {source}: absolute local path")
    path = (source.parent / value).resolve()
    need(path == root or root in path.parents, f"link in {source}: path escapes package: {value}")
    return path

def quoted_yaml(text: str, allowed: set[str], label: str) -> dict[str, str]:
    out = {}
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"): continue
        match = re.fullmatch(r'([a-z_]+):\s*"([^"\r\n]*)"', line)
        need(match is not None, f'{label}:{number}: expected key: "value"')
        key, value = match.groups()
        need(key in allowed, f"{label}:{number}: unknown key {key}")
        need(key not in out, f"{label}:{number}: duplicate key {key}")
        out[key] = value
    return out

def validate_skill(root: Path) -> None:
    parts = read(root / "SKILL.md").split("---", 2)
    need(len(parts) == 3 and not parts[0].strip(), "SKILL.md: invalid frontmatter")
    entries = [line for line in parts[1].splitlines() if line.strip()]
    need(len(entries) == 2, "SKILL.md: frontmatter must contain exactly name and description")
    name = re.fullmatch(r"name:\s*([a-z0-9-]+)\s*", entries[0])
    description = re.fullmatch(r'description:\s*"([^"\r\n]*)"\s*', entries[1])
    need(name is not None and name.group(1) == NAME, f"SKILL.md: name must be {NAME}")
    need(description is not None and 40 <= len(description.group(1)) <= 240, "SKILL.md: quoted description must be 40..240 characters")

def validate_openai(root: Path) -> None:
    lines = [(n, x) for n, x in enumerate(read(root / "agents/openai.yaml").splitlines(), 1) if x.strip() and not x.lstrip().startswith("#")]
    need(lines and lines[0][1] == "interface:", "agents/openai.yaml: only top-level interface allowed")
    body = []
    for number, line in lines[1:]:
        need(line.startswith("  ") and not line.startswith("   "), f"agents/openai.yaml:{number}: use two-space indentation")
        body.append(line[2:])
    keys = {"display_name", "short_description", "icon_small", "icon_large", "brand_color", "default_prompt"}
    values = quoted_yaml("\n".join(body), keys, "agents/openai.yaml")
    need(set(values) == keys, f"agents/openai.yaml: expected exactly {sorted(keys)}")
    need(bool(values["display_name"].strip()), "agents/openai.yaml: display_name required")
    need(25 <= len(values["short_description"]) <= 64, "agents/openai.yaml: short_description must be 25..64 characters")
    need(re.fullmatch(r"#[0-9a-fA-F]{6}", values["brand_color"]) is not None, "agents/openai.yaml: brand_color must be #RRGGBB")
    for key in ("icon_small", "icon_large"):
        need(resolve(root, values[key].removeprefix("./"), key).is_file(), f"agents/openai.yaml: missing {key}")
    prompt = values["default_prompt"]
    need(f"${NAME}" in prompt, "agents/openai.yaml: default_prompt must name $agent-mission-control")
    need(PLUGIN_PUSH.search(prompt) is None, "agents/openai.yaml: default_prompt must not push multi-agent defaults")
    need(PLUGIN_SMALLEST.search(prompt) is not None and PLUGIN_EVIDENCE.search(prompt) is not None, "agents/openai.yaml: default_prompt must describe the smallest useful workflow and verified evidence")

def load_toml(path: Path) -> dict:
    try: return tomllib.loads(read(path))
    except tomllib.TOMLDecodeError as exc: raise ValueError(f"{path}: invalid or duplicate TOML key: {exc}") from exc

def require_model(value: object, label: str) -> None:
    need(isinstance(value, str) and bool(value.strip()), f"{label}: model reference required")
    need(MODEL_REF.fullmatch(value.strip()) is not None, f"{label}: invalid model reference")

def sandbox_for(name: str) -> set[str]:
    lowered = name.lower()
    if any(hint in lowered for hint in READ_ONLY_HINTS):
        return {"read-only"}
    return SANDBOXES

def validate_codex(root: Path) -> None:
    directory = root / "examples/codex/.codex/agents"
    config = root / "examples/codex/.codex/config.toml"
    if not directory.is_dir() and not config.is_file():
        return
    files = sorted(directory.glob("*.toml")) if directory.is_dir() else []
    names = set()
    for path in files:
        data = load_toml(path)
        need(set(data) == AGENT_KEYS, f"{path}: expected exactly {sorted(AGENT_KEYS)}")
        need(all(isinstance(data[k], str) and data[k].strip() for k in AGENT_KEYS), f"{path}: fields must be non-empty strings")
        need(data["name"] not in names, f"{path}: duplicate agent name {data['name']}"); names.add(data["name"])
        need(data["name"] == path.stem, f"{path}: name must match filename")
        require_model(data["model"], f"{path} model")
        need(data["model_reasoning_effort"] in EFFORTS, f"{path}: bad reasoning effort")
        need(data["sandbox_mode"] in SANDBOXES, f"{path}: unknown sandbox mode")
        allowed = sandbox_for(data["name"])
        need(data["sandbox_mode"] in allowed, f"{path}: unsafe sandbox mode for role")
    if not config.is_file():
        return
    data = load_toml(config); agents = data.get("agents")
    need(set(data) == {"model", "model_reasoning_effort", "agents"}, f"{config}: unsupported top-level key")
    require_model(data["model"], f"{config} root model")
    need(data["model_reasoning_effort"] in EFFORTS, f"{config}: root model must be supported with supported reasoning")
    need(isinstance(agents, dict) and set(agents) == {"enabled", "max_concurrent_threads_per_session", "default_subagent_model", "default_subagent_reasoning_effort"}, f"{config}: unsupported [agents] key")
    need(isinstance(agents.get("enabled"), bool), f"{config}: [agents].enabled must be boolean")
    threads = agents.get("max_concurrent_threads_per_session")
    need(isinstance(threads, int) and 1 <= threads <= 32, f"{config}: max_concurrent_threads_per_session must be 1..32")
    require_model(agents["default_subagent_model"], f"{config} default subagent model")
    need(agents["default_subagent_reasoning_effort"] in EFFORTS, f"{config}: bad default subagent reasoning effort")

def srcset_urls(value: str):
    while value.strip(" ,"):
        value = value.lstrip(" ,")
        parts = value.split(maxsplit=1)
        url, rest = parts[0], parts[1] if len(parts) > 1 else ""
        yield url.rstrip(",")
        # A trailing comma ends a URL; otherwise skip its optional descriptors.
        # Commas inside a data URL stay part of that URL.
        value = rest if url.endswith(",") else rest.partition(",")[2]


def validate_links(root: Path) -> None:
    patterns = (re.compile(r"!?\[[^\]]*\]\(([^)]+)\)"), re.compile(r"<(?:img|source)\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.I))
    for path in sorted(root.rglob("*.md")):
        text = read(path)
        links = [raw for pattern in patterns for raw in pattern.findall(text)]
        for value in re.findall(r"<(?:img|source)\b[^>]*\bsrcset=[\"']([^\"']+)[\"']", text, re.I):
            links.extend(srcset_urls(value))
        for raw in links:
            value = raw.strip().strip("<>").split(maxsplit=1)[0]
            if not value or value.startswith("#") or re.match(r"^(?:https?:|mailto:|data:)", value, re.I): continue
            target = value.split("#", 1)[0].split("?", 1)[0]
            need(resolve_link(root, target, path).exists(), f"{path}: broken local link {raw}")

def validate_svgs(root: Path) -> None:
    files = sorted(root.rglob("*.svg")); need(bool(files), "no SVG assets found")
    for path in files:
        try: tree = ET.parse(path)
        except ET.ParseError as exc: raise ValueError(f"{path}: malformed SVG: {exc}") from exc
        root_node = tree.getroot()
        need(root_node.tag == "{http://www.w3.org/2000/svg}svg", f"{path}: root must use SVG namespace")
        child_names = {node.tag.rsplit("}", 1)[-1].lower() for node in root_node}
        need({"title", "desc"} <= child_names, f"{path}: title and desc required")
        for node in tree.iter():
            local_name = node.tag.rsplit("}", 1)[-1].lower()
            need(local_name not in {"script", "style", "foreignobject"}, f"{path}: unsafe SVG element {local_name}")
            for key, value in node.attrib.items():
                attribute = key.rsplit("}", 1)[-1].lower()
                need(not attribute.startswith("on"), f"{path}: SVG event handler forbidden")
                if attribute in {"href", "src"}: need(value.startswith("#"), f"{path}: external SVG resource")
                for url in re.findall(r"url\(([^)]+)\)", value, re.I): need(url.strip(" '\"").startswith("#"), f"{path}: external CSS resource")

def headings(text: str) -> list[str]: return re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.M)
def labels(text: str) -> tuple[str, ...]: return tuple(x.strip() for x in re.findall(r"^([^\n:#]+):(?:[ \t].*)?$", text, re.M))

def validate_packets(root: Path) -> None:
    for name, expected, filename in (("Context Packet", CONTEXT, "context-packet.md"), ("Evidence Packet", EVIDENCE, "evidence-packet.md")):
        path = root / "templates" / filename; text = read(path); present = labels(text)
        need(present == expected, f"{path}: fields must be exactly {expected}")
        for field in expected:
            body = re.search(rf"^{re.escape(field)}:[ \t]*(\S.*)$", text, re.M)
            need(body is not None and body.group(1).strip(), f"{path}: {field} needs content")
        if name == "Evidence Packet":
            verdict = re.search(r"^Verdict:\s*(.+?)\s*$", text, re.M)
            need(verdict is not None and verdict.group(1) in STATUSES, f"{path}: invalid Verdict")

def validate_blank_templates(root: Path) -> None:
    directory = root / "templates"
    need(directory.is_dir(), "missing templates directory")
    for path in sorted(directory.glob("*.md")):
        text = read(path)
        need(TEMPLATE_FICTION.search(text) is None, f"{path}: blank templates must not contain case fiction")
        need("populated" not in text.lower(), f"{path}: blank templates must not look like populated demonstrations")

def parse_jobs(section: str, path: Path, allow_legacy_scope: bool = False) -> list[dict[str, str]]:
    job_lines = [line for line in section.splitlines() if line.strip().startswith("|")]
    need(len(job_lines) >= 3, f"{path}: Jobs table needs header and a job")
    headers = [cell.strip() for cell in job_lines[0].strip().strip("|").split("|")]
    allowed_headers = [JOB_COLUMNS]
    if allow_legacy_scope:
        allowed_headers.append(LEGACY_JOB_COLUMNS)
    need(headers in allowed_headers, f"{path}: Jobs header must be {' | '.join(JOB_COLUMNS)}")
    scope_column = "Writable owned scope" if headers == JOB_COLUMNS else "Owned scope"
    jobs = []
    for row in job_lines[2:]:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        need(len(cells) == len(headers), f"{path}: malformed Jobs row")
        job = dict(zip(headers, cells))
        need(job["Job"] and job["Agent"] and job[scope_column], f"{path}: Jobs row needs job, agent, and writable owned scope")
        need(job["Required"] in JOB_REQUIRED, f"{path}: invalid job required flag")
        need(job["Lifecycle"] in JOB_LIFECYCLE, f"{path}: invalid job lifecycle status")
        need(job["Verdict"] in STATUSES, f"{path}: invalid job verdict")
        if job["Lifecycle"] in {"queued", "running"}:
            need(job["Verdict"] == "NOT VERIFIED", f"{path}: unfinished jobs must have verdict NOT VERIFIED")
        if job["Lifecycle"] == "superseded":
            need(job["Required"] == "no", f"{path}: superseded jobs must be optional")
            need(job["Verdict"] == "NOT VERIFIED", f"{path}: superseded jobs must have verdict NOT VERIFIED")
            need(re.search(r"(?i)superseded:", job[scope_column]) is not None, f"{path}: superseded jobs need a superseded: reason")
        jobs.append(job)
    need(bool(jobs), f"{path}: Jobs table needs a job")
    need(any(job["Required"] == "yes" for job in jobs), f"{path}: at least one required job")
    return jobs

def check_mission(
    text: str,
    path: Path,
    instance: bool = False,
    allow_legacy_job_scope: bool = False,
) -> None:
    need(re.search(r"^schema_version:\s*1\s*$", text, re.M) is not None, f"{path}: schema_version must be 1")
    status = re.search(r"^overall:\s*(.+?)\s*$", text, re.M)
    need(status is not None and status.group(1) in STATUSES, f"{path}: invalid overall")
    present = headings(text); positions = [present.index(x) if x in present else -1 for x in MISSION]
    need(all(present.count(x) == 1 for x in MISSION), f"{path}: required headings must be unique")
    need(all(x >= 0 for x in positions) and positions == sorted(positions), f"{path}: missing or reordered headings")
    sections = {}
    for heading in MISSION:
        match = re.search(rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        need(match is not None and match.group(1).strip(), f"{path}: empty section {heading}")
        sections[heading] = match.group(1).strip()
    artifact = re.search(r"^Current artifact:\s*(\S.*)$", sections["Base and candidate"], re.M)
    need(artifact is not None and artifact.group(1).strip(), f"{path}: Current artifact identity required")
    hard_gates = re.search(r"^## Hard gates\s*$\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    need(hard_gates is not None, f"{path}: Hard gates table required")
    rows = [line for line in hard_gates.group(1).splitlines() if line.strip().startswith("|")][2:]
    gate_lines = [line for line in hard_gates.group(1).splitlines() if line.strip().startswith("|")]
    gate_headers = [cell.strip() for cell in gate_lines[0].strip().strip("|").split("|")] if gate_lines else []
    need(gate_headers == ["Gate", "Status", "Evidence"], f"{path}: Hard gates header must be Gate | Status | Evidence")
    need(bool(rows), f"{path}: at least one hard gate required")
    gate_statuses = []
    for row in rows:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        need(len(cells) >= 3 and cells[1] in STATUSES, f"{path}: invalid hard-gate status")
        need(bool(cells[0]) and bool(cells[2]), f"{path}: hard gates require name and evidence")
        gate_statuses.append(cells[1])
    jobs = parse_jobs(sections["Jobs"], path, allow_legacy_scope=allow_legacy_job_scope)
    ident = artifact.group(1).strip()
    if instance:
        need(PLACEHOLDERS.search(text) is None, f"{path}: unresolved template placeholders")
    if status.group(1) == "PASS":
        need(all(item == "PASS" for item in gate_statuses), f"{path}: overall PASS requires every hard gate PASS")
        need(
            len(ident) >= 16 and re.search(r"[A-Za-z]", ident) is not None and re.search(r"[0-9]", ident) is not None and re.match(r"\d{4}-\d{2}-\d{2}", ident) is None,
            f"{path}: overall PASS requires a current artifact identity",
        )
        need(MISSING_VALUE.fullmatch(ident) is None, f"{path}: overall PASS requires a current artifact identity")
        for row in rows:
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            need(UNVERIFIED_EVIDENCE.search(cells[2]) is None, f"{path}: overall PASS forbids missing hard-gate evidence")
        need(any(ident in [cell.strip() for cell in row.strip().strip("|").split("|")][2] for row in rows), f"{path}: overall PASS requires current artifact identity in hard-gate evidence")
        need(re.fullmatch(r"(?is)none\.?\s*", sections["Blockers"]) is not None, f"{path}: overall PASS requires no blockers")
        need(re.search(r"(?i)\bblocked\b", sections["Next action"]) is None, f"{path}: overall PASS forbids a blocker in Next action")
        evidence = sections["Decisions and evidence"]
        need(MISSING_VALUE.match(evidence.split("\n", 1)[0]) is None, f"{path}: overall PASS requires reopenable evidence")
        need(ident in evidence and ident in sections["Last verified"], f"{path}: overall PASS requires reopenable evidence")
        need(re.search(r"(?i)not[ -]?verified", sections["Last verified"]) is None, f"{path}: overall PASS requires current last-verified identity")
        for heading in ("Goal / Definition of Done", "Authority", "Decisions and evidence", "Next action"):
            need(PASS_UNFINISHED_TEXT.search(sections[heading]) is None, f"{path}: overall PASS forbids unfinished work in narrative fields")
        for job in jobs:
            need(job["Lifecycle"] not in {"queued", "running"}, f"{path}: overall PASS forbids unfinished jobs")
            if job["Required"] == "yes":
                need(job["Lifecycle"] == "completed" and job["Verdict"] == "PASS", f"{path}: overall PASS requires required jobs completed with PASS")
            if job["Lifecycle"] == "completed":
                need(job["Verdict"] == "PASS", f"{path}: overall PASS forbids completed jobs with a negative verdict")
    if status.group(1) == "BLOCKED":
        need(not re.match(r"(?is)^none\b", sections["Blockers"]), f"{path}: overall BLOCKED requires a concrete blocker")

def validate_mission(root: Path) -> None:
    path = root / "templates/mission-view.md"
    check_mission(read(path), path, instance=False)
    live = root / "MISSION.md"
    if live.is_file():
        check_mission(read(live), live, instance=True, allow_legacy_job_scope=True)
    demo = root / "examples/packets/mission-view.populated.md"
    if demo.is_file():
        check_mission(read(demo), demo, instance=True)

def validate_evals(root: Path) -> None:
    path = root / "evals/cases.json"
    try: data = json.loads(read(path))
    except json.JSONDecodeError as exc: raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    need(isinstance(data, dict) and set(data) == {"schema_version", "cases"} and data["schema_version"] == 2, f"{path}: invalid root schema")
    need(isinstance(data["cases"], list) and bool(data["cases"]), f"{path}: cases must be nonempty")
    required = {"id", "prompt", "expected_routing", "fixture", "checks", "activation"}; ids = set()
    for case in data["cases"]:
        need(isinstance(case, dict) and set(case) == required, f"{path}: bad case fields")
        need(all(isinstance(case[k], str) and case[k] for k in ("id", "prompt", "expected_routing")), f"{path}: empty case string")
        need(case["id"] not in ids, f"{path}: duplicate id {case['id']}"); ids.add(case["id"])
        need(isinstance(case["activation"], str) and case["activation"] in {"explicit", "description"}, f"{path}: invalid activation")
        fixture_paths(case["fixture"])
        need(isinstance(case["checks"], list) and case["checks"] and all(isinstance(x, str) and x for x in case["checks"]), f"{path}: checks required")
    rubric = read(root / "evals/rubric.md").lower(); need("behavioral" in rubric and "structural" in rubric, "evals/rubric.md: proof types missing")

def validate_plugin_copy(text: str, path: Path) -> None:
    blob = json.dumps(text) if not isinstance(text, str) else text
    need(PLUGIN_PUSH.search(blob) is None, f"{path}: plugin copy must not push multi-agent defaults")

def validate_plugin(root: Path) -> None:
    packager = root / "scripts/package_plugin.py"
    if packager.is_file():
        text = read(packager)
        validate_plugin_copy(text, packager)
        need(PLUGIN_SMALLEST.search(text) is not None and PLUGIN_EVIDENCE.search(text) is not None, f"{packager}: plugin copy must describe the smallest useful workflow and verified evidence")
    path = root / ".codex-plugin/plugin.json"
    if not path.exists(): return
    try: data = json.loads(read(path))
    except json.JSONDecodeError as exc: raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    need(isinstance(data, dict), f"{path}: root must be object")
    for key in ("name", "version", "description"): need(isinstance(data.get(key), str) and data[key].strip(), f"{path}: {key} required")
    validate_plugin_copy(json.dumps(data), path)
    interface = data.get("interface")
    if isinstance(interface, dict):
        prompts = interface.get("defaultPrompt")
        if isinstance(prompts, list):
            joined = " ".join(str(item) for item in prompts)
            need(PLUGIN_SMALLEST.search(joined) is not None, f"{path}: defaultPrompt must describe the smallest useful workflow")
    for key, value in data.items():
        if key.endswith(("path", "_path")): need(isinstance(value, str) and resolve(root, value, f"{path} {key}").exists(), f"{path}: invalid {key}")

def validate(root: Path) -> None:
    root = root.resolve(); need(root.is_dir(), f"bad root: {root}")
    validate_skill(root); validate_openai(root); validate_codex(root); validate_links(root); validate_svgs(root); validate_packets(root); validate_blank_templates(root); validate_mission(root); validate_evals(root); validate_plugin(root)
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".toml", ".yaml", ".yml", ".svg", ".json"} and ".git" not in path.parts:
            need(re.search(r"\b(?:TBD|TODO|FIXME)\b", read(path)) is None, f"{path}: unfinished placeholder")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1]); args = parser.parse_args(argv)
    try: validate(args.root)
    except (OSError, ValueError) as exc: print(f"FAIL: {exc}", file=sys.stderr); return 1
    print("PASS: package structural contracts are valid; this is not runtime or product PASS"); return 0

if __name__ == "__main__": raise SystemExit(main())
