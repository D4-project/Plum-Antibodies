# Plum-Antibodies

Plum-Antibodies is a collection of YAML detection rules used by [Plum-Island](https://github.com/D4-project/Plum-Island). It identifies services from scanner data—HTTP headers, favicon hashes, banners, and certificates—and applies normalized tags such as `product:nginx`, `vendor:cisco`, and `proto:ssh`.

Rules live in [`tags/`](tags/). Plum-Island consumes this repository as the `webapp/tags/` submodule.

## Documentation

- [Writing tag rules](documentation/tagging.md)
- [Query syntax](documentation/query-syntax.md)
- [Sanity checker](documentation/sanity-check.md)
- [Plum-Island operations](documentation/operations.md)
- [Tag validation library](documentation/tag-validation.md)
