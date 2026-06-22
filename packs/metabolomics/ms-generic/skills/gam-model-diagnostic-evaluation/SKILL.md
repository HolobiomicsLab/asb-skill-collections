---
name: gam-model-diagnostic-evaluation
description: Use when after fitting candidate GAM splines with B-spline basis functions across a range of basis dimensions (k values 12–20) to anchor feature pairs (m/z and retention time coordinates).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mgcv
  - R
  - metabCombiner
  techniques:
  - mass-spectrometry
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03693
  all_source_dois:
  - 10.1021/acs.analchem.0c03693
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gam-model-diagnostic-evaluation

## Summary

Evaluate and select the optimal generalized additive model (GAM) spline fit for retention time mapping by applying iterative outlier filtering and cross-validation across multiple basis dimensions. This skill ensures that the fitted spline captures true anchor point relationships while down-weighting anomalous measurements that would distort RT alignment.

## When to use

After fitting candidate GAM splines with B-spline basis functions across a range of basis dimensions (k values 12–20) to anchor feature pairs (m/z and retention time coordinates). Use this skill when you need to simultaneously identify outlier anchor points and select the optimal model complexity that balances bias–variance trade-off without overfitting to measurement noise.

## When NOT to use

- Anchor points are already known to be free of measurement outliers or systematic bias — filtering may discard valid variation.
- Retention time mapping is linear or nearly linear; GAM splines are unnecessary and add model complexity without benefit.
- Sample size of anchor points is very small (n < 20); cross-validation folds become unreliable and outlier filtering unstable.

## Inputs

- Anchor feature pair table with m/z and retention time values
- Candidate basis dimension values (k from 12 to 20 in steps of 2)
- Iterative filter parameters: iterFilter count, coef threshold, prop proportion

## Outputs

- Fitted GAM model object with optimal basis dimension k
- Outlier weight vector (0 for outliers, 1 for retained points)
- Cross-validation or information criterion scores across k values
- Diagnostic statistics (residuals, fitted spline coefficients)

## How to apply

Apply iterative outlier filtering where points are flagged as outliers if their absolute error to mean absolute model error ratio exceeds the coef threshold (e.g., coef=2) in over prop of model fits (e.g., prop=0.5), then assign these outliers a weight of 0 to down-weight their influence. Perform 10-fold cross-validation to select the best k value from candidate integers; evaluate model fit using information criterion or cross-validation error. Retain the final model object containing fitted spline coefficients, selected k, outlier weight vector, and diagnostic statistics. Set seed to 100 for reproducibility to ensure consistent outlier identification and k selection across runs.

## Related tools

- **mgcv** (Provides gam() function with B-spline basis (bs='bs'), Gaussian family, and smoothness penalty (m=c(3,2)) for fitting and evaluating candidate splines across basis dimensions) — https://cran.r-project.org/package=mgcv
- **R** (Statistical computing environment for implementing iterative filtering logic, cross-validation loops, and model selection workflows)
- **metabCombiner** (Orchestrates the full RT mapping workflow including this diagnostic evaluation step as part of the 'Anchor Selection and RT Mapping Spline' stage) — https://github.com/hhabra/metabCombiner

## Examples

```
# Fit GAM with candidate k values 12–20 and select optimal k via iterative filtering and cross-validation
fit_result <- fit_gam(anchor_pairs, k_values = seq(12, 20, by = 2), iterFilter = 2, coef = 2, prop = 0.5, seed = 100)
```

## Evaluation signals

- Outlier weight vector contains only 0 or 1 values; count and proportion of outliers align with iterFilter iterations and coef threshold logic.
- Selected k value minimizes cross-validation error or information criterion across candidate range; no sudden jumps or plateau effects suggest overfitting.
- Diagnostic residual plots show roughly symmetric, zero-centered distribution after outlier down-weighting; standardized residuals do not exceed ±3–4 sigma for retained points.
- Fitted spline coefficients are stable across random seed repetitions (seed=100); model selection reproducible.
- Final model object contains non-null slots for coefficients, basis functions, and weights; GAM summary shows significant smooth term (p < 0.05) indicating meaningful RT–m/z relationship.

## Limitations

- Outlier filtering threshold (coef=2) and proportion (prop=0.5) are heuristic and may require tuning for datasets with systematically biased anchor selection or extreme measurement noise.
- 10-fold cross-validation assumes anchor points are independent and identically distributed; clustered or time-correlated errors may bias k selection.
- GAM with B-spline basis assumes smooth nonlinear relationship; sharp discontinuities or multi-modal RT drift patterns within the anchor range may not be captured.
- Reproducibility via seed=100 is framework-specific; cross-platform or updated package versions may produce slightly different random subsets during cross-validation fold assignment.

## Evidence

- [other] Iterative outlier filtering and basis dimension selection mechanism: "The fit_gam function performs iterative outlier filtering where points are flagged as outliers if their absolute error to mean absolute model error ratio exceeds the coef argument in over prop of the"
- [other] GAM setup with B-spline basis and smoothness penalty: "Fit a GAM spline using mgcv::gam with bs='bs' (B-spline basis), family='gaussian', and smoothness penalty m=c(3,2) across candidate k values from 12 to 20 in steps of 2."
- [other] Iterative filtering parameters and reproducibility: "Apply iterative filtering with iterFilter=2 iterations and coefficient threshold coef=2 to identify and downweight outliers, using prop=0.5 to proportion outlier contributions. 5. Retain the final"
- [intro] Anchor selection context in workflow: "3) Anchor Selection and RT Mapping Spline"
- [intro] RT mapping function in metabCombiner: "a modified form of the `gam` function implemented in the *mgcv* R package"
