#!/usr/bin/env python3
"""Validate Plum-Antibodies YAML rules before they are imported by Plum-Island."""

from __future__ import annotations

import argparse
import re
import shlex
import sys
import warnings
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as error:  # pragma: no cover - environment setup
    print(
        "ERROR: PyYAML is required; install it with 'pip install PyYAML'.",
        file=sys.stderr,
    )
    raise SystemExit(2) from error


ALLOWED_FIELDS = {
    "ip",
    "net",
    "fqdn",
    "fqdn_requested",
    "host",
    "domain",
    "domain_requested",
    "tld",
    "tag",
    "port",
    "http_title",
    "http_favicon_path",
    "http_favicon_mmhash",
    "http_favicon_md5",
    "http_favicon_sha256",
    "http_cookiename",
    "http_etag",
    "http_header",
    "http_headval",
    "http_server",
    "x509_issuer",
    "x509_issuer_cn",
    "x509_md5",
    "x509_sha1",
    "x509_sha256",
    "x509_subject",
    "x509_subject_cn",
    "x509_san",
    "banner",
}
ALLOWED_MODIFIERS = {".lk", ".like", ".bg", ".begin", ".not", ".nt"}
VALUE_MODIFIERS = {".lk", ".like", ".bg", ".begin"}
EXACT_ONLY_FIELDS = {"tag"}
VERSION_RE = re.compile(r"^\d{8}T\d{6}Z$")
HTTP_HEADER_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9a-z]+$")


class RuleError(ValueError):
    """A rule is not valid for the Plum-Island importer or search parser."""


def split_groups(query: str) -> list[list[str]]:
    try:
        parts = shlex.split(query)
    except ValueError as error:
        raise RuleError(f"invalid quoting: {error}") from error

    if not parts:
        raise RuleError("empty query")

    groups: list[list[str]] = []
    current: list[str] = []
    previous = None
    for part in parts:
        operator = part.upper()
        if operator == "OR":
            if not current:
                raise RuleError("OR cannot start, end, or follow another OR")
            groups.append(current)
            current = []
        elif operator == "AND":
            if not current or previous in {"AND", "OR"}:
                raise RuleError("AND must join two search terms")
        else:
            current.append(part)
        previous = operator

    if not current:
        raise RuleError("query cannot end with OR")
    groups.append(current)
    return groups


def validate_http_headval(term: str) -> None:
    payload = term[len("http_headval:") :]
    if ":" not in payload:
        raise RuleError("http_headval requires header:value")

    header_expr, value = payload.split(":", 1)
    if not header_expr or not value.strip():
        raise RuleError("http_headval requires a non-empty header and value")

    for modifier in VALUE_MODIFIERS:
        if header_expr.endswith(modifier):
            header_expr = header_expr[: -len(modifier)]
            break

    header_expr = header_expr.lower()
    if not HTTP_HEADER_RE.fullmatch(header_expr) or len(header_expr) > 128:
        raise RuleError(f"invalid HTTP header name: {header_expr!r}")


def validate_term(term: str, negated: bool = False) -> None:
    if term.lower().startswith("http_headval:"):
        validate_http_headval(term)
        return

    if ":" not in term:
        raise RuleError(f"expected field:value, got {term!r}")

    key, value = term.split(":", 1)
    key = key.lower()
    if not value:
        raise RuleError(f"empty value for {key}")

    modifier = ""
    base = key
    for suffix in ALLOWED_MODIFIERS:
        if key.endswith(suffix):
            modifier = suffix
            base = key[: -len(suffix)]
            break

    if base not in ALLOWED_FIELDS:
        raise RuleError(f"unsupported search field: {base}")
    if modifier and base in EXACT_ONLY_FIELDS:
        raise RuleError(f"{base} does not support {modifier}")
    if negated and modifier in {".not", ".nt"}:
        raise RuleError("NOT cannot be combined with .not or .nt")


def validate_query(query: object) -> None:
    if not isinstance(query, str):
        raise RuleError("query must be a string")

    for group in split_groups(query):
        positive_terms = []
        tokens = iter(group)
        for token in tokens:
            if token.upper() == "NOT":
                operand = next(tokens, None)
                if operand is None or operand.upper() in {"AND", "OR", "NOT"}:
                    raise RuleError("NOT must be followed by a field:value term")
                validate_term(operand, negated=True)
            else:
                positive_terms.append(token)
                validate_term(token)
        if not positive_terms:
            raise RuleError("each OR group containing NOT needs a positive term")


def normalize_tags(raw_tags: object) -> list[str]:
    if isinstance(raw_tags, str):
        raw_tags = [raw_tags]
    if not isinstance(raw_tags, list) or not raw_tags:
        raise RuleError("tags must be a non-empty YAML list")

    tags = []
    seen = set()
    for raw_tag in raw_tags:
        if not isinstance(raw_tag, str):
            raise RuleError("every tag must be a string")
        tag = raw_tag.strip().lower()
        while tag.startswith("tag:") and tag.count(":") >= 2:
            tag = tag.split(":", 1)[1].strip()
        if not tag:
            raise RuleError("tags cannot contain empty values")
        if tag in seen:
            raise RuleError(f"duplicate tag: {tag}")
        seen.add(tag)
        tags.append(tag)
    return tags


def validate_rule(path: Path) -> list[str]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise RuleError(f"cannot load YAML: {error}") from error

    if not isinstance(payload, dict):
        raise RuleError("top level must be a YAML mapping")

    for field in ("description", "query", "tags", "version"):
        if field not in payload:
            raise RuleError(f"missing required field: {field}")

    if not isinstance(payload["description"], str) or not payload["description"].strip():
        raise RuleError("description must be a non-empty string")
    validate_query(payload["query"])
    tags = normalize_tags(payload["tags"])

    version = payload["version"]
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise RuleError("version must use YYYYMMDDTHHMMSSZ")
    return tags


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "rules_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "tags",
        help="directory containing YAML rules (default: ../tags)",
    )
    parser.add_argument(
        "--type",
        dest="show_types",
        action="store_true",
        help="print type tags for each rule and a unique sorted summary",
    )
    args = parser.parse_args()
    paths = sorted(args.rules_dir.glob("*.yaml"))
    if not paths:
        print(f"ERROR: no YAML rules found in {args.rules_dir}", file=sys.stderr)
        return 2

    failures = 0
    found_types: set[str] = set()
    for path in paths:
        try:
            tags = validate_rule(path)
        except RuleError as error:
            failures += 1
            warnings.warn(f"{path.name}: {error}", stacklevel=0)
            print(f"WARNING {path.name}: invalid rule", flush=True)
            continue
        if args.show_types:
            type_tags = [tag for tag in tags if tag.startswith("type:")]
            found_types.update(type_tags)
            display = ", ".join(type_tags) if type_tags else "(none)"
            print(f"{path.name}: types -> {display}", flush=True)
        else:
            print(f"OK {path.name}: tags -> {', '.join(tags)}", flush=True)

    print(f"Checked {len(paths)} rules: {len(paths) - failures} OK, {failures} warning(s).")
    if args.show_types:
        print("Unique types found:")
        for type_tag in sorted(found_types):
            print(type_tag)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
