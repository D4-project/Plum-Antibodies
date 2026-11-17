# Sanity checker

Run the checker before committing rule changes. It validates every YAML rule, including required short names, unique UUID values, versions, query syntax, references, and normalized tags.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/sanity-check.py
```

It exits non-zero if any rule is invalid. Check per-rule output and exit status; warnings must be fixed.

Query validation distinguishes quoted literal parentheses from runtime grouping
syntax. Values such as `banner.lk:"(Debian)"`, `http_title.lk:"phpinfo()"` and
`http_server.lk:"(Win64)"` must be quoted. Their unquoted forms fail validation
with the affected filename and a quoting hint, and the command exits with code
1. Valid one-level groups, including sibling groups, remain supported; empty,
nested and unbalanced groups are rejected. See [query syntax](query-syntax.md).

Use development dependencies for tooling work:

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
```

From a Plum-Island checkout, run the submodule copy with its virtual environment:

```bash
.venv/bin/python webapp/tags/tools/sanity-check.py
```

## Coverage summaries

Print every rule's asset-family tags and a sorted unique summary:

```bash
.venv/bin/python tools/sanity-check.py --type
```

Use `--proto` for protocol tags; options can combine:

```bash
.venv/bin/python tools/sanity-check.py --type --proto
```

Run library tests with:

```bash
.venv/bin/python -m pytest tests/
```
