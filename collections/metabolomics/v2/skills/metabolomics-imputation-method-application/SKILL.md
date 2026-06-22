---
name: metabolomics-imputation-method-application
description: Use when your metabolomics dataset (LC/MS or GC/MS) contains missing values encoded as NA or zero that represent compounds below the instrument's limit of detection (LOD) or limit of quantification (LOQ), rather than values missing completely at random.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - GSimp
  - imputeLCMD (R package)
  - kNN-TN (Truncation k-nearest neighbors)
  - 'R (base and packages: Amelia, doParallel, FNN, glmnet, missForest, ropls, vegan)'
  techniques:
  - LC-MS
  - GC-MS
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

# metabolomics-imputation-method-application

## Summary

Apply Gibbs sampler-based or alternative imputation methods to recover left-censored missing values in metabolomics data matrices, where missingness is caused by detection limits below which metabolite concentrations cannot be quantified. This skill encompasses method selection, preprocessing, parameter tuning, and convergence assessment to produce complete imputed datasets suitable for downstream statistical analysis.

## When to use

Your metabolomics dataset (LC/MS or GC/MS) contains missing values encoded as NA or zero that represent compounds below the instrument's limit of detection (LOD) or limit of quantification (LOQ), rather than values missing completely at random. Use this skill when you need to impute these left-censored values before multivariate analysis, and you have a matrix with rows=samples and columns=metabolite features with known or estimated detection thresholds for each variable.

## When NOT to use

- Your missing values are missing completely at random (MCAR) or missing at random (MAR) without a known detection limit—use non-informative bounds (lo=-Inf, hi=+Inf) or MCAR-specific methods instead.
- Your data are already fully imputed or contain no missing values—there is nothing to impute.
- You need to impute right-censored data (e.g., upper truncation)—swap the initialization method to 'rsym' and set hi=Inf, lo='max'.

## Inputs

- metabolomics data matrix with rows=samples, columns=metabolite features (CSV or data frame format)
- matrix with missing values encoded as NA or zero
- detection limit threshold values per metabolite (scalar or per-variable vector)
- initial imputed values or initialization method name ('qrilc', 'lsym', 'rsym')

## Outputs

- imputed metabolomics data matrix (same dimensions, numeric, no NA)
- Gibbs sampler chain trace (3D array: std/yhat/yres × missing positions × iterations) if tracing enabled
- scaling/centering parameters if recovery to original scale needed

## How to apply

First, perform data preprocessing: log-transform the raw intensity matrix (for non-normal distribution), initialize missing values using QRILC imputation, then center and scale the data. Next, select an imputation method appropriate to your missingness mechanism—GSimp (Gibbs sampler) for MNAR data with known detection limits, QRILC for quantile-based truncated sampling, or kNN-TN for correlation-driven approaches. For GSimp specifically, set the upper bound (hi) to the minimum non-missing value per variable (or a quantile like 10th percentile if minimum is too strict) and lower bound (lo) to -Inf; run the iterative sampler with iters_all=10–20 and iters_each=50–100 until chain stabilization. After imputation, reverse the transformations (scaling recovery, then exponential transformation) to return to original scale. Compare methods using MNAR evaluation functions if ground-truth missingness positions are available or simulated.

## Related tools

- **GSimp** (Core Gibbs sampler imputation engine with wrapper functions (GS_impute) and preprocessing (pre_processing_GS_wrapper)) — https://github.com/WandeRum/GSimp
- **imputeLCMD (R package)** (Provides QRILC (Quantile Regression Imputation of Left-Censored data) method for initialization and comparison)
- **kNN-TN (Truncation k-nearest neighbors)** (Alternative left-censored imputation via truncated distribution estimation and correlation-based kNN) — https://github.com/WandeRum/GSimp
- **R (base and packages: Amelia, doParallel, FNN, glmnet, missForest, ropls, vegan)** (Execution environment; parallel computing, elastic-net prediction, multivariate analysis)

## Examples

```
source('GSimp.R'); after_GS_imp <- pre_processing_GS_wrapper(untargeted_data); # or directly: result <- GS_impute(data_scaled, iters_each=50, iters_all=10, initial=data_qrilc, lo=-Inf, hi='min', n_cores=2, imp_model='glmnet_pred')
```

## Evaluation signals

- Imputed matrix has no NA or zero values and matches input dimensions; all previously missing positions are now populated with numeric values within the detectable range of the metabolite.
- If ground-truth missingness is available (e.g., simulation data), compare imputed values to true values using RMSE, bias, or correlation; GSimp should outperform QRILC and kNN-TN on MNAR data.
- Gibbs sampler chain trace (gibbs_res) shows stabilization over iterations (yhat and yres converge, std plateaus); no divergence or oscillation indicates convergence.
- Log-scale imputed values after centering/scaling are plausible given the distribution of non-missing values—visually, density plots of imputed values should overlap with non-missing kernel density.
- Downstream multivariate analysis (e.g., PCA, OPLS-DA with ropls) on imputed data produces stable loadings and scores compared to other imputation methods; reproducibility across random seeds is high when seed is set.

## Limitations

- GSimp convergence depends on iteration counts (iters_all, iters_each); smaller counts (e.g., iters_all=10, iters_each=50) are faster but may not fully stabilize the Markov chain, though testing shows minimal accuracy loss.
- Method requires reliable detection limit (hi/lo bounds); if bounds are poorly estimated, imputation bias increases. The default hi='min' may be too strict for some distributions—quantile-based thresholds (e.g., 10th percentile) may be preferable.
- Parallel computing (n_cores > 1) imputes all missing variables simultaneously, sequential mode imputes from least to most missing; choice affects memory usage and iteration order but not final accuracy.
- The wrapper function pre_processing_GS_wrapper uses elastic-net prediction (imp_model='glmnet_pred'); if multicollinearity or overfitting is severe, other prediction models (e.g., randomForest) in Prediction_funcs.R may be needed.
- GSimp assumes metabolite concentrations follow a truncated normal distribution; severely skewed or multimodal distributions may not be well represented, and the method is specifically designed for MNAR data with left-censoring (not MCAR/MAR).

## Evidence

- [other] GSimp implements a Gibbs sampler based approach for left-censored missing value imputation, with core functions provided in GSimp.R that enable application to metabolomics datasets.: "GSimp implements a Gibbs sampler based approach for left-censored missing value imputation, with core functions provided in GSimp.R that enable application to metabolomics datasets."
- [other] Run the Gibbs sampler iterative sampling loop, alternating between imputing missing values from a truncated normal distribution (conditioned on the detection limit) and updating the posterior estimates of metabolite parameters.: "Run the Gibbs sampler iterative sampling loop, alternating between imputing missing values from a truncated normal distribution (conditioned on the detection limit) and updating the posterior"
- [readme] data pre-processing, simulated data generation, missing not at random (MNAR) generation, wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and evaluations of these methods.: "data pre-processing, simulated data generation, missing not at random (MNAR) generation, wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and evaluations"
- [readme] Log transformation, Initialization for missing values (e.g., QRILC), Centralization and scaling (for elastic-net prediction), Imputation using GSimp, Scaling recovery, Exponential recovery: "Log-transformation (for non-normal data), Initialization for missing values (e.g., QRILC), Centralization and scaling (for elastic-net prediction), Imputation using GSimp, Scaling recovery,"
- [readme] lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part: "lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part"
- [readme] iters_each is the number of iterations for imputing each missing variable (default=100). iters_all is the number of iterations for imputing the whole data matrix (default=20).: "iters_each is the number of iterations for imputing each missing variable (default=100). iters_all is the number of iterations for imputing the whole data matrix (default=20)."
- [readme] Although a large number of iterations (e.g., iters_all=20 and iters_each=100) is recommended for the convergence of MCMC, a smaller number of iterations (iters_all=10, iters_each=50) won't severely affect the imputation accuracy.: "Although a large number of iterations (e.g., iters_all=20 and iters_each=100) is recommended for the convergence of MCMC, a smaller number of iterations (iters_all=10, iters_each=50) won't severely"
