# Writing tag rules

Plum-Island applies computed tags to scan documents through rules maintained in this repository. A rule matches scanner fields and writes its tags to the document index.

Rules are YAML files in `tags/`; each filename is its rule name.

```yaml
description: HashiCorp Vault
query: http_favicon_mmhash:747250914 AND http_title.bg:Vault
tags:
- product:hashicorp-vault
- vendor:hashicorp
version: 20260428T170756Z
```

| Field | Required | Description |
| ----- | -------- | ----------- |
| `description` | yes | Human-readable rule description. |
| `query` | yes | Query using documented [syntax](query-syntax.md). |
| `tags` | yes | One or more normalized tags. |
| `version` | yes | UTC timestamp: `YYYYMMDDTHHMMSSZ`. |
| `references` | no | HTTP(S) links supporting detection. |

`references` are maintainer metadata; they do not affect matching.

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
