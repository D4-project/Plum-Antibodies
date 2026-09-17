# Tag validation library

This repository provides the Python validator used by Plum-Island and the sanity checker. Install it from a checkout:

```bash
python3 -m pip install -e .
```

```python
from plum_antibodies import TagValidationError, validate_tag, validate_tags

tag = validate_tag("Product:Nginx")
# "product:nginx"

tags = validate_tags(["proto:http", "type:web-server"])

try:
    validate_tag("product:bad tag")
except TagValidationError as error:
    print(error)
```

The validator normalizes case, accepts legacy `tag:namespace:value` input, and rejects whitespace and invalid namespaces or values. `validate_tags()` rejects an empty collection and removes duplicates after normalization. Internal document processing can use `allow_empty=True` when a scan has no tags.
