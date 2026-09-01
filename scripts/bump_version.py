#!/usr/bin/env python3
"""Bump the plugin version everywhere validate_packaging.py requires it to match.

The version lives in three places that must stay identical:

    plugins/xweather/.claude-plugin/plugin.json    "version"
    plugins/xweather/.codex-plugin/plugin.json     "version"
    plugins/xweather/skills/*/SKILL.md             metadata.version (frontmatter)

Edits are line-targeted rather than a JSON/YAML round-trip, so formatting, key order, and
non-ASCII characters in the surrounding files survive untouched.

    python3 scripts/bump_version.py --level patch     # 0.14.0 -> 0.14.1
    python3 scripts/bump_version.py --set 1.0.0
    python3 scripts/bump_version.py --check           # report the current version, write nothing

On success the new version is printed to stdout on its own line, so a workflow can capture it:

    version=$(python3 scripts/bump_version.py --level patch)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SEMVER_PATTERN = re.compile(r"\A(\d+)\.(\d+)\.(\d+)\Z")
FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
# Matches a JSON "version": "X" pair at the top level of a manifest.
MANIFEST_VERSION_PATTERN = re.compile(
    r'^(?P<prefix>[ \t]*"version"[ \t]*:[ \t]*")(?P<version>[^"]*)(?P<suffix>",?)[ \t]*$', re.MULTILINE
)
# Matches a `version: X` line inside YAML frontmatter, quoted or bare.
FRONTMATTER_VERSION_PATTERN = re.compile(r'^(?P<prefix>[ \t]*version[ \t]*:[ \t]*)(?P<quote>["\']?)(?P<version>[^"\'\r\n]*)(?P=quote)[ \t]*$', re.MULTILINE)


class BumpError(Exception):
    """A problem that should stop the bump before anything is written."""


def next_version(current: str, level: str) -> str:
    match = SEMVER_PATTERN.match(current)
    if not match:
        raise BumpError(f"current version {current!r} is not MAJOR.MINOR.PATCH")

    major, minor, patch = (int(part) for part in match.groups())
    if level == "major":
        return f"{major + 1}.0.0"
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def manifest_paths(plugin_root: Path) -> list[Path]:
    return [
        plugin_root / ".claude-plugin/plugin.json",
        plugin_root / ".codex-plugin/plugin.json",
    ]


def read_manifest_version(path: Path) -> str:
    try:
        text = path.read_text()
    except FileNotFoundError as error:
        raise BumpError(f"missing required file: {path}") from error

    matches = MANIFEST_VERSION_PATTERN.findall(text)
    if len(matches) != 1:
        raise BumpError(
            f"expected exactly one top-level \"version\" line in {path}, found {len(matches)}"
        )
    return matches[0][1]


def read_skill_version(path: Path) -> str:
    frontmatter = FRONTMATTER_PATTERN.match(path.read_text())
    if not frontmatter:
        raise BumpError(f"missing or malformed YAML frontmatter in {path}")

    matches = FRONTMATTER_VERSION_PATTERN.findall(frontmatter.group(1))
    if len(matches) != 1:
        raise BumpError(
            f"expected exactly one 'version:' line in the frontmatter of {path}, "
            f"found {len(matches)}"
        )
    return matches[0][2]


def write_manifest_version(path: Path, version: str) -> None:
    text = path.read_text()
    updated = MANIFEST_VERSION_PATTERN.sub(
        lambda match: f"{match.group('prefix')}{version}{match.group('suffix')}", text, count=1
    )
    path.write_text(updated)


def write_skill_version(path: Path, version: str) -> None:
    # Rewrite inside the frontmatter block only — skill bodies discuss SDK versions in prose.
    text = path.read_text()
    frontmatter = FRONTMATTER_PATTERN.match(text)
    assert frontmatter is not None  # read_skill_version already validated this

    block = frontmatter.group(1)
    updated_block = FRONTMATTER_VERSION_PATTERN.sub(
        lambda match: f"{match.group('prefix')}{match.group('quote')}{version}{match.group('quote')}",
        block,
        count=1,
    )
    path.write_text(text[: frontmatter.start(1)] + updated_block + text[frontmatter.end(1) :])


def collect(root: Path) -> tuple[str, list[Path], list[Path]]:
    """Return the shared current version plus the manifest and skill files holding it."""
    plugin_root = root / "plugins/xweather"
    manifests = manifest_paths(plugin_root)
    skills = sorted((plugin_root / "skills").glob("*/SKILL.md"))
    if not skills:
        raise BumpError(f"no skills found under {plugin_root / 'skills'}")

    versions = {path: read_manifest_version(path) for path in manifests}
    versions.update({path: read_skill_version(path) for path in skills})

    distinct = set(versions.values())
    if len(distinct) != 1:
        details = "\n".join(f"  {path}: {value!r}" for path, value in sorted(versions.items()))
        raise BumpError(
            "versions already disagree — fix the drift before bumping:\n" + details
        )

    return distinct.pop(), manifests, skills


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--level",
        choices=("major", "minor", "patch"),
        default="patch",
        help="which component to increment (default: patch)",
    )
    parser.add_argument("--set", dest="explicit", help="set this exact version instead of incrementing")
    parser.add_argument("--check", action="store_true", help="print the current version and write nothing")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root (defaults to the parent of this script's directory)",
    )
    args = parser.parse_args()

    try:
        current, manifests, skills = collect(args.root.resolve())

        if args.check:
            print(current)
            return 0

        if args.explicit:
            if not SEMVER_PATTERN.match(args.explicit):
                raise BumpError(f"--set {args.explicit!r} is not MAJOR.MINOR.PATCH")
            new = args.explicit
        else:
            new = next_version(current, args.level)

        if new == current:
            raise BumpError(f"new version {new!r} matches the current version")

        for path in manifests:
            write_manifest_version(path, new)
        for path in skills:
            write_skill_version(path, new)
    except BumpError as error:
        print(f"bump_version: {error}", file=sys.stderr)
        return 1

    print(f"Bumped {current} -> {new} across {len(manifests)} manifests and {len(skills)} skills.", file=sys.stderr)
    print(new)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
