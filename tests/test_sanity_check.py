"""Unit tests for the Plum-Antibodies sanity-check implementation."""

import importlib.util
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).parents[1] / "tools" / "sanity-check.py"
SPEC = importlib.util.spec_from_file_location("sanity_check", SCRIPT_PATH)
sanity_check = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sanity_check)


def test_valid_query_supports_groups_modifiers_and_not():
    """Accept the search syntax supported by Plum-Island tag rules."""
    sanity_check.validate_query(
        'http_server.bg:"Apache/" AND NOT port:443 OR banner.lk:"OpenSSH"'
    )


@pytest.mark.parametrize(
    "query",
    [
        "unknown_field:value",
        "tag.like:router",
        "NOT port:443",
        "http_headval:Bad Header:value",
        "port:443 OR",
    ],
)
def test_invalid_query_is_rejected(query):
    """Reject unsupported fields, modifiers, headers, and group syntax."""
    with pytest.raises(sanity_check.RuleError):
        sanity_check.validate_query(query)


def test_http_headval_accepts_header_and_value_modifiers():
    """Accept the special header-name and header-value query form."""
    sanity_check.validate_query('http_headval:content-type.lk:"application/json"')


def test_normalize_tags_matches_runtime_tag_normalization():
    """Normalize case and legacy tag prefixes before reporting applied tags."""
    assert sanity_check.normalize_tags(["TAG:Vendor:Cisco", "type:Router"]) == [
        "vendor:cisco",
        "type:router",
    ]


def test_valid_rule_returns_normalized_tags(tmp_path):
    """Validate a complete synthetic rule and return its applied tags."""
    rule_path = tmp_path / "example.yaml"
    rule_path.write_text(
        "description: Example\n"
        "query: http_server.bg:Example\n"
        "tags:\n"
        "- product:example\n"
        "- type:service\n"
        "references:\n"
        "- https://example.com/advisory\n"
        "version: 20260916T000000Z\n",
        encoding="utf-8",
    )

    assert sanity_check.validate_rule(rule_path) == ["product:example", "type:service"]


@pytest.mark.parametrize("references", ["https://example.com", ["ftp://example.com"]])
def test_invalid_references_are_rejected(tmp_path, references):
    """Reject non-list references and links outside HTTP(S)."""
    rule_path = tmp_path / "invalid-references.yaml"
    rule_path.write_text(
        "description: Example\n"
        "query: banner:Example\n"
        "tags:\n"
        "- type:service\n"
        f"references: {references!r}\n"
        "version: 20260916T000000Z\n",
        encoding="utf-8",
    )

    with pytest.raises(sanity_check.RuleError, match="references"):
        sanity_check.validate_rule(rule_path)


def test_rule_without_version_is_rejected(tmp_path):
    """Require a version so imports can apply the update policy safely."""
    rule_path = tmp_path / "missing-version.yaml"
    rule_path.write_text(
        "description: Example\nquery: banner:Example\ntags:\n- type:service\n",
        encoding="utf-8",
    )

    with pytest.raises(sanity_check.RuleError, match="missing required field: version"):
        sanity_check.validate_rule(rule_path)
