#!/usr/bin/env python3
"""Add short, stable names to Plum-Antibodies rules missing one."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = REPOSITORY_ROOT / "tags"
NAME_RE = re.compile(r"^name:.*$", re.MULTILINE)
DESCRIPTION_RE = re.compile(r"^description:", re.MULTILINE)
VERSION_RE = re.compile(r"^version:.*$", re.MULTILINE)


def rule_name(path: Path) -> str:
    """Build a lowercase, readable rule name of at most 25 characters."""
    stem = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    return stem[:25].rstrip("-")


def update_rule(path: Path, stamp: str) -> bool:
    """Insert a derived name and update version when name is absent."""
    content = path.read_text(encoding="utf-8")
    if NAME_RE.search(content):
        return False
    if not DESCRIPTION_RE.search(content):
        raise ValueError(f"{path}: cannot find description field")
    content = DESCRIPTION_RE.sub(
        f'name: "{rule_name(path)}"\ndescription:', content, count=1
    )
    if not VERSION_RE.search(content):
        raise ValueError(f"{path}: cannot find version field")
    content = VERSION_RE.sub(f"version: {stamp}", content, count=1)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    """Update YAML rules missing short names."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    paths = sorted(RULES_DIR.glob("*.yaml"))
    changed = sum(update_rule(path, stamp) for path in paths)
    print(f"Updated {changed} rules (version {stamp}).")


if __name__ == "__main__":
    main()
