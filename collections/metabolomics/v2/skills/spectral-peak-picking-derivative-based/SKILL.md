---
name: spectral-peak-picking-derivative-based
description: Use when you have preprocessed MSImagingArrays objects (normalized via normalize(), smoothed via smooth(), and baseline-reduced via reduceBaseline()) and need to identify discrete peaks across all spectra in a mass spectrometry imaging dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0081
  tools:
  - Cardinal
  - BiocParallel
  - R
  - Cardinal 3.6
  - matter 2.4 / 2.6
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
---

# spectral-peak-picking-derivative-based

## Summary

Detect peaks in preprocessed mass spectra using derivative-based signal-to-noise ratio (SNR) estimation in peakPick(). This method identifies peaks by comparing the spectrum's derivative against a rolling average and flagging deviations that exceed a specified SNR threshold, suitable for imzML and Analyze 7.5 imaging data after normalization, smoothing, and baseline reduction.

## When to use

Apply this skill when you have preprocessed MSImagingArrays objects (normalized via normalize(), smoothed via smooth(), and baseline-reduced via reduceBaseline()) and need to identify discrete peaks across all spectra in a mass spectrometry imaging dataset. Use derivative-based peak picking when you want SNR estimation to reflect localized noise characteristics in the preprocessed spectrum rather than global intensity statistics.

## When NOT to use

- Input spectra have not been preprocessed (normalized, smoothed, baseline-reduced); derivative-based SNR estimation assumes clean preprocessing
- Peak picking has already been performed; do not re-pick on already-picked spectra
- Raw, unprocessed imzML spectra are input directly; preprocessing steps must precede peak picking

## Inputs

- MSImagingArrays object (normalized, smoothed, baseline-reduced)
- Preprocessed mass spectra from imzML or Analyze 7.5 format

## Outputs

- Picked-peaks spectrum (MSImagingArrays with detected peak m/z and intensity values)
- Peak detection results suitable for statistical analysis or imaging visualization

## How to apply

Load a preprocessed MSImagingArrays object and queue the peakPick() function with method='diff' and SNR parameter set to 3 (or adjusted based on noise tolerance). The derivative-based method estimates signal-to-noise ratio by computing deviations between the spectrum and a rolling average of its derivative, then detects peaks wherever the deviation exceeds the SNR threshold. Execute the peak detection pipeline using BiocParallel for parallelized processing across all spectra in the array. Extract the resulting picked-peaks spectrum, which contains detected peak m/z values and intensities for downstream statistical analysis or visualization.

## Related tools

- **Cardinal 3.6** (Provides peakPick() function with method='diff' for derivative-based peak detection and MSImagingArrays data structures) — github.com/kuwisdelu/Cardinal
- **BiocParallel** (Enables parallel processing of peak detection across multiple spectra via BPPARAM option)
- **matter 2.4 / 2.6** (Provides low-level signal processing functions supporting Cardinal's spectral preprocessing and peak picking)

## Examples

```
# Load and preprocess MSImagingArrays, then perform derivative-based peak picking
msi <- readMSIData('data.imzML')
msi <- normalize(msi, method='tic')
msi <- smooth(msi, method='gaussian')
msi <- reduceBaseline(msi, method='snip')
msi_peaks <- peakPick(msi, method='diff', SNR=3, BPPARAM=BiocParallel::bpparam())
```

## Evaluation signals

- Output peak list contains m/z and intensity values above the SNR=3 threshold with no NaN or infinite values
- Number of detected peaks per spectrum is consistent with expected spectral complexity and preprocessing quality
- Peak m/z values align with known calibration range and do not appear at baseline or artifact regions after baseline reduction
- Comparison with alternative peak picking methods (quantile-based, CWT) shows consistent major peak detection while differing on minor/shoulder peaks
- Derivative-based SNR estimates vary appropriately across spectra based on local noise characteristics rather than global intensity scaling

## Limitations

- Derivative-based SNR estimation may be sensitive to residual noise or ripples from smoothing; ensure smooth() preprocessing is appropriate
- SNR threshold (default 3) is a single global parameter; spectra with highly variable local noise may require manual SNR tuning or post-hoc filtering
- Method assumes spectra are already baseline-corrected; substantial baseline residuals will inflate derivative estimates and degrade peak detection
- No changelog available; version-specific behavior differences between Cardinal 3.6 and prior releases are undocumented

## Evidence

- [other] peakPick() with method='diff' and SNR=3 estimates signal-to-noise ratio from deviations between the spectrum and a rolling average of its derivative, then detects peaks exceeding the specified SNR threshold.: "peakPick() with method='diff' and SNR=3 estimates signal-to-noise ratio from deviations between the spectrum and a rolling average of its derivative, then detects peaks exceeding the specified SNR"
- [other] Preprocessing workflow includes normalization, smoothing, and baseline reduction before peak picking.: "Load the preprocessed MSImagingArrays object (normalized via normalize(), smoothed via smooth(), and baseline-reduced via reduceBaseline())."
- [intro] Parallel processing support via BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
- [intro] New peak picking methods in peakPick() include derivative-based noise estimation among others.: "New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering, Continuous wavelet transform (CWT)"
- [intro] Cardinal natively supports reading and writing imzML and Analyze 7.5 formats via readMSIData() and writeMSIData() functions: "Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions"
