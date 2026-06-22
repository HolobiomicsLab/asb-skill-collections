---
name: ft-icr-spectrum-recalibration-validation
description: 'Use when after applying mass calibration functions (LedFord, linear, or quadratic equations) to an FT-ICR transient or magnitude-mode dataset, before running SearchMolecularFormulas. Specifically, validate recalibration when: (1) comparing recalibrated spectra against reference calibration files (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - CoreMS
  - pandas
  - numpy
  - Bruker Solarix (ReadBrukerSolarix)
  - matplotlib
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.'
- import pandas as pd
- import numpy as np
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

# FT-ICR Spectrum Recalibration Validation

## Summary

Validates the quality and accuracy of mass calibration in recalibrated FT-ICR mass spectra by assessing mass error distributions, resolving power, and peak assignment consistency across a 12 T field-strength instrument. This skill ensures that downstream molecular formula assignment relies on reliable m/z measurements within acceptable ppm error tolerances.

## When to use

After applying mass calibration functions (LedFord, linear, or quadratic equations) to an FT-ICR transient or magnitude-mode dataset, before running SearchMolecularFormulas. Specifically, validate recalibration when: (1) comparing recalibrated spectra against reference calibration files (e.g., SRFA.ref), (2) transitioning between different calibration equations or calibration signal-to-noise thresholds, or (3) processing data from a new instrument configuration or magnetic field strength.

## When NOT to use

- Input data are already centroided (peak-picked) or in profile mode without access to raw transient — recalibration requires raw time-domain or magnitude-mode data.
- No reference calibration file is available and the goal is absolute mass assignment rather than relative accuracy validation.
- Spectrum is from a low-resolution instrument (e.g., nominal mass accuracy) where ppm error tolerances and resolving power calculations are not applicable.

## Inputs

- Bruker .d directory (recalibrated FT-ICR transient or magnitude-mode spectrum)
- Reference calibration file (.ref format, e.g., SRFA.ref)
- MSParameters object (noise_threshold_method, noise_threshold_min_relative_abundance, peak_min_prominence_percent)

## Outputs

- Validated mass error distribution (ppm error per peak across m/z range)
- Experimental resolving power estimate (m/Δm FWHM)
- Peak assignment quality report (number of peaks with acceptable ppm error, outliers flagged)
- Calibration fit diagnostic metrics (residuals, fit quality indicator)

## How to apply

Load the recalibrated FT-ICR mass spectrum (Bruker .d format) and reference calibration file using CoreMS ReadBrukerSolarix. Calculate experimental resolving power by measuring peak width at half-maximum intensity. Compare observed m/z values against the reference calibration using a mass error metric (ppm error = [(observed m/z − theoretical m/z) / theoretical m/z] × 10⁶). Inspect the mass error distribution across the m/z range to identify systematic drift or outliers; acceptable calibration typically exhibits ppm errors within ±2 ppm for high-resolution FT-ICR. Verify peak prominence thresholds and noise thresholding method settings (e.g., relative_abundance or log mode) are appropriate for the signal-to-noise ratio of the dataset. If mass errors exceed acceptable bounds or resolving power is degraded, re-run calibration with adjusted parameters (e.g., LedFort equation coefficients, number of calibrant peaks) and re-validate.

## Related tools

- **CoreMS** (Mass spectrum I/O, calibration function implementation, resolving power calculation, and mass error metric computation) — https://github.com/EMSL-Computing/CoreMS
- **Bruker Solarix (ReadBrukerSolarix)** (Import and parse Bruker .d format FT-ICR transient or CompassXtract data) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Tabular storage and statistical analysis of mass error distributions and peak metrics)
- **numpy** (Numerical computation of ppm error, resolving power, and signal-to-noise ratios)
- **matplotlib** (Visualization of mass error distribution plots and resolving power vs. m/z trends)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix; ms = ReadBrukerSolarix('tests/tests_data/ftms/ESI_NEG_SRFA.d'); ms.calibrate(ref_file='tests/tests_data/ftms/SRFA.ref'); print(f'Mass error (ppm): {ms.mass_error_ppm.mean():.2f}±{ms.mass_error_ppm.std():.2f}'); print(f'Resolving power: {ms.resolving_power_FWHM()}')
```

## Evaluation signals

- Mass error distribution mean and standard deviation are within specification (±2 ppm or better for 12 T FT-ICR); no systematic m/z drift across the analyzed m/z range.
- Experimental resolving power meets or exceeds theoretical expectation based on ICR transient time and magnetic field strength; peak widths are consistent with the selected noise thresholding method.
- Peak prominence and signal-to-noise ratio thresholds (e.g., peak_min_prominence_percent = 1, noise_threshold_min_relative_abundance = 1) recover expected peaks without excessive false positives or negatives compared to reference spectrum.
- Calibration fit residuals (observed − predicted m/z) show no systematic polynomial structure; if a higher-order equation was used, it should not overfit.
- Recalibrated spectrum and reference calibration file align within acceptable tolerance; m/z mismatches for known reference peaks (e.g., SRFA homologue series) are < 2 ppm.

## Limitations

- Recalibration validation assumes availability of a high-quality reference calibration file or set of calibrant peaks; accuracy is limited if reference data are noisy or incomplete.
- Resolving power estimates depend on accurate peak-picking and apex quadratic fitting; poor peak picking or low signal-to-noise regions may yield inflated or deflated resolving power values.
- Mass error tolerances (ppm thresholds) are instrument-dependent and may vary with magnetic field strength, transient duration, and sample composition; the ±2 ppm threshold is representative for 12 T but may not generalize to other configurations.
- Systematic calibration drift caused by temperature fluctuations, instrumental aging, or sample-dependent space-charge effects may not be fully captured by a global polynomial calibration function.
- No changelog is available in the CoreMS repository; version-to-version changes in calibration algorithms or mass error calculation methods are not explicitly documented, limiting reproducibility across CoreMS versions.

## Evidence

- [other] How does SearchMolecularFormulas assign molecular formulas to detected peaks in a recalibrated FT-ICR mass spectrum using 12 T field-strength parameters?: "research_question: How does SearchMolecularFormulas assign molecular formulas to detected peaks in a recalibrated FT-ICR mass spectrum using 12 T field-strength parameters?"
- [other] Perform mass calibration with calibration functions (LedFord, linear, quadratic equations) and experimental resolving power calculation.: "Workflow: 3. Perform mass calibration"
- [other] SearchMolecularFormulas configures molecular search settings including mass error tolerance (min/max ppm error), element atom constraints, ionization mode, and calibration signal-to-noise threshold.: "SearchMolecularFormulas operates by configuring molecular search settings including mass error tolerance (min/max ppm error), element atom constraints (C, H, O, N, S), ionization mode (protonated,"
- [readme] CoreMS supports FT magnitude mode and provides frequency and m/z domain calibration functions.: "Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation"
- [readme] Experimental resolving power is calculated; peak picking uses apex quadratic fitting.: "Peak picking using apex quadratic fitting, Experimental resolving power calculation"
- [other] Noise thresholding methods include relative_abundance and log modes with configurable thresholds.: "noise_threshold_method = 'relative_abundance' or 'log'; MSParameters.mass_spectrum.noise_threshold_min_relative_abundance = 1; MSParameters.ms_peak.peak_min_prominence_percent = 1"
- [readme] Bruker Solarix transients support FT magnitude mode only in CoreMS input formats.: "Bruker Solarix transients, ser and fid (FT magnitude mode only)"
- [readme] CoreMS data structures are designed with intuitive mass-spectrometric hierarchical structure for organized access to data and calculations.: "The data structures were designed with an intuitive, mass spectrometric hierarchical structure, thus allowing organized and easy access to the data and calculations."
