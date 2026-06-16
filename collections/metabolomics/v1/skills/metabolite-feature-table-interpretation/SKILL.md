---
name: metabolite-feature-table-interpretation
description: Use when immediately after executing the MetaboAnalystR 4.0 unified LC-MS workflow (feature detection and quantification module) on raw mzML or netCDF data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MetaboAnalystR
derived_from:
- doi: 10.1038/s41467-024-48009-6
  title: metaboanalystr
evidence_spans:
- 'MetaboAnalystR 4.0: a unified LC-MS workflow for global metabolomics'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboanalystr
    doi: 10.1038/s41467-024-48009-6
    title: metaboanalystr
  dedup_kept_from: coll_metaboanalystr
schema_version: 0.2.0
---

# metabolite-feature-table-interpretation

## Summary

Extract and interpret quantitative and structural properties from LC-MS feature tables produced by MetaboAnalystR 4.0, including table dimensions, peak intensity statistics, and feature quality metrics. This skill bridges raw feature detection output to downstream statistical and functional analysis by characterizing the scope and quality of the detected metabolome.

## When to use

Apply this skill immediately after executing the MetaboAnalystR 4.0 unified LC-MS workflow (feature detection and quantification module) on raw mzML or netCDF data. Use it when you need to: (1) verify that feature detection parameters were appropriate for your dataset (sample count, feature count, intensity dynamic range); (2) identify potential data quality issues before proceeding to normalization or statistical analysis; (3) report quantitative properties of the feature table in methods/results sections; (4) decide whether to apply batch effect correction or filtering based on observed intensity distributions and sample-to-feature ratios.

## When NOT to use

- Input is already a normalized or filtered feature table—skip to direct statistical analysis instead of re-summarizing raw intensities.
- Feature detection has not yet been executed—run the MetaboAnalystR 4.0 LC-MS workflow first to generate the feature table.
- You are analyzing MS/MS spectra or compound annotations rather than peak intensities—use compound annotation or spectral matching skills instead.

## Inputs

- Feature table matrix (mzML or netCDF raw LC-MS data processed by MetaboAnalystR 4.0 unified LC-MS workflow)
- Feature detection and quantification output (rows = m/z features, columns = samples, values = peak intensities)
- Metadata file linking samples to experimental groups (optional but recommended for per-group summaries)

## Outputs

- Feature table dimensions report (number of features, number of samples)
- Intensity statistics summary (mean, median, standard deviation, min, max across all features)
- Per-feature quality metrics (intensity range, coefficient of variation, detection frequency)
- Per-sample quality metrics (total intensity, feature count, outlier flags)
- Structured output report (text, CSV, or R object format)

## How to apply

Load the feature table output (typically a matrix of m/z features × samples with intensity values) from the MetaboAnalystR 4.0 LC-MS workflow. Compute and document: (1) table dimensions as number of features (rows) and number of samples (columns); (2) summary statistics on peak intensity values including mean, median, standard deviation, minimum, and maximum across all features; (3) per-feature statistics such as intensity range and coefficient of variation to identify low-quality or highly variable features; (4) per-sample statistics to identify outlier or low-intensity samples. Compare observed feature count and intensity ranges against literature benchmarks and your experimental design (e.g., expected metabolite diversity for the biological matrix). Use these metrics to evaluate whether the auto-optimized peak picking parameters yielded reasonable sensitivity and specificity, and to guide downstream filtering or normalization decisions.

## Related tools

- **MetaboAnalystR** (Unified LC-MS workflow platform that performs feature detection, quantification, and produces the feature table matrix for downstream interpretation) — https://github.com/xia-lab/MetaboAnalystR

## Examples

```
# Load feature table from MetaboAnalystR 4.0 output; compute and summarize dimensions and intensity statistics
mbaObj <- readRDS("mba_feature_table.rds"); summary(colSums(mbaObj$data_proc)); summary(rowSums(mbaObj$data_proc)); dim(mbaObj$data_proc)
```

## Evaluation signals

- Feature table dimensions (number of features and samples) are reported and match the input dataset size.
- Intensity statistics are non-negative, with max ≥ median ≥ mean ≥ min, and standard deviation ≤ (max − min).
- Per-feature coefficient of variation values are ≥ 0 and span a plausible range for metabolomic data (typically 0–200%).
- Sample outlier detection flags (e.g., samples with total intensity >3 SD from mean) align with known batch effects or sample quality issues.
- Feature count and intensity ranges are consistent with literature values for the biological matrix and LC-MS platform used (e.g., 1000–10000 features for untargeted human plasma).

## Limitations

- Feature table interpretation depends critically on the correctness of the upstream peak picking parameters in MetaboAnalystR 4.0; if parameters are misspecified, statistics may reflect false positives or false negatives rather than true metabolite abundance.
- No changelog or version-specific parameter documentation is available in the README, making it difficult to reproduce results across different MetaboAnalystR 4.0 versions.
- Intensity statistics alone do not indicate biological significance or compound identity; this skill only characterizes quantitative properties of the feature table.
- Very low-intensity features (below instrument noise floor) may not be reliably detected or quantified, leading to underestimation of true feature count and dynamic range.
- Batch effects, instrumental drift, and sample preparation variability are not deconvolved by this skill; consider specialized batch correction functions (e.g., ComBat, SVA) for downstream analysis.

## Evidence

- [other] Extract feature table dimensions (number of rows as features, number of columns as samples) and compute summary statistics on peak intensity values (mean, median, standard deviation, min, max).: "Extract feature table dimensions (number of rows as features, number of columns as samples) and compute summary statistics on peak intensity values (mean, median, standard deviation, min, max)."
- [readme] an auto-optimized feature detection and quantification module for LC-MS1 spectra processing: "an auto-optimized feature detection and quantification module for LC-MS1 spectra processing"
- [readme] Serial dilutions demonstrate that MetaboAnalystR 4.0 can accurately detect and identify > 10% more high-quality MS and MS/MS features.: "Serial dilutions demonstrate that MetaboAnalystR 4.0 can accurately detect and identify > 10% more high-quality MS and MS/MS features."
- [readme] MetaboAnalystR 4.0 contains the R functions and libraries underlying the popular MetaboAnalyst web server, including metabolomic data analysis, visualization, and functional interpretation.: "MetaboAnalystR 4.0 contains the R functions and libraries underlying the popular MetaboAnalyst web server, including metabolomic data analysis, visualization, and functional interpretation."
