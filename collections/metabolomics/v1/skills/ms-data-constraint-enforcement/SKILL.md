---
name: ms-data-constraint-enforcement
description: 'Use when implementing or validating a new MsBackend class that stores m/z and intensity values, or when assigning peak data to an existing backend. Triggers include: (1) implementing a replacement method (e.g., mz<- or intensity<-) for a backend class;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - S4Vectors
  - Spectra
  - MsBackendTest
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- library(Spectra) library(IRanges)
- library(Spectra)
- return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectra
    doi: 10.3390/metabo12020173
    title: spectra
  dedup_kept_from: coll_spectra
schema_version: 0.2.0
---

# ms-data-constraint-enforcement

## Summary

Validate and enforce critical constraints on mass spectrometry peak data (m/z and intensity values) within backend storage classes to ensure data integrity and conformance to expected physical properties. This skill detects violations early using efficient vectorised methods on NumericList objects, preventing downstream analysis errors.

## When to use

Apply this skill when implementing or validating a new MsBackend class that stores m/z and intensity values, or when assigning peak data to an existing backend. Triggers include: (1) implementing a replacement method (e.g., mz<- or intensity<-) for a backend class; (2) testing that a backend correctly rejects unsorted or invalid peak data; (3) ensuring backend implementations comply with the Spectra API specification that m/z values must be increasingly sorted within each spectrum.

## When NOT to use

- Backend is read-only (no replacement methods required); constraint enforcement applies only to writable backends that expose peak data assignment.
- Constraint validation is already delegated to a lower-level storage layer (e.g., database schema enforces sort order); avoid redundant checks unless API contract requires explicit enforcement at the R object level.
- Input is already a fully-validated, immutable data structure with guaranteed invariants; constraint enforcement adds overhead without benefit.

## Inputs

- MsBackend class definition (S4 class extending virtual MsBackend)
- NumericList object containing m/z values for one or more spectra
- NumericList object containing intensity values for one or more spectra
- Replacement method signature (e.g., setReplaceMethod('mz', 'MsBackendTest', function(object, value) ...)

## Outputs

- Updated MsBackend object with validated and assigned peak data
- Error message (stop) if constraint is violated, halting assignment
- Silent successful assignment if constraint is satisfied

## How to apply

Implement constraint validation in the replacement method (e.g., mz<-) by applying is.unsorted() in vectorised form directly to the NumericList object containing peak values across all spectra. This avoids slower vapply iteration and leverages S4Vectors' efficient implementation. Insert a conditional guard (e.g., if (any(is.unsorted(value))) stop(...)) that raises an informative error message naming the constraint violation before assignment succeeds. Test the constraint enforcement by invoking the replacement method with both valid (sorted) and intentionally invalid (unsorted) m/z vectors, confirming that valid assignments complete silently while invalid assignments throw a named stop error. Document the validation logic in the method's roxygen/docstring to signal to users which constraints are enforced by the backend.

## Related tools

- **Spectra** (Defines the MsBackend virtual class API and provides the NumericList-based peak data infrastructure on which constraint enforcement methods operate.) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides the NumericList class and its efficient is.unsorted() vectorised method used to validate m/z sort order across multiple spectra in a single call.)
- **MsBackendTest** (Example backend class demonstrating the correct implementation of constraint enforcement in the mz<- replacement method.) — https://github.com/RforMassSpectrometry/Spectra

## Examples

```
if (any(is.unsorted(value))) stop("m/z values need to be increasingly sorted within each spectrum")
```

## Evaluation signals

- Constraint-valid input (sorted m/z values): assignment completes without error and object slot is updated correctly.
- Constraint-invalid input (unsorted m/z values within any spectrum): stop error is raised with a message naming the constraint (e.g., 'm/z values need to be increasingly sorted within each spectrum') before any assignment occurs.
- is.unsorted() is applied directly to the NumericList in vectorised form (not via vapply or lapply loop), verified by code inspection and confirmed by absence of slower iteration patterns in the method body.
- Error message is raised early, preventing corrupted backend state; backend object remains unchanged and usable after the failed assignment attempt.
- Documentation or roxygen comments describe the constraint and the error condition, making the validation contract explicit to users of the backend class.

## Limitations

- Vectorised is.unsorted() works only on NumericList objects in S4Vectors; alternative peak data structures (e.g., list of vectors, matrix) require wrapper logic or bespoke iteration.
- Constraint enforcement occurs only at the replacement method boundary; direct slot modification via @ accessor bypasses validation—this is acceptable for internal development but should be discouraged in user-facing APIs.
- Error message is raised after is.unsorted() scans the entire input; for very large spectra datasets, this may incur a performance cost, though vectorised evaluation is still faster than per-spectrum checks.
- Constraint applies to m/z sort order only; intensity values and other peak properties are not validated by this method, requiring separate enforcement logic if needed.

## Evidence

- [intro] The MsBackend virtual class defines the API that new backend classes need to implement to be used with the Spectra object.: "The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object."
- [intro] m/z values are required to be sorted increasingly within each spectrum.: "m/z values within each spectrum are expected to be sorted increasingly."
- [other] The mz<- replacement method uses is.unsorted() in vectorised form on NumericList and raises a stop error when validation fails.: "if (any(is.unsorted(value))) stop("m/z values need to be increasingly sorted within each spectrum")"
- [other] The replacement method applies is.unsorted() efficiently to NumericList rather than using slower per-spectrum iteration.: "The mz<- replacement method uses the efficient is.unsorted() implementation for NumericList rather than vapply"
- [intro] Backends can represent data with only accessor methods (read-only) or with both accessor and replacement methods (writable).: "`MsBackend` implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods."
