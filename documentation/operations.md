# Plum-Island operations

Plum-Island mounts this repository at `webapp/tags/`. Clone Plum-Island with submodules:

```bash
git clone --recurse-submodules https://github.com/D4-project/Plum-Island.git
```

Update this repository in an existing Plum-Island checkout:

```bash
git -C webapp/tags pull --ff-only origin main
```

Import and reindex commands run from the root of a Plum-Island checkout:

```bash
.venv/bin/python tools/tag_mgmt.py import --all
.venv/bin/python tools/tag_mgmt.py reindex --allrules
```

Import one rule with `--tags-file webapp/tags/tags/<rule>.yaml`, or preview an import with `--all --dry-run`. Use [Plum-Island tag-tools documentation](https://github.com/D4-project/Plum-Island/blob/main/documentation/tools.md#tag-tools) for complete import, delete, rollback, and reindex procedures.

## Retired rules

Deleting a YAML file does not remove an already imported SQLite rule. Remove
the retired rule with `tools/tag_mgmt.py delete --id <database-rule-id>` or
`delete --tags-file <archived-yaml>`, then import its replacement and reindex.
The database rule ID is distinct from the stable UUID below.

| Retired YAML | Retired UUID | Replacement |
| --- | --- | --- |
| `dokuwiki-0-0-20080505.yaml` | `95d71f4a-e3d0-5330-807d-1d8bdaf7ed64` | `dokuwiki.yaml` (`2aed88a9-663d-50e6-ae3a-019ba035b718`) |
| `mantis-bug-tracker-1-1-2-bugs-images-favicon-ico.yaml` | `510060d8-5281-5920-8130-e4165b91cd32` | `mantis-bug-tracker-1-2-9-1-2-15.yaml` (`00ab3fbc-4f83-5f3e-ba2c-1dca5431db01`) |
| `drupal-2-x-4-x.yaml` | `4af8d5ad-f8ef-5189-ae4f-acf64c21f5a4` | `drupal.yaml` (`85483dc3-fd56-5443-9ca9-e4388dff6152`) |
| `drupal-7-x.yaml` | `b5a4448b-1e16-5d19-b358-06f5991d572b` | `drupal.yaml` (`85483dc3-fd56-5443-9ca9-e4388dff6152`) |
| `drupal-cms_e6a9dc66.yaml` | `b0f43bde-df6b-56e4-92e6-5812924506a4` | `drupal.yaml` (`85483dc3-fd56-5443-9ca9-e4388dff6152`) |

The retired DokuWiki fingerprint is also present in the official 2020 release
and cannot identify the 2008 version. Retiring the imported rule and reindexing
removes that unsupported version attribution from historical documents.

The MantisBT replacement preserves both historical favicon families under the
generic `product:mantisbt` tag. The favicon previously attributed to releases
1.2.9–1.2.15 is still shipped by current upstream and cannot establish those
versions. Remove the retired imported rule, import the updated primary rule,
and reindex to replace the old product and vendor tags. The primary filename
remains unchanged for compatibility; its name and description are generic.

The Drupal replacement preserves every predicate from the three retired rules
under `product:drupal`. Favicon fingerprints alone do not establish the old
release labels or the newer Drupal CMS distribution. Remove all three retired
imported rules, import `drupal.yaml`, and reindex to replace their historical
product tags. The separate Drupal Commerce rule remains active.
