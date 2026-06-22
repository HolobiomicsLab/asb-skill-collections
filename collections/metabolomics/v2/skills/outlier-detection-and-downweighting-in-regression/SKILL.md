---
name: outlier-detection-and-downweighting-in-regression
description: Use when when fitting a nonlinear regression (GAM spline) through retention time anchor points derived from feature pair alignments in LC-MS metabolomics, and you suspect some anchor points are measurement errors or misaligned features that could bias the smooth curve.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# outlier-detection-and-downweighting-in-regression

## Summary

Iteratively identify and downweight anomalous observations in generalized additive model (GAM) fitting by flagging points whose absolute error exceeds a threshold multiple of the mean absolute model error, then assigning them zero weight to stabilize spline coefficient estimation. This technique is applied during nonlinear retention time mapping in LC-MS metabolomics to prevent outlier anchor points from distorting the fitted spline.

## When to use

When fitting a nonlinear regression (GAM spline) through retention time anchor points derived from feature pair alignments in LC-MS metabolomics, and you suspect some anchor points are measurement errors or misaligned features that could bias the smooth curve. Use this skill if you need to select optimal basis dimension (k) and produce a robust model that generalizes across cross-validation folds.

## When NOT to use

- The anchor feature pairs are already known to be high-confidence validated matches (e.g., isotope standards or synthetic spike-ins with negligible error).
- Sample size is very small (n < 20 total anchor points), since iterative filtering may eliminate too many observations and leave insufficient data for spline fitting.
- You require transparent, audit-trail retention of all observations for regulatory compliance; downweighting removes transparency compared to explicit inclusion/exclusion flags.

## Inputs

- anchor feature pairs with m/z and retention time values
- candidate k (basis dimension) values
- coef threshold (numeric, typically 2)
- prop (proportion of fits used to flag outliers, typically 0.5)
- iterFilter (number of filtering iterations, typically 2)

## Outputs

- fitted GAM spline model object with selected k
- outlier weight vector (0 for downweighted points, 1 for retained)
- cross-validation diagnostics and model selection criterion
- final spline coefficients and smoothness parameters

## How to apply

Load anchor feature pairs (m/z and retention time values) and fit a B-spline GAM using mgcv::gam with bs='bs' basis, family='gaussian', and smoothness penalty m=c(3,2). Apply iterative outlier filtering: in each iteration, compute absolute errors to the current fit, flag points where the error-to-mean-absolute-error ratio exceeds the coef threshold (e.g., coef=2) in at least prop×100% (e.g., prop=0.5) of candidate k model fits, then assign these outliers weight=0. Repeat for iterFilter iterations (e.g., 2). After filtering, use 10-fold cross-validation to select optimal k from candidate values (e.g., 12 to 20 in steps of 2). Retain the final model object containing fitted spline coefficients, selected k, outlier weight vector, and diagnostics; set seed=100 for reproducibility.

## Related tools

- **mgcv** (Implements gam function with B-spline basis (bs='bs'), Gaussian family, and smoothness penalties (m=c(3,2)) for iterative spline fitting and k selection via cross-validation) — https://cran.r-project.org/package=mgcv
- **metabCombiner** (Parent workflow step that generates anchor feature pairs and calls fit_gam for RT mapping spline in LC-MS metabolomics dataset alignment) — https://github.com/hhabra/metabCombiner

## Examples

```
fit_gam(anchorData, k=seq(12, 20, 2), iterFilter=2, coef=2, prop=0.5, seed=100)
```

## Evaluation signals

- Outlier weight vector is binary (0 or 1) with length equal to number of anchor points; verify no NA values introduced.
- Selected k value lies within the candidate range (e.g., 12–20) and cross-validation error is minimized at that k; inspect the cross-validation curve for a clear optimum.
- Fitted spline passes through or near non-downweighted anchor points; residual sum of squares for retained observations should be lower than a model without filtering.
- Outlier count is plausible (typically <10% of total anchor points flagged); if >50% are downweighted, inspect data quality or adjust coef/prop thresholds.
- Reproducibility: when seed=100 is set, the same model, k, and weight vector are recovered on re-run with identical input data.

## Limitations

- The coef and prop thresholds are sensitive hyperparameters; no principled method for choosing them is given beyond rule-of-thumb (coef=2, prop=0.5). Practitioners must validate choices on reference data.
- Iterative filtering is greedy and does not guarantee globally optimal outlier set; early removals can influence subsequent iterations.
- k selection via cross-validation assumes anchor points are representative of true RT–m/z relationship; if anchor selection itself is biased, filtering cannot recover unbiased spline.
- Very small effective sample size (n < 5–10 retained anchor points after filtering) may yield overly flexible or numerically unstable splines; no minimum-sample stopping rule is documented.

## Evidence

- [other] iterative outlier filtering where points are flagged as outliers if their absolute error to mean absolute model error ratio exceeds the coef argument in over prop of the model fits, then assigns these outliers a weight of 0: "The fit_gam function performs iterative outlier filtering where points are flagged as outliers if their absolute error to mean absolute model error ratio exceeds the coef argument in over prop of the"
- [other] 10-fold cross-validation to select the best k value from multiple integer choices: "followed by 10-fold cross-validation to select the best k value from multiple integer choices."
- [other] GAM spline using mgcv::gam with bs='bs' (B-spline basis), family='gaussian', and smoothness penalty m=c(3,2) across candidate k values from 12 to 20: "Fit a GAM spline using mgcv::gam with bs='bs' (B-spline basis), family='gaussian', and smoothness penalty m=c(3,2) across candidate k values from 12 to 20"
- [other] iterative filtering with iterFilter=2 iterations and coefficient threshold coef=2 to identify and downweight outliers, using prop=0.5: "Apply iterative filtering with iterFilter=2 iterations and coefficient threshold coef=2 to identify and downweight outliers, using prop=0.5 to proportion outlier contributions."
- [intro] metabCombiner determines possible feature pair alignments and validates them through pairwise similarity scoring: "`metabCombiner` determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score."
