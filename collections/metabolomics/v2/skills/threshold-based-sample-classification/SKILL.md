---
name: threshold-based-sample-classification
description: Use when after normalization (step 7) in untargeted metabolomic profiling pipelines, when you have a preprocessed feature matrix and need to identify samples with anomalous metabolic profiles that violate multivariate assumptions or represent technical failures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R ≥4.1.2
  - R
  - OUKS (step 9. Statistics.R)
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
---

# Threshold-based sample classification

## Summary

Classify LC-MS metabolomic samples as outliers or normal using statistical distance metrics (Hotelling T-squared and DModX) with predefined thresholds. This skill detects and flags samples that deviate from the expected multivariate distribution, enabling quality control and removal of anomalous observations before downstream analysis.

## When to use

After normalization (step 7) in untargeted metabolomic profiling pipelines, when you have a preprocessed feature matrix and need to identify samples with anomalous metabolic profiles that violate multivariate assumptions or represent technical failures. Apply this when sample size permits reliable covariance estimation and you want per-sample outlier status for quality filtering.

## When NOT to use

- Input feature matrix is very small (n < 10 samples) — covariance estimation will be unstable.
- Features are already known to be heavily non-Gaussian or the sample set is highly heterogeneous by design — multivariate normality assumptions may be violated.
- You require univariate outlier detection on individual features rather than multivariate sample-level anomaly detection.

## Inputs

- Preprocessed feature matrix (normalized intensities, post-step 7)
- Sample metadata with class/batch information (optional, for stratified thresholds)

## Outputs

- Per-sample outlier flags (TRUE/FALSE vector)
- Hotelling T-squared scores (numeric vector, one per sample)
- DModX scores (numeric vector, one per sample)
- Outlier classification table (tabular format with sample IDs, scores, and flags)

## How to apply

Load the normalized feature matrix into R and compute the mean vector and covariance matrix. Calculate the Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance; this measures deviation from the multivariate center weighted by feature covariance. In parallel, compute DModX (distance to model in X-space) as the orthogonal distance of each sample from the principal component model subspace. Define separate outlier thresholds: for T-squared use the critical value from an F-distribution or the 95th percentile of the control distribution; for DModX use the 95th percentile or a user-specified limit. Flag any sample exceeding either threshold as an outlier (TRUE/FALSE). Output per-sample outlier status, T-squared scores, and DModX scores in tabular format for downstream filtering and reporting.

## Related tools

- **R** (Primary environment for computing covariance, Mahalanobis distance, and PCA-based DModX scores) — https://cran.r-project.org/index.html
- **OUKS (step 9. Statistics.R)** (Implements Hotelling Ellipse with T-squared and DModX for sample outlier detection in metabolomic workflows) — https://github.com/plyush1993/OUKS

## Examples

```
# In R, after loading normalized feature matrix X and metadata: source('Scripts (R)/9. Statistics.R'); outlier_results <- detect_outliers_hotelling_dmodx(X, method='T2_DModX', threshold_percentile=0.95, output_file='outlier_flags.csv')
```

## Evaluation signals

- Outlier flags are binary (TRUE/FALSE) with no missing values; counts match input sample size.
- T-squared and DModX scores are non-negative numeric vectors with length equal to sample count.
- Samples flagged as outliers have T-squared or DModX scores at or above the stated percentile threshold (e.g., 95th percentile).
- Threshold values (F-critical or percentile cutoffs) are explicitly documented and reproducible across re-runs with the same input data.
- Output table is human-readable (CSV or similar) with sample identifiers, scores, and outlier status clearly labeled.

## Limitations

- Requires sufficient samples (typically n ≥ 30–50) to reliably estimate the covariance matrix and establish robust percentile thresholds.
- Assumes feature vectors are approximately multivariate normal; heavy-tailed or skewed distributions may inflate false positive outlier rate.
- DModX computation depends on principal component model quality; if PCA dimensionality reduction is poor, DModX may lose discriminative power.
- Thresholds (e.g., 95th percentile) are data-dependent and may be overly conservative or liberal if the reference distribution is itself contaminated with outliers.
- No explicit guidance is provided in the OUKS documentation on parameter selection, sensitivity analysis, or tuning for domain-specific metabolomic datasets.

## Evidence

- [other] Step 9 (Statistics) implements Hotelling Ellipse with T-squared statistic and DModX metric for sample outlier detection, generating per-sample outlier flags.: "Step 9 (Statistics) implements Hotelling Ellipse with T-squared statistic and DModX metric for sample outlier detection, generating per-sample outlier flags."
- [other] Calculate Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance. Compute DModX (distance to model in X-space) metric as the orthogonal distance of each sample from the principal component model subspace. Define outlier thresholds for T-squared (e.g., critical value from F-distribution or 95th percentile) and DModX (95th percentile or user-specified limit). Flag samples exceeding either threshold as outliers and generate per-sample outlier status (TRUE/FALSE) with associated scores.: "Calculate Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance. Compute DModX (distance to model in X-space) metric as the orthogonal distance of"
- [other] Load the preprocessed feature matrix (post-normalization from step 7) into R. Compute the mean vector and covariance matrix of the feature data. Output outlier flags, T-squared scores, and DModX scores to a tabular format.: "Load the preprocessed feature matrix (post-normalization from step 7) into R. Compute the mean vector and covariance matrix of the feature data. Output outlier flags, T-squared scores, and DModX"
- [discussion] "9. Statistics": Hotelling Ellipse with T-squared statistic and DModX metric: ""9. Statistics": Hotelling Ellipse with T-squared statistic and DModX metric"
