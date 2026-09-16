# AGENT.md

## Scope

This repository owns Plum Island's YAML detection and tag rules. The files in
`tags/` are consumed by Plum Island through the Git submodule mounted at
`webapp/tags/`, so the effective application path is `webapp/tags/tags/`.

The importer and runtime tag engine live in the Plum-Island repository. Keep
changes here focused on rule content, naming, queries, and versions. The
operational import and reindex commands are documented in
`documentation/tagging.md`.

Install runtime dependencies with `pip install -r requirements.txt`. Use
`pip install -r requirements-dev.txt` when working on validation or repository
maintenance tooling.

## Code quality

Keep code changes regression-free. Before committing Python changes, run the
relevant tests and the following checks from the repository root:

```bash
.venv/bin/python -m black tools
.venv/bin/python -m py_compile tools/sanity-check.py
PYLINTHOME=/tmp/pylint .venv/bin/python -m pylint tools
```

Do not introduce new Black or Pylint violations. Preserve existing behavior
unless a rule or validation change explicitly requires a behavior change, and
document that change in the commit and relevant documentation.

Every public function and every non-trivial helper must have an English
docstring describing its purpose, inputs, outputs, and important validation or
failure behavior. Keep comments focused on intent and invariants rather than
restating the code.

Keep each source file below 1000 lines. Split new functionality into focused
modules before a file reaches that limit; do not create a large catch-all
module to avoid making the split.

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

## Plum-Island search contract

The source of truth for rule-query parsing is
`Plum-Island/webapp/app/views.py:KVSearchView.parse_query()` and its
`parse_query_group()` helper. Do not introduce a field or operator here unless
the Plum-Island parser, tag-rule evaluator, and search documentation support it
as well.

The currently allowed rule fields are:

- `ip`, `net`, `port`;
- `fqdn`, `fqdn_requested`, `host`, `domain`, `domain_requested`, `tld`;
- `tag`;
- `http_title`, `http_favicon_path`, `http_favicon_mmhash`,
  `http_favicon_md5`, `http_favicon_sha256`;
- `http_cookiename`, `http_etag`, `http_header`, `http_headval`, `http_server`;
- `x509_issuer`, `x509_issuer_cn`, `x509_md5`, `x509_sha1`, `x509_sha256`,
  `x509_subject`, `x509_subject_cn`, `x509_san`;
- `banner`.

Supported value modifiers are `.lk`/`.like` for substring matching,
`.bg`/`.begin` for prefix matching, and `.not`/`.nt` for exact negation. The
`tag` field is exact-only. The special `http_headval` form is
`http_headval:header:value`, with optional `.lk`, `.like`, `.bg`, or `.begin`
on the header expression.

Queries use `field:value` terms, implicit `AND` within a group, and explicit
`OR` between groups. Quoted values are supported. Standalone `NOT` must be
followed by a field term, and every OR group containing `NOT` must also contain
at least one positive term. Do not use `.not` or `.nt` as the operand of a
standalone `NOT`.

Raw scanner documents and Meilisearch documents do not contain computed tags.
Tags are derived from active rules while parsed documents are indexed into
Kvrocks. A rule must not rely on tags produced by another rule, and rules must
not introduce a fallback that merges pre-existing document tags.

When a new scanner field becomes available, the corresponding Plum-Island
parser output, Kvrocks keyword list, query parser allow-list, and search
documentation must be updated together before a rule uses that field.

## Change workflow

For a detection-only YAML change:

1. edit only the relevant file under `tags/`;
2. update its UTC `version`;
3. run `tools/sanity-check.py` and fix every warning;
4. update Plum-Island's `release_note.md` when the change is user-visible;
5. commit and push Plum-Antibodies;
6. update the Plum-Island submodule pointer when the application should use it.

Use `tools/sanity-check.py --type` when reviewing asset-family coverage. It
prints each rule's `type:*` tags and a unique sorted summary at the end.

Do not add automated tests for detection-only rule changes. Add or update
tests in Plum-Island when parser, indexer, query, or tag-engine behavior
changes. After importing changed rules, reindex existing documents when
historical results must receive the new tags.

Before committing changes to a rule, run the sanity checker and inspect both
its per-rule output and its exit status. Do not treat a warning as harmless:
the checker is intended to catch malformed YAML, unsupported search syntax,
missing versions, and tags that cannot be imported safely.
