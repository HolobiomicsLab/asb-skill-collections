---
name: spectral-reference-peak-summarization
description: Use when after peak picking and alignment have been performed on preprocessed spectra (normalized, smoothed, and baseline-reduced), and you need to create a unified peak reference table that can be applied consistently across all spectra in an imaging dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Cardinal
  - BiocParallel
  - R
  - matter
  techniques:
  - MS-imaging
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

# spectral-reference-peak-summarization

## Summary

Aggregate detected and aligned peaks across a subset of mass spectrometry imaging spectra to create reference peak positions, then summarize these positions for every spectrum in the full dataset. This skill transforms preprocessed MSImagingArrays data into an aligned, filtered MSImagingExperiment with consistent peak annotations across the imaging array.

## When to use

After peak picking and alignment have been performed on preprocessed spectra (normalized, smoothed, and baseline-reduced), and you need to create a unified peak reference table that can be applied consistently across all spectra in an imaging dataset. Use this when working with MSImagingArrays data where you want to reduce m/z alignment noise and establish a canonical set of peaks for downstream statistical analysis or classification.

## When NOT to use

- Input is already a feature table or peak intensity matrix — peakProcess() is a detection and summarization step, not a transformation of pre-computed features.
- Spectra have not been preprocessed (normalized, smoothed, baseline-reduced) — reference peak quality depends on clean input spectra.
- You require peak picking on the full dataset without subset sampling — sampleSize=1.0 may be computationally expensive but is supported if necessary.

## Inputs

- MSImagingArrays object (preprocessed with normalization, smoothing, and baseline reduction)
- Peak picking results (detected peaks with m/z positions and intensities)
- Alignment information (spectral alignment warping or local maxima correspondences)

## Outputs

- MSImagingExperiment object with reference peak table
- Peak feature matrix (features × spectra)
- Reference peak metadata (m/z positions, frequency, SNR per peak)

## How to apply

First, apply peakProcess() with method='diff' to detect and align peaks across a representative subset of spectra (controlled by sampleSize parameter, e.g., 0.3 for 30% of spectra). Specify noise estimation parameters (SNR=6, filterFreq=0.02) to filter out weak or low-frequency peaks during reference creation. The function aggregates detected peaks into reference peak positions by finding consensus m/z values across the subset. Finally, summarize these reference peaks for every spectrum in the full dataset, outputting an MSImagingExperiment object containing the reference peak table and associated metadata. Optionally apply quality filtering by frequency threshold or signal-to-noise ratio to further refine the reference peaks.

## Related tools

- **Cardinal** (Primary package implementing peakProcess() function and MSImagingArrays/MSImagingExperiment classes for peak detection, alignment, and summarization) — github.com/kuwisdelu/Cardinal
- **BiocParallel** (Enables parallel processing of peakProcess() via BPPARAM option to accelerate peak detection across large imaging arrays)
- **matter** (Underlying low-level signal processing library providing efficient handling of out-of-memory spectra data structures)

## Examples

```
library(Cardinal); data <- readMSIData("data.imzML"); data_proc <- normalize(data) %>% smooth() %>% reduceBaseline(); peaks <- peakProcess(data_proc, method="diff", SNR=6, sampleSize=0.3, filterFreq=0.02); summary_peaks <- featureApply(peaks, fun=mean)
```

## Evaluation signals

- Output MSImagingExperiment contains non-zero reference peak table with m/z positions and frequencies matching input spectra alignment.
- Number of reference peaks is substantially smaller than total number of peaks detected in raw data (compression confirms successful summarization).
- Peak intensity values in full dataset are aligned to reference m/z values with minimal m/z drift (verify via histogram of peak position residuals).
- Quality metrics (SNR, frequency) of reference peaks meet specified thresholds (SNR ≥ 6, filterFreq ≥ 0.02 in this example).
- Downstream statistical analysis (e.g., PCA, clustering) shows improved separation and reproducibility compared to non-summarized peaks.

## Limitations

- Reference peak quality depends heavily on the sampleSize parameter — too small a subset may miss rare or low-intensity peaks; too large risks computational overhead.
- Peak summarization assumes spectra are adequately aligned before reference creation; misalignment will produce multiple reference peaks for the same true m/z.
- Filtering by frequency threshold (filterFreq) removes infrequent peaks, which may discard biologically relevant features that are present in only a subset of pixels.
- Out-of-memory datasets require Cardinal 3.6+ support for continuous and processed imzML formats; older versions may require data subsetting.

## Evidence

- [other] peakProcess() performs peak picking and alignment on a subset of spectra (specified by sampleSize) to create reference peaks, then summarizes these reference peaks for every spectrum in the full dataset: "peakProcess() performs peak picking and alignment on a subset of spectra (specified by sampleSize) to create reference peaks, then summarizes these reference peaks for every spectrum in the full"
- [other] Apply peakProcess() function in Cardinal to detect and align peaks across all spectra, using specified noise estimation and peak filtering parameters: "Apply peakProcess() function in Cardinal to detect and align peaks across all spectra, using specified noise estimation and peak filtering parameters"
- [other] Filter peaks according to quality criteria (e.g., frequency threshold, signal-to-noise ratio): "Filter peaks according to quality criteria (e.g., frequency threshold, signal-to-noise ratio)"
- [intro] New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering, Continuous wavelet transform (CWT): "New peak picking methods in peakPick(): Derivative-based noise estimation, Quantile-based noise estimation, SD/MAD-based noise estimatino, Dynamic peak filtering"
- [intro] Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [intro] Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
