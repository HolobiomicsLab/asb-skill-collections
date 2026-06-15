---
name: contact-frequency-smoothing-log-space
description: 'Use when you have a precomputed expected contact frequency table (TSV with columns: dist_bp, contact_frequency, n_valid) derived from cooler Hi-C matrices and need to generate a smoothed, log-binned P(s) curve for downstream analysis such as TAD detection, contact probability visualization, or.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3206
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0092
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

# contact-frequency-smoothing-log-space

## Summary

Apply logarithmic binning and smoothing to precomputed expected contact frequency tables to produce log-binned, smoothed contact probability P(s) curves suitable for Hi-C distance decay analysis. This skill transforms raw distance-frequency pairs into log-spaced bins with smoothed contact frequencies, essential for characterizing the relationship between genomic distance and contact probability.

## When to use

You have a precomputed expected contact frequency table (TSV with columns: dist_bp, contact_frequency, n_valid) derived from cooler Hi-C matrices and need to generate a smoothed, log-binned P(s) curve for downstream analysis such as TAD detection, contact probability visualization, or comparison of contact decay across conditions or cell types.

## When NOT to use

- Input is already a log-binned or smoothed contact frequency table; applying this skill twice will over-smooth and lose resolution.
- Raw contact matrix (cooler file) is available and you need to compute expected frequency de novo; use cooler's built-in expected/observed computation first.
- Analysis requires linear (not logarithmic) binning of distances, e.g., fixed-width bins for regulatory element analysis.

## Inputs

- precomputed expected contact frequency table (TSV format with columns: dist_bp, contact_frequency, n_valid)
- cooler-derived Hi-C dataset (optional, if generating expected table de novo)

## Outputs

- log-binned and smoothed P(s) table (TSV format with columns: dist_bp, count.avg.smoothed, bin statistics)
- log-space contact probability curve suitable for visualization and downstream analysis

## How to apply

Load the expected_cis table (TSV format) into Python and apply the cooltools `logbin_expected()` function to perform logarithmic binning on distance values and apply smoothing to contact frequencies within each log bin. The function uses a logarithmic scale to group genomic distances such that relative changes in distance are equally represented, which is critical for Hi-C contact decay typically follows a power law. Configure the logarithmic bin spacing (e.g., base 2 or custom log factor) to balance resolution at short distances with coverage at long distances. The smoothing algorithm within `logbin_expected()` estimates mean smoothed contact frequency for each log bin, reducing noise while preserving the overall decay shape. Output the result as a TSV with columns for binned distance (dist_bp), mean smoothed contact frequency (count.avg.smoothed), and associated bin statistics (e.g., bin count, variance). Validate that the output curve is monotonically decreasing and spans the full input distance range.

## Related tools

- **cooltools** (Provides logbin_expected() function to perform logarithmic binning and smoothing on precomputed expected contact frequency tables) — https://github.com/open2c/cooltools
- **cooler** (Stores and retrieves Hi-C contact matrices in cooler format; used to generate or access the precomputed expected_cis table) — https://github.com/open2c/cooler
- **Python** (Host language for cooltools API and data manipulation (NumPy, Pandas for table I/O and processing))

## Examples

```
from cooltools.expected import logbin_expected; import pandas as pd; expected = pd.read_csv('expected_cis.tsv', sep='\t'); smoothed = logbin_expected(expected, logbase=2.0); smoothed.to_csv('expected_cis.logbin.tsv', sep='\t', index=False)
```

## Evaluation signals

- Output TSV contains expected columns (dist_bp, count.avg.smoothed, bin statistics) with correct data types and no missing values.
- Contact frequency values are monotonically decreasing or non-increasing as a function of distance (no spurious oscillations introduced by smoothing).
- Log bin boundaries follow logarithmic spacing (e.g., bin width in log space is constant); verify by computing log ratios of consecutive bin edges.
- Number of output bins is significantly smaller than input rows, confirming binning aggregation; typical reduction to 20–50 bins for mammalian genome.
- Smoothed curve visually and statistically resembles the power-law or inverse-power decay expected for Hi-C contact probability; fit to power law should be monotonically decreasing with coefficient of determination (R²) > 0.95.

## Limitations

- The API for smoothing P(s) and its derivatives is not yet stable in cooltools, meaning function signature, parameter names, or output format may change across versions.
- Smoothing algorithm details (kernel type, bandwidth selection, edge handling) are not fully documented; users cannot easily customize or replicate smoothing independently.
- Log binning inherently sacrifices resolution at long genomic distances; short-range contacts may be underrepresented if bin width is too coarse.
- The skill assumes a unimodal, monotone-decreasing contact decay; it may produce artifacts or misleading smoothing for complex, multimodal distance-frequency distributions (e.g., if topologically associating domains create secondary peaks).

## Evidence

- [other] Load precomputed expected_cis table (TSV format with columns dist_bp, contact_frequency, n_valid) from a deposited cooler-derived dataset.: "Load precomputed expected_cis table (TSV format with columns dist_bp, contact_frequency, n_valid) from a deposited cooler-derived dataset."
- [other] Apply logbin_expected function with logarithmic binning to group distance values into log-spaced bins and smooth contact frequency within each log bin.: "Apply logbin_expected function with logarithmic binning to group distance values into log-spaced bins. 3. Smooth contact frequency within each log bin using the smoothing algorithm provided by the"
- [other] Generate output table containing binned distance (dist_bp), mean smoothed contact frequency (count.avg.smoothed), and bin statistics.: "Generate output table containing binned distance (dist_bp), mean smoothed contact frequency (count.avg.smoothed), and bin statistics."
- [discussion] New functionality for smoothing P(s) and derivatives (API is not yet stable): "New functionality for smoothing P(s) and derivatives (API is not yet stable)"
- [other] Cooltools includes new functionality for smoothing P(s) and its derivatives, though the API for this smoothing mechanism is not yet stable.: "Cooltools includes new functionality for smoothing P(s) and its derivatives, though the API for this smoothing mechanism is not yet stable."
