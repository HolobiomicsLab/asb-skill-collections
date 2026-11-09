# EDAM labels

`edam_labels.json` contains the EDAM topic and operation terms used by
`scripts/build_facets.py`: identifier, preferred label, synonyms and parents.
The table records its source file, generation date, EDAM release and the
`CC-BY-SA-4.0` licence of the ontology. Retain that attribution when copying or
publishing the derived table.

The current table was derived offline from `EDAM.csv` on 2026-11-08. The CSV has
no ontology release row, so the refresh command infers release `1.25` from the
highest numeric value in its `Created in` column. Check that convention against
the release metadata when replacing the CSV, and pass the actual generation
date explicitly.

From the tooling repository root, refresh it from a locally obtained EDAM CSV:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_facets.py refresh-labels \
  --csv /path/to/EDAM.csv \
  --out scripts/data/edam_labels.json \
  --date YYYY-MM-DD
```

No download is part of the refresh. Inspect the resulting labels and diff
before using them to name facets.

`edam_vocabulary.json` is the separate four-branch resolution table used by
`scripts/remap_edam.py` and `scripts/domain_content_gates.py`. Generate it with
`scripts/edam_vocabulary.py refresh` from a local CSV and an explicit date. It
records the source digest, obsolete status, replacement identifiers, and the
same inferred release convention and CC-BY-SA-4.0 attribution as the label
table. Refreshing this file does not change `edam_labels.json`.
