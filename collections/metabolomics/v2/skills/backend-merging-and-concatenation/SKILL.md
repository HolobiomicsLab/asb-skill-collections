---
name: backend-merging-and-concatenation
description: Use when when you have two or more MsBackend objects (e.g., multiple
  MsBackendMemory, MsBackendDataFrame, or MsBackendMzR instances) containing distinct
  sets of MS spectra and you need to consolidate them into a single backend for downstream
  analysis, parallel processing, or export.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3364
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - S4Vectors
  - R
  - Spectra
  - MsBackendMemory
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- '`DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)'
- DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)
- library(Spectra) library(IRanges)
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

# backend-merging-and-concatenation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Combine multiple MsBackend objects of the same type into a single instance while preserving all spectra and their peak data. This skill is essential for aggregating mass spectrometry data from multiple sources or processing stages into a unified backend representation.

## When to use

When you have two or more MsBackend objects (e.g., multiple MsBackendMemory, MsBackendDataFrame, or MsBackendMzR instances) containing distinct sets of MS spectra and you need to consolidate them into a single backend for downstream analysis, parallel processing, or export. Specifically apply this when spectra are logically partitioned across backends (by file, by batch, by processing stage) and must be unified without data loss or reordering.

## When NOT to use

- Backends are of different types (e.g., attempting to merge MsBackendMemory with MsBackendMzR directly without type coercion)
- You need to deduplicate or filter spectra during merging based on properties (use extractByIndex() or subsetting before merging)
- Peak data is not stored as list of matrices but as separate m/z and intensity slots (use peaksData() and reconstruction instead)

## Inputs

- list of MsBackend objects of the same type
- each backend containing spectra variables (DataFrame) and peak data (list of numerical matrices with m/z and intensity columns)

## Outputs

- single MsBackend object containing concatenated spectra and peak data
- merged spectra variables DataFrame
- concatenated list of peak matrices

## How to apply

Implement the backendMerge() method for your MsBackend subclass to accept a list of backend objects of the same type and combine them into a single instance. Internally, use rbindFill() (or equivalent S4Vectors function) to merge the spectra variables data frames from all backends, concatenating them row-wise while handling schema differences gracefully. For peak data stored as lists of matrices, concatenate the lists sequentially preserving spectrum order and dimensionality. Verify that the resulting merged backend contains all spectra from all input backends in their original order (or as documented), that peak matrix dimensions are preserved (each with m/z and intensity columns), and that no spectra or peaks are duplicated or lost during merging.

## Related tools

- **Spectra** (provides the MsBackend virtual class and backendMerge() interface that subclasses implement) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (provides rbindFill() and DataFrame for merging spectra variables data frames while preserving schema)
- **MsBackendMemory** (example backend implementation that stores all data in memory as list of matrices, requiring backendMerge() for concatenation) — https://github.com/RforMassSpectrometry/Spectra

## Examples

```
merged_backend <- backendMerge(list(backend1, backend2, backend3))
```

## Evaluation signals

- Verify that the merged backend's spectra count equals the sum of input backend spectra counts (no loss, no duplication)
- Confirm that peaksData() on the merged backend returns a list with length equal to total spectrum count, with each matrix having exactly 2 columns (m/z, intensity) and matching row counts to originals
- Check that spectraVariables() on the merged backend includes all variables from input backends, with no missing or corrupted values
- Validate that extractByIndex() preserves peak ordering and allows correct subset selection from the merged backend
- Ensure that m/z values within each merged spectrum remain sorted increasingly and contain no NA values

## Limitations

- backendMerge() only works with backends of identical type; heterogeneous merging requires explicit type conversion or intermediate representation (e.g., conversion to MsBackendDataFrame)
- Spectra order in merged output depends on rbindFill() behavior and input list order; explicit sorting must be applied if canonical ordering is required
- If input backends contain spectra variables with incompatible data types or schemas, rbindFill() may coerce or pad with NA values; schema reconciliation should occur before merging
- No automatic deduplication or filtering is performed during merge; spectra with identical m/z–intensity profiles are not detected or consolidated

## Evidence

- [other] task_004 finding on rbindFill: "Implement backendMerge() method to combine multiple MsBackend objects of the same type into a single instance using rbindFill for data frame merging."
- [other] task_004 workflow step on backendMerge: "The `backendMerge()` method merges (combines) `MsBackend` objects (of the same type!) into a single instance."
- [readme] README on MsBackendMemory backend design: "The `MsBackendMemory` backend (package: *Spectra*): *default* backend which keeps all data in memory. Optimized for fast processing."
- [intro] article on MsBackend API definition: "The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object."
