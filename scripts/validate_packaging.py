#!/usr/bin/env python3
"""Validate metadata shared by the Xweather plugin packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
        return {}
    except json.JSONDecodeError as error:
        errors.append(f"invalid JSON in {path}: {error}")
        return {}

    if not isinstance(value, dict):
        errors.append(f"expected a JSON object in {path}")
        return {}
    return value


def frontmatter_value(path: Path, field: str, errors: list[str]) -> str | None:
    try:
        text = path.read_text()
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
        return None

    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        errors.append(f"missing or malformed YAML frontmatter in {path}")
        return None

    field_match = re.search(
        rf"^[ \t]*{re.escape(field)}:\s*(.+?)\s*$", match.group(1), re.MULTILINE
    )
    if not field_match:
        errors.append(f"missing frontmatter field {field!r} in {path}")
        return None
    return field_match.group(1).strip("\"'")


def compare_values(label: str, values: dict[str, Any], errors: list[str]) -> None:
    serialized = {
        source: json.dumps(value, ensure_ascii=False, sort_keys=True)
        for source, value in values.items()
    }
    if len(set(serialized.values())) <= 1:
        return

    details = ", ".join(f"{source}={value}" for source, value in serialized.items())
    errors.append(f"{label} drift: {details}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    plugin_root = root / "plugins/xweather"
    marketplace_path = root / ".claude-plugin/marketplace.json"
    claude_manifest_path = plugin_root / ".claude-plugin/plugin.json"
    codex_manifest_path = plugin_root / ".codex-plugin/plugin.json"

    marketplace = load_json(marketplace_path, errors)
    claude_manifest = load_json(claude_manifest_path, errors)
    codex_manifest = load_json(codex_manifest_path, errors)
    if errors:
        return errors

    shared_fields = ("name", "version", "description", "author", "homepage", "license", "keywords")
    for manifest_path, manifest in (
        (claude_manifest_path, claude_manifest),
        (codex_manifest_path, codex_manifest),
    ):
        for field in shared_fields:
            if field not in manifest:
                errors.append(f"missing shared field {field!r} in {manifest_path}")

    for field in shared_fields:
        compare_values(
            f"plugin {field}",
            {
                str(claude_manifest_path): claude_manifest.get(field),
                str(codex_manifest_path): codex_manifest.get(field),
            },
            errors,
        )

    plugin_name = claude_manifest.get("name")
    if plugin_name != plugin_root.name:
        errors.append(
            f"plugin name {plugin_name!r} must match directory name {plugin_root.name!r}"
        )

    if codex_manifest.get("skills") != "./skills/":
        errors.append(f"{codex_manifest_path} must set skills to './skills/'")

    marketplace_plugins = marketplace.get("plugins")
    if not isinstance(marketplace_plugins, list):
        errors.append(f"{marketplace_path} must contain a plugins array")
        marketplace_plugins = []

    matching_entries = [
        entry
        for entry in marketplace_plugins
        if isinstance(entry, dict) and entry.get("name") == plugin_name
    ]
    if len(matching_entries) != 1:
        errors.append(
            f"{marketplace_path} must contain exactly one entry named {plugin_name!r}"
        )
        marketplace_entry: dict[str, Any] = {}
    else:
        marketplace_entry = matching_entries[0]

    if marketplace_entry.get("source") != "./plugins/xweather":
        errors.append(
            f"marketplace source must be './plugins/xweather', got {marketplace_entry.get('source')!r}"
        )

    codex_interface = codex_manifest.get("interface")
    if not isinstance(codex_interface, dict):
        errors.append(f"{codex_manifest_path} must contain an interface object")
        codex_interface = {}

    compare_values(
        "plugin display name",
        {
            str(marketplace_path): marketplace_entry.get("displayName"),
            str(claude_manifest_path): claude_manifest.get("displayName"),
            str(codex_manifest_path): codex_interface.get("displayName"),
        },
        errors,
    )

    manifest_version = claude_manifest.get("version")
    skill_paths = sorted((plugin_root / "skills").glob("*/SKILL.md"))
    if not skill_paths:
        errors.append(f"no skills found under {plugin_root / 'skills'}")

    for skill_path in skill_paths:
        skill_name = frontmatter_value(skill_path, "name", errors)
        skill_version = frontmatter_value(skill_path, "version", errors)
        description = frontmatter_value(skill_path, "description", errors)

        if skill_name != skill_path.parent.name:
            errors.append(
                f"skill name {skill_name!r} in {skill_path} must match directory name "
                f"{skill_path.parent.name!r}"
            )
        if skill_version != manifest_version:
            errors.append(
                f"skill version drift: {skill_path}={skill_version!r}, "
                f"plugin manifests={manifest_version!r}"
            )
        if description is not None and len(description) > 1024:
            errors.append(f"skill description exceeds 1024 characters in {skill_path}")

    if claude_manifest.get("license") and not (root / "LICENSE").is_file():
        errors.append("plugin declares a license but the repository has no LICENSE file")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root (defaults to the parent of this script's directory)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate(root)

    if errors:
        print("Packaging validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Packaging validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
