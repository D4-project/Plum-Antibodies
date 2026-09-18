# Sanity checker

Run the checker before committing rule changes. It validates every YAML rule, including required fields, unique UUID values, versions, query syntax, references, and normalized tags.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/sanity-check.py
```

It exits non-zero if any rule is invalid. Check per-rule output and exit status; warnings must be fixed.

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
