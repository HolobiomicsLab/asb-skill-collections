---
name: spectral-noise-filtering-dynamic-peak
description: Use when use this skill after normalizing, smoothing, and baseline-reducing MSImagingArrays objects when you need to detect peaks across multiple spectra with consistent SNR-based thresholding.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# Spectral noise filtering with dynamic peak picking

## Summary

Apply derivative-based signal-to-noise ratio (SNR) estimation and dynamic peak filtering in peakPick() to identify true peaks in preprocessed mass spectra while suppressing noise-driven false positives. This skill is essential when baseline-reduced and smoothed spectra contain peaks of varying intensity and width that require intelligent noise thresholding.

## When to use

Use this skill after normalizing, smoothing, and baseline-reducing MSImagingArrays objects when you need to detect peaks across multiple spectra with consistent SNR-based thresholding. Apply it when spectral noise varies across the dataset or when peak widths are heterogeneous, requiring dynamic filtering rather than fixed intensity cutoffs.

## When NOT to use

- Input spectra have not been baseline-reduced; derivative-based SNR estimation may conflate baseline drift with signal.
- Spectra are extremely noisy or contain broad, overlapping peaks; SNR method may fail to separate them.
- Your analysis goal requires intensity-quantified peaks rather than presence/absence; peakPick() returns binary peak locations.

## Inputs

- MSImagingArrays object (preprocessed: normalized, smoothed, baseline-reduced)
- Spectra with m/z vectors and intensity values

## Outputs

- Picked-peaks spectrum (m/z and intensity of detected peaks)
- Peak detection results compatible with downstream statistical analysis

## How to apply

Load a preprocessed MSImagingArrays object (normalized via normalize(), smoothed via smooth(), and baseline-reduced via reduceBaseline()). Queue derivative-based peak picking using peakPick() with method='diff' and SNR=3, which estimates signal-to-noise ratio from deviations between the spectrum and a rolling average of its derivative. The method detects peaks exceeding the specified SNR threshold while rejecting noise-driven candidates. Execute the peak detection pipeline on all spectra in the array using BiocParallel for efficiency. Extract the resulting picked-peaks spectrum and validate that peaks are above the noise floor and consistent across replicate spectra.

## Related tools

- **Cardinal 3.6** (Implements peakPick() with method='diff' SNR estimation, smooth(), normalize(), and reduceBaseline() preprocessing functions.) — github.com/kuwisdelu/Cardinal
- **BiocParallel** (Enables parallel processing of peak detection across all spectra in the array via BPPARAM option.)
- **matter 2.4 / 2.6** (Provides low-level signal processing functions supporting Cardinal 3.6 spectral operations.)

## Examples

```
mse <- readMSIData(path); mse <- normalize(mse); mse <- smooth(mse, method='Gaussian'); mse <- reduceBaseline(mse, method='SNIP'); peaks <- peakPick(mse, method='diff', SNR=3)
```

## Evaluation signals

- Detected peaks have SNR values ≥ 3 (as specified); noise-driven candidates below threshold are rejected.
- Peak locations are reproducible across replicate spectra or technical replicates, indicating robust detection.
- Peaks align with known mass values or reference m/z standards when available; systematic mass offsets suggest recalibration is needed.
- Peak count and distribution are consistent with domain expectations (e.g., known protein or lipid mass ranges).
- Derivative-based SNR estimates reflect local noise variation; peaks in low-noise regions are detected at lower absolute intensities than in noisy regions.

## Limitations

- SNR=3 threshold is user-specified; suboptimal choice may over- or under-detect peaks depending on noise profile.
- Derivative-based method assumes smooth baseline after reduceBaseline(); residual baseline curvature may inflate noise estimates.
- Dynamic peak filtering is sensitive to spectrum smoothing parameters; over-smoothing suppresses true peaks, under-smoothing increases false positives.
- No changelog or detailed parameter tuning guidance provided in the article; optimization requires iterative experimentation.

## Evidence

- [other] peakPick() with method='diff' and SNR=3 estimates signal-to-noise ratio from deviations between the spectrum and a rolling average of its derivative, then detects peaks exceeding the specified SNR threshold.: "peakPick() with method='diff' and SNR=3 estimates signal-to-noise ratio from deviations between the spectrum and a rolling average of its derivative, then detects peaks exceeding the specified SNR"
- [intro] New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering, Continuous wavelet transform (CWT): "New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering, Continuous wavelet transform (CWT)"
- [other] Load the preprocessed MSImagingArrays object (normalized via normalize(), smoothed via smooth(), and baseline-reduced via reduceBaseline()): "Load the preprocessed MSImagingArrays object (normalized via normalize(), smoothed via smooth(), and baseline-reduced via reduceBaseline())"
- [intro] Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
