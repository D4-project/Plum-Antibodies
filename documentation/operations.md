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
