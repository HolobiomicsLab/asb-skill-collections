---
name: validity-constraint-enforcement-for-msdata
description: Use when when designing a custom MsBackend subclass (e.g., MsBackendTest) that stores spectral data in multiple slots (a data.frame for spectra variables, NumericList objects for m/z and intensity peaks). Use this skill to guard against slot desynchronization—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - S4Vectors
  - Spectra
  - R (S4 system)
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# validity-constraint-enforcement-for-msdata

## Summary

Enforce consistency constraints across S4 slots in custom MsBackend classes to ensure that spectra variable metadata, m/z values, and intensity values remain synchronized and meet mass spectrometry data requirements (sorted m/z, no NA values). This is critical when extending the virtual MsBackend class to create new mass spectrometry data storage backends.

## When to use

When designing a custom MsBackend subclass (e.g., MsBackendTest) that stores spectral data in multiple slots (a data.frame for spectra variables, NumericList objects for m/z and intensity peaks). Use this skill to guard against slot desynchronization—e.g., when spectraVars rows do not match the length of mz/intensity elements, or when m/z values are unsorted or contain NA values per spectrum.

## When NOT to use

- Working with an existing, pre-validated backend implementation (e.g., MsBackendMemory, MsBackendMzR)—no need to re-validate.
- Using a read-only backend wrapper (e.g., MsBackendCached) that delegates validation to its parent backend.
- Data is already guaranteed consistent by external constraints (e.g., loaded from a single coherent SQL database via MsBackendSql).

## Inputs

- S4 class definition extending MsBackend
- data.frame slot (spectraVars) with spectrum-level metadata
- NumericList slot (mz) with m/z peak values per spectrum
- NumericList slot (intensity) with intensity values per spectrum

## Outputs

- Validated MsBackend instance (passes setValidity checks)
- Character vector of validation error messages (if validation fails)
- Boolean result from validObject() call

## How to apply

Define a setValidity() method on your MsBackend subclass that enforces three key invariants: (1) nrow(spectraVars) == length(mz) == length(intensity), ensuring all slots index the same number of spectra; (2) for each element in the mz NumericList, values must be sorted increasingly with no NA entries, as required by the Spectra package specification; (3) optionally, validate that spectra variables include required core variables (e.g., dataStorage, dataOrigin) and that intensity values are non-negative. The setValidity method should return TRUE on success or a descriptive character vector of error messages on failure. Call validObject() after instantiation to trigger validation.

## Related tools

- **Spectra** (defines the MsBackend virtual class and spectra data model; provides setValidity and validObject infrastructure for S4 class validation) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (provides NumericList and DataFrame slot types used to store peak data and spectra metadata in MsBackend subclasses)
- **R (S4 system)** (language and object system; setClass, setValidity, validObject, setMethod are core functions for defining and validating S4 classes)

## Examples

```
setValidity("MsBackendTest", function(object) { if (nrow(object@spectraVars) != length(object@mz)) return("nrow(spectraVars) != length(mz)"); if (length(object@mz) != length(object@intensity)) return("length(mz) != length(intensity)"); if (!all(sapply(object@mz, function(x) !anyNA(x) && !is.unsorted(x)))) return("mz not sorted or contains NA"); TRUE }); validObject(backend_instance)
```

## Evaluation signals

- validObject(backend_instance) returns TRUE for a correctly populated backend; returns an error or character vector listing constraint violations when slots are mismatched.
- nrow(spectraVars) equals length(mz) and length(intensity)—inspect via `all(nrow(backend@spectraVars) == length(backend@mz), length(backend@mz) == length(backend@intensity))`.
- For each element in mz NumericList, m/z values are sorted increasingly and contain no NA: `all(sapply(backend@mz, function(x) all(!is.na(x)) && is.unsorted(x) == FALSE))`.
- Attempt to create an invalid backend (e.g., mismatched slot lengths) and verify setValidity rejects it with a descriptive error message.
- After valid instantiation, call spectraData() and peaksData() methods and confirm returned DataFrame and matrices are internally consistent.

## Limitations

- setValidity is called only at object creation and after explicit validObject() calls; modifications via direct slot assignment (@ operator) may bypass validation—use accessor methods with validity checks instead.
- Validation logic is backend-specific; core requirements (m/z sorting, no NA in mz) apply to all backends, but custom spectra variables or file format constraints must be added per subclass.
- Performance cost scales with number of spectra; for very large backends (millions of spectra), validation may be slow—consider deferred or partial validation strategies.
- The Spectra package requires m/z values sorted increasingly per spectrum with no NA values; backends storing unsorted or missing m/z data must pre-process or reject such data at initialization.

## Evidence

- [other] A setValidity method enforces that the number of rows in spectraVars matches the length of both mz and intensity slots, ensuring data consistency across the backend.: "A setValidity method enforces that the number of rows in spectraVars matches the length of both mz and intensity slots, ensuring data consistency across the backend."
- [intro] m/z values within each spectrum are expected to be sorted increasingly. Missing values (NA) for m/z values are not supported.: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (NA) for m/z values are not supported."
- [intro] The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object.: "The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object."
- [other] Define a setValidity method that enforces the constraint that the number of rows in the spectraVars data.frame matches the length of the m/z and intensity NumericList elements, and that m/z values are sorted increasingly with no NA values per spectrum.: "Define a setValidity method that enforces the constraint that the number of rows in the spectraVars data.frame matches the length of the m/z and intensity NumericList elements, and that m/z values"
- [intro] One `Spectra` object is supposed to contain MS (spectral) data of multiple MS spectra. m/z values within each spectrum are expected to be sorted increasingly.: "One `Spectra` object is supposed to contain MS (spectral) data of multiple MS spectra. m/z values within each spectrum are expected to be sorted increasingly."
