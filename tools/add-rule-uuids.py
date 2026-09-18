#!/usr/bin/env python3
"""Add random UUID identifiers to Plum-Antibodies rules missing one."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = REPOSITORY_ROOT / "tags"
UUID_RE = re.compile(r"^uuid:.*$", re.MULTILINE)
VERSION_RE = re.compile(r"^version:.*$", re.MULTILINE)


def update_rule(path: Path, stamp: str) -> bool:
    """Insert a random UUID and update the version when UUID is absent."""
    content = path.read_text(encoding="utf-8")
    if UUID_RE.search(content):
        return False
    if "\nquery:" not in content:
        raise ValueError(f"{path}: cannot find query field")
    content = content.replace("\nquery:", f"\nuuid: {uuid4()}\nquery:", 1)
    if not VERSION_RE.search(content):
        raise ValueError(f"{path}: cannot find version field")
    content = VERSION_RE.sub(f"version: {stamp}", content, count=1)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    """Update YAML rules missing a random UUID."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    paths = sorted(RULES_DIR.glob("*.yaml"))
    changed = sum(update_rule(path, stamp) for path in paths)
    print(f"Updated {changed} rules (version {stamp}).")


if __name__ == "__main__":
    main()
