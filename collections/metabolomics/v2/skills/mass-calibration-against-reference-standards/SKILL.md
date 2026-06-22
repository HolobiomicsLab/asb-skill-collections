---
name: mass-calibration-against-reference-standards
description: Use when when processing raw FT-ICR transient data (e.g., ESI_NEG_SRFA.d) that requires assignment of molecular formulas to experimental m/z peaks. Calibration is necessary before SearchMolecularFormulas because uncalibrated mass error will cause false formula rejections or incorrect assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-calibration-against-reference-standards

## Summary

Perform m/z domain calibration of FT-ICR mass spectra using a reference standard file to correct instrumental mass deviations before molecular formula assignment. This calibration step is essential for achieving accurate mass error metrics and reliable formula annotation in high-resolution mass spectrometry workflows.

## When to use

When processing raw FT-ICR transient data (e.g., ESI_NEG_SRFA.d) that requires assignment of molecular formulas to experimental m/z peaks. Calibration is necessary before SearchMolecularFormulas because uncalibrated mass error will cause false formula rejections or incorrect assignments. Apply this skill when you have both raw transient data and a reference standard file (e.g., SRFA.ref) containing known calibration masses.

## When NOT to use

- Input spectrum is already in centroid mode from vendor software and pre-calibrated — recalibration may introduce artifacts if reference standards are not representative of the actual sample mass range.
- Reference standard file is missing, corrupted, or contains fewer than 3–5 calibration points — calibration quality will degrade and mass error estimates become unreliable.
- Working with GC-MS or LC-MS data that use different calibration strategies (retention index calibration or external lock-mass correction) — FT-ICR m/z domain calibration is specific to Fourier-transform instruments.

## Inputs

- Processed FT-MS spectrum (magnitude-mode, after apodization, zero-fill, and noise thresholding)
- Reference standard file (.ref format, e.g., SRFA.ref) containing known calibration masses and their theoretical m/z values

## Outputs

- Calibrated m/z values for all detected peaks
- Calibration coefficients (linear, quadratic, or Ledford equation parameters)
- Mass error metric (in ppm) for each peak relative to theoretical m/z

## How to apply

After apodization, zero-fill, and magnitude-mode Fourier transformation, and following noise thresholding to remove low-intensity peaks, apply MzDomainCalibration by loading both the processed mass spectrum and the reference standard file. The calibration algorithm uses the reference masses to fit a correction function (e.g., linear or quadratic equations as documented in CoreMS) that maps observed m/z values to corrected m/z values. Execute the calibration before the SearchMolecularFormulas step so that the mass error calculation during formula matching uses corrected m/z values, ensuring mass error stays within acceptable thresholds (typically <2 ppm for high-resolution FT-ICR). The calibration coefficients and applied correction are retained as metadata for downstream reporting and quality control.

## Related tools

- **CoreMS** (Provides MzDomainCalibration class and mass spectrometry data structures (MSParameters, mass spectrum objects) for calibration execution and parameter configuration) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Data handling and export of calibrated m/z values and mass error metrics to CSV or other tabular formats for downstream analysis)
- **numpy** (Numerical computation of calibration curve fitting (linear, quadratic, Ledford equation) and mass error calculations)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; from corems.data_source.factory import MSFileFactory; ms = MSFileFactory('ESI_NEG_SRFA.d').get_data_from_file()[0]; ms.calibrate_mass_axis('tests/tests_data/ftms/SRFA.ref'); ms.molecular_search_settings.min_ppm_error = -2; ms.molecular_search_settings.max_ppm_error = 2
```

## Evaluation signals

- Mass error (in ppm) for calibration reference peaks should be ≤ 0.5 ppm (i.e., calibration residuals are minimal).
- Calibrated m/z values should monotonically increase with peak index; no reversals or discontinuities in m/z ordering indicate proper calibration fit.
- Post-calibration mass error distribution for assigned molecular formulas should be centered near zero with standard deviation < 2 ppm for high-resolution FT-ICR data.
- Calibration coefficients should be physically plausible (e.g., linear slope near 1.0, intercept near 0 for well-tuned instruments) and reproducible across repeated processing runs with the same reference file.
- Number of unambiguous formula assignments should increase post-calibration compared to uncalibrated data, indicating that mass error tolerance windows now correctly match true peak masses.

## Limitations

- Calibration accuracy is limited by the quality, coverage, and representativeness of the reference standard file — if reference masses do not span the full m/z range of the sample, edge regions may have higher residual error.
- Ledford, linear, and quadratic calibration models assume a fixed functional form; real instrumental mass deviation may be nonlinear over very wide m/z ranges, requiring piecewise or higher-order corrections not captured by standard CoreMS functions.
- Calibration does not correct for mass shift due to space-charge effects in high-abundance samples; such effects are dynamic and require real-time calibration or post-hoc drift modeling.
- If the reference standard file contains incorrect or outdated theoretical m/z values, calibration will propagate that error to all subsequent formula assignments.

## Evidence

- [other] Perform mass-domain calibration using MzDomainCalibration against SRFA.ref reference data: "Perform mass-domain calibration using MzDomainCalibration against SRFA.ref reference data"
- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions:
- LedFord equation
- Linear equation
- Quadratic equation"
- [other] The pipeline executes complete molecular formula assignment by applying Hanning apodization with zero-fill, noise thresholding, MzDomainCalibration against SRFA.ref reference data, and SearchMolecularFormulas: "The pipeline executes complete molecular formula assignment by applying Hanning apodization with zero-fill, noise thresholding, MzDomainCalibration against SRFA.ref reference data, and"
- [readme] CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis: "CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis."
