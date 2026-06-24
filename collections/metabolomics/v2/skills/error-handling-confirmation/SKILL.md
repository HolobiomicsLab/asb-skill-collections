---
name: error-handling-confirmation
description: Use when when implementing or auditing a data replacement method (e.g.,
  `mz<-`, `intensity<-`) in an MsBackend subclass that must enforce ordering or format
  constraints on peak data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - S4Vectors
  - Spectra
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- library(Spectra) library(IRanges)
- library(Spectra)
- return the **full** spectra data within a backend as a `DataFrame` object (defined
  in the `r Biocpkg("S4Vectors")`
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

# error-handling-confirmation

## Summary

Validate that a replacement method for mass spectrometry backend data raises informative errors when input violates domain constraints, using efficient vectorised checks. This skill ensures that data integrity rules (e.g., m/z sorting) are enforced at assignment time through explicit error messages rather than silent failure.

## When to use

When implementing or auditing a data replacement method (e.g., `mz<-`, `intensity<-`) in an MsBackend subclass that must enforce ordering or format constraints on peak data. Specifically, when m/z values must be increasingly sorted within each spectrum and you need to confirm the method detects and rejects unsorted input.

## When NOT to use

- Input data already validated upstream (e.g., imported from trusted source with pre-sorted m/z); error-handling confirmation is redundant.
- Replacement method is for read-only backends that do not implement data assignment methods.
- Constraint is optional or best-effort; method is designed to coerce/repair data rather than reject it.

## Inputs

- MsBackend subclass (e.g., MsBackendTest) with a data replacement method (e.g., mz<-)
- NumericList object containing peak m/z or intensity values
- test vectors: one sorted increasingly, one with out-of-order elements

## Outputs

- silent assignment (no error) when input satisfies constraint
- stop() error with descriptive message when input violates constraint
- documentation confirming vectorised is.unsorted() implementation

## How to apply

Inspect the replacement method's validation logic to confirm it applies vectorised is.unsorted() to NumericList objects rather than scalar loops (vapply), which is more efficient for large spectra. The method should call is.unsorted(value) and wrap it in any() to produce a single boolean; if TRUE, it should raise a stop() error with an informative message naming the constraint violated (e.g., 'm/z values need to be increasingly sorted within each spectrum'). Test the method twice: once with valid sorted m/z values to confirm silent success, and once with intentionally unsorted values to confirm the error is raised with the expected message. Document that the validation uses vectorised operations on the NumericList class for performance.

## Related tools

- **Spectra** (provides MsBackend virtual class and NumericList infrastructure for defining and testing replacement methods) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (defines NumericList class used to store peak m/z and intensity values with vectorised is.unsorted() method)
- **R** (executes is.unsorted(), any(), and stop() functions for constraint checking and error reporting)

## Examples

```
# Test mz<- replacement method error handling
library(Spectra)
mz_valid <- NumericList(c(100, 101, 102), c(50, 51, 52))
value(backend)[, "mz"] <- mz_valid  # succeeds silently
mz_invalid <- NumericList(c(102, 100, 101), c(50, 51, 52))  # first spectrum unsorted
value(backend)[, "mz"] <- mz_invalid  # raises: Error in if (any(is.unsorted(value))) stop(...)
```

## Evaluation signals

- Inspect method source code: confirm is.unsorted(value) is applied directly to NumericList, not wrapped in vapply or other scalar loop.
- Execute replacement with valid sorted m/z values: assignment succeeds silently without error.
- Execute replacement with unsorted m/z values: stop() error is raised with exact message 'm/z values need to be increasingly sorted within each spectrum'.
- Confirm any(is.unsorted(value)) returns TRUE only when at least one spectrum has unsorted m/z within itself, not across spectra.
- Verify performance: method completes in < 1 second on NumericList with 10,000+ spectra, indicating vectorised rather than scalar evaluation.

## Limitations

- The is.unsorted() check only detects within-spectrum sorting violations; it does not validate m/z values across spectrum boundaries or cross-spectrum comparisons.
- Error message is generic; it does not report which spectrum index violated the constraint, making debugging harder for large datasets.
- The method does not offer automatic repair (sorting) as an alternative to rejection; users must manually correct and retry assignment.

## Evidence

- [other] Does the mz<- replacement method use an efficient vectorised is.unsorted() implementation on NumericList objects rather than vapply?: "The mz<- replacement method uses the efficient is.unsorted() implementation for NumericList rather than vapply"
- [other] Confirmation of the exact error message and logic.: "'if (any(is.unsorted(value))) stop("m/z values need to be increasingly sorted within each spectrum")'"
- [intro] Domain constraint on m/z values from the article.: "m/z values within each spectrum are expected to be sorted increasingly."
- [intro] Role of NumericList in storing peak data.: "slots = c(
             spectraVars = "data.frame",
             mz = "NumericList",
             intensity = "NumericList"
         )"
