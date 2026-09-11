#!/usr/bin/env python3
"""Standard-library structural validation for the skill package."""
from __future__ import annotations
import argparse, json, re, sys, tomllib
from pathlib import Path, PurePosixPath
import xml.etree.ElementTree as ET
from prepare_eval import fixture_paths

NAME = "agent-mission-control"
CONTEXT = ("Objective", "Reason for delegation", "Base commit or snapshot", "Owned scope", "Relevant paths, symbols and inputs", "Dependencies already satisfied", "Constraints and invariants", "Authorized actions", "Required deliverable", "Acceptance check")
EVIDENCE = ("Verdict", "Claims", "Files and symbols inspected or changed", "Commands run and observed results", "Acceptance-check result", "Risks and uncertainties", "Blocking decision, if any")
MISSION = ("Goal / Definition of Done", "Base and candidate", "Hard gates", "Authority", "Jobs", "Decisions and evidence", "Blockers", "Next action", "Last verified")
AGENT_KEYS = {"name", "description", "developer_instructions", "model", "model_reasoning_effort", "sandbox_mode"}
STATUSES = {"PASS", "FAIL", "BLOCKED", "NOT VERIFIED"}
MODELS = {"gpt-6-astra", "gpt-5.6-luna", "gpt-5.6-sol", "gpt-5.6-terra"}

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
    path = ((base or root) / Path(*relative(value, label).parts)).resolve()
    need(path == root or root in path.parents, f"{label}: path escapes package: {value}")
    return path

def resolve_link(root: Path, value: str, source: Path) -> Path:
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
    need(f"${NAME}" in values["default_prompt"], "agents/openai.yaml: default_prompt must name $agent-mission-control")

def load_toml(path: Path) -> dict:
    try: return tomllib.loads(read(path))
    except tomllib.TOMLDecodeError as exc: raise ValueError(f"{path}: invalid or duplicate TOML key: {exc}") from exc

def validate_codex(root: Path) -> None:
    directory = root / "examples/codex/.codex/agents"
    files = sorted(directory.glob("*.toml")) if directory.is_dir() else []
    expected_roles = {"mission_researcher", "mission_reviewer", "mission_verifier", "mission_worker"}
    need({path.stem for path in files} == expected_roles, f"custom agent examples must be exactly {sorted(expected_roles)}")
    names = set()
    expected_modes = {"mission_researcher": "read-only", "mission_reviewer": "read-only", "mission_verifier": "read-only", "mission_worker": "workspace-write"}
    for path in files:
        data = load_toml(path)
        need(set(data) == AGENT_KEYS, f"{path}: expected exactly {sorted(AGENT_KEYS)}")
        need(all(isinstance(data[k], str) and data[k].strip() for k in AGENT_KEYS), f"{path}: fields must be non-empty strings")
        need(data["name"] not in names, f"{path}: duplicate agent name {data['name']}"); names.add(data["name"])
        need(data["name"] == path.stem and data["name"] in expected_modes, f"{path}: unsupported role name")
        need(data["model"] in MODELS, f"{path}: unsupported model")
        need(data["model_reasoning_effort"] in {"low", "medium", "high", "xhigh"}, f"{path}: bad reasoning effort")
        need(data["sandbox_mode"] == expected_modes[data["name"]], f"{path}: unsafe sandbox mode for role")
    path = root / "examples/codex/.codex/config.toml"
    data = load_toml(path); agents = data.get("agents")
    need(set(data) == {"model", "model_reasoning_effort", "agents"}, f"{path}: unsupported top-level key")
    need(data["model"] == "gpt-6-astra" and data["model_reasoning_effort"] in {"low", "medium", "high", "xhigh"}, f"{path}: root model must be gpt-6-astra with supported reasoning")
    need(isinstance(agents, dict) and set(agents) == {"enabled", "max_concurrent_threads_per_session"}, f"{path}: unsupported [agents] key")
    need(isinstance(data.get("model"), str) and data["model"].strip(), f"{path}: root model required")
    need(isinstance(agents, dict) and agents.get("enabled") is True and agents.get("max_concurrent_threads_per_session") == 3, f"{path}: [agents] must enable 3 concurrent threads")

def validate_links(root: Path) -> None:
    patterns = (re.compile(r"!?\[[^\]]*\]\(([^)]+)\)"), re.compile(r"<(?:img|source)\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.I))
    for path in sorted(root.rglob("*.md")):
        text = read(path)
        for pattern in patterns:
            for raw in pattern.findall(text):
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

def validate_mission(root: Path) -> None:
    path = root / "templates/mission-view.md"; text = read(path)
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
    job_lines = [line for line in sections["Jobs"].splitlines() if line.strip().startswith("|")]
    need(len(job_lines) >= 3, f"{path}: Jobs table needs header and a job")
    headers = [cell.strip() for cell in job_lines[0].strip().strip("|").split("|")]
    required_columns = {"Job", "Agent", "Status", "Owned scope"}
    need(required_columns <= set(headers), f"{path}: Jobs missing required columns")
    indices = {name: headers.index(name) for name in required_columns}
    lifecycle = STATUSES | {"queued", "running", "completed"}
    for row in job_lines[2:]:
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        need(len(cells) == len(headers), f"{path}: malformed Jobs row")
        need(cells[indices["Status"]] in lifecycle, f"{path}: invalid job lifecycle status")
        need(bool(cells[indices["Job"]]) and bool(cells[indices["Agent"]]) and bool(cells[indices["Owned scope"]]), f"{path}: Jobs row needs job, agent, and owned scope")
    if status.group(1) == "PASS":
        need(all(item == "PASS" for item in gate_statuses), f"{path}: overall PASS requires every hard gate PASS")
        need(re.fullmatch(r"(?is)(?:none|none[.;].*)", sections["Blockers"]) is not None, f"{path}: overall PASS requires no blockers")
        need(sections["Decisions and evidence"].lower() not in {"none", "not verified"}, f"{path}: overall PASS requires evidence")
    if status.group(1) == "BLOCKED":
        need(not re.match(r"(?is)^none\b", sections["Blockers"]), f"{path}: overall BLOCKED requires a concrete blocker")

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

def validate_plugin(root: Path) -> None:
    path = root / ".codex-plugin/plugin.json"
    if not path.exists(): return
    try: data = json.loads(read(path))
    except json.JSONDecodeError as exc: raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    need(isinstance(data, dict), f"{path}: root must be object")
    for key in ("name", "version", "description"): need(isinstance(data.get(key), str) and data[key].strip(), f"{path}: {key} required")
    for key, value in data.items():
        if key.endswith(("path", "_path")): need(isinstance(value, str) and resolve(root, value, f"{path} {key}").exists(), f"{path}: invalid {key}")

def validate(root: Path) -> None:
    root = root.resolve(); need(root.is_dir(), f"bad root: {root}")
    validate_skill(root); validate_openai(root); validate_codex(root); validate_links(root); validate_svgs(root); validate_packets(root); validate_mission(root); validate_evals(root); validate_plugin(root)
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".toml", ".yaml", ".yml", ".svg", ".json"} and ".git" not in path.parts:
            need(re.search(r"\b(?:TBD|TODO|FIXME)\b", read(path)) is None, f"{path}: unfinished placeholder")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1]); args = parser.parse_args(argv)
    try: validate(args.root)
    except (OSError, ValueError) as exc: print(f"FAIL: {exc}", file=sys.stderr); return 1
    print("PASS: package structural contracts are valid"); return 0

if __name__ == "__main__": raise SystemExit(main())
