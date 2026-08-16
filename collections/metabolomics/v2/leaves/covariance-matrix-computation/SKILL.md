---
name: covariance-matrix-computation
description: Use when after normalization (Step 7) is complete and you have a clean
  feature matrix ready for multivariate statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R ≥4.1.2
  - R
  - OUKS Step 9 Statistics.R
  techniques:
  - LC-MS
  license_tier: open
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
  - build: coll_minfer_cq
    doi: 10.1016/j.cmpb.2025.108672
    title: MInfer
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

# covariance-matrix-computation

## Summary

Compute the mean vector and covariance matrix from preprocessed metabolomic feature data to establish the multivariate statistical foundation for Hotelling T-squared and Mahalanobis distance calculations in outlier detection.

## When to use

After normalization (Step 7) is complete and you have a clean feature matrix ready for multivariate statistical analysis. Apply this skill immediately before calculating per-sample Hotelling T-squared statistics or Mahalanobis distances to detect outlier samples in untargeted LC-MS metabolomic datasets.

## When NOT to use

- Input data contains missing values or zero-variance features; impute and filter before covariance computation.
- Feature matrix is highly rank-deficient (number of samples << number of features); apply dimensionality reduction (PCA) first.
- Covariance matrix is singular or numerically unstable; use regularized covariance estimators or Moore–Penrose pseudoinverse.

## Inputs

- Preprocessed feature intensity matrix (samples × features, post-normalization from Step 7)
- Metadata table with sample identifiers and class/batch annotations (optional, for stratified covariance if needed)

## Outputs

- Mean vector (1 × features)
- Covariance matrix (features × features, symmetric)
- Inverse covariance matrix (features × features, if required for Mahalanobis distance)

## How to apply

Load the preprocessed feature matrix (post-normalization, rows = samples, columns = features) into R. Compute the sample mean vector across all features. Calculate the sample covariance matrix using standard covariance estimation (e.g., `cov()` function in R), which captures pairwise feature correlations. Store both the mean vector and covariance matrix for subsequent Mahalanobis distance and inverse covariance calculations. The covariance matrix must be non-singular; if rank-deficient, apply dimensionality reduction (e.g., PCA) or regularization before inversion. Verify the matrix is symmetric and positive semi-definite as a sanity check.

## Related tools

- **R** (Computing environment for covariance matrix calculation using base `cov()`, `colMeans()`, and matrix algebra functions) — https://cran.r-project.org/index.html
- **OUKS Step 9 Statistics.R** (Script that implements covariance matrix computation and subsequent Hotelling T-squared and DModX outlier detection) — https://github.com/plyush1993/OUKS/blob/main/Scripts%20(R)/9.%20Statistics.R

## Examples

```
# Load normalized feature matrix (samples × features)
X <- read.csv('normalized_features.csv', row.names=1)
mean_vec <- colMeans(X)
cov_mat <- cov(X)
inv_cov <- solve(cov_mat)  # Compute inverse for Mahalanobis distance
```

## Evaluation signals

- Covariance matrix is symmetric (matrix == t(matrix))
- All diagonal elements (variances) are positive and match feature-wise variances
- Matrix rank equals the minimum of (samples - 1, features); if rank-deficient, flag for PCA preprocessing
- Inverse covariance matrix is numerically stable (condition number is reasonable, no NaN/Inf values)
- Mahalanobis distances computed from the covariance matrix show expected univariate and multivariate patterns (e.g., QC samples cluster near zero distance)

## Limitations

- Covariance estimation is unreliable when sample size n is comparable to or smaller than feature count p; requires n >> p or regularization.
- Assumes multivariate normality of features; violations can inflate Hotelling T-squared statistics and outlier thresholds.
- Non-robust to extreme outliers; a single outlier sample can distort the covariance matrix. Consider robust covariance estimators (e.g., Minimum Covariance Determinant) if pre-screening for gross outliers is needed.
- No guidance provided in the article on parameter selection for regularization (e.g., ridge parameter λ) or dimensionality reduction cutoff.

## Evidence

- [other] Compute the mean vector and covariance matrix of the feature data.: "Compute the mean vector and covariance matrix of the feature data."
- [other] Load the preprocessed feature matrix (post-normalization from step 7) into R.: "Load the preprocessed feature matrix (post-normalization from step 7) into R."
- [other] Calculate Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance.: "Calculate Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance."
- [other] Step 9 (Statistics) implements Hotelling Ellipse with T-squared statistic and DModX metric for sample outlier detection: "Step 9 (Statistics) implements Hotelling Ellipse with T-squared statistic and DModX metric for sample outlier detection"
