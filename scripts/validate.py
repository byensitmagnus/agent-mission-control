#!/usr/bin/env python3
"""Dependency-free repository validation."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> None:
    require(SKILL.is_file(), "SKILL.md is missing")
    require(README.is_file(), "README.md is missing")

    text = SKILL.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    require(len(parts) == 3 and not parts[0].strip(), "invalid YAML frontmatter")

    frontmatter = parts[1]
    name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", frontmatter, re.MULTILINE)
    description = re.search(r'^description:\s*"(.+)"\s*$', frontmatter, re.MULTILINE)
    require(name is not None, "name must use lowercase letters, numbers, and hyphens")
    require(name.group(1) == "agent-mission-control", "unexpected skill name")
    require(description is not None and len(description.group(1)) >= 40, "description is missing or too vague")

    combined = text + README.read_text(encoding="utf-8")
    require(not re.search(r"\b(TBD|TODO|FIXME)\b", combined), "unfinished placeholder found")
    require("$agent-mission-control" in combined, "README invocation example is missing")
    require((ROOT / "assets" / "mission-control.svg").is_file(), "banner is missing")

    print("PASS: skill, metadata, docs, and assets are valid")


if __name__ == "__main__":
    main()
