---
name: ftms-mass-calibration-workflow
description: Use when when you have a processed Bruker Solarix FT-ICR mass spectrum
  object (from ReadBrukerSolarix) and a reference peak list file (SRFA.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - CoreMS
  - numpy
  - pandas
  - Bruker Solarix
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development
  and data analysis of small molecules analysis.'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ftms-mass-calibration-workflow

## Summary

A Bruker FT-ICR mass calibration workflow that recalibrates a processed mass spectrum using MzDomainCalibration against a reference peak list (e.g., SRFA.ref), applying polynomial recalibration to correct m/z values and quantifying calibration accuracy via mass error statistics.

## When to use

When you have a processed Bruker Solarix FT-ICR mass spectrum object (from ReadBrukerSolarix) and a reference peak list file (SRFA.ref or equivalent) available, and you need to correct systematic m/z measurement errors to improve mass accuracy for molecular formula assignment or comparison against known standards.

## When NOT to use

- Reference peak list is unavailable or does not overlap with the measured m/z range (cannot establish calibration points).
- Input is uncalibrated raw transient data; apply FFT, apodization, and noise thresholding before calibration.
- Mass spectrum has already been calibrated against the same reference; re-calibration may degrade accuracy if systematic errors have been corrected.

## Inputs

- Processed mass spectrum object (CoreMS MassSpectrum from Bruker Solarix dataset)
- Reference peak list file (.ref format, e.g., SRFA.ref containing m/z and intensity pairs)
- Mass error tolerance bounds (ppm or Da) for calibration point matching
- Polynomial recalibration model selection (linear, quadratic, Ledford, or other)

## Outputs

- Recalibrated mass spectrum object (MassSpectrum with updated m/z assignments)
- Calibration report (number of matched peaks, RMSE, mass error distribution statistics)
- Exported recalibrated spectrum (optional: Excel, CSV, or CoreMS HDF5 format)

## How to apply

Load the processed mass spectrum object using CoreMS ReadBrukerSolarix from the Bruker FT-ICR dataset (.d directory). Load the reference peak list (e.g., SRFA.ref) containing known calibration standards. Initialize MzDomainCalibration with the reference peaks and apply it to the spectrum, specifying mass error bounds (tolerance window in ppm or Da) to identify valid calibration point matches. The routine applies polynomial recalibration (linear, quadratic, or Ledford equation as configured) to transform measured m/z values. Extract calibration statistics including matched calibration peak count, root-mean-square error (RMSE), and mass error distribution to validate calibration success before exporting the recalibrated spectrum.

## Related tools

- **CoreMS** (Framework providing MzDomainCalibration class, mass spectrum object model (MassSpectrum), and ReadBrukerSolarix importer for loading Bruker FT-ICR data and applying polynomial recalibration.) — https://github.com/EMSL-Computing/CoreMS
- **Bruker Solarix** (Instrument data acquisition and vendor format (.d, CompassXtract) providing raw and processed FT-ICR mass spectra.)
- **numpy** (Numerical library for polynomial fitting and mass error distribution calculations during recalibration.)
- **pandas** (Data manipulation library for organizing and exporting calibration statistics and recalibrated peak tables.)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix; ms = ReadBrukerSolarix('tests/tests_data/ftms/ESI_NEG_SRFA.d'); from corems.maldimaging.imzml.calibration import MzDomainCalibration; calib = MzDomainCalibration('tests/tests_data/ftms/SRFA.ref'); calib.calibrate(ms); print(f'Matched peaks: {calib.matched_peaks}, RMSE: {calib.rmse:.4f} ppm')
```

## Evaluation signals

- RMSE of recalibrated mass errors falls below target threshold (typically <1 ppm for FT-ICR on 15 T instruments with known standards).
- Number of matched calibration peaks is ≥ 3 and distributed across the measured m/z range (no clustering in low or high m/z region only).
- Mass error distribution (before vs. after calibration) shows reduced mean absolute deviation and narrower spread (visually or via quantile statistics).
- Recalibrated m/z values of matched peaks agree with reference within stated tolerance bounds; unmatched peaks show systematic shift consistent with polynomial correction.
- Molecular formula assignments downstream of calibration converge to fewer candidate formulas per peak due to improved mass accuracy.

## Limitations

- Calibration accuracy depends on reference peak list quality and overlap with measured spectrum m/z range; missing or misidentified reference peaks degrade recalibration.
- Polynomial recalibration model order (linear, quadratic, Ledford) choice affects accuracy and extrapolation behavior outside calibration point range; over-fitting with high-order polynomials can amplify errors.
- Mass spectrum must contain sufficient signal and low noise; very low-abundance peaks or high baseline may not be reliably matched to reference peaks.
- Requires manual specification of mass error tolerance bounds; too-tight bounds exclude valid calibration points; too-loose bounds include spurious matches.

## Evidence

- [other] MzDomainCalibration accepts a processed mass spectrum object and a reference file path (SRFA.ref), then applies recalibration by finding calibration points within specified mass error bounds and applying polynomial recalibration to the spectrum.: "MzDomainCalibration accepts a processed mass spectrum object and a reference file path (SRFA.ref), then applies recalibration by finding calibration points within specified mass error bounds and"
- [other] Load the processed mass spectrum object from the Bruker FT-ICR dataset (ESI_NEG_SRFA.d) using CoreMS ReadBrukerSolarix. Load the SRFA reference peak list (SRFA.ref) as the calibration standard. Initialize MzDomainCalibration with the reference peaks and apply calibration to the mass spectrum. Extract and report calibration statistics including mass error distribution, root-mean-square error (RMSE), and number of matched calibration peaks.: "Load the processed mass spectrum object from the Bruker FT-ICR dataset (ESI_NEG_SRFA.d) using CoreMS ReadBrukerSolarix. Load the SRFA reference peak list (SRFA.ref) as the calibration standard."
- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
- [readme] We'll use a Bruker FTICR-MS dataset of Suwannee River Fulvic Acid (SRFA) acquired on a 15 Tesla instrument: "We'll use a Bruker FTICR-MS dataset of Suwannee River Fulvic Acid (SRFA) acquired on a 15 Tesla instrument"
- [readme] CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.: "CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis."
