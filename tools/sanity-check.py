#!/usr/bin/env python3
"""Validate Plum-Antibodies YAML rules before they are imported by Plum-Island."""

from __future__ import annotations

import argparse
import re
import shlex
import sys
import warnings
from uuid import UUID
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from plum_antibodies import (  # pylint: disable=wrong-import-position
    TagValidationError,
    validate_tags,
)

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
    "service",
    "engine",
}
ALLOWED_MODIFIERS = {".lk", ".like", ".bg", ".begin", ".not", ".nt"}
VALUE_MODIFIERS = {".lk", ".like", ".bg", ".begin"}
EXACT_ONLY_FIELDS = {"tag", "engine"}
VERSION_RE = re.compile(r"^\d{8}T\d{6}Z$")
HTTP_HEADER_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9a-z]+$")
LINK_RE = re.compile(r"^https?://\S+$", re.IGNORECASE)
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,24}$")


class RuleError(ValueError):
    """A rule is not valid for the Plum-Island importer or search parser."""


def tokenize_query(query: str) -> list[tuple[str, str]]:
    """Decode terms while keeping unquoted parentheses as runtime syntax tokens."""
    tokens: list[tuple[str, str]] = []
    start = 0
    quote = None
    escaped = False

    def emit(stop: int) -> None:
        """Decode one original token without reinterpreting its quoted contents."""
        raw = query[start:stop]
        if raw:
            try:
                value = shlex.split(raw)[0]
            except ValueError as error:
                raise RuleError(f"invalid quoting: {error}") from error
            kind = value.upper() if value.upper() in {"AND", "OR", "NOT"} else "TERM"
            tokens.append((kind, value))

    for position, char in enumerate(query):
        if escaped:
            escaped = False
        elif char == "\\" and quote != "'":
            escaped = True
        elif quote:
            if char == quote:
                quote = None
        elif char in {"'", '"'}:
            quote = char
        elif char.isspace() or char in "()":
            emit(position)
            if char in "()":
                tokens.append((char, char))
            start = position + 1
    emit(len(query))
    return tokens


class QueryValidator:
    """Validate one-level Boolean groups without expanding their combinations."""

    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        """Initialize validation over quote-aware tokens with a shared cursor."""
        self.tokens = tokens
        self.position = 0

    def peek(self) -> str:
        """Return the next token kind, or END when input has been consumed."""
        return (
            self.tokens[self.position][0] if self.position < len(self.tokens) else "END"
        )

    def parse_or(self, grouped: bool = False) -> bool:
        """Validate OR branches and report whether every path has a positive bound."""
        bounds = [self.parse_and(grouped)]
        while self.peek() == "OR":
            self.position += 1
            bounds.append(self.parse_and(grouped))
        return all(bounds)

    def parse_and(self, grouped: bool) -> bool:
        """Validate explicit/implicit conjunctions and report any positive bound."""
        positive = False
        expect_operand = True
        while self.peek() not in {"END", "OR", ")"}:
            kind = self.peek()
            if kind == "AND":
                if expect_operand:
                    raise RuleError("AND must join two search terms or groups")
                self.position += 1
                expect_operand = True
                continue
            if kind == "(":
                if grouped:
                    raise RuleError("nested parentheses are not supported")
                self.position += 1
                bounded = self.parse_or(grouped=True)
                if self.peek() != ")":
                    raise RuleError("missing closing parenthesis")
                self.position += 1
                positive = positive or bounded
            else:
                negated = kind == "NOT"
                if negated:
                    self.position += 1
                    if self.peek() != "TERM":
                        raise RuleError("NOT must be followed by a field:value term")
                validate_term(self.tokens[self.position][1], negated=negated)
                self.position += 1
                positive = positive or not negated
            expect_operand = False
        if expect_operand:
            raise RuleError("missing search term or empty group")
        return positive


def validate_http_headval(term: str) -> None:
    """Validate the special header:value term and its value-matching modifier."""
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


def validate_nse_body(term: str) -> None:
    """Validate an exact or script-scoped NSE result term."""
    key, _, value = term.partition(":")
    key = key.lower()
    modifier = key.removeprefix("nse.body")
    if key == "nse.body" and ":" in value:
        scope, _, value = value.partition(":")
        script, dot, mode = scope.lower().partition(".")
        if not re.fullmatch(r"[a-z0-9_-]+", script):
            raise RuleError("invalid NSE script name")
        modifier = dot + mode
    if modifier and modifier not in VALUE_MODIFIERS:
        raise RuleError("invalid nse.body modifier")
    if not value.strip():
        raise RuleError("nse.body requires non-empty output text")


def validate_term(term: str, negated: bool = False) -> None:
    """Validate a field/value term, including allowed modifiers and negation."""
    if term.lower().startswith("http_headval:"):
        validate_http_headval(term)
        return
    if term.lower().startswith(("nse.body:", "nse.body.")):
        validate_nse_body(term)
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
    """Reject malformed queries using the runtime's quote and group semantics."""
    if not isinstance(query, str):
        raise RuleError("query must be a string")
    tokens = tokenize_query(query)
    if not tokens:
        raise RuleError("empty query")
    validator = QueryValidator(tokens)
    try:
        bounded = validator.parse_or()
        if validator.peek() != "END":
            raise RuleError("unexpected closing parenthesis")
        if not bounded:
            raise RuleError("each OR path needs a positive search term")
    except RuleError as error:
        if any(kind in {"(", ")"} for kind, _ in tokens):
            raise RuleError(
                f"{error}; quote literal parentheses in field values, "
                'for example banner.lk:"(Debian)" or http_title.lk:"phpinfo()"'
            ) from error
        raise


def normalize_tags(raw_tags: object) -> list[str]:
    """Normalize rule tags through the shared public validation library."""
    try:
        return validate_tags(raw_tags)
    except TagValidationError as error:
        raise RuleError(str(error)) from error


def validate_references(raw_references: object) -> None:
    """Validate optional rule references as a list of HTTP(S) links."""
    if not isinstance(raw_references, list) or not raw_references:
        raise RuleError("references must be a YAML list of links")
    for reference in raw_references:
        if not isinstance(reference, str) or not LINK_RE.fullmatch(reference.strip()):
            raise RuleError(f"invalid reference link: {reference!r}")


def validate_rule(path: Path) -> tuple[list[str], str]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise RuleError(f"cannot load YAML: {error}") from error

    if not isinstance(payload, dict):
        raise RuleError("top level must be a YAML mapping")

    for field in ("name", "description", "uuid", "query", "tags", "version"):
        if field not in payload:
            raise RuleError(f"missing required field: {field}")

    if (
        not isinstance(payload["description"], str)
        or not payload["description"].strip()
    ):
        raise RuleError("description must be a non-empty string")
    name = payload["name"]
    if not isinstance(name, str) or not NAME_RE.fullmatch(name):
        raise RuleError("name must be a lowercase slug of at most 25 characters")
    rule_uuid = payload["uuid"]
    if not isinstance(rule_uuid, str):
        raise RuleError("uuid must be a canonical UUID string")
    try:
        parsed_uuid = UUID(rule_uuid)
    except ValueError as error:
        raise RuleError("uuid must be a canonical UUID string") from error
    if str(parsed_uuid) != rule_uuid:
        raise RuleError("uuid must be a canonical UUID string")
    validate_query(payload["query"])
    tags = normalize_tags(payload["tags"])
    if "references" in payload:
        validate_references(payload["references"])

    version = payload["version"]
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise RuleError("version must use YYYYMMDDTHHMMSSZ")
    return tags, rule_uuid


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
    parser.add_argument(
        "--proto",
        dest="show_protocols",
        action="store_true",
        help="print protocol tags for each rule and a unique sorted summary",
    )
    args = parser.parse_args()
    paths = sorted(args.rules_dir.glob("*.yaml"))
    if not paths:
        print(f"ERROR: no YAML rules found in {args.rules_dir}", file=sys.stderr)
        return 2

    failures = 0
    found_types: set[str] = set()
    found_protocols: set[str] = set()
    seen_uuids: dict[str, Path] = {}
    for path in paths:
        try:
            tags, rule_uuid = validate_rule(path)
        except RuleError as error:
            failures += 1
            warnings.warn(f"{path.name}: {error}", stacklevel=0)
            print(f"WARNING {path.name}: invalid rule", flush=True)
            continue
        if rule_uuid in seen_uuids:
            failures += 1
            warnings.warn(
                f"{path.name}: duplicate uuid also used by {seen_uuids[rule_uuid].name}",
                stacklevel=0,
            )
            print(f"WARNING {path.name}: invalid rule", flush=True)
            continue
        seen_uuids[rule_uuid] = path
        if args.show_types or args.show_protocols:
            type_tags = [tag for tag in tags if tag.startswith("type:")]
            protocol_tags = [tag for tag in tags if tag.startswith("proto:")]
            found_types.update(type_tags)
            found_protocols.update(protocol_tags)
            details = []
            if args.show_types:
                details.append(
                    f"types -> {', '.join(type_tags) if type_tags else '(none)'}"
                )
            if args.show_protocols:
                details.append(
                    f"protocols -> {', '.join(protocol_tags) if protocol_tags else '(none)'}"
                )
            print(f"{path.name}: {' | '.join(details)}", flush=True)
        else:
            print(f"OK {path.name}: tags -> {', '.join(tags)}", flush=True)

    print(
        f"Checked {len(paths)} rules: {len(paths) - failures} OK, {failures} warning(s)."
    )
    if args.show_types:
        print("Unique types found:")
        for type_tag in sorted(found_types):
            print(type_tag)
    if args.show_protocols:
        print("Unique protocols found:")
        for protocol_tag in sorted(found_protocols):
            print(protocol_tag)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
