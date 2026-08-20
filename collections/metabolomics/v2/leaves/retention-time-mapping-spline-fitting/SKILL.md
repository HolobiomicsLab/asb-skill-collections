---
name: retention-time-mapping-spline-fitting
description: Use when after anchor feature pairs (m/z and retention time values) have
  been selected from two disparately-acquired LC-MS datasets, and you need to correct
  for systematic retention time differences between the datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mgcv
  - R
  - metabCombiner
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.0c03693
  title: metabCombiner
evidence_spans:
- a modified form of the `gam` function implemented in the *mgcv* R package
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS
  metabolomics.
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS
  metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabcombiner_cq
    doi: 10.1021/acs.analchem.0c03693
    title: metabCombiner
  dedup_kept_from: coll_metabcombiner_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03693
  all_source_dois:
  - 10.1021/acs.analchem.0c03693
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-mapping-spline-fitting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Fit a nonlinear generalized additive model (GAM) spline through retention time anchor points to map and correct systematic RT drift between two LC-MS datasets. This skill selects optimal basis dimension and filters outliers iteratively to produce a smooth, robust RT transformation function.

## When to use

After anchor feature pairs (m/z and retention time values) have been selected from two disparately-acquired LC-MS datasets, and you need to correct for systematic retention time differences between the datasets. This skill is triggered when the RT distributions of anchor features show nonlinear drift that cannot be corrected by a linear transformation alone.

## When NOT to use

- Anchor feature pairs are already perfectly aligned with linear RT relationship (use linear regression instead).
- Number of anchor points is too small (<10–15) to robustly fit a spline with k ≥ 12.
- Retention time data contain severe batch effects or multimodal distributions that violate Gaussian model assumptions.

## Inputs

- anchor feature pairs (m/z, retention time tuples from dataset 1)
- anchor feature pairs (m/z, retention time tuples from dataset 2)
- candidate basis dimension values (integers 12–20)

## Outputs

- fitted GAM spline model object
- selected optimal basis dimension (k)
- outlier weight vector
- cross-validation diagnostic statistics
- RT transformation function (continuous mapping from dataset 1 RT to dataset 2 RT)

## How to apply

Load anchor feature pairs consisting of m/z and retention time values from both datasets. Fit a generalized additive model using mgcv::gam with B-spline basis (bs='bs'), Gaussian family, and smoothness penalty m=c(3,2) across candidate basis dimensions (k) ranging from 12 to 20 in steps of 2. Apply iterative outlier filtering in 2 iterations where points are flagged if their absolute error-to-mean-absolute-error ratio exceeds a coefficient threshold (coef=2) in at least 50% of model fits; assign flagged outliers a weight of 0. Perform 10-fold cross-validation to select the optimal k value that minimizes prediction error. Retain the final GAM model object containing fitted spline coefficients, selected k, outlier weight vector, and diagnostic statistics. Set the random seed to 100 for reproducibility.

## Related tools

- **mgcv** (Provides gam function implementing B-spline basis fitting, smoothness penalties, and cross-validation model selection for nonlinear RT mapping) — https://cran.r-project.org/package=mgcv
- **metabCombiner** (Parent workflow package that orchestrates anchor selection and calls fit_gam for RT mapping in the third major workflow step) — https://github.com/hhabra/metabCombiner

## Examples

```
fit_gam(anchor_features_dataset1, anchor_features_dataset2, k_candidates = seq(12, 20, 2), coef = 2, prop = 0.5, iterFilter = 2, seed = 100)
```

## Evaluation signals

- Cross-validation error decreases monotonically or plateaus across candidate k values, with no k value showing anomalously high error.
- Outlier weight vector contains only 0 and 1 values; proportion of zero-weighted points matches the coef and prop thresholds (approximately 50% of outliers detected in ≥2 iterations).
- Final GAM model produces smooth, visually continuous RT transformation curve with no discontinuities or extreme local curvature.
- Residuals from fitted spline are approximately normally distributed with mean close to zero and no systematic patterns across RT range.
- Seed=100 reproducibly produces identical fitted coefficients and outlier weights across multiple runs.

## Limitations

- GAM assumes Gaussian errors; severe non-Gaussian noise or heavy tails in anchor RT differences may produce suboptimal fits.
- Iterative outlier filtering with coef=2 may be too aggressive for anchor sets with genuine biological or instrumental variation in RT.
- Basis dimension (k) selection is restricted to 12–20; datasets with very sparse or very dense anchor points may benefit from extended k ranges not explored.
- The method does not handle anchors with missing or ambiguous RT values; pre-filtering is assumed.

## Evidence

- [other] fit_gam performs iterative outlier filtering where points are flagged as outliers if their absolute error to mean absolute model error ratio exceeds the coef argument in over prop of the model fits, then assigns these outliers a weight of 0: "The fit_gam function performs iterative outlier filtering where points are flagged as outliers if their absolute error to mean absolute model error ratio exceeds the coef argument in over prop of the"
- [other] 10-fold cross-validation to select the best k value from multiple integer choices: "followed by 10-fold cross-validation to select the best k value from multiple integer choices"
- [other] Fit a GAM spline using mgcv::gam with bs='bs' (B-spline basis), family='gaussian', and smoothness penalty m=c(3,2) across candidate k values from 12 to 20 in steps of 2: "Fit a GAM spline using mgcv::gam with bs='bs' (B-spline basis), family='gaussian', and smoothness penalty m=c(3,2) across candidate k values from 12 to 20 in steps of 2"
- [other] Apply iterative filtering with iterFilter=2 iterations and coefficient threshold coef=2 to identify and downweight outliers, using prop=0.5: "Apply iterative filtering with iterFilter=2 iterations and coefficient threshold coef=2 to identify and downweight outliers, using prop=0.5"
- [intro] Anchor Selection and RT Mapping Spline is the third major step in the metabCombiner workflow: "3) Anchor Selection and RT Mapping Spline"
