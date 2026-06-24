---
name: spectra-data-extraction-and-subsetting
description: Use when when you need to extract m/z and intensity peak values from
  a Spectra object backed by MsBackendMzR or similar on-disk backends; when analyzing
  subsets of spectra without loading all peaks into memory;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Spectra
  - MsBackendMzR
  - R
  - S4Vectors
  - mzR
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- The *Spectra* package defines an efficient infrastructure for storing and handling
  mass spectrometry spectra
- Backends such as the `MsBackendMzR` for example retrieve the data on the fly from
  the raw MS data files
- library(Spectra) library(IRanges)
- library(Spectra)
- return the **full** spectra data within a backend as a `DataFrame` object (defined
  in the `r Biocpkg("S4Vectors")`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectra
    doi: 10.3390/metabo12020173
    title: spectra
  dedup_kept_from: coll_spectra
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12020173
  all_source_dois:
  - 10.3390/metabo12020173
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectra-data-extraction-and-subsetting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extraction and subsetting of mass spectrometry spectral data from MsBackend objects using peaksData(), intensity(), mz() accessor methods and extractByIndex() to retrieve peak m/z and intensity values for specified spectra. This skill enables efficient retrieval of peak data in chunk-wise fashion, reducing memory footprint by loading only the required spectra into memory.

## When to use

When you need to extract m/z and intensity peak values from a Spectra object backed by MsBackendMzR or similar on-disk backends; when analyzing subsets of spectra without loading all peaks into memory; when implementing parallel processing workflows that require spectra-by-file or spectra-by-chunk subsetting via backendParallelFactor().

## When NOT to use

- Input data is already a fully in-memory backend (e.g., MsBackendMemory) where chunk-wise extraction offers no memory advantage
- Analysis requires random access to all spectra simultaneously and sequential chunk iteration is not feasible
- Peak data is already pre-loaded into a feature table or matrix; re-extraction is redundant

## Inputs

- MsBackend object (e.g., MsBackendMzR instance with dataStorage and dataOrigin metadata)
- integer indices or logical vector for subsetting
- factor grouping spectra by chunk (from backendParallelFactor())

## Outputs

- NumericList of m/z values per spectrum
- NumericList of intensity values per spectrum
- list of matrices with m/z and intensity columns (from peaksData())
- subsetted MsBackend object

## How to apply

Call peaksData() on the MsBackend to extract peaks as a list of m/z–intensity matrices; use extractByIndex() or [ ] subsetting to isolate spectra by index before peak extraction; leverage backendParallelFactor() to obtain a grouping factor (e.g., by source file from dataStorage variable) and iterate over chunks, realizing peak data only for the current chunk. This approach keeps only active chunk peaks in memory rather than loading all spectra at initialization, reducing peak-data memory demand proportionally to chunk size relative to total spectra count. Verify that m/z values within each spectrum are sorted increasingly before further processing.

## Related tools

- **Spectra** (High-level S4 class that wraps MsBackend and provides spectra subsetting and accessor interface) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMzR** (On-disk backend that retrieves peak data on-the-fly from mzML/mzXML/CDF files; implements backendParallelFactor() for chunk grouping by source file) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides NumericList and DataFrame classes used to store and return peak and spectra variable data)
- **mzR** (Underlying library used by MsBackendMzR to read raw MS data files)

## Examples

```
library(Spectra); sps <- Spectra(backendInitialize(MsBackendMzR(), files=c('file1.mzML', 'file2.mzML'))); pf <- backendParallelFactor(sps@backend); peaks_chunk1 <- peaksData(sps@backend[which(pf == levels(pf)[1])]);
```

## Evaluation signals

- peaksData() returns a list with length equal to the number of spectra in the subset, and each element is a matrix with two columns (m/z and intensity) of matching length
- m/z values are sorted in increasing order within each spectrum (invariant from article)
- Memory profiling shows peak-data memory footprint proportional to chunk size, not total dataset size
- extractByIndex() or [ ] subsetting produces an MsBackend with spectraVariables() unchanged but fewer rows in dataStorage/dataOrigin
- backendParallelFactor() returns a factor with levels corresponding to unique source file names in dataStorage, enabling reproducible chunk grouping

## Limitations

- backendParallelFactor() depends on consistent and unique dataStorage file-path values; missing or duplicated paths may produce incorrect chunk grouping
- peaksData() requires the underlying data files (mzML, mzXML, CDF) to remain accessible on disk; moving or deleting files breaks on-the-fly retrieval
- Chunk-wise extraction incurs repeated I/O overhead if the same chunks are accessed multiple times without caching; in-memory backends may be preferable for repeated random access
- Read-only backends (e.g., MsBackendMzR) do not support data replacement methods, limiting in-place modification of peaks during subsetting

## Evidence

- [other] MsBackendMzR's backendParallelFactor() enables chunk-wise splitting: "MsBackendMzR's backendParallelFactor() returns a factor based on dataStorage file names to split the backend for parallel or serial processing."
- [other] Chunk-wise processing reduces memory demand: "Chunk-wise processing via this splitting reduces memory demand because only the peak data of the current chunk—not all spectra—needs to be realized in memory during operations."
- [intro] peaksData() method purpose and return type: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum."
- [intro] m/z sorting requirement: "m/z values within each spectrum are expected to be sorted increasingly."
- [intro] extractByIndex() method for subsetting: "The `extractByIndex()` and `[` methods allows to subset `MsBackend` objects."
- [intro] Backends retrieve data on-the-fly: "Backends such as the `MsBackendMzR` for example retrieve the data on the fly from the raw MS data files"
- [readme] MsBackendMzR retrieves peaks on-the-fly from raw files: "`MsBackendMzR` (package: *Spectra*): by using the `mzR` package it supports import of MS data from mzML, mzXML and CDF files. This backend keeps only general spectra variables in memory and retrieves"
