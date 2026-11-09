# Per-domain rules

The tooling reads deterministic, domain-specific vocabulary from
`scripts/rules/<domain>/`, where `<domain>` is the `domain` or `slug` in the
collection's `collection.yaml`.

- `technique_rules.yaml` defines technique tags and their field-aware regular
  expressions for `tag_techniques.py`. `build_packs.py` requires the same file
  when it resolves a collection, although pack membership uses the tags already
  present in the index.
- `edam_remap_rules.yaml` defines the foreign text pattern, foreign tools and
  T3b/T4 operation removals for `remap_edam.py`. T1 and T2 are generic and do
  not load this file.
- `release_surface_rules.yaml` defines foreign release identifiers merged with
  the global retracted phrases by `check_release_surface.py`. It is optional;
  an absent file contributes no identifiers.

Each file carries `rules_version`. Increment it whenever its vocabulary or
rules change so receipts and reviews identify the exact rule revision.

To add a domain, create `scripts/rules/<domain>/`, copy the three metabolomics
files, replace the vocabulary and identifiers, and set new `rules_version`
values. Preview tagging before writing:

```bash
python scripts/tag_techniques.py \
  --collection <domain checkout>/collections/<domain>/<version> \
  --report <evidence>/technique-tags.json
```

Every command accepts `--rules` for an explicit override. Technique tagging and
EDAM T3 through T4 fail with the expected path when their required domain file
is absent. There is no deprecated `scripts/technique_rules.yaml` fallback.
