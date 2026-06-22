---
name: noise-estimation-snr-thresholding
description: Use when after normalizing, smoothing, and baseline-reducing mass spectra via normalize(), smooth(), and reduceBaseline(), when you need to distinguish true peaks from noise-induced artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0943
  - http://edamontology.org/topic_3520
  tools:
  - Cardinal
  - BiocParallel
  - R
  - matter
derived_from:
- doi: 10.1093/bioinformatics/btv146
  title: Cardinal
evidence_spans:
- library(Cardinal)
- '*Cardinal 3.6* is a major update with breaking changes. It bring support many of the new low-level signal processing functions'
- Parallel processing support via the *BiocParallel* package for all pre-processing methods
- Parallel processing support via the *BiocParallel* package for all pre-processing methods and any statistical analysis methods with a `BPPARAM` option
- 'Once installed, Cardinal can be loaded with library(): library(Cardinal)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cardinal_cq
    doi: 10.1093/bioinformatics/btv146
    title: Cardinal
  dedup_kept_from: coll_cardinal_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btv146
  all_source_dois:
  - 10.1093/bioinformatics/btv146
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# noise-estimation-snr-thresholding

## Summary

Estimate signal-to-noise ratio (SNR) from preprocessed mass spectra using derivative-based, quantile-based, or statistical deviation methods, then apply an SNR threshold to identify and retain only peaks that exceed the noise floor. This skill separates genuine spectral peaks from noise artifacts in mass spectrometry imaging data.

## When to use

After normalizing, smoothing, and baseline-reducing mass spectra via normalize(), smooth(), and reduceBaseline(), when you need to distinguish true peaks from noise-induced artifacts. Use this skill when you have preprocessed MSImagingArrays or MSImagingExperiment objects and require robust peak detection with tunable SNR thresholds (e.g., SNR=3) tailored to your instrument's noise characteristics.

## When NOT to use

- Input spectra have not been normalized, smoothed, or baseline-reduced—preprocessing must precede SNR thresholding to establish reliable noise estimates.
- SNR threshold is set without reference to instrument characteristics or dataset-specific noise profiles; arbitrary thresholds may eliminate true peaks or retain noise.
- Peak picking is already complete and you need only to filter or re-rank existing peaks—use a filtering step instead of re-applying peakPick().

## Inputs

- MSImagingArrays object (normalized, smoothed, baseline-reduced)
- MSImagingExperiment object (normalized, smoothed, baseline-reduced)
- preprocessed mass spectra with m/z and intensity values

## Outputs

- picked-peaks spectrum (m/z and intensity for detected peaks only)
- peak annotations with SNR values per spectrum
- binary peak matrix (spectra × m/z features)

## How to apply

Load a preprocessed MSImagingArrays object that has undergone normalization (via normalize()), smoothing (via smooth()), and baseline reduction (via reduceBaseline()). Select a noise-estimation method in peakPick(): derivative-based (method='diff') estimates SNR from deviations between the spectrum and a rolling average of its derivative; quantile-based and SD/MAD-based methods offer alternative statistical approaches. Set the SNR threshold parameter (e.g., SNR=3) to control sensitivity—lower thresholds detect more peaks but increase false positives, while higher thresholds reduce false discoveries but may miss weak signals. Execute peakPick() across all spectra in the array using BiocParallel for efficiency. Extract the resulting picked-peaks spectrum and verify that peak heights exceed the expected noise floor.

## Related tools

- **Cardinal** (Provides peakPick() function with derivative-based, quantile-based, SD/MAD-based, dynamic peak filtering, and CWT noise estimation methods; manages MSImagingArrays and MSImagingExperiment data structures) — https://github.com/kuwisdelu/Cardinal
- **BiocParallel** (Enables parallel processing of peakPick() across all spectra in the imaging array for improved performance)
- **matter** (Provides low-level signal processing functions underlying Cardinal's noise estimation and peak detection pipeline)

## Examples

```
spc_picked <- peakPick(spc_preprocessed, method="diff", SNR=3, BPPARAM=BiocParallel::bpparam())
```

## Evaluation signals

- Peak detection rate: verify that the number of detected peaks is consistent with expected spectral complexity; too few peaks may indicate SNR threshold too high, too many may indicate threshold too low or preprocessing artifacts.
- SNR distribution check: examine histogram or summary statistics of per-peak SNR values to confirm they cluster above the threshold and that the threshold is appropriate for the noise floor.
- Reproducibility across spectra: confirm that spectra with similar chemical composition show concordant peak lists after SNR thresholding, indicating stable noise estimation.
- Baseline noise verification: spot-check low-intensity regions of raw spectra to confirm that peaks below the SNR threshold correspond to actual noise rather than weak but real signals.
- Comparison with reference method: if available, compare picked-peaks output against manually validated peaks or peaks from alternative peak-picking software to assess false positive and false negative rates.

## Limitations

- SNR threshold is a global parameter applied uniformly across all spectra; localized or dynamic thresholding may be needed for spectra with spatially varying noise profiles.
- Derivative-based noise estimation (method='diff') assumes that the rolling average of the derivative is a reliable proxy for noise; in spectra with high baseline residuals or sharp discontinuities, this assumption may fail.
- SNR estimation does not account for instrumental drift, detector saturation, or mass calibration errors, which can inflate or deflate apparent SNR values.
- Choice of preprocessing methods (normalization method, smoothing kernel, baseline algorithm) influences the final noise floor and SNR estimates; suboptimal preprocessing can degrade peak picking performance regardless of SNR threshold.

## Evidence

- [other] peakPick() with method='diff' and SNR=3 estimates signal-to-noise ratio from deviations between the spectrum and a rolling average of its derivative, then detects peaks exceeding the specified SNR threshold.: "peakPick() with method='diff' and SNR=3 estimates signal-to-noise ratio from deviations between the spectrum and a rolling average of its derivative, then detects peaks exceeding the specified SNR"
- [other] 1. Load the preprocessed MSImagingArrays object (normalized via normalize(), smoothed via smooth(), and baseline-reduced via reduceBaseline()). 2. Queue derivative-based peak picking using peakPick() with method="diff" and SNR threshold set to 3.: "Load the preprocessed MSImagingArrays object (normalized via normalize(), smoothed via smooth(), and baseline-reduced via reduceBaseline()). 2. Queue derivative-based peak picking using peakPick()"
- [intro] New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering, Continuous wavelet transform (CWT): "New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering, Continuous wavelet transform (CWT)"
- [intro] Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
- [intro] Use normalize() to queue normalization on MSImagingArrays or MSImagingExperiment: "Use normalize() to queue normalization on MSImagingArrays or MSImagingExperiment"
