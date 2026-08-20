---
name: circular-dependency-avoidance-in-method-design
description: Use when you are implementing multiple accessor methods on a backend class that logically depend on each other (e.g., one returns full data and another returns column metadata), and both methods are required by downstream code.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - S4Vectors
  - R
  - MSnbase
  - Spectra
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# circular-dependency-avoidance-in-method-design

## Summary

A design pattern for implementing interdependent accessor methods in object-oriented backends that prevents infinite recursion by ensuring one method populates data without calling the other. This is essential when designing MsBackend subclasses where spectraData() and spectraVariables() must both be available but risk calling each other cyclically.

## When to use

You are implementing multiple accessor methods on a backend class that logically depend on each other (e.g., one returns full data and another returns column metadata), and both methods are required by downstream code. The risk of circular calls arises when one method naturally queries the other to fulfill its contract.

## When NOT to use

- Backend design does not require both full data access and column enumeration (use only spectraData() or only spectraVariables()).
- Downstream code never calls spectraVariables() independently; if only spectraData() is called, cyclicity cannot occur.
- Backend is read-only and pre-populated; no lazy loading or on-demand computation is needed.

## Inputs

- MsBackend subclass with internal data storage (e.g., data.frame, list, or on-disk format)
- Core spectra variable definitions (mz, intensity, rtime, scanIndex, etc.)
- Backend-specific column names and their values

## Outputs

- spectraData() method returning S4Vectors::DataFrame with m/z and intensity as NumericList columns
- spectraVariables() method returning character vector of all available spectra variable names
- Acyclic method call graph confirmed by static analysis or runtime instrumentation

## How to apply

Structure spectraData() to independently populate missing core spectra variables (m/z, intensity, retention time, scan index) by calling fillCoreSpectraVariables() and combining them with backend-specific columns into a DataFrame—without invoking spectraVariables(). Separately, implement spectraVariables() as a simple union of core variable names and backend column names, explicitly NOT calling spectraData(). This asymmetry breaks the cycle: spectraData() is self-contained and provides both peaks and metadata, while spectraVariables() is a lightweight catalog that does not trigger data retrieval. Verify no caller paths lead from spectraVariables() → spectraData() or vice versa by tracing method call graphs.

## Related tools

- **Spectra** (Defines the Spectra class and MsBackend virtual class API; provides fillCoreSpectraVariables() utility for populating core variables) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame class for structuring spectraData() return value with proper column and list handling)
- **R** (Language for implementing MsBackend subclass methods and verifying method call graph acyclicity)

## Examples

```
# Define spectraData() method
setMethod('spectraData', 'MyBackend', function(object, columns = character()) {
  df <- fillCoreSpectraVariables(object, columns)
  S4Vectors::DataFrame(df)
})
# Define spectraVariables() method
setMethod('spectraVariables', 'MyBackend', function(object) {
  union(c('mz', 'intensity', 'rtime', 'scanIndex'), names(object@metadata))
})
```

## Evaluation signals

- spectraData() returns a DataFrame object with all requested core variables and backend columns populated; m/z and intensity are NumericList, not NA.
- spectraVariables() returns a character vector containing the union of core variable names ('mz', 'intensity', 'rtime', 'scanIndex') and backend-specific column names with no duplicates.
- Static analysis confirms spectraVariables() source code does not invoke spectraData(); conversely, spectraData() source code does not invoke spectraVariables().
- Runtime call tracing shows no recursive loops when both methods are invoked by external code in any order.
- fillCoreSpectraVariables() is called only within spectraData(), never from spectraVariables().

## Limitations

- The pattern assumes fillCoreSpectraVariables() utility is available and correctly implements core variable population; custom backends may need to replicate this logic if the utility is unavailable.
- Requires explicit enumeration of backend-specific column names; if column metadata is generated dynamically or lazily, the union in spectraVariables() may become stale or incomplete.
- Does not address transitive dependencies; if spectraData() calls a helper method that internally calls spectraVariables() (or vice versa), the cycle may still exist and require deeper refactoring.
- Applicable only to object-oriented backend classes; functional or procedural data access patterns may not benefit from this design principle.

## Evidence

- [other] Acyclicity via method structure: "spectraData() uses fillCoreSpectraVariables() to populate missing core spectra variables into a DataFrame, while spectraVariables() returns the union of core variable names and backend column names"
- [intro] spectraData() design requirements: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] spectraVariables() design requirements: "The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables of the backend"
- [intro] Core variable handling: "While backends can define their own properties, a minimum required set of spectra variables **must** be provided by each backend"
- [other] DataFrame and NumericList usage: "The DataFrame returned by spectraData() includes m/z and intensity as NumericList columns when requested."
