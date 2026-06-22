---
name: mass-spectrum-averaging-and-processing
description: Use when you have loaded a Bruker Solarix transient file (.d format with .ser or .fid content) and need to generate a processed mass spectrum for peak picking and molecular formula annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - CoreMS
  - numpy
  - matplotlib
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

# mass-spectrum-averaging-and-processing

## Summary

Apply transient averaging and windowing functions (e.g., Hanning apodization) to Bruker FT-ICR raw transient data, followed by zero-filling and Fourier transformation, to produce a high-quality mass spectrum with reduced noise and improved peak definition. This skill is essential for converting raw time-domain transient data into interpretable frequency-domain mass spectra.

## When to use

You have loaded a Bruker Solarix transient file (.d format with .ser or .fid content) and need to generate a processed mass spectrum for peak picking and molecular formula annotation. Use this skill when raw transient data requires noise reduction, improved peak resolution, and frequency-domain conversion to enable downstream analysis such as Kendrick classification or molecular formulae assignment.

## When NOT to use

- Input is already a centroided mass spectrum or peak list; re-processing would introduce artifacts.
- Data originates from a vendor already providing processed spectra (e.g., Bruker CompassXtract output); re-processing raw transients is redundant.
- Transient file is corrupt or truncated; processing will fail or produce spurious peaks.

## Inputs

- Bruker Solarix transient file (.d directory with .ser or .fid files)
- MSParameters configuration object specifying apodization, zero-fill, and averaging parameters

## Outputs

- Processed mass spectrum object with detected peaks (m/z, abundance, resolving power)
- Peak list with m/z values, abundances, and associated metadata

## How to apply

Import the transient using CoreMS's ReadBrukerSolarix class and configure MSParameters to specify apodization window function (e.g., Hanning), zero-fill factor (e.g., 1), and averaging settings. Process the transient data through CoreMS's transient processing pipeline, which applies the selected apodization window, performs zero-filling, and computes the magnitude-mode Fourier transform to generate the final mass spectrum. Verify output by inspecting the resulting peak count, m/z range, and abundance distribution; peaks should span the expected m/z window (e.g., m/z 155–1000 for SRFA ESI-negative data) with noise floor clearly below the lowest detected peaks.

## Related tools

- **CoreMS** (Core framework providing ReadBrukerSolarix transient import, apodization window application, zero-filling, Fourier transform, and peak detection algorithms) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Underlying numerical library for FFT and array operations during transient processing)
- **matplotlib** (Visualization of processed mass spectrum and peak picking results)

## Examples

```
from corems.transient.input.brukerSolarix import ReadBrukerSolarix; lcms = ReadBrukerSolarix('tests/tests_data/ftms/ESI_NEG_SRFA.d'); lcms.transient_process()
```

## Evaluation signals

- Peak count matches literature or expected range for the sample (e.g., ~10,588 peaks for SRFA ESI-NEG); order-of-magnitude deviation suggests processing error or wrong parameters.
- m/z range of detected peaks spans expected molecular weight window (e.g., m/z 155–1000 for natural organic matter); gaps or truncation indicate calibration or processing failure.
- Abundance distribution shows clear separation between noise floor and detected peaks; if lowest-abundance peaks approach noise floor or peaks appear uniformly distributed, windowing or threshold parameters need adjustment.
- Resolving power values are consistent with instrument specification and transient time; resolving power should scale with transient length and magnetic field strength.
- No spurious high-abundance peaks at m/z extremes or with unrealistic isotope patterns; such artifacts indicate phase correction, zero-fill, or apodization errors.

## Limitations

- Apodization window choice (Hanning vs. others) affects peak shape and sensitivity; Hanning reduces spectral noise but may broaden peaks and reduce mass resolving power compared to other windows.
- Zero-filling factor impacts spectral appearance and computational cost; insufficient zero-fill (e.g., factor=1) may not fully resolve closely spaced peaks, while excessive zero-fill adds computational overhead without improving mass accuracy.
- Processing assumes transient data is in magnitude-mode FT format; phase-corrected or other non-magnitude representations will produce incorrect spectra.
- Noise threshold settings (relative_abundance, log, signal_noise) must be tuned per sample; inappropriate thresholds will either lose low-abundance peaks or retain excessive noise.
- Phase correction and frequency axis calibration are prerequisites; uncorrected phase errors or miscalibrated frequency offsets will distort peak positions and shapes.

## Evidence

- [other] Using Hanning apodization with zero fill settings on ESI_NEG_SRFA.d produces a mass spectrum with 10588 detected m/z peaks spanning from m/z 155.87 to m/z 999.66.: "Using Hanning apodization with zero fill settings on ESI_NEG_SRFA.d produces a mass spectrum with 10588 detected m/z peaks spanning from m/z 155.87 to m/z 999.66."
- [other] Import the ReadBrukerSolarix class from CoreMS and load the ESI_NEG_SRFA.d transient file. Configure transient processing parameters to apply Hanning apodization window function. Process the transient data to generate the mass spectrum with averaging applied.: "Import the ReadBrukerSolarix class from CoreMS and load the ESI_NEG_SRFA.d transient file. Configure transient processing parameters to apply Hanning apodization window function. Process the"
- [readme] Apodization, Zerofilling, and Magnitude mode FT: "Apodization, Zerofilling, and Magnitude mode FT"
- [readme] from corems.transient.input.brukerSolarix import ReadBrukerSolarix: "from corems.transient.input.brukerSolarix import ReadBrukerSolarix"
