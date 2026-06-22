---
name: msbackend-api-implementation
description: Use when you need to create a new backend to integrate MS data from a novel file format, database, or in-memory storage system into the Spectra ecosystem. Use this skill when existing backends (MsBackendMemory, MsBackendMzR, MsBackendSql, etc.) do not support your data source or storage paradigm.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - S4Vectors
  - MSnbase
  - Spectra
  - MsBackendMemory
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- library(Spectra) library(IRanges)
- '`DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)'
- DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)
- extension of the of *in-memory* and *on-disk* data representations from the `r Biocpkg("MSnbase")` package
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

# msbackend-api-implementation

## Summary

Implement a custom MsBackend subclass that extends the virtual MsBackend API to store and provide mass spectrometry spectral data (m/z, intensity, and metadata) to Spectra objects. This skill involves designing S4 class slots, enforcing data consistency through validity methods, and implementing core accessor and data-manipulation methods.

## When to use

You need to create a new backend to integrate MS data from a novel file format, database, or in-memory storage system into the Spectra ecosystem. Use this skill when existing backends (MsBackendMemory, MsBackendMzR, MsBackendSql, etc.) do not support your data source or storage paradigm.

## When NOT to use

- Your data source is already supported by an existing backend (e.g., mzML files via MsBackendMzR, SQL databases via MsBackendSql, in-memory matrices via MsBackendMemory).
- You only need to analyze pre-loaded Spectra objects without defining new storage or access patterns.
- Your m/z values are not sorted increasingly or contain NA values per spectrum, as these violate MsBackend core requirements.

## Inputs

- S4 class definition extending MsBackend
- data.frame containing spectra variables (e.g., retention time, precursor m/z, scan index)
- list or NumericList of m/z values (sorted increasingly per spectrum)
- list or NumericList of intensity values (parallel to m/z)
- optional: complete DataFrame containing both variables and peak data

## Outputs

- MsBackend subclass instance with populated slots
- DataFrame returned by spectraData() with core and backend-specific columns
- NumericList returned by mz() and intensity()
- list of numerical matrices (m/z and intensity columns) from peaksData()
- extracted or merged MsBackend objects from extractByIndex() and backendMerge()

## How to apply

Define an S4 class extending MsBackend with slots for spectra variables (data.frame) and peak data (NumericList for m/z and intensity). Implement a setValidity method enforcing that spectraVars row count matches m/z and intensity list lengths, with m/z values sorted increasingly and free of NA. Implement backendInitialize() to populate slots from input data (data.frame, lists, or complete DataFrame), automatically setting dataStorage and dataOrigin variables. Implement accessor methods (spectraVariables(), spectraData(), peaksData(), mz(), intensity()) that return core variables combined with backend-specific columns; use fillCoreSpectraVariables() to avoid circular dependencies. Implement data manipulation methods (extractByIndex(), backendMerge()) to subset and combine backends; for peaksData() efficiency, consider storing peak data as pre-assembled matrices rather than separate lists.

## Related tools

- **Spectra** (defines the virtual MsBackend class API and Spectra object that uses backend implementations; provides fillCoreSpectraVariables() helper and S4 class infrastructure) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (provides DataFrame and NumericList classes for storing spectra variables and peak data)
- **MsBackendMemory** (reference implementation storing peak data as list of matrices, demonstrating efficient peaksData() pattern) — https://github.com/RforMassSpectrometry/Spectra
- **MSnbase** (predecessor package; Spectra extends in-memory and on-disk representations originally defined here)

## Examples

```
setClass("MsBackendTest", contains="MsBackend", slots=c(spectraVars="data.frame", mz="NumericList", intensity="NumericList")); setValidity("MsBackendTest", function(object) { if(nrow(object@spectraVars) != length(object@mz)) return("spectraVars rows must match mz length"); TRUE }); setMethod("backendInitialize", "MsBackendTest", function(object, ...) { object@spectraVars <- data.frame(...); object@mz <- as(list(...), "NumericList"); object@intensity <- as(list(...), "NumericList"); object })
```

## Evaluation signals

- Validity checks reject objects where spectraVars row count does not match mz and intensity list lengths
- spectraVariables() returns character vector containing union of core names (mz, intensity, rtime, scanIndex) and backend-specific column names without duplicates
- spectraData() returns a DataFrame with m/z and intensity as NumericList columns; does not call spectraVariables()
- peaksData() returns list of numerical matrices with correct dimensionality (one matrix per spectrum, two columns: m/z and intensity)
- extractByIndex() and backendMerge() preserve peak data ordering and allow spectrum duplication; no data is lost during merge

## Limitations

- m/z values must be sorted increasingly with no missing (NA) values per spectrum; backends cannot relax this constraint
- Backends storing peak data in separate m/z and intensity slots require looping to assemble matrices in peaksData(), incurring performance overhead compared to pre-stored matrix storage (e.g., MsBackendMemory pattern)
- Read-only backends must implement only accessor methods but not data replacement methods; partially read-only backends (like MsBackendMzR) may allow spectra variable modification but prevent peak data changes
- Circular dependencies between spectraData() and spectraVariables() must be avoided; use fillCoreSpectraVariables() in spectraData() and populate spectraVariables() only from backend column names

## Evidence

- [intro] MsBackend virtual class defines API; S4 class with data.frame and NumericList slots: "The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object."
- [intro] spectraData must return full data as DataFrame; spectraVariables must return available variable names: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] m/z values sorted increasingly; NA not supported: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [intro] backendInitialize prepares backend after instantiation: "The `backendInitialize()` method is expected to be called after creating an instance of the backend class and should prepare (initialize) the backend"
- [intro] peaksData returns list of matrices; extractByIndex subsets; backendMerge combines: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum"
- [intro] MsBackendMemory stores data as list of matrices for efficient peaksData: "The `MsBackendMemory` backend for example stores the MS data already as a `list` of matrices"
