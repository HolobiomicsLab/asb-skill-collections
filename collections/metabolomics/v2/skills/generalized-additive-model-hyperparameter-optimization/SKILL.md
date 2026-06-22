---
name: generalized-additive-model-hyperparameter-optimization
description: Use when when fitting a nonlinear retention time (RT) mapping spline to anchor feature pairs (m/z and RT values) from two LC-MS datasets acquired under different conditions, you need to determine both the optimal B-spline basis dimension and identify which anchor points are outliers.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mgcv
  - R
  - metabCombiner
derived_from:
- doi: 10.1021/acs.analchem.0c03693
  title: metabCombiner
evidence_spans:
- a modified form of the `gam` function implemented in the *mgcv* R package
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics.
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics
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
---

# generalized-additive-model-hyperparameter-optimization

## Summary

Optimize the basis dimension (k) and outlier detection parameters of a GAM spline fitted to retention time anchor points in LC-MS metabolomics. This skill selects the best model complexity through cross-validation while iteratively downweighting high-error points, balancing fit quality against overfitting.

## When to use

When fitting a nonlinear retention time (RT) mapping spline to anchor feature pairs (m/z and RT values) from two LC-MS datasets acquired under different conditions, you need to determine both the optimal B-spline basis dimension and identify which anchor points are outliers. This is required after anchor selection and before feature pair alignment scoring in the metabCombiner workflow.

## When NOT to use

- Anchor feature pairs have not yet been selected or validated; run anchor selection first.
- Retention time data contain missing values or are already cleaned by an external alignment tool.
- Input data are already a combined feature table; hyperparameter optimization applies only to the intermediate RT mapping step.

## Inputs

- anchor feature pairs: data frame with m/z and retention time columns
- candidate basis dimension values: integer vector (e.g., seq(12, 20, by=2))
- iterFilter: number of outlier filtering iterations (integer)
- coef: error ratio threshold for outlier flagging (numeric)
- prop: proportion threshold for outlier flagging across model fits (numeric between 0 and 1)

## Outputs

- fitted GAM spline model object (mgcv::gam class)
- selected optimal basis dimension k (integer)
- outlier weight vector (numeric, 0 for outliers, 1 for inliers)
- cross-validation error metrics for each k value
- diagnostic statistics (e.g., residuals, fitted values)

## How to apply

Load anchor feature pairs (m/z and retention time values) from the anchor selection step. Fit a GAM spline using mgcv::gam with B-spline basis (bs='bs'), Gaussian family, and smoothness penalty m=c(3,2) across candidate k values (e.g., 12 to 20 in steps of 2). Apply iterative outlier filtering: in each of iterFilter=2 iterations, flag points as outliers if their absolute error to mean absolute model error ratio exceeds the coef threshold (e.g., 2) in more than prop=0.5 of model fits, then assign these outliers a weight of 0. Evaluate all k values using 10-fold cross-validation and select the k that minimizes prediction error or information criterion. Retain the final model object containing fitted spline coefficients, selected k, the outlier weight vector, and diagnostic statistics; set seed=100 for reproducibility.

## Related tools

- **mgcv** (Implements generalized additive model fitting with gam function, B-spline basis specification, and smoothness penalties; core engine for spline coefficient estimation and cross-validation.)
- **metabCombiner** (Orchestrates the full workflow including anchor selection, GAM hyperparameter optimization, and feature pair alignment scoring for combining disparate LC-MS datasets.) — github.com/hhabra/metabCombiner

## Examples

```
fit_gam(anchor_pairs, k = seq(12, 20, by = 2), iterFilter = 2, coef = 2, prop = 0.5, seed = 100)
```

## Evaluation signals

- Cross-validation error decreases and then stabilizes or increases as k increases, indicating optimal k is found within the candidate range and not at a boundary.
- Outlier weight vector contains only 0 and 1 values, with outlier count reasonable relative to input size (typically < 20% for well-behaved anchor sets).
- Fitted spline passes through or near the majority of inlier anchor points (residual mean absolute error < threshold relative to RT range).
- Reproducibility check: fitting with set.seed(100) produces identical model coefficients and k selection across repeated runs.
- Diagnostic plots (e.g., residuals vs. fitted, Q-Q plot) show no systematic patterns suggesting model misspecification.

## Limitations

- Performance depends critically on anchor selection quality; spurious anchors will inflate outlier counts or bias spline shape.
- The iterative filtering process with fixed coef and prop thresholds may not adapt to datasets with unusual error distributions; threshold tuning may be necessary.
- B-spline basis (bs='bs') is less flexible than thin-plate regression splines; may underfit complex RT drift patterns.
- Cross-validation with small anchor sets (n < 30) may suffer high variance; 10-fold CV may create folds too small to estimate model error reliably.

## Evidence

- [other] The fit_gam function performs iterative outlier filtering where points are flagged as outliers if their absolute error to mean absolute model error ratio exceeds the coef argument in over prop of the model fits, then assigns these outliers a weight of 0: "The fit_gam function performs iterative outlier filtering where points are flagged as outliers if their absolute error to mean absolute model error ratio exceeds the coef argument in over prop of the"
- [other] Fit a GAM spline using mgcv::gam with bs='bs' (B-spline basis), family='gaussian', and smoothness penalty m=c(3,2) across candidate k values from 12 to 20 in steps of 2: "Fit a GAM spline using mgcv::gam with bs='bs' (B-spline basis), family='gaussian', and smoothness penalty m=c(3,2) across candidate k values from 12 to 20 in steps of 2"
- [other] followed by 10-fold cross-validation to select the best k value from multiple integer choices: "followed by 10-fold cross-validation to select the best k value from multiple integer choices"
- [other] Apply iterative filtering with iterFilter=2 iterations and coefficient threshold coef=2 to identify and downweight outliers, using prop=0.5 to proportion outlier contributions: "Apply iterative filtering with iterFilter=2 iterations and coefficient threshold coef=2 to identify and downweight outliers, using prop=0.5 to proportion outlier contributions"
- [intro] a modified form of the `gam` function implemented in the *mgcv* R package: "a modified form of the `gam` function implemented in the *mgcv* R package"
