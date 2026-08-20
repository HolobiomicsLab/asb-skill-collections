---
name: iterative-fitting-convergence
description: Use when you have 1D mass spectrometry signal data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - scipy
  - numpy
  - scipy.optimize
  - mzapy.peaks.find_peaks_1d_gauss
  techniques:
  - mass-spectrometry
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

# Iterative Fitting Convergence

## Summary

A peak detection and fitting workflow that iteratively applies least-squares Gaussian curve fitting to 1D mass spectrometry signal data, subtracting each fitted component from residuals until reaching a stopping criterion (maximum peak count or height threshold). This method enables accurate extraction of overlapping peaks and their parameters from noisy spectral data.

## When to use

Apply this skill when you have 1D mass spectrometry signal data (e.g., extracted ion chromatograms, arrival time distributions, or MS spectra) with multiple overlapping or close peaks that cannot be resolved by simple local-maximum detection alone, and you need precise estimates of peak position, height, and width for downstream quantitation or identification.

## When NOT to use

- Input signal contains only isolated, well-separated peaks that are adequately resolved by local-maximum detection (use simpler peak-picking methods instead).
- Signal exhibits strong non-Gaussian peak shapes (e.g., asymmetric or multimodal peaks); Gaussian model assumptions will be violated.
- Real-time or latency-critical applications where iterative refinement cost is prohibitive.

## Inputs

- 1D signal array (intensity values)
- absolute or relative intensity threshold (numeric)
- maximum number of peaks to detect (integer)
- Gaussian fitting configuration (optimizer settings, tolerance)

## Outputs

- list of detected peaks with fitted parameters: position (mean), height (amplitude), width (standard deviation)
- convergence metrics: peak heights per iteration, residual sum-of-squares trajectory

## How to apply

Initialize parameters: set an absolute or relative intensity threshold for minimum peak height, specify the maximum number of peaks to detect, and configure the Gaussian fitting method (e.g., least-squares optimizer). Fit a Gaussian curve to the full 1D signal using scipy.optimize or equivalent; extract the peak's amplitude, mean (position), and standard deviation (width). Check if the fitted peak height exceeds the stopping threshold. Subtract the fitted Gaussian from the signal to produce residuals. Repeat fitting on the residuals until either the maximum peak count is reached or the peak height falls below threshold. Validate convergence by confirming that peak heights decrease monotonically across iterations and that residual sum-of-squares (RSS) improves or plateaus with each iteration. Return all detected peaks with their fitted parameters.

## Related tools

- **scipy.optimize** (Provides least-squares optimization backend for Gaussian curve fitting in iterative loop) — https://docs.scipy.org/doc/scipy/reference/optimize.html
- **numpy** (Array manipulation, residual computation, parameter extraction and validation) — https://numpy.org
- **mzapy.peaks.find_peaks_1d_gauss** (Reference implementation of iterative Gaussian fitting for 1D peak detection in mass spectrometry data) — https://github.com/PNNL-m-q/mzapy

## Examples

```
from mzapy.peaks import find_peaks_1d_gauss; peaks = find_peaks_1d_gauss(signal_array, height_threshold=100, max_peaks=10)
```

## Evaluation signals

- Detected peak heights form a monotonically decreasing sequence across iterations (each fitted peak is smaller than the previous).
- Residual sum-of-squares (RSS) decreases or plateaus with each iteration; RSS should not increase significantly.
- All returned peaks have fitted parameters (position, height, width) within physically reasonable ranges for the signal domain.
- Peak count does not exceed the specified maximum; stopping threshold is honored (final peak height ≤ threshold).
- Subtraction of all fitted Gaussians from the original signal leaves residuals with no systematic structure or remaining peaks above the height threshold.

## Limitations

- Assumes peak shapes are well-modeled by Gaussian curves; real mass spectrometry peaks may be asymmetric or have tails, leading to model mismatch.
- Convergence speed and accuracy are sensitive to initial signal quality and noise level; very noisy or low-signal regions may produce spurious fits.
- Requires careful tuning of intensity threshold and maximum peak count; too lenient thresholds can extract noise, too strict thresholds can miss weak peaks.
- Least-squares fitting can be unstable if peaks overlap heavily or if residuals become very small; ill-conditioned matrices may occur.

## Evidence

- [other] Perform iterative least-squares Gaussian fitting on the signal: fit a Gaussian curve to the current data, extract peak parameters (amplitude, mean, standard deviation), and check if peak height exceeds the stopping threshold.: "Perform iterative least-squares Gaussian fitting on the signal: fit a Gaussian curve to the current data, extract peak parameters (amplitude, mean, standard deviation), and check if peak height"
- [other] Subtract the fitted Gaussian from the residuals and repeat fitting on the updated residuals until reaching maximum peak count or falling below height threshold.: "Subtract the fitted Gaussian from the residuals and repeat fitting on the updated residuals until reaching maximum peak count or falling below height threshold."
- [other] Validation: verify that detected peaks have decreasing height across iterations and that residual sum-of-squares improves with each fit.: "Validation: verify that detected peaks have decreasing height across iterations and that residual sum-of-squares improves with each fit."
- [other] Two functions are provided for performing peak fitting on 1-dimensional data: mzapy.peaks.find_peaks_1d_localmax and mzapy.peaks.find_peaks_1d_gauss: "Two functions are provided for performing peak fitting on 1-dimensional data: mzapy.peaks.find_peaks_1d_localmax and mzapy.peaks.find_peaks_1d_gauss"
- [other] mzapy provides a find_peaks_1d_gauss function for performing peak fitting on 1-dimensional data via Gaussian fitting, distinguished as a separate method from the local-maximum approach.: "mzapy provides a find_peaks_1d_gauss function for performing peak fitting on 1-dimensional data via Gaussian fitting, distinguished as a separate method from the local-maximum approach."
