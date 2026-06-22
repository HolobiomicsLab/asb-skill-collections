---
name: vectorized-operation-verification
description: Use when when implementing or auditing S4 replacement methods (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - R
  - S4Vectors
  - Spectra
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- library(Spectra) library(IRanges)
- library(Spectra)
- return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`
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

# vectorized-operation-verification

## Summary

Verify that replacement methods for S4 objects use efficient vectorized operations (e.g., is.unsorted() on NumericList) rather than slower row-wise approaches (e.g., vapply), and that they enforce domain constraints (e.g., sorted m/z values) with informative error messages.

## When to use

When implementing or auditing S4 replacement methods (e.g., mz<-, intensity<-) on backends that store peak data in NumericList format, you need to confirm that the method applies vectorized constraint checking to all spectra at once, rather than looping over individual spectra, and that validation errors are raised before assignment occurs.

## When NOT to use

- Backend represents read-only data resources where replacement methods are not implemented at all
- Peak data is not stored in NumericList format (e.g., stored as plain vectors or matrices)
- Constraint checking is intentionally deferred to post-assignment validation rather than pre-assignment

## Inputs

- S4 backend class definition (e.g., MsBackendTest source code)
- NumericList object (e.g., m/z values for multiple spectra)
- Test data: sorted m/z values (valid case)
- Test data: unsorted m/z values (invalid case)

## Outputs

- Verification report confirming vectorized constraint check implementation
- Error message text raised on constraint violation
- Assignment confirmation on valid input

## How to apply

Locate the S4 replacement method in the backend class source code and inspect its implementation. Confirm it applies vectorized operations such as is.unsorted() directly to the NumericList object rather than using vapply or similar loop constructs. Verify that the method checks domain constraints (e.g., increasing m/z ordering within each spectrum) using these vectorized operations. Execute the method with valid input (sorted m/z values) and confirm assignment succeeds. Execute the method with intentionally invalid input (unsorted m/z values) and confirm an informative stop() error is raised before any assignment. Document the results, including the exact constraint check logic and error message.

## Related tools

- **Spectra** (S4 package providing MsBackend virtual class and NumericList-based peak storage infrastructure) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides NumericList class and vectorized operations for constraint validation)
- **R** (Language runtime; is.unsorted() is a base R vectorized function)

## Examples

```
# In R, after loading Spectra and the backend source:
obj <- new("MsBackendTest", mz = NumericList(c(100, 101, 102), c(200, 201, 202)))
mz(obj) <- NumericList(c(102, 101, 100), c(201, 200, 202))  # Raises: Error in if (any(is.unsorted(value))) stop("m/z values need to be increasingly sorted within each spectrum")
```

## Evaluation signals

- Replacement method applies is.unsorted() directly to the NumericList input, not via vapply or loop over individual spectra
- Constraint check (e.g., any(is.unsorted(value))) executes before assignment and stops with informative error if violated
- Valid input (sorted m/z values) passes validation and assignment succeeds without error
- Invalid input (unsorted m/z values) raises stop() error with message referencing the constraint (e.g., 'increasingly sorted')
- Error is raised in a single vectorized operation rather than checking each spectrum individually

## Limitations

- This verification applies only to backends using NumericList storage; other peak data representations (matrices, plain lists) may not support is.unsorted() and require alternative constraint checking approaches
- The skill verifies the *implementation* of the constraint check but does not validate whether the constraint itself is appropriate for all use cases (e.g., some backends may intentionally allow unsorted m/z during intermediate operations)
- Vectorized is.unsorted() reports only whether *any* spectrum is unsorted, not which specific spectra fail; debugging of constraint violations may require additional introspection

## Evidence

- [other] research_question: "Does the mz<- replacement method for MsBackendTest correctly validate that m/z values are increasingly sorted within each spectrum, and does it use an efficient vectorised is.unsorted()"
- [other] finding: "The mz<- replacement method uses the efficient is.unsorted() implementation for NumericList rather than vapply, and raises a stop error when any spectrum has unsorted m/z values: 'if"
- [readme] intro: "m/z values within each spectrum are expected to be sorted increasingly."
- [other] workflow_step: "Inspect the method to confirm it applies is.unsorted() in vectorised form to detect unsorted m/z values within each spectrum's NumericList."
