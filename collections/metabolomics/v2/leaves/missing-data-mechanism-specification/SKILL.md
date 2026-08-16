---
name: missing-data-mechanism-specification
description: Use when when you have a metabolomics abundance table with missing values
  and need to decide which imputation method to apply, or when designing a simulation
  to evaluate imputation performance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - R
  - GSimp_evaluation.R
  - GSimp.R
  - imputeLCMD (R package)
  - Trunc_KNN
  techniques:
  - LC-MS
  - GC-MS
  license_tier: noncommercial
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-SA-4.0
    url: WandeRum/GSimp
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

# Missing-Data Mechanism Specification

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Specify the missing-data mechanism (MCAR, MAR, or MNAR) and censoring parameters for metabolomics datasets to enable appropriate selection and benchmarking of imputation methods. This skill determines whether missingness is random, dependent on observed covariates, or dependent on unobserved (left-censored) values, which constrains which imputation strategies are valid.

## When to use

When you have a metabolomics abundance table with missing values and need to decide which imputation method to apply, or when designing a simulation to evaluate imputation performance. Specifically, use this skill when you have identified a detection limit (LOQ/LOD) or when you need to characterize whether missingness follows a left-censoring pattern (feature-dependent or sample-dependent) versus completely random missingness.

## When NOT to use

- Data has already been imputed or filtered for missing values; re-specification risks double-imputation or bias.
- Missingness is known to be completely random (MCAR) and you are simply applying a standard MCAR imputation method — specification is unnecessary but does not harm.
- You lack any information about the detection limit or censoring process (e.g., legacy data with no metadata); in this case, exploratory analysis of the empirical missing-value distribution should precede mechanism specification.

## Inputs

- Complete or partially-complete metabolomics abundance matrix (numeric data frame or matrix)
- Detection-limit specification (absolute LOQ/LOD value, percentile threshold, or per-feature vector)
- Missingness pattern metadata (which features/samples are affected, magnitude of missingness)
- Prior knowledge of instrument/protocol (e.g., LC/MS vs. GC/MS, targeted vs. untargeted)

## Outputs

- Specification document or code defining: missing-data mechanism (MCAR/MAR/MNAR), censoring threshold(s), affected features/samples, and rationale
- MNAR-censored data matrix with synthetic missing values placed according to mechanism (for simulation/evaluation)
- Metadata object recording threshold used, number of features/samples affected, and pattern of missingness

## How to apply

First, examine the missing-value distribution across features and samples to infer the mechanism: left-censored missingness (MNAR) typically clusters at low abundance values and correlates with feature detection thresholds, whereas MCAR appears uniformly distributed. Define the censoring threshold as a percentile (e.g., 10th percentile of non-missing values per feature) or an absolute quantification limit (LOQ/LOD) reported by the instrument. Specify feature-dependent missing rates (e.g., some metabolites have inherently higher missingness) or sample-dependent rates (e.g., low-concentration samples have more missing values). For MNAR generation in simulation, randomly select features and samples according to your specified mechanism, then replace values below the threshold with NA. Document the threshold value(s), affected features/samples, and the assumed mechanism to ensure the downstream imputation method matches the data-generation process. For left-censored data (the default in metabolomics), set imputation bounds to lo=-Inf and hi='min' (or a quantile thereof) to constrain imputations to the lower tail.

## Related tools

- **GSimp_evaluation.R** (Contains MNAR generation functions to simulate missing-not-at-random data according to specified mechanism and thresholds) — https://github.com/WandeRum/GSimp
- **GSimp.R** (Core imputation function (GS_impute) with parameters (lo, hi) that encode the missing-data mechanism bounds) — https://github.com/WandeRum/GSimp
- **imputeLCMD (R package)** (Provides QRILC and related functions for left-censored imputation; requires prior specification of censoring mechanism)
- **Trunc_KNN** (kNN-TN algorithm for truncated imputation; requires specification of truncation bounds consistent with detected mechanism) — https://github.com/WandeRum/GSimp

## Examples

```
# Specify left-censored MNAR mechanism with 10th percentile threshold per feature
NA_pos <- which(is.na(untargeted_data), arr.ind=TRUE)
threshold_per_feature <- sapply(untargeted_data, function(x) quantile(x, 0.1, na.rm=TRUE))
# Then apply GS_impute with mechanism-aligned bounds:
result <- GS_impute(data_raw_log_sc, lo=-Inf, hi=threshold_per_feature, iters_each=50, iters_all=10)
```

## Evaluation signals

- Specification document includes explicit statement of mechanism (MCAR/MAR/MNAR) with supporting evidence from data distribution (e.g., 'missingness clusters at low abundance, consistent with left-censoring MNAR').
- Threshold value(s) (absolute or percentile) are documented and match the reported instrument LOQ/LOD or exploratory analysis of the empirical data.
- If MNAR was specified, simulated censored data reproduces the observed missing-value distribution (comparison of original and synthetic missingness patterns using heatmaps or tallies).
- Imputation method selected (GSimp, QRILC, kNN-TN, or HM) has bounds (lo, hi) that align with the specified mechanism (e.g., lo=-Inf, hi='min' for left-censored MNAR).
- Number and location of synthetic missing values introduced during simulation match the specified feature/sample-dependent rates.

## Limitations

- Specification of mechanism relies on subject-matter knowledge and exploratory visualization; in the absence of instrument metadata, inference can be ambiguous, especially distinguishing MAR from MNAR.
- Left-censoring threshold (LOQ/LOD) is often not precisely reported in legacy datasets, forcing practitioners to estimate it post-hoc (e.g., from percentiles), which introduces uncertainty into the specification.
- GSimp and related methods are optimized for left-censored MNAR in metabolomics; specification for right-censored data or other domains may require parameter adjustment or different methods (e.g., symmetrical strategies 'lsym', 'rsym' in GSimp are less validated).
- When non-informative bounds (±∞) are applied to extend GSimp to MCAR/MAR, the specification remains theoretically sound but performance gains over simpler methods are not empirically confirmed in the paper.

## Evidence

- [readme] MNAR definition and left-censoring context: "GSimp is a gibbs sampler based left-censored missing value imputation approach for metabolomics studies. This vignette provides a quick tour of GSimp that contains, data pre-processing, simulated"
- [other] Workflow for MNAR generation and specification: "Define left-censoring threshold parameters (detection limit as a percentile or absolute value). Randomly select features and samples according to a specified missing-data mechanism (e.g.,"
- [readme] Bounds encoding the mechanism in imputation: "lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part"
- [readme] Real-world example of mechanism specification: "The untargeted GC/MS dataset contains 37 samples and 112 variables with 317 missing elements and 221 of them were retrieved manually. From the following kernel density plot, we found overlaps between"
- [readme] Extension of bounds for MCAR/MAR specification: "When non-informative bounds for both upper and lower limits (e.g., +∞, -∞) were applied, GSimp could be extended to the situation of MCAR/MAR."
