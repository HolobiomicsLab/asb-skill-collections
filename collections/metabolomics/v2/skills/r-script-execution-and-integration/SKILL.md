---
name: r-script-execution-and-integration
description: Use when when you have pre-written R functions organized across multiple .R files (e.g., GSimp.R, GSimp_evaluation.R, Impute_wrapper.
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
  - Impute_wrapper.R
  - Trunc_KNN/Imput_funcs.r
  - R (imputeLCMD package)
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

# R Script Execution and Integration

## Summary

Execute modular R scripts containing statistical functions and pipelines, then integrate their outputs into downstream analysis workflows. This skill is essential for reproducible metabolomics data imputation and evaluation where multiple specialized scripts (data preprocessing, imputation, evaluation) must be sourced and chained together in a controlled sequence.

## When to use

When you have pre-written R functions organized across multiple .R files (e.g., GSimp.R, GSimp_evaluation.R, Impute_wrapper.R) that need to be loaded into the same R session and applied sequentially to log-transformed, scaled metabolomics data matrices containing left-censored missing values, producing imputed matrices and performance metrics.

## When NOT to use

- Input metabolomics data is already imputed or contains no missing values — preprocessing and imputation steps become unnecessary.
- Missing values are known to be missing completely at random (MCAR) with non-informative bounds — GSimp is optimized for left-censored missing (MNAR with lower detection limit) and requires appropriate bounds (lo=-Inf, hi='min' by default).
- R environment lacks required package dependencies (Amelia, doParallel, FNN, foreach, ggplot2, glmnet, impute, imputeLCMD, missForest, randomForest, reshape2, ropls, vegan, knitr, pheatmap, abind, magrittr, markdown) — script sourcing will fail at first function call.

## Inputs

- metabolomics data matrix (CSV/TSV format, rows=samples, columns=metabolites) with missing values marked as NA
- R scripts containing imputation and evaluation functions (GSimp.R, GSimp_evaluation.R, Impute_wrapper.R, Trunc_KNN/Imput_funcs.r, MVI_global.R, Prediction_funcs.R)
- true/reference metabolomics data matrix (for evaluation against known values)

## Outputs

- imputed data matrix (CSV/TSV) with recovered values in original scale (not log-transformed)
- evaluation comparison table (CSV/TSV) documenting method-wise performance metrics (RMSE, bias) across GSimp, QRILC, and kNN-TN
- Gibbs sampler trace arrays (three-dimensional: std/yhat/yres × missing elements × MCMC iterations) for specified missing positions

## How to apply

First, set R options to suppress automatic string-to-factor conversion (options(stringsAsFactors = F)), then source each specialized script in dependency order (e.g., source('Trunc_KNN/Imput_funcs.r'), source('GSimp_evaluation.R'), source('GSimp.R')). Apply wrapper functions like pre_processing_GS_wrapper() to input data, which internally orchestrate log transformation, QRILC initialization, centering/scaling, Gibbs sampler imputation (GS_impute with parameters iters_each=50, iters_all=10, imp_model='glmnet_pred'), and recovery transformations (scale_recover, exponential back-transform). Finally, evaluate imputed outputs using evaluation functions from GSimp_evaluation.R by comparing against known true values with metrics like RMSE or bias, aggregating results into comparison tables across methods (GSimp, QRILC, kNN-TN).

## Related tools

- **GSimp.R** (Core Gibbs sampler imputation engine; contains GS_impute() and related MCMC functions for left-censored missing value recovery) — https://github.com/WandeRum/GSimp
- **GSimp_evaluation.R** (MNAR data generation and evaluation pipeline; computes performance metrics (RMSE, bias) against true values for method comparison) — https://github.com/WandeRum/GSimp
- **Impute_wrapper.R** (High-level wrapper functions (pre_processing_GS_wrapper); orchestrates log transformation, initialization, centering/scaling, and imputation in single call) — https://github.com/WandeRum/GSimp
- **Trunc_KNN/Imput_funcs.r** (kNN-TN imputation algorithm (truncation k-nearest neighbors); alternative method for comparison against GSimp and QRILC) — https://github.com/WandeRum/GSimp
- **R (imputeLCMD package)** (Provides impute.QRILC() function for quantile regression imputation initialization and wrapper method comparison)

## Examples

```
source('GSimp.R')
source('Impute_wrapper.R')
untargeted_data <- read.csv('untargeted_data.csv', row.names=1)
set.seed(123)
after_GS_imp <- pre_processing_GS_wrapper(untargeted_data)
```

## Evaluation signals

- All R scripts source without errors and all declared functions are callable in the R environment (check via ls() output after sourcing).
- Imputed data matrix has no NA values remaining, and dimensions match input (rows=samples, cols=metabolites); values are in original measurement scale (not log-transformed).
- Performance metrics (RMSE, bias) computed by GSimp_evaluation.R functions show GSimp outperforming or comparable to QRILC and kNN-TN on simulated MNAR data, with results aggregated into structured comparison table.
- Gibbs sampler trace arrays (if requested via gibbs parameter) show convergence: variance of sampled values across MCMC iterations decreases or stabilizes by iteration iters_all.
- Exponential back-transformation and scale recovery parameters are correctly applied: mean and SD of imputed values in recovered scale should match precomputed centralization/scaling parameters from log-transformed data.

## Limitations

- Large-scale data (>10,000 variables or >1,000 samples) may require substantial computational time; parallel computing (n_cores parameter) mitigates but does not eliminate this constraint.
- Method is optimized for left-censored missing (MNAR with lower detection limit); extension to right-censored or MCAR/MAR requires modification of bounds (lo, hi) and may reduce imputation accuracy if theoretical assumptions are violated.
- Initialization step (QRILC) must not introduce new NAs; if input data contains extreme sparsity (>80% missing per variable), QRILC may fail to estimate quantile regression parameters and crash.
- No automated convergence diagnostic provided; users must manually inspect gibbs traces or run sensitivity analyses to confirm MCMC mixing, especially for non-default iteration counts (iters_each, iters_all).
- Evaluation against true values requires synthetic/simulated data or availability of a held-out reference; real-world datasets may lack ground truth, limiting quantitative assessment of imputation accuracy.

## Evidence

- [readme] source('Trunc_KNN/Imput_funcs.r')
source('GSimp_evaluation.R')
source('GSimp.R'): "source('Trunc_KNN/Imput_funcs.r')
source('GSimp_evaluation.R')
source('GSimp.R')"
- [intro] GSimp provides data pre-processing, simulated data generation, MNAR generation, wrapper functions for different imputation methods (GSimp, QRILC, and kNN-TN) and evaluations: "data pre-processing, simulated data generation, missing not at random (MNAR) generation, wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and evaluations"
- [readme] All aboved steps has been wrapped into the pre_processing_GS_wrapper function for a one-step processing and imputation. The function will give the final imputed dataset.: "wrapped into the pre_processing_GS_wrapper function for a one-step processing and imputation. The function will give the final imputed dataset."
- [readme] GS_impute is the core function for the imputation of missing data and tracing the Gibbs sampler with certain missing positions.: "GS_impute is the core function for the imputation of missing data and tracing the Gibbs sampler"
- [readme] iters_each is the number of iterations for imputing each missing variable (default=100). iters_all is the number of iterations for imputing the whole data matrix (default=20). Although a large number of iterations (e.g., iters_all=20 and iters_each=100) is recommended for the convergence of MCMC, a smaller number of iterations (iters_all=10, iters_each=50) won't severely affect the imputation accuracy: "iters_each is the number of iterations for imputing each missing variable (default=100). iters_all is the number of iterations for imputing the whole data matrix (default=20)."
- [other] Execute the evaluation functions on each imputed matrix, computing performance metrics (e.g., root mean squared error, bias, or other quality measures) against the known true values.: "Execute the evaluation functions on each imputed matrix, computing performance metrics (e.g., root mean squared error, bias, or other quality measures) against the known true values."
