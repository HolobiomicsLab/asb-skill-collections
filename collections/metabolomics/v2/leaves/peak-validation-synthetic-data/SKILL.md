---
name: peak-validation-synthetic-data
description: Use when after running a 1D peak detection function (e.g., mzapy.peaks.find_peaks_1d_localmax
  or mzapy.peaks.find_peaks_1d_gauss) on synthetic mass spectra with known peak locations
  and heights.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - scipy
  - numpy
  - scipy.signal.find_peaks
  - mzapy.peaks.find_peaks_1d_localmax
  - mzapy.peaks.find_peaks_1d_gauss
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

# Validate peak detection against synthetic ground truth

## Summary

Assess the accuracy of 1D peak detection algorithms by comparing detected peaks (count, m/z positions, intensities) against known synthetic peaks generated from a controlled mass spectrum. This validation step ensures peak-finding parameters (threshold, prominence) are appropriately tuned before application to real MS data.

## When to use

After running a 1D peak detection function (e.g., mzapy.peaks.find_peaks_1d_localmax or mzapy.peaks.find_peaks_1d_gauss) on synthetic mass spectra with known peak locations and heights. Use this skill when developing or tuning peak detection workflows, or when validating that parameter choices (e.g., scipy.signal.find_peaks threshold and prominence settings) correctly recover expected peaks from controlled inputs.

## When NOT to use

- Input is real MS data without annotated or independently verified ground truth; use orthogonal methods (e.g., known standards, isotope patterns) to establish truth instead.
- Peak detection has already been validated against independent reference data; re-validation on synthetic data adds no new information.
- The goal is exploratory peak discovery on real data where ground truth is unknown; use unsupervised metrics (e.g., signal-to-noise ratio, peak width consistency) instead.

## Inputs

- Synthetic 1D mass spectrum (m/z array with intensity values)
- Known ground-truth peak locations (m/z values and expected heights)
- Peak detection function output (detected peak indices, heights, prominence values)

## Outputs

- Validation report with detected vs. ground-truth peak counts
- Peak-by-peak comparison table (detected m/z, intensity, expected m/z, intensity, error)
- Sensitivity and specificity metrics
- Tuned peak detection parameters (threshold, prominence) documented for reuse

## How to apply

Generate or load a synthetic 1D mass spectrum with a known set of peaks (m/z positions and intensities). Run the peak detection function on the intensity array to extract detected peak indices, heights, and prominence values. Extract the m/z coordinates corresponding to detected peak indices. Compare the detected peaks against ground truth: count the number of peaks detected and check if each falls within an acceptable tolerance (e.g., ±0.1 m/z units, or ±5% intensity error). Compute metrics such as sensitivity (fraction of true peaks detected) and specificity (fraction of detected peaks that match ground truth). Adjust threshold and prominence parameters iteratively if the detection rate falls below acceptable levels. Document the final parameter set for use on real spectra.

## Related tools

- **scipy.signal.find_peaks** (Core peak detection function called on intensity array with threshold and prominence parameters to identify local maxima) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- **mzapy.peaks.find_peaks_1d_localmax** (Wrapper function around scipy.signal.find_peaks for 1D mass spectrum peak detection, returns structured peak indices and heights) — https://github.com/PNNL-m-q/mzapy
- **mzapy.peaks.find_peaks_1d_gauss** (Alternative 1D peak detection function for comparison; can be validated alongside local-maximum approach) — https://github.com/PNNL-m-q/mzapy
- **numpy** (Array manipulation and indexing to extract m/z values from detected peak indices and compute error metrics)

## Examples

```
import numpy as np; from mzapy.peaks import find_peaks_1d_localmax; synthetic_mz = np.array([100.0, 100.5, 101.0, 101.5, 102.0]); synthetic_intensity = np.array([10, 150, 200, 150, 10]); detected_peaks_mz, heights = find_peaks_1d_localmax(synthetic_intensity, threshold=50, prominence=30); print(f"Detected: {len(detected_peaks_mz)} peaks; expected: 1 peak at m/z ~101.0")
```

## Evaluation signals

- Detected peak count matches ground truth count exactly or within ±1 peak (accounting for noise floor sensitivity)
- Each detected peak m/z position is within ±0.1 m/z or ±5% of expected m/z, whichever is more stringent for the instrument resolution
- Detected peak intensity is within ±10–20% of expected synthetic height (accounting for quantization and scipy interpolation)
- Sensitivity ≥ 95% (95% of true peaks detected) and specificity ≥ 90% (≥90% of detected peaks correspond to real peaks, not noise artifacts)
- Parameter set (threshold, prominence) is documented and reproducible; re-running on identical synthetic data yields identical results

## Limitations

- Synthetic peaks may not capture the full complexity of real MS noise, peak shapes (asymmetry, tailing), or isotope patterns; validation on real annotated spectra is recommended before deployment.
- scipy.signal.find_peaks performance depends strongly on threshold and prominence parameters, which must be tuned per instrument type and mass range; no universal parameter set is provided by the article.
- The article does not specify tolerance thresholds (e.g., acceptable m/z error, intensity error) for declaring a detected peak valid; practitioners must establish these based on instrument specifications.
- Validation on synthetic data alone does not account for coeluting peaks, low-abundance shoulders, or resolution limits that may affect real-world detection rates.

## Evidence

- [other] Two functions are provided for performing peak fitting on 1-dimensional data: mzapy.peaks.find_peaks_1d_localmax and mzapy.peaks.find_peaks_1d_gauss: "Two functions are provided for performing peak fitting on 1-dimensional data: ``mzapy.peaks.find_peaks_1d_localmax`` and ``mzapy.peaks.find_peaks_1d_gauss``"
- [other] Describes the workflow: generate/load synthetic 1D mass spectrum, call scipy.signal.find_peaks with threshold and prominence, extract peak indices and heights, return structured array, validate output against known synthetic peaks by comparing detected peak count and positions to ground truth: "1. Generate or load a synthetic 1D mass spectrum (m/z array with intensity values). 2. Call scipy.signal.find_peaks on the intensity array with appropriate threshold and prominence parameters to"
- [other] Identifies mzapy.peaks.find_peaks_1d_localmax as one of two peak fitting functions for 1D data: "mzapy.peaks.find_peaks_1d_localmax is one of two functions provided for performing peak fitting on 1-dimensional data."
- [other] Describes how scipy.signal.find_peaks is used to detect peaks via local maxima with threshold and prominence parameters: "How does mzapy.peaks.find_peaks_1d_localmax detect peaks in a 1D signal using scipy.signal.find_peaks?"
