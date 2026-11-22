"""Unit tests for the Plum-Antibodies sanity-check implementation."""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

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


def test_scanner_engine_is_exact_and_observed_service_is_supported():
    """Keep scanner provenance and observed services aligned with Island."""
    sanity_check.validate_query("engine:masscan AND service:ftp OR engine:nmap")
    with pytest.raises(sanity_check.RuleError):
        sanity_check.validate_query("engine.lk:masscan")


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


def test_normalize_tags_accepts_existing_product_punctuation():
    """Accept punctuation already used by legitimate product tag values."""
    assert sanity_check.normalize_tags(["product:Fritz!Box"]) == ["product:fritz!box"]


def test_normalize_tags_collapses_matching_rule_duplicates():
    """Keep a tag once when several matching rules apply it."""
    assert sanity_check.normalize_tags(["proto:ssh", "PROTO:SSH"]) == ["proto:ssh"]


@pytest.mark.parametrize("tag", ["product", "product:bad tag", ":nginx"])
def test_invalid_tag_syntax_is_rejected(tag):
    """Reject tag values outside the shared tag syntax."""
    with pytest.raises(sanity_check.RuleError, match="namespace:value"):
        sanity_check.normalize_tags([tag])


def test_valid_rule_returns_normalized_tags(tmp_path):
    """Validate a complete synthetic rule and return its applied tags."""
    rule_path = tmp_path / "example.yaml"
    rule_path.write_text(
        "name: example\n"
        "uuid: 61f5f651-504e-46ec-83d7-8c38ee61bc99\n"
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

    assert sanity_check.validate_rule(rule_path) == (
        ["product:example", "type:service"],
        "61f5f651-504e-46ec-83d7-8c38ee61bc99",
    )


@pytest.mark.parametrize("references", ["https://example.com", ["ftp://example.com"]])
def test_invalid_references_are_rejected(tmp_path, references):
    """Reject non-list references and links outside HTTP(S)."""
    rule_path = tmp_path / "invalid-references.yaml"
    rule_path.write_text(
        "name: example\n"
        "uuid: 61f5f651-504e-46ec-83d7-8c38ee61bc99\n"
        "description: Example\n"
        "query: banner:Example\n"
        "tags:\n"
        "- type:service\n"
        f"references: {references!r}\n"
        "version: 20260916T000000Z\n",
        encoding="utf-8",
    )

    with pytest.raises(sanity_check.RuleError, match="reference"):
        sanity_check.validate_rule(rule_path)


def test_rule_without_version_is_rejected(tmp_path):
    """Require a version so imports can apply the update policy safely."""
    rule_path = tmp_path / "missing-version.yaml"
    rule_path.write_text(
        "name: example\nuuid: 61f5f651-504e-46ec-83d7-8c38ee61bc99\n"
        "description: Example\nquery: banner:Example\ntags:\n- type:service\n",
        encoding="utf-8",
    )

    with pytest.raises(sanity_check.RuleError, match="missing required field: version"):
        sanity_check.validate_rule(rule_path)


@pytest.mark.parametrize(
    "query",
    ["banner.lk:(Debian)", "http_title.lk:phpinfo()", "http_server.lk:(Win64)"],
)
def test_unquoted_literal_parentheses_are_rejected(query):
    """Reject literal parentheses interpreted as malformed runtime group syntax."""
    with pytest.raises(sanity_check.RuleError, match="quote literal parentheses"):
        sanity_check.validate_query(query)


@pytest.mark.parametrize(
    "query",
    [
        'banner.lk:"(Debian)"',
        'http_title.lk:"phpinfo()"',
        'http_server.lk:"(Win64)"',
        "banner.lk:'(Debian)'",
        r"http_title.lk:phpinfo\(\)",
        'http_headval:server.lk:"Apache (Debian)"',
        "(http_server:Apache OR http_server:nginx) AND port:443",
        "port:443 (http_server:Apache OR http_server:nginx)",
        "(port:80 OR port:443) AND (http_server:Apache OR http_server:nginx)",
        "port:443 AND (NOT banner:x OR NOT banner:y)",
        "(port:443 AND NOT banner:x) OR port:80",
        'http_title:"Literal \\"quoted\\" (text)"',
    ],
)
def test_quotes_escapes_and_runtime_groups_remain_valid(query):
    """Preserve literal values, one-level sibling groups and bounded exclusions."""
    sanity_check.validate_query(query)


@pytest.mark.parametrize(
    "query",
    [
        "()",
        "port:443 AND ()",
        "(port:443 OR)",
        "(port:443",
        "port:443)",
        "((port:443))",
        "NOT (port:443)",
        "(NOT port:443) OR port:80",
        "(port:443 OR NOT port:80)",
        "port:443 AND",
        "port:443 AND OR port:80",
        'http_title:"unterminated',
        "NOT NOT port:443",
        "port:443 AND NOT port.nt:80",
    ],
)
def test_invalid_runtime_groups_are_rejected(query):
    """Reject empty, nested, unbalanced and unbounded Boolean expressions."""
    with pytest.raises(sanity_check.RuleError):
        sanity_check.validate_query(query)


@pytest.mark.parametrize(
    "query",
    ["banner.lk:(Debian)", "http_title.lk:phpinfo()", "http_server.lk:(Win64)"],
)
@pytest.mark.parametrize("quoted", [False, True])
def test_cli_exit_status_for_literal_parentheses(tmp_path, query, quoted):
    """Fail the CLI for invalid literals and succeed after quoting each value."""
    if quoted:
        field, value = query.split(":", 1)
        query = f'{field}:"{value}"'
    payload = {
        "name": "example",
        "description": "Detect example",
        "uuid": "61f5f651-504e-46ec-83d7-8c38ee61bc99",
        "query": query,
        "tags": ["product:example"],
        "version": "20261117T000000Z",
    }
    (tmp_path / "example.yaml").write_text(yaml.safe_dump(payload), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == (0 if quoted else 1)
    if quoted:
        assert "1 OK, 0 warning(s)" in result.stdout
    else:
        assert "OK example.yaml" not in result.stdout
        assert "example.yaml" in result.stderr
        assert "quote literal parentheses" in result.stderr
