# Local build-capsule records

`scripts/pack_capsules.py` turns a released paper view or a plain builds root
into a deterministic, local archive set. It performs no network operation,
deposit, upload, or collection-record change.

```sh
python scripts/pack_capsules.py \
  --view <paper-view-or-builds-root> \
  --collection <released-collection-root> \
  --out <local-output-directory> \
  --date YYYY-MM-DD \
  --access-records <same-doi-access.json> \
  --strict
```

Use `--limit N` for the first N builds in sorted order, `--with-indicium` to
add build knowledge graphs, and `--deny-patterns-file` for runtime-only
literal, case-insensitive strings. Deny strings are never printed or written
to receipts. The release date and tooling commit are explicit receipt values;
importable code never reads the clock.

## Archive layout

- `builds/<build-slug>.zip`: one sorted, fixed-timestamp archive per passing
  build. It contains the slim-plus capsule set, build ledger and manifests.
- `MANIFEST.json`: `asb-capsules-manifest/1`, including source digests, archive
  sizes and hashes, access, validation, evaluation and per-build screen data.
- `capsules.jsonl`: one row per capsule. A Parquet copy is optional only when
  `pyarrow` is already installed.
- `SCREEN.json`: `asb-capsules-screen/1`, with totals and per-build failures.
- `benchmark-manifest.json`: the complete operational-evaluation subset,
  without a second payload copy.
- `zenodo/metadata.json` and `hf/README.md`: local record descriptions.

## Screen order

Every staged JSON, JSONL, JSON-LD, Markdown, YAML and plain-text member is
screened before zipping. Quoted text follows one of three regimes, recorded
per build as `quote_retention` in `MANIFEST.json` and `SCREEN.json`. Open
sources under a permissive licence (the CC-BY family, CC0, public domain, or
an explicit reuse grant) keep their attributed text in full (`full`). Open
sources under any other licence string keep structured quote fields and
evidence blockquotes under 300 characters per field and 1,500 retained
characters per DOI (`capped`). Restricted, unresolved, licence-less, and
ungranted-preprint sources drop quote text and retain a DOI, location,
offsets, original length, digest and reason (`dropped`). Emails and phone-shaped values then use the release-gate rules.
Build-machine paths become build locators and RO-Crates use the canonical
release pruning rule. The optional deny list runs last.

Residual sensitive content or a deny hit is a build failure. In advisory mode
the failing build is omitted while receipts remain. `--strict` returns
non-zero and removes all generated build archives on any failure, while
retaining the receipts for diagnosis.

The generated metadata links only the collection's Zenodo DOI, the public
pipeline repository and this tooling repository. A capsules DOI placeholder
remains until the owner publishes the record. No existing collection record is
modified.
