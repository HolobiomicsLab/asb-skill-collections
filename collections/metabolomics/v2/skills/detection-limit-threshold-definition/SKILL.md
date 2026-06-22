---
name: detection-limit-threshold-definition
description: Use when when preparing metabolomics abundance tables with left-censored missingness (values below instrument detection limit or quantification limit) for imputation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GSimp.R
  - GSimp_evaluation.R
  - imputeLCMD (QRILC)
  - kNN-TN (Truncation k-nearest neighbors)
derived_from:
- doi: 10.1371/journal.pcbi.1005973
  title: GSimp
- doi: 10.1186/s12859-017-1547-6
  title: ''
evidence_spans:
- '**GSimp.R** contains the core functions for GSimp'
- GSimp.R contains the core functions for GSimp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gsimp_cq
    doi: 10.1371/journal.pcbi.1005973
    title: GSimp
  dedup_kept_from: coll_gsimp_cq
schema_version: 0.2.0
---

# Detection-Limit Threshold Definition

## Summary

Define and parameterize detection/quantification limits (LOD/LOQ) as the upper bound for left-censored missing values in metabolomics data, enabling proper constraint specification for imputation algorithms. This step operationalizes the biological and instrumental detection threshold as a computational boundary for missing-value simulation and bounds-constrained imputation.

## When to use

When preparing metabolomics abundance tables with left-censored missingness (values below instrument detection limit or quantification limit) for imputation. Triggered when you have metabolomics data with known or inferred LOD/LOQ thresholds and need to simulate MNAR missingness patterns or constrain imputation to respect instrumental detection limits.

## When NOT to use

- Input data already contains fully imputed or complete values with no missing data.
- Missingness is assumed MCAR/MAR and not mechanistically linked to detection limits.
- Right-censored data (e.g., values above an upper quantification limit) — use hi=Inf or hi='max' instead.

## Inputs

- Complete metabolomics abundance matrix (samples × metabolites)
- Detection limit specification (scalar, 'min', 'max', 'median', percentile, or feature-specific vector)
- Metadata on feature/sample selection for censoring (optional)

## Outputs

- Left-censored data matrix with values below LOD/LOQ replaced by NA
- Metadata recording threshold applied, affected features/samples, and missingness pattern
- Bounds vector for use in downstream imputation (hi parameter)

## How to apply

Define the detection limit as either an absolute value, a percentile of the non-missing distribution, or a feature-specific vector. In GSimp, this threshold is passed as the upper bound (hi parameter) to constrain imputed values: set hi='min' to use the minimum observed value per feature as the LOD, or hi=quantile(x, 0.1, na.rm=TRUE) to use a less-strict percentile-based threshold. The rationale is that left-censored observations represent measurements below the instrument's capability, so imputed values must respect this physical boundary. For MNAR simulation, apply the threshold uniformly across selected features and samples to create a realistic censoring pattern before benchmarking imputation methods.

## Related tools

- **GSimp.R** (Core imputation function accepting hi (upper bound) parameter to enforce detection-limit constraints during Gibbs sampling) — https://github.com/WandeRum/GSimp
- **GSimp_evaluation.R** (MNAR generation and evaluation module that simulates left-censored missingness using user-defined thresholds) — https://github.com/WandeRum/GSimp
- **imputeLCMD (QRILC)** (Quantile regression imputation for left-censored data; comparative baseline method)
- **kNN-TN (Truncation k-nearest neighbors)** (Newton-Raphson truncated mean/SD estimation for left-censored imputation; comparative baseline) — https://doi.org/10.1186/s12859-017-1547-6

## Examples

```
result <- data_raw_log_sc %>% GS_impute(., iters_each=50, iters_all=10, initial=data_raw_log_qrilc_sc_df, lo=-Inf, hi='min', n_cores=2, imp_model='glmnet_pred')
```

## Evaluation signals

- Threshold is correctly applied: verify that all imputed values respect the upper bound (imputed values ≤ hi for each feature).
- Missingness pattern matches specification: confirm NA positions align with features/samples selected for censoring and are below the threshold.
- Bounds metadata is recorded: missingness pattern, threshold values applied, number and identity of affected features/samples are logged.
- Reproducibility check: re-running imputation with the same threshold and seed produces identical or near-identical results.
- Comparison consistency: MNAR data generated with the same threshold yields similar imputation performance across methods (GSimp, QRILC, kNN-TN) when compared on simulation benchmarks.

## Limitations

- Threshold specification requires prior knowledge or estimation of LOD/LOQ; misspecification (e.g., threshold too loose or too strict) biases imputation and benchmark comparisons.
- Feature-specific thresholds assume heterogeneous detection limits across metabolites; if not available, a global threshold may oversimplify real instrumental behavior.
- The 'min' threshold choice may be too strict if the observed minimum is an outlier; quantile-based thresholds (e.g., 10th percentile) are recommended for robustness.
- This skill assumes left-censoring; right-censored data or mixed censoring patterns require different bound specifications and may violate method assumptions.

## Evidence

- [other] Define left-censoring threshold parameters (detection limit as a percentile or absolute value).: "Define left-censoring threshold parameters (detection limit as a percentile or absolute value)."
- [other] Replace values below the detection threshold with NA to simulate left-censored observations.: "Replace values below the detection threshold with NA to simulate left-censored observations."
- [readme] **lo** is the lower limits (default='-Inf') and **hi** (default='min') is the upper limits for missing values. These two arguments can be defined as -Inf/Inf/'min'/'max'/'median'/'mean' or any single determined value or a vector of values... Here, lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part.: "Here, lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part"
- [readme] The targeted LC/MS dataset contains 40 samples and 41 variables with 88 missing elements are failed to be quantified due to LOQ/LOD.: "The targeted LC/MS dataset contains 40 samples and 41 variables with 88 missing elements are failed to be quantified due to LOQ/LOD."
- [other] Return the censored data matrix and metadata (missingness pattern, threshold used, features/samples affected) for downstream imputation and evaluation.: "Return the censored data matrix and metadata (missingness pattern, threshold used, features/samples affected)"
