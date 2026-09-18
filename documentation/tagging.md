# Writing tag rules

Plum-Island applies computed tags to scan documents through rules maintained in this repository. A rule matches scanner fields and writes its tags to the document index.

Rules are YAML files in `tags/`; each filename is its rule name.

```yaml
name: hashicorp-vault
description: HashiCorp Vault
uuid: afb4ef43-da13-5a98-b80e-499e2f908ef1
query: http_favicon_mmhash:747250914 AND http_title.bg:Vault
tags:
- product:hashicorp-vault
- vendor:hashicorp
version: 20260428T170756Z
```

| Field | Required | Description |
| ----- | -------- | ----------- |
| `name` | yes | Lowercase rule slug, 25 characters maximum. |
| `description` | yes | Human-readable detection statement, beginning with `Detect`. |
| `uuid` | yes | Unique canonical UUID. |
| `query` | yes | Query using documented [syntax](query-syntax.md). |
| `tags` | yes | One or more normalized tags. |
| `version` | yes | UTC timestamp: `YYYYMMDDTHHMMSSZ`. |
| `references` | no | HTTP(S) links supporting detection. |

`references` are maintainer metadata; they do not affect matching.

Descriptions should use `Detect <product or vendor>` and append a useful asset type
when it is not already evident; for example, `Detect F5 BIG-IP (load balancer)`.
Run `python3 tools/normalize-rule-descriptions.py` to apply this convention.

## Rule names

Every rule has a short lowercase slug (`a-z`, `0-9`, `-`), maximum 25 characters.
Generate names from filenames with `python3 tools/add-rule-names.py`; long filenames
are truncated to 25 characters. Names may be duplicated. The sanity checker requires
the field and validates its format.

## Rule UUIDs

Every rule has a unique, canonical UUID. It is opaque metadata and does not depend
on the filename; a random UUID4 is suitable for a new rule.

Run `python3 tools/add-rule-uuids.py` to populate missing UUIDs. It preserves existing
UUIDs and updates versions only for changed rules. The sanity checker rejects missing,
malformed, or duplicate UUIDs.

## Versions

Plum-Island replaces an existing database rule only when YAML version is newer. Update `version` whenever changing `description`, `query`, or `tags`.

## Tag names

Tags use normalized `<namespace>:<value>` values. Common namespaces:

- `vendor:*` — vendor, project, or organization.
- `product:*` — product, service, or device family.
- `type:*` — broad asset family, such as `firewall`, `router`, `cms`, or `vpn`.
- `proto:*` — protocol, such as `http`, `ssh`, or `ftp`.
- `vuln:*` — vulnerability-oriented classification.

Do not store `tag:` in a YAML tag: it belongs to the search field and Kvrocks key prefix. Do not add new `soft:*` or `hard:*` tags.

Favicon detections normally apply `product:*` and `vendor:*`; add `type:*` when the favicon identifies an asset family. Protocol-only detections should apply `proto:*` unless the signal identifies a specific product.

## Sources

- https://github.com/OWASP/www-project-secure-headers
- https://github.com/nmap/nmap/blob/9965fef7743c9f67dfe310b8e42c83cf170fa434/nselib/data/favicon-db
- https://github.com/sansatart/scrapts/blob/master/shodan-favicon-hashes.csv
