# Query syntax

`query` uses Plum-Island search syntax. See [Plum-Island search documentation](https://github.com/D4-project/Plum-Island/blob/main/documentation/search.md) for the complete runtime contract.

## Terms and groups

Terms use `field:value`. Terms in one group are implicitly joined with `AND`; use `OR` to start another group.

```text
http_favicon_mmhash:747250914 AND http_title.bg:Vault
http_server.bg:"Apache/" OR banner.lk:"OpenSSH"
```

Use quotes for values containing spaces. Every `OR` group must contain a positive term.

## Value matching

- Rule matching is case-insensitive: query values and indexed field values are
  normalized to lowercase before comparison.
- Exact matching has no modifier and is fastest.
- `.bg` or `.begin` matches from the beginning of a value.
- `.lk` or `.like` matches anywhere in a value.

Use the least expensive form preserving required semantics. `http_server.bg:"Apache/"` matches a banner prefix; `http_server.lk:"(Debian)"` matches a marker later in a banner.

`http_title` contains the scanner's complete `http-title.output`. It can include
a newline followed by `Requested resource was ...` after the page title.
Use `.bg` for a distinctive title when this redirect suffix is possible;
an exact match would fail. A distinctive application path in that output can
also be matched with `.lk`.

## Negation

Use standalone `NOT` before a term:

```text
port:443 AND NOT http_server.lk:apache
```

An absent excluded value passes. Do not use computed tags as rule dependencies: tagging happens while documents are indexed, so a rule cannot consume tags from another rule.

## HTTP headers

`http_header:<name>` tests header presence. Use `http_headval:<header>:<value>` for a header value, for example:

```text
http_headval:x-powered-by.lk:plesklin
```

Active rules automatically enable collection of exact header names they use,
including names absent from the current header catalogue. `http_header` enables
presence collection; `http_headval` also enables value collection. A missing
catalogue entry alone does not require a parser change or rule rejection.

Rule import reconciles these dependencies through
`analyze_header_dependencies()` and `ensure_rule_required_headers()` in
Plum-Island. The scheduler also reconciles them when exporting parser
configuration. Import the rules and reindex existing scans to apply the new
collection settings to historical documents; see
[Plum-Island operations](operations.md).
