---
name: temporal-signal-drift-detection-and-adjustment
description: Use when raw MS quantification data (feature-by-sample intensity matrix) shows systematic variation in detector response across the run sequence—i.e., when the same analyte produces different intensities at different timepoints in the measurement despite constant sample concentration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# temporal-signal-drift-detection-and-adjustment

## Summary

Detect and correct intensity drifts that occur across the sample run sequence in mass spectrometry quantification datasets using statistical or bracketing-based correction strategies. This skill ensures accurate quantification when instrumental signal degrades or fluctuates systematically over time.

## When to use

Apply this skill when raw MS quantification data (feature-by-sample intensity matrix) shows systematic variation in detector response across the run sequence—i.e., when the same analyte produces different intensities at different timepoints in the measurement despite constant sample concentration. This is common in long acquisition runs where instrumental sensitivity drifts due to column degradation, ion source fouling, or detector aging.

## When NOT to use

- Input is already a drift-corrected or normalized intensity matrix (e.g., pre-processed by the MS instrument vendor or another tool).
- MS data lacks sufficient calibration standards distributed across the run sequence to model drift over time.
- Analysis goal is exploratory or qualitative (e.g., presence/absence detection) rather than quantitative accuracy—drift correction introduces computational overhead without benefit.

## Inputs

- raw MS quantification table (feature-by-sample intensity matrix)
- sample run-sequence metadata (acquisition order, timestamps)
- calibration standards intensities (external calibration data across the run)

## Outputs

- drift-corrected intensity table (feature-by-sample matrix with normalized intensities)
- correction metadata (applied strategy, model parameters, residuals)

## How to apply

Load the raw MS quantification table (feature-by-sample intensity matrix) into QuantyFey along with sample run-sequence metadata. Select one of the available drift-correction strategies—Internal Standard (IS) correction, statistical drift correction, custom bracketing (assigning calibration data to predefined blocks of the sequence), or weighted bracketing (weighting calibration curves by sample position between calibrations). For each feature, the selected strategy normalizes intensities across the run sequence by either scaling against an internal standard response, fitting a statistical model (linear or quadratic regression) to calibration standards over time, or interpolating calibration curves to the sample's position in the sequence. The automatic optimization module can select the appropriate regression model and standard levels; manual adjustment is available for interactive refinement. Export the drift-corrected intensity table with preserved feature identifiers and sample metadata.

## Related tools

- **QuantyFey** (Interactive Shiny application for applying multiple drift-correction strategies to MS quantification data and manually optimizing regression models) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Corrected intensities for replicate standards injected at different timepoints show reduced variation (lower coefficient of variation) compared to uncorrected data.
- Calibration curves fitted to drift-corrected data display lower residuals and higher R² values across all retention timepoints.
- Quantified analyte concentrations (from corrected intensities) match reference values or expected concentrations more closely than uncorrected results.
- Plot of corrected intensity vs. run sequence position shows no systematic trend (horizontal scatter) for standards, indicating drift removal.
- Feature identifiers, sample metadata, and run-sequence information are preserved in the output table and match the input schema.

## Limitations

- QuantyFey standalone version is compatible with Windows operating systems only; Linux and macOS require Apptainer containerization, which is slower and more complex to set up on macOS.
- Drift correction strategies assume that calibration standards are representative of the analytes and that drift is monotonic or smooth; sudden instrumental failures or non-linear instabilities may not be fully corrected.
- Weighted bracketing and custom bracketing methods require careful placement of calibration standards throughout the run; sparse or unevenly distributed standards may lead to poor interpolation.
- No changelog is available, limiting visibility into model updates or known issues across versions.

## Evidence

- [other] task workflow confirms skill application pattern: "Load the raw MS quantification table (feature-by-sample intensity matrix) into QuantyFey. Select and apply one of the available drift-correction strategies to normalize intensities across the run"
- [readme] drift correction strategies explicitly listed: "QuantyFey provides: commonly applied drift correction methods: Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification (Assigning calibration"
- [readme] purpose and design intent: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification."
- [readme] automatic and manual optimization capability: "Interactive Regression Model Optimization - manual adjustment of model, weights, standard levels etc. Automatic Optimization Module - automatic selection of linear or quadratic regression model, and"
- [readme] target use case and audience: "QuantyFey is intended for users with a basic understanding of mass spectrometry and data analysis, including: Analytical chemists conducting MS data quantification. Laboratory technicians processing"
- [readme] platform limitation: "QuantyFey is compatible with Windows operating systems only."
- [readme] macOS setup difficulty with containerization: "the apptainer setup is (more) complicated on macOS and runs not very fast. Try to avoid setting it up on macOS"
