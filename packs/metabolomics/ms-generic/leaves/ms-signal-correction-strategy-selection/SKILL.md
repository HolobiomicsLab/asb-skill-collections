---
name: ms-signal-correction-strategy-selection
description: Use when you have loaded raw MS intensity tables into QuantyFey and observe
  or suspect intensity drift artifacts across your measurement sequence. Drift is
  especially likely in long-running targeted MS experiments where calibration curves
  or internal standards show systematic variation over time.
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
  license_tier: open
  provenance_tier: literature
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

# ms-signal-correction-strategy-selection

## Summary

Selecting and applying intensity drift correction strategies to mass spectrometry datasets to remove systematic signal artifacts and ensure accurate quantification. This skill addresses the common problem of signal intensity drifting over long measurement sequences by choosing from multiple correction methods suited to the dataset's characteristics.

## When to use

Apply this skill when you have loaded raw MS intensity tables into QuantyFey and observe or suspect intensity drift artifacts across your measurement sequence. Drift is especially likely in long-running targeted MS experiments where calibration curves or internal standards show systematic variation over time. Use this skill before proceeding to final quantification when external calibration is applied.

## When NOT to use

- Input is already a drift-corrected or preprocessed intensity table from another software pipeline
- Measurement sequence has no detectable temporal drift or shows only random noise
- Dataset lacks internal standards or calibration reference data needed for most correction strategies

## Inputs

- Raw MS intensity table (tab-separated or Excel format compatible with Shiny)
- Measurement sequence metadata (sample order, timing, calibration point positions)
- Internal standard intensities (if applying IS correction)
- Calibration curve data with known concentrations

## Outputs

- Corrected intensity table with drift artifacts removed
- Corrected intensity data in standard MS quantification format (exportable)
- Drift correction model parameters and metadata
- Visualizations showing before/after drift profiles

## How to apply

Load your raw MS intensity table into the QuantyFey Shiny application. Inspect the intensity profiles across your measurement sequence to identify drift patterns. Select one or more drift correction strategies from QuantyFey's available methods: Internal Standard (IS) correction (uses stable labeled standards to normalize signal), Drift Correction using statistical models (fits temporal trends), Custom Bracketing (assigns calibration data to predefined blocks of the sequence), or Weighted Bracketing (weights calibration curves based on sample position between calibration points). Use the Interactive Regression Model Optimization module to manually adjust model selection (linear vs. quadratic), standard levels, and weights if needed, or invoke the Automatic Optimization Module to automatically select the best linear or quadratic regression model and appropriate standards. Generate the corrected intensity table with drift artifacts removed and export in standard MS quantification format. The rationale is that different correction strategies suit different drift profiles: IS correction handles instrumental drift well; bracketing methods handle time-dependent calibration drift; statistical models capture non-linear drift.

## Related tools

- **QuantyFey** (Shiny application providing interactive selection, application, and optimization of intensity drift correction strategies for mass spectrometry data) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Corrected intensity values show reduced or eliminated temporal trend across the measurement sequence when plotted against sample order
- Internal consistency check: replicates or QC samples show smaller coefficient of variation after correction compared to before
- Regression model fit improves (R² increases, residuals are randomly distributed) after applying the selected correction strategy
- Exported corrected intensity table is in valid MS quantification format and is importable by downstream quantification software
- Visual inspection of before/after drift profiles confirms removal of systematic signal decay, rise, or curvature while preserving biological/sample variation

## Limitations

- QuantyFey standalone version is compatible with Windows operating systems only; Linux and macOS users require the Apptainer containerized version which is slower and more complex to set up on macOS
- Correction strategies assume external calibration framework; internal calibration approaches are not supported
- Automatic Optimization Module is limited to selection between linear and quadratic regression models; more complex non-parametric drift patterns may require manual Interactive Regression Model Optimization
- Strategy effectiveness depends on quality and positioning of internal standards or calibration points; sparse or poorly-distributed calibration data may degrade correction performance
- No changelog is available, limiting visibility into method refinements or known issues across versions

## Evidence

- [readme] QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data: "QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data"
- [readme] It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification"
- [readme] Drift correction methods offered include Internal Standard correction, statistical model-based Drift Correction, Custom Bracketing, and Weighted Bracketing: "commonly applied drift correction methods: Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification (Assigning calibration data to predefined"
- [readme] Interactive and Automatic Optimization capabilities for regression model selection: "Interactive Regression Model Optimization - manual adjustment of model, weights, standard levels etc. Automatic Optimization Module - automatic selection of linear or quadratic regression model"
- [other] Corrected data is exported in standard MS quantification format: "Generate corrected intensity table with drift artifacts removed. 4. Export corrected intensity data in standard MS quantification format"
- [readme] Windows-only compatibility for standalone version: "QuantyFey is compatible with Windows operating systems only"
- [readme] Apptainer version available for Linux with caveats for macOS: "The apptainer version is recommanded for running on Linux systems. For MacOS Systems, this version is generally slow and difficult to setup"
