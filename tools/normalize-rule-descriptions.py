#!/usr/bin/env python3
"""Normalize rule descriptions as concise detection statements."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = REPOSITORY_ROOT / "tags"
DESCRIPTION_RE = re.compile(r"^description: (.+)$", re.MULTILINE)
VERSION_RE = re.compile(r"^version:.*$", re.MULTILINE)
TYPE_LABELS = {
    "api-gateway": "API gateway",
    "c2": "C2",
    "camera": "camera",
    "cms": "CMS",
    "dashboard": "dashboard",
    "database": "database",
    "datalogger": "datalogger",
    "firewall": "firewall",
    "iot": "IoT",
    "linux": "Linux",
    "message-queue": "message queue",
    "nas": "NAS",
    "parking": "domain parking",
    "proxy": "proxy",
    "router": "router",
    "slb": "load balancer",
    "supervision": "supervision",
    "switch": "switch",
    "telephony": "telephony",
    "voip": "VoIP",
    "vpn": "VPN",
    "webmail": "webmail",
}


def normalized_description(description: str, tags: list[str]) -> str:
    """Prefix detection intent and append absent human-readable type tags."""
    base = description.removeprefix("Detect ").strip()
    type_labels = [
        TYPE_LABELS[tag.removeprefix("type:")]
        for tag in tags
        if tag.startswith("type:")
    ]
    missing_labels = [
        label for label in type_labels if label.lower() not in base.lower()
    ]
    suffix = f" ({', '.join(missing_labels)})" if missing_labels else ""
    return f"Detect {base}{suffix}"


def update_rule(path: Path, stamp: str) -> bool:
    """Rewrite description and version only when normalization changes it."""
    content = path.read_text(encoding="utf-8")
    payload = yaml.safe_load(content)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: top level must be a mapping")
    description = payload.get("description")
    tags = payload.get("tags")
    if not isinstance(description, str) or not isinstance(tags, list):
        raise ValueError(f"{path}: invalid description or tags")
    replacement = normalized_description(description, tags)
    if replacement == description:
        return False
    if not DESCRIPTION_RE.search(content):
        raise ValueError(f"{path}: unsupported description format")
    yaml_description = yaml.safe_dump(
        replacement, allow_unicode=True, default_style='"'
    ).strip()
    content = DESCRIPTION_RE.sub(
        f"description: {yaml_description}", content, count=1
    )
    content = VERSION_RE.sub(f"version: {stamp}", content, count=1)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    """Normalize all descriptions in the rules directory."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    changed = sum(update_rule(path, stamp) for path in sorted(RULES_DIR.glob("*.yaml")))
    print(f"Updated {changed} rules (version {stamp}).")


if __name__ == "__main__":
    main()
