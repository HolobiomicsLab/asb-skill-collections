---
name: feature-table-row-count-validation
description: Use when after peak quality filtering has been applied to a composite
  map peak detection output using SNR (>2), goodness-of-fit (peakshape > 0.5), minimum
  peak height (default 1e5), and prominence (≥20% of peak_height) thresholds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - asari peaks module
  - scipy.signal.find_peaks
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- See [peaks.evaluate_gaussian_peak_on_intensity_list](peaks.evaluate_gaussian_peak_on_intensity_list),
  [peaks.__peaks_cSelectivity_stats_](peaks.__peaks_cSelectivity_stats_),
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-row-count-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate the effectiveness of peak quality filtering by comparing row counts between the full unfiltered feature table and the filtered feature table to confirm appropriate selectivity. This quantitative check ensures that filtering thresholds (SNR, peak shape, height, prominence) have been applied and are reducing the feature list to a reasonable degree.

## When to use

After peak quality filtering has been applied to a composite map peak detection output using SNR (>2), goodness-of-fit (peakshape > 0.5), minimum peak height (default 1e5), and prominence (≥20% of peak_height) thresholds. Use this skill when you need to confirm that the filtering pipeline executed correctly and that the selectivity metrics actually reduced the detected feature count rather than passing through all raw peaks unchanged.

## When NOT to use

- Input is already a feature table without access to the corresponding unfiltered peak list — comparison requires both full and filtered tables.
- Peak quality filtering has not yet been applied; this validation is a post-filtering step, not a pre-filtering diagnostic.
- Data has been heavily pruned by other workflow steps (e.g., statistical filtering, sample-level thresholds) prior to peak quality filtering — row count reduction will conflate multiple filtering sources.

## Inputs

- full_unfiltered_peak_list.json (or structured format) from composite track peak detection, containing SNR, goodness_fitting (peakshape), peak_height, prominence, m/z, and retention time fields
- preferred_Feature_table.tsv (filtered feature table after quality filtering)
- full_Feature_table.tsv (optional; alternative unfiltered reference in export directory)

## Outputs

- row_count_comparison_report (numeric: full_table_rows, filtered_table_rows, reduction_count, reduction_percentage)
- validation_log (structured record confirming filtering was applied and selectivity metrics were tracked)

## How to apply

Load both the full unfiltered peak list (JSON or structured format from composite track peak detection containing SNR, goodness_fitting, peak_height, and prominence values) and the filtered feature table (preferred_Feature_table.tsv) generated after applying all quality thresholds. Count the number of rows in each table. Compare the row counts and calculate the reduction ratio or percentage. Confirm that the filtered table has fewer rows than the full table by an amount proportional to the stringency of the thresholds applied. Document both counts and verify that the reduction is not unexpectedly small (suggesting filters were not applied) or unexpectedly large (suggesting over-filtering or data loss). This validation step tracks the selectivity of the filtering mechanism and confirms reproducibility of the peak detection and filtering workflow.

## Related tools

- **asari peaks module** (Executes peak quality filtering and outputs both full_Feature_table.tsv and preferred_Feature_table.tsv for comparison) — https://github.com/shuzhao-li/asari
- **scipy.signal.find_peaks** (Underlying peak detection algorithm used in composite map peak detection prior to filtering) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **Python** (Language for loading, parsing, counting rows in feature tables and peak lists) — https://www.python.org/

## Examples

```
import pandas as pd; full_df = pd.read_csv('export/full_Feature_table.tsv', sep='\t'); filtered_df = pd.read_csv('preferred_Feature_table.tsv', sep='\t'); print(f'Full: {len(full_df)} rows, Filtered: {len(filtered_df)} rows, Reduction: {len(full_df) - len(filtered_df)} ({100*(len(full_df)-len(filtered_df))/len(full_df):.1f}%)')
```

## Evaluation signals

- Row count in filtered_Feature_table.tsv is less than or equal to row count in full_Feature_table.tsv (logical consistency).
- Row count reduction is proportional to filter stringency: SNR > 2, peakshape > 0.5, height ≥ 1e5, and prominence ≥ 20% of peak_height together should eliminate roughly 20–60% of raw peaks in typical LC-MS data (domain expectation).
- Reduction is not zero (confirming filters were applied) and not >95% (confirming over-filtering or pipeline error did not occur).
- All peaks retained in filtered table pass all four quality thresholds when row-wise inspection is performed on a sample subset.
- Row counts are reproducible across independent runs of the same input data with identical parameters.

## Limitations

- Row count comparison alone does not reveal which specific thresholds removed the most features; a threshold-by-threshold breakdown requires additional filtering diagnostics.
- Reduction ratio depends heavily on sample quality and data acquisition parameters (e.g., instrument noise, ionization efficiency); no universal 'expected' reduction exists across different datasets or instrument types.
- If the full_Feature_table.tsv includes features present in only one sample, the preferred_Feature_table.tsv may also include them, complicating interpretation of row count reduction without additional metadata on sample coverage.
- Missing or incomplete SNR, peakshape, height, or prominence values in the unfiltered peak list can lead to filtering stepping behaving unexpectedly; validation requires confidence in input data completeness.

## Evidence

- [methods] Count rows in both full and filtered tables and confirm row count reduction is appropriate relative to the unfiltered reference.: "Count rows in both full and filtered tables and confirm row count reduction is appropriate relative to the unfiltered reference."
- [readme] All peaks are kept in export/full_Feature_table.tsv if they meet signal (snr) and shape standards: "All peaks are kept in export/full_Feature_table.tsv if they meet signal (snr) and shape standards"
- [methods] Apply SNR threshold filter (SNR > 2) to retain only peaks with sufficient signal-to-noise ratio. Apply peakshape threshold filter (goodness_fitting > 0.5) using gaussian peak evaluation to retain well-shaped peaks. Apply minimum peak height threshold (default 1e5) combined with prominence requirement (≥20% of peak_height) to retain only sufficiently tall and prominent peaks.: "Apply SNR threshold filter (SNR > 2) to retain only peaks with sufficient signal-to-noise ratio. Apply peakshape threshold filter (goodness_fitting > 0.5) using gaussian peak evaluation to retain"
- [readme] The recommended feature table is preferred_Feature_table.tsv.: "The recommended feature table is preferred_Feature_table.tsv."
