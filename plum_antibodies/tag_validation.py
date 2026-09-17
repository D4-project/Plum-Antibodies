"""Canonical syntax validation for Plum-Island tag values."""

import re

TAG_RE = re.compile(r"^[a-z][a-z0-9_-]*:[a-z0-9!._:/-]*$")


class TagValidationError(ValueError):
    """Raised when a tag cannot be normalized to a valid stored tag value."""


def validate_tag(raw_tag):
    """Return one normalized tag or raise ``TagValidationError``.

    ``raw_tag`` must be a string containing ``namespace:value``. Input is
    stripped and lowercased; legacy ``tag:namespace:value`` values are reduced
    to their stored form. Namespaces begin with a letter. Values begin with an
    alphanumeric character and may contain letters, digits, ``!``, ``.``,
    ``_``, ``-``, ``/``, and additional ``:`` separators (for example
    ``cpe:cisco:ios``).
    """
    if not isinstance(raw_tag, str):
        raise TagValidationError("every tag must be a string")

    tag = raw_tag.strip().lower()
    while tag.startswith("tag:") and tag.count(":") >= 2:
        tag = tag.split(":", 1)[1].strip()
    if not TAG_RE.fullmatch(tag):
        raise TagValidationError(
            "tag must use namespace:value syntax with no whitespace"
        )
    return tag


def validate_tags(raw_tags, *, allow_empty=False):
    """Return normalized unique tags or raise ``TagValidationError``.

    ``raw_tags`` accepts a string or an iterable of tag strings. At least one
    tag is required by default; set ``allow_empty`` for document-tag collection
    paths where an empty result is valid. Duplicate tags after normalization
    are collapsed while retaining their first occurrence.
    """
    if raw_tags is None and allow_empty:
        return []
    if isinstance(raw_tags, str):
        raw_tags = [raw_tags]
    if isinstance(raw_tags, dict):
        raise TagValidationError("tags must be a non-empty list of tag strings")

    try:
        raw_tags = list(raw_tags)
    except TypeError as error:
        raise TagValidationError(
            "tags must be a non-empty list of tag strings"
        ) from error
    if not raw_tags:
        if allow_empty:
            return []
        raise TagValidationError("tags must be a non-empty list of tag strings")

    tags = []
    seen = set()
    for raw_tag in raw_tags:
        tag = validate_tag(raw_tag)
        if tag in seen:
            continue
        seen.add(tag)
        tags.append(tag)
    return tags
