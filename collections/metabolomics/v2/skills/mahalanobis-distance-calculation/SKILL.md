---
name: mahalanobis-distance-calculation
description: Use when after data normalization (Box-Cox transformation) and before hypothesis testing in Step 9 of untargeted metabolomic workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R ≥4.1.2
  - R
  - OUKS (Omics Untargeted Key Script)
derived_from:
- doi: 10.1021/acs.jproteome.1c00392
  title: Omics Untargeted Key Script
evidence_spans:
- '[![](https://img.shields.io/badge/R≥4.1.2-5fb9ed.svg?style=flat&logo=r&logoColor=white?)](https://cran.r-project.org/index.html)'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Mahalanobis Distance Calculation

## Summary

Compute the Mahalanobis distance (Hotelling T-squared statistic) for each sample in a normalized metabolomic feature matrix to quantify multivariate distance from the population mean, accounting for feature correlations and covariance structure. This metric is used to identify statistical outliers in untargeted LC-MS datasets.

## When to use

After data normalization (Box-Cox transformation) and before hypothesis testing in Step 9 of untargeted metabolomic workflows. Apply when you have a preprocessed feature matrix and need to detect samples that are multivariate statistical outliers relative to the population distribution, particularly to flag anomalous samples before downstream statistical analysis or when comparing cases vs. controls in biomarker discovery.

## When NOT to use

- Input data has not been normalized or Box-Cox transformed; covariance structure will not reflect true biological variation.
- Feature matrix contains missing values; imputation must be completed in Step 3 before covariance computation.
- Sample size is very small (n < number of features); the covariance matrix will be singular and T² calculation will fail.

## Inputs

- Normalized feature intensity matrix (post-Box-Cox transformation from Step 7)
- Sample metadata (optional, for stratification or QC flagging)

## Outputs

- Per-sample Hotelling T-squared scores (numeric vector)
- Per-sample outlier status (Boolean vector: TRUE/FALSE)
- Outlier threshold value (scalar: F-distribution critical value or 95th percentile)
- Tabular output file with sample IDs, T² scores, and outlier flags

## How to apply

Load the normalized feature matrix (post-Step 7) into R. Compute the mean vector (centroid) and covariance matrix of all features across samples. For each sample, calculate the Hotelling T-squared statistic using the formula T² = (x − μ)ᵀ Σ⁻¹ (x − μ), where x is the sample vector, μ is the mean vector, and Σ⁻¹ is the inverse covariance matrix. Define an outlier threshold using either the critical value from the F-distribution or the 95th percentile of T² scores. Flag samples exceeding this threshold as outliers and output per-sample T² scores and binary outlier status (TRUE/FALSE) for downstream filtering or interpretation.

## Related tools

- **R** (Computational environment for covariance matrix estimation and T-squared calculation) — https://cloud.r-project.org/
- **OUKS (Omics Untargeted Key Script)** (Integrated nine-step metabolomic pipeline containing Step 9 statistics module with Hotelling T-squared implementation) — https://github.com/plyush1993/OUKS

## Evaluation signals

- Per-sample T² scores are non-negative scalars; the distribution should be approximately right-skewed with most values < threshold.
- Outlier flags are binary (TRUE/FALSE) with count of outliers typically 1–5% of total samples at 95th percentile threshold.
- T² scores for known QC or technical replicates should cluster tightly near the mean; if dispersed, covariance matrix may be ill-conditioned.
- Tabular output contains exactly one row per sample with matching sample IDs from input feature matrix; no rows should be missing or duplicated.
- Threshold value (critical F-value or 95th percentile) is reported; verify it is appropriate for the sample size and feature dimensionality.

## Limitations

- Covariance matrix inversion fails if the feature matrix is singular or ill-conditioned (e.g., highly correlated features or n < p); regularization (e.g., PCA-based approach) may be needed.
- Hotelling T² assumes multivariate normality; if features are heavily skewed despite Box-Cox transformation, outlier thresholds may be inaccurate.
- The article provides no validation dataset, benchmarking study, or comparative performance evaluation against alternative outlier methods (e.g., isolation forest, local outlier factor).
- No parameter tuning guidance or sensitivity analysis is provided; choice of F-distribution critical value vs. percentile-based threshold is not justified.

## Evidence

- [other] Calculate Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance.: "Calculate Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance."
- [other] Compute the mean vector and covariance matrix of the feature data.: "Compute the mean vector and covariance matrix of the feature data."
- [other] Define outlier thresholds for T-squared (e.g., critical value from F-distribution or 95th percentile): "Define outlier thresholds for T-squared (e.g., critical value from F-distribution or 95th percentile)"
- [other] Load the preprocessed feature matrix (post-normalization from step 7) into R.: "Load the preprocessed feature matrix (post-normalization from step 7) into R."
- [other] Output outlier flags, T-squared scores, and DModX scores to a tabular format.: "Output outlier flags, T-squared scores, and DModX scores to a tabular format."
- [discussion] "9. Statistics": Hotelling Ellipse with T-squared statistic and DModX metric: ""9. Statistics": Hotelling Ellipse with T-squared statistic and DModX metric"
