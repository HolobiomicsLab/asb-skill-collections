---
name: collision-cross-section-calibration-ccs
description: Use when when you have acquired ion mobility–mass spectrometry data (drift time and m/z dimensions) and need to convert observed drift times into calibrated CCS values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DEIMoS
  - conda
  - pip
  - Python
  - numpy
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool
- import deimos
- Use conda to create a virtual environment with required dependencies.
- 'Install DEIMoS using pip: pip install -e .'
- is a Python application programming interface and command-line tool
- import numpy as np
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos
schema_version: 0.2.0
---

# collision-cross-section-calibration-ccs

## Summary

Calibrate ion collision cross section (CCS) values from drift-time and m/z measurements using a polynomial model fitted to tune mix reference data. This skill establishes the quantitative m/z–drift-time–CCS relationship required to convert drift times into absolute CCS values for downstream feature characterization.

## When to use

When you have acquired ion mobility–mass spectrometry data (drift time and m/z dimensions) and need to convert observed drift times into calibrated CCS values. Apply this skill at the beginning of a multi-dimensional MS workflow, immediately after peak detection and before feature alignment, using publicly available tune mix reference standards (e.g., Agilent tune mix) acquired in the same ion mode and on the same instrument to establish instrument-specific calibration coefficients.

## When NOT to use

- When tune mix calibrant data is not available or was acquired on a different instrument or ion mode
- When drift time dimension is absent from the MS data (calibration is specific to ion-mobility-equipped instruments)
- When the tune mix calibration yields R-squared < 0.99997, indicating inadequate model fit and potential instrument drift or data quality issues

## Inputs

- tune mix reference data (HDF5 format with ms1 key containing drift time, m/z, and intensity)
- known CCS values for tune mix reference compounds
- experimental MS data (drift_time, mz, retention_time, intensity columns)

## Outputs

- fitted calibration model object (ccs_cal) with polynomial coefficients
- R-squared metric quantifying model fit quality
- calibrated feature table with CCS column populated from drift time via the fitted model

## How to apply

Load tune mix reference data in positive or negative ion mode using deimos.load(), specifying the HDF5 file containing known CCS reference compounds and their corresponding drift times and m/z values. Initialize a DEIMoS calibration object with the loaded tunemix data and known CCS values, then fit a polynomial calibration model using calibration.fit() to establish the functional m/z–drift-time–CCS mapping. Extract the R-squared metric from the fitted model (ccs_cal.fit['r'] ** 2) and verify it meets or exceeds 0.99997, indicating excellent model fit. Apply the calibrated model to all experimental MS data in the same ion mode by transforming each observed drift time into a CCS value using the established polynomial coefficients. Perform separate calibrations for positive and negative ion modes, as the m/z–drift-time–CCS relationship differs between ion polarities.

## Related tools

- **DEIMoS** (calibration API and command-line tool for fitting polynomial CCS models to tune mix data) — https://github.com/pnnl/deimos
- **Python** (runtime environment for executing deimos.load() and calibration.fit() routines)
- **numpy** (numerical computation library underlying polynomial fitting and matrix operations)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1'); ccs_cal_pos = deimos.calibrate.CCSCalibration(tune_pos); ccs_cal_pos.fit(); print('r-squared:\t', ccs_cal_pos.fit['r'] ** 2)
```

## Evaluation signals

- R-squared value of fitted calibration model ≥ 0.99997 for both positive and negative ion modes
- Calibration coefficients are reproducible and stable when refitted on the same tune mix data
- All experimental features in the output HDF5 table have non-null CCS values within physically plausible range (typically 50–300 Ų for peptides/metabolites)
- Residual plot of observed vs. predicted CCS shows random scatter with no systematic bias across the m/z–drift-time space
- Cross-validation or replicate tune mix measurements yield calibration R-squared values within ≤ 0.00001 of each other

## Limitations

- Calibration is specific to the instrument, ion source, and ion mode used during tune mix acquisition; transfer to different hardware or polarity requires new reference measurements.
- Polynomial model assumes a smooth, monotonic m/z–drift-time–CCS relationship; nonlinear instrumental responses or compound-dependent deviations may reduce accuracy.
- Tune mix must contain structurally diverse compounds spanning the m/z and drift-time ranges of experimental samples to ensure extrapolation reliability.
- Instrument drift, detector sensitivity loss, or contamination over time can degrade calibration quality; periodic re-calibration with fresh tune mix is recommended for long-term studies.

## Evidence

- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [results] DEIMoS tunemix calibration routine applied to positive ion mode tune mix data yields R-squared = 0.9999784552958121, and to negative ion mode yields R-squared = 0.9999784552958134, both exceeding the 0.99997 threshold.: "DEIMoS tunemix calibration routine applied to positive ion mode tune mix data yields R-squared = 0.9999784552958121, and to negative ion mode yields R-squared = 0.9999784552958134, both exceeding the"
- [other] Initialize a DEIMoS calibration object with the loaded tunemix data, specifying known CCS values and m/z-to-CCS mapping. Fit a polynomial calibration model to the tunemix data using the calibration.fit() method to establish the m/z–drift-time–CCS relationship.: "Initialize a DEIMoS calibration object with the loaded tunemix data, specifying known CCS values and m/z-to-CCS mapping. Fit a polynomial calibration model to the tunemix data using the"
- [other] Extract and record the R-squared value from the fitted model (ccs_cal.fit['r'] ** 2) to verify it meets the threshold of ≥0.99997. Repeat steps 1–4 for negative ion mode using the corresponding tunemix reference data.: "Extract and record the R-squared value from the fitted model (ccs_cal.fit['r'] ** 2) to verify it meets the threshold of ≥0.99997. Repeat steps 1–4 for negative ion mode using the corresponding"
- [other] Load tunemix reference data for positive ion mode using deimos.load() specifying the example_tune_pos.h5 file and ms1 key.: "Load tunemix reference data for positive ion mode using deimos.load() specifying the example_tune_pos.h5 file and ms1 key."
