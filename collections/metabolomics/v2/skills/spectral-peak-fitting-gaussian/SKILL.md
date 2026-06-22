---
name: spectral-peak-fitting-gaussian
description: Use when you have 1D MS signal data (extracted ion chromatograms, arrival time distributions, or intensity profiles) and need to resolve overlapping or closely-spaced peaks with accurate position, height, and width estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - scipy
  - numpy
  - mzapy.peaks.find_peaks_1d_gauss
  - scipy.optimize.least_squares or scipy.optimize.curve_fit
  - mzapy.peaks.calc_gauss_psnr
  - mzapy.peaks.calc_peak_area
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
---

# Spectral peak fitting via Gaussian decomposition

## Summary

Detect and quantify peaks in 1D mass spectrometry signal data by iteratively fitting Gaussian curves to the signal and subtracting fitted components from residuals. This method is preferred over local-maximum detection when peak shape, amplitude, and width must be resolved precisely.

## When to use

Apply this skill when you have 1D MS signal data (extracted ion chromatograms, arrival time distributions, or intensity profiles) and need to resolve overlapping or closely-spaced peaks with accurate position, height, and width estimates. Use Gaussian fitting instead of local-maximum detection when the signal contains peaks with continuous intensity distributions that require shape characterization or when you need quantitative peak parameters for downstream feature extraction or isotope pattern analysis.

## When NOT to use

- Input signal is already pre-processed into a feature table (e.g., aligned peak matrix); use this skill on raw or minimally-processed 1D traces, not aggregate matrices.
- Peak shapes are known to be non-Gaussian (e.g., highly asymmetric due to instrumental distortion); consider alternative fitting models (e.g., exponential Gaussian hybrid) or validate Gaussian assumption first.
- Signal-to-noise ratio is very low or baseline is highly irregular; Gaussian fitting may converge to noise artifacts; apply baseline subtraction and noise filtering before peak fitting.

## Inputs

- 1D signal array (numpy array or similar) — m/z intensities, chromatographic intensities, or arrival time distribution counts
- Absolute or relative intensity threshold (scalar) — minimum peak height to retain
- Maximum peak count (integer) — upper limit on number of peaks to extract
- Gaussian fitting configuration (dict or parameters) — initial guess strategy, optimization tolerances, bounds

## Outputs

- Detected peaks array or list of dicts — each peak with position (mean), height (amplitude), width (standard deviation), and optionally goodness-of-fit metrics
- Residual signal array — final residuals after all peaks subtracted
- Peak parameters table — columns: scan/spectrum identifier, peak index, fitted mean m/z, fitted intensity, fitted sigma, residual sum-of-squares

## How to apply

Accept a 1D signal array and configure stopping criteria: an absolute or relative intensity threshold below which fitted peaks are discarded, and a maximum number of peaks to extract. Initialize by fitting a Gaussian curve to the full signal using least-squares optimization. Extract the fitted peak's parameters (amplitude, mean position, standard deviation width). Check if the peak height exceeds the stopping threshold; if yes, retain it and subtract the fitted Gaussian from the signal to produce residuals. Repeat the fitting process on the residuals until either the maximum peak count is reached or the next fitted peak falls below the height threshold. Return all detected peaks with their position, height, and width parameters. Validate the results by confirming that detected peak heights decrease across iterations and that residual sum-of-squares improves monotonically with each fit.

## Related tools

- **mzapy.peaks.find_peaks_1d_gauss** (Core function implementing iterative Gaussian peak fitting and subtraction on 1D MZA spectral arrays) — https://github.com/PNNL-m-q/mzapy
- **scipy.optimize.least_squares or scipy.optimize.curve_fit** (Underlying nonlinear optimization engine for Gaussian parameter estimation)
- **numpy** (Array manipulation and residual calculation)
- **mzapy.peaks.calc_gauss_psnr** (Post-fit validation metric; computes peak signal-to-noise ratio to assess goodness of Gaussian fit) — https://github.com/PNNL-m-q/mzapy
- **mzapy.peaks.calc_peak_area** (Auxiliary function to compute integrated peak area from fitted Gaussian parameters) — https://github.com/PNNL-m-q/mzapy

## Examples

```
from mzapy.peaks import find_peaks_1d_gauss; peaks = find_peaks_1d_gauss(signal_array, intensity_threshold=100, max_peaks=10, fit_config={'method': 'lsq'})
```

## Evaluation signals

- Monotonic decrease in fitted peak heights across successive iterations (first peak height ≥ second peak height ≥ ... ≥ last peak height).
- Residual sum-of-squares (RSS) decreases with each fitted Gaussian and does not increase after subtraction of subsequent peaks.
- All retained peaks have height ≥ configured intensity threshold; peaks below threshold are correctly rejected and not included in output.
- Fitted Gaussian parameters (mean, sigma) are within physically plausible bounds for the instrument and signal range (e.g., mean within m/z axis range, sigma > 0).
- Visual inspection: overlay of fitted Gaussian curves on original signal shows alignment with observed peak features; residual trace after peak subtraction exhibits noise-like character (no systematic over/under-fit).

## Limitations

- Gaussian assumption may fail for asymmetric or distorted peaks common in high-mass or time-of-flight spectra; method performs best on approximately bell-shaped profiles.
- Iterative subtraction can propagate fitting errors from early peaks into residuals; poor initial fits may cause spurious peaks in later iterations or false convergence.
- Requires careful tuning of intensity threshold and maximum peak count to avoid both under-detection (threshold too high) and over-detection (max count too high or threshold too low), especially in noisy data.
- Computational cost grows with signal length and number of peaks; may be slow for very long chromatographic traces or high-dimensional (2D) data without prior dimensionality reduction.
- Performance degrades when baseline is non-flat or contains systematic drift; pre-processing (baseline subtraction, smoothing) is recommended.

## Evidence

- [other] Two functions are provided for performing peak fitting on 1-dimensional data: ``mzapy.peaks.find_peaks_1d_localmax`` and ``mzapy.peaks.find_peaks_1d_gauss``: "Two functions are provided for performing peak fitting on 1-dimensional data: ``mzapy.peaks.find_peaks_1d_localmax`` and ``mzapy.peaks.find_peaks_1d_gauss``"
- [other] mzapy provides a find_peaks_1d_gauss function for performing peak fitting on 1-dimensional data via Gaussian fitting, distinguished as a separate method from the local-maximum approach.: "mzapy provides a find_peaks_1d_gauss function for performing peak fitting on 1-dimensional data via Gaussian fitting, distinguished as a separate method from the local-maximum approach."
- [other] Perform iterative least-squares Gaussian fitting on the signal: fit a Gaussian curve to the current data, extract peak parameters (amplitude, mean, standard deviation), and check if peak height exceeds the stopping threshold. Subtract the fitted Gaussian from the residuals and repeat fitting on the updated residuals until reaching maximum peak count or falling below height threshold.: "Perform iterative least-squares Gaussian fitting on the signal: fit a Gaussian curve to the current data, extract peak parameters (amplitude, mean, standard deviation), and check if peak height"
- [other] Validation: verify that detected peaks have decreasing height across iterations and that residual sum-of-squares improves with each fit.: "Validation: verify that detected peaks have decreasing height across iterations and that residual sum-of-squares improves with each fit."
- [other] Accept a 1D signal array as input. Initialize parameters: absolute or relative intensity threshold for peak height, maximum number of peaks to find, and Gaussian fitting configuration.: "Accept a 1D signal array as input. Initialize parameters: absolute or relative intensity threshold for peak height, maximum number of peaks to find, and Gaussian fitting configuration."
