---
name: spectral-peak-detection-local-maxima
description: Use when you have a 1D intensity array (e.g., a single MS1 or MS2 spectrum extracted from an MZA HDF5 file) and need to identify prominent peaks with their m/z indices and heights.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - scipy
  - numpy
  - scipy.signal.find_peaks
  - mzapy.peaks.find_peaks_1d_localmax
  - mzapy
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.3c01653
  title: mzapy
- doi: 10.1021/acs.jproteome.2c00313
  title: ''
evidence_spans:
- Dependencies ------------------------------ * ``scipy``
- '* ``scipy``'
- '* ``numpy``'
- Dependencies ------------------------------ * ``numpy``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzapy_cq
    doi: 10.1021/acs.analchem.3c01653
    title: mzapy
  dedup_kept_from: coll_mzapy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c01653
  all_source_dois:
  - 10.1021/acs.analchem.3c01653
  - 10.1021/acs.jproteome.2c00313
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Peak Detection via Local Maxima

## Summary

Detects peaks in 1D mass spectra by identifying local maxima using scipy.signal.find_peaks with prominence and threshold parameters. This is one of two primary peak-fitting approaches in mzapy for extracting m/z positions and intensities from MS data.

## When to use

Apply this skill when you have a 1D intensity array (e.g., a single MS1 or MS2 spectrum extracted from an MZA HDF5 file) and need to identify prominent peaks with their m/z indices and heights. Use this approach when you expect well-resolved, sharply-peaked spectral features and want computational efficiency over analytical precision—it is faster and more straightforward than Gaussian fitting for exploratory peak detection or high-throughput screening.

## When NOT to use

- Input spectrum is already a peak table or feature matrix (i.e., peaks have been pre-extracted)—apply this skill on raw intensity arrays only.
- Spectrum contains heavily overlapping or unresolved peaks where sub-peak resolution is critical—consider Gaussian decomposition (find_peaks_1d_gauss) instead.
- Spectrum is very noisy with SNR < 3 and no reliable threshold exists—preprocessing (smoothing, baseline correction) should precede peak detection.

## Inputs

- 1D intensity array (numpy.ndarray, dtype float or int)
- Corresponding m/z array (numpy.ndarray, same length as intensity array)
- Threshold parameter (float, minimum intensity value for peak consideration)
- Prominence parameter (float, minimum vertical distance from baseline to peak)

## Outputs

- Peak indices (numpy.ndarray, integer indices into the input intensity array)
- Peak m/z positions (numpy.ndarray, m/z values at detected peak indices)
- Peak heights (numpy.ndarray, intensity values at peak indices)
- Peak prominence values (numpy.ndarray, vertical prominence of each peak)

## How to apply

Load or generate a 1D mass spectrum (intensity array paired with m/z values) from an MZA file using mzapy data access functions (e.g., collect_ms1_arrays_by_rt). Pass the intensity array to scipy.signal.find_peaks with tuned threshold and prominence parameters to suppress noise and select peaks matching your SNR expectations. Extract peak indices from scipy output, map indices to m/z values, and retrieve corresponding heights and prominence values. Validate by comparing detected peak count and m/z positions against known reference peaks or synthetic ground truth. Document the threshold and prominence settings used, as these directly control false positive and false negative rates.

## Related tools

- **scipy.signal.find_peaks** (Core algorithm: detects local maxima in 1D array using prominence and height filtering) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **mzapy.peaks.find_peaks_1d_localmax** (Wrapper function integrating scipy.signal.find_peaks for mass spectrometry data) — https://github.com/PNNL-m-q/mzapy
- **numpy** (Array indexing and manipulation of intensity and m/z arrays)
- **mzapy** (Data loading and extraction of 1D MS spectra from MZA HDF5 files) — https://github.com/PNNL-m-q/mzapy

## Examples

```
from mzapy.peaks import find_peaks_1d_localmax; import numpy as np; mz_vals, heights, prominences = find_peaks_1d_localmax(intensity_array, mz_array, threshold=100, prominence=50)
```

## Evaluation signals

- Detected peak count matches or is within ±10% of ground truth for synthetic/reference spectra.
- Peak m/z positions agree with known reference peaks within ±0.01 m/z (or instrument mass accuracy specification).
- No peaks detected in noise-only regions (regions below threshold or with prominence < set parameter).
- Height and prominence values are non-negative and physically consistent (height ≤ max intensity in spectrum).
- Rerunning with slightly different threshold/prominence values produces stable, reproducible peak sets (rank order preserved).

## Limitations

- Cannot resolve overlapping or co-eluting peaks; adjacent peaks closer than the prominence window will be merged or missed.
- Performance depends critically on threshold and prominence parameter tuning; no universal defaults work for all MS instruments or sample types.
- Does not account for instrumental artifacts (e.g., electronic noise, baseline drift, isotope satellites) without prior preprocessing.
- Mzapy provides find_peaks_1d_localmax for local-maximum detection but a separate Gaussian-fitting function (find_peaks_1d_gauss) is recommended for quantitative, sub-resolution peak characterization.

## Evidence

- [other] Two functions are provided for performing peak fitting on 1-dimensional data: `mzapy.peaks.find_peaks_1d_localmax` and `mzapy.peaks.find_peaks_1d_gauss`: "Two functions are provided for performing peak fitting on 1-dimensional data: ``mzapy.peaks.find_peaks_1d_localmax`` and ``mzapy.peaks.find_peaks_1d_gauss``"
- [other] Call scipy.signal.find_peaks on the intensity array with appropriate threshold and prominence parameters to identify local maxima.: "Call scipy.signal.find_peaks on the intensity array with appropriate threshold and prominence parameters to identify local maxima."
- [other] Extract peak indices, heights, and prominence values from the scipy output.: "Extract peak indices, heights, and prominence values from the scipy output."
- [other] Return a structured array or tuple containing peak locations (m/z values) and corresponding heights.: "Return a structured array or tuple containing peak locations (m/z values) and corresponding heights."
- [other] Validate output against known synthetic peaks by comparing detected peak count and positions to ground truth.: "Validate output against known synthetic peaks by comparing detected peak count and positions to ground truth."
- [other] mzapy is installable from the PyPI via `pip`: "mzapy is installable from the PyPI via `pip`"
