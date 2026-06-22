---
name: imputation-algorithm-selection
description: Use when you have a metabolomics dataset with left-censored missing values (e.g., below limit of quantification in LC/MS or GC/MS) and need to evaluate multiple imputation approaches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GSimp.R
  - Impute_wrapper.R
  - imputeLCMD R package
  - Trunc_KNN/Imput_funcs.r
derived_from:
- doi: 10.1371/journal.pcbi.1005973
  title: GSimp
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1005973
  all_source_dois:
  - 10.1371/journal.pcbi.1005973
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# imputation-algorithm-selection

## Summary

Select and dispatch missing-value matrices to appropriate MNAR imputation methods (GSimp, QRILC, kNN-TN) based on data characteristics and missingness mechanism. This skill routes preprocessed metabolomics data through method-specific wrapper functions to produce algorithm-specific imputed matrices for downstream comparison and evaluation.

## When to use

You have a metabolomics dataset with left-censored missing values (e.g., below limit of quantification in LC/MS or GC/MS) and need to evaluate multiple imputation approaches. Select this skill when you must compare GSimp (Gibbs sampler with elastic-net prediction), QRILC (quantile regression with truncated sampling), or kNN-TN (truncation k-nearest neighbors) on the same input matrix and retain separate imputed outputs for each method to assess performance differences.

## When NOT to use

- Input data contains only MCAR (missing completely at random) or MAR (missing at random) patterns with no left-censoring; GSimp's truncated bounds (lo=-Inf, hi='min') are designed for MNAR left-censored data and will not provide additional benefit over simpler methods.
- Imputed output is already produced by a single method and no algorithm comparison is required; this skill is for dispatch and multi-method evaluation, not single-pass imputation.
- Data has not been log-transformed or pre-initialized; the wrapper functions assume log-scale preprocessing and will produce incorrect scale-recovery steps if applied to raw-scale input.

## Inputs

- Log-transformed metabolomics matrix (samples × variables, numeric)
- QRILC pre-initialized matrix with missing values re-introduced at original NA positions
- Centralized and scaled data frame with scale/centering parameters recorded
- NA position matrix (row-column indices of missing elements)

## Outputs

- GSimp-imputed matrix (post-scale-recovery, post-exponential-recovery)
- QRILC-imputed matrix (post-exponential-recovery)
- kNN-TN-imputed matrix (post-exponential-recovery)
- Method-indexed list or separate CSV files of imputed matrices for comparison

## How to apply

Begin with log-transformed, QRILC-initialized, and centrally-scaled data. For each imputation method, invoke its corresponding wrapper function: (1) GSimp via pre_processing_GS_wrapper with parameters iters_each=50, iters_all=10, imp_model='glmnet_pred', lo=-Inf, hi='min' for left-censored bounds; (2) QRILC via sim_QRILC_wrapper for direct quantile-regression imputation; (3) kNN-TN via sim_trKNN_wrapper with k=3 and distance='truncation'. Record the NA position matrix before imputation, apply each method independently to the same initialized data, and recover scale/log transformation post-imputation. The choice between methods depends on computational budget (GSimp requires more iterations for MCMC convergence but provides uncertainty estimates) and whether truncated mean estimation (kNN-TN) or regression quantiles (QRILC) better match your data distribution assumptions.

## Related tools

- **GSimp.R** (Core function library for Gibbs sampler imputation; contains GS_impute() for MCMC-based left-censored value sampling) — https://github.com/WandeRum/GSimp
- **Impute_wrapper.R** (Dispatch and wrapper functions for method routing; contains pre_processing_GS_wrapper, sim_QRILC_wrapper, and sim_trKNN_wrapper) — https://github.com/WandeRum/GSimp
- **imputeLCMD R package** (Provides impute.QRILC() function for quantile-regression-based left-censored imputation)
- **Trunc_KNN/Imput_funcs.r** (kNN-TN algorithm implementation with imputeKNN() for truncation-based k-nearest-neighbor imputation) — https://github.com/WandeRum/GSimp

## Examples

```
source('Impute_wrapper.R'); source('GSimp.R'); source('Trunc_KNN/Imput_funcs.r'); after_GS_imp <- pre_processing_GS_wrapper(untargeted_data); after_QRILC_imp <- sim_QRILC_wrapper(log(untargeted_data)) %>% exp(); after_trKNN_imp <- sim_trKNN_wrapper(log(untargeted_data)) %>% exp()
```

## Evaluation signals

- Each method produces a complete imputed matrix with no remaining NA values at original missing positions; verify by intersecting output matrix NA positions with input NA positions (should be disjoint).
- Scale recovery post-imputation is consistent: verify that mean and variance of non-missing features match pre-scaling values (using recorded param_df) within numerical tolerance.
- Imputed values for left-censored positions fall within expected bounds: GSimp and QRILC imputed values should be ≤ minimum of non-missing data in each variable (hi='min' constraint); kNN-TN values should reflect truncated distribution estimates.
- Gibbs sampler convergence (GSimp only): check that repeated imputations with different random seeds produce stable imputed values at traced positions (gibbs_res output); standard deviation of traced elements should stabilize across iterations.
- Method-specific output schemas are met: GSimp returns list with data_imp and gibbs_res; QRILC and kNN-TN return imputed data frame only.

## Limitations

- GSimp convergence requires tuning iters_each and iters_all; default iters_all=10, iters_each=50 is a compromise between speed and convergence and may not be sufficient for high-dimensional or extremely sparse data. Larger iterations (iters_all=20, iters_each=100) are recommended for critical analyses but increase runtime quadratically.
- kNN-TN truncated mean estimation assumes Pearson correlation structure and may perform poorly on metabolites with non-linear or multimodal distributions after log transformation.
- QRILC imputation assumes that quantile regression surfaces are smooth; performance degrades when variables have extreme outliers or bimodal distributions that violate underlying quantile regression assumptions.
- All methods assume that log transformation linearizes the relationship between features and makes residuals approximately normal; log-transformation may not be appropriate for datasets with zero or negative values, or for very sparse omics data where most samples are below detection limit.
- The wrapper functions are specific to left-censored MNAR data (lo=-Inf, hi='min'); extending to right-censored or MCAR/MAR data requires parameter reconfiguration (lo/hi bounds, initial method) and may invalidate the preprocessing pipeline.

## Evidence

- [intro] wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and evaluations of these methods: "GSimp provides data pre-processing, simulated data generation, MNAR generation, wrapper functions for different imputation methods (GSimp, QRILC, and kNN-TN) and evaluations of these"
- [readme] Impute_wrapper.R dispatches to GSimp, QRILC, kNN-TN with pre_processing_GS_wrapper: "**Impute_wrapper.R** contains wrapper functions for different imputation methods (contains *pre_processing_GS_wrapper*)."
- [readme] pre_processing_GS_wrapper orchestrates log transformation, QRILC initialization, scaling, GSimp imputation, and scale/log recovery: "All aboved steps has been wrapped into the *pre_processing_GS_wrapper* function for a one-step processing and imputation. The function will give the final imputed dataset."
- [readme] GSimp parameters: iters_each controls per-variable iterations, iters_all controls full-matrix iterations, lo/hi set truncation bounds for left-censored data: "**iters_each** is the number of iterations for imputing each missing variable (default=100). **iters_all** is the number of iterations for imputing the whole data matrix (default=20). **lo** is the"
- [readme] QRILC and kNN-TN are compared as alternative left-censored methods using wrapper functions on log-transformed data with exponential recovery: "data_raw_log <- untargeted_data %>% log()
after_trKNN_imp <- sim_trKNN_wrapper(data_raw_log) %>% data.frame() %>% exp()
after_QRILC_imp <- sim_QRILC_wrapper(data_raw_log) %>% exp()"
