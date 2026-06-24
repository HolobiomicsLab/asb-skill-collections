---
name: calibration-curve-validation
description: Use when when you have loaded standard compound MS intensity measurements
  with known concentrations and need to select between linear or quadratic regression
  models before applying the calibration to unknown samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Shiny
  - QuantyFey
  license_tier: open
derived_from:
- doi: 10.1016/j.aca.2025.344571
  title: quantyfey
evidence_spans:
- '**QuantyFey** is a Shiny application for the **visualization, analysis, and quantification**
  of **mass spectrometry (MS) data**'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_quantyfey_cq
    doi: 10.1016/j.aca.2025.344571
    title: quantyfey
  dedup_kept_from: coll_quantyfey_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.aca.2025.344571
  all_source_dois:
  - 10.1016/j.aca.2025.344571
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# calibration-curve-validation

## Summary

Validate and optimize calibration models (linear or quadratic regression) fitted to standard compound MS intensity measurements before applying them to convert sample intensities into quantitative concentrations. This skill ensures that the selected model accurately relates measured intensities to known concentrations across the dynamic range of the assay.

## When to use

When you have loaded standard compound MS intensity measurements with known concentrations and need to select between linear or quadratic regression models before applying the calibration to unknown samples. Particularly important when intensity drift is observed across a measurement sequence, requiring model optimization and selection of appropriate standard levels.

## When NOT to use

- Sample MS intensity data without any standard compounds available for model fitting.
- When the instrument platform does not measure MS intensity linearly or exhibits non-standard response behavior that violates regression model assumptions.
- Input data already processed through validated external calibration by another quantification tool; re-validation may introduce inconsistency.

## Inputs

- Standard compound MS intensity measurements
- Known standard concentrations
- MS intensity data file (format compatible with QuantyFey)

## Outputs

- Validated calibration model (linear or quadratic regression)
- Model parameters and regression coefficients
- Residual diagnostics and goodness-of-fit metrics
- Selected subset of standards deemed appropriate for quantification

## How to apply

Fit candidate calibration models (linear and quadratic regression) relating MS intensity to standard concentrations. Use QuantyFey's interactive regression model optimization module to manually adjust model parameters, weights, and standard level inclusion, or use the automatic optimization module to select the best-fit model and appropriate standards. Evaluate model quality by inspecting residuals, goodness-of-fit metrics, and prediction accuracy across standard levels. Apply the validated model to convert sample MS intensities into predicted concentrations only after confirming adequate model performance and sensitivity to expected concentration ranges.

## Related tools

- **QuantyFey** (Shiny application for interactive calibration model optimization, selection, and application; provides both manual regression model adjustment and automatic optimization modules for linear/quadratic model selection) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Model residuals are randomly distributed around zero with no systematic bias across the standard concentration range.
- Goodness-of-fit metrics (R², residual standard error) meet predefined acceptance criteria for the analytical method.
- Predicted concentrations for held-out or replicate standards fall within expected accuracy bounds (e.g., ±10–20% of nominal values).
- Selected standard levels span the full dynamic range of expected sample concentrations without extrapolation beyond the highest or lowest standard.
- Model selection is consistent between manual optimization and automatic optimization modules, or documented rationale explains deliberate deviation.

## Limitations

- QuantyFey is compatible with Windows operating systems only for the standalone version; Linux users must use the Apptainer container, and macOS support is slow and difficult to configure.
- Calibration curve validation assumes linearity or quadratic relationships; non-linear or sigmoidal dose–response curves are not natively supported.
- Interactive model optimization requires manual intervention and domain expertise; automatic optimization may not detect misspecified models if outliers or systematic errors in standards are present.
- Validation is performed on standards only; true predictive performance on unknown samples cannot be fully assessed without external reference or replicate measurements.

## Evidence

- [readme] QuantyFey provides Interactive Regression Model Optimization and Automatic Optimization Module: "**Interactive Regression Model Optimization** - manual adjustment of model, weights, standard levels etc. **Automatic Optimization Module** - automatic selection of **linear** or **quadratic**"
- [other] Calibration model fitting workflow with standards and samples: "1. Load standard compound MS intensity measurements and their known concentrations. 2. Fit a calibration model (linear or non-linear regression) relating intensity to concentration using the"
- [other] Model application to predict sample concentrations: "3. Load sample MS intensity data. 4. Apply the fitted calibration model to convert sample intensities into predicted concentrations."
- [intro] Intensity drift correction strategies affecting model selection: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification"
- [readme] Bracketing and weighting approaches for calibration curve validation: "**Custom Bracketing** Quantification (Assigning calibration data to predefined blocks of the sequence). **Weighted Bracketing** Weighting of calibration curves based on the position of the samples"
