---
name: intensity-to-concentration-conversion
description: Use when you have raw MS intensity data paired with measurements from known concentration standards, and you need to produce absolute quantified concentration values rather than relative intensity measurements.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - QuantyFey
derived_from:
- doi: 10.1016/j.aca.2025.344571
  title: quantyfey
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_quantyfey
    doi: 10.1016/j.aca.2025.344571
    title: quantyfey
  dedup_kept_from: coll_quantyfey
schema_version: 0.2.0
---

# intensity-to-concentration-conversion

## Summary

Convert raw mass spectrometry intensity measurements into quantified concentration values using external calibration curve fitting. This skill is essential when processing targeted MS data that exhibits intensity drift, requiring application of drift-corrected calibration models to produce concentration tables with sample identifiers.

## When to use

Apply this skill when you have raw MS intensity data paired with measurements from known concentration standards, and you need to produce absolute quantified concentration values rather than relative intensity measurements. This is particularly critical if the MS run shows evidence of intensity drift over the measurement sequence, which would bias uncorrected intensity-to-concentration mapping.

## When NOT to use

- Input data are already quantified concentrations or relative abundance values—skip to downstream analysis.
- MS data lack calibration standards or standard measurements are not available—external calibration cannot be constructed.
- Intensity values span multiple orders of magnitude without preprocessing—consider log-transformation or heteroscedastic weighting before model fitting.

## Inputs

- raw MS intensity measurements (per sample, per analyte)
- calibration standard measurements with known concentration values
- sample sequence metadata (for drift detection and bracketing)
- optional: internal standard intensity data (for IS-correction workflows)

## Outputs

- quantified concentration table with sample identifiers and concentration values
- calibration curve fit statistics and model parameters
- drift-corrected intensity profiles (if drift correction applied)

## How to apply

Load raw MS intensity data and corresponding calibration standard measurements into the quantification module. Fit external calibration curves (linear or polynomial regression) relating intensity to known concentration standards, selecting the regression model (linear or quadratic) that best describes the relationship. If intensity drift is detected, apply one of the available correction strategies—Internal Standard (IS) correction, statistical drift correction, Custom Bracketing (assigning calibration data to predefined blocks of the sequence), or Weighted Bracketing (weighting calibration curves based on sample position between standards). Apply the fitted and corrected calibration model to raw intensity data to compute quantified concentration values. Output a concentration table with sample identifiers and quantified values, verifying that the model achieves acceptable fit statistics and that quantified values fall within the range of the calibration standards used.

## Related tools

- **QuantyFey** (Shiny application for interactive external calibration, drift correction, and quantification of targeted MS data; provides manual and automatic regression model optimization, multiple drift correction strategies (IS, bracketing, weighted bracketing), and concentration table output.) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Calibration curve R² or adjusted R² exceeds 0.95 for the fitted regression model (linear or polynomial).
- Quantified concentrations for all samples fall within the calibration range (bounded by minimum and maximum standard concentrations used).
- Sample replicates (if available) yield concentration values with relative standard deviation < 20% (or journal/laboratory-specific target).
- Drift-correction strategy (if applied) reduces residual intensity variation across the sequence, verifiable by comparing pre- and post-correction calibration curve fit statistics.
- Output concentration table contains no missing or out-of-range values for samples within the valid measurement window.

## Limitations

- QuantyFey is compatible with Windows operating systems only for the standalone version; Apptainer version available for Linux but runs slowly on macOS.
- The skill assumes linear or polynomial relationships between intensity and concentration; non-linear response curves (e.g., saturation effects) may require log transformation or alternative calibration models not explicitly described in the README.
- Intensity drift correction depends on the temporal spacing and quality of calibration standards in the run; sparse or poorly distributed standards may yield unreliable drift estimation.
- External calibration is sensitive to matrix effects and ion suppression that differ between calibration standards and samples; if sample matrices differ significantly from standard matrices, quantification bias may persist despite drift correction.

## Evidence

- [other] Fit external calibration curves (linear or polynomial regression) relating intensity to known concentration standards.: "Fit external calibration curves (linear or polynomial regression) relating intensity to known concentration standards."
- [other] Apply the fitted calibration model to raw intensity data to compute quantified concentration values.: "Apply the fitted calibration model to raw intensity data to compute quantified concentration values."
- [readme] QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data using external calibration.: "QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data using external calibration."
- [readme] It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification.: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification."
- [readme] automatic selection of linear or quadratic regression model, and selection of appropriate standards.: "automatic selection of linear or quadratic regression model, and selection of appropriate standards."
- [readme] QuantyFey is compatible with Windows operating systems only.: "QuantyFey is compatible with Windows operating systems only."
