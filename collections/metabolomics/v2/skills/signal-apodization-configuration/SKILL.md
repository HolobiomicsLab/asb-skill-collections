---
name: signal-apodization-configuration
description: Use when when processing raw Bruker Solarix transient files (.d format) destined for FT-MS analysis, especially for ESI-negative or low-abundance natural organic matter samples where baseline noise and side-lobe artifacts around intense peaks degrade peak picking and formula assignment accuracy.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - numpy
  - matplotlib
  - Bruker Solarix instrument
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Signal Apodization Configuration

## Summary

Configure and apply apodization window functions (e.g., Hanning) to FT-ICR transient data prior to magnitude-mode Fourier transformation to reduce spectral artifacts and improve mass peak definition. Apodization trades resolving power for dynamic range and baseline quality.

## When to use

When processing raw Bruker Solarix transient files (.d format) destined for FT-MS analysis, especially for ESI-negative or low-abundance natural organic matter samples where baseline noise and side-lobe artifacts around intense peaks degrade peak picking and formula assignment accuracy.

## When NOT to use

- Input is already a centroided or processed mass list (.csv, .xlsx, or mzML); apodization applies only to raw transients.
- Analysis requires maximum resolving power (e.g., sub-ppm mass accuracy for ultra-high-mass lipids); Hanning apodization sacrifices ~30% resolving power.
- Transient data is already apodized by the instrument acquisition software; double-apodization will over-damp the signal.

## Inputs

- Bruker Solarix transient file (.d directory)
- Transient processing parameters object (MSParameters)
- Raw time-domain transient data (ser or fid files within .d)

## Outputs

- Apodized transient (time-domain signal after windowing)
- Mass spectrum object with detected m/z peaks and abundances
- Peak list (m/z, intensity, resolving power per peak)

## How to apply

After loading a Bruker Solarix transient (.d file) using CoreMS's ReadBrukerSolarix class, configure the transient processing parameters to select and apply a Hanning apodization window function before zero-filling and FFT. Hanning apodization suppresses spectral ringing by smoothing the transient edges, reducing side-lobe intensity at the cost of ~30% resolving power reduction. Set the apodization window parameter in the MSParameters before calling the process method to generate the magnitude-mode mass spectrum. The choice of Hanning (vs. other windows like Blackman or Kaiser) depends on the trade-off desired: Hanning offers moderate side-lobe suppression and is widely used for ESI-FT workflows. Verify output by inspecting the resulting m/z peak count, mass accuracy distribution, and visual baseline quality in matplotlib plots.

## Related tools

- **CoreMS** (Provides ReadBrukerSolarix class to load and configure transient processing with apodization window selection; MSParameters object stores and applies apodization settings during FFT pipeline.) — https://github.com/EMSL-Computing/CoreMS
- **Bruker Solarix instrument** (Source of raw transient data (.d file format); metadata includes calibration constants and acquisition parameters needed for frequency-to-m/z conversion post-FFT.)
- **numpy** (Underlying numerical library for windowing function calculation and FFT magnitude computation.)
- **matplotlib** (Visualization of apodized vs. non-apodized spectra for quality assessment and baseline inspection.)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix; lcms = ReadBrukerSolarix('ESI_NEG_SRFA.d'); lcms.apodization_method = 'Hanning'; lcms.zero_fill_factor = 1; lcms.process()
```

## Evaluation signals

- Output mass spectrum peak count and m/z range match expected analyte composition (e.g., ESI_NEG_SRFA: 10588 detected m/z peaks from m/z 155.87–999.66).
- Baseline noise floor is flat and free of significant spectral ringing artifacts around intense peaks.
- Mass accuracy (calculated m/z vs. theoretical) remains within calibration tolerance (typically <2 ppm for FT-ICR).
- Peak width (full width at half maximum) and resolving power are consistent with the known magnetic field strength (e.g., 15 Tesla) and transient collection time.
- Comparison of peak abundances before/after apodization shows expected redistribution (lower peak height, wider baseline, reduced artifacts).

## Limitations

- Hanning apodization reduces resolving power by ~30%, making it unsuitable for very high-mass or isobaric analytes requiring sub-ppm separation.
- Choice of window function (Hanning vs. Blackman vs. Kaiser) is problem-dependent and not automatically optimized; manual parameter sweep may be needed for novel sample types.
- Transient truncation or incomplete data collection will degrade apodization effectiveness; quality depends on signal-to-noise and transient length.
- Double-apodization (instrument + software) can over-suppress signal; user must verify whether the acquisition already applied windowing.

## Evidence

- [other] Using Hanning apodization with zero fill settings on ESI_NEG_SRFA.d produces a mass spectrum with 10588 detected m/z peaks spanning from m/z 155.87 to m/z 999.66.: "Using Hanning apodization with zero fill settings on ESI_NEG_SRFA.d produces a mass spectrum with 10588 detected m/z peaks spanning from m/z 155.87 to m/z 999.66."
- [other] Import the ReadBrukerSolarix class from CoreMS and load the ESI_NEG_SRFA.d transient file. Configure transient processing parameters to apply Hanning apodization window function. Process the transient data to generate the mass spectrum with averaging applied.: "Import the ReadBrukerSolarix class from CoreMS and load the ESI_NEG_SRFA.d transient file. Configure transient processing parameters to apply Hanning apodization window function. Process the"
- [readme] Apodization, Zerofilling, and Magnitude mode FT: "Apodization, Zerofilling, and Magnitude mode FT"
- [readme] from corems.transient.input.brukerSolarix import ReadBrukerSolarix: "from corems.transient.input.brukerSolarix import ReadBrukerSolarix"
- [readme] The data structures were designed with an intuitive, mass spectrometric hierarchical structure, thus allowing organized and easy access to the data and calculations.: "The data structures were designed with an intuitive, mass spectrometric hierarchical structure, thus allowing organized and easy access to the data and calculations."
