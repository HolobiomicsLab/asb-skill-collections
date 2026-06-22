---
name: type-safety-and-length-matching-validation
description: Use when implementing data replacement methods (such as `[<-`, `$<-`, `mz<-`, `intensity<-`, `peaksData<-`) in a writable MsBackend subclass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - R
  - S4Vectors
  - Spectra
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

# Type-safety-and-length-matching-validation

## Summary

Enforce data integrity constraints in writable MS backends by validating that replacement values match expected types (NumericList for m/z and intensity, character for names) and vector lengths (equal to spectrum count or individual spectrum peak counts). This ensures that m/z values remain sorted, peak counts are preserved, and NA values are excluded from critical fields.

## When to use

Apply this skill when implementing data replacement methods (such as `[<-`, `$<-`, `mz<-`, `intensity<-`, `peaksData<-`) in a writable MsBackend subclass. Use it whenever you must modify spectra variables or peak data in place and need to prevent silent data corruption or inconsistency between m/z and intensity vector lengths within a spectrum.

## When NOT to use

- When working with read-only backends (e.g., MsBackendMzR, MsBackendMassbankSql) that do not implement replacement methods.
- When the backend is immutable by design and replacement functionality is not required or supported.
- When input data has already been pre-validated upstream and re-validation would introduce redundant computation without added safety.

## Inputs

- MsBackend subclass instance (writable backend)
- Replacement vector or matrix (NumericList, numeric vector, character vector, or DataFrame)
- Spectrum index or variable name (for selective replacement)
- Expected length (number of spectra or peaks per spectrum)

## Outputs

- MsBackend object with validated and replaced data
- Validation errors or warnings (if constraints violated)
- Updated internal data structure (DataFrame, list of matrices, or equivalent)

## How to apply

Define replacement method signatures using S4 method definitions (`setReplaceMethod`) in the MsBackend subclass. For each replacement operation: (1) validate input length against the number of spectra in the backend using `.match_length()` or equivalent length checking; (2) verify data types before assignment (e.g., confirm m/z and intensity inputs are NumericList objects, names are character vectors); (3) for peak data replacement, check that m/z values are sorted in increasing order using `is.unsorted()` and that intensity vector length equals m/z vector length for each spectrum; (4) enforce that m/z values contain no NA values and that peak-count consistency is maintained across all spectra; (5) apply the validated replacement values to the internal data structure (e.g., DataFrame or list of matrices); (6) test all replacement methods on a concrete backend instance to confirm constraint enforcement.

## Related tools

- **Spectra** (Provides MsBackend virtual class and S4 method definitions for implementing replacement methods with schema validation) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Supplies DataFrame and NumericList container classes used to store and validate spectra variables and peak data)
- **R** (Execution environment for S4 method definitions and constraint checking logic (is.unsorted, length matching))

## Examples

```
setReplaceMethod("mz", "MsBackendMemory", function(object, value) { if (!is(value, "NumericList")) stop("mz must be NumericList"); if (length(value) != length(object)) stop("Length mismatch"); if (any(is.na(unlist(value)))) stop("NA values not allowed in mz"); if (any(sapply(value, is.unsorted))) stop("mz values must be sorted"); object@data[["mz"]] <- value; object })
```

## Evaluation signals

- Replacement values are accepted only if their length matches the number of spectra (for spectra variables) or individual spectrum peak counts (for peak data).
- m/z and intensity values are confirmed to be NumericList objects; character data is confirmed to be character vectors; numeric data types match expected schema.
- m/z values within each spectrum are verified to be sorted in increasing order via `is.unsorted()` check; NA values are rejected for m/z fields.
- For peak data replacement, intensity vector length equals m/z vector length for every spectrum; total peak count per spectrum is preserved.
- Replacement operations on concrete backend instances (e.g., MsBackendMemory or MsBackendDataFrame) succeed and produce consistent internal state; failed replacements throw informative errors without partial updates.

## Limitations

- Validation overhead increases with backend size (number of spectra and peaks per spectrum); large backends may see performance impact during bulk replacement operations.
- The skill is specific to writable backends; read-only backends do not implement replacement methods and thus cannot be modified in place.
- Constraint checking (e.g., m/z sorting) is performed only at replacement time; pre-existing data corruption in the underlying data structure will not be detected or corrected unless explicitly accessed.
- Parallel processing of replacement operations is not addressed; concurrent modifications to the same backend instance may violate constraints if synchronization is not handled at a higher level.

## Evidence

- [other] Replacement methods enforce length matching via `.match_length()` to ensure value length equals spectrum count: "length matching via `.match_length()` to ensure value length equals spectrum count"
- [other] Data type validation checking that m/z and intensity are NumericList objects: "data type validation checking that m/z and intensity are NumericList objects"
- [other] m/z ordering validation using `is.unsorted()` to verify m/z values are increasingly sorted within each spectrum: "m/z ordering validation using `is.unsorted()` to verify m/z values are increasingly sorted within each spectrum"
- [intro] m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported.: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [other] Implement input validation in each replacement method to check that replacement vectors match the length of the backend (number of spectra) or individual spectrum peak counts: "Implement input validation in each replacement method to check that replacement vectors match the length of the backend (number of spectra) or individual spectrum peak counts"
