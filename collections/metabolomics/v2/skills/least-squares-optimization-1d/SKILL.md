---
name: least-squares-optimization-1d
description: Use when when you have a 1D signal array (e.g., extracted ion chromatogram, arrival time distribution, or MS1 spectrum intensity profile) and need to identify and quantify overlapping or adjacent peaks with precise position, height, and width estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - scipy
  - numpy
  - scipy.optimize (least-squares fitting backend)
  - mzapy.peaks.find_peaks_1d_gauss
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

# Least-squares optimization for 1D peak fitting

## Summary

Iteratively fit Gaussian curves to 1D mass spectrometry signals using least-squares optimization, extracting peak parameters (amplitude, mean, standard deviation) and refining estimates by subtracting fitted components from residuals until convergence or stopping thresholds are met.

## When to use

When you have a 1D signal array (e.g., extracted ion chromatogram, arrival time distribution, or MS1 spectrum intensity profile) and need to identify and quantify overlapping or adjacent peaks with precise position, height, and width estimates. This is the appropriate choice when peaks follow approximately Gaussian distributions and you need fitted parameters (not just local maxima) for downstream isotope pattern matching, peak area integration, or mass accuracy assessment.

## When NOT to use

- Input signal is already a feature table or pre-extracted peak list (peaks are already resolved).
- Peaks in your signal do not follow Gaussian distributions (e.g., highly asymmetric, multi-modal, or instrumental artifacts); local-maxima detection may be more robust.
- You need only peak counts or presence/absence calls without quantitative parameters; simpler threshold-based or derivative-based peak finding suffices.

## Inputs

- 1D signal array (intensity values as numpy array or list)
- Absolute or relative intensity threshold (float, for peak height filtering)
- Maximum peak count (integer)
- Gaussian fitting configuration (scipy.optimize parameters or equivalent)

## Outputs

- List of detected peaks with fitted parameters: position (mean), height (amplitude), width (standard deviation)
- Residual signal array after subtracting all fitted Gaussians
- Convergence diagnostic: residual sum-of-squares per iteration

## How to apply

Initialize a least-squares fitter with your signal array and configure stopping criteria: an absolute or relative intensity threshold for minimum peak height and a maximum number of peaks to extract. Fit a Gaussian curve to the current signal using iterative least-squares minimization, extracting the fitted peak's amplitude (height), mean (position), and standard deviation (width). Check if the peak height exceeds your stopping threshold; if so, record the peak parameters and subtract the fitted Gaussian from the signal to obtain residuals. Repeat the fitting process on the residuals with the updated signal until you reach the maximum peak count or fall below the height threshold. Validate the fit quality by verifying that detected peak heights decrease monotonically across iterations and that the residual sum-of-squares improves with each successive fit.

## Related tools

- **scipy.optimize (least-squares fitting backend)** (Provides iterative least-squares minimization algorithm for fitting Gaussian curve parameters to signal data)
- **numpy** (Efficient array operations for signal manipulation, residual computation, and peak parameter storage)
- **mzapy.peaks.find_peaks_1d_gauss** (High-level implementation of 1D Gaussian peak fitting for mass spectrometry data in MZA format) — https://github.com/PNNL-m-q/mzapy
- **mzapy.peaks.calc_gauss_psnr** (Validation utility to compute peak signal-to-noise ratio for fitted Gaussian peaks) — https://github.com/PNNL-m-q/mzapy
- **mzapy.peaks.calc_peak_area** (Quantitative integration of peak area under fitted Gaussian curves for intensity measurement) — https://github.com/PNNL-m-q/mzapy

## Examples

```
from mzapy.peaks import find_peaks_1d_gauss; peaks = find_peaks_1d_gauss(signal_array, intensity_threshold=100, max_peaks=10)
```

## Evaluation signals

- Fitted peak heights are strictly decreasing across iterations (monotonicity check).
- Residual sum-of-squares decreases with each successive Gaussian subtraction; fit quality improves.
- Detected peak positions, heights, and widths are consistent across repeated runs on the same signal (reproducibility).
- Peak heights exceed the configured intensity threshold and do not fall below it prematurely.
- Total number of detected peaks does not exceed the maximum count parameter; fitting terminates correctly.

## Limitations

- Assumes peaks follow Gaussian distributions; non-Gaussian peak shapes (e.g., Lorentzian, exponential tails) will be poorly fit and yield biased parameters.
- Iterative subtraction can accumulate numerical error if residuals become very small or noisy; may require regularization or stopping criteria tuning.
- Highly overlapping or adjacent peaks may not be resolved independently; fitting may attribute merged intensity to a single peak.
- Performance depends critically on initial guess and choice of stopping thresholds; poor threshold tuning may leave residual peaks unfitted or extract noise as spurious peaks.

## Evidence

- [other] Gaussian fitting is iterative least-squares approach: "Perform iterative least-squares Gaussian fitting on the signal: fit a Gaussian curve to the current data, extract peak parameters (amplitude, mean, standard deviation)"
- [other] Residual subtraction and convergence stopping criteria: "Subtract the fitted Gaussian from the residuals and repeat fitting on the updated residuals until reaching maximum peak count or falling below height threshold"
- [other] Output peak parameters and validation metrics: "Collect and return all detected peaks with their fitted parameters (position, height, width). 6. Validation: verify that detected peaks have decreasing height across iterations and that residual"
- [other] mzapy provides dedicated 1D Gaussian peak fitting function: "Two functions are provided for performing peak fitting on 1-dimensional data: ``mzapy.peaks.find_peaks_1d_localmax`` and ``mzapy.peaks.find_peaks_1d_gauss``"
