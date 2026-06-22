---
name: s4-class-definition-and-inheritance
description: Use when you are designing a new backend or data container that must integrate seamlessly with an existing Spectra-based workflow. You have identified a virtual parent class (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3365
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - S4Vectors
  - R
  - Spectra
  - IRanges
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`
- library(Spectra) library(IRanges)
- library(Spectra)
- '`DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)'
- DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectra
    doi: 10.3390/metabo12020173
    title: spectra
  - build: coll_spectra_cq
    doi: 10.3390/metabo12020173
    title: spectra
  dedup_kept_from: coll_spectra
schema_version: 0.2.0
---

# S4 Class Definition and Inheritance

## Summary

Define custom S4 classes that extend virtual parent classes and implement required slots and methods to create domain-specific data structures. This skill is essential when building extensible bioinformatics infrastructure where multiple implementations need to conform to a common API contract.

## When to use

You are designing a new backend or data container that must integrate seamlessly with an existing Spectra-based workflow. You have identified a virtual parent class (e.g., MsBackend) that defines the API, and you need to create a concrete implementation with specific data representation choices (e.g., in-memory NumericList storage for peaks, data.frame for metadata).

## When NOT to use

- You are reading from an existing data source (file, database) where a backend already exists (e.g., MsBackendMzR for mzML files, MsBackendSql for SQL databases) — use the existing backend instead.
- You only need read-only access to a remote or cached resource — extend MsBackendCached rather than implementing the full MsBackend API.
- Your data fits naturally into a simple in-memory list-of-matrices structure — MsBackendMemory or MsBackendDataFrame may already meet your needs without custom class definition.

## Inputs

- Virtual parent class definition (e.g., MsBackend from Spectra package)
- Data representation design specification (slot names, types, structure)
- Sample mass spectrometry data (m/z, intensity pairs; metadata variables)

## Outputs

- Concrete S4 class extending the virtual parent
- Implemented accessor methods returning typed objects (DataFrame, NumericList, character vectors)
- Implemented data replacement methods for write-capable backends
- Functional backend instance ready for integration into Spectra workflows

## How to apply

First, identify the virtual parent class and its required methods by consulting the API documentation. Define your S4 class using setClass() with explicit slots that match your data model (e.g., spectraVars as data.frame, mz and intensity as NumericList). Implement all required accessor methods (spectraData, spectraVariables, peaksData, extractByIndex, backendMerge, intensity, mz, spectraNames) and initialization method (backendInitialize) with signatures matching the parent contract. For read-write backends, also implement replacement methods (intensity<-, mz<-, spectraData<-, etc.). Ensure m/z values within each spectrum are sorted increasingly and that core variables (dataStorage, dataOrigin) are always provided. Validate the implementation by instantiating the class, populating it with test data via backendInitialize(), and confirming all accessor methods return expected types and shapes.

## Related tools

- **Spectra** (Provides the virtual MsBackend class definition and integration framework that your custom S4 class must extend and implement) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame and NumericList data structures used as return types in spectraData() and peaks accessor methods)
- **IRanges** (Companion infrastructure package for S4 class and method system integration)

## Examples

```
setClass('MsBackendTest', contains='MsBackend', slots=c(spectraVars='data.frame', mz='NumericList', intensity='NumericList')); setMethod('spectraData', 'MsBackendTest', function(object) { cbind(object@spectraVars, mz=object@mz, intensity=object@intensity) })
```

## Evaluation signals

- All required accessor methods (spectraData, spectraVariables, backendInitialize, peaksData, extractByIndex, backendMerge, intensity, mz, spectraNames) are implemented with correct signatures and return types (DataFrame, character, NumericList, integer-indexed subsets).
- backendInitialize() successfully populates slots with test data and subsequent spectraData() returns a complete DataFrame with all variables and matching row count.
- intensity() and mz() return NumericList objects with length equal to spectrum count, where each element is a numeric vector with increasing m/z values.
- extractByIndex(backend, c(1,3,5)) returns a valid instance with 3 spectra and consistent internal structure (spectraVars nrow equals length of mz/intensity lists).
- Data replacement methods (intensity<-, mz<-) update slots without breaking invariants: m/z remains sorted and list lengths remain synchronized with spectraVars row count.

## Limitations

- M/z values within each spectrum are expected to be sorted increasingly — unsorted input data must be preprocessed or will violate API contracts.
- The MsBackend API is read-only-capable; backends extending MsBackendCached avoid implementing expensive replacement methods, meaning write-capable backends incur full implementation cost.
- merging (backendMerge()) two instances of different MsBackend classes is not supported — only same-type backends can be combined.

## Evidence

- [intro] S4 class extension definition: "To create a new backend a class extending the virtual `MsBackend` needs to be implemented."
- [intro] Slot structure for in-memory backend: "slots = c( spectraVars = "data.frame", mz = "NumericList", intensity = "NumericList" )"
- [intro] spectraData() return type requirement: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] Required accessor methods enumeration: "MsBackendTest requires implementation of 9 required accessor methods (spectraData, spectraVariables, backendInitialize, peaksData, extractByIndex, backendMerge, intensity, mz, spectraNames)"
- [intro] M/z sorting invariant: "m/z values within each spectrum are expected to be sorted increasingly."
- [intro] Core variables requirement: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [intro] Read-only backend option: "`MsBackend` implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods."
- [intro] peaksData() extraction method: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum."
