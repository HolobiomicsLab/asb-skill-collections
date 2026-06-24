---
name: mass-spectrometry-intensity-drift-correction
description: Use when mS quantification data exhibits intensity drift—a systematic
  decline or variation in detector response across the run sequence. Intensity drift
  is particularly common in long measurement sessions and compromises the accuracy
  of feature-by-sample intensity matrices.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Shiny
  - QuantyFey
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1016/j.aca.2025.344571
  title: quantyfey
evidence_spans:
- '**QuantyFey** is a Shiny application for the **visualization, analysis, and quantification**
  of **mass spectrometry (MS) data**'
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

# mass-spectrometry-intensity-drift-correction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Corrects systematic intensity drifts that accumulate during mass spectrometry runs using calibration-aware statistical methods. This skill ensures accurate quantification of targeted analytes by normalizing feature intensities across the sample sequence.

## When to use

Apply this skill when MS quantification data exhibits intensity drift—a systematic decline or variation in detector response across the run sequence. Intensity drift is particularly common in long measurement sessions and compromises the accuracy of feature-by-sample intensity matrices. Trigger conditions include: (1) visual inspection of raw MS chromatograms or intensity profiles showing temporal degradation, (2) calibration curve residuals that increase systematically with run position, or (3) quantified features with coefficient-of-variation that correlates with sample injection order.

## When NOT to use

- Input is already a pre-normalized or drift-corrected feature table from an integrated MS software pipeline; applying additional correction may introduce over-normalization artifacts.
- Measurement contains fewer than 3 calibration points per drift-correction block; statistical models require sufficient calibration density to estimate drift reliably.
- Non-targeted or untargeted MS data without external calibration; QuantyFey is designed for external-calibration workflows and cannot correct drift without known-concentration reference standards.

## Inputs

- Raw MS quantification table (feature-by-sample intensity matrix)
- Feature identifiers (compound names or mass-to-charge ratios)
- Sample metadata (injection order, sample type, calibration status)
- Calibration sample intensities and known concentrations
- Internal standard intensity data (if using IS correction)

## Outputs

- Drift-corrected intensity table (feature-by-sample matrix)
- Preserved feature identifiers and sample metadata
- Regression model parameters (linear or quadratic coefficients)
- Correction factor visualization (optional: intensity drift profile plots)

## How to apply

Load the raw MS quantification table (feature-by-sample intensity matrix with preserved feature identifiers and sample metadata) into QuantyFey. Select one of four correction strategies based on study design: Internal Standard (IS) correction if IS compounds were co-injected; Drift Correction using statistical models for parametric estimation; Custom Bracketing Quantification if calibration samples were distributed at predefined blocks in the sequence; or Weighted Bracketing if calibration curves should be weighted by sample position between calibration runs. For automated selection, use the Automatic Optimization Module to choose between linear or quadratic regression models and appropriate standard levels. Export the drift-corrected intensity table, verifying that feature identifiers and sample metadata are preserved and that intensity ranges remain plausible post-correction.

## Related tools

- **QuantyFey** (Interactive Shiny application for drift-correction strategy selection, model optimization, and export of corrected quantification tables) — https://github.com/CDLMarkus/QuantyFey

## Evaluation signals

- Corrected feature intensities no longer show statistically significant correlation with sample injection order (Spearman or Pearson r → 0; p > 0.05).
- Residuals of the fitted regression model (linear or quadratic) are randomly distributed around zero with no systematic trend across the run sequence.
- Coefficient-of-variation (CV) for replicate samples injected at different positions in the sequence decreases after correction (e.g., CV < 15% for targeted quantification).
- Feature identifiers, sample metadata, and intensity ranges are preserved in the corrected output table; no spurious negative values or out-of-range intensities post-correction.
- When available, quantified concentrations computed from drift-corrected intensities match independently verified reference values within expected analytical error (e.g., ±20% relative error).

## Limitations

- QuantyFey standalone version is compatible with Windows operating systems only; Apptainer version for Linux is available but more complex to configure; macOS users should launch via R/RStudio directly.
- Correction strategies assume that calibration samples are representative of analyte behavior across the run; if instrumental conditions shift non-linearly or analyte ionization efficiency changes unpredictably, even quadratic models may fail.
- Automatic model optimization selects between linear and quadratic regression but does not account for segmented or piecewise drift patterns; manual intervention via Interactive Regression Model Optimization is required for complex drift profiles.
- No changelog documented in the repository; version tracking and backward-compatibility guarantees are not explicit.

## Evidence

- [readme] QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data: "QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data"
- [readme] It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies: "It is specifically designed to address intensity drifts in datasets, offering multiple correction strategies to ensure accurate quantification"
- [other] Load the raw MS quantification table into QuantyFey, select and apply drift-correction strategies, export the corrected table: "Load the raw MS quantification table (feature-by-sample intensity matrix) into QuantyFey. 2. Select and apply one of the available drift-correction strategies to normalize intensities across the run"
- [readme] QuantyFey provides Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification, and Weighted Bracketing: "commonly applied drift correction methods: Internal Standard (IS) correction, Drift Correction using statistical models, Custom Bracketing Quantification, Weighted Bracketing Weighting of calibration"
- [readme] Automatic Optimization Module selects between linear or quadratic regression models and appropriate standards: "Automatic Optimization Module - automatic selection of linear or quadratic regression model, and selection of appropriate standards"
- [readme] QuantyFey is compatible with Windows operating systems only: "QuantyFey is compatible with Windows operating systems only"
- [readme] The standalone version only works on Windows systems and the Apptainer version is recommended for Linux: "The standalone version only works on Windows systems. The apptainer version is recommanded for running on Linux systems"
