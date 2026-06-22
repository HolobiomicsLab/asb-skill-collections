---
name: peak-height-threshold-selection
description: Use when when applying iterative peak detection (local-maximum or Gaussian-fit methods) to 1D extracted ion chromatograms (XICs), arrival time distributions (ATDs), or MS1 spectra from MZA-format files, and you need to decide which peaks to retain based on their intensity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - scipy
  - numpy
  - mzapy.peaks.find_peaks_1d_gauss
  - mzapy.peaks.find_peaks_1d_localmax
  - scipy.optimize.curve_fit
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

# peak-height-threshold-selection

## Summary

Selection of absolute or relative intensity thresholds to filter detected peaks in 1D mass spectrometry signals, controlling which local maxima or fitted Gaussian peaks are retained as valid analyte features. This is a critical preprocessing decision that balances signal recovery against noise rejection in iterative peak-fitting workflows.

## When to use

When applying iterative peak detection (local-maximum or Gaussian-fit methods) to 1D extracted ion chromatograms (XICs), arrival time distributions (ATDs), or MS1 spectra from MZA-format files, and you need to decide which peaks to retain based on their intensity. Use this skill when the raw signal contains both genuine analyte peaks and background noise, and you must establish a stopping criterion for iterative fitting or a minimum feature height to report.

## When NOT to use

- Input is already a feature table or quantification matrix (threshold has already been applied upstream).
- Signal contains only noise or is uniformly flat (no peaks will survive any reasonable threshold; diagnostic should precede thresholding).
- Threshold selection is part of a supervised classification or machine-learning pipeline where threshold should be tuned by cross-validation rather than set manually (use parameter-search skill instead).

## Inputs

- 1D signal array (XIC, ATD, or MS1 spectrum from MZA file)
- Peak detection method (local-maximum or Gaussian-fit)
- Candidate absolute or relative intensity threshold value

## Outputs

- Set of detected peaks meeting threshold criterion
- Peak parameters: position, height, width (for Gaussian fits)
- Residual signal after peak subtraction

## How to apply

Set either an absolute intensity threshold (minimum peak height in intensity units) or a relative threshold (e.g., as a fraction of maximum signal intensity) before invoking find_peaks_1d_gauss or find_peaks_1d_localmax. In iterative Gaussian fitting, the algorithm fits successive Gaussian curves to residuals and terminates when fitted peak height falls below the threshold, ensuring only significant peaks are extracted. The threshold acts as both a stopping criterion and a validation filter: peaks with height below threshold are discarded, reducing noise while preserving high-confidence features. Choose absolute thresholds when instrument calibration is stable and noise floor is well-characterized; use relative thresholds for cross-sample robustness. Validate selection by inspecting residual sum-of-squares improvement per iteration and verifying that detected peak heights decrease monotonically across iterations.

## Related tools

- **mzapy.peaks.find_peaks_1d_gauss** (Perform iterative Gaussian fitting with peak-height threshold as stopping criterion; returns peaks exceeding the threshold.) — https://github.com/PNNL-m-q/mzapy
- **mzapy.peaks.find_peaks_1d_localmax** (Detect local maxima in 1D signal and filter by absolute/relative intensity threshold.) — https://github.com/PNNL-m-q/mzapy
- **scipy.optimize.curve_fit** (Underlying least-squares Gaussian fitting engine used by find_peaks_1d_gauss.)
- **numpy** (Array manipulation and residual computation during iterative peak subtraction.)

## Examples

```
from mzapy.peaks import find_peaks_1d_gauss; peaks = find_peaks_1d_gauss(signal_array, height_threshold=100, max_peaks=50, method='absolute')
```

## Evaluation signals

- Detected peak heights are strictly decreasing across iterations (monotonicity check).
- Residual sum-of-squares improves (decreases) with each fitted Gaussian subtracted.
- No peaks are reported with height below the specified threshold (completeness of filtering).
- Peak count stabilizes at or near expected number (e.g., known reference peaks in synthetic or QC data).
- Manual inspection of residuals shows remaining signal is primarily noise, with no visually obvious missed peaks above threshold.

## Limitations

- Threshold value is data-dependent and instrument-specific; no single universal threshold exists across vendor formats or acquisition conditions.
- Absolute thresholds are sensitive to instrument gain, ionization efficiency, and sample concentration—may require recalibration between MS methods.
- Relative thresholds can miss low-abundance isotopologs or metabolites if set too high relative to the major peak.
- Iterative fitting is computationally expensive for high-resolution spectra with hundreds of potential peaks; threshold choice affects convergence time.
- Overlapping or closely-spaced peaks may be incorrectly assigned to a single Gaussian, reducing detection sensitivity for multiplexed signals.

## Evidence

- [other] Initialize parameters: absolute or relative intensity threshold for peak height, maximum number of peaks to find, and Gaussian fitting configuration.: "Initialize parameters: absolute or relative intensity threshold for peak height, maximum number of peaks to find, and Gaussian fitting configuration."
- [other] fit a Gaussian curve to the current data, extract peak parameters (amplitude, mean, standard deviation), and check if peak height exceeds the stopping threshold.: "fit a Gaussian curve to the current data, extract peak parameters (amplitude, mean, standard deviation), and check if peak height exceeds the stopping threshold."
- [other] Subtract the fitted Gaussian from the residuals and repeat fitting on the updated residuals until reaching maximum peak count or falling below height threshold.: "Subtract the fitted Gaussian from the residuals and repeat fitting on the updated residuals until reaching maximum peak count or falling below height threshold."
- [other] verify that detected peaks have decreasing height across iterations and that residual sum-of-squares improves with each fit.: "verify that detected peaks have decreasing height across iterations and that residual sum-of-squares improves with each fit."
- [other] Two functions are provided for performing peak fitting on 1-dimensional data: ``mzapy.peaks.find_peaks_1d_localmax`` and ``mzapy.peaks.find_peaks_1d_gauss``: "Two functions are provided for performing peak fitting on 1-dimensional data: ``mzapy.peaks.find_peaks_1d_localmax`` and ``mzapy.peaks.find_peaks_1d_gauss``"
