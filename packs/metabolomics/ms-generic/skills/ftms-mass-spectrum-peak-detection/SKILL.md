---
name: ftms-mass-spectrum-peak-detection
description: Use when you have loaded an FT-ICR raw spectrum (e.g., ESI_NEG_SRFA.d in Bruker or ThermoFisher .raw format) and need to identify the m/z positions and intensities of individual mass spectral peaks.
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
  techniques:
  - mass-spectrometry
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

# FT-MS Mass Spectrum Peak Detection

## Summary

Automated identification and localization of mass spectral peaks in Fourier-transform ion cyclotron resonance (FT-ICR) mass spectrometry data using apex quadratic fitting. This skill is essential for converting raw FT-MS transients into interpretable peak lists suitable for downstream calibration and molecular formula assignment.

## When to use

Apply this skill when you have loaded an FT-ICR raw spectrum (e.g., ESI_NEG_SRFA.d in Bruker or ThermoFisher .raw format) and need to identify the m/z positions and intensities of individual mass spectral peaks. The skill is triggered after noise threshold calculation (manual or automatic) and precedes mass calibration and molecular formula search workflows.

## When NOT to use

- Input is already a centroided peak list or pre-processed mass list; peak detection has already been performed.
- The spectrum is severely baseline-corrupted or contains unresolved multiplets where quadratic fitting cannot reliably separate overlapping peaks.
- Profile-mode data from very low resolving power instruments (R < 10,000) where individual peaks are not resolved from noise.

## Inputs

- FT-ICR raw spectrum (Bruker .d transient, .ser, or .fid; ThermoFisher .raw; or other vendor format supported by CoreMS)
- Noise threshold value (scalar, automatically calculated or user-defined)
- Mass spectrum object (MassSpectrum instance from CoreMS encapsulation)

## Outputs

- Peak list (list of MassSpectrumPeak objects with m/z, intensity, resolving power, and quadratic fit parameters)
- Mass spectral peak table (pandas DataFrame or serialized output with peak metadata)

## How to apply

After loading the mass spectrum using CoreMS data encapsulation modules and applying noise threshold filtering, invoke the peak-picking algorithm with apex quadratic fitting. This method iterates through the centroided or profile-mode spectrum, identifies local maxima that exceed the noise threshold, and fits a quadratic polynomial to the apex region to refine the m/z position and intensity estimate. The quadratic fitting improves localization accuracy compared to simple centroid or maximum-intensity methods, particularly important for high-resolving-power FT-ICR data where peak shape carries mass information. The algorithm outputs a list of detected peaks with their m/z values, intensities, and estimated resolving power.

## Related tools

- **CoreMS** (Provides data encapsulation, noise thresholding, and peak-picking API (apex quadratic fitting implementation)) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Numerical computation and polynomial fitting (quadratic coefficients))
- **pandas** (Peak list serialization and tabular peak metadata export)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; from corems.data_source.raw_data import RawDataReader; spectrum = RawDataReader('tests/tests_data/ftms/ESI_NEG_SRFA.d').get_mass_spectrum(0); spectrum.peaks = spectrum.pick_peaks()
```

## Evaluation signals

- Peak count is within expected range for spectrum complexity (e.g., >50 peaks for complex natural organic matter, <20 for simple synthetic mixtures).
- Detected peak m/z values fall within the instrument's operational mass range and do not contain spurious peaks at extreme m/z or intensity values.
- Quadratic fit residuals are small (typically <1 ppm error) compared to subsequent mass calibration errors.
- Resolving power estimates from peak shape are consistent with instrument specifications (e.g., >100,000 FWHM for FT-ICR at m/z 400 in 7 Tesla field).
- Peak intensity distribution is reasonable (e.g., maximum peak intensity >>noise threshold, intensity distribution follows expected mass spectral patterns).

## Limitations

- Quadratic fitting assumes approximately symmetric peak shapes; asymmetric or tailed peaks typical of certain ion sources may have slightly degraded m/z accuracy.
- Severely overlapping or unresolved multiplets are not resolved by this algorithm; additional deconvolution workflows may be required.
- Baseline artifacts, electronic noise spikes, or contamination peaks can be mistaken for real m/z signals if noise thresholding is set too low.
- The method requires careful tuning of noise threshold; too-high thresholds miss weak peaks, too-low thresholds introduce noise peaks.

## Evidence

- [readme] Peak picking using apex quadratic fitting: "Peak picking using apex quadratic fitting"
- [other] Load the mass spectrum from ESI_NEG_SRFA.d and the reference m/z file SRFA.ref using CoreMS data encapsulation modules.: "Load the mass spectrum from ESI_NEG_SRFA.d and the reference m/z file SRFA.ref using CoreMS data encapsulation modules"
- [readme] Manual and automatic noise threshold calculation: "Manual and automatic noise threshold calculation"
- [readme] Apodization, Zerofilling, and Magnitude mode FT: "Apodization, Zerofilling, and Magnitude mode FT"
- [readme] CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis: "CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis"
