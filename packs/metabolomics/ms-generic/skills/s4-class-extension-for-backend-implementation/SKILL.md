---
name: s4-class-extension-for-backend-implementation
description: Use when you are building a new data representation or storage strategy for MS spectra (e.g., on-disk HDF5, SQL database, remote file access) and need to integrate it seamlessly into workflows that use the Spectra package.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MsBackendMzR
  - R
  - S4Vectors
  - Spectra
  - IRanges
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- Backends such as the `MsBackendMzR` for example retrieve the data on the fly from the raw MS data files
- library(Spectra) library(IRanges)
- library(Spectra)
- return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# s4-class-extension-for-backend-implementation

## Summary

Design and implement a custom S4 class that extends the MsBackend virtual class to define a new backend representation for mass spectrometry data. This skill enables integration of alternative data storage strategies (e.g., on-disk, database, memory) into the Spectra ecosystem while decoupling data representation from analysis code.

## When to use

You are building a new data representation or storage strategy for MS spectra (e.g., on-disk HDF5, SQL database, remote file access) and need to integrate it seamlessly into workflows that use the Spectra package. Use this when existing backends (MsBackendMemory, MsBackendMzR, MsBackendSql) do not match your storage constraints or data access patterns.

## When NOT to use

- Your data already fits comfortably in memory and speed is the priority; use MsBackendMemory instead.
- You are importing MS data from a standard format (mzML, mzXML, CDF) with no custom access pattern; MsBackendMzR is sufficient.
- You only need to read-only access a SQL database without custom filtering or transformation; MsBackendSql or MsBackendMassbankSql are designed for this.

## Inputs

- Raw MS data files (mzML, mzXML, CDF, or custom formats)
- Metadata defining spectra variables (e.g., precursor m/z, retention time, scan number)
- Peak data source (m/z and intensity pairs per spectrum)

## Outputs

- Custom MsBackend S4 class instance with fully implemented required methods
- Spectra object linked to the custom backend via @backend slot
- Memory profile and chunk-wise processing benchmark results

## How to apply

Create an S4 class that extends the MsBackend virtual class and define slots for spectra variables (as a DataFrame or data.frame) and peak data (m/z and intensity as NumericList or equivalent). Implement the required methods: backendInitialize() to load and prepare MS data from your source (e.g., raw files via MsBackendMzR, databases, or custom formats); spectraData() and spectraVariables() to expose all available metadata; peaksData(), intensity(), and mz() accessor methods to extract peak values; extractByIndex() and [ for subsetting; and backendMerge() for combining multiple instances. Ensure m/z values are sorted increasingly within each spectrum. For parallel processing efficiency, implement backendParallelFactor() to return a factor (typically based on dataStorage file paths) that enables chunk-wise processing rather than loading all peaks into memory. Test memory usage during chunk-wise versus whole-load scenarios to validate the overhead reduction.

## Related tools

- **Spectra** (Provides the MsBackend virtual class, Spectra container, and integration framework for backends) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMzR** (Reference backend implementation for on-disk peak data retrieval from mzML/mzXML/CDF; used as data source during backendInitialize()) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame and NumericList classes for storing spectra variables and peak data in backend slots) — https://bioconductor.org/packages/release/bioc/html/S4Vectors.html
- **IRanges** (Complementary S4 infrastructure for range-based data manipulation in backend implementation)

## Examples

```
setClass('MyMsBackend', contains='MsBackend', slots=c(spectraVars='data.frame', mz='NumericList', intensity='NumericList')); setMethod('backendInitialize', 'MyMsBackend', function(object, x, ...) { b <- backendInitialize(MsBackendMzR(), x); object@spectraVars <- spectraData(b); object@mz <- mz(b); object@intensity <- intensity(b); object }); sps <- Spectra(backendInitialize(new('MyMsBackend'), 'data.mzML'))
```

## Evaluation signals

- All required MsBackend virtual methods are implemented and do not raise 'not implemented' errors when called on a Spectra object using your backend.
- peaksData() returns a list of matrices with m/z and intensity columns; row count per matrix matches the number of peaks in each spectrum.
- m/z values within each spectrum are sorted in increasing order (verifiable via lapply(peaksData(backend), function(x) is.unsorted(x[, 'mz'])) should return all FALSE).
- backendParallelFactor() returns a factor with length equal to the number of spectra, grouping spectra by dataStorage file path.
- Chunk-wise processing (using backendParallelFactor() to subset via extractByIndex()) consumes measurably less peak memory than loading all spectra peaksData() at once; memory reduction ≥ 20% for moderately sized datasets is typical.

## Limitations

- The virtual MsBackend class requires implementation of all accessor and manipulation methods; partial implementations will fail when workflows attempt data access patterns you did not implement.
- Chunk-wise memory advantage only manifests if your backend does lazy loading of peak data; eagerly loading all peaks during backendInitialize() negates the memory benefit.
- Parallel processing via backendParallelFactor() assumes spectra are logically grouped by dataStorage (file path); custom grouping strategies require overriding this method.
- Read-only backends (those extending MsBackendCached) need not implement data replacement methods, but analysis workflows expecting mutable backends will fail silently or with cryptic errors if mutations are attempted.

## Evidence

- [intro] To create a new backend a class extending the virtual `MsBackend` needs to be implemented.: "To create a new backend a class extending the virtual `MsBackend` needs to be implemented."
- [intro] Each `Spectra` object contains an implementation of such a `MsBackend` within its `@backend` slot which provides the MS data to the `Spectra` object.: "Each `Spectra` object contains an implementation of such a `MsBackend` within its `@backend` slot which provides the MS data to the `Spectra` object."
- [intro] The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object.: "The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object."
- [intro] this separation allows to define new, alternative, data representations and integrate them seamlessly into a `Spectra`-based data analysis workflow.: "this separation allows to define new, alternative, data representations and integrate them seamlessly into a `Spectra`-based data analysis workflow."
- [intro] The `backendInitialize()` method is expected to be called after creating an instance of the backend class and should prepare (initialize) the backend: "The `backendInitialize()` method is expected to be called after creating an instance of the backend class and should prepare (initialize) the backend"
- [other] MsBackendMzR's backendParallelFactor() returns a factor based on dataStorage file names to split the backend for parallel or serial processing. Chunk-wise processing via this splitting reduces memory demand because only the peak data of the current chunk—not all spectra—needs to be realized in memory during operations.: "MsBackendMzR's backendParallelFactor() returns a factor based on dataStorage file names to split the backend for parallel or serial processing. Chunk-wise processing via this splitting reduces memory"
- [intro] `dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [intro] The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum.: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum."
- [intro] m/z values within each spectrum are expected to be sorted increasingly.: "m/z values within each spectrum are expected to be sorted increasingly."
- [intro] Backends such as the `MsBackendMzR` for example retrieve the data on the fly from the raw MS data files: "Backends such as the `MsBackendMzR` for example retrieve the data on the fly from the raw MS data files"
- [readme] *Spectra* provides different implementations (backends) to store mass spectrometry data. These comprise backends tuned for fast data access and processing and backends for very large data sets ensuring a small memory footprint.: "*Spectra* provides different implementations (backends) to store mass spectrometry data. These comprise backends tuned for fast data access and processing and backends for very large data sets"
