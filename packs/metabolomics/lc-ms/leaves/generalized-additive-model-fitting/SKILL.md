---
name: generalized-additive-model-fitting
description: Use when when a feature table from LC-MS metabolomic profiling contains QC (quality control) sample annotations and exhibits systematic signal drift correlated with run order or batch number.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetCorR
  - R
  - OUKS
  techniques:
  - LC-MS
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

# Generalized Additive Model Fitting for QC-Based Signal Drift Correction

## Summary

Fit Generalized Additive Models (GAMs) to QC samples to estimate and correct run-order and batch-dependent signal drift in untargeted LC-MS metabolomic feature tables. This skill models non-linear batch effects using QC reference points, then applies the fitted correction factors to all sample features.

## When to use

When a feature table from LC-MS metabolomic profiling contains QC (quality control) sample annotations and exhibits systematic signal drift correlated with run order or batch number. Apply this skill after imputation and before annotation to remove technical variation that could confound biological interpretation.

## When NOT to use

- Input feature table has no QC samples or QC labels are not reliably annotated.
- Samples are from a single batch with minimal run-order drift (correction may introduce noise without benefit).
- Feature table is already log-normalized or heavily right-skewed; consider data transformation first.

## Inputs

- QC-annotated feature intensity table (samples × features, numeric matrix or data.frame)
- Sample metadata with run order, batch identifier, and QC sample label indicator
- Raw or previously imputed feature abundances

## Outputs

- Batch and run-order corrected feature intensity table (same dimensions as input)
- Fitted GAM model object (for diagnostics and reproducibility)
- Correction factor predictions for all samples

## How to apply

Load the QC-annotated feature table (samples × features matrix) with associated metadata (run order, batch ID, QC sample labels) into R. Fit a GAM using the QC samples as reference points, modeling intensity as a smoothed function of run order and/or batch via the formula y ~ s(order, batch) or y ~ s(order) depending on experimental design. The GAM learns correction factors that account for instrumental drift; extract predictions for all samples and divide the original intensities by these factors to obtain drift-corrected abundances. Output the corrected feature table in CSV or tabular format, preserving sample and feature identifiers for downstream analysis.

## Related tools

- **MetCorR** (R package implementing QC-GAM correction via the MetCorR() function; orchestrates GAM fitting and factor application) — https://github.com/plyush1993/MetCorR
- **R** (Runtime environment; GAMs are fitted using the mgcv package (loaded by MetCorR)) — https://cran.r-project.org/index.html
- **OUKS** (Umbrella R-based metabolomics workflow in which the Correction step (step 4) applies MetCorR) — https://github.com/plyush1993/OUKS

## Examples

```
library(MetCorR); data(example_intensity, package='MetCorR'); data(example_meta, package='MetCorR'); out <- MetCorR(method=2, int_data=example_intensity, order=example_meta$order, class=example_meta$class, batch=example_meta$batch, qc_label='QC')
```

## Evaluation signals

- Corrected feature table has same dimensions and identifiers as input (no rows/columns lost).
- Distribution of correction factors is unimodal and centered near 1.0 (large factors >2 or <0.5 may indicate overfitting or poor QC coverage).
- RLA plots (Relative Log Abundance) computed on corrected features show reduced median RLA and tighter interquartile ranges compared to uncorrected data.
- QC sample replicates cluster tightly in PCA or UMAP space after correction; biological sample separation is preserved.
- Correlation between correction factors and run order is substantially reduced post-correction (validate via scatterplot or correlation coefficient).

## Limitations

- Requires sufficient QC samples (typically ≥5–10) distributed across the run to accurately model drift; sparse QC sampling may lead to overfitting.
- GAM smoothing spline degree of freedom (basis dimension) must be tuned; default settings may oversmooth small studies or undersmooth large studies.
- Non-linear drift patterns not captured by run order and batch (e.g., instrument maintenance events, column aging) require additional metadata or preprocessing.
- Method assumes QC sample composition is constant and representative of all features; outlier QC replicates can bias GAM fit.
- No explicit parameter selection criteria, sensitivity analysis, or tuning guidelines provided in the documentation.

## Evidence

- [other] Load the QC-annotated feature table (samples × features with QC sample identifiers) into R. 2. Execute the MetCorR QC-GAM correction algorithm via the MetCorR package, which models batch-dependent signal drift using QC samples as reference points and applies Generalized Additive Models (GAM) to estimate run-order-dependent correction factors.: "Load the QC-annotated feature table (samples × features with QC sample identifiers) into R. Execute the MetCorR QC-GAM correction algorithm via the MetCorR package, which models batch-dependent"
- [other] Apply the fitted correction factors to all feature abundances across the entire table. 4. Output the corrected feature table in CSV or tabular format, preserving sample and feature identifiers.: "Apply the fitted correction factors to all feature abundances across the entire table. Output the corrected feature table in CSV or tabular format, preserving sample and feature identifiers."
- [other] New QC-GAM method (MetCorR) with associated scripts for correcting QC-annotated feature tables in untargeted metabolomic profiling.: "New QC-GAM method called MetCorR with associated scripts for correcting QC-annotated feature tables in untargeted metabolomic profiling."
- [readme] Method 2 has been selected. Used formula: y ~ s(order, batch). Fitting GAMs on QC samples... Predicting for all samples...: "Method 2 has been selected. Used formula: y ~ s(order, batch). Fitting GAMs on QC samples... Predicting for all samples..."
- [other] "4. Correction": D-Ratio metric, RLA-plot, correlogram, 2-factors PCA: "Correction step includes D-Ratio metric, RLA-plot, correlogram, 2-factors PCA for diagnostic assessment."
