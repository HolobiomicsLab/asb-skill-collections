---
name: truncated-normal-distribution-sampling
description: Use when imputing left-censored missing values in metabolomics data where missingness is caused by values falling below the limit of quantification (LOQ) or limit of detection (LOD). The input matrix should have missing values flagged as NA, with a defined upper bound (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - GSimp
  - R (imputeLCMD package, truncated distributions)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Truncated-Normal-Distribution Sampling

## Summary

Sample missing values from a truncated normal distribution conditioned on detection limits (lower and upper bounds) during iterative Gibbs sampling for left-censored missing value imputation in metabolomics data. This approach preserves the constraint that imputed values cannot fall below the instrument's detection limit.

## When to use

Apply this skill when imputing left-censored missing values in metabolomics data where missingness is caused by values falling below the limit of quantification (LOQ) or limit of detection (LOD). The input matrix should have missing values flagged as NA, with a defined upper bound (e.g., minimum observed value per metabolite) and lower bound (typically −∞ for left-censored data). Use this within an iterative Gibbs sampler loop where you alternate between sampling missing values and updating posterior parameter estimates.

## When NOT to use

- Do not use if missing values are missing completely at random (MCAR) or missing at random (MAR) without a known detection limit — use non-truncated normal or other MCAR-appropriate methods instead.
- Do not use if the data have already been imputed or filtered to remove missing values — this skill requires the original missing value positions and bounds.
- Do not use if you lack a defensible upper bound (detection limit) for truncation; ad hoc choices can introduce bias.

## Inputs

- Metabolomics data matrix (rows=samples, columns=metabolite features) with missing values encoded as NA
- Detection limit threshold per metabolite (upper bound for left-censored imputation)
- Posterior estimates of mean and variance for each metabolite from non-missing data
- Lower and upper truncation bounds (lo, hi) — typically lo=−∞ and hi='min' for left-censored data

## Outputs

- Imputed values drawn from truncated normal distribution for each missing cell
- Updated Gibbs chain trace (mean, predicted value, sampled value) for specified missing elements across iterations
- Converged imputed data matrix with no remaining NA values

## How to apply

During each Gibbs iteration, for each metabolite with missing values, draw samples from a truncated normal distribution with mean and variance estimated from the current non-missing observations, constrained by the detection limit bounds (lo and hi). The truncation ensures imputed values respect the censoring mechanism: for left-censored data, set lo=−∞ and hi to the minimum observed value (or a quantile like the 10th percentile) of that metabolite. Repeat this sampling across multiple iterations (e.g., iters_each=50 iterations per variable, iters_all=10 iterations across the full matrix) until the Gibbs chain stabilizes. The rationale is that truncated normal sampling preserves the distributional assumptions of the metabolite measurements while honoring the physical constraint that undetected values must lie below the detection threshold.

## Related tools

- **GSimp** (Implements Gibbs sampler with truncated normal sampling as core imputation engine for left-censored metabolomics data) — https://github.com/WandeRum/GSimp
- **R (imputeLCMD package, truncated distributions)** (Provides base functions for sampling from truncated normal distributions and prior parameter estimation)

## Examples

```
result <- data_raw_log_sc %>% GS_impute(., iters_each=50, iters_all=10, initial=data_raw_log_qrilc_sc_df, lo=-Inf, hi='min', n_cores=2, imp_model='glmnet_pred')
```

## Evaluation signals

- Verify that imputed values fall within the specified truncation bounds [lo, hi] for every missing cell.
- Check that the Gibbs chain trace (gibbs_res output) shows stabilization of the mean and predicted value estimates across iterations, indicating convergence.
- Compare the distributional shape of imputed values (kernel density plot) with non-missing values to confirm plausible recovery of the left tail below the detection limit.
- Validate imputation accuracy on a hold-out subset by comparing imputed values to known left-censored true values (in simulation studies) using RMSE or correlation metrics.
- Confirm that the final imputed matrix has no remaining NA values and reasonable ranges (e.g., log-scale imputed values are numeric and finite).

## Limitations

- Truncated normal sampling assumes the underlying metabolite distribution is approximately normal (on the log scale); non-normal distributions may lead to poor imputation.
- Choice of upper bound (hi parameter) is critical: setting hi='min' (minimum observed value) may be too strict and underestimate missing values; alternative quantiles (e.g., 10th percentile) can be used but must be justified.
- Gibbs sampler convergence depends on iteration counts (iters_each, iters_all); insufficient iterations may yield sub-optimal imputation. The authors note that smaller counts (e.g., iters_all=10, iters_each=50) may not severely affect accuracy but large counts are recommended.
- Method assumes missing not at random (MNAR) mechanism driven by detection limits; it is not appropriate for MCAR/MAR data without a known censoring threshold.
- Computational cost scales with the number of missing values and samples; parallel computing (n_cores parameter) can mitigate but large datasets may require optimization.

## Evidence

- [other] Run the Gibbs sampler iterative sampling loop, alternating between imputing missing values from a truncated normal distribution (conditioned on the detection limit) and updating the posterior estimates of metabolite parameters.: "alternating between imputing missing values from a truncated normal distribution (conditioned on the detection limit) and updating the posterior estimates"
- [readme] For left-censored missing values where the upper bound is set to the minimum value of non-missing part (notably, quantile values can be applied if minimum is too strict).: "lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part (notably, quantile values can be applied if minimum is too"
- [other] GSimp implements a Gibbs sampler based approach for left-censored missing value imputation, with core functions provided in GSimp.R that enable application to metabolomics datasets.: "GSimp implements a Gibbs sampler based approach for left-censored missing value imputation, with core functions provided in GSimp.R"
- [readme] Although a large number of iterations (e.g., iters_all=20 and iters_each=100) is recommended for the convergence of MCMC, a smaller number of iterations (iters_all=10, iters_each=50) won't severely affect the imputation accuracy as we tested on the simulation data.: "a large number of iterations (e.g., iters_all=20 and iters_each=100) is recommended for the convergence of MCMC, a smaller number of iterations (iters_all=10, iters_each=50) won't severely affect the"
- [other] Initialize the Gibbs sampler with prior parameters for mean and variance of the metabolite distribution.: "Initialize the Gibbs sampler with prior parameters for mean and variance of the metabolite distribution."
