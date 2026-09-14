#!/usr/bin/env python3
"""Offline documentation/skill shape checks, not security or runtime validation."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

EXCLUDED = {".git", ".venv", "node_modules", "__pycache__", ".next"}
FENCED = re.compile(r"^```[^\n]*\n.*?^```[ \t]*$", re.MULTILINE | re.DOTALL)
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def check_markdown(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    label = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{label}: cannot read UTF-8: {exc}"]
    if text and not text.endswith("\n"):
        errors.append(f"{label}: missing final newline")
    for number, line in enumerate(text.splitlines(), 1):
        if line.rstrip() != line:
            errors.append(f"{label}:{number}: trailing whitespace")
    for raw in LINK.findall(FENCED.sub("", text)):
        try:
            link = urlsplit(raw.strip("<>"))
        except ValueError:
            errors.append(f"{label}: malformed link {raw}")
            continue
        if link.scheme or link.netloc or not link.path:
            continue
        target = (path.parent / unquote(link.path)).resolve()
        if not target.is_relative_to(root.resolve()):
            errors.append(f"{label}: link outside repository: {raw}")
        elif not target.exists():
            errors.append(f"{label}: missing link target: {raw}")
    return errors


def check_skill(path: Path) -> list[str]:
    label = path.parent.name
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return [f"{label}: missing skill frontmatter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return [f"{label}: unclosed skill frontmatter"]
    fields: dict[str, str] = {}
    errors: list[str] = []
    for line in lines[1:end]:
        key, separator, value = line.partition(":")
        if not separator or key in fields:
            errors.append(f"{label}: invalid or duplicate frontmatter field")
            continue
        fields[key] = value.strip()
    name = fields.get("name", "")
    if not NAME.fullmatch(name) or len(name) > 64:
        errors.append(f"{label}: invalid skill name")
    if name != label:
        errors.append(f"{label}: skill name does not match directory")
    description = fields.get("description", "")
    if not description.startswith("Use when ") or len(description) > 1024:
        errors.append(f"{label}: description must be a bounded 'Use when' trigger")
    if not "\n".join(lines[end + 1 :]).strip():
        errors.append(f"{label}: empty skill body")
    return errors


def load_object(path: Path) -> tuple[dict, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {}, [f"{path.name}: invalid JSON or unreadable file: {exc}"]
    if not isinstance(data, dict):
        return {}, [f"{path.name}: JSON root must be an object"]
    if data.get("schema_version") != 1:
        return {}, [f"{path.name}: unsupported schema_version"]
    return data, []


def check_catalog(root: Path) -> list[str]:
    data, errors = load_object(root / ".agents/skills/catalog.json")
    if errors:
        return errors
    items = data.get("skills")
    if not isinstance(items, list):
        return ["catalog.json: skills must be a list"]
    names: set[str] = set()
    paths: set[str] = set()
    for entry in items:
        if not isinstance(entry, dict):
            errors.append("catalog.json: skill entry must be an object")
            continue
        name, path = entry.get("name"), entry.get("path")
        if not isinstance(name, str) or not isinstance(path, str):
            errors.append("catalog.json: name and path must be strings")
            continue
        if name in names or path in paths:
            errors.append(f"catalog.json: duplicate skill entry: {name}")
        names.add(name)
        paths.add(path)
        expected = f".agents/skills/{name}/SKILL.md"
        if not NAME.fullmatch(name) or path != expected:
            errors.append(f"catalog.json: invalid path/name: {name}")
        elif not (root / path).is_file():
            errors.append(f"catalog.json: missing skill file: {path}")
    actual = {p.relative_to(root).as_posix() for p in (root / ".agents/skills").glob("*/SKILL.md")}
    for path in sorted(actual - paths):
        errors.append(f"catalog.json: skill not in catalog: {path}")
    return errors


def check_scenarios(root: Path) -> list[str]:
    catalog, errors = load_object(root / ".agents/skills/catalog.json")
    data, scenario_errors = load_object(root / "tests/skills/scenarios.json")
    errors.extend(scenario_errors)
    if errors:
        return errors
    items = data.get("scenarios")
    if not isinstance(items, list) or not items:
        return ["scenarios.json: nonempty scenarios list required"]
    if data.get("execution_status") not in {"NOT_RUN", "PASS", "FAIL"}:
        errors.append("scenarios.json: invalid execution_status")
    names = {item.get("name") for item in catalog.get("skills", []) if isinstance(item, dict)}
    covered: set[str] = set()
    ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            errors.append("scenarios.json: scenario must be an object")
            continue
        identity, skill = item.get("id"), item.get("skill")
        if not isinstance(identity, str) or not identity or identity in ids:
            errors.append("scenarios.json: missing or duplicate scenario id")
        else:
            ids.add(identity)
        if not isinstance(skill, str) or skill not in names:
            errors.append(f"scenarios.json: unknown skill: {skill}")
        else:
            covered.add(skill)
        if not isinstance(item.get("prompt"), str) or not item["prompt"].strip():
            errors.append(f"scenarios.json: {identity}: prompt required")
        for field in ("expected", "forbidden"):
            values = item.get(field)
            if not isinstance(values, list) or not values or not all(isinstance(v, str) and v.strip() for v in values):
                errors.append(f"scenarios.json: {identity}: nonempty {field} strings required")
    for name in sorted(names - covered):
        errors.append(f"scenarios.json: no pressure scenario for {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args().root.resolve()
    markdown = sorted(p for p in root.rglob("*.md") if not EXCLUDED.intersection(p.relative_to(root).parts))
    skills = sorted((root / ".agents/skills").glob("*/SKILL.md"))
    errors: list[str] = []
    for path in markdown:
        errors.extend(check_markdown(path, root))
    for path in skills:
        errors.extend(check_skill(path))
    errors.extend(check_catalog(root))
    errors.extend(check_scenarios(root))
    if errors:
        print("Documentation validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS: {len(markdown)} Markdown files; {len(skills)} skills; catalog and scenario shape.")
    print("Not checked: external links, heading anchors, secret exposure, runtime behavior, or agent compliance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
