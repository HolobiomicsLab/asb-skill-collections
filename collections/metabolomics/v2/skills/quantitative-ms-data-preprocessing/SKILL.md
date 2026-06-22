---
name: quantitative-ms-data-preprocessing
description: Use when you have raw MS intensity tables showing systematic drift during a measurement sequence (e.g., declining or variable ion counts across a run), particularly in targeted quantification workflows where external calibration standards are available.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3564
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# quantitative-ms-data-preprocessing

## Summary

Correct intensity drifts in targeted mass spectrometry datasets using external calibration and multiple drift correction strategies (Internal Standard, statistical models, bracketing methods) to ensure accurate quantification before downstream analysis. This skill is essential when intensity artifacts accumulate during MS measurement runs and would otherwise bias quantitative results.

## When to use

Apply this skill when you have raw MS intensity tables showing systematic drift during a measurement sequence (e.g., declining or variable ion counts across a run), particularly in targeted quantification workflows where external calibration standards are available. Intensity drift is a common artifact in long MS runs and must be corrected before reliable concentration estimates can be derived.

## When NOT to use

- Input MS data has already been corrected for intensity drift by an earlier preprocessing step.
- No calibration standards or external reference materials are available in the measurement sequence.
- The measurement run is very short (< 10–20 samples) with no observable intensity drift; correction may introduce noise without benefit.

## Inputs

- Raw MS intensity table (with sample and calibration standard intensities indexed by measurement position)
- Calibration standard intensities (external calibration curve data)
- Sample metadata (measurement sequence order, sample types, standard assignments)

## Outputs

- Drift-corrected MS intensity table
- Corrected quantification estimates (concentrations or amounts derived from calibration)
- Regression model parameters and fit statistics

## How to apply

Load your raw MS intensity table (with sample intensities and calibration standard intensities indexed by measurement position/time) into QuantyFey. Select one or more drift correction strategies based on your experimental design: (1) Internal Standard (IS) correction if suitable internal standards were co-analyzed; (2) statistical drift correction (linear or quadratic regression) to model intensity decay across the run; (3) Custom Bracketing to assign calibration curves to predefined blocks of the sequence; or (4) Weighted Bracketing to interpolate calibration curves between standards based on sample position. Use the Interactive Regression Model Optimization module to manually inspect and tune the chosen model, or invoke the Automatic Optimization module to select the best-fit regression model (linear vs. quadratic) and appropriate standard levels automatically. Export the corrected intensity table in standard MS quantification format and verify that residual drift artifacts are removed and quantification accuracy is improved.

## Related tools

- **QuantyFey** (Interactive Shiny application for visualization, drift correction strategy selection, regression model optimization, and export of corrected MS quantification data.) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Corrected intensity table shows linearized or smoothed trend across the measurement sequence (visual inspection of drift-corrected vs. raw intensities).
- Regression model fit statistics (R², residual standard error) indicate good agreement between observed and predicted calibration curve intensities.
- Quantification accuracy improves: replicate standard measurements show lower coefficient of variation (CV) in corrected vs. uncorrected data.
- Residual plot (observed minus predicted intensity) shows random scatter around zero with no systematic trends remaining.
- Output file schema matches standard MS quantification format (e.g., column headers for sample ID, corrected intensity, calculated concentration).

## Limitations

- QuantyFey is compatible with Windows operating systems only (standalone version); Linux users must use the Apptainer version, and macOS support is limited and slow.
- Automatic optimization assumes linear or quadratic regression models; more complex drift patterns (e.g., exponential or periodic) may not be captured.
- Correction quality depends on the number and distribution of calibration standards across the measurement sequence; sparse or poorly distributed standards may yield unreliable drift estimates.
- No changelog is available for version history or bug fixes.
- The tool requires R 4.2.x or R 4.5.x for direct R/RStudio launch and RTools 4.2 for Windows standalone installation.

## Evidence

- [readme] QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data using external calibration.: "QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data using external calibration."
- [readme] It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification.: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification."
- [readme] QuantyFey offers multiple correction strategies including Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification, and Weighted Bracketing.: "commonly applied drift correction methods: Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification (Assigning calibration data to predefined"
- [readme] The application provides automatic selection of linear or quadratic regression models and appropriate standards.: "Automatic Optimization Module - automatic selection of linear or quadratic regression model, and selection of appropriate standards."
- [other] Corrected intensity table with drift artifacts removed is exported in standard MS quantification format.: "Generate corrected intensity table with drift artifacts removed. Export corrected intensity data in standard MS quantification format."
- [readme] QuantyFey is compatible with Windows operating systems only.: "QuantyFey is compatible with Windows operating systems only."
- [readme] The application works as an additional software to already integrated mass spectrometry data and provides tools to effectively handle intensity drift during measurement.: "Especially when Intensity Drift is observed during the Measurement, the app provides the user with tools to effectively handle these drift."
