---
name: regression-model-validation-quantification
description: Use when when you have fitted one or more regression models (linear or polynomial) to external calibration standards in MS data and need to verify model adequacy before applying it to unknown samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - QuantyFey
derived_from:
- doi: 10.1016/j.aca.2025.344571
  title: quantyfey
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_quantyfey
    doi: 10.1016/j.aca.2025.344571
    title: quantyfey
  dedup_kept_from: coll_quantyfey
schema_version: 0.2.0
---

# regression-model-validation-quantification

## Summary

Validate and optimize regression models (linear or polynomial) fitted to mass spectrometry external calibration data to ensure accurate conversion of raw intensity measurements to quantified concentration values. This skill ensures the selected model appropriately captures the intensity–concentration relationship and correctly handles intensity drift correction.

## When to use

When you have fitted one or more regression models (linear or polynomial) to external calibration standards in MS data and need to verify model adequacy before applying it to unknown samples. Specifically when intensity drift is observed during measurement and you must choose between competing correction strategies (IS correction, drift correction, bracketing, or weighted bracketing) to ensure the fitted model reliably predicts concentration from raw intensity.

## When NOT to use

- If raw intensity data have not yet been loaded or calibration standards have not been measured.
- If the intensity–concentration relationship is known to be nonlinear beyond quadratic order (QuantyFey supports only linear and quadratic models).
- If no drift correction is needed and the simple linear model with default weights is deemed sufficient without interactive inspection.

## Inputs

- Raw MS intensity measurements for calibration standards
- Known concentration values for calibration standards
- Fitted regression model(s) (linear or polynomial)
- Drift correction strategy choice (Internal Standard, Drift Correction, Custom Bracketing, or Weighted Bracketing)

## Outputs

- Validated regression model with selected parameters and weights
- Goodness-of-fit summary (R², RMSE, residual plots)
- Calibration curve visualization with fitted line and standard points
- Model selection report (optimal model order and standard subset)

## How to apply

Load the fitted calibration curve(s) and corresponding known standard measurements and their predicted intensity values. Inspect residuals and goodness-of-fit metrics (e.g., R², RMSE) to assess whether the model explains the intensity–concentration relationship adequately. Use QuantyFey's Interactive Regression Model Optimization module to manually adjust model order (linear vs. quadratic), weight settings, and standard level inclusion, comparing model performance across drift correction strategies. Alternatively, invoke the Automatic Optimization Module to computationally select the best linear or quadratic model and appropriate standard subset. Validate the chosen model by verifying that predictions on held-out calibration standards fall within acceptable error bounds, and confirm visual fit quality on a calibration curve plot. Only after validation passes should the model be applied to quantify unknown samples.

## Related tools

- **QuantyFey** (Shiny application providing Interactive Regression Model Optimization and Automatic Optimization Module for selection and validation of linear or quadratic calibration models with multiple drift correction strategies) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Fitted model achieves R² or other goodness-of-fit metric within acceptable range (typically R² > 0.95 for MS quantification).
- Residual plots show random scatter around zero with no systematic patterns or heteroscedasticity.
- Predicted values for all calibration standards fall within pre-defined error tolerance (e.g., within ±10–15% of known concentration).
- Model order selection (linear vs. quadratic) is supported by AIC/BIC or by visual improvement in fit quality when tested on validation subset.
- Calibration curve visualization overlays fitted regression line cleanly through standard points without visible outliers or systematic deviation.

## Limitations

- QuantyFey is compatible with Windows operating systems only for the standalone version; Apptainer version is available for Linux but runs slowly on macOS.
- Model selection is restricted to linear and quadratic (polynomial order 2) regression; nonlinear relationships beyond quadratic order cannot be modeled.
- The application does not provide integration capabilities; it accepts pre-extracted mass spectrometry data and assumes proper calibration standard assignment to sequence blocks.
- No changelog is available to track changes in model optimization algorithms or validation criteria across versions.

## Evidence

- [readme] Interactive Regression Model Optimization allows manual adjustment of model, weights, and standard levels.: "**Interactive Regression Model Optimization** - manual adjustment of model, weights, standard levels etc."
- [readme] Automatic Optimization Module selects the best linear or quadratic regression model and appropriate standards.: "**Automatic Optimization Module** - automatic selection of **linear** or **quadratic** regression model, and selection of appropriate standards."
- [other] Fitted calibration model is applied to raw intensity data to compute quantified concentration values.: "Apply the fitted calibration model to raw intensity data to compute quantified concentration values."
- [intro] QuantyFey is designed to address intensity drifts and offers multiple correction strategies for accurate quantification.: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification"
