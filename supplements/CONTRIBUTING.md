# Contributing supplementary information (SI)

ASB grounds skills/cards against a paper's text + its code repo, but the richest
evidence often lives in **supplementary information** — methods PDFs, parameter
tables, protocols, extended data — which is **not reliably collectable
programmatically** (Unpaywall has no SI field; only PMC-OA papers expose SI in
JATS). This directory lets experts/users deposit SI, keyed to a paper DOI, so
ASB can ingest it. See [`SPEC.md`](SPEC.md) for the full design.

## How to deposit (PR-based)

1. **Make a directory** named after the DOI slug — lowercase the DOI and replace
   every run of non-`[a-z0-9]` with `-`:

   ```
   10.1038/s41467-022-32016-6  ->  supplements/10-1038-s41467-022-32016-6/
   ```

2. **Write `manifest.yaml`** (schema `asb-supplements/1.0`). Each entry is either
   a **deposited file** or a **download link** — never both:

   ```yaml
   schema: asb-supplements/1.0
   doi: 10.1038/s41467-022-32016-6
   title: Rivularia native-metabolomics screen
   entries:
     - kind: si-table                       # si-pdf | si-table | protocol | extended-data | dataset-readme | repo-wiki | other
       file: supplementary_table_1.csv      # path relative to this dir (REDISTRIBUTED -> must be OA)
       label: Supplementary Table 1 — feature parameters
       license: cc-by                       # cc-by | cc-by-sa | cc0 | public-domain  (OA required for file:)
       depositor_orcid: 0000-0001-6711-6719
       provenance: "journal SI tab, fetched 2026-06-16"
     - kind: si-pdf
       url: https://static-content.springer.com/.../MOESM1_ESM.pdf   # POINTER only -> any license
       label: Supplementary Methods
       license: publisher-si
       depositor_orcid: 0000-0001-6711-6719
       provenance: "publisher SI, not redistributable"
   ```

3. **`file:` vs `url:` — the license gate** (`CONTENT_POLICY.md` §3/§4):
   - A **`file:`** is committed to this public repo, i.e. *redistributed*, so its
     `license` MUST be OA/permissive: `cc-by`, `cc-by-sa`, `cc0`,
     `public-domain`. Non-OA files are **rejected**.
   - A **`url:`** is only a pointer (no redistribution), so **any** license is
     allowed. A non-OA `url` is fetched at ingest time into the **private/local
     KB only** (Tier-2); it never enters public skill text beyond the fair-use
     paraphrase the release gate already enforces.
   - When in doubt, or if the publisher prohibits redistribution, use a `url:`.

4. **Validate locally** before opening the PR:

   ```bash
   python scripts/validate_supplements.py supplements/<doi-slug>      # schema + license + file/sha256
   python scripts/validate_supplements.py --check-links               # also probe url: entries
   ```

5. **Open a PR.** CI runs `validate_supplements.py` (schema + license gate +
   dead-link check). A maintainer reviews and merges.

## What happens after merge

A maintainer (or a scheduled job) runs:

```bash
python scripts/ingest_supplements.py supplements/<doi-slug>     # -> KB asb-paper-<doi-slug>
```

which resolves each entry (local file, or `url:` fetch), extracts text (PDF via
the server parser; csv/xlsx/txt directly), and ingests it into the paper's KB so
it grounds that paper's skills/cards on the next build/re-validation. Ingest is
idempotent (recorded in `<doi>/.ingested.json`).

## Field reference

| field             | required | notes |
|-------------------|----------|-------|
| `kind`            | yes      | one of `si-pdf, si-table, protocol, extended-data, dataset-readme, repo-wiki, other` |
| `file` **or** `url` | yes (exactly one) | `file` = path in this dir (OA only); `url` = http(s) download link (any license) |
| `label`           | yes      | human label; becomes the ingested document title |
| `license`         | yes      | SI's own license; OA set required for `file:` |
| `depositor_orcid` | yes      | your ORCID (accountability/provenance) |
| `provenance`      | recommended | where/when you obtained it |
| `sha256`          | optional | for `file:` entries; verified at validation |

Accepted file types for ingest: `.pdf` (text extracted server-side), `.xlsx`/
`.xls` (flattened client-side), `.csv`/`.tsv`/`.txt`/`.md`/`.json`/`.rst`/
`.html` (ingested as text). Other binaries are skipped — convert to one of these.
