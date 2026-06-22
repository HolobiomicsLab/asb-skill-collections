---
name: s4-class-definition-and-slot-management
description: 'Use when you are extending the MsBackend virtual class to create a new backend for storing MS spectra data and need to define the internal data structure. Specifically: when you have multiple types of spectra variables (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3088
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - S4Vectors
  - R
  - Spectra
  - R (S4 OOP system)
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`
- library(Spectra) library(IRanges)
- library(Spectra)
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

# S4 Class Definition and Slot Management

## Summary

Design and implement S4 classes with typed slots to store heterogeneous MS data structures (spectra variables, peak data, metadata) in a memory-efficient, type-safe manner. This skill is essential when building backend implementations that must enforce data consistency and support polymorphic method dispatch across different MS data representations.

## When to use

You are extending the MsBackend virtual class to create a new backend for storing MS spectra data and need to define the internal data structure. Specifically: when you have multiple types of spectra variables (e.g., numeric msLevel, character polarity, list-like mz and intensity pairs) that must coexist, be validated at instantiation, and support both read-only and read-write access patterns; or when you need type-safe slot accessors to prevent accidental mixing of incompatible data structures (e.g., storing a data.frame where a NumericList is expected).

## When NOT to use

- Your MS data is already stored in a non-structured format (flat CSV) and you need only basic tabular access—use MsBackendDataFrame directly without custom subclassing.
- You are analyzing a small, in-memory dataset and do not need lazy evaluation or on-disk backends—plain data.frames or matrices may suffice without the S4 overhead.
- You are implementing a read-only wrapper around a third-party data source (e.g., SQL database) where you cannot enforce slot invariants at initialization time—consider using MsBackendCached or a delegation pattern instead.

## Inputs

- User-supplied spectra variables (msLevel, rtime, polarity, etc.) as vectors or data.frame columns
- Peak data: m/z and intensity values as list-like structures (NumericList or lists of numeric vectors)
- Metadata: dataStorage (file path) and dataOrigin (data source identifier) as character vectors
- Optional core spectra variables (centroided, isSpectrum, smoothed) provided by user or to be filled with NA

## Outputs

- S4 object instance with typed slots holding spectra variables, peak data, and metadata
- DataFrame with all core spectra variables (including NA-filled missing ones) accessible via spectraData()
- NumericList or list of matrices for m/z and intensity accessible via mz() and intensity() methods

## How to apply

Define an S4 class extending MsBackend with typed slots: use `data.frame` or `DataFrame` for spectra variables (msLevel, rtime, polarity, etc.), `NumericList` for paired m/z and intensity values, and `character` for metadata like dataStorage and dataOrigin. Each slot declaration includes its expected class type (e.g., `slots = c(spectraVars = "data.frame", mz = "NumericList", intensity = "NumericList")`). Implement a `backendInitialize()` method that validates input data against slot types before assignment, ensuring m/z values are sorted increasingly within each spectrum and all core spectra variables are initialized (with NA for user-unspecified variables). Implement accessor methods (e.g., `spectraData()`, `intensity()`, `mz()`) that enforce type consistency on return, and implement `spectraVariables()` to report all available variables (both user-supplied and core). Use `setClass()` to register the class, and optionally define `setMethod()` for `show()` to provide user-friendly summaries of the backend contents.

## Related tools

- **Spectra** (Provides the MsBackend virtual class and core MS data infrastructure; backendInitialize(), spectraData(), spectraVariables() are defined here and called by your S4 subclass.) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame and NumericList classes used for typed slot definitions; ensures consistent handling of heterogeneous data in slots.)
- **R (S4 OOP system)** (Core language runtime; setClass(), setMethod(), setValidity() are base R functions used to define S4 classes and enforce slot contracts.)

## Examples

```
setClass('MsBackendTest', contains='MsBackend', slots=c(spectraVars='data.frame', mz='NumericList', intensity='NumericList')); setMethod('backendInitialize', 'MsBackendTest', function(object, msLevel, rtime, ...) { object@spectraVars <- data.frame(msLevel=msLevel, rtime=rtime); object });
```

## Evaluation signals

- Instantiate the S4 class with backendInitialize() and confirm all slots contain the expected types (e.g., is(obj@spectraVars, 'data.frame') == TRUE).
- Call spectraData() and verify the returned DataFrame contains all core spectra variables (centroided, polarity, isSpectrum, etc.) with NA values for user-unspecified variables.
- Call spectraVariables() and confirm it returns a union of user-supplied and core variable names; length must be ≥ length of core variables.
- Call mz() and intensity() and confirm they return NumericList objects with lengths matching the number of spectra; verify m/z values are sorted increasingly within each spectrum.
- Attempt to assign invalid data to a slot (e.g., assign a character vector to the 'mz' slot expecting NumericList) and confirm the S4 validator or accessor method rejects it with an error.

## Limitations

- S4 slot type checking is enforced only at assignment and instantiation time; if you bypass slots via direct `@` access, type violations are possible.
- Filling missing core spectra variables with NA requires explicit logic in backendInitialize() and spectraData()—there is no automatic schema enforcement.
- NumericList slot definition expects m/z and intensity to have identical lengths within each spectrum; unequal lengths will silently create inconsistent peak data unless validated in backendInitialize().
- S4 class definitions are module-scoped to the R package; exporting and documenting slot names and expected content is necessary for users to extend your backend correctly.

## Evidence

- [intro] To create a new backend a class extending the virtual `MsBackend` needs to be implemented.: "To create a new backend a class extending the virtual `MsBackend` needs to be implemented."
- [intro] Define required slots for spectra variables and peak data with explicit type declarations.: "slots = c(
             spectraVars = "data.frame",
             mz = "NumericList",
             intensity = "NumericList"
         )"
- [intro] The spectraData() method should return the full spectra data within a backend as a DataFrame object.: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] The backendInitialize() method is expected to be called after creating an instance and should prepare the backend.: "The `backendInitialize()` method is expected to be called after creating an instance of the backend class and should prepare (initialize) the backend"
- [intro] MsBackend implementations can represent purely read-only data resources requiring only accessor methods.: "`MsBackend` implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods."
