---
name: smoothing-spline-basis-selection
description: Use when you have a set of anchor feature pairs (m/z and retention time
  values) from two disparately-acquired LC-MS datasets and need to fit a smooth, nonlinear
  RT correction spline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0634
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

# smoothing-spline-basis-selection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Select the optimal basis dimension (k) for a generalized additive model (GAM) B-spline by iteratively filtering outliers and applying cross-validation across candidate k values. This skill is essential when fitting nonlinear retention time (RT) mappings through anchor feature pairs in LC-MS metabolomics alignment, where robust outlier handling and principled model complexity selection determine mapping accuracy.

## When to use

Apply this skill when you have a set of anchor feature pairs (m/z and retention time values) from two disparately-acquired LC-MS datasets and need to fit a smooth, nonlinear RT correction spline. Specifically, use this when anchor points are contaminated by misaligned or spurious pairs that would distort the mapping, and you must choose between multiple plausible spline complexities (k values from 12 to 20) without overfitting.

## When NOT to use

- Anchor point set is already known to be clean and uncontaminated; simple linear or low-order polynomial regression may be more efficient.
- Retention time mapping is expected to be piecewise linear or has known breakpoints; a segmented or change-point model is more appropriate.
- Sample size is very small (<10 anchor pairs); overfitting risk is high and k selection becomes unreliable.

## Inputs

- anchor feature pairs (data frame with m/z and retention time columns)
- candidate k values (integer sequence, e.g., 12, 14, 16, 18, 20)

## Outputs

- fitted GAM spline model object with selected k
- outlier weight vector (0 for flagged outliers, 1 otherwise)
- cross-validation or information criterion scores across k values
- diagnostic statistics (model residuals, basis coefficients)

## How to apply

Load anchor feature pairs as input data. Initialize a candidate k range (e.g., 12 to 20 in steps of 2) and fit a B-spline GAM with mgcv::gam using bs='bs', family='gaussian', and smoothness penalty m=c(3,2). Apply iterative outlier filtering: flag points as outliers if their absolute error-to-mean-absolute-model-error ratio exceeds the coefficient threshold (coef=2) in a proportion (prop=0.5) of the model fits, then assign these outliers weight 0. Perform 10-fold cross-validation or use an information criterion (e.g., AIC, GCV) to compare fitted models across all k values and select the k that minimizes prediction error or generalization loss. Set seed=100 for reproducibility. The final output is a fitted GAM object containing spline coefficients, the selected k, outlier weight vector, and diagnostic statistics.

## Related tools

- **mgcv** (GAM fitting and B-spline basis construction with gam() function and cross-validation) — https://cran.r-project.org/package=mgcv
- **R** (Host language and scripting environment for spline fitting workflow)
- **metabCombiner** (Orchestrates anchor selection and fit_gam spline-fitting step within the RT mapping workflow) — https://github.com/hhabra/metabCombiner

## Examples

```
fit_gam(anchor_pairs, k_candidates = seq(12, 20, 2), iterFilter = 2, coef = 2, prop = 0.5, seed = 100)
```

## Evaluation signals

- Selected k value falls within the candidate range and is supported by cross-validation error metrics or information criterion scores.
- Outlier weight vector contains only 0s and 1s, and the proportion of downweighted points is consistent with prop=0.5 and the iterFilter iterations.
- Fitted spline passes through (or near) non-outlier anchor points with absolute residuals below a domain-specific RT tolerance (e.g., ±0.05 min).
- Cross-validation scores improve monotonically up to the selected k, then plateau or increase, confirming that k was not chosen in an underfitting regime.
- Diagnostic plots (fitted vs. residual, Q-Q plot) show no systematic pattern or heteroscedasticity in model residuals.

## Limitations

- Outlier detection relies on iterative filtering with fixed coefficients (coef=2, prop=0.5); these thresholds may not generalize across datasets with differing anchor point quality or noise profiles.
- B-spline basis with fixed penalty m=c(3,2) assumes a specific trade-off between smoothness and model fit; alternative penalty structures may be needed for highly nonlinear RT drifts.
- Cross-validation fold structure (10-fold) may be unstable if the anchor set is very small (<30 points); alternative selection criteria (e.g., AIC, GCV) should be considered.
- No changelog provided; reproducibility across software versions (especially mgcv updates) is not guaranteed without pinning package versions.

## Evidence

- [other] task_004 finding and workflow: "The fit_gam function performs iterative outlier filtering where points are flagged as outliers if their absolute error to mean absolute model error ratio exceeds the coef argument in over prop of the"
- [other] task_004 workflow detail: "Fit a GAM spline using mgcv::gam with bs='bs' (B-spline basis), family='gaussian', and smoothness penalty m=c(3,2) across candidate k values from 12 to 20 in steps of 2."
- [intro] metabCombiner workflow context: "Anchor Selection and RT Mapping Spline is a major step in the five-part metabCombiner workflow for combining LC-MS datasets."
- [readme] README — metabCombiner purpose: "metabCombiner takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)> features"
