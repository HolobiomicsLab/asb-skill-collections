---
name: intensity-to-concentration-conversion
description: Use when you have raw mass spectrometry intensity measurements from sample analyses and need absolute quantitative concentrations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
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
  - build: coll_quantyfey
    doi: 10.1016/j.aca.2025.344571
    title: quantyfey
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

# intensity-to-concentration-conversion

## Summary

Convert mass spectrometry signal intensities into quantitative analyte concentrations using external calibration regression. This skill applies a fitted calibration model (linear or non-linear) derived from standard compounds to unknown sample intensity measurements, accounting for intensity drift during measurement runs.

## When to use

Use this skill when you have raw mass spectrometry intensity measurements from sample analyses and need absolute quantitative concentrations. Trigger conditions include: (1) you have measured MS intensities for both calibration standards (with known concentrations) and unknown samples in the same analytical run; (2) intensity drift is observed or suspected during the measurement sequence; (3) you need tabular concentration predictions rather than relative abundance or peak area data.

## When NOT to use

- Your MS data lacks measured calibration standards or known reference concentrations—relative quantification methods should be used instead.
- You are performing untargeted metabolomics or discovery-mode analysis where absolute concentration calibration is not required.
- Your intensity measurements are already normalized to a feature table or have been pre-processed by integrated MS data acquisition software with built-in quantification.

## Inputs

- Standard compound MS intensity measurements paired with known reference concentrations (tabular format)
- Sample MS intensity measurements (tabular format)
- Measurement sequence metadata (for drift detection and bracketing-based corrections)
- Optional: internal standard intensity values (for IS-based drift correction)

## Outputs

- Fitted calibration model (linear or non-linear regression coefficients and model parameters)
- Predicted sample concentrations in tabular format
- Diagnostic plots (intensity vs. concentration, residual plots, model fit visualization)
- Drift-corrected intensity data (if drift correction was applied)

## How to apply

Load standard compound MS intensity measurements paired with their known concentrations into QuantyFey. Fit a calibration model (linear or non-linear regression) relating intensity to concentration using the standards dataset. Inspect the fitted model graphically and optimize using QuantyFey's interactive regression module or automatic optimization (which selects between linear and quadratic models). Load sample MS intensity data and apply the fitted calibration model to convert each sample intensity into a predicted concentration. If intensity drift is detected across the run, select an appropriate drift correction strategy (Internal Standard correction, statistical drift correction, custom bracketing, or weighted bracketing) before or during model fitting. Export concentration predictions in tabular format for downstream analysis.

## Related tools

- **QuantyFey** (Shiny application that implements external calibration quantification with interactive regression model optimization, automatic model selection (linear vs. quadratic), and multiple drift correction strategies (Internal Standard, statistical drift correction, custom bracketing, weighted bracketing)) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Calibration model R² or goodness-of-fit metric meets domain standards (typically R² > 0.99 for targeted MS quantification).
- Predicted sample concentrations fall within expected biological or analytical ranges (e.g., no negative values, values consistent with spike-in or recovery study expectations).
- Residual plots show no systematic pattern or heteroscedasticity; residuals are approximately normally distributed around zero.
- If drift correction was applied, intensity-drift-corrected sample intensities show reduced correlation with measurement sequence position compared to raw intensities.
- Cross-validation or independent replicate analysis yields consistent concentration predictions (coefficient of variation < 15–20% typical for quantitative MS).

## Limitations

- QuantyFey standalone version is compatible with Windows operating systems only; Linux and macOS users must use the Apptainer containerized version or launch from R/RStudio directly, which requires additional prerequisites and can be slow on macOS.
- The skill assumes intensity drift is linear or can be modeled by the available statistical/bracketing correction strategies; nonlinear or instrument-specific drift patterns may not be adequately corrected.
- Accuracy depends on the assumption that calibration standards and samples are measured under identical MS conditions and ionization efficiency; matrix effects or ion suppression not accounted for by internal standard correction will reduce prediction accuracy.
- The application does not integrate raw MS data directly; pre-extracted intensity measurements must be provided in tabular format, limiting automation in high-throughput environments.

## Evidence

- [other] external calibration methodology workflow: "Fit a calibration model (linear or non-linear regression) relating intensity to concentration using the standards. Load sample MS intensity data. Apply the fitted calibration model to convert sample"
- [readme] drift correction strategies: "commonly applied drift correction methods: Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification, Weighted Bracketing"
- [readme] automated model selection: "Automatic Optimization Module - automatic selection of linear or quadratic regression model, and selection of appropriate standards."
- [readme] intensity drift design rationale: "QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data using external calibration. It is specifically designed to address intensity drifts"
- [other] output format specification: "Export concentration predictions in tabular format."
