---
name: contact-distance-binning-logarithmic
description: 'Use when you have a precomputed expected contact frequency table (TSV format with columns: dist_bp, contact_frequency, n_valid) derived from cooler files and need to compress distance-dependent contact probabilities into log-spaced bins.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3125
  tools:
  - cooltools
  - cooler
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

# contact-distance-binning-logarithmic

## Summary

Apply logarithmic binning to genomic distance values in a precomputed contact frequency table, grouping distances into log-spaced bins and smoothing contact frequencies within each bin to produce a log-binned P(s) contact probability curve. This skill is essential for compressing high-resolution Hi-C contact data into a manageable number of distance-dependent bins suitable for downstream analysis.

## When to use

You have a precomputed expected contact frequency table (TSV format with columns: dist_bp, contact_frequency, n_valid) derived from cooler files and need to compress distance-dependent contact probabilities into log-spaced bins. This is necessary when you want to plot or analyze the P(s) curve (contact probability as a function of genomic distance) with reduced noise and improved interpretability, particularly when the raw frequency table spans multiple orders of magnitude in genomic distance.

## When NOT to use

- The input is already a log-binned contact probability table or does not require smoothing.
- You need per-bin contact counts for individual genomic regions rather than genome-wide expected contact frequency.
- The precomputed expected table is in a non-standard format lacking the required dist_bp and contact_frequency columns.

## Inputs

- precomputed expected_cis table (TSV format with columns: dist_bp, contact_frequency, n_valid)

## Outputs

- log-binned and smoothed P(s) table (TSV with columns: dist_bp, count.avg.smoothed, and bin statistics)

## How to apply

Load the precomputed expected_cis table (TSV) containing dist_bp, contact_frequency, and n_valid columns. Apply the cooltools logbin_expected function, which performs logarithmic binning by grouping distance values into log-spaced bins and applies an integrated smoothing algorithm to each bin's contact frequencies. The function computes the mean smoothed contact frequency for each log bin, outputting a reduced table with binned distance (dist_bp), mean smoothed contact frequency (count.avg.smoothed), and associated bin statistics. Save the output as a TSV file with appropriate numeric precision. The logarithmic binning is motivated by the observation that Hi-C contact frequencies follow a power-law decay with distance; log-spacing ensures equal representation across the range of distances while the smoothing algorithm reduces noise within each bin.

## Related tools

- **cooltools** (Provides the logbin_expected function to perform logarithmic binning and smoothing on precomputed contact frequency tables) — https://github.com/open2c/cooltools
- **cooler** (Stores and provides access to high-resolution Hi-C contact matrices from which expected contact frequencies are precomputed) — https://github.com/open2c/cooler
- **Python** (Execution environment for running cooltools functions and data processing scripts)

## Evaluation signals

- Output TSV contains expected columns (dist_bp, count.avg.smoothed, bin statistics) with numeric precision consistent with input.
- Distance bins are spaced logarithmically: bin widths increase exponentially (e.g., ratio between consecutive bin edges is constant).
- Smoothed contact frequency values are monotonically decreasing or follow expected power-law decay trend with distance.
- Number of output bins is substantially less than the number of input distance values, confirming compression via binning.
- Bin statistics (e.g., counts per bin or standard deviation within each bin) indicate that smoothing was applied; individual outliers should not dominate bin values.

## Limitations

- The API for the smoothing mechanism in logbin_expected is not yet stable and may change in future releases, potentially affecting reproducibility.
- Logarithmic binning assumes contact frequency follows a power-law relationship with distance; deviations from this assumption may require custom binning strategies.
- The function requires precomputed expected contact frequencies as input; it does not handle raw contact matrices directly.
- Edge cases at very short distances (< 1 bp) or very long distances (> chromosome length) may produce unexpected bin boundaries or insufficient data per bin.

## Evidence

- [other] how does the logbin_expected function in cooltools perform log-binning and smoothing on a precomputed expected contact frequency table to produce a log-binned contact probability P(s) curve: "Apply logbin_expected function with logarithmic binning to group distance values into log-spaced bins. Smooth contact frequency within each log bin using the smoothing algorithm provided by the"
- [other] input file format and columns: "Load precomputed expected_cis table (TSV format with columns dist_bp, contact_frequency, n_valid) from a deposited cooler-derived dataset."
- [other] output table structure: "Generate output table containing binned distance (dist_bp), mean smoothed contact frequency (count.avg.smoothed), and bin statistics."
- [discussion] stability caveat: "New functionality for smoothing P(s) and its derivatives, though the API for this smoothing mechanism is not yet stable."
- [intro] purpose of log-binning in Hi-C analysis: "The recently-introduced cooler format readily handles storage of high-resolution datasets enabling high-resolution Hi-C analysis in Python"
