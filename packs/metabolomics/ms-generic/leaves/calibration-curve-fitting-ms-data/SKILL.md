---
name: calibration-curve-fitting-ms-data
description: Use when you have raw mass spectrometry intensity data from targeted analytes and a set of calibration standard measurements with known concentrations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - QuantyFey
  techniques:
  - mass-spectrometry
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

# calibration-curve-fitting-ms-data

## Summary

Fit external calibration curves (linear or polynomial regression) to mass spectrometry intensity measurements using known concentration standards, then apply the fitted model to convert raw sample intensities into quantified concentration values. Essential when intensity drift occurs during measurement runs.

## When to use

You have raw mass spectrometry intensity data from targeted analytes and a set of calibration standard measurements with known concentrations. Use this skill when you need to convert raw intensity measurements into absolute or relative concentration values, particularly when intensity drift is observed across the measurement sequence.

## When NOT to use

- Input is already a concentration table or absolute quantified feature matrix—direct calibration fitting would be inappropriate.
- Calibration standards are absent or have incomplete/unreliable concentration metadata.
- Mass spectrometry data is untargeted or uses internal calibration (e.g., lock masses) rather than external standards.
- Intensity measurements fall outside the range covered by calibration standards—extrapolation beyond the fitted domain may yield unreliable predictions.

## Inputs

- Raw MS intensity measurements (sample ions)
- Calibration standard measurements with known concentration values
- Sample identifiers and run sequence metadata
- Optional: internal standard intensity measurements

## Outputs

- Fitted calibration curve model (linear or polynomial)
- Quantified concentration table with sample identifiers and computed values
- Model diagnostics and regression statistics
- Drift-corrected intensity values (if correction applied)

## How to apply

Load raw MS intensity data alongside corresponding calibration standard measurements with known concentration values. Fit external calibration curves using linear or quadratic regression models relating intensity to concentration—QuantyFey's automatic optimization module can select the appropriate model degree and identify relevant standard levels. If intensity drift is detected during the measurement, apply correction strategies (internal standard correction, drift correction using statistical models, custom or weighted bracketing) before or during model fitting to account for systematic variation. Apply the fitted calibration model to all sample intensity measurements to compute quantified concentration values. Validate the model fit quality by inspecting regression diagnostics (residuals, R² values) and comparing predicted versus observed standard concentrations.

## Related tools

- **QuantyFey** (Interactive Shiny application for visualization, regression model optimization, automatic model selection, drift correction, and quantification of MS data via external calibration) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Fitted model R² and residual distribution: R² > 0.99 for high-quality calibration; residuals should be randomly distributed around zero with no systematic trend.
- Cross-validation or hold-out prediction: predicted concentrations of withheld calibration standards should match observed values within acceptable accuracy (e.g., ±10% relative error).
- Concentration table completeness: all samples have quantified values; no missing or NaN entries unless intentionally flagged.
- Model selection consistency: if automatic optimization is used, verify that the chosen model (linear vs. quadratic) matches visual inspection of the standard curve and produces lower residuals than competing models.
- Drift correction validation: if drift correction is applied, intensity-corrected standard measurements should show reduced systematic variation across the run sequence compared to raw intensity.

## Limitations

- QuantyFey is compatible with Windows operating systems only for the standalone version; Apptainer version available for Linux but runs slowly on macOS.
- The tool does not provide integration capabilities—it requires pre-processed, targeted MS data (ion intensities already extracted) as input.
- Calibration curves fitted outside the range of standards (extrapolation) are unreliable; predictions must remain within the concentration span of the standards.
- No changelog is publicly available, limiting transparency on version updates and method changes.
- Drift correction assumes that intensity drift follows one of the implemented statistical models (internal standard, polynomial, bracketing); complex non-linear or non-systematic drift may not be adequately corrected.

## Evidence

- [other] QuantyFey is a Shiny application designed for quantification of mass spectrometry data using external calibration methodology.: "QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data using external calibration"
- [other] The core workflow loads raw MS intensity and calibration data, fits calibration curves, and applies the model to compute sample concentrations.: "1. Load raw MS intensity data and corresponding calibration standard measurements. 2. Fit external calibration curves (linear or polynomial regression) relating intensity to known concentration"
- [readme] QuantyFey offers multiple strategies to handle intensity drift during measurement runs.: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification"
- [readme] The application provides automatic regression model optimization and interactive manual adjustment.: "Automatic Optimization Module - automatic selection of linear or quadratic regression model, and selection of appropriate standards"
- [readme] Multiple drift correction methods are implemented: internal standard, statistical drift correction, custom bracketing, and weighted bracketing.: "Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification, Weighted Bracketing Weighting of calibration curves based on the position of the"
