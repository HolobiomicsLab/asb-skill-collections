---
name: spatial-spectral-array-processing
description: Use when you have preprocessed MSImagingArrays data (after normalization, smoothing, and baseline reduction) and need to detect peaks consistently across all spectra in an imaging experiment, create reference peak positions from a representative subset, and filter by signal-to-noise ratio and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
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
---

# spatial-spectral-array-processing

## Summary

Transform raw mass spectrometry imaging data into aligned, filtered reference peak matrices by applying noise estimation, peak picking, and frequency-based quality filtering across spatial spectral arrays. This skill bridges low-level signal processing (normalization, smoothing, baseline reduction) and high-level peak summarization for downstream statistical analysis.

## When to use

Apply this skill when you have preprocessed MSImagingArrays data (after normalization, smoothing, and baseline reduction) and need to detect peaks consistently across all spectra in an imaging experiment, create reference peak positions from a representative subset, and filter by signal-to-noise ratio and frequency thresholds to produce a uniform peak table for statistical analysis or image generation.

## When NOT to use

- Input is already a peak feature table or summarized peak matrix — peakProcess() requires raw spectra
- Spectra have not undergone normalization, smoothing, and baseline reduction — apply Cardinal preprocessing workflow first
- Analysis requires retention of all detected peaks without frequency filtering — use peakPick() alone if no aggregate filtering is needed

## Inputs

- MSImagingArrays (preprocessed with normalization, smoothing, baseline reduction)
- noise estimation parameter (method, SNR threshold)
- sampleSize (fraction of spectra for reference peak detection)
- filterFreq (peak frequency threshold)

## Outputs

- MSImagingExperiment (with aligned reference peak table)
- reference peak positions and intensities
- filtered peak matrix (peaks meeting SNR and frequency criteria)

## How to apply

Load preprocessed MSImagingArrays data and invoke peakProcess() with method='diff' for derivative-based noise estimation, SNR threshold (e.g., SNR=6), sampleSize parameter to define the fraction of spectra used for reference peak creation (e.g., sampleSize=0.3), and filterFreq to remove infrequent peaks (e.g., filterFreq=0.02 removes peaks occurring in <2% of spectra). The function detects and aligns peaks across the sample subset using specified noise thresholds, aggregates aligned peaks into reference positions, then applies the reference peak table to all spectra in the full dataset. Filter detected peaks by frequency and SNR criteria to ensure only robust, reproducible peaks are retained. The output is a single MSImagingExperiment object containing aligned reference peaks and associated metadata ready for downstream analysis.

## Related tools

- **Cardinal** (Core package providing peakProcess(), MSImagingArrays, MSImagingExperiment classes, and spectral preprocessing (normalize, smooth, reduceBaseline)) — github.com/kuwisdelu/Cardinal
- **BiocParallel** (Enables parallel processing of peakProcess() and other preprocessing methods across multiple cores via BPPARAM option)
- **matter** (Low-level signal processing backend for Cardinal 3.6 spectral operations)

## Examples

```
library(Cardinal); msidata_preproc <- normalize(msidata) %>% smooth(method='Gaussian') %>% reduceBaseline(method='SNIP'); peaks_exp <- peakProcess(msidata_preproc, method='diff', SNR=6, sampleSize=0.3, filterFreq=0.02)
```

## Evaluation signals

- Output MSImagingExperiment contains a reference peak table with m/z values and intensities for all spectra; check dimensions match input spectrum count
- Peaks in reference table meet SNR ≥ 6 threshold and appear in ≥ filterFreq (2%) of spectra
- Peak alignment is consistent: m/z values across spectra cluster within expected mass calibration tolerance (~ppm range)
- Preprocessing history is preserved in metadata; peakProcess() call parameters (method, SNR, sampleSize, filterFreq) are documented
- No spectra contain NaN or missing peak intensity values after filtering; peak table is complete and ready for statistical analysis

## Limitations

- Peak detection sensitivity depends critically on sampleSize and SNR threshold; small sampleSize may miss rare peaks, while high SNR may lose weak but consistent signals
- filterFreq threshold is dataset-dependent; peaks rare in one tissue region may be filtered out even if biologically important in another region
- Method='diff' noise estimation assumes derivative-based peak detection; other noise methods (quantile, SD/MAD, CWT) may perform differently on low-intensity or overlapping peaks
- peakProcess() requires aligned spectra; if input spectra have large m/z shifts, recalibrate() should be applied before peakProcess() to avoid reference peak fragmentation

## Evidence

- [other] peakProcess() performs peak picking and alignment on a subset of spectra (specified by sampleSize) to create reference peaks, then summarizes these reference peaks for every spectrum in the full dataset, optionally filtering peaks by frequency threshold.: "peakProcess() performs peak picking and alignment on a subset of spectra (specified by sampleSize) to create reference peaks, then summarizes these reference peaks for every spectrum in the full"
- [other] 1. Load preprocessed MSImagingArrays data containing spectra that have undergone normalization, smoothing, and baseline reduction. 2. Apply peakProcess() function in Cardinal to detect and align peaks across all spectra, using specified noise estimation and peak filtering parameters.: "Load preprocessed MSImagingArrays data containing spectra that have undergone normalization, smoothing, and baseline reduction. 2. Apply peakProcess() function in Cardinal to detect and align peaks"
- [intro] New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering, Continuous wavelet transform (CWT): "New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering, Continuous wavelet transform (CWT)"
- [intro] Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
- [intro] Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
