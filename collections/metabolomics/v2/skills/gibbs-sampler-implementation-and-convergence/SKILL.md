---
name: gibbs-sampler-implementation-and-convergence
description: Use when your metabolomics dataset contains missing values below a known detection limit (left-censored MNAR data), and you need to recover these values while respecting the truncation constraint.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3370
  tools:
  - R
  - GSimp (R package)
  - imputeLCMD (R package)
  - Trunc_KNN
  - glmnet (R package)
  - doParallel (R package)
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

# Gibbs sampler implementation and convergence

## Summary

Implement a Gibbs sampling algorithm to iteratively impute left-censored missing values in metabolomics datasets by alternating between sampling missing values from truncated normal distributions and updating posterior parameter estimates. Convergence is assessed via chain stabilization or maximum iteration count to ensure reliable imputation.

## When to use

Your metabolomics dataset contains missing values below a known detection limit (left-censored MNAR data), and you need to recover these values while respecting the truncation constraint. Use this skill when missingness is informative and biased toward the lower tail of the distribution, such as in LC/MS or GC/MS data with LOQ/LOD thresholds.

## When NOT to use

- Missing data are Missing Completely At Random (MCAR) or Missing At Random (MAR) without clear censoring — use simpler methods like kNN or multiple imputation instead.
- No detection limit threshold is known or missingess is not informative — the truncation bounds cannot be justified.
- Computational budget is extremely limited — Gibbs sampling requires multiple iterations and can be slow without parallel cores; consider QRILC or half-minimum substitution for rapid screening.

## Inputs

- metabolomics data matrix (rows=samples, columns=metabolite features)
- missing value positions (NA or zero encoding)
- detection limit threshold or quantile level
- initialization method ('qrilc', 'lsym', 'rsym', or pre-initialized data frame)
- lower bound (lo, default −∞ for left-censored)
- upper bound (hi, default minimum of non-missing values)

## Outputs

- imputed data matrix (same dimensions as input)
- Gibbs sampling trace array (optional: records iterations for specified missing elements)
- convergence diagnostics

## How to apply

Initialize the Gibbs sampler with prior parameters (mean and variance) for the metabolite distributions, then alternate between two steps: (1) impute missing values by sampling from a truncated normal distribution conditioned on the detection limit (lower bound = −∞, upper bound = minimum non-missing value or a quantile thereof), and (2) update posterior estimates of metabolite mean and variance from the completed data. Run the sampler for iters_all outer iterations (recommended ≥10), each containing iters_each inner iterations per missing variable (recommended ≥50), tracking convergence through chain stabilization diagnostics. Once converged, extract the final imputed matrix. Log-transform data before sampling and exponential-transform the result after convergence for non-normal metabolomics distributions.

## Related tools

- **GSimp (R package)** (Core implementation of Gibbs sampler with wrapper functions (GS_impute, pre_processing_GS_wrapper) for left-censored imputation) — https://github.com/WandeRum/GSimp
- **imputeLCMD (R package)** (Provides QRILC method for initialization and comparison)
- **Trunc_KNN** (Alternative kNN-based truncation imputation for method comparison)
- **glmnet (R package)** (Elastic net prediction model used within GSimp for posterior updates)
- **doParallel (R package)** (Enables parallel imputation of multiple missing variables across cores)

## Examples

```
result <- data_raw_log_sc %>% GS_impute(., iters_each=50, iters_all=10, initial=data_raw_log_qrilc_sc_df, lo=-Inf, hi='min', n_cores=2, imp_model='glmnet_pred')
```

## Evaluation signals

- Gibbs chain diagnostics: check for stabilization of posterior mean and variance estimates across iterations; visual inspection of trace plots should show no systematic drift in later iterations.
- Imputation accuracy on simulated data: compare imputed values to known ground truth using metrics like RMSE or correlation; GSimp typically outperforms QRILC and kNN-TN on MNAR metabolomics data.
- Missing value distribution: verify that imputed values fall below the detection limit threshold (hi parameter) and match the quantile structure of non-missing values.
- Convergence criterion met: confirm that iters_all and iters_each parameters resulted in chain stabilization (e.g., effective sample size > 1000 or Gelman-Rubin R̂ < 1.05 if available).
- Data recovery integrity: after exponential back-transformation, check that imputed metabolite values are positive and within the expected range for the metabolomics platform (LC/MS or GC/MS).

## Limitations

- Computational cost scales with matrix size and number of iterations; parallel computing (n_cores parameter) mitigates but does not eliminate this.
- Initialization method ('qrilc', 'lsym', 'rsym') can influence final results; sensitivity analysis is recommended for critical biomarkers.
- Convergence assessment is heuristic (e.g., chain stabilization or max iterations); formal diagnostics (Gelman-Rubin R̂, effective sample size) are not implemented in the provided wrapper.
- Extension to right-censored or MCAR/MAR data requires modification of bounds (lo, hi); the method is optimized for left-censored MNAR scenarios.
- No built-in handling of batch effects or instrumental drift; data should be normalized and corrected before imputation.

## Evidence

- [other] Run the Gibbs sampler iterative sampling loop, alternating between imputing missing values from a truncated normal distribution (conditioned on the detection limit) and updating the posterior estimates of metabolite parameters.: "alternating between imputing missing values from a truncated normal distribution (conditioned on the detection limit) and updating the posterior estimates of metabolite parameters"
- [other] Continue iterations until convergence is detected (e.g., chain stabilization or maximum iteration count reached).: "Continue iterations until convergence is detected (e.g., chain stabilization or maximum iteration count reached)"
- [readme] iters_each is the number of iterations for imputing each missing variable (default=100). iters_all is the number of iterations for imputing the whole data matrix (default=20). Although a large number of iterations (e.g., iters_all=20 and iters_each=100) is recommended for the convergence of MCMC, a smaller number of iterations (iters_all=10, iters_each=50) won't severely affect the imputation accuracy as we tested on the simulation data.: "iters_each is the number of iterations for imputing each missing variable (default=100). iters_all is the number of iterations for imputing the whole data matrix (default=20). Although a large number"
- [readme] lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part (notably, quantile values can be applied if minimum is too strict).: "lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part (notably, quantile values can be applied if minimum is too"
- [readme] Log transformation, Initialization, Centralization and scaling, Imputation using GSimp, Scaling recovery, Exponential recovery, Imputed data output.: "Log transformation (for non-normal data), Initialization for missing values (e.g., QRILC), Centralization and scaling (for elastic-net prediction), Imputation using GSimp, Scaling recovery,"
