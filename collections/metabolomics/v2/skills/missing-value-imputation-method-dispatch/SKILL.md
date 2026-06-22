---
name: missing-value-imputation-method-dispatch
description: Use when you have a metabolomics data matrix with missing-not-at-random (MNAR) left-censored values and need to apply multiple imputation methods to the same data in a standardized way, compare their outputs, or integrate the imputation step into a larger pre-processing pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - R
  - Impute_wrapper.R
  - GSimp.R
  - GSimp_evaluation.R
  - imputeLCMD R package
  - Trunc_KNN
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

# missing-value-imputation-method-dispatch

## Summary

Route a missing-value matrix to one of multiple left-censored imputation methods (GSimp, QRILC, kNN-TN) via a wrapper function that handles method selection, parameter passing, and output collection. This skill is essential when comparing or selecting the best imputation strategy for metabolomics data with left-censored missingness.

## When to use

You have a metabolomics data matrix with missing-not-at-random (MNAR) left-censored values and need to apply multiple imputation methods to the same data in a standardized way, compare their outputs, or integrate the imputation step into a larger pre-processing pipeline. The missing values must represent values below a detection limit (LOQ/LOD) rather than random missingness.

## When NOT to use

- Your data contains MCAR (missing completely at random) or MAR (missing at random) missingness rather than MNAR left-censored values — use non-truncated imputation methods (e.g., Amelia, missForest) with bounds set to (-∞, +∞) instead.
- Your data are already fully imputed or contain no missing values — the wrapper is designed only for datasets with NA entries that require imputation.
- You are comparing imputation methods and need traceability of Gibbs sampler convergence — you must configure the wrapper to set the `gibbs` parameter to record missing element trajectories across MCMC iterations.

## Inputs

- data matrix (data.frame or matrix) with missing values as NA
- method parameter (string: 'GSimp', 'QRILC', 'kNN-TN', or 'HM')
- optional: imputation-specific parameters (e.g., iters_each, iters_all, initial, lo, hi for GSimp)
- optional: initialization method or pre-imputed matrix (e.g., QRILC-imputed values for scaling reference)

## Outputs

- imputed data matrix (data.frame) with no NA values
- method identifier label for result tracking
- optional: Gibbs sampler trace arrays (gibbs_res) if tracing specified missing positions

## How to apply

Load the log-transformed, initialized, and scaled data matrix (or raw matrix if using a full wrapper) into the dispatch function along with a method identifier string ('GSimp', 'QRILC', or 'kNN-TN'). Parse the method argument to route execution to the appropriate handler function. For GSimp, configure bounds (lo=-Inf, hi='min' for left-censored data), iteration counts (e.g., iters_each=50, iters_all=10), and prediction model (e.g., 'glmnet_pred'). For QRILC and kNN-TN, apply log-transformation before routing and exponential transformation after imputation. Capture the imputed matrix output from the selected method and return it indexed by method name. The wrapper abstracts method-specific preprocessing requirements (scaling, transformation, initialization) so that downstream evaluation functions can consume standardized outputs.

## Related tools

- **Impute_wrapper.R** (Contains the wrapper functions that dispatch method selection and route matrices to GSimp, QRILC, kNN-TN handlers; includes pre_processing_GS_wrapper for one-step preprocessing and GSimp imputation) — https://github.com/WandeRum/GSimp
- **GSimp.R** (Provides the core GS_impute function implementing Gibbs sampler MNAR imputation with configurable bounds, iterations, and prediction models) — https://github.com/WandeRum/GSimp
- **GSimp_evaluation.R** (Contains MNAR generation and evaluation functions to assess performance metrics (RMSE, bias) across imputed matrices from all dispatched methods) — https://github.com/WandeRum/GSimp
- **imputeLCMD R package** (Provides impute.QRILC function used by the QRILC wrapper for quantile regression imputation of left-censored data)
- **Trunc_KNN** (Contains imputeKNN function and truncation-based kNN imputation algorithm used by the kNN-TN wrapper (Shah et al., 2017)) — https://github.com/WandeRum/GSimp

## Examples

```
source('Impute_wrapper.R'); source('GSimp.R'); after_GS_imp <- pre_processing_GS_wrapper(untargeted_data); after_QRILC_imp <- sim_QRILC_wrapper(log(untargeted_data)) %>% exp(); after_trKNN_imp <- sim_trKNN_wrapper(log(untargeted_data)) %>% exp()
```

## Evaluation signals

- Verify that the returned matrix has no NA values and the same dimensions as the input data.
- Confirm that the method label matches the requested method and is correctly indexed in the output (e.g., results_GSimp, results_QRILC).
- Check that log-transformation was applied before dispatch to QRILC and kNN-TN and that exponential transformation was applied to their outputs to recover original scale.
- For GSimp, validate that the imputed matrix respects the bounds (lo=-Inf, hi='min') by confirming that no imputed left-censored values exceed the minimum of the non-missing values in their respective variables.
- Compare imputed values against known true values (using simulated data) by computing RMSE or bias; dispatch success is signaled by method-comparable performance metrics reported by GSimp_evaluation.R functions.

## Limitations

- The wrapper assumes input data has been log-transformed for non-normal metabolomics distributions; if data violate normality assumptions post-transformation, imputation accuracy may degrade.
- QRILC and kNN-TN require pre-initialization (e.g., QRILC imputation or quantile-based fill) before scaling and Gibbs sampling; poor initialization may bias final results.
- GSimp convergence depends on iteration counts (iters_each, iters_all); the README notes that smaller iterations (iters_all=10, iters_each=50) will not severely affect accuracy but may under-converge for highly sparse datasets.
- kNN-TN uses fixed k=3 neighbors in the README example; this parameter is not exposed as a wrapper argument, limiting adaptability to datasets with varying sparsity or correlation structure.
- The wrapper does not handle missing values in covariates or sample metadata — only the main data matrix is imputed.

## Evidence

- [other] Impute_wrapper.R contains wrapper functions that dispatch missing-value matrices to different imputation methods, including GSimp, QRILC, and kNN-TN, with pre_processing_GS_wrapper available as part of the wrapper function suite.: "Impute_wrapper.R contains wrapper functions that dispatch missing-value matrices to different imputation methods, including GSimp, QRILC, and kNN-TN"
- [readme] The README describes wrapper functions for different imputation methods in the context of the GSimp approach.: "wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN)"
- [readme] The pre_processing_GS_wrapper function unifies preprocessing and method dispatch in one call.: "All aboved steps has been wrapped into the *pre_processing_GS_wrapper* function for a one-step processing and imputation."
- [readme] Specific bounds are configured for left-censored missing values where the upper bound is the minimum.: "lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part"
- [readme] The wrapper implementation shows method-specific preprocessing (log-transformation, QRILC initialization, scaling, then GSimp imputation).: "Log transformation # data_raw_log <- data_raw %>% log() # Initialization # data_raw_log_qrilc <- impute.QRILC(data_raw_log) %>% extract2(1) # Centralization and scaling"
- [readme] Comparison of three different imputation methods via wrappers is demonstrated in the README.: "We compared GSimp with other left-censored missing imputation/substitution methods: QRILC, kNN-TN, and HM"
- [readme] The iteration parameters control convergence of the Gibbs sampler within the wrapper.: "iters_each is the number of iterations for imputing each missing variable (default=100). iters_all is the number of iterations for imputing the whole data matrix (default=20)."
