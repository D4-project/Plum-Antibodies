# AGENT.md

## Scope

This repository owns Plum Island's YAML detection and tag rules. The files in
`tags/` are consumed by Plum Island through the Git submodule mounted at
`webapp/tags/`, so the effective application path is `webapp/tags/tags/`.

The importer and runtime tag engine live in the Plum-Island repository. Keep
changes here focused on rule content, naming, queries, and versions. The
operational import and reindex commands are documented in
`documentation/tagging.md`.

## Documentation language

All repository documentation, comments intended for maintainers, commit-facing
examples, and new explanatory text must be written in English. Keep code
identifiers, YAML values, and product names unchanged when they are part of a
technical contract.

## YAML rule contract

Each rule contains:

- `description`: human-readable rule description;
- `query`: structured Plum Island search query;
- `tags`: one or more normalized `<namespace>:<value>` tag values;
- `version`: recommended UTC timestamp in `YYYYMMDDTHHMMSSZ` format.

When changing an existing rule's `description`, `query`, or `tags`, update its
`version`. Plum Island only replaces an existing SQLite rule when the YAML
version is newer than the stored rule timestamp.

Do not prefix YAML values with `tag:`. That prefix belongs to the search field
and Kvrocks index keys. Use namespaces such as `vendor:*`, `product:*`,
`type:*`, `proto:*`, and `vuln:*`; do not add new `soft:*` or `hard:*` values.

Prefer exact query terms, then `.bg`/`.begin`, then `.lk`/`.like` when the
required matching semantics allow it. Tag rules must use the same structured
query syntax as Plum Island search. Standalone `NOT` requires a positive term
in each OR group, and rules must not depend on computed tags from other rules.

## Change workflow

For a detection-only YAML change:

1. edit only the relevant file under `tags/`;
2. update its UTC `version`;
3. update the release notes when the change is user-visible;
4. commit and push Plum-Antibodies;
5. update the Plum-Island submodule pointer when the application should use it.

Do not add automated tests for detection-only rule changes. Add or update
tests in Plum-Island when parser, indexer, query, or tag-engine behavior
changes. After importing changed rules, reindex existing documents when
historical results must receive the new tags.
