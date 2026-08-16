---
name: ion-mobility-calibration-curve-fitting
description: Use when you have TWIM-MS experimental data with arrival times and m/z
  values, and access to calibrant reference standards with known CCS values (typically
  loaded from a calibration template).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - MOCCal
  - DEIMoS
  techniques:
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moccal_cq
    doi: 10.1021/acs.analchem.3c04290
    title: moccal
  dedup_kept_from: coll_moccal_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04290
  all_source_dois:
  - 10.1021/acs.analchem.3c04290
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-mobility-calibration-curve-fitting

## Summary

Fit a regression model (linear or polynomial) to drift time vs. collision cross section (CCS) reference standards to establish a calibration curve for converting experimental TWIM-MS arrival times into calibrated CCS values. This is a core step in high-dimensional multi-omic ion mobility mass spectrometry data analysis.

## When to use

You have TWIM-MS experimental data with arrival times and m/z values, and access to calibrant reference standards with known CCS values (typically loaded from a calibration template). You need to convert raw arrival times into calibrated CCS values across the m/z range before downstream biomolecular class assignment or quantification.

## When NOT to use

- Arrival times have already been manually converted to drift times using a different method or instrument calibration—re-fitting may introduce inconsistency.
- Reference calibrant standards are unavailable, unlabeled, or have uncertain CCS values.
- The experimental m/z range extends far beyond the m/z coverage of reference standards, leading to extrapolation beyond the validated calibration domain.

## Inputs

- TWIM-MS arrival times (time at detector) and m/z values from experimental sample
- Instrument-specific time-of-flight offset parameter
- Calibrant reference standards with known CCS values
- Calibration template (data structure defining reference standards and CCS assignments)

## Outputs

- Calibration curve model (linear or polynomial regression coefficients)
- Calibrated CCS values for all ions in experimental dataset
- CCS table with m/z, charge state, drift time, and quality metrics
- Calibration quality report (e.g., residuals, R² goodness-of-fit)

## How to apply

Load calibrant reference standards with known CCS values from the calibration template. Convert experimental arrival times to drift times by subtracting the instrument-specific time-of-flight offset. Fit a linear or polynomial regression model to the calibrant reference standards, mapping drift time to CCS across the m/z range. Apply the resulting calibration function to the experimental drift times to generate calibrated CCS values for all ions. Export the calibrated CCS table with associated m/z, charge state, and quality metrics (e.g., residuals or goodness-of-fit). Validate that calibration residuals are acceptable and that the curve spans the full m/z range of experimental data.

## Related tools

- **MOCCal** (Python application that implements CCS calibration as a core workflow step, including data import, drift time conversion, calibrant loading, and calibration curve fitting for TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Dependency for MOCCal when processing raw (unprocessed) calibration files; version 1.3.2 required for RawDT workflow) — http://github.com/pnnl/deimos

## Evaluation signals

- Calibration curve residuals (difference between fitted and reference CCS values) are within acceptable bounds (typically < 2% relative error for high-quality standards).
- Goodness-of-fit metric (R² or adjusted R²) is ≥ 0.99, indicating the model explains ≥ 99% of variance in reference standards.
- Calibrated CCS values for unknown samples fall within the m/z and drift time range spanned by the reference standards (no extrapolation).
- Quality metrics (charge state, m/z assignment) are correctly propagated to output CCS table and match input experimental data.
- Calibration is reproducible: re-fitting with the same standards and parameters yields identical or near-identical CCS values (bit-identical or within floating-point tolerance).

## Limitations

- TWIM platforms record arrival time (time at detector) rather than drift time (time in TWIM cell), and the conversion requires an accurate instrument-specific time-of-flight offset; incorrect offset propagates systematic error into all calibrated CCS values.
- Linear or polynomial regression assumes a smooth, monotonic relationship between drift time and CCS; non-ideal behavior (e.g., instrument hysteresis or space-charge effects) may violate this assumption and degrade calibration accuracy at extreme m/z or CCS values.
- Reference calibrant standards must cover the m/z and CCS range of experimental data; sparse or unevenly distributed standards lead to poor fit quality or unreliable predictions in sparse regions.
- No changelog provided; version history and known issues are not documented in the repository README.

## Evidence

- [other] Convert arrival times to drift times by accounting for the time-of-flight offset specific to the instrument platform.: "Convert arrival times to drift times by accounting for the time-of-flight offset specific to the instrument platform."
- [other] Load calibrant reference standards with known CCS values from the calibration template.: "Load calibrant reference standards with known CCS values from the calibration template."
- [other] Apply linear or polynomial regression to establish a calibration curve mapping drift time to CCS across the m/z range.: "Apply linear or polynomial regression to establish a calibration curve mapping drift time to CCS across the m/z range."
- [other] Apply the calibration function to experimental arrival times to generate calibrated CCS values for all ions.: "Apply the calibration function to experimental arrival times to generate calibrated CCS values for all ions."
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [readme] Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations.: "Functionality includes collision cross section (CCS) calibration, experimental data biomolecular class assignment, and experimental class-specific CCS calculations."
