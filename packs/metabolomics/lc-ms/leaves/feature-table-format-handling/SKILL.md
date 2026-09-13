---
name: feature-table-format-handling
description: Use when transitioning feature intensity data between pipeline stages
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3906
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetCorR
  - R
  - OUKS
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.1c00392
  title: Omics Untargeted Key Script
evidence_spans:
- New QC-GAM method (MetCorR) with associated scripts were introduced.
- R based open-source collection of scripts called :red_circle:*OUKS*
- R ≥4.1.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omics_untargeted_key_script_cq
    doi: 10.1021/acs.jproteome.1c00392
    title: Omics Untargeted Key Script
  dedup_kept_from: coll_omics_untargeted_key_script_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.1c00392
  all_source_dois:
  - 10.1021/acs.jproteome.1c00392
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Feature Table Format Handling

## Summary

Convert, validate, and manage metabolomic feature tables across multiple formats (CSV, RData, tabular) while preserving sample and feature identifiers for downstream processing in LC-MS untargeted profiling workflows. This skill ensures consistent representation of intensity matrices (samples × features) with associated metadata throughout the nine-step OUKS pipeline.

## When to use

Apply this skill when transitioning feature intensity data between pipeline stages (e.g., post-integration to pre-imputation, post-correction to pre-filtering), when importing raw peak-picked data into R for OUKS processing, or when exporting corrected/normalized tables for external validation or cross-tool analysis. Specifically use it when the feature table must preserve QC sample identifiers and run-order metadata needed for batch correction, or when downstream steps require specific row/column ordering or naming conventions.

## When NOT to use

- Input is already a validated, in-memory R data.frame ready for imputation or normalization without format conversion.
- Feature table lacks clear sample or feature identifiers (unindexed or single-column layouts) and cannot be reliably parsed into samples × features structure.
- QC sample labels are inconsistent or missing but required for batch correction or drift assessment steps.

## Inputs

- Raw feature intensity table (samples × features, CSV or tabular format)
- Sample metadata (class labels, QC identifiers, batch/run-order columns)
- Feature annotations (m/z, retention time, or feature IDs as column names)
- RData objects containing pre-computed feature tables from prior pipeline stages

## Outputs

- Validated feature intensity matrix (samples × features) in R memory
- Corrected or filtered feature table (CSV or RData) with preserved identifiers
- Sample-feature mapping metadata for traceability and validation

## How to apply

Load the feature intensity matrix (samples × features dimension) along with associated metadata (sample class labels, QC identifiers, batch/run-order information) into R as a data.frame or matrix. Validate that row names match sample identifiers in the metadata file and column names correspond to detected features (m/z-RT pairs or feature IDs). Standardize column/row naming to remove special characters or whitespace that may cause parsing errors in downstream R packages. For tables requiring QC-based correction (e.g., before MetCorR GAM application), ensure QC sample rows are clearly marked with a consistent label (e.g., 'QC') in the class column. Export corrected or filtered tables as CSV or RData format, preserving the same sample-feature structure and identifiers to maintain traceability through the pipeline.

## Related tools

- **R** (Primary environment for loading, validating, and exporting feature tables as data.frames; manages metadata integration) — https://cran.r-project.org/index.html
- **MetCorR** (Consumes feature table with QC labels and batch metadata; outputs corrected intensity matrix preserving original structure) — https://github.com/plyush1993/MetCorR
- **OUKS** (Pipeline framework integrating feature table handling across nine processing steps; scripts load/export tables at each stage) — https://github.com/plyush1993/OUKS

## Examples

```
# Load feature table and metadata into R
int_data <- read.csv('feature_intensity_table.csv', row.names=1)
meta <- read.csv('metadata.csv', row.names=1)
# Pass to MetCorR for QC-GAM correction
out <- MetCorR(method=2, int_data=int_data, order=meta$order, class=meta$class, batch=meta$batch, qc_label='QC')
# Export corrected table
write.csv(out$corrected_data, 'corrected_feature_table.csv')
```

## Evaluation signals

- Feature table dimensions (samples × features) are preserved after load/export cycles; row count equals number of samples, column count equals number of detected features.
- Sample and feature identifiers remain intact and human-readable post-processing (no truncation, corruption, or encoding artifacts).
- QC sample rows are correctly marked and retrievable from the metadata class column for use in batch correction algorithms.
- Intensity values remain numeric, without conversion to strings or loss of precision; NaN/NA missingness is handled consistently.
- CSV and RData formats are round-trip compatible: loading and re-exporting produces functionally identical tables with identical row/column ordering.

## Limitations

- No guidance provided on parameter selection, sensitivity analysis, or tuning for handling sparse or high-dimensional tables (>>10,000 features).
- Article does not specify maximum table size, memory requirements, or performance characteristics for very large sample cohorts (>10,000 samples).
- No validation dataset or benchmarking study documented to assess format handling robustness across different LC-MS instrument outputs or vendor software exports.
- R version requirement (≥4.1.2) is stated but compatibility with newer major versions or older legacy R code is not tested.

## Evidence

- [other] Load the QC-annotated feature table (samples × features with QC sample identifiers) into R.: "Load the QC-annotated feature table (samples × features with QC sample identifiers) into R."
- [other] Output the corrected feature table in CSV or tabular format, preserving sample and feature identifiers.: "Output the corrected feature table in CSV or tabular format, preserving sample and feature identifiers."
- [readme] Scripts (R) with comments, notes and references are stored in Scripts folder: "Scripts (R) with comments, notes and references are stored in Scripts folder at a previously defined order"
- [readme] Datasets in .csv and other files (.RData, .R) are available for reproducibility: "Datasets in .csv and other files (.RData, .R) are available for reproducibility from corresponding folders."
