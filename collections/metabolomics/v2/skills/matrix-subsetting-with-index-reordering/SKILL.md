---
name: matrix-subsetting-with-index-reordering
description: Use when when you need to subset a backend containing multiple MS spectra to a user-defined subset (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - S4Vectors
  - R
  - Spectra
  - MsBackendMemory
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
---

# matrix-subsetting-with-index-reordering

## Summary

Implement an extractByIndex() method for MsBackend objects that subsets MS spectral peak data (m/z and intensity matrices) to selected spectra while preserving peak ordering and supporting index duplication. This is essential for parallel processing workflows and spectral filtering operations where arbitrary reordering and selective duplication of spectra are required.

## When to use

When you need to subset a backend containing multiple MS spectra to a user-defined subset (e.g., spectra matching a filter criterion, or spectra selected for parallel processing), and the subsetting operation must preserve the internal ordering of m/z and intensity values within each spectrum while allowing reordering and duplication of entire spectra.

## When NOT to use

- Backend is read-only and does not support subsetting operations (though most backends should implement at least extractByIndex as a read-only operation).
- You need to filter spectra based on complex criteria (e.g., retention time range, precursor m/z threshold) — use a filtering workflow first to generate indices, then apply extractByIndex.
- Input is a Spectra object rather than a raw MsBackend — use Spectra's subsetting operators ([, subset) instead, which internally call extractByIndex on the backend.

## Inputs

- MsBackend object (or subclass) containing stored spectral peak data and spectra variables
- integer vector of indices to select (1-based or 0-based depending on implementation convention)

## Outputs

- MsBackend object (same class as input) containing subset of spectra in order specified by index vector
- preserved peak data matrices (m/z and intensity columns) for selected spectra
- updated spectra variables DataFrame matching the subset

## How to apply

Implement extractByIndex() to accept an integer vector of indices specifying which spectra to retain. The method should: (1) use integer indices to directly subset the internal peak data storage (whether stored as a list of matrices, data frame rows, or file offsets depending on backend type); (2) preserve the m/z and intensity ordering within each selected spectrum; (3) support duplicated indices so that the same spectrum can appear multiple times in the output (useful for replication or parallel processing); (4) return a new MsBackend instance of the same class containing only the selected spectra in the specified order; (5) update all associated spectra variables (dataStorage, dataOrigin, and backend-specific metadata) to match the subsetting. Validate that the subset operation maintains invariants: all peaks within each spectrum remain in increasing m/z order, no data loss occurs, and duplicate indices produce identical spectra in output.

## Related tools

- **Spectra** (Framework class that manages a Spectra object by delegating peak data subsetting to the backend's extractByIndex() implementation; used to subset collections of spectra for parallel processing or filtering) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame class for storing and subsetting spectra variables (metadata) associated with each spectrum during extractByIndex operation)
- **MsBackendMemory** (Reference backend implementation (from Spectra package) that stores peaks as a list of matrices; extractByIndex subsets this list while preserving matrix structure and ordering) — https://github.com/RforMassSpectrometry/Spectra

## Examples

```
backend_subset <- extractByIndex(backend, c(1, 3, 3, 5))
```

## Evaluation signals

- Selected spectra appear in output in the exact order specified by the index vector (order is preserved, not sorted).
- Duplicated indices produce identical copies of the selected spectrum; both copies contain the same m/z and intensity values in the same order.
- m/z values within each selected spectrum remain sorted in increasing order; no NA values appear in m/z columns.
- All spectra variables (rows in the spectra variables DataFrame) are correctly subset and aligned with the selected peak data; no row mismatch occurs.
- Peak count and dimensionality of intensity matrices match expected output; subsetting does not lose or corrupt individual peak values.

## Limitations

- Performance depends on backend storage strategy: list-of-matrices backends (MsBackendMemory) support fast subsetting via R's list indexing, while file-based backends (MsBackendMzR) may require reading selected peaks from disk sequentially, resulting in slower performance for non-contiguous indices.
- Duplicated indices multiply memory/storage usage proportionally; creating many copies of the same spectrum can quickly exhaust memory in in-memory backends.
- The method does not validate that indices are within bounds or positive; implementations must add bounds checking or rely on underlying R subsetting to raise appropriate errors.
- Backends that are read-only for peaks but allow modification of spectra variables may implement a restricted version of extractByIndex that only reorders metadata without copying peak data structures.

## Evidence

- [other] extractByIndex workflow definition: "Implement extractByIndex() method to subset the backend to selected spectra using integer indices, preserving order and supporting duplicates."
- [intro] extractByIndex purpose and usage: "The `extractByIndex()` and `[` methods allows to subset `MsBackend` objects. This operation is expected to reduce a `MsBackend` object to the selected spectra."
- [intro] peaksData output format for validation: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum"
- [intro] m/z ordering invariant: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [other] MsBackendMemory storage and efficiency: "The `MsBackendMemory` backend stores data as a list of matrices instead, yielding more efficient peaksData() implementation with lower overhead for adding/replacing/checking MS data."
