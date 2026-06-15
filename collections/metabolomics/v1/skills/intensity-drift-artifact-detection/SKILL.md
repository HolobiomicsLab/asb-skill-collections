---
name: intensity-drift-artifact-detection
description: Use when processing raw MS intensity tables from long measurement sequences where you observe systematic, time-dependent changes in signal magnitude (e.g., progressive increase or decrease in peak intensity across a run).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_quantyfey
    doi: 10.1016/j.aca.2025.344571
    title: quantyfey
  dedup_kept_from: coll_quantyfey
schema_version: 0.2.0
---

# intensity-drift-artifact-detection

## Summary

Detection and correction of intensity drift artifacts in targeted mass spectrometry quantification data using statistical models and calibration-based strategies. This skill addresses systematic loss or gain of signal intensity over the course of a measurement sequence, which compromises quantification accuracy.

## When to use

Apply this skill when processing raw MS intensity tables from long measurement sequences where you observe systematic, time-dependent changes in signal magnitude (e.g., progressive increase or decrease in peak intensity across a run). Particularly critical when external calibration is used and calibration standards are distributed across the sequence rather than concentrated at the beginning or end.

## When NOT to use

- Input is already a feature table or has undergone normalization by upstream software — intensity drift correction is a preprocessing step for raw quantification data.
- Measurement sequence is very short (< 5–10 samples) or contains no repeated calibration standards; drift cannot be reliably estimated without calibration reference points distributed across the run.
- Operating environment is macOS; QuantyFey standalone version is not optimized for macOS (Apptainer version is slow and difficult to configure on this platform).

## Inputs

- raw MS intensity table (numeric matrix with m/z or compound identifiers as rows, scan/sample order as columns)
- measurement sequence metadata (sample type, calibration standard identifiers, injection order)
- internal standard peak intensities (optional, for IS-based correction)

## Outputs

- drift-corrected MS intensity table (same structure as input, with systematic drift removed)
- correction model parameters (regression coefficients, weights, model order selected)
- quality metrics (R² values, residuals, drift trajectory before/after correction)

## How to apply

Load the raw MS intensity table into QuantyFey's Shiny interface. Inspect the intensity profiles of calibration standards and quality control samples plotted against measurement order to visually confirm drift patterns. Select one or more of the available correction strategies: Internal Standard (IS) correction (normalizing to co-measured internal standards), statistical drift correction models (linear or quadratic regression), Custom Bracketing (assigning calibration data to predefined blocks of the sequence), or Weighted Bracketing (interpolating calibration curves based on sample position between flanking standards). Use the Interactive Regression Model Optimization module to manually adjust regression model order, weights, and standard levels if needed, or invoke the Automatic Optimization module to select between linear and quadratic models and appropriate standard subsets. Export the corrected intensity table in standard MS quantification format and verify that drift-induced intensity variations have been removed while preserving biological or chemical signal differences.

## Related tools

- **QuantyFey** (Interactive Shiny application for loading raw MS intensity data, selecting and applying drift correction strategies, optimizing regression models, and exporting corrected quantification tables.) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Visual inspection: drift trajectory plots of calibration standards show removal of systematic intensity trend; residuals around the fitted model are random and centered near zero.
- Quantitative: R² of the drift correction model is ≥ 0.70, indicating that the temporal intensity variation is adequately captured.
- Consistency check: corrected intensities of the same compound in replicate samples (at similar measurement times) now have comparable values, whereas uncorrected intensities differed systematically by position.
- Calibration curve quality: after drift correction, external calibration curves (intensity vs. concentration) show improved linearity and smaller prediction errors on quality control samples not used to fit the model.
- Reproducibility: re-running the same correction workflow with the same parameter choices produces identical corrected intensity values (deterministic output).

## Limitations

- Windows-only standalone version; Apptainer alternative available for Linux but not recommended for macOS due to performance and setup complexity.
- Requires calibration standards or internal standards distributed throughout the measurement sequence; sparse or single-point calibration data will not support reliable drift estimation.
- Assumes drift follows a smooth temporal trend (linear or low-order polynomial); rapid, non-monotonic intensity fluctuations due to instrument maintenance or environmental transients may not be fully corrected.
- No changelog documented in repository; version history and bug fixes not explicitly tracked, limiting reproducibility and auditing.

## Evidence

- [readme] It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies: "It is specifically designed to address **intensity drifts** in datasets, offering multiple **correction strategies**"
- [other] QuantyFey offers multiple correction strategies as a mechanism to address intensity drifts in mass spectrometry datasets: "QuantyFey offers multiple correction strategies as a mechanism to address intensity drifts in mass spectrometry datasets and ensure accurate quantification"
- [readme] Drift correction methods include Internal Standard correction, statistical drift correction models, Custom Bracketing, and Weighted Bracketing: "commonly applied **drift correction** methods: **Internal Standard (IS) correction**, **Drift Correction** using statistical models, **Custom Bracketing** Quantification, **Weighted Bracketing**"
- [readme] Interactive and automatic optimization of regression models for drift correction: "**Interactive Regression Model Optimization** - manual adjustment of model, weights, standard levels etc. **Automatic Optimization Module** - automatic selection of **linear** or **quadratic**"
- [other] Workflow loads raw MS intensity data, selects correction strategies, generates corrected table, and exports in standard format: "1. Load raw MS intensity table into QuantyFey Shiny application. 2. Select and apply one or more intensity drift correction strategies. 3. Generate corrected intensity table with drift artifacts"
