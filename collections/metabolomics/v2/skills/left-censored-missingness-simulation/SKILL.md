---
name: left-censored-missingness-simulation
description: Use when when you have a complete metabolomics abundance table (e.g., targeted LC/MS or untargeted GC/MS counts) and need to generate synthetic left-censored missingness for evaluating imputation algorithm performance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GSimp_evaluation.R
  - impute.QRILC
  - R base and tidyverse (magrittr, dplyr)
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

# left-censored-missingness-simulation

## Summary

Simulate missing-not-at-random (MNAR) left-censored data in metabolomics matrices by applying detection limits and feature-dependent missing mechanisms, enabling benchmarking of imputation methods against realistic instrument censoring patterns.

## When to use

When you have a complete metabolomics abundance table (e.g., targeted LC/MS or untargeted GC/MS counts) and need to generate synthetic left-censored missingness for evaluating imputation algorithm performance. This is appropriate when your goal is to benchmark multiple imputation methods (GSimp, QRILC, kNN-TN, HM) against known ground truth, or when real datasets have insufficient or unevenly distributed missing values for robust method comparison.

## When NOT to use

- Input data already contains real missing values — mask and document those separately first to avoid confounding synthetic and real missingness.
- Missingness is right-censored (e.g., values above an upper saturation limit) — use hi=quantile() upper bounds instead of lo=-Inf, hi='min'.
- Analysis goal is exploratory or descriptive (not method comparison) — the synthetic ground truth may not reflect actual data patterns in your study.

## Inputs

- Complete metabolomics data matrix (numeric data frame, no pre-existing NAs)
- Detection limit threshold (percentile quantile, absolute value, or per-variable vector)
- Missing-data mechanism specification (uniform MCAR, feature-dependent, or sample-dependent rates)
- Feature/sample indices for selective missingness (optional)

## Outputs

- Left-censored data matrix (same dimensions, with NAs below threshold)
- NA position matrix (row/column indices of introduced missingness)
- Missingness metadata (threshold used, mechanism applied, count of missing elements, features/samples affected)

## How to apply

Load a complete metabolomics data matrix into R and define a left-censoring threshold as either a percentile quantile of each variable's non-missing distribution or an absolute detection limit value. Randomly select features and samples according to a specified missing-data mechanism (e.g., uniformly random selection, or feature-dependent rates that increase for lower-abundance metabolites). Replace all values below the threshold with NA to simulate left-censored observations below the limit of quantification (LOQ). The workflow typically follows: (1) log-transformation for normality, (2) threshold application and NA masking, (3) optional initial imputation with QRILC, (4) centralization/scaling, (5) downstream imputation method application. Record the original positions of masked values (NA_pos) to enable later evaluation by comparing imputed values against ground truth.

## Related tools

- **GSimp_evaluation.R** (Contains MNAR generation and evaluation functions that execute left-censoring threshold application and missing-data mechanism assignment) — https://github.com/WandeRum/GSimp
- **impute.QRILC** (Quantile Regression Imputation of Left-Censored data; used for initial imputation before Gibbs sampling in the pre_processing_GS_wrapper pipeline) — https://cran.r-project.org/package=imputeLCMD
- **R base and tidyverse (magrittr, dplyr)** (Data manipulation, matrix operations, and NA masking during threshold application)

## Examples

```
source('GSimp_evaluation.R'); NA_pos <- which(is.na(untargeted_data), arr.ind=T); data_censored <- untargeted_data; data_censored[NA_pos] <- NA
```

## Evaluation signals

- Count of NA elements introduced matches expected number given threshold and mechanism (e.g., if threshold=10th percentile, ~10% of values should be NA).
- NA positions correctly fall below the applied threshold: all original values at NA_pos should be ≤ threshold value for that variable.
- Remaining non-missing values are unchanged (bit-for-bit identical) compared to input matrix.
- Missingness map (visualized with missmap()) shows expected pattern: uniform random for MCAR, clustered by feature for feature-dependent mechanism.
- Ground-truth matrix (original values before censoring) is retained separately to enable imputation accuracy metrics (RMSE, MAE) during evaluation.

## Limitations

- Simulated MNAR mechanism may not capture real-world instrument behavior (e.g., ion suppression, chromatographic interference); this is acknowledged as a simplification for controlled benchmarking.
- If threshold is too aggressive (e.g., 50th percentile), missingness becomes MCAR-like rather than left-censored; threshold choice should reflect actual LOQ/LOD in your instrument.
- log-transformation is required before threshold application to avoid distortion of the censoring boundary; exponential recovery must be applied after imputation to restore original scale.
- The simulated MNAR data assume conditional independence given the observed values; real metabolomics data may exhibit more complex missing-data dependencies (e.g., covariate-dependent censoring).

## Evidence

- [readme] GSimp_evaluation.R contains MNAR generation and evaluation functions which are part of our missing value imputation evaluation pipeline.: "**GSimp_evaluation.R** contains MNAR generation and evaluation functions which are part of our missing value imputation evaluation pipeline."
- [other] Define left-censoring threshold parameters (detection limit as a percentile or absolute value). Randomly select features and samples according to a specified missing-data mechanism.: "Define left-censoring threshold parameters (detection limit as a percentile or absolute value). Randomly select features and samples according to a specified missing-data mechanism (e.g.,"
- [other] Replace values below the detection threshold with NA to simulate left-censored observations.: "Replace values below the detection threshold with NA to simulate left-censored observations."
- [readme] log-transformation is needed for non-normal data; initialization with QRILC; centralization and scaling for elastic-net prediction; imputation using GSimp; scaling recovery; exponential recovery.: "Log-transformation (for non-normal data), Initialization for missing values (e.g., QRILC), Centralization and scaling (for elastic-net prediction), Imputation using GSimp, Scaling recovery,"
- [readme] lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part: "Here, lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part"
