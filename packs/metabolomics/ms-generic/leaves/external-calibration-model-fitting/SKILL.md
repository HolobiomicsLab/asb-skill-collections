---
name: external-calibration-model-fitting
description: Use when you have acquired targeted mass spectrometry data with measured ion intensities for known standard compounds at multiple concentration levels, and you need to convert sample intensities into absolute or relative concentrations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# external-calibration-model-fitting

## Summary

Fit a calibration model (linear or non-linear regression) to relate mass spectrometry signal intensities to known standard concentrations, enabling conversion of sample intensities into quantitative predictions. This skill addresses intensity drift in MS datasets through multiple correction strategies (internal standard, drift correction, bracketing, weighted bracketing).

## When to use

You have acquired targeted mass spectrometry data with measured ion intensities for known standard compounds at multiple concentration levels, and you need to convert sample intensities into absolute or relative concentrations. Apply this skill especially when intensity drift is observed across the measurement sequence—drift that would bias uncorrected intensity-to-concentration relationships.

## When NOT to use

- Input is already a processed feature table or normalized concentration matrix—this skill operates on raw or drift-corrected intensities, not pre-quantified data.
- No standard compounds with known concentrations are available—the skill requires a calibration set to fit the model.
- Measurement sequence order is unknown or unavailable—drift correction strategies (bracketing, IS correction) depend on knowing sample position and timing.

## Inputs

- Standard compound MS intensity measurements (numeric intensities per compound)
- Standard compound reference concentrations (known concentration values)
- Sample MS intensity data (measured intensities for unknown samples)
- Measurement sequence metadata (sample order, time stamps for drift detection)

## Outputs

- Fitted calibration model (linear or quadratic regression parameters)
- Model diagnostics (R², residuals, weights applied per standard level)
- Sample concentration predictions (predicted concentrations in tabular format)
- Drift-corrected intensities (after internal standard, bracketing, or statistical correction)

## How to apply

Load standard compound MS intensity measurements alongside their known concentrations into QuantyFey. Select a regression model type (linear or quadratic) and choose appropriate standard levels; the automatic optimization module can assist model selection. Apply one or more drift correction strategies: internal standard (IS) correction for sample-by-sample normalization, statistical drift correction for systematic instrument drift, custom bracketing to assign calibration data to predefined measurement blocks, or weighted bracketing to weight calibration curves by sample position between calibrations. Fit the model to the corrected intensities. Validate the fitted model by examining residuals and R² values across the calibration range. Once validated, apply the fitted model to sample intensities to generate predicted concentrations.

## Related tools

- **QuantyFey** (Shiny application that implements external calibration model fitting with drift correction, regression optimization (linear/quadratic), and bracketing-based quantification strategies) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Fitted model R² is ≥ 0.95 across the calibration range, indicating good linearity or quadratic fit.
- Residuals are randomly distributed around zero with no systematic trends across concentration levels or measurement sequence.
- Applied drift correction strategy (IS, statistical, bracketing) reduces intensity variance between replicate standards measured at different times.
- Sample concentrations fall within the interpolation range of the calibration curve (not extrapolated far beyond standard range).
- Exported concentration predictions are in consistent tabular format with identifiable sample IDs and concentration units matching the standard reference data.

## Limitations

- QuantyFey standalone version is compatible with Windows operating systems only; Linux users must use the Apptainer version, and macOS setup is slow and difficult.
- The tool does not provide raw mass spectrometry data integration; it accepts pre-extracted intensity data and operates as a post-acquisition quantification module.
- Automatic model optimization selects between linear and quadratic models only; more complex non-linear models require manual parameter adjustment.
- Bracketing and weighted bracketing strategies assume calibration standards are interspersed regularly throughout the measurement sequence; performance degrades if standards are clustered.
- No changelog is available, limiting transparency on version differences and potential bug fixes.

## Evidence

- [other] Fit a calibration model (linear or non-linear regression) relating intensity to concentration using the standards.: "Fit a calibration model (linear or non-linear regression) relating intensity to concentration using the standards."
- [other] Load standard compound MS intensity measurements and their known concentrations.: "Load standard compound MS intensity measurements and their known concentrations."
- [other] Apply the fitted calibration model to convert sample intensities into predicted concentrations.: "Apply the fitted calibration model to convert sample intensities into predicted concentrations."
- [readme] It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies"
- [readme] Interactive Regression Model Optimization - manual adjustment of model, weights, standard levels etc.: "Interactive Regression Model Optimization - manual adjustment of model, weights, standard levels etc."
- [readme] automatic selection of linear or quadratic regression model, and selection of appropriate standards: "automatic selection of linear or quadratic regression model, and selection of appropriate standards"
- [readme] Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification, Weighted Bracketing: "Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification, Weighted Bracketing"
