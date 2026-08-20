---
name: bioconductor-backend-architecture-design
description: 'Use when you are building a new mass spectrometry data backend or storage layer and need to integrate it with the Spectra ecosystem. Triggers include: (1) you have a novel data source (raw files, databases, web APIs) that should be accessible through Spectra objects;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - R
  - S4Vectors
  - Spectra
  - mzR
  - CompoundDb
  - MsBackendMgf
  - MsBackendMsp
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- library(Spectra) library(IRanges)
- '`DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)'
- DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectra_cq
    doi: 10.3390/metabo12020173
    title: spectra
  dedup_kept_from: coll_spectra_cq
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

# bioconductor-backend-architecture-design

## Summary

Design and implement a modular MsBackend subclass that separates MS data representation from analysis logic, enabling pluggable storage strategies (in-memory, on-disk, SQL, HDF5) while maintaining a unified Spectra API. This architecture allows analysis code to remain agnostic to data provenance and storage format.

## When to use

You are building a new mass spectrometry data backend or storage layer and need to integrate it with the Spectra ecosystem. Triggers include: (1) you have a novel data source (raw files, databases, web APIs) that should be accessible through Spectra objects; (2) you need to optimize for a specific memory/speed tradeoff (e.g., large datasets requiring on-disk storage or cached retrieval); (3) you want to support read-only or partially writable access to MS data without reimplementing analysis code.

## When NOT to use

- You are analyzing pre-existing Spectra objects and do not need to implement storage; use existing backends (MsBackendMemory, MsBackendMzR, etc.) instead.
- Your data source does not fit the MsBackend API (e.g., single-spectrum analysis tools, non-peak-based MS data); consider wrapping it at the Spectra analysis layer instead.
- You need real-time modification of massive peak datasets; partially read-only backends like MsBackendMzR may be more appropriate than full writable implementations with peak-count constraints.

## Inputs

- Virtual MsBackend class definition (S4)
- MS data source (raw files, database connection, in-memory table, or API endpoint)
- Spectra variable schema (core and optional properties)
- Peak data (m/z values and intensity values per spectrum)

## Outputs

- Concrete MsBackend subclass (S4 class extending MsBackend)
- Implemented accessor methods (spectraData, spectraVariables, peaksData, mz, intensity, spectraNames, extractByIndex)
- Optional: replacement methods ($<-, [<-, peaksData<-) for writable backends
- Optional: backendMerge() method for combining instances
- Tested backend instance compatible with Spectra objects

## How to apply

Create an S4 class extending the virtual MsBackend, then implement the required accessor methods: spectraVariables() returning a character vector of available spectra properties, spectraData() returning a DataFrame with m/z and intensity as NumericList objects, peaksData() extracting m/z–intensity matrices, and intensity()/mz() returning NumericList columns in increasing m/z order per spectrum. For writable backends, implement replacement methods ($<-, [<-, peaksData<-) with four constraint layers: length matching via .match_length() ensuring replacement vectors equal spectrum count, data type validation (e.g., NumericList for m/z/intensity), peak-count preservation maintaining peaks per spectrum, and m/z ordering validation using is.unsorted() to verify increasing sort. Initialize the backend with backendInitialize(), set dataStorage and dataOrigin for each spectrum, and implement extractByIndex() for subsetting and backendMerge() for combining backends. The design decouples analysis (Spectra class) from data provision (MsBackend implementations), allowing backends to use heterogeneous storage (in-memory DataFrames, HDF5 files, SQL databases, lazy file retrieval via mzR) while preserving a single analysis interface.

## Related tools

- **Spectra** (Virtual MsBackend class, analysis interface, and concrete backends (MsBackendMemory, MsBackendMzR, MsBackendDataFrame, MsBackendHdf5Peaks)) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame and NumericList classes for structured spectra data and m/z/intensity storage)
- **mzR** (File I/O layer for lazy retrieval of peaks data from mzML/mzXML/CDF files in MsBackendMzR)
- **CompoundDb** (Example backend (MsBackendCompDb) retrieving spectra on-the-fly from a database) — https://github.com/rformassspectrometry/CompoundDb
- **MsBackendMgf** (Example backend extending MsBackendDataFrame for import/export in mascot generic format) — https://github.com/rformassspectrometry/MsBackendMgf
- **MsBackendMsp** (Example backend extending MsBackendDataFrame for NIST MSP format) — https://github.com/rformassspectrometry/MsBackendMsp

## Examples

```
setClass("MyMsBackend", contains="MsBackend", slots=c(data="DataFrame", peaks="list")); setMethod("spectraVariables", "MyMsBackend", function(object) colnames(object@data)); setMethod("peaksData", "MyMsBackend", function(object, columns=c("mz","intensity")) mapply(cbind, mz=object@peaks[[1]], intensity=object@peaks[[2]])); b <- new("MyMsBackend", data=data.frame(...), peaks=list(mz=..., intensity=...)); sps <- Spectra(b)
```

## Evaluation signals

- All core spectra variables (mz, intensity, precursorMz, collisionEnergy, retentionTime, acquisitionNum, etc.) are returned by spectraVariables() and accessible via spectraData()
- peaksData() returns a list of two-column numeric matrices with m/z in column 1 and intensity in column 2; m/z values are sorted increasingly within each spectrum and contain no NA values
- extractByIndex() reduces the backend to the selected spectra without data loss; length and peak counts are preserved
- For writable backends: replacement method constraints are enforced (e.g., mz<- rejects vectors with length ≠ number of spectra, rejects unsorted m/z values, rejects NA entries; peaksData<- preserves peak counts per spectrum)
- A Spectra object instantiated with the new backend executes analysis code without modification, confirming backend transparency

## Limitations

- m/z values within each spectrum must be sorted in increasing order and may not contain NA values; backends enforcing this constraint will reject invalid data during replacement
- Peak-count preservation is mandatory for writable backends: replacement of peaksData must maintain the same number of peaks per spectrum, preventing data truncation or expansion
- Backends extending MsBackendCached (read-only) do not support data replacement methods; only full writable backends like MsBackendMemory or MsBackendDataFrame can implement $<- and [<- methods
- Parallel processing via backendParallelFactor() requires backends to suggest appropriate splitting factors; lazy-loading backends (MsBackendMzR) may have different parallelization constraints than in-memory backends

## Evidence

- [intro] The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object.: "The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object."
- [intro] The `Spectra` package separates the code for the analysis of MS data from the code needed to import, represent and provide the data.: "The `Spectra` package separates the code for the analysis of MS data from the code needed to import, represent and provide the data."
- [other] Replacement methods for writable backends enforce four key constraints: (1) length matching via .match_length() to ensure value length equals spectrum count, (2) data type validation checking that m/z and intensity are NumericList objects, (3) peak-count preservation requiring that replacement values maintain the same number of peaks per spectrum, and (4) m/z ordering validation using is.unsorted() to verify m/z values are increasingly sorted within each spectrum.: "Replacement methods for writable backends enforce four key constraints: (1) length matching via `.match_length()` to ensure value length equals spectrum count, (2) data type validation checking that"
- [intro] m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported.: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [intro] To create a new backend a class extending the virtual `MsBackend` needs to be implemented. In the example below we create thus a simple class with a `data.frame` to contain general spectral properties: "To create a new backend a class extending the virtual `MsBackend` needs to be implemented. In the example below we create thus a simple class with a `data.frame` to contain general spectral properties"
- [intro] `MsBackend` implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods.: "`MsBackend` implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods."
- [intro] The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] Backends such as the `MsBackendMzR` for example retrieve the data on the fly from the raw MS data files: "Backends such as the `MsBackendMzR` for example retrieve the data on the fly from the raw MS data files"
- [readme] *Spectra* provides different implementations (backends) to store mass spectrometry data. These comprise backends tuned for fast data access and processing and backends for very large data sets ensuring a small memory footprint.: "*Spectra* provides different implementations (backends) to store mass spectrometry data. These comprise backends tuned for fast data access and processing and backends for very large data sets"
