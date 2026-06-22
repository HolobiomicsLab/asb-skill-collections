---
name: signal-residual-deconvolution
description: Use when analyzing 1D signal arrays (e.g., extracted ion chromatograms, arrival time distributions, or MS1 spectra intensity profiles) where multiple peaks may overlap or where peak shape information (amplitude, position, width) is required beyond simple local-maximum detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - scipy
  - numpy
  - scipy.optimize.least_squares
  - mzapy.peaks.find_peaks_1d_gauss
  - mzapy.peaks.calc_gauss_psnr
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

# Implement the Gaussian-fit 1D peak detection function

## Summary

Iteratively fit Gaussian curves to 1D mass spectrometry signal data, subtracting each fitted peak from the residuals to detect and quantify overlapping peaks by successive least-squares optimization. This approach is distinguished from local-maximum peak detection and is particularly suited to noisy or densely-packed spectral features.

## When to use

Apply this skill when analyzing 1D signal arrays (e.g., extracted ion chromatograms, arrival time distributions, or MS1 spectra intensity profiles) where multiple peaks may overlap or where peak shape information (amplitude, position, width) is required beyond simple local-maximum detection. Use when the input signal is dense enough that simple thresholding would miss smaller peaks hidden in the residuals of larger ones, or when Gaussian peak shape models are appropriate for the instrumentation (e.g., LC-MS, ion-mobility MS).

## When NOT to use

- Signal contains non-Gaussian peak shapes (e.g., sharp rectangular or Lorentzian profiles) where Gaussian model assumption is violated.
- Input is already a deconvolved or processed peak table; re-deconvolving may introduce spurious peaks or distort existing peak parameters.
- Signal-to-noise ratio is extremely low (sparse or heavily baseline-dominated data) where threshold-based stopping criteria become unreliable.

## Inputs

- 1D signal array (numpy array or list of intensity values)
- Intensity threshold parameter (absolute or relative)
- Maximum number of peaks to detect (integer)
- Gaussian fitting configuration (scipy least-squares parameters)

## Outputs

- List of detected peaks with fitted parameters (position, height, width)
- Peak amplitude values (Gaussian fit coefficient)
- Peak mean/position (Gaussian fit center)
- Peak standard deviation/width (Gaussian fit sigma)
- Residual array after all peak subtractions

## How to apply

Initiate iterative least-squares Gaussian fitting on the input 1D signal array by setting an absolute or relative intensity threshold for peak-height stopping criterion, a maximum peak count, and Gaussian fitting configuration parameters. In each iteration, fit a Gaussian curve to the current data (or residuals on first iteration), extract peak parameters (amplitude, mean, standard deviation), and verify that peak height exceeds the stopping threshold. Subtract the fitted Gaussian from the residuals and repeat fitting on the updated residuals. Terminate when reaching the maximum peak count or when residual peak heights fall below threshold. Collect all detected peaks and validate that detected peak heights show monotonic decrease across iterations and that residual sum-of-squares improves with each new fit.

## Related tools

- **scipy.optimize.least_squares** (Performs iterative least-squares optimization for Gaussian curve fitting to signal data) — https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
- **numpy** (Provides 1D array operations for signal residual subtraction and parameter storage) — https://numpy.org/
- **mzapy.peaks.find_peaks_1d_gauss** (Reference implementation of Gaussian-fit 1D peak detection for mzapy data objects) — https://github.com/PNNL-m-q/mzapy
- **mzapy.peaks.calc_gauss_psnr** (Compute peak signal-to-noise ratio from Gaussian fit results for validation) — https://github.com/PNNL-m-q/mzapy

## Examples

```
from mzapy.peaks import find_peaks_1d_gauss; peaks = find_peaks_1d_gauss(signal_array, intensity_threshold=100, max_peaks=10, method='gaussian')
```

## Evaluation signals

- Detected peak heights form a monotonically decreasing sequence across iterations (amplitude_iter_i ≥ amplitude_iter_(i+1)).
- Residual sum-of-squares (RSS) monotonically decreases with each iteration: RSS_i ≥ RSS_(i+1) before stopping criterion is met.
- All returned peaks have heights strictly exceeding the specified stopping threshold; no peak below threshold is reported.
- Peak count does not exceed the configured maximum; iteration terminates as soon as max count is reached or threshold is breached.
- Gaussian fit parameters (amplitude, mean, sigma) are physically plausible for the signal domain (e.g., sigma > 0, amplitude > 0, mean within signal array bounds).

## Limitations

- Gaussian model assumes peak shapes follow normal distribution; real MS peaks may have tails or asymmetry not captured by this model.
- Iterative subtraction can accumulate fitting errors; early iterations with poor fits propagate into residuals for later peaks, potentially degrading later peak quality.
- Performance depends critically on initialization of fitting parameters and convergence criteria; poor choices may result in local minima or missed peaks.
- Method does not account for baseline drift, noise coloration, or instrumental artifacts that may violate Gaussian assumption.
- Computational cost scales with signal length and maximum peak count; very long signals or high peak counts may be slow.

## Evidence

- [other] Gaussian fitting and residual subtraction workflow: "Perform iterative least-squares Gaussian fitting on the signal: fit a Gaussian curve to the current data, extract peak parameters (amplitude, mean, standard deviation), and check if peak height"
- [other] Peak detection method distinction: "Two functions are provided for performing peak fitting on 1-dimensional data: ``mzapy.peaks.find_peaks_1d_localmax`` and ``mzapy.peaks.find_peaks_1d_gauss``"
- [other] Validation of iterative fits: "Validation: verify that detected peaks have decreasing height across iterations and that residual sum-of-squares improves with each fit."
- [other] Output parameters from Gaussian fit: "Collect and return all detected peaks with their fitted parameters (position, height, width)."
- [readme] MZA data access for 1D arrays: "extract extracted ion chromatograms ... Extracted Ion Chromatograms ... collect arrival time distributions ... Arrival Time Distributions"
