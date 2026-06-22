---
name: multivariate-statistical-quality-control
description: Use when after data normalization (Step 7) when you have a preprocessed feature matrix and need to identify samples that deviate significantly from the multivariate center of the data distribution due to instrumental drift, batch effects, sample degradation, or genuine biological outliers that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multivariate Statistical Quality Control with Hotelling T-squared and DModX

## Summary

Detects and flags outlier samples in LC-MS untargeted metabolomic datasets by computing Hotelling T-squared statistic (Mahalanobis distance) and DModX (distance to model in X-space) metrics, enabling removal of anomalous or batch-affected observations before downstream statistical modeling.

## When to use

Apply this skill after data normalization (Step 7) when you have a preprocessed feature matrix and need to identify samples that deviate significantly from the multivariate center of the data distribution due to instrumental drift, batch effects, sample degradation, or genuine biological outliers that warrant exclusion from group-level hypothesis testing.

## When NOT to use

- If the feature matrix has not yet been normalized (missing Step 7 normalization via Box-Cox or equivalent transformation).
- If sample size is very small (n < 10–15) relative to the number of features, rendering covariance matrix estimation unstable or singular.
- If you intend to retain all samples for downstream analysis regardless of multivariate distance; this skill is specifically designed to identify and filter outliers, not to score or rank samples in place.

## Inputs

- Preprocessed feature matrix (post-normalization, rows=samples, columns=metabolic features)
- Feature intensity values (numeric matrix, typically post-Box-Cox transformation)

## Outputs

- Per-sample Hotelling T-squared scores (numeric)
- Per-sample DModX scores (numeric, orthogonal distance)
- Binary outlier flags (logical TRUE/FALSE for each sample)
- Tabular outlier report with sample identifiers, T², DModX, and outlier status

## How to apply

Load the normalized feature matrix into R and compute the mean vector and inverse covariance matrix of the feature data. Calculate the Hotelling T-squared statistic for each sample using the Mahalanobis distance formula: T² = (x − μ)ᵀ Σ⁻¹ (x − μ), where x is the sample vector, μ is the mean, and Σ⁻¹ is the inverse covariance. In parallel, compute DModX as the orthogonal distance of each sample from the principal component model subspace. Define statistical thresholds: use the F-distribution critical value (e.g., α = 0.05) or the 95th percentile of the T² distribution for the T-squared threshold, and apply a 95th percentile cutoff (or user-specified limit) for DModX. Flag any sample exceeding either threshold as an outlier (TRUE/FALSE status), and output per-sample T² scores, DModX scores, and binary outlier flags in tabular format for review and potential removal before statistical testing.

## Related tools

- **R** (Host environment for computing covariance matrices, Mahalanobis distances, principal component analysis, and statistical threshold calculations) — https://cloud.r-project.org/
- **OUKS (Omics Untargeted Key Script)** (Step 9 (Statistics.R) implements Hotelling Ellipse with T-squared and DModX in integrated LC-MS metabolomic pipeline) — https://github.com/plyush1993/OUKS

## Examples

```
# Load normalized feature matrix and compute T-squared + DModX in R
data <- read.csv('normalized_features.csv', row.names=1)
mean_vec <- colMeans(data)
cov_mat <- cov(data)
inv_cov <- solve(cov_mat)
T_squared <- rowSums((data - mean_vec) * (data - mean_vec) %*% inv_cov)
outlier_flag <- T_squared > quantile(T_squared, 0.95)
write.csv(data.frame(sample=rownames(data), T_squared=T_squared, outlier=outlier_flag), 'outlier_report.csv')
```

## Evaluation signals

- Outlier flags are TRUE/FALSE binary with no missing values for any sample in the preprocessed matrix.
- T-squared scores follow an approximately F-distributed pattern when visualized as a Q–Q plot or histogram; extreme outliers cluster in the right tail.
- DModX scores are non-negative real numbers; samples flagged as outliers by either metric have scores exceeding the stated threshold (e.g., >95th percentile).
- The number and identity of flagged outliers are consistent across repeated runs with identical input data and parameters, confirming reproducibility.
- Removal of flagged outlier samples results in improved model fit (e.g., lower residual variance, higher R² in downstream PCA or regression) and more stable statistical inference in the next step (hypothesis testing).

## Limitations

- Covariance matrix singularity or near-singularity can occur if the number of features approaches or exceeds the number of samples; regularization (ridge penalty) or dimensionality reduction (PCA pre-filtering) may be required.
- The choice of T-squared and DModX thresholds (e.g., F-distribution quantile vs. 95th percentile) is partly arbitrary and can shift the number of detected outliers; sensitivity analysis and visual inspection of score distributions are recommended.
- Hotelling T-squared assumes multivariate normality within the non-outlier population; extreme deviations in feature distributions (e.g., heavy tails, zero-inflation) may violate this assumption and inflate false positive or false negative rates.
- DModX relies on a principal component model whose number of retained components must be specified (not explicitly detailed in the workflow); suboptimal component selection can miss or spuriously flag outliers in neglected high-variance directions.
- The method does not distinguish between technical outliers (instrumental artifacts, batch drift) and genuine biological outliers (disease heterogeneity); post-hoc review of flagged samples is essential before removal.

## Evidence

- [other] Step 9 (Statistics) implements Hotelling Ellipse with T-squared statistic and DModX metric for sample outlier detection, generating per-sample outlier flags.: "Step 9 (Statistics) implements Hotelling Ellipse with T-squared statistic and DModX metric for sample outlier detection, generating per-sample outlier flags."
- [other] Calculate Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance.: "Calculate Hotelling T-squared statistic for each sample using the inverse covariance matrix and Mahalanobis distance."
- [other] Compute DModX (distance to model in X-space) metric as the orthogonal distance of each sample from the principal component model subspace.: "Compute DModX (distance to model in X-space) metric as the orthogonal distance of each sample from the principal component model subspace."
- [other] Define outlier thresholds for T-squared (e.g., critical value from F-distribution or 95th percentile) and DModX (95th percentile or user-specified limit).: "Define outlier thresholds for T-squared (e.g., critical value from F-distribution or 95th percentile) and DModX (95th percentile or user-specified limit)."
- [other] Flag samples exceeding either threshold as outliers and generate per-sample outlier status (TRUE/FALSE) with associated scores.: "Flag samples exceeding either threshold as outliers and generate per-sample outlier status (TRUE/FALSE) with associated scores."
- [readme] "9. Statistics": Hotelling Ellipse with T-squared statistic and DModX metric: ""9. Statistics": Hotelling Ellipse with T-squared statistic and DModX metric"
