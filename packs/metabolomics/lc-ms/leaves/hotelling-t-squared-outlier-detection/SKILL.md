---
name: hotelling-t-squared-outlier-detection
description: Use when after data normalization (Step 7) on the preprocessed feature matrix when you need to identify and flag anomalous samples before statistical testing or biomarker discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R ≥4.1.2
  - R
  - OUKS (Omics Untargeted Key Script)
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Hotelling T-squared / DModX Outlier Detection

## Summary

Detect and flag outlier samples in untargeted LC-MS metabolomic datasets using Hotelling T-squared statistic combined with DModX (distance to model in X-space) metric. This multivariate approach identifies samples that deviate abnormally from the central tendency in feature space, protecting downstream statistical and biomarker discovery analyses from influential outliers.

## When to use

Apply this skill after data normalization (Step 7) on the preprocessed feature matrix when you need to identify and flag anomalous samples before statistical testing or biomarker discovery. Use it when you have a normalized feature matrix with multiple metabolomic features across biological samples and want to detect samples that are statistical outliers in multivariate space—typically before performing hypothesis tests or deriving classifier models.

## When NOT to use

- The input feature matrix has not yet been normalized; apply Step 7 (Normalization) first.
- Sample size is very small (n < 10), as covariance matrix estimation becomes unstable and thresholds less reliable.
- The feature matrix contains missing values; apply Step 3 (Imputation) before this skill.

## Inputs

- Normalized feature matrix (post-normalization from Step 7, numeric matrix or data.frame with samples as rows and metabolomic features as columns)

## Outputs

- Per-sample outlier flags (binary TRUE/FALSE vector)
- T-squared scores (numeric vector, one value per sample)
- DModX scores (numeric vector, one value per sample)
- Outlier detection summary table (tabular format with sample identifiers, outlier status, and associated scores)

## How to apply

Load the normalized feature matrix from Step 7 into R and compute the sample mean vector and covariance matrix. Calculate the Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance; define an outlier threshold (e.g., critical value from the F-distribution or 95th percentile of the T-squared distribution). Independently compute DModX as the orthogonal distance of each sample from the principal component model subspace and set a DModX threshold (typically the 95th percentile or a user-specified limit). Flag any sample exceeding either threshold as an outlier, generating a per-sample binary outlier status (TRUE/FALSE) along with the associated T-squared and DModX scores. Output these flags and scores in tabular format for downstream review and sample filtering.

## Related tools

- **R** (Core statistical computing environment for computing Mahalanobis distance, covariance matrices, and multivariate outlier statistics) — https://cloud.r-project.org/
- **OUKS (Omics Untargeted Key Script)** (Integrated R-based toolbox providing Step 9 (Statistics) implementation of Hotelling Ellipse with T-squared and DModX outlier detection) — https://github.com/plyush1993/OUKS

## Examples

```
# Load normalized feature matrix and compute Hotelling T² and DModX outliers
feature_matrix <- read.csv('normalized_features_step7.csv', row.names=1)
mean_vec <- colMeans(feature_matrix)
cov_matrix <- cov(feature_matrix)
inv_cov <- solve(cov_matrix)
hotelling_tsq <- mahalanobis(feature_matrix, mean_vec, cov_matrix)
outlier_threshold_t2 <- qf(0.95, df1=ncol(feature_matrix), df2=nrow(feature_matrix)-ncol(feature_matrix))
outlier_flags <- hotelling_tsq > outlier_threshold_t2
results <- data.frame(sample=rownames(feature_matrix), outlier_flag=outlier_flags, hotelling_tsq=hotelling_tsq)
write.csv(results, 'outlier_detection_results_step9.csv')
```

## Evaluation signals

- Verify that all samples receive a valid T-squared score and DModX score (no missing values in output unless input had structural issues).
- Check that the outlier flag distribution is reasonable (typically 5–10% of samples flagged when using 95th percentile thresholds, unless biological context suggests otherwise).
- Confirm that flagged outliers exhibit high values in at least one of the two metrics (T-squared OR DModX), indicating genuine multivariate anomalies rather than metric inconsistency.
- Inspect the range and distribution of T-squared and DModX scores; they should follow approximately chi-squared-like or F-like behavior with most samples clustered near the lower tail and a few extreme values in the tail.
- Validate that removal of flagged outliers does not dramatically change covariance structure or downstream statistical test results (e.g., effect sizes or p-values should stabilize or improve).

## Limitations

- Hotelling T-squared assumes multivariate normality; severe non-normality may inflate false positive rates. Combined use of DModX mitigates this somewhat by capturing orthogonal distance independent of normality assumption.
- Performance depends critically on threshold selection; the article mentions '95th percentile' or 'critical value from F-distribution' but does not provide extensive validation of optimal thresholds across different dataset types.
- Covariance matrix estimation is sensitive to sample size and collinearity among features; high feature dimensionality relative to sample count may lead to singular or unstable covariance matrices.
- The method does not inherently distinguish between biological outliers (samples with genuinely unusual biology) and technical outliers (instrument drift, contamination); manual review and metadata inspection are recommended.
- No explicit guidance provided in the article on how to handle batch effects before applying Hotelling detection; the workflow assumes batch-corrected data from Step 4.

## Evidence

- [other] Step 9 (Statistics) implements Hotelling Ellipse with T-squared statistic and DModX metric for sample outlier detection, generating per-sample outlier flags.: "Step 9 (Statistics) implements Hotelling Ellipse with T-squared statistic and DModX metric for sample outlier detection, generating per-sample outlier flags."
- [other] Calculate Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance. Compute DModX (distance to model in X-space) metric as the orthogonal distance of each sample from the principal component model subspace.: "Calculate Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance. Compute DModX (distance to model in X-space) metric as the orthogonal distance of"
- [other] Define outlier thresholds for T-squared (e.g., critical value from F-distribution or 95th percentile) and DModX (95th percentile or user-specified limit). Flag samples exceeding either threshold as outliers.: "Define outlier thresholds for T-squared (e.g., critical value from F-distribution or 95th percentile) and DModX (95th percentile or user-specified limit). Flag samples exceeding either threshold as"
- [other] Load the preprocessed feature matrix (post-normalization from step 7) into R. Compute the mean vector and covariance matrix of the feature data.: "Load the preprocessed feature matrix (post-normalization from step 7) into R. Compute the mean vector and covariance matrix of the feature data."
- [readme] The only requirements are to be familiar with the basic syntax of the R language, PC with Internet connection and Windows OS (desirable), RStudio and R (≥ 4.1.2).: "The only requirements are to be familiar with the basic syntax of the R language, PC with Internet connection and Windows OS (desirable), RStudio and R (≥ 4.1.2)."
