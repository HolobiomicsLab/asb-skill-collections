---
name: mass-spectrum-calibration-validation
description: Use when after applying frequency domain calibration (Ledford, linear,
  or quadratic equation) to a raw FT-ICR mass spectrum, validate the calibration quality
  by measuring residual mass errors across the m/z range.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  - matplotlib
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters
  import MSParameters']
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-calibration-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate calibrated mass spectra by comparing theoretical and measured m/z values across multiple calibration equations and assessing mass error distributions. This skill ensures that frequency-to-m/z domain transformations have been applied correctly before molecular formula assignment.

## When to use

After applying frequency domain calibration (Ledford, linear, or quadratic equation) to a raw FT-ICR mass spectrum, validate the calibration quality by measuring residual mass errors across the m/z range. Use this skill when preparing spectra for downstream molecular formula search, especially when first-hit or all-hits assignment modes will be compared, since poor calibration can artificially inflate or suppress assignment counts.

## When NOT to use

- Input spectrum has not yet undergone any calibration — use calibration assignment first.
- Spectrum is centroid-only without access to peak position metadata — validation requires measured vs. theoretical m/z pairs.
- Analysis goal is exploratory and tolerates large mass errors (e.g., compound class screening rather than molecular formula assignment).

## Inputs

- Processed mass spectrum (Bruker CompassXtract, Bruker transients, ThermoFisher .raw, CoreMS .hdf5)
- Calibration model parameters (Ledford, linear, or quadratic coefficients)
- Reference mass list or internal standard compounds with known accurate m/z

## Outputs

- Mass error distribution table (m/z, measured m/z, calculated m/z, error in ppm or Da, residuals)
- Summary statistics (mean, median, std, min, max of mass error)
- Calibration validation plots (mass error vs. m/z, error histogram, Q-Q plot)
- Pass/fail assessment and recommendation for recalibration if needed

## How to apply

Load the processed mass spectrum from vendor-specific formats (Bruker .d, ThermoFisher .raw, or CoreMS .hdf5) and extract both measured and theoretical m/z values. Calculate mass error (ppm or absolute m/z difference) for each detected peak using the calibration equation applied. Compute summary statistics (mean, median, standard deviation, min, max) of the mass error distribution. Generate plots (e.g., mass error vs. m/z, histogram of error distribution) to identify systematic bias or outliers. Compare error metrics against acceptance thresholds appropriate to your analysis (typically < 2–5 ppm for FT-ICR). If residual errors exceed tolerance, re-calibrate using alternative reference compounds or a different calibration model (e.g., switch from linear to quadratic) before proceeding to formula assignment.

## Related tools

- **CoreMS** (Framework for loading spectrum data, applying calibration models (Ledford, linear, quadratic equations), and computing mass error metrics) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Tabulating and summarizing mass error statistics (mean, median, std, min, max) into comparison tables)
- **numpy** (Computing mass error arrays and statistical distributions)
- **matplotlib** (Generating diagnostic plots (mass error vs. m/z, error histograms, calibration curves))

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; spectrum.calibrate(freq_shift=0); errors = [(p.mz_theor - p.mz) / p.mz * 1e6 for p in spectrum]; print(f'Mean error: {np.mean(errors):.3f} ppm, Std: {np.std(errors):.3f} ppm')
```

## Evaluation signals

- Mass error mean is centered near zero ppm and does not show systematic bias across the m/z range (slope close to 0).
- Mass error standard deviation is within specification for the instrument (typically < 2–5 ppm for FT-ICR).
- Residual mass error histogram is approximately normal-distributed, indicating random rather than systematic error.
- No outliers or anomalous peaks with error > 3σ from the mean (indicates miscalibrated peaks or contaminants).
- Recalibration with an alternative model (e.g., quadratic vs. linear) does not substantially reduce mean absolute error, confirming convergence.

## Limitations

- Calibration validation requires high-confidence reference masses; sparse or low-quality reference lists can produce unreliable error estimates.
- Mass error assessment is local to the m/z range covered by detected peaks; extrapolation beyond this range is not validated.
- Different calibration models (Ledford, linear, quadratic) may show different residual error profiles; the choice of model affects interpretation of validation results.
- The CoreMS README notes that calibration functions support frequency and m/z domain transformations but does not specify automatic model selection; users must choose the appropriate equation for their instrument and sample type.

## Evidence

- [readme] Frequency and m/z domain calibration functions: LedFord equation, Linear equation, Quadratic equation: "Frequency and m/z domain calibration functions: - LedFord equation - Linear equation - Quadratic equation"
- [other] Extract and tabulate assignment counts and score distribution statistics (mean, median, std, min, max) for each mode.: "Extract and tabulate assignment counts and score distribution statistics (mean, median, std, min, max) for each mode."
- [readme] CoreMS supports direct access for almost all vendors' data formats, allowing for the centralization and automation of all data processing workflows: "CoreMS supports direct access for almost all vendors' data formats, allowing for the centralization and automation of all data processing workflows from the raw signal to data annotation and curation."
- [other] Load the calibrated mass spectrum from ESI_NEG_SRFA.d dataset and reference file SRFA.ref.: "Load the calibrated mass spectrum from ESI_NEG_SRFA.d dataset and reference file SRFA.ref."
- [readme] High Resolution Mass Spectrum Simulations: Peak shape (Lorentz, Gaussian, Voigt, and pseudo-Voigt), Peak fitting for peak shape definition, Peak position in function of data points, signal to noise and resolving power: "High Resolution Mass Spectrum Simulations: Peak shape (Lorentz, Gaussian, Voigt, and pseudo-Voigt), Peak fitting for peak shape definition, Peak position in function of data points, signal to noise"
