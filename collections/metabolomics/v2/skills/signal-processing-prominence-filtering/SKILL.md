---
name: signal-processing-prominence-filtering
description: Use when when you have a 1D intensity array from a mass spectrum (m/z
  or retention time dimension) and need to identify and rank local maxima that are
  biochemically meaningful rather than noise-driven.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - scipy
  - numpy
  - scipy.signal.find_peaks
  - mzapy.peaks.find_peaks_1d_localmax
  - h5py
  techniques:
  - mass-spectrometry
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Signal Processing Prominence Filtering

## Summary

Filter and rank peaks in 1D mass spectrometry signals by their prominence—a measure of how much a peak stands out relative to surrounding baseline and neighboring peaks. This skill is essential for distinguishing true signal peaks from noise in intensity arrays extracted from unprocessed MS data.

## When to use

When you have a 1D intensity array from a mass spectrum (m/z or retention time dimension) and need to identify and rank local maxima that are biochemically meaningful rather than noise-driven. Use this skill when threshold-based filtering alone is insufficient—for example, when working with heterogeneous MS data from orthogonal separations (LC-IM-MS) where signal-to-noise varies across the spectrum.

## When NOT to use

- Input intensity array is already filtered or denoised via other methods (e.g., median filtering, wavelet denoising)—applying prominence filtering may over-suppress weak but genuine peaks.
- Peak widths vary so dramatically that a single prominence threshold cannot accommodate both narrow and broad peaks; consider using alternative peak-finding strategies (e.g., find_peaks_1d_gauss) or adaptive prominence windows.
- The 1D signal is severely saturated or clipped; prominence calculation assumes a continuous baseline, which breaks down when many peaks reach maximum detector capacity.

## Inputs

- 1D intensity array (numpy array or list of float values)
- Height threshold parameter (minimum intensity, units depend on instrument)
- Prominence parameter (vertical distance units, same scale as intensity)
- Optional: ground-truth peak locations for validation

## Outputs

- Peak indices (positions in the 1D array)
- Peak heights (intensity values at detected peaks)
- Prominence values (height above neighboring baseline)
- Optionally: m/z or retention time values corresponding to peak indices

## How to apply

Load or generate a 1D intensity array (e.g., from an extracted ion chromatogram or MS1 spectrum stored in MZA HDF5 format). Call scipy.signal.find_peaks on the intensity array, specifying both a height threshold (minimum intensity) and a prominence parameter (the vertical distance a peak must rise above surrounding baseline). Extract the peak indices from the output, along with prominence values computed by scipy. Rank peaks by prominence to prioritize high-confidence detections. Validate the result by comparing detected peak count, positions, and heights against synthetic or known ground-truth peaks to ensure the parameter choices effectively separate signal from noise at your instrument's sensitivity.

## Related tools

- **scipy.signal.find_peaks** (Core function that performs 1D peak detection, computes prominence for each local maximum, and returns peak indices and attributes) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **mzapy.peaks.find_peaks_1d_localmax** (Wrapper function in mzapy that applies scipy.signal.find_peaks to mass spectrometry intensity arrays with domain-specific parameter defaults and returns structured output compatible with MZA workflows) — https://github.com/PNNL-m-q/mzapy
- **h5py** (Loads 1D intensity arrays from MZA HDF5 files (Arrays_intensity group) for prominence-based peak filtering) — https://github.com/h5py/h5py
- **numpy** (Array manipulation and indexing of peak indices and prominence values during extraction and validation) — https://numpy.org/

## Examples

```
from scipy.signal import find_peaks; import h5py; f = h5py.File('example.mza', 'r'); intensity = f['Arrays_intensity/630'][()]; peaks, props = find_peaks(intensity, height=20, prominence=10); mz = f['Arrays_mz/630'][()]; print(f'Detected {len(peaks)} peaks at m/z: {mz[peaks]}')
```

## Evaluation signals

- Detected peak count matches expected number from ground-truth synthetic peaks or published standards within ±10% tolerance.
- Peak positions (indices or m/z/RT coordinates) align with ground truth within instrument resolution (e.g., ±5 ppm for m/z).
- Prominence values decrease monotonically when peaks are sorted by rank; no negative or zero prominences are returned.
- False-positive rate (noise peaks detected above prominence threshold) remains below domain-specific acceptable level, validated by visual inspection or known-negative control spectra.
- Parameter sensitivity: small perturbations to prominence and height thresholds produce stable peak rankings; dramatic changes in peak count indicate parameters are near a decision boundary and may require refinement.

## Limitations

- Prominence calculation assumes a continuous or piecewise-continuous baseline; in spectra with sharp cliffs, saturation, or extreme dynamic range (>1000:1), baseline estimation may fail.
- Single global prominence threshold cannot accommodate peaks with fundamentally different widths; narrow peaks in high-noise regions may be missed while broad peaks in low-noise regions are over-detected.
- The method is sensitive to preprocessing choices (e.g., smoothing kernel size, despiking, baseline subtraction) applied before prominence filtering; different preprocessing pipelines on the same raw data may yield different results.
- In multidimensional MS workflows (LC-IM-MS) with heterogeneous retention time or arrival time distributions, prominence filtering applied independently to each 1D slice may miss weak features that become visible only after 2D or 3D integration.

## Evidence

- [other] mzapy.peaks.find_peaks_1d_localmax is one of two functions provided for performing peak fitting on 1-dimensional data.: "mzapy.peaks.find_peaks_1d_localmax is one of two functions provided for performing peak fitting on 1-dimensional data."
- [other] Call scipy.signal.find_peaks on the intensity array with appropriate threshold and prominence parameters to identify local maxima.: "Call scipy.signal.find_peaks on the intensity array with appropriate threshold and prominence parameters to identify local maxima."
- [other] Extract peak indices, heights, and prominence values from the scipy output.: "Extract peak indices, heights, and prominence values from the scipy output."
- [other] Validate output against known synthetic peaks by comparing detected peak count and positions to ground truth.: "Validate output against known synthetic peaks by comparing detected peak count and positions to ground truth."
- [intro] A Python package that provides an interface to unprocessed MS data in the MZA format.: "A Python package that provides an interface to unprocessed MS data in the MZA format."
- [readme] scipy.signal provides peak detection routines (find_peaks) with prominence-based filtering.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group"
