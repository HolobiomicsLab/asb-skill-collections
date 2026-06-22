---
name: posterior-parameter-estimation-for-metabolite-distributions
description: Use when you have metabolomics data with left-censored missing values (below detection limit) and need to impute them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - R
  - GSimp
  - R (base + imputeLCMD, doParallel)
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

# Posterior parameter estimation for metabolite distributions

## Summary

Estimate posterior mean and variance parameters of metabolite abundance distributions during iterative Gibbs sampling, conditioning on observed non-missing values and respecting left-censoring limits. This enables principled imputation of left-censored missing metabolites by sampling from truncated normal distributions informed by data-driven parameter estimates.

## When to use

Apply this skill when you have metabolomics data with left-censored missing values (below detection limit) and need to impute them. The skill is triggered when the Gibbs sampler enters its iterative loop and must alternate between imputing missing values and updating distributional parameters—you use it at each iteration to condition the truncated normal sampling on current posterior estimates rather than fixed priors.

## When NOT to use

- Data contains no left-censored missing values or missingness is not MNAR (missing not at random); use simpler initialization (e.g., half-minimum substitution) instead.
- Prior information on metabolite distributions is unavailable and sample size is too small to estimate reliable posterior parameters; consider fixed-parameter or empirical Bayes approaches.
- Computational resources are severely limited; full Gibbs sampling with per-iteration parameter updates is expensive—use kNN or quantile regression imputation as faster approximations.

## Inputs

- Log-transformed metabolomics data matrix (rows=samples, columns=metabolite features, with NA or zero encoding missing values)
- Initialization matrix (e.g., QRILC-imputed values for missing positions)
- Detection limit threshold (upper bound hi, lower bound lo for truncation)
- Prior hyperparameters for mean and variance (optional; can use empirical Bayes from observed data)

## Outputs

- Posterior mean and variance estimates for each metabolite at each iteration
- Imputed metabolomics data matrix with left-censored values drawn from updated truncated normal distributions
- Gibbs sampler chain traces (optional; records full trajectory of imputed values for specified positions across iterations)

## How to apply

At each Gibbs iteration, update the posterior estimates of mean and variance for each metabolite's distribution based on the current observed (non-missing) values and the most recent imputations. These posterior parameters are then used to define the truncated normal distribution from which new missing values are sampled, with the truncation bounds set by the detection limit (lo=-Inf, hi='min' for left-censored data). The iterative cycle continues until convergence—typically detected by chain stabilization or reaching a maximum iteration count (e.g., iters_all=10–20 outer iterations × iters_each=50–100 per-variable iterations). This Bayesian updating scheme ensures imputed values remain coherent with the inferred metabolite abundance distribution while respecting the censoring mechanism.

## Related tools

- **GSimp** (Core implementation of Gibbs sampler with posterior parameter updates; provides GS_impute() function and scale_recover() utilities) — https://github.com/WandeRum/GSimp
- **R (base + imputeLCMD, doParallel)** (Execution environment; imputeLCMD provides QRILC initialization; doParallel enables parallel per-variable imputation within iterations)

## Examples

```
result <- data_raw_log_sc %>% GS_impute(., iters_each=50, iters_all=10, initial=data_raw_log_qrilc_sc_df, lo=-Inf, hi='min', n_cores=2, imp_model='glmnet_pred')
```

## Evaluation signals

- Posterior variance estimates decrease with increasing sample size (asymptotic consistency check).
- Imputed values respect the left-censoring bound: all imputed values lie below the detection limit threshold (hi='min').
- Gibbs chain traces show convergence: posterior parameter updates stabilize after ~10–20 iterations; variance of traced imputations decreases over iterations.
- Downstream statistical tests (e.g., PCA, differential abundance) are robust to the choice of iters_all and iters_each (sensitivity analysis), indicating the imputation is not artifactually dependent on iteration count.
- Cross-validation on held-out non-missing values: imputation error (e.g., RMSE) on artificially masked non-missing data is comparable to or better than QRILC or kNN-TN baselines.

## Limitations

- Requires strong MNAR assumption (left-censoring mechanism); if missingness is MCAR or MAR, posterior parameters may be biased by selection effects.
- Computational cost scales quadratically with sample size and number of metabolites due to per-iteration parameter updates; parallel computing (n_cores > 1) is recommended.
- Convergence depends on initialization quality; poor QRILC or LSYM initialization can lead to slow mixing or biased posterior estimates.
- Assumes metabolite abundances follow a (log-)normal distribution after transformation; heavily skewed or multimodal distributions may violate this assumption.
- Detection limit must be specified accurately (hi='min' assumes the minimum observed value is the true limit); misspecification can bias imputation.

## Evidence

- [other] Initialize the Gibbs sampler with prior parameters for mean and variance of the metabolite distribution. Run the Gibbs sampler iterative sampling loop, alternating between imputing missing values from a truncated normal distribution (conditioned on the detection limit) and updating the posterior estimates of metabolite parameters.: "Initialize the Gibbs sampler with prior parameters for mean and variance of the metabolite distribution. Run the Gibbs sampler iterative sampling loop, alternating between imputing missing values"
- [other] GSimp implements a Gibbs sampler based approach for left-censored missing value imputation, with core functions provided in GSimp.R that enable application to metabolomics datasets.: "GSimp implements a Gibbs sampler based approach for left-censored missing value imputation, with core functions provided in GSimp.R"
- [readme] lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part: "lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part"
- [readme] iters_each is the number of iterations for imputing each missing variable (default=100). iters_all is the number of iterations for imputing the whole data matrix (default=20).: "iters_each is the number of iterations for imputing each missing variable (default=100). iters_all is the number of iterations for imputing the whole data matrix (default=20)."
- [readme] Although a large number of iterations (e.g., iters_all=20 and iters_each=100) is recommended for the convergence of MCMC, a smaller number of iterations (iters_all=10, iters_each=50) won't severely affect the imputation accuracy as we tested on the simulation data.: "Although a large number of iterations (e.g., iters_all=20 and iters_each=100) is recommended for the convergence of MCMC, a smaller number of iterations won't severely affect imputation accuracy"
