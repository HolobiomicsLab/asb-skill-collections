---
name: metabolomics-matrix-manipulation
description: Use when you have a raw metabolomics abundance table (e.g., LC/MS or GC/MS peak intensities or concentrations) with non-normal distributions and missing values, and you need to prepare it for Gibbs sampler or other model-based imputation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - imputeLCMD (R package)
  - GSimp.R
  - R base (log, exp, scale functions)
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

# metabolomics-matrix-manipulation

## Summary

Transform and standardize metabolomics abundance matrices through log-transformation, scaling, centralization, and recovery operations to prepare data for imputation and downstream analysis. This skill chains pre- and post-processing steps that preserve data integrity and enable missing-value algorithms to work on normalized scales.

## When to use

You have a raw metabolomics abundance table (e.g., LC/MS or GC/MS peak intensities or concentrations) with non-normal distributions and missing values, and you need to prepare it for Gibbs sampler or other model-based imputation. Use this skill before applying GSimp or similar left-censored missing-value methods, especially when your data exhibit right-skewed or log-normal distributions typical of metabolomics.

## When NOT to use

- Data are already known to be normally distributed or have been pre-transformed by the data provider.
- You require untransformed abundance values for compliance with downstream tools that expect raw instrument output (e.g., certain LC/MS quantification workflows).
- Missing values are known to be MCAR/MAR rather than left-censored (MNAR); use non-informative bounds (lo=-Inf, hi=Inf) in GS_impute instead of applying log and scale recovery.

## Inputs

- raw metabolomics abundance matrix (data frame or matrix; rows=samples, columns=metabolites; numeric values with NAs marking missing)
- log-transformed abundance matrix (optional intermediate; output from log() applied to raw matrix)
- initialized matrix with QRILC or symmetry-based imputation (intermediate)
- scaling parameters (centering and scaling attributes; output from scale_recover(..., method='scale'); used only for recovery)

## Outputs

- log-transformed and scaled data matrix (prepared for imputation; rows=samples, columns=metabolites)
- imputed abundance matrix on original scale (final output; same dimensions as input, no NAs)
- scaling parameters data frame (metadata for post-imputation recovery; contains means and standard deviations per metabolite)

## How to apply

Apply a five-step transformation chain: (1) Log-transform the raw abundance matrix to normalize skewed metabolomics distributions; (2) Initialize missing values using QRILC or symmetric quantile methods to stabilize the matrix; (3) Standardize (center and scale) the initialized data using scale_recover(..., method='scale'), capturing centering parameters for later recovery; (4) Replace initialized values at original missing positions with NA to mark them for imputation; (5) After imputation, recover the original scale by reversing standardization with scale_recover(..., method='recover', param_df=...), then exponentiate to restore abundance units. The wrapper function pre_processing_GS_wrapper automates all steps and accepts raw (non-log) data as input, returning final imputed abundances on the original scale.

## Related tools

- **imputeLCMD (R package)** (Provides impute.QRILC() function for initialization of left-censored missing values before log-scaling)
- **GSimp.R** (Core imputation engine; receives scaled matrix with marked missing positions and returns imputed values; called via GS_impute()) — https://github.com/WandeRum/GSimp
- **R base (log, exp, scale functions)** (Implements log-transformation, exponentiation, and standardization operations; scale() and manual centering/scaling in scale_recover())

## Examples

```
source('GSimp.R'); source('GSimp_evaluation.R'); source('Trunc_KNN/Imput_funcs.r'); data_imp <- pre_processing_GS_wrapper(untargeted_data)
```

## Evaluation signals

- Log-transformed matrix values are numeric and right-skewed distribution flattens to near-normal (inspect via histogram or Q-Q plot before and after log).
- Scaling parameters (means and standard deviations per metabolite) are finite, positive, and stored correctly for later recovery (spot-check: recover parameters must match original data statistics).
- Post-imputation values after scale recovery and exponentiation fall within biologically plausible ranges (e.g., positive abundances; compare to original non-missing distribution).
- NA positions in raw data are correctly preserved and marked in the scaled matrix; imputed values appear only at originally-NA positions after recovery.
- Recovered final matrix has identical dimensions and sample/metabolite names as the input raw matrix.

## Limitations

- Log-transformation is undefined for zero or negative abundance values; pre-filter metabolites with all-zero or negative values, or add small pseudocounts (not described in paper).
- QRILC initialization may be unstable if a metabolite has very few non-missing values (≤2–3 observations); consider alternative initializers (lsym, rsym) or exclude such features.
- Scaling recovery assumes that centering and scaling parameters are preserved and applied in the correct order (scale_recover must be called with method='recover' and param_df argument); parameter loss results in incorrect final abundance units.
- The skill assumes left-censored missingness (MNAR); for MCAR/MAR data, informative bounds (lo, hi) in GS_impute should be relaxed to -Inf/Inf, and scale recovery may not be appropriate if bounds are non-informative.

## Evidence

- [readme] All aboved steps has been wrapped into the pre_processing_GS_wrapper function for a one-step processing and imputation.: "All aboved steps has been wrapped into the *pre_processing_GS_wrapper* function for a one-step processing and imputation. The function will give the final imputed dataset."
- [readme] Log transformation, initialization, centralization and scaling, imputation, scaling recovery, exponential recovery, output.: "Log-transformation (for non-normal data) / Initialization for missing values (e.g., QRILC) / Centralization and scaling (for elastic-net prediction) / Imputation using GSimp / Scaling recovery /"
- [intro] data pre-processing, simulated data generation, missing not at random (MNAR) generation, wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and evaluations: "data pre-processing, simulated data generation, missing not at random (MNAR) generation, wrapper functions for different MNAR imputation methods (GSimp, QRILC, and kNN-TN) and evaluations of these"
- [readme] NA position marked; log-scaled-initialized data with NAs reinserted; GSimp imputation applied; imputed data recovered via scale_recover and exp().: "NA position / NA introduced to log-scaled-initialized data / Feed initialized and missing data into GSimp imputation / Data recovery / data_imp_log_sc %>% scale_recover(., method = 'recover',"
- [readme] lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part.: "lo=-Inf, hi='min' are default setting for left-censored missing values where the upper bound is set to the minimum value of non-missing part"
