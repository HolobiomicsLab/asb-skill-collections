---
name: core-spectra-variable-definition-and-population
description: Use when when implementing a custom MsBackend class for the Spectra package, you must define these two methods to satisfy the MsBackend virtual class API contract.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Spectra
  - S4Vectors
  - R
  - MSnbase
  - MsBackendMemory
  - MsBackendMzR
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- The *Spectra* package defines an efficient infrastructure for storing and handling mass spectrometry spectra
- '`DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)'
- DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)
- library(Spectra) library(IRanges)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# core-spectra-variable-definition-and-population

## Summary

Implement spectraData() and spectraVariables() methods in MsBackend subclasses to safely expose mass spectrometry core variables (m/z, intensity, retention time, scan index) without cyclic function calls. This skill ensures that peak data and metadata are correctly merged into a single DataFrame while maintaining architectural separation between variable discovery and data retrieval.

## When to use

When implementing a custom MsBackend class for the Spectra package, you must define these two methods to satisfy the MsBackend virtual class API contract. Use this skill when you are creating a new backend that stores spectral data in a novel format (database, file type, or in-memory structure) and need to expose that data safely to Spectra analysis code.

## When NOT to use

- You are not implementing a custom backend — use this skill only when extending MsBackend, not when using existing backends like MsBackendMemory or MsBackendMzR.
- Your backend is read-only and does not need to support modification of peak data — you still must implement these methods, but they will not expose writable slots.
- You are analyzing pre-loaded spectra data without implementing new storage backends — use the Spectra API directly instead.

## Inputs

- MsBackend subclass instance with internal data storage (data.frame, list, or external resource handle)
- Optional character vector of requested spectra variables (subset of spectraVariables())
- Internal peak data storage (m/z and intensity matrices or lists)

## Outputs

- DataFrame object with one row per spectrum, containing all core variables and backend-specific columns
- NumericList columns for m/z (sorted increasingly) and intensity values
- Character vector of all available spectra variable names (union of core + backend-specific)

## How to apply

Implement spectraData() by calling fillCoreSpectraVariables() to populate missing core variables (m/z, intensity, rtime, scanIndex) into a DataFrame, then extract backend-specific columns from your internal storage (e.g., data.frame or list-based structures) and combine both sets using S4Vectors::DataFrame(). Ensure m/z and intensity are returned as NumericList columns when requested. Separately implement spectraVariables() to return a character vector containing the union of core variable names and backend column names without calling spectraData(). Verify no circular dependency exists by confirming spectraVariables() does not invoke spectraData() and vice versa. This separation allows Spectra to discover available variables cheaply before fetching actual peak data, critical for lazy-loading backends that retrieve peaks on-the-fly from raw files.

## Related tools

- **Spectra** (Defines the MsBackend virtual class and provides fillCoreSpectraVariables() utility; the Spectra class consumes backend implementations) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame class for constructing the output data structure combining core and backend-specific columns)
- **R** (Language and runtime for implementing S4 methods in MsBackend subclasses)
- **MsBackendMemory** (Reference implementation within Spectra package showing how spectraData() and spectraVariables() are realized for in-memory list-based storage) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMzR** (Reference implementation showing lazy-loading pattern where peaks are retrieved on-the-fly; demonstrates partial read-only semantics) — https://github.com/RforMassSpectrometry/Spectra

## Examples

```
setMethod('spectraData', 'MyMsBackend', function(object, columns = spectraVariables(object)) { core <- object@data; core <- fillCoreSpectraVariables(core); S4Vectors::DataFrame(core[, columns, drop=FALSE]) }); setMethod('spectraVariables', 'MyMsBackend', function(object) { union(c('mz','intensity','rtime','scanIndex','dataStorage','dataOrigin'), colnames(object@data)) })
```

## Evaluation signals

- spectraData() returns a DataFrame with exactly one row per spectrum in the backend, with no NA values in core columns (mz, intensity, rtime, scanIndex where applicable).
- m/z values returned as NumericList are sorted increasingly within each spectrum; intensity values are returned as NumericList of same length as m/z.
- spectraVariables() returns a character vector containing at least all core variable names ('mz', 'intensity', 'rtime', 'scanIndex', 'dataStorage', 'dataOrigin') plus any backend-specific columns, with no duplicates.
- No circular function calls exist: calling spectraVariables() does not trigger spectraData(), and vice versa; verify by profiling or static code inspection.
- extractByIndex(backend, idx) followed by spectraData() returns a DataFrame with nrow(result) == length(idx) and identical column structure and m/z ordering as the full backend.

## Limitations

- m/z values must be sorted increasingly within each spectrum; missing (NA) values for m/z are not supported by the Spectra framework.
- Backends must populate both dataStorage and dataOrigin spectra variables to indicate where data is stored and from where it derives; failure to do so violates the MsBackend contract.
- The spectraData() method must return the full spectra data; subsetting and filtering should be implemented separately via extractByIndex() rather than within spectraData() parameters.
- If a backend is partially read-only (e.g., allowing modification of metadata but not peaks), spectraData() must still return all requested variables; write-protection is enforced via separate replacement methods, not in the accessor.
- For large or lazy-loading backends (e.g., MsBackendMzR), calling spectraData() on all spectra may trigger disk I/O or network access; callers should subset via extractByIndex() before requesting full data.

## Evidence

- [intro] spectraData() and spectraVariables() method implementation pattern: "spectraData() uses fillCoreSpectraVariables() to populate missing core spectra variables into a DataFrame, while spectraVariables() returns the union of core variable names and backend column names"
- [intro] Core variables definition: "a minimum required set of spectra variables **must** be provided by each backend"
- [intro] m/z and intensity data structure requirement: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] spectraVariables() method contract: "The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables of the backend"
- [intro] m/z ordering constraint: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [intro] DataStorage and dataOrigin requirement: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [intro] Workflow for spectraData() implementation: "Define the spectraData() method in the MsBackend subclass to call fillCoreSpectraVariables() to populate core spectra variables (m/z, intensity, retention time, and other required properties)."
- [intro] Preventing cyclicity in backend methods: "Verify that spectraVariables() does not call spectraData() and that spectraData() does not call spectraVariables() to prevent circular dependencies."
