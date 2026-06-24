---
name: transient-window-function-application
description: Use when when processing raw FT-ICR transient files (Bruker Solarix .d
  format or equivalent) intended for high-resolution mass spectral analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - numpy
  - matplotlib
  - Bruker Solarix (instrument/software)
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development
  and data analysis of small molecules analysis.'
- import numpy as np
- from matplotlib import pyplot
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

# transient-window-function-application

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply frequency-domain apodization window functions (e.g., Hanning) to FT-ICR transient data before zero-filling and magnitude-mode Fourier transform to suppress spectral artifacts and improve mass peak quality. This preprocessing step is essential for controlling spectral resolution and dynamic range tradeoffs in high-resolution mass spectrometry.

## When to use

When processing raw FT-ICR transient files (Bruker Solarix .d format or equivalent) intended for high-resolution mass spectral analysis. Apply this skill before FFT if the goal is to reduce spectral leakage artifacts and improve peak signal-to-noise in regions with complex, overlapping peaks—particularly for complex mixtures like natural organic matter (e.g., Suwannee River Fulvic Acid) where dynamic range demands are high. Choose this skill when the instrument and acquisition parameters allow direct access to time-domain transient data rather than pre-processed magnitude spectra.

## When NOT to use

- Input is a pre-processed magnitude spectrum or centroid mass list (apodization is already applied or irrelevant).
- Data source is low-resolution (e.g., time-of-flight or orbitrap) where transient-domain processing does not apply.
- Acquisition mode is already frequency-domain (e.g., direct magnitude mode export from instrument software) rather than raw time-domain transient.

## Inputs

- Bruker Solarix transient binary file (.d directory with ser/fid data)
- Transient acquisition metadata (frequency, sampling rate, number of data points)
- Apodization window function selection (string enum: 'Hanning', 'Hamming', etc.)
- Zero-fill parameter (integer: number of zero-fill passes)

## Outputs

- Processed mass spectrum (mass-to-charge and abundance pairs, m/z range ~155–1000)
- Detected peak list with m/z and intensity values
- Peak count summary (e.g., 10,588 peaks for ESI_NEG_SRFA.d with Hanning apodization)
- Visualization (matplotlib figure of processed spectrum)

## How to apply

Import the raw transient file using CoreMS's ReadBrukerSolarix class and instantiate a mass spectrum object. Configure the MSParameters to specify the apodization window function (e.g., Hanning window). Set the zero-fill parameter (e.g., one zero fill = doubling the number of data points prior to FFT). Apply the apodization window to the time-domain transient signal before magnitude-mode FFT computation. The windowing function tapers the signal amplitude at the edges of the acquisition window to minimize spectral leakage at the cost of slight broadening of peak line widths. Averaging can be applied across multiple transients if available. Export or visualize the resulting processed mass spectrum to confirm peak detection range, count, and mass accuracy.

## Related tools

- **CoreMS** (Provides ReadBrukerSolarix class for importing transient data, transient processing pipeline (apodization, zero-fill, FFT), and mass spectrum object model for peak picking and visualization.) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Underlying numerical computation for FFT, windowing function application, and array manipulation during transient processing.)
- **matplotlib** (Visualization of processed mass spectrum for quality assessment and peak range verification.)
- **Bruker Solarix (instrument/software)** (Source instrument and associated acquisition software (CompassXtract) that generates the raw transient binary format (.d files) being processed.)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix; lcms = ReadBrukerSolarix('tests/tests_data/ftms/ESI_NEG_SRFA.d'); lcms.transient.window_function = 'Hanning'; lcms.transient.zero_fill_count = 1; spec = lcms.get_mass_spectrum(); print(f'Detected {len(spec.peaks)} peaks from m/z {spec.min_mz:.2f} to {spec.max_mz:.2f}')
```

## Evaluation signals

- Peak count and m/z range match expected profile for the sample (e.g., 10,588 peaks, m/z 155.87–999.66 for ESI_NEG_SRFA.d).
- Mass spectrum visualization shows well-resolved peaks without excessive spectral leakage artifacts or baseline distortion.
- Comparison of peak picking results (m/z, intensity, prominence) before and after apodization confirms reduction of false positives in low-abundance regions.
- Zero-fill parameter produces expected data-point density increase (e.g., 1 zero-fill = 2× original points) without introducing numerical artifacts.
- Metadata (apodization window name, zero-fill count, FFT algorithm) is correctly recorded in output for reproducibility.

## Limitations

- Apodization window choice introduces a resolution–dynamic-range tradeoff; Hanning and similar smooth windows reduce spectral leakage but broaden peak line widths compared to rectangular windows.
- Excessive zero-filling (e.g., > 3 passes) does not improve peak resolution (Rayleigh criterion is set by acquisition time, not FFT padding) and may increase computational cost.
- FT magnitude mode only; phase information is discarded, limiting advanced spectral reconstruction techniques.
- No changelog documented in the repository, so versioning and changes to apodization algorithm across CoreMS releases may not be transparently tracked.

## Evidence

- [other] Using Hanning apodization with zero fill settings on ESI_NEG_SRFA.d produces a mass spectrum with 10588 detected m/z peaks spanning from m/z 155.87 to m/z 999.66.: "Using Hanning apodization with zero fill settings on ESI_NEG_SRFA.d produces a mass spectrum with 10588 detected m/z peaks spanning from m/z 155.87 to m/z 999.66."
- [other] 1. Import and process transient data 2. Apply noise thresholding and peak picking 3. Perform mass calibration: "Import and process transient data; Apply noise thresholding and peak picking; Perform mass calibration"
- [readme] Apodization, Zerofilling, and Magnitude mode FT: "Apodization, Zerofilling, and Magnitude mode FT"
- [other] from corems.transient.input.brukerSolarix import ReadBrukerSolarix: "from corems.transient.input.brukerSolarix import ReadBrukerSolarix"
- [other] We'll use a Bruker FTICR-MS dataset of Suwannee River Fulvic Acid (SRFA) acquired on a 15 Tesla instrument: "Bruker FTICR-MS dataset of Suwannee River Fulvic Acid (SRFA) acquired on a 15 Tesla instrument"
