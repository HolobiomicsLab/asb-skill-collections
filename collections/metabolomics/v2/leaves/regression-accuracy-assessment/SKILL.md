---
name: regression-accuracy-assessment
description: Use when after fitting linear regression models to relate peak area intensities
  to known concentrations in targeted metabolomics curves (standard samples and quality
  control replicates).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GetFeatistics
  - lme4
  - AER
  - R (base stats)
  license_tier: open
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)
- The **GetFeatistics** (GF) package provides several functions useful for the elaboration
  of metabolomics data
- linear models with mixed effects (random and fixed), using the _lmer_ function from
  the lme4 package
- TOBIT linear models, using the _tobit_ function of the AER package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# regression-accuracy-assessment

## Summary

Evaluate the predictive accuracy and quality of linear regression models fitted to targeted metabolomics calibration data by computing coefficient of determination (R²), mean absolute error, and internal standard reproducibility metrics. This skill validates whether concentration predictions are reliable enough for downstream interpretation.

## When to use

After fitting linear regression models to relate peak area intensities to known concentrations in targeted metabolomics curves (standard samples and quality control replicates). Apply this skill when you need to validate model fit quality, assess whether predictions for unknown samples will be trustworthy, and quantify systematic bias or measurement noise via internal standard variability.

## When NOT to use

- Input peak areas have not been normalized to internal standards or do not have matched internal standards assigned.
- Calibration curve is non-linear or spans multiple orders of magnitude requiring log-transformation or segmented regression (use non-linear fitting instead).
- QC sample replicates are too few (n < 3) to reliably estimate internal standard CV or regression residuals.

## Inputs

- peak area intensity table (samples × compounds)
- sample legend with type classification (blank/curve/qc/unknown) and known concentration values
- compound legend with internal standard assignments and metadata
- fitted linear regression models (from lm or lmer function)

## Outputs

- results_accuracy table (R² values for curves and QC points, mean absolute error)
- cv_internal_standards metric (relative standard deviation of internal standard intensities)
- summary_regression_models (slope, intercept, R², residual standard error, p-values)
- compound-level accuracy assessment report (pass/fail per compound)

## How to apply

Extract from the get_targeted_elaboration output the results_accuracy table (containing R² values for calibration curves and QC sample predictions), the cv_internal_standards metric (relative standard deviation of internal standard intensities across samples), and summary_regression_models (slope, intercept, and fit statistics). Compare R² to a project-defined threshold (typically >0.95 for good fit in metabolomics); flag models with R² below this as requiring recalibration or compound exclusion. Cross-check accuracy by computing mean absolute error between predicted and actual concentrations for QC samples. Calculate and document the coefficient of variation (CV%) of internal standards; CV > ~20–25% indicates high instrumental noise or normalization problems requiring investigation. Synthesize these three metrics (R², MAE, CV_IS) into a single quality report that identifies which compounds meet accuracy requirements.

## Related tools

- **GetFeatistics** (Provides get_targeted_elaboration function that computes regression models, accuracy metrics (R², MAE), and internal standard CV for targeted metabolomics data.) — https://github.com/FrigerioGianfranco/GetFeatistics
- **lme4** (Fits linear models with mixed effects (random and fixed) for calibration when accounting for batch or instrumental variation in internal standards.)
- **AER** (Provides tobit function for censored regression models when dealing with features below limit of detection (LOD) in QC or calibration samples.)
- **R (base stats)** (Core lm function fits linear regression models to calibration data; used as foundation for accuracy assessment.)

## Examples

```
library(GetFeatistics); result <- get_targeted_elaboration(df_example_targeted, df_example_targeted_legend, df_example_targeted_compounds_legend); accuracy_df <- result$results_accuracy; cv_is <- result$cv_internal_standards; cat('R² =', accuracy_df$r_squared, 'CV_IS =', cv_is, '%\n')
```

## Evaluation signals

- R² for each compound's calibration curve is ≥ 0.95 (or project-defined threshold); R² < 0.90 triggers manual review or exclusion.
- Mean absolute error (MAE) for QC predictions is within ±10–15% of nominal concentration (or smaller, depending on instrument and metabolite class).
- Coefficient of variation (CV%) of internal standard intensities across all samples is ≤ 20–25%; CV > 30% suggests instrumental drift or normalization failure.
- Residuals from regression models are approximately normally distributed (Shapiro–Wilk p > 0.05) with no systematic bias across the concentration range.
- Predictions for unknown samples fall within the calibration range (no extrapolation beyond curve endpoints) and have confidence intervals that do not cross zero.

## Limitations

- Accuracy assessment assumes that internal standards are truly invariant across samples and that peak area normalization is correct; if internal standard concentrations drift or ionization efficiency varies, reported CV and R² may be artificially inflated.
- Linear regression assumes homoscedasticity (constant variance across concentration range); heteroscedastic data (e.g., higher CV at low concentrations) may yield inflated R² and underestimated prediction intervals.
- QC sample size and concentration distribution affect the sensitivity of accuracy metrics; sparse or uneven QC sampling (e.g., QC only at high concentrations) can mask poor fit at low concentrations.
- The package does not automatically flag or exclude outlier peaks or samples that strongly violate regression assumptions; manual inspection of residual plots is required to detect such cases.

## Evidence

- [other] get_targeted_elaboration returns results_accuracy (accuracy % for curve and QC points), cv_internal_standards (relative standard deviation of internal standard intensities): "get_targeted_elaboration returns a list containing: results_concentrations (calculated concentrations), results_accuracy (accuracy % for curve and QC points), cv_internal_standards (relative standard"
- [intro] Linear regression models with fixed effects, mixed effects, and TOBIT censored regression available: "linear models (with fixed effects), using the _lm_ function...linear models with mixed effects (random and fixed), using the _lmer_ function...TOBIT linear models, using the _tobit_ function"
- [other] Regression model summaries include slope, intercept, and R² values for validation: "summary_regression_models (slope, intercept, R² values), and regression_models (fitted linear regression models)"
- [readme] Package documentation emphasizes QC processing and statistical validation workflows: "Getting streamlined elaboration of targeted and non-targeted metabolomics data, including elaboration of feature tables, separate QC processing, advanced statistics"
- [intro] Targeted analyses require sample type classification (blank, curve, qc) and known concentration values: "the second column should contain the following: "blank", "curve", "qc", or "unknown". the third column should have the actual known values for "curve" and "qc" samples"
