---
name: tsv-file-io-and-formatting
description: Use when you have computed or received a precomputed expected contact frequency table (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0654
  tools:
  - cooler
  - cooltools
  - black
  - Python
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cooltools
    doi: 10.1371/journal.pcbi.1012067
    title: cooltools
  dedup_kept_from: coll_cooltools
schema_version: 0.2.0
---

# TSV file I/O and formatting

## Summary

Load, validate, and save tabular genomic data (e.g., precomputed expected contact frequency tables) as tab-separated values with proper column headers and numeric precision. This skill ensures reproducible interchange of Hi-C-derived frequency tables and their smoothed derivatives across cooltools analysis pipelines.

## When to use

You have computed or received a precomputed expected contact frequency table (e.g., from cooler-derived datasets) with columns such as dist_bp, contact_frequency, and n_valid, and need to persist it in a human-readable, column-labeled format suitable for downstream smoothing operations like logbin_expected, or you have generated a log-binned and smoothed P(s) table and must serialize it for sharing or archival.

## When NOT to use

- Raw Hi-C contact matrix is still in cooler HDF5 format and has not yet been aggregated into expected frequency profile — use cooler's native API instead.
- Data is already stored in a compressed binary format (e.g., .h5, .npz) optimized for performance and you do not need human readability or column-level schema inspection.
- The workflow requires streaming or incremental I/O on datasets too large to fit in memory — TSV parsing via standard Python I/O is not designed for chunked processing.

## Inputs

- TSV file with columns: dist_bp (genomic distance in base pairs), contact_frequency (observed or expected contact probability), n_valid (count of valid bin pairs or normalization factor)
- Python dict or pandas DataFrame with contact frequency data
- Expected contact frequency table from cooler-derived dataset deposit

## Outputs

- TSV file with log-binned distance (dist_bp), mean smoothed contact frequency (count.avg.smoothed), and bin statistics
- Validated and serialized P(s) table with proper column headers and numeric precision
- Human-readable tabular file suitable for downstream Hi-C analysis or archival

## How to apply

Load a TSV file containing precomputed expected contact frequencies using Python's standard file I/O or pandas, ensuring column names (e.g., dist_bp, contact_frequency, n_valid) are present in the header row. After processing (e.g., applying logbin_expected smoothing), write the output as a TSV with explicit column headers, maintaining numeric precision for distance and frequency values. Use Python tooling like black or autopep8 to ensure consistent code style when writing file-handling code. Validate that the saved TSV preserves the original data types and row order, and that all rows are present with no silent truncation.

## Related tools

- **cooler** (Source of precomputed expected contact frequency tables; provides the HDF5 cooler format from which TSV expected tables are exported) — https://github.com/open2c/cooler
- **cooltools** (Applies logbin_expected smoothing function to the loaded TSV expected table and generates output TSV with binned and smoothed P(s)) — https://github.com/open2c/cooltools
- **black** (Code formatter used during development to ensure consistent and readable style in file I/O code) — https://github.com/psf/black
- **Python** (Primary language for reading, validating, and writing TSV files using built-in I/O or pandas)

## Examples

```
import pandas as pd; expected = pd.read_csv('expected_cis.tsv', sep='\t'); smoothed = cooltools.logbin_expected(expected); smoothed.to_csv('expected_cis_logbin.tsv', sep='\t', index=False, float_format='%.10g')
```

## Evaluation signals

- TSV file is readable as plain text and contains exactly the expected column headers (dist_bp, contact_frequency, n_valid, or post-processing: dist_bp, count.avg.smoothed, etc.) on the first row.
- All data rows are present with no truncation; row count after loading and saving matches the original.
- Numeric columns (distance, frequency) maintain sufficient precision (floating-point representation is consistent; no unexpected rounding or scientific notation artifacts that break downstream parsing).
- File can be successfully round-tripped: load TSV → apply operation → save TSV → load again, producing identical or near-identical values (accounting for floating-point tolerance).
- Tab-delimited format is verified by confirming that each row contains the correct number of fields separated by single tab characters (no spaces as delimiters, no extra whitespace).

## Limitations

- The API for smoothing P(s) and its derivatives in cooltools is not yet stable; TSV schema and column names may change in future releases, potentially breaking compatibility.
- TSV format is human-readable but inefficient for very large frequency tables; for multi-gigabyte datasets, binary formats (HDF5, Parquet) may be preferable for memory and I/O performance.
- No built-in validation that column values are scientifically sensible (e.g., contact frequency in [0, 1] or distance > 0); invalid data will be silently persisted unless explicitly checked by the caller.

## Evidence

- [other] Load precomputed expected_cis table (TSV format with columns dist_bp, contact_frequency, n_valid) from a deposited cooler-derived dataset.: "Load precomputed expected_cis table (TSV format with columns dist_bp, contact_frequency, n_valid) from a deposited cooler-derived dataset."
- [other] Generate output table containing binned distance (dist_bp), mean smoothed contact frequency (count.avg.smoothed), and bin statistics. Save log-binned and smoothed P(s) table as TSV with proper column headers and numeric precision.: "Generate output table containing binned distance (dist_bp), mean smoothed contact frequency (count.avg.smoothed), and bin statistics. 5. Save log-binned and smoothed P(s) table as TSV with proper"
- [discussion] New functionality for smoothing P(s) and derivatives has an unstable API.: "New functionality for smoothing P(s) and derivatives (API is not yet stable)"
- [other] Use code formatters like black or autopep8 to maintain consistent style.: "You can use a code formatter like [black](https://github.com/psf/black) or [autopep8](https://github.com/hhatto/autopep8)"
