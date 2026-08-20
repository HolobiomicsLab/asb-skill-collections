---
name: msi-array-data-structure-handling
description: Use when you have imported raw imzML or Analyze 7.5 imaging data and need to represent it as a preprocessed spectral array before applying statistical methods (PCA, clustering, classification).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Cardinal
  - BiocParallel
  - R
  - Cardinal 3.6
  - matter 2.4 and 2.6
  - CardinalIO
  - BiocManager
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MSI Array Data Structure Handling

## Summary

Load, represent, and manipulate mass spectrometry imaging (MSI) spectra using Cardinal's redesigned MSImagingArrays class, which provides efficient in-memory and out-of-memory handling of raw spectral data with support for preprocessing pipelines. This skill bridges data import and statistical analysis by maintaining spectral integrity through normalization, smoothing, baseline reduction, and peak picking workflows.

## When to use

Use this skill when you have imported raw imzML or Analyze 7.5 imaging data and need to represent it as a preprocessed spectral array before applying statistical methods (PCA, clustering, classification). Specifically, choose MSImagingArrays when working with raw or lightly processed spectra that require coordinated application of multiple signal-processing steps (normalize → smooth → reduceBaseline → peakPick); avoid MSImagingExperiment for this initial structuring unless you are already integrating experimental metadata and sample annotations.

## When NOT to use

- Data is already in feature-table form (e.g., presence/absence of known m/z peaks) — use MSImagingExperiment or statistical methods directly instead.
- You need to integrate sample-level metadata, phenotypes, or experimental design — use MSImagingExperiment class which adds ExpressionSet-like annotation slots.
- Working with already-picked peak lists from external software; MSImagingArrays is designed for raw or baseline-corrected spectra, not summarized ion images.

## Inputs

- MSImagingArrays object (newly instantiated or converted from readMSIData() output)
- imzML or Analyze 7.5 raw imaging file
- Raw or minimally processed spectral data in continuous or processed format

## Outputs

- Preprocessed MSImagingArrays object with queued or executed normalization, smoothing, baseline reduction, and peak picking
- Picked-peaks spectrum (output of peakPick() workflow)
- Normalized and smoothed spectra (output of normalize() and smooth() workflows)

## How to apply

After importing raw data with readMSIData(), instantiate or convert to an MSImagingArrays object. Queue preprocessing methods in sequence using the signature peakPick(object, method=..., SNR=threshold) and similar functions for normalize(), smooth(), reduceBaseline(), and recalibrate(). For derivative-based peak picking specifically, set method='diff' and SNR threshold (e.g., 3) to estimate signal-to-noise from rolling-average deviations of the spectrum derivative, then execute the full pipeline via processing functions that apply all queued steps to all spectra. Enable parallel execution via the BPPARAM option with BiocParallel if the imaging array is large. Extract the resulting picked-peaks spectrum or normalized/smoothed spectrum as the output for downstream analysis.

## Related tools

- **Cardinal 3.6** (Primary package providing MSImagingArrays class, readMSIData(), normalize(), smooth(), reduceBaseline(), recalibrate(), peakPick(), and image contrast/spatial smoothing methods) — github.com/kuwisdelu/Cardinal
- **matter 2.4 and 2.6** (Low-level signal processing functions underlying Cardinal's spectral preprocessing methods)
- **BiocParallel** (Enables parallel processing across spectra via BPPARAM option in preprocessing and statistical analysis methods)
- **CardinalIO** (Provides example imzML files and additional I/O utilities for reading continuous and processed imzML formats)
- **BiocManager** (Installation and dependency management for Cardinal and related Bioconductor packages)

## Examples

```
msi_array <- readMSIData('continuous.imzML'); msi_array <- normalize(msi_array, method='tic'); msi_array <- smooth(msi_array, method='gaussian'); msi_array <- reduceBaseline(msi_array, method='snip'); msi_array <- peakPick(msi_array, method='diff', SNR=3, BPPARAM=BiocParallel::bpparam())
```

## Evaluation signals

- MSImagingArrays object is successfully instantiated and contains metadata (number of pixels, m/z values, spectral dimensions) matching the input imzML or Analyze file.
- Queued preprocessing steps (normalize, smooth, reduceBaseline, peakPick) can be inspected via the object's processing history or queue without errors.
- After execution, normalized spectra have consistent per-spectrum sums or RMS values (depending on normalize method: TIC, RMS, or reference feature); smoothed spectra show reduced noise without loss of peak shape; baseline-reduced spectra have near-zero intensity at low m/z regions.
- Peak picking with method='diff' and SNR=3 produces a spectrum with detected peaks that exceed the SNR threshold when compared to rolling-average derivative noise estimate; number and location of peaks are consistent across replicates or known standards.
- Processed MSImagingArrays object can be successfully passed to downstream statistical methods (spatialKMeans, spatialShrunkenCentroids, PCA, NMF) without reformatting.

## Limitations

- Cardinal 3.6 introduced breaking changes to the class hierarchy; code written for Cardinal 3.5 or earlier may not be compatible without updates to MSImagingArrays instantiation and method calls.
- Parallel processing via BiocParallel assumes sufficient memory for distributing spectra across worker processes; very large imaging arrays may require incremental or disk-backed processing strategies not detailed in the provided context.
- Peak picking with method='diff' and SNR threshold assumes Gaussian-like noise distribution around local baselines; performance may degrade on spectra with non-Gaussian noise, weak SNR globally, or dense peak clusters.
- The article does not provide explicit guidance on how to validate or tune SNR thresholds for specific instrument types or sample matrices; practitioners must use domain knowledge or cross-validation.

## Evidence

- [intro] Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [intro] Redesigned class hierarchy that includes a greater emphasis on spectra: SpectralImagingData, SpectralImagingArrays, and SpectralImagingExperiment: "Redesign class hierarchy that includes a greater emphasis on spectra: SpectralImagingData, SpectralImagingArrays, and SpectralImagingExperiment lay the groundwork for the new data structures"
- [intro] New imaging experiment classes such as ImagingExperiment, SparseImagingExperiment, and MSImagingExperiment provide better support for out-of-memory datasets: "New imaging experiment classes such as ImagingExperiment, SparseImagingExperiment, and MSImagingExperiment provide better support for out-of-memory datasets"
- [intro] Parallel processing support via the BiocParallel package for all pre-processing methods: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
- [intro] Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions: "Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions"
- [other] peakPick() with method='diff' and SNR=3 estimates signal-to-noise ratio from deviations between the spectrum and a rolling average of its derivative, then detects peaks exceeding the specified SNR threshold: "peakPick() with method='diff' and SNR=3 estimates signal-to-noise ratio from deviations between the spectrum and a rolling average of its derivative, then detects peaks exceeding the specified SNR"
- [readme] Cardinal provides an interface for manipulating mass spectrometry (MS) imaging datasets, simplifying most of the basic programmatic tasks encountered during the statistical analysis of MS imaging data: "Cardinal provides an interface for manipulating mass spectrometry (MS) imaging datasets, simplifying most of the basic programmatic tasks encountered during the statistical analysis of MS imaging data"
