---
name: dataframe-construction-and-column-merging
description: Use when when implementing a new MsBackend subclass and need to return
  complete spectra data as a single DataFrame object that combines required core variables
  with backend-specific metadata columns, while avoiding cyclic function calls between
  spectraData() and spectraVariables().
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - S4Vectors
  - R
  - MSnbase
  - Spectra
  - IRanges
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- '`DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)'
- DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)
- library(Spectra) library(IRanges)
- extension of the of *in-memory* and *on-disk* data representations from the `r Biocpkg("MSnbase")`
  package
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

# dataframe-construction-and-column-merging

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct a unified DataFrame for mass spectrometry spectra by merging core spectra variables (m/z, intensity, retention time, scan index) with backend-specific columns, ensuring no circular dependencies between accessor methods. This skill is essential for implementing the spectraData() method in custom MsBackend subclasses.

## When to use

When implementing a new MsBackend subclass and need to return complete spectra data as a single DataFrame object that combines required core variables with backend-specific metadata columns, while avoiding cyclic function calls between spectraData() and spectraVariables().

## When NOT to use

- Backend is read-only and does not need to support data replacement—use simplified accessor methods instead.
- Data is already stored in a pre-built DataFrame and needs only direct access, not reconstruction.
- Core spectra variables cannot be extracted or are intentionally omitted (violates MsBackend API contract).

## Inputs

- MsBackend subclass instance with internal data storage (data.frame, list of matrices, or external resource connection)
- Core spectra variables: m/z values (NumericList), intensity values (NumericList), retention time (numeric), scan index (integer)
- Backend-specific column definitions (names and data)

## Outputs

- DataFrame object containing all spectra variables with m/z and intensity as NumericList columns
- Character vector of spectra variable names (union of core and backend-specific names)

## How to apply

First, populate core spectra variables (m/z, intensity, retention time, scan index) into a DataFrame using fillCoreSpectraVariables(), which handles missing values and ensures proper data types. Extract backend-specific columns from internal storage (e.g., data.frame or list-based structures). Use S4Vectors::DataFrame() to combine core variables and backend columns into a single unified object. Ensure m/z and intensity values are returned as NumericList columns when extracted. Finally, verify that spectraData() does not call spectraVariables() and vice versa to prevent circular dependencies—spectraVariables() should return a character vector of union of core variable names and backend column names independently.

## Related tools

- **S4Vectors** (Provides DataFrame class for constructing the unified data structure containing core and backend-specific columns) — http://bioconductor.org/packages/release/bioc/html/S4Vectors.html
- **Spectra** (Defines MsBackend virtual class and fillCoreSpectraVariables() utility function for populating core spectra variables) — https://github.com/RforMassSpectrometry/Spectra
- **IRanges** (Provides NumericList class for storing m/z and intensity peak data as per-spectrum lists) — http://bioconductor.org/packages/release/bioc/html/IRanges.html

## Examples

```
# In an MsBackend subclass implementation:
setMethod('spectraData', 'MyBackend', function(object) {
  core_vars <- fillCoreSpectraVariables(object)
  backend_cols <- data.frame(myVar=object@metadata$values)
  DataFrame(core_vars, backend_cols)
})
setMethod('spectraVariables', 'MyBackend', function(object) {
  union(names(core_spectra_variables), names(object@metadata))
})
```

## Evaluation signals

- Verify spectraData() returns a DataFrame with all core variables (mz, intensity, rtime, scanIndex) present as columns.
- Confirm m/z and intensity columns are NumericList type with correct per-spectrum ordering (m/z increasingly sorted).
- Check that spectraVariables() returns a character vector with no duplicates and includes both core names and backend column names.
- Verify no circular function calls: spectraData() should not invoke spectraVariables() and vice versa.
- Validate that DataFrame structure matches S4Vectors::DataFrame specification and integrates backend-specific metadata without data loss.

## Limitations

- m/z values within each spectrum must be sorted increasingly; missing values (NA) for m/z are not supported by the MsBackend API.
- fillCoreSpectraVariables() may have computational overhead if populating many missing core variables; consider caching results for large backends.
- Circular dependency prevention requires careful API design; if a backend needs dynamic column discovery at query time, special care must be taken to avoid triggering spectraData() from spectraVariables().

## Evidence

- [intro] Core spectra variables definition: "While backends can define their own properties, a minimum required set of spectra variables **must** be provided by each backend"
- [intro] spectraData() method purpose: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] spectraVariables() method purpose: "The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables of the backend"
- [other] fillCoreSpectraVariables workflow: "spectraData() uses fillCoreSpectraVariables() to populate missing core spectra variables into a DataFrame"
- [other] Preventing circular dependencies: "spectraVariables() returns the union of core variable names and backend column names without calling spectraData(), preventing cyclicity"
- [intro] m/z value constraints: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
