---
name: mass-error-distribution-analysis
description: Use when after applying polynomial m/z recalibration using a reference
  peak list (e.g., SRFA.ref) to an FT-ICR mass spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - numpy
  - pandas
  - matplotlib
  - Bruker Solarix
  techniques:
  - mass-spectrometry
  license_tier: restricted
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

# mass-error-distribution-analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extraction and statistical characterization of mass measurement errors across a recalibrated FT-ICR mass spectrum, including RMSE, error distribution metrics, and matched calibration peak counts. Essential for validating calibration quality and assessing measurement accuracy against reference standards.

## When to use

After applying polynomial m/z recalibration using a reference peak list (e.g., SRFA.ref) to an FT-ICR mass spectrum. Use this skill when you need to quantify how well the recalibration reduced systematic mass errors and to report confidence metrics for downstream molecular formula assignment.

## When NOT to use

- Mass spectrum has not yet been recalibrated or no calibration reference list is available—run calibration first.
- Calibration matched fewer than 3–5 reference peaks; statistics will be unreliable and should not be trusted for publication.
- Input spectrum is from an uncalibrated or linearity-poor instrument mode (e.g., magnitude-only FT without transient); error distribution will not reflect true calibration performance.

## Inputs

- MzDomainCalibration-recalibrated mass spectrum object (CoreMS MassSpectrum)
- Reference peak list file (SRFA.ref or equivalent .ref format)
- Calibration match results (matched peak indices and errors)

## Outputs

- Mass error distribution (histogram/array of ppm or Da values)
- RMSE statistic (scalar, units ppm or Da)
- Count of matched calibration peaks (integer)
- Calibration report (CSV, JSON, or pandas DataFrame with per-peak errors)
- Visualization (matplotlib figure with error histogram and statistics overlay)

## How to apply

Following MzDomainCalibration application on a Bruker Solarix transient or processed spectrum, extract the calibration statistics by computing differences between observed m/z and theoretical reference m/z for all matched calibration peaks. Calculate root-mean-square error (RMSE) across the matched set, construct a histogram or distribution plot of mass errors (typically in ppm or Da), and report the count of successfully matched calibration peaks within the specified mass error bounds (e.g., 0.5–5 ppm tolerance window). Use numpy and pandas to aggregate and visualize; confirm that RMSE is reduced relative to pre-calibration error and that the error distribution is centered near zero ppm with no systematic bias across the m/z range.

## Related tools

- **CoreMS** (Provides MassSpectrum data structure, MzDomainCalibration class, and methods to extract calibration statistics and matched peak errors) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Compute RMSE, mean, std dev, and histogram binning for error distribution)
- **pandas** (Aggregate and export calibration statistics to CSV/Excel for reporting)
- **matplotlib** (Visualize mass error distribution as histogram with RMSE and mean error annotations)
- **Bruker Solarix** (Source instrument and file format (.d transient data) for recalibration workflow)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix; from corems.mz_domain_calibration import MzDomainCalibration; ms = ReadBrukerSolarix('ESI_NEG_SRFA.d'); cal = MzDomainCalibration(ms, 'SRFA.ref'); rmse, n_matched, errors_ppm = cal.extract_calibration_statistics(); print(f'RMSE: {rmse:.3f} ppm, Matched peaks: {n_matched}')
```

## Evaluation signals

- RMSE value is lower than pre-calibration baseline error (if available); typically < 1 ppm for high-resolution FT-ICR after successful calibration.
- Mass error distribution is approximately normal (Gaussian) and centered at or very close to 0 ppm with no significant systematic offset across the m/z range.
- Number of matched calibration peaks is ≥ 5 and represents ≥ 80% of the reference peaks supplied; substantial mismatch count indicates calibration failure.
- Error histogram shows no multimodal peaks or long outlier tails beyond ±3 × RMSE; outliers suggest uncalibrated spectral features or reference list mismatch.
- Calibration report can be exported and compared against a reference report from a prior analysis or a different calibration method; statistics should be reproducible.

## Limitations

- RMSE and error distribution depend heavily on quality and accuracy of the reference peak list; if the .ref file has errors or is mismatched to the sample, reported statistics will be misleading.
- Analysis assumes matched peaks are correctly identified by the MzDomainCalibration algorithm; if calibration search parameters (e.g., mass error bounds) are too loose, false matches will inflate error distribution.
- For low-abundance spectra or high-noise conditions, the number of matched calibration peaks may be small, reducing statistical reliability; evaluation signals may be difficult to interpret.
- Mass error distribution statistics are specific to the m/z range and peak intensity distribution of the input spectrum; they do not transfer directly to other samples or ionization modes.
- The skill requires successful prior calibration; it does not detect or diagnose calibration failures—only quantifies the results of calibration already applied.

## Evidence

- [other] Extract and report calibration statistics including mass error distribution, root-mean-square error (RMSE), and number of matched calibration peaks.: "Extract and report calibration statistics including mass error distribution, root-mean-square error (RMSE), and number of matched calibration peaks."
- [other] MzDomainCalibration accepts a processed mass spectrum object and a reference file path (SRFA.ref), then applies recalibration by finding calibration points within specified mass error bounds and applying polynomial recalibration to the spectrum.: "MzDomainCalibration accepts a processed mass spectrum object and a reference file path (SRFA.ref), then applies recalibration by finding calibration points within specified mass error bounds"
- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
- [other] This workbook demonstrates how to extract peak heights ('abundance') from a mass spectrum object: "This workbook demonstrates how to extract peak heights ('abundance') from a mass spectrum object"
- [readme] from matplotlib import pyplot: "from matplotlib import pyplot"
