---
name: mass-spectrometry-peak-detection-and-alignment
description: Use when after normalization, smoothing, and baseline reduction have been performed on raw MSImagingArrays data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - Cardinal
  - BiocParallel
  - R
  - Cardinal 3.6
  - matter 2.4 / matter 2.6
  - CardinalIO
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

# mass-spectrometry-peak-detection-and-alignment

## Summary

Detects and aligns peaks across mass spectrometry imaging spectra using Cardinal's peakPick() and peakProcess() functions, creating a unified reference peak table that summarizes detected peaks across the full imaging dataset. This skill transforms preprocessed MSImagingArrays data into an aligned, filtered MSImagingExperiment suitable for downstream statistical analysis.

## When to use

Apply this skill after normalization, smoothing, and baseline reduction have been performed on raw MSImagingArrays data. Use it when you need to create a reference peak table with consistent m/z positions across all spectra in an imaging experiment, enabling peak-based feature extraction and cross-spectrum comparison. Particularly useful when working with continuous imzML format data where peak alignment is essential for downstream clustering or classification.

## When NOT to use

- Input spectra have not undergone normalization, smoothing, and baseline reduction—apply preprocessing first.
- You require detection of peaks at the individual-spectrum level only without cross-spectrum alignment or reference peak generation.
- Working with already-processed peak tables or feature matrices—peakProcess() expects raw spectral data as input.

## Inputs

- MSImagingArrays object with normalized, smoothed, baseline-reduced spectra
- imzML file (continuous format) read via readMSIData()
- Analyze 7.5 format imaging data

## Outputs

- MSImagingExperiment object containing aligned reference peak table
- Peak m/z positions and intensities summarized across all spectra
- Filtered peak set meeting SNR and frequency thresholds

## How to apply

Load preprocessed MSImagingArrays data and call peakProcess() with method='diff' (or alternative noise estimation: derivative-based, quantile-based, or SD/MAD-based) and specify SNR threshold and sampleSize to control which spectra inform reference peak detection. peakProcess() performs peak picking on a subset of spectra (e.g., sampleSize=0.3), aggregates detected peaks into reference positions, then summarizes these reference peaks for every spectrum in the full dataset. Apply filterFreq threshold (e.g., 0.02) to retain only peaks meeting minimum frequency criteria. Output is an MSImagingExperiment object containing aligned reference peaks, metadata, and quality metrics. Use BiocParallel (via BPPARAM option) to parallelize across spectra for large datasets.

## Related tools

- **Cardinal 3.6** (Provides peakPick() and peakProcess() functions for peak detection, alignment, and reference peak summarization with multiple noise estimation methods.) — https://github.com/kuwisdelu/Cardinal
- **BiocParallel** (Enables parallel processing of peak picking and alignment across spectra via BPPARAM option for improved performance on large datasets.)
- **matter 2.4 / matter 2.6** (Low-level signal processing library underlying Cardinal's peak detection algorithms.)
- **CardinalIO** (Provides example imzML files and I/O support for reading continuous and processed imzML formats.)

## Examples

```
peakProcess(msi_arrays, method='diff', SNR=6, sampleSize=0.3, filterFreq=0.02, BPPARAM=BiocParallel::bpparam())
```

## Evaluation signals

- Reference peak table is non-empty and contains m/z positions with corresponding intensities or frequencies across all spectra.
- Peaks in the reference table meet specified SNR threshold (e.g., SNR=6) and frequency filter criteria (e.g., filterFreq=0.02).
- Number of aligned peaks is reasonable relative to sampleSize—subset-derived peaks generalize to full dataset without spurious inflation.
- Output MSImagingExperiment object contains coherent metadata, with peak counts and m/z ranges consistent with input preprocessing parameters.
- Downstream statistical analyses (PCA, clustering, classification) on peak-summarized data show expected spatial or phenotypic structure.

## Limitations

- Peak alignment quality depends critically on preprocessing quality; poor normalization, smoothing, or baseline reduction propagates into misaligned peaks.
- sampleSize parameter controls computational cost but may underrepresent rare or regional peaks if set too low.
- SNR and filterFreq thresholds must be tuned for specific instrument, sample type, and mass range; default values may not suit all applications.
- No changelog provided in the source documentation, making version-specific behavior changes difficult to trace.
- Continuous imzML files require memory-efficient handling; out-of-memory datasets may require iterative or chunked processing strategies not detailed in the primary workflow.

## Evidence

- [other] peakProcess() performs peak picking and alignment on a subset of spectra (specified by sampleSize) to create reference peaks, then summarizes these reference peaks for every spectrum in the full dataset, optionally filtering peaks by frequency threshold.: "peakProcess() performs peak picking and alignment on a subset of spectra (specified by sampleSize) to create reference peaks, then summarizes these reference peaks for every spectrum in the full"
- [intro] New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering, Continuous wavelet transform (CWT): "New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimation, Dynamic peak filtering, Continuous wavelet transform (CWT)"
- [intro] Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
- [intro] Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions: "Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions"
- [intro] Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
