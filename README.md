# Plum-Antibodies

Plum-Antibodies contains the YAML rules used by
[Plum-Island](https://github.com/D4-project/Plum-Island) to detect and classify
services from scanner reports.

When a scan report is received, Plum-Island extracts technical fields such as
banners, HTTP titles, favicons, certificates, and protocols. The rules in this
repository search those fields for matches and add normalized tags such as
`product:nginx`, `vendor:cisco`, or `proto:ssh`.

Rules are stored as YAML files in [`tags/`](tags/). Each rule defines:

- a human-readable description;
- a search query;
- the tags to apply;
- a UTC version used during imports.

Exemple :

```yaml
description: HashiCorp Vault
query: http_favicon_mmhash:747250914 AND http_title.bg:Vault
tags:
- product:hashicorp-vault
- vendor:hashicorp
version: 20260428T170756Z
```

## Documentation

- [Tag rule guide](documentation/tagging.md)
- [Plum-Island search syntax](https://github.com/D4-project/Plum-Island/blob/main/documentation/search.md)
- [Import and reindex tools](https://github.com/D4-project/Plum-Island/blob/main/documentation/tools.md#tag-tools)
- [Plum-Island installation and submodule setup](https://github.com/D4-project/Plum-Island/blob/main/documentation/installation.md)

The `query` field uses Plum-Island's search syntax. Read its documentation
before creating a rule, especially for exact operators, `.bg`/`.begin`,
`.lk`/`.like`, `AND`, `OR`, and `NOT`.

## Utilisation comme sous-module

Plum-Island mounts this repository at `webapp/tags/`. The rules are therefore
available to the application under `webapp/tags/tags/`.

```bash
git clone --recurse-submodules https://github.com/D4-project/Plum-Island.git
```

To update the rules in an existing checkout:

```bash
git -C webapp/tags pull --ff-only origin main
```

After changing a rule, import the rules and reindex existing documents with the
Plum-Island tools.

## Sanity check

Run the checker from the root of this repository before committing rule
changes:

```bash
python3 tools/sanity-check.py
```

It loads every YAML rule, validates the required fields and version, checks
the allowed search fields and query syntax, and prints the tags that each rule
will apply on one line. It exits with a non-zero status when a warning is
found. The script requires PyYAML; the Plum-Island virtual environment already
provides it:

```bash
.venv/bin/python webapp/tags/tools/sanity-check.py
```
