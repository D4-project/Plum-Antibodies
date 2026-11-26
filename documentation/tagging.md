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

## Web server classification

Rules that identify an HTTP server implementation carry `type:webserver` and
one canonical `product:*` tag. CMS, CDN, and proxy rules do not gain this type
solely because they answer over HTTP. Plum Island can read active imported rule
rows to derive the web-server product catalogue without a hard-coded product
list. A scan document may still have several `type:*` and `product:*` tags from
different matching rules; downstream rankings must intersect observed products
with this rule-derived catalogue rather than treating every product on a
`type:webserver` port as a web server.

## Retiring and consolidating rules

Preserve the retained rule's UUID, combine equivalent signatures with `OR`, and
increase its version. Record removed UUIDs and their replacement so existing
installations can retire the correct SQL definitions. Rule UUIDs identify rules;
scan UIDs identify captures and must not be deleted as part of rule cleanup.

The current Plum-Island importer inserts or updates YAML rules by UUID but does
not retire SQL rows merely because their files disappeared. A Git update or an
ordinary full import therefore does not, by itself, remove those old producers.
Source-aware automatic retirement, preservation of manual rules and migration of
existing installations are tracked in
[Plum-Island #282](https://github.com/D4-project/Plum-Island/issues/282).
The machine-readable [retirement register](../retired_rules.yaml) records each
removed rule's exact YAML `name`, canonical `uuid` and replacement UUID in
`replaced_by`. UUID is the identity; names are descriptive and may repeat. The
register includes the Jira retirements below and subsequent consolidations.
It is migration metadata until the source-aware importer in #282 consumes it;
publishing this file does not itself delete SQL rules.

Once a producer is removed or deactivated in SQL, the current scheduler-supervised
reconciliation engine recomputes its contributions and publishes the updated tag
indexes. Tags still produced by another active rule survive. Catalogue candidates
with no remaining indexed captures are filtered from display; per-worker caches
may retain the previous display for up to 60 seconds. This requires the automatic
reconciliation scheduler to be enabled, running and able to complete its work.
See Plum-Island's
[automatic indexing](https://github.com/D4-project/Plum-Island/blob/main/documentation/automatic-indexing.md)
and [tag management](https://github.com/D4-project/Plum-Island/blob/main/documentation/tools.md#tag_mgmtpy)
documentation for operational status and existing deletion commands. Repository
maintenance does not execute production SQL changes or index cleanup.

### Jira consolidation, 2026-11-18

Retained rule: `tags/jira.yaml`, UUID
`bb9e4d87-89a3-5e73-856d-8202171d9b4b`. It contains all five previous favicon
predicates and produces `product:jira`, `vendor:atlassian`, `type:issue-tracker`,
`lang:java` and `proto:http`.

| Removed definition | Retired rule UUID | Obsolete unique tag |
| --- | --- | --- |
| `atlassian-jira.yaml` | `bb226460-8e5c-52ad-a2e0-ddd9de8425f4` | `product:atlassian-jira` |
| `atlassian-jira-bug-tracker.yaml` | `89aa48b6-dd2f-56cf-972e-7195948616a3` | `product:atlassian-jira-bug-tracker` |

Updating the retained rule also replaces its previous `vendor:jira` contribution.
Existing installations need the retained definition imported and the two retired
SQL producers removed or deactivated before reconciliation can eliminate all
three obsolete tag values. Preserve unrelated manual rules and shared tags.

### Elasticsearch consolidation, 2026-11-18

Retained rule: `tags/elasticsearch.yaml`, UUID
`39de06b7-6eb7-5e07-8be9-b0ac4a1bac89`. Both favicon predicates from the retired
rule are preserved as `OR` alternatives alongside the HTTP product header and
HTTP CA issuer. Their bytes were verified against official Elasticsearch assets.
The canonical tags are `product:elasticsearch`, `vendor:elastic`, `lang:java`,
`type:search-engine` and `proto:http`.

| Removed rule name | Removed definition | Retired rule UUID | Obsolete unique tag |
| --- | --- | --- | --- |
| `elastic-database` | `elastic-database.yaml` | `6e569407-9ed6-501c-8660-aefee60f2136` | `product:elastic-database` |

The same identity/replacement mapping is maintained in `retired_rules.yaml`.
Existing installations need the retained definition imported and the retired SQL
producer removed or deactivated before reconciliation can eliminate the old
product tag. Shared `vendor:elastic` contributions must survive.

## Tag names

Tags use normalized `<namespace>:<value>` values. Common namespaces:

- `vendor:*` — vendor, project, or organization.
- `product:*` — product, service, or device family.
- `type:*` — broad asset family, such as `firewall`, `router`, `cms`, or `vpn`.
- `proto:*` — protocol, such as `http`, `ssh`, or `ftp`.
- `lang:*` — language associated with the identified technology, such as `java` or `php`.
- `vuln:*` — vulnerability-oriented classification.

Do not store `tag:` in a YAML tag: it belongs to the search field and Kvrocks key prefix. Do not add new `soft:*` or `hard:*` tags.

Favicon detections normally apply `product:*` and `vendor:*`; add `type:*` when the favicon identifies an asset family. Protocol-only detections should apply `proto:*` unless the signal identifies a specific product.

Language classification has the same evidence limitations as the detection that
produces it. A favicon associated with Java documentation or a Java library can
classify that technology as `lang:java`, but does not establish a running JVM,
the implementation language of the HTTP server serving the asset, or an installed
Java version. In particular, the historical Ant/POI and SwarmCache favicon rules
identify associated artifacts; their legacy release labels are not independently
verified by the icon. Their official project references establish the technology's
language, while the historical favicon database records the existing attribution.
For runtime investigations, inspect the matched predicate and corroborate artifact
matches with servlet headers or other application-specific runtime evidence.

## Sources

- https://github.com/OWASP/www-project-secure-headers
- https://github.com/nmap/nmap/blob/9965fef7743c9f67dfe310b8e42c83cf170fa434/nselib/data/favicon-db
- https://github.com/sansatart/scrapts/blob/master/shodan-favicon-hashes.csv
