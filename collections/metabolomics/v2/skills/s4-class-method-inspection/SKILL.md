---
name: s4-class-method-inspection
description: Use when you need to verify that an S4 replacement method (e.g., `mz<-`) in a bioinformatics backend class correctly validates input data using vectorized operations on NumericList or similar container objects, rather than inefficient loops or apply functions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3520
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
---

# S4 Class Method Inspection

## Summary

Systematically locate, examine, and validate S4 replacement methods in R packages to verify they correctly implement required validation logic, such as vectorized efficiency checks on complex data structures. This skill is essential for auditing backend implementations in bioinformatics packages where data integrity constraints (e.g., sorted m/z values) must be enforced.

## When to use

You need to verify that an S4 replacement method (e.g., `mz<-`) in a bioinformatics backend class correctly validates input data using vectorized operations on NumericList or similar container objects, rather than inefficient loops or apply functions. Apply this skill when auditing custom MsBackend implementations for conformance to data ordering or structural requirements.

## When NOT to use

- Input is a read-only backend class that does not implement replacement methods (only accessor methods are required).
- The validation target is a simple numeric vector rather than a NumericList; is.unsorted() behavior differs for atomic vectors vs. S4 objects.
- You are inspecting a finished, published package that has passed CRAN/Bioconductor review; validation audit is no longer necessary for deployment.

## Inputs

- S4 class source code file (e.g., R/AllClasses.R or MsBackendTest.R)
- NumericList object (m/z values, typically)
- Sorted numeric vector(s) for valid test case
- Unsorted numeric vector(s) for invalid test case

## Outputs

- Boolean verification that vectorized is.unsorted() is used (not vapply)
- Test result confirming successful assignment with valid sorted input
- Error message text confirming validation failure with unsorted input
- Documentation report of conformance status

## How to apply

First, locate the S4 class definition and target replacement method in the package source code (e.g., MsBackendTest class and its `mz<-` method). Inspect the method body to confirm it uses vectorized functions like is.unsorted() applied to NumericList objects, rather than vapply or row-wise loops, to detect constraint violations. Execute the method with valid input (sorted m/z values as a NumericList) and verify assignment succeeds silently. Then execute with intentionally malformed input (unsorted m/z values) and confirm an informative error message is raised (e.g., 'stop("m/z values need to be increasingly sorted within each spectrum")'), indicating the validation logic is active. Document the findings, including the exact validation code and test outcomes, to confirm conformance to the specification.

## Related tools

- **Spectra** (Package containing MsBackend virtual class and test backends that implement s4 replacement methods with validation logic) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides NumericList container class and is.unsorted() vectorized method for efficient constraint checking) — https://bioconductor.org/packages/release/bioc/html/S4Vectors.html
- **R** (Language and runtime for executing S4 class definitions and method inspections)

## Examples

```
library(Spectra); library(S4Vectors); backend <- new("MsBackendTest"); backend@mz <- NumericList(c(100, 200, 300)); # valid; backend@mz <- NumericList(c(300, 100, 200)) # raises error
```

## Evaluation signals

- Code inspection confirms is.unsorted() is called directly on NumericList value, not wrapped in vapply or sapply loop.
- Execution with sorted m/z input (e.g., NumericList(c(100, 200, 300))) completes without error and assignment succeeds.
- Execution with unsorted m/z input (e.g., NumericList(c(300, 100, 200))) raises stop() error containing the text 'm/z values need to be increasingly sorted'.
- Method signature matches S4 replacement pattern `setMethod("mz<-", ...)` and the value parameter is documented as NumericList.
- No warning or silent NA handling occurs; validation is deterministic and raises error for any spectrum with unsorted m/z values detected by is.unsorted().

## Limitations

- is.unsorted() behavior on NumericList may differ from behavior on atomic vectors; inspection must confirm the method is designed for the correct input type.
- Read-only backend classes (e.g., MsBackendMzR) do not implement replacement methods, so this skill does not apply; confirm the backend supports write operations before inspection.
- Error message text and validation thresholds are backend-specific; conformance must be validated against the documented specification, not assumed to match other backends.

## Evidence

- [other] Task specification — vectorized validation logic requirement: "does it use an efficient vectorised is.unsorted() implementation on NumericList objects rather than vapply?"
- [other] Implementation finding — actual use of is.unsorted(): "The mz<- replacement method uses the efficient is.unsorted() implementation for NumericList rather than vapply, and raises a stop error when any spectrum has unsorted m/z values: 'if"
- [intro] Data structure requirement — m/z values must be sorted: "m/z values within each spectrum are expected to be sorted increasingly."
- [intro] Backend class design — replacement methods optional for read-only resources: "MsBackend implementations can also represent purely read-only data resources. In this case only data accessor methods need to be implemented but not data replacement methods."
- [intro] Expected slot definition for NumericList storage: "slots = c(
             spectraVars = "data.frame",
             mz = "NumericList",
             intensity = "NumericList"
         )"
