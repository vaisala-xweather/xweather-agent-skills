#!/usr/bin/env python3
"""Build OpenAI and Claude plugin archives in the distribution directory."""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path


FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
EXCLUDED_NAMES = {".DS_Store", "__pycache__"}


def without_metadata_frontmatter(text: str, path: Path) -> str:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        raise ValueError(f"missing or malformed YAML frontmatter in {path}")

    lines = match.group(1).splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line != "metadata:":
            output.append(line)
            index += 1
            continue

        index += 1
        while index < len(lines) and (
            not lines[index] or lines[index][0].isspace()
        ):
            index += 1

    newline = "\r\n" if "\r\n" in match.group(0) else "\n"
    frontmatter = newline.join(output)
    return f"---{newline}{frontmatter}{newline}---{newline}{text[match.end():]}"


def should_include(relative_path: Path, provider: str) -> bool:
    if (
        any(part in EXCLUDED_NAMES for part in relative_path.parts)
        or relative_path.suffix == ".pyc"
    ):
        return False
    if provider == "claude" and relative_path.parts[0] == "bin":
        return False
    if provider == "openai":
        return not (
            relative_path.name == "openai.yaml"
            and relative_path.parent.name == "agents"
            and "skills" in relative_path.parts
        )
    return True


def build_archive(plugin_root: Path, output_path: Path, provider: str) -> None:
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for source_path in sorted(plugin_root.rglob("*")):
            relative_path = source_path.relative_to(plugin_root)
            if not source_path.is_file() or not should_include(relative_path, provider):
                continue

            archive_path = Path(plugin_root.name) / relative_path
            if provider == "openai" and source_path.name == "SKILL.md":
                content = without_metadata_frontmatter(
                    source_path.read_text(), source_path
                )
                archive_info = zipfile.ZipInfo.from_file(
                    source_path, archive_path.as_posix()
                )
                archive_info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(archive_info, content)
            else:
                archive.write(source_path, archive_path.as_posix())


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plugin-root",
        type=Path,
        default=root / "plugins/xweather",
    )
    parser.add_argument(
        "--dist",
        type=Path,
        default=root / "dist",
    )
    args = parser.parse_args()

    plugin_root = args.plugin_root.resolve()
    dist = args.dist.resolve()
    dist.mkdir(parents=True, exist_ok=True)

    providers = {"openai": "OpenAI", "claude": "Claude"}
    for provider, display_name in providers.items():
        output_path = dist / f"{plugin_root.name}-{provider}.zip"
        build_archive(plugin_root, output_path, provider)
        print(f"{display_name} plugin archive built: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
