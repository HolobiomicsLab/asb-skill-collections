---
name: python-pandas-data-manipulation
description: Use when you have precomputed expected contact frequency tables (TSV format with columns like dist_bp, contact_frequency, n_valid) and need to apply log-binning and smoothing to group distance values into log-spaced bins, aggregate statistics within each bin, and export a cleaned, annotated output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0654
  tools:
  - Python
  - cooltools
  - cooler
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans:
- enabling high-resolution Hi-C analysis in Python
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

# Python pandas data manipulation

## Summary

Use Python and pandas to load, transform, and export tabular datasets (TSV/CSV) containing precomputed genomic statistics, applying binning, smoothing, and aggregation operations to prepare contact frequency curves for downstream analysis.

## When to use

You have precomputed expected contact frequency tables (TSV format with columns like dist_bp, contact_frequency, n_valid) and need to apply log-binning and smoothing to group distance values into log-spaced bins, aggregate statistics within each bin, and export a cleaned, annotated output table for visualization or further analysis.

## When NOT to use

- Input is already a log-binned or aggregated contact frequency curve; re-binning would introduce redundant or conflicting bin boundaries.
- Contact frequency data is in cooler (.cool/.mcool) HDF5 format; use cooler API methods directly rather than manual TSV export and pandas re-import.
- Analysis goal is real-time or streaming; pandas requires full dataset in memory.

## Inputs

- TSV table with columns: dist_bp (genomic distance), contact_frequency, n_valid (bin size/validity counts)
- Logarithmic binning parameters (e.g., log base, minimum/maximum bin edges)
- Optional: precomputed smoothing kernel or smoothing algorithm specification

## Outputs

- Log-binned TSV table with columns: dist_bp (bin representative or range), count.avg.smoothed (mean contact frequency per bin), and bin statistics (e.g., bin size, variance)
- Optionally: metadata or column headers documenting bin structure and smoothing method

## How to apply

Load the precomputed expected_cis table from TSV format into a pandas DataFrame. Apply logarithmic binning to group genomic distances into log-spaced bins using the cooltools logbin_expected function or equivalent binning logic. Compute aggregated statistics within each bin (e.g., mean smoothed contact frequency, bin counts) using pandas groupby and aggregation operations. Generate an output DataFrame with columns including binned distance, mean smoothed contact frequency, and bin statistics. Ensure numeric precision and proper column headers, then export to TSV format for downstream use.

## Related tools

- **cooltools** (Provides logbin_expected function for log-binning and smoothing of precomputed expected contact frequency tables; implements the binning and smoothing algorithm) — https://github.com/open2c/cooltools
- **cooler** (Stores and retrieves Hi-C contact matrices and precomputed statistics in HDF5 format; source of expected_cis tables) — https://github.com/open2c/cooler
- **Python** (Core language for executing pandas operations and cooltools functions)

## Examples

```
from cooltools.analysis.expected import logbin_expected; import pandas as pd; exp_table = pd.read_csv('expected_cis.tsv', sep='\t'); binned = logbin_expected(exp_table); binned.to_csv('expected_binned.tsv', sep='\t', index=False)
```

## Evaluation signals

- Output TSV contains exactly the expected columns (dist_bp, count.avg.smoothed, bin statistics) with no missing or extraneous fields.
- Numeric precision is preserved: check that floating-point values maintain consistency with source precomputed table (e.g., no truncation or NaN artifacts introduced).
- Bin structure is monotonically increasing in distance and conforms to log-spacing: verify that consecutive bin edges follow a logarithmic progression (e.g., bin width ratio ≈ constant log base).
- Aggregation is idempotent: re-running the same binning operation on the output should yield identical results (no stochastic or state-dependent smoothing).
- Bin counts match row count expectations: sum of n_valid (or bin size column) should reconcile with input row count if no filtering is applied.

## Limitations

- The cooltools logbin_expected API is not yet stable; function signature, smoothing algorithm, or output format may change in future releases.
- Log-binning discards fine-grained distance information; spurious or signal near bin boundaries may be averaged away, reducing resolution for distance-dependent features.
- Smoothing can introduce artificial correlations between adjacent bins; downstream statistical tests (e.g., χ² tests) may be biased if smoothing is not accounted for.
- Large datasets may exhaust memory if loaded entirely into pandas; streaming or chunked processing is not straightforward.

## Evidence

- [other] Load precomputed expected_cis table (TSV format with columns dist_bp, contact_frequency, n_valid) from a deposited cooler-derived dataset.: "Load precomputed expected_cis table (TSV format with columns dist_bp, contact_frequency, n_valid) from a deposited cooler-derived dataset"
- [other] Apply logbin_expected function with logarithmic binning to group distance values into log-spaced bins.: "Apply logbin_expected function with logarithmic binning to group distance values into log-spaced bins"
- [other] Smooth contact frequency within each log bin using the smoothing algorithm provided by the logbin_expected implementation.: "Smooth contact frequency within each log bin using the smoothing algorithm provided by the logbin_expected implementation"
- [other] Generate output table containing binned distance (dist_bp), mean smoothed contact frequency (count.avg.smoothed), and bin statistics.: "Generate output table containing binned distance (dist_bp), mean smoothed contact frequency (count.avg.smoothed), and bin statistics"
- [discussion] New functionality for smoothing P(s) and derivatives (API is not yet stable): "New functionality for smoothing P(s) and derivatives (API is not yet stable)"
