---
name: mass-spectrometry-data-constraint-validation
description: Use when implementing replacement methods ($<-, [<-, spectraData<-, mz<-, intensity<-, peaksData<-) for a writable MsBackend subclass, or when modifying peak data in an existing backend.
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
  - IRanges
  techniques:
  - tandem-MS
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

# mass-spectrometry-data-constraint-validation

## Summary

Enforce data integrity constraints on m/z values, intensity values, and peak data when implementing or modifying writable MsBackend instances in the Spectra package. This skill ensures that replacement methods maintain critical invariants: length matching, data type validation, peak-count preservation, and m/z ordering.

## When to use

Apply this skill when implementing replacement methods ($<-, [<-, spectraData<-, mz<-, intensity<-, peaksData<-) for a writable MsBackend subclass, or when modifying peak data in an existing backend. Trigger conditions include: (1) adding write capability to a read-only backend, (2) validating user-provided replacement values before assignment, (3) ensuring that m/z and intensity vectors remain consistent after modification, or (4) verifying that m/z values remain sorted increasingly within each spectrum after update.

## When NOT to use

- Backend is purely read-only (e.g., MsBackendMzR retrieving data on-the-fly from raw files) — implement only accessor methods (mz(), intensity(), peaksData()), not replacement methods.
- Input is raw mzML/mzXML/CDF file data being imported for the first time — use backendInitialize() instead to load and structure initial data.
- m/z values are not expected to be increasingly sorted (e.g., in synthetic or reordered spectral data where sort order is intentionally violated) — this skill enforces the Spectra design assumption that m/z values must be ordered.

## Inputs

- S4 MsBackend subclass instance (writable or partially writable)
- Replacement vector or list (m/z values, intensity values, or peak data as NumericList or matrix)
- Index or spectra variable name (for $<- or [<- replacement)
- Integer or logical vector (for subsetting via extractByIndex)

## Outputs

- Modified MsBackend instance with validated replacement data
- Internal DataFrame or list-of-matrices structure updated with new peak or spectra data
- Boolean validation status or error message if constraints violated

## How to apply

Define replacement method signatures using S4 method definitions in R (e.g., `setReplaceMethod('[<-', ...)` for index-based replacement). For each replacement method, implement a four-stage validation pipeline: (1) Match length validation using `.match_length()` to ensure the replacement vector's length equals either the spectrum count (for full backend replacement) or individual spectrum peak counts (for per-spectrum replacement); (2) Data type validation to confirm that m/z and intensity values are NumericList objects and other spectra variables conform to expected types (e.g., numeric, character); (3) Peak-count preservation checks to ensure that replacement values maintain the same number of peaks per spectrum; (4) m/z ordering validation using `is.unsorted()` to verify that m/z values are increasingly sorted within each spectrum after replacement, and confirm that no NA values appear in m/z vectors. After validation passes, update the internal data structure (DataFrame, list of matrices, or on-disk storage) and return the modified backend. Test all replacement methods on a concrete backend instance to confirm writable functionality and constraint enforcement.

## Related tools

- **Spectra** (R package providing the MsBackend virtual class and S4 infrastructure for defining replacement method signatures and validating replacement operations on backend instances) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (R package providing DataFrame class and NumericList container for storing and validating structured spectra data (m/z, intensity, other variables))
- **IRanges** (R package providing base infrastructure for length and index validation operations used in replacement method implementations)

## Examples

```
setReplaceMethod('mz<-', 'MsBackendMemory', function(object, value) { if (length(value) != length(object)) stop('Length mismatch'); if (!is(value, 'NumericList')) stop('m/z must be NumericList'); if (any(is.na(unlist(value)))) stop('NA values not allowed in m/z'); object@mz <- value; object })
```

## Evaluation signals

- Replacement method successfully rejects input vectors with length not matching spectrum count or individual spectrum peak count (via .match_length() validation).
- Replacement method rejects non-NumericList m/z or intensity values and non-matching data types for other spectra variables.
- After successful replacement, peak-count per spectrum remains identical to pre-replacement state (invariant preservation).
- m/z values post-replacement remain increasingly sorted within each spectrum; is.unsorted() returns FALSE for all modified spectra.
- m/z replacement vectors contain no NA values; all replacement operations succeed without introducing missing values in critical peak data.
- Concrete backend instance (e.g., MsBackendMemory) passes all unit tests confirming writable functionality and constraint enforcement.

## Limitations

- Replacement methods are only available for writable backends (e.g., MsBackendMemory, MsBackendDataFrame); partially read-only backends like MsBackendMzR do not support peak data replacement, only spectra variable modification.
- m/z ordering constraint assumes increasingly sorted order within each spectrum; data with unsorted or reversed m/z values will fail validation and cannot be stored.
- Length matching constraint requires exact correspondence between replacement vector length and spectrum count or peak count; subsetting and reordering must be handled separately via extractByIndex() or other subsetting operations.
- No support for sparse or variable-length peak data structures; all spectra must maintain consistent peak-count relationships (if present).
- NA values are not permitted in m/z vectors; spectra with missing m/z measurements cannot be represented in this framework.

## Evidence

- [other] length matching via `.match_length()` to ensure value length equals spectrum count: "length matching via `.match_length()` to ensure value length equals spectrum count"
- [other] data type validation checking that m/z and intensity are NumericList objects: "data type validation checking that m/z and intensity are NumericList objects"
- [other] peak-count preservation requiring that replacement values maintain the same number of peaks per spectrum: "peak-count preservation requiring that replacement values maintain the same number of peaks per spectrum"
- [other] m/z ordering validation using `is.unsorted()` to verify m/z values are increasingly sorted within each spectrum: "m/z ordering validation using `is.unsorted()` to verify m/z values are increasingly sorted within each spectrum"
- [intro] m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported.: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [intro] `MsBackend` implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods.: "`MsBackend` implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods."
- [other] Implement input validation in each replacement method to check that replacement vectors match the length of the backend (number of spectra) or individual spectrum peak counts.: "Implement input validation in each replacement method to check that replacement vectors match the length of the backend (number of spectra) or individual spectrum peak counts."
- [other] For peak data replacement, verify that m/z values remain sorted in increasing order within each spectrum and that intensity vector length equals m/z vector length.: "For peak data replacement, verify that m/z values remain sorted in increasing order within each spectrum and that intensity vector length equals m/z vector length."
