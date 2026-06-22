---
name: msi-imaging-experiment-class-manipulation
description: Use when when loading mass spectrometry imaging data from imzML or Analyze 7.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Cardinal
  - BiocParallel
  - R
  - CardinalIO
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

# msi-imaging-experiment-class-manipulation

## Summary

Construct and manipulate Cardinal's redesigned MSImagingArrays and MSImagingExperiment class hierarchy to represent raw spectra and processed imaging data with support for out-of-memory datasets. This skill bridges raw spectral input to statistical analysis by selecting the appropriate imaging class and applying queued preprocessing operations.

## When to use

When loading mass spectrometry imaging data from imzML or Analyze 7.5 formats and deciding whether to work with raw spectra (MSImagingArrays) or fully processed experiment objects (MSImagingExperiment), especially when the dataset is too large to fit in memory or when preprocessing steps need to be queued and executed in parallel.

## When NOT to use

- Data is already in peak-intensity matrix format (feature table); use readMSIData() first to preserve spectral structure.
- Analysis requires only univariate statistics on pre-extracted features; the class hierarchy overhead is unnecessary for tabular feature data.
- Dataset fits comfortably in memory and parallelization is not a concern; simpler in-memory objects may suffice.

## Inputs

- imzML file (continuous or processed format)
- Analyze 7.5 format file
- MSImagingArrays object (raw spectra with queued operations)

## Outputs

- MSImagingArrays object (raw spectra, out-of-memory capable)
- MSImagingExperiment object (processed spectra with reference peaks and metadata)
- SpectralImagingData or SpectralImagingArrays (base classes in redesigned hierarchy)

## How to apply

Load imzML or Analyze 7.5 data using readMSIData(), which returns an MSImagingArrays object for raw spectra. Apply a sequence of preprocessing operations—normalize(), smooth(), reduceBaseline(), recalibrate(), and peakPick()—which queue transformations on the MSImagingArrays without immediate evaluation. These queued operations are executed lazily and can be parallelized via the BPPARAM option in BiocParallel. The result is coerced to an MSImagingExperiment object, which consolidates the processed spectra, reference peak table, and imaging metadata. Choose MSImagingArrays for memory-efficient access to raw spectra; use MSImagingExperiment for statistical analysis, imaging visualization, and downstream modeling (e.g., PCA, clustering). Verify class integrity by inspecting the object's featureNames (m/z values), pixelNames (spatial coordinates), and metadata slots.

## Related tools

- **Cardinal** (Core package providing redesigned class hierarchy (SpectralImagingData, MSImagingArrays, MSImagingExperiment), readMSIData() import, preprocessing methods (normalize, smooth, reduceBaseline, recalibrate, peakPick), and lazy evaluation of queued operations) — https://github.com/kuwisdelu/Cardinal
- **BiocParallel** (Enables parallel execution of queued preprocessing operations across spectra via BPPARAM option)
- **CardinalIO** (Provides example imzML files for development and testing)
- **matter** (Low-level signal processing backend for Cardinal 3.6+ (versions 2.4 and 2.6))

## Examples

```
library(Cardinal); path_continuous <- CardinalIO::exampleImzMLFile('continuous'); msi_data <- readMSIData(path_continuous); msi_proc <- normalize(msi_data, method='tic') %>% smooth(method='gaussian') %>% reduceBaseline(method='snip') %>% peakPick(method='derivative'); msi_exp <- as(msi_proc, 'MSImagingExperiment')
```

## Evaluation signals

- Object class is confirmed as MSImagingArrays or MSImagingExperiment using class() or is() function.
- featureNames slot contains valid m/z values sorted in increasing order; pixelNames slot contains spatial coordinates matching the imaging array dimensions.
- Queued preprocessing operations are listed in the object's processing history or metadata without errors; lazy evaluation completes without data loss when operations are forced.
- Reference peak table (if peakProcess applied) contains expected number of aligned peaks with frequency ≥ SNR threshold and consistent summarization across all spectra.
- Parallel execution with BPPARAM completes faster than sequential execution; output dimensions (features × pixels) remain consistent before and after preprocessing.

## Limitations

- Cardinal 3.6 includes breaking changes; existing code written for Cardinal 2.x may require refactoring to work with the new class hierarchy.
- Out-of-memory support requires adequate storage and I/O bandwidth; very large imzML files may be slow to load or process even with lazy evaluation.
- Queued operations are applied in order; some combinations of preprocessing (e.g., smoothing before baseline reduction) may alter results compared to different orderings.
- Writing imzML output is now supported, but conversion between 'continuous' and 'processed' imzML formats may lose or alter metadata depending on the target format.

## Evidence

- [intro] Cardinal 3.6 redesigned class hierarchy emphasis: "Redesign class hierarchy that includes a greater emphasis on spectra: SpectralImagingData, SpectralImagingArrays, and SpectralImagingExperiment lay the groundwork for the new data structures"
- [intro] MSImagingArrays for raw spectra representation: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [intro] Out-of-memory dataset support: "New imaging experiment classes such as ImagingExperiment, SparseImagingExperiment, and MSImagingExperiment provide better support for out-of-memory datasets"
- [intro] readMSIData import function: "Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions"
- [intro] Parallel preprocessing via BiocParallel: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
