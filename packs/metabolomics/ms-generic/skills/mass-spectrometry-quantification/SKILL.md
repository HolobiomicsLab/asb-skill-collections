---
name: mass-spectrometry-quantification
description: Use when you have measured MS intensity data from unknown samples and known-concentration standard compounds, and you need to convert sample intensities into predicted concentrations. Specifically applicable when intensity drift is observed across the measurement sequence (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Shiny
  - QuantyFey
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1016/j.aca.2025.344571
  title: quantyfey
evidence_spans:
- '**QuantyFey** is a Shiny application for the **visualization, analysis, and quantification** of **mass spectrometry (MS) data**'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-quantification

## Summary

Convert raw mass spectrometry intensities into quantitative analyte concentrations using external calibration with regression modeling, accounting for intensity drift through drift correction strategies. This skill is essential when processing targeted MS data where accurate concentration prediction depends on fitting and applying calibration curves derived from known standard compounds.

## When to use

You have measured MS intensity data from unknown samples and known-concentration standard compounds, and you need to convert sample intensities into predicted concentrations. Specifically applicable when intensity drift is observed across the measurement sequence (e.g., systematic signal loss or gain over time) and you require multiple drift correction strategies (internal standard correction, statistical drift models, bracketing, or weighted bracketing) to ensure accuracy.

## When NOT to use

- Input is already a feature table or preprocessed concentration values—no need to apply calibration and quantification again.
- MS data has not been processed for peak integration or intensity extraction; raw spectral data requires preprocessing before calibration.
- Running on macOS or Linux without Apptainer—standalone QuantyFey is Windows-only; alternative deployment (Apptainer or R/RStudio launch) required on other platforms.

## Inputs

- Standard compound MS intensity measurements with known concentrations (CSV or tabular format)
- Sample MS intensity data (CSV or tabular format)
- Measurement sequence metadata (run order, timing) for drift correction

## Outputs

- Fitted calibration model (linear or quadratic regression coefficients)
- Sample concentration predictions (tabular format with concentration values and uncertainty)
- Calibration curve visualization with fitted model and residuals
- Drift correction parameters and model diagnostics

## How to apply

Load MS intensity measurements and known concentrations for standard compounds, then fit a calibration model (linear or quadratic regression) relating intensity to concentration. Select and apply an appropriate drift correction strategy—internal standard correction, custom bracketing (assigning calibration data to predefined sequence blocks), or weighted bracketing (weighting calibration curves by sample position between standards)—based on the degree and pattern of intensity drift observed. Apply the fitted and drift-corrected calibration model to sample intensities to predict concentrations. Use interactive optimization to manually adjust model type, weights, and standard levels, or invoke automatic optimization to select the best linear or quadratic model and appropriate standards. Export predictions in tabular format for downstream analysis.

## Related tools

- **Shiny** (Interactive web application framework for building the quantification interface, model optimization, and visualization)
- **QuantyFey** (Standalone Shiny application implementing the complete workflow for MS quantification with external calibration and drift correction) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Calibration curve R² or adjusted R² indicates good model fit (typically >0.95 for well-behaved standards).
- Residual plots show no systematic pattern; residuals are randomly distributed around zero, indicating adequate model specification.
- Predicted concentrations for quality control (QC) or replicate samples fall within expected ranges and have low coefficient of variation (CV) across replicates.
- Drift correction reduces or eliminates systematic trends in residuals when samples and standards are plotted in run order; post-correction residuals should not correlate with sequence position.
- Automatic optimization module selects a simpler model (linear) when quadratic adds no significant improvement; manual optimization produces predictions consistent with the automatic module on validation set.

## Limitations

- Windows operating system required for standalone version; Apptainer setup is more complicated on macOS and runs slowly.
- Application does not provide integration capabilities and requires pre-extracted MS intensities as input; no direct spectral processing functionality.
- Designed for targeted MS analysis with discrete standards; not suitable for untargeted quantification or complex multi-component matrices without prior method development.
- No changelog available to track version history, bug fixes, or method improvements.

## Evidence

- [other] External calibration methodology with regression modeling: "Fit a calibration model (linear or non-linear regression) relating intensity to concentration using the standards."
- [readme] Drift correction strategies for intensity variation: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies"
- [readme] Drift correction methods available: "commonly applied drift correction methods: Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification, Weighted Bracketing"
- [readme] Model optimization workflow: "Interactive Regression Model Optimization - manual adjustment of model, weights, standard levels etc. Automatic Optimization Module - automatic selection of linear or quadratic regression model"
- [readme] Windows-only standalone deployment: "QuantyFey is compatible with Windows operating systems only."
- [readme] Application scope and input/output: "This app works as an additional software to already integrated mass spectrometry data, and does not provide any integration cabailities, but rather offers the user an interactive tool for efficient"
