---
name: reference-peak-matching-and-alignment
description: Use when when you have a processed mass spectrum object (e.g., from Bruker FT-ICR acquisition) and a reference peak list (e.g., SRFA.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - CoreMS
  - numpy
  - pandas
  - Bruker Solarix
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.'
- import numpy as np
- import pandas as pd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
schema_version: 0.2.0
---

# reference-peak-matching-and-alignment

## Summary

Match and align observed mass spectrum peaks against a reference peak list to establish calibration points, enabling mass recalibration via polynomial fitting. This skill is essential for high-resolution FT-ICR-MS where precise m/z assignment depends on matching experimental peaks to known standards within specified mass error tolerances.

## When to use

When you have a processed mass spectrum object (e.g., from Bruker FT-ICR acquisition) and a reference peak list (e.g., SRFA.ref standard), and you need to quantify mass calibration error, identify robust calibration points, and apply polynomial recalibration to improve m/z accuracy across the mass domain.

## When NOT to use

- Input spectrum has been recalibrated already and mass error is already within acceptable tolerance (< 1 ppm for FT-ICR).
- Reference peak list is unavailable or does not cover the m/z range of the observed spectrum.
- Spectrum has not undergone baseline correction, noise thresholding, or peak picking; recalibration requires a processed (not raw transient) spectrum object.

## Inputs

- Processed mass spectrum object (Bruker FT-ICR dataset)
- Reference peak list file (.ref format, e.g., SRFA.ref)
- Mass error tolerance bounds (ppm)
- MSParameters configuration (noise threshold, peak picking settings)

## Outputs

- Recalibrated mass spectrum object
- Calibration statistics table (RMSE, matched peak count, mass error distribution)
- Polynomial recalibration coefficients
- Calibration report (exportable as Excel, CSV, or JSON)

## How to apply

Load the processed mass spectrum object using CoreMS ReadBrukerSolarix and the reference peak list file. Initialize MzDomainCalibration with the reference peaks, specifying mass error bounds (e.g., in ppm) to define the acceptable tolerance for peak matching. Apply the calibration algorithm, which identifies calibration points by finding observed peaks within the specified error window around each reference peak. Extract calibration statistics including the number of matched calibration peaks, root-mean-square error (RMSE), and mass error distribution. The matched peaks are then used to fit a polynomial recalibration function (linear, quadratic, or higher order) to the spectrum, correcting systematic mass shifts. Verify the recalibration by confirming that post-calibration RMSE is significantly reduced and that the mass error distribution is centered near zero across the m/z domain.

## Related tools

- **CoreMS** (Provides ReadBrukerSolarix, MzDomainCalibration, and mass spectrum data structures for loading FT-ICR data and applying recalibration) — https://github.com/EMSL-Computing/CoreMS
- **Bruker Solarix** (Instrument and data format source; CompassXtract processes raw transient into mass spectrum object)
- **numpy** (Numerical array operations for polynomial fitting and mass error calculations)
- **pandas** (Tabular data manipulation and export of calibration statistics and aligned peak tables)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix
ms = ReadBrukerSolarix('tests/tests_data/ftms/ESI_NEG_SRFA.d').ms[0]
ms.calibrate(ref_file_location='tests/tests_data/ftms/SRFA.ref')
print(ms.calibration_stats)
```

## Evaluation signals

- Post-calibration RMSE is significantly lower than pre-calibration RMSE (target < 0.5 ppm for FT-ICR 15T).
- Mass error distribution is centered near zero (mean error ≈ 0 ppm) with symmetric spread after recalibration.
- Number of matched calibration peaks is > 10 and distributed across the m/z range (not clustered in one region).
- Polynomial coefficients fit the observed-vs-reference peak pairs with R² > 0.99.
- Recalibrated m/z values align to reference peaks within the specified tolerance window.

## Limitations

- Recalibration quality depends on the coverage and accuracy of the reference peak list; sparse or poorly characterized reference lists will yield fewer matched points and higher residual error.
- Mass error bounds must be set wide enough to capture true calibration peaks but narrow enough to avoid false matches; incorrect tolerance values can lead to spurious calibration.
- Polynomial order (linear, quadratic, cubic) must balance fit quality against overfitting; higher-order polynomials may capture noise rather than true instrumental drift.
- Reference peaks must be present and resolved in the observed spectrum; weak or overlapping peaks will fail to match and reduce the number of calibration points.
- Systematic biases in the reference list (e.g., misidentified peaks or database errors) will propagate into the recalibration and degrade accuracy downstream.

## Evidence

- [other] MzDomainCalibration accepts a processed mass spectrum object and a reference file path (SRFA.ref), then applies recalibration by finding calibration points within specified mass error bounds and applying polynomial recalibration to the spectrum.: "MzDomainCalibration accepts a processed mass spectrum object and a reference file path (SRFA.ref), then applies recalibration by finding calibration points within specified mass error bounds and"
- [other] Extract and report calibration statistics including mass error distribution, root-mean-square error (RMSE), and number of matched calibration peaks.: "Extract and report calibration statistics including mass error distribution, root-mean-square error (RMSE), and number of matched calibration peaks."
- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
- [readme] We'll use a Bruker FTICR-MS dataset of Suwannee River Fulvic Acid (SRFA) acquired on a 15 Tesla instrument: "We'll use a Bruker FTICR-MS dataset of Suwannee River Fulvic Acid (SRFA) acquired on a 15 Tesla instrument"
- [other] Load the processed mass spectrum object from the Bruker FT-ICR dataset (ESI_NEG_SRFA.d) using CoreMS ReadBrukerSolarix. Load the SRFA reference peak list (SRFA.ref) as the calibration standard.: "Load the processed mass spectrum object from the Bruker FT-ICR dataset (ESI_NEG_SRFA.d) using CoreMS ReadBrukerSolarix. Load the SRFA reference peak list (SRFA.ref) as the calibration standard."
