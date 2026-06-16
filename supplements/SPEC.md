# ASB Supplements — community/expert deposition of supplementary grounding

**Problem.** ASB grounds skills/cards against a paper's full text (+ its code repo).
But the richest evidence often lives in **supplementary information (SI)** —
methods PDFs, parameter tables (xlsx/csv), protocols, extended data — and SI is
**not reliably collectable programmatically**:

- Unpaywall exposes only the OA PDF / landing page — **no SI field** (verified).
- Perspicacité can pull SI **only** from PMC-OA papers whose JATS XML marks
  `<supplementary-material>` (`pmc.py:get_supplementary_from_pmc`) — a minority.
- Everything else (paywalled SI, SI as separate files, publisher-specific layouts)
  has no automated path.

**Solution.** A community deposition layer: experts/users contribute SI — either by
**depositing an OA file** or by **providing a download link** — keyed to the paper
DOI. ASB ingests it into that paper's KB so it grounds the generated skills/cards.
This doubles as the expert-contribution path in the ASBB plan (§9.7 expert review):
the people who review tasks are exactly who can supply the SI that grounds them.

## Layout

```
supplements/
  <doi-slug>/                         # doi.lower(), [^a-z0-9]+ -> '-'
    manifest.yaml                     # the deposition record (REQUIRED)
    <files...>                        # OA-licensed deposited files (optional)
```

`<doi-slug>` example: `10.1038/s41467-022-32016-6` -> `10-1038-s41467-022-32016-6`.

## manifest.yaml schema (`asb-supplements/1.0`)

```yaml
schema: asb-supplements/1.0
doi: 10.1038/s41467-022-32016-6
title: Rivularia native-metabolomics screen      # human label (optional)
entries:
  - kind: si-pdf | si-table | protocol | extended-data | dataset-readme | repo-wiki | other
    # exactly ONE of `file` or `url`:
    file: methods_supplement.pdf                  # path relative to this dir (must be OA)
    url:  https://static-content.springer.com/...si.pdf   # download link (publisher SI etc.)
    label: Supplementary Methods
    license: cc-by | cc-by-nc | publisher-si | unknown    # license of the SI itself
    depositor_orcid: 0000-0001-6711-6719
    provenance: "journal SI tab, fetched 2026-06-16"
    sha256: <optional, for deposited files>
```

## License gate (CONTENT_POLICY.md §3/§4)

- **Deposited `file:`** is REDISTRIBUTED in this public repo → it MUST be
  OA/permissive (`cc-by`, `cc0`, `cc-by-sa`, `public-domain`). Non-OA files are
  rejected at validation; use a `url:` instead.
- **`url:`** (download link) is NOT redistribution — we only store the pointer +
  fetch at ingest time into the (private/local) KB. Any license is allowed for
  `url:`, but the license is recorded and a non-OA `url` ingests only into the
  Tier-2 private KB (never into the public skill text beyond fair-use paraphrase,
  enforced by the existing release_gate strip-verbatim caps).

## Ingest

`scripts/ingest_supplements.py <doi> --kb <asb-paper-slug>` reads the manifest,
resolves each entry (local file or `url` fetch), extracts text (PDF via parser;
csv/xlsx/txt directly), and ingests it into the paper's KB as labeled documents.
Re-runnable; keyed by sha256/url so it doesn't double-ingest.

## Contribution flow

PR-based: a contributor adds `supplements/<doi>/manifest.yaml` (+ OA files), CI
(`.github/workflows/verify-supplements.yml`) runs `scripts/validate_supplements.py`
(schema + license gate hard-fail; dead-link probe advisory), a maintainer merges.
See `CONTRIBUTING.md`.

## Files in this directory

- `SPEC.md` — this design.
- `CONTRIBUTING.md` — depositor-facing how-to + field reference.
- `_example/` — a valid template (`manifest.yaml` + a CC-BY `file:` + a `url:`);
  kept passing so CI stays green. Copy it to `supplements/<doi-slug>/` to start.
- `scripts/validate_supplements.py` (repo root `scripts/`) — schema + license gate
  + file-presence/sha256; `--check-links` probes urls.
- `scripts/ingest_supplements.py` — resolves each entry (local file / `url:` fetch),
  extracts text (pdf server-side; xlsx client-side; csv/txt/md/json as text),
  uploads to KB `asb-paper-<doi-slug>` via `POST /api/kb/<kb>/local-files`;
  idempotent via `<doi>/.ingested.json`.
