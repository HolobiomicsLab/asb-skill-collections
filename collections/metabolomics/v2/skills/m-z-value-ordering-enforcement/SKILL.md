---
name: m-z-value-ordering-enforcement
description: Use when when implementing or modifying data replacement methods (e.g., `mz<-`, `peaksData<-`) in a writable MsBackend subclass, or when accepting user-supplied m/z vectors destined for storage in a Spectra backend.
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
  - R base
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
---

# m-z-value-ordering-enforcement

## Summary

Enforce that m/z values within each mass spectrometry spectrum are sorted in strictly increasing order and contain no missing values. This constraint is critical for data integrity in writable MsBackend implementations and is validated during peak data replacement operations.

## When to use

When implementing or modifying data replacement methods (e.g., `mz<-`, `peaksData<-`) in a writable MsBackend subclass, or when accepting user-supplied m/z vectors destined for storage in a Spectra backend. Apply this skill whenever peak data is assigned to a backend to prevent downstream analysis failures caused by unsorted or NA-containing m/z values.

## When NOT to use

- When reading m/z values from a read-only backend (e.g., MsBackendMzR); in this case m/z ordering is guaranteed by the data source and validation is unnecessary.
- When m/z values are retrieved via accessor methods like `mz()` rather than replacement methods; accessor methods should always return pre-validated data.
- When performing non-destructive operations such as subsetting (extractByIndex) or visualization; validation applies only to write operations that modify the backend.

## Inputs

- NumericList of m/z values (one list element per spectrum)
- Corresponding NumericList of intensity values
- Integer count of spectra in the backend (for length matching)
- Existing backend data structure (DataFrame, list of matrices, or equivalent)

## Outputs

- Validated NumericList of m/z values ready for backend storage
- Error message or exception if validation fails
- Boolean flag indicating validation success

## How to apply

Before committing replacement m/z values to the backend's internal data structure, apply the following validation workflow: (1) Check that m/z values are sorted increasingly within each spectrum using `is.unsorted()` on each element of the NumericList; (2) Verify that no NA values are present in any m/z vector; (3) Confirm that the length of the m/z vector matches the corresponding intensity vector length for each spectrum; (4) If validation fails, raise an informative error identifying which spectrum(s) violate the constraint; (5) Only update the backend's data structure (e.g., DataFrame or list of matrices) after all validations pass. The rationale is that unsorted or missing m/z values break the fundamental assumption that spectra are ordered increasingly, which is relied upon by peak matching, visualization, and spectral comparison algorithms downstream.

## Related tools

- **Spectra** (Provides S4 class infrastructure and MsBackend virtual class API for defining replacement method signatures and NumericList data structures) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Supplies NumericList and DataFrame containers used to hold m/z and intensity data in writable backends)
- **R base** (Provides is.unsorted() function for detecting unsorted numeric vectors and NA detection functions)

## Examples

```
setMethod("mz<-", "MyWritableBackend", function(x, value) { if (!all(sapply(value, function(v) !is.unsorted(v) && !any(is.na(v))))) stop("m/z values must be sorted increasingly with no NA values"); x@mz <- value; x })
```

## Evaluation signals

- m/z vectors pass `!is.unsorted(mz)` check for each spectrum in the NumericList after replacement
- No NA values are present when checked with `any(is.na(mz))` on each spectrum element
- Length of m/z vector equals length of intensity vector for every spectrum (verified via `lengths(mz) == lengths(intensity)`)
- Backend accessor method `mz()` returns the replaced m/z values unchanged, confirming persistence to storage
- Replacement methods raise an informative error (not a silent failure) when given unsorted or NA-containing m/z values, with error message identifying the violating spectrum index

## Limitations

- The constraint applies only to writable backends; read-only backends and on-the-fly retrieval backends (e.g., MsBackendMzR) are exempt because data is sourced from immutable files or databases.
- Validation overhead grows linearly with the number of spectra and average peaks per spectrum; for very large backends, this may become a performance bottleneck if not vectorized.
- The `is.unsorted()` function does not distinguish between ties (equal consecutive values) and inversions; if the analysis requires strictly increasing order (no ties), additional validation is needed.
- NA detection and length matching are scalar-level checks; they do not detect logical errors such as m/z values that are mathematically valid but biologically implausible (e.g., negative masses or extreme outliers).

## Evidence

- [intro] m/z-ordering-validation-required: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [other] replacement-method-validation-framework: "For peak data replacement, verify that m/z values remain sorted in increasing order within each spectrum and that intensity vector length equals m/z vector length."
- [other] is-unsorted-usage: "m/z ordering validation using `is.unsorted()` to verify m/z values are increasingly sorted within each spectrum"
- [other] na-constraint: "Apply constraints that m/z values must not contain NA values and that all spectra must retain their peak-count consistency."
- [intro] numeric-list-data-type: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum"
