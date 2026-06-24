---
name: ms-quantitative-analysis-standards
description: Use when you have raw MS intensity data paired with known-concentration
  calibration standard measurements, and you need to convert intensities to absolute
  or relative concentrations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - QuantyFey
  techniques:
  - mass-spectrometry
  license_tier: restricted
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

# MS Quantitative Analysis via External Calibration Standards

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A method for converting raw mass spectrometry intensity measurements into quantified concentration values by fitting external calibration curves (linear or polynomial regression) against known concentration standards and applying the model to sample data. Essential for handling intensity drift in targeted MS workflows.

## When to use

You have raw MS intensity data paired with known-concentration calibration standard measurements, and you need to convert intensities to absolute or relative concentrations. This is especially critical when intensity drift is observed across the measurement sequence, as calibration curves must be fitted and optionally reweighted to account for temporal drift.

## When NOT to use

- Input is untargeted MS data without pre-identified analytes or m/z targets — use feature detection and alignment first.
- Calibration standards are absent or their concentration values are unknown — external calibration cannot be performed; consider internal standard normalization only.
- Intensity values show no detectable drift and linear response across the measurement range is confirmed — simpler single-curve calibration may suffice.

## Inputs

- Raw MS intensity data (with m/z and retention time dimensions)
- Calibration standard measurements with known concentration values
- Sample identifiers and measurement sequence order
- Optional: internal standard peak intensities (for IS correction)

## Outputs

- Quantified concentration table (sample ID × analyte × concentration)
- Fitted calibration curve parameters (slope, intercept, model order)
- Drift correction factors or model coefficients
- Residual diagnostics and model quality metrics (R², RMSE)

## How to apply

Load raw MS intensity data and corresponding calibration standard measurements into a regression framework. Fit external calibration curves using linear or polynomial regression, relating measured intensity to known concentration standards. Choose model order (linear vs. quadratic) based on residual diagnostics and R² fit quality. If intensity drift is detected, apply drift correction via internal standard (IS) normalization, statistical drift models, custom bracketing (assigning calibration data to sample blocks), or weighted bracketing (reweighting calibration curves based on sample position between standards). Apply the fitted calibration model to raw sample intensities to compute quantified concentrations. Output a concentration table with sample identifiers and quantified values, including uncertainty estimates where applicable.

## Related tools

- **QuantyFey** (Interactive Shiny application for MS data quantification via external calibration; provides drift correction strategies (IS correction, statistical drift models, custom/weighted bracketing), interactive and automatic regression model optimization (linear/quadratic), and concentration output.) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Calibration curve R² value is ≥ 0.99 and residuals show no systematic trend with concentration (visual inspection or Shapiro–Wilk test).
- Quantified sample concentrations fall within expected biological or analytical ranges (e.g., detection limit to quantitation limit); outliers are flagged and investigated.
- Drift-corrected calibration curves (internal standard, bracketed, or weighted) show reduced residual variance compared to uncorrected curve when intensity drift is present.
- Back-calculated concentration of calibration standards from the fitted model agrees with nominal values within ±15–20% (typical acceptable error in MS quantification).
- Output concentration table contains no missing or infinite values; all sample identifiers are preserved and matched to their original measurement records.

## Limitations

- QuantyFey is compatible with Windows operating systems only for the standalone version; Apptainer (Linux) and R/RStudio (Windows, Linux, macOS) alternatives are available but more complex to configure.
- External calibration assumes linearity or low-order polynomial response over the measured intensity range; non-linear or biphasic responses may require segmented calibration or alternative quantification strategies.
- Drift correction methods (IS, bracketing, weighted bracketing) require that calibration standards are interspersed regularly throughout the measurement sequence; sparse or clustered standards limit correction effectiveness.
- The application requires pre-integrated MS data (e.g., peak areas or heights for each analyte and standard); it does not provide raw spectrum integration or m/z alignment and is designed as a post-integration analysis tool.

## Evidence

- [other] External calibration methodology and curve fitting: "QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data using external calibration"
- [other] Drift correction as a key application driver: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification"
- [readme] Multiple drift correction strategies: "Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification, Weighted Bracketing"
- [readme] Regression model optimization: "automatic selection of linear or quadratic regression model, and selection of appropriate standards"
- [other] Calibration workflow steps: "Fit external calibration curves (linear or polynomial regression) relating intensity to known concentration standards. Apply the fitted calibration model to raw intensity data to compute quantified"
- [other] Windows-only limitation of standalone: "QuantyFey is compatible with Windows operating systems only"
- [readme] Post-integration tool scope: "This app works as an additional software to already integrated mass spectrometry data, and does not provide any integration cabailities"
