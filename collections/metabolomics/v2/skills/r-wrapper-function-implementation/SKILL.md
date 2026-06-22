---
name: r-wrapper-function-implementation
description: Use when when you have multiple imputation methods with different function signatures and parameter conventions that need to be applied to the same input data matrix, and you want to allow users or downstream code to switch between methods via a single method argument without rewriting calling code.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - GSimp.R
  - Impute_wrapper.R
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
---

# R wrapper function implementation

## Summary

Design and implement R wrapper functions that encapsulate method-specific imputation logic (GSimp, QRILC, kNN-TN) behind a uniform interface, enabling method dispatch, parameter binding, and standardized output formatting for left-censored missing value imputation in metabolomics data.

## When to use

When you have multiple imputation methods with different function signatures and parameter conventions that need to be applied to the same input data matrix, and you want to allow users or downstream code to switch between methods via a single method argument without rewriting calling code.

## When NOT to use

- Data is already fully complete or imputation is not needed; wrapper adds overhead without benefit.
- Missing mechanism is known to be Missing Completely At Random (MCAR) and simple statistical methods (e.g., listwise deletion) are sufficient for your analysis.
- Input is not a numeric matrix/data frame (e.g., sparse matrices, categorical data) unless you extend the wrapper to handle type conversion or method selection.

## Inputs

- data matrix or data frame with numeric values and NA for missing elements
- method name (string: 'GSimp', 'QRILC', 'kNN-TN')
- method-specific parameters (e.g., iters_each, iters_all, n_cores for GSimp; k, distance for kNN-TN)

## Outputs

- imputed data frame with NAs replaced by estimated values
- optional: MCMC trace array (gibbs_res) if tracing specific missing positions across iterations

## How to apply

Create a wrapper function that accepts the input data matrix and method-specific parameters. Parse the method argument to route to the appropriate imputation handler (GSimp, QRILC, or kNN-TN). Each wrapper should normalize the input format (e.g., ensure data frame or matrix representation), call the selected imputation function with its required parameters, and return output in a consistent format (data frame with imputed values replacing NAs). For example, the pre_processing_GS_wrapper integrates log-transformation, QRILC initialization, centralization/scaling, GSimp imputation with iters_each=50 and iters_all=10, and recovery steps into a single reproducible pipeline. Document the lo and hi bounds used (e.g., lo=-Inf, hi='min' for left-censored data) since these govern whether imputation respects detection limits or assumes MCAR/MAR.

## Related tools

- **GSimp.R** (Core imputation engine; defines GS_impute function with Gibbs sampler for left-censored MNAR imputation) — https://github.com/WandeRum/GSimp
- **Impute_wrapper.R** (Container for method wrapper functions including pre_processing_GS_wrapper; dispatches to GSimp, QRILC, kNN-TN based on method argument) — https://github.com/WandeRum/GSimp
- **imputeLCMD R package** (Provides impute.QRILC function for quantile regression imputation of left-censored data)
- **Trunc_KNN** (Provides imputeKNN function for truncation k-nearest neighbors imputation with correlation-based distance) — https://github.com/WandeRum/GSimp

## Examples

```
source('Impute_wrapper.R'); source('GSimp.R'); after_GS_imp <- pre_processing_GS_wrapper(untargeted_data)
```

## Evaluation signals

- Wrapper function returns a data frame with same dimensions as input; no NAs remain at positions specified in original NA_pos.
- Imputed values respect bounds: all imputed values fall between lo and hi (e.g., between -Inf and minimum for left-censored MNAR).
- Wrapper consistently handles all three methods (GSimp, QRILC, kNN-TN) without error and produces numeric output suitable for downstream analysis (e.g., scaling recovery, exponential transformation).
- Reproducibility: setting seed and applying wrapper to same input data yields identical imputed values across repeated runs.
- Pre-processing wrapper output matches expected workflow: log-transformed input → QRILC initialization → scaled GSimp imputation → scale/exp recovery yields final data in original scale space.

## Limitations

- Wrapper assumes input data is numeric; categorical or mixed-type data requires pre-processing outside the wrapper or extended type-handling logic.
- GSimp parameters (iters_each, iters_all, n_cores) require tuning; smaller iterations (iters_all=10, iters_each=50) trade accuracy for speed; convergence not guaranteed without domain knowledge of data.
- QRILC and kNN-TN assume left-censored MNAR; wrapper bounds (lo=-Inf, hi='min') may be too strict for right-censored or MCAR data; users must manually adjust lo and hi or choose alternative wrapper for different mechanisms.
- Parallel computing (n_cores parameter in GSimp) may not be faster on small datasets or high-memory systems; sequential imputation (n_cores=1) may be more appropriate for very small datasets.
- Wrapper does not validate that input data satisfies assumptions (e.g., sufficient non-missing data per variable for correlation estimation); failure modes include singular covariance matrices or convergence issues on sparse data.

## Evidence

- [other] Impute_wrapper.R contains wrapper functions that dispatch missing-value matrices to different imputation methods, including GSimp, QRILC, and kNN-TN, with pre_processing_GS_wrapper available as part of the wrapper function suite.: "Impute_wrapper.R contains wrapper functions that dispatch missing-value matrices to different imputation methods, including GSimp, QRILC, and kNN-TN, with pre_processing_GS_wrapper available"
- [readme] All aboved steps has been wrapped into the *pre_processing_GS_wrapper* function for a one-step processing and imputation. The function will give the final imputed dataset.: "All aboved steps has been wrapped into the *pre_processing_GS_wrapper* function for a one-step processing and imputation."
- [intro] Data pre-processing, simulated data generation, missing not at random (MNAR) generation, wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and evaluations of these methods.: "wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN)"
- [readme] Although a large number of iterations (e.g., iters_all=20 and iters_each=100) is recommended for the convergence of MCMC, a smaller number of iterations (iters_all=10, iters_each=50) won't severely affect the imputation accuracy as we tested on the simulation data.: "smaller number of iterations (iters_all=10, iters_each=50) won't severely affect the imputation accuracy"
- [readme] Here, lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part: "lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value"
- [other] Parse the method argument to route to the appropriate imputation handler (GSimp, QRILC, or kNN-TN). Call the selected imputation function with the input matrix and any method-specific parameters.: "Parse the method argument to route to the appropriate imputation handler (GSimp, QRILC, or kNN-TN). Call the selected imputation function"
