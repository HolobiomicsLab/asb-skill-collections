---
name: spectrum-subsetting-and-merging
description: Use when when you have a large MsBackend object and need to (1) select a contiguous or non-contiguous range of spectra for focused analysis, or (2) combine spectra from multiple independently-loaded backends (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - S4Vectors
  - R
  - Spectra
  - IRanges
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`
- library(Spectra) library(IRanges)
- library(Spectra)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectra
    doi: 10.3390/metabo12020173
    title: spectra
  dedup_kept_from: coll_spectra
schema_version: 0.2.0
---

# spectrum-subsetting-and-merging

## Summary

Extract subsets of mass spectrometry spectra from a backend by index range and merge multiple backend instances into a unified object for consolidated analysis. This skill enables efficient partitioning and recombination of spectral datasets within the Spectra framework.

## When to use

When you have a large MsBackend object and need to (1) select a contiguous or non-contiguous range of spectra for focused analysis, or (2) combine spectra from multiple independently-loaded backends (e.g., from different mzML files or database queries) into a single Spectra object for joint processing, comparison, or visualization.

## When NOT to use

- Input is a Spectra object rather than a raw MsBackend; use Spectra's [ method directly instead of accessing the backend.
- Backends are of different classes (e.g., mixing MsBackendMzR and MsBackendSql); backendMerge() requires all inputs to be the same type.
- You need to filter spectra by properties (e.g., precursor m/z, retention time, intensity threshold) rather than by explicit index; use Spectra filterIntensity(), filterMzRange(), or other feature-based filtering methods instead.

## Inputs

- MsBackend object (or subclass: MsBackendMemory, MsBackendMzR, MsBackendTest, etc.)
- numeric vector of spectrum indices for subsetting (integer or logical)
- list of MsBackend objects of identical class for merging

## Outputs

- MsBackend object (same class as input) containing selected spectra
- unified MsBackend object combining all input backends

## How to apply

To subset: call extractByIndex() or the [ method on an MsBackend object, passing a numeric vector of spectrum indices (1-based or logical); this returns a new backend instance containing only those spectra, with all corresponding peak data (m/z, intensity), spectra variables (dataStorage, dataOrigin, etc.), and metadata preserved. To merge: invoke backendMerge() on a list or sequence of MsBackend objects of the same class (e.g., multiple MsBackendMemory or MsBackendMzR instances); the method combines spectra row-wise, concatenating spectra variables and peaks data, and returns a single unified backend. Verify correct subsetting by confirming the output backend has the expected spectrum count and that m/z values within each spectrum remain sorted increasingly. Verify merging by checking that the final spectrum count equals the sum of input counts and that no duplicate spectra were inadvertently created.

## Related tools

- **Spectra** (R package providing the MsBackend virtual class and default implementations (MsBackendMemory); used to create, load, and wrap backends for subsetting and merging via [ and backendMerge()) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame and NumericList classes used internally by MsBackend to store and return spectra variables and peak data during subsetting and merging)
- **IRanges** (Used for efficient indexing and subsetting operations on backend data structures)

## Examples

```
# Subset spectra by index
backend_subset <- extractByIndex(backend, indices = c(1, 3, 5, 10))

# Merge two backends
backend_merged <- backendMerge(list(backend1, backend2))
```

## Evaluation signals

- Output backend spectrum count equals the number of requested indices (for subsetting) or sum of input backend counts (for merging).
- All spectra variables (dataStorage, dataOrigin, precursorMz, etc.) are present in the output and match the input subset or combined set.
- m/z values within each spectrum remain sorted increasingly after subsetting or merging.
- Peak data (m/z and intensity NumericLists) have the same length as spectra variables and correspond to the correct spectrum indices.
- No rows or spectrum objects are duplicated or corrupted; verify by comparing spectraData() before and after the operation.

## Limitations

- backendMerge() requires all input backends to be of the same class; merging heterogeneous backends (e.g., MsBackendMzR + MsBackendMemory) is not supported and will raise an error.
- Subsetting by index is O(n) in the number of spectra; extremely large backends with millions of spectra may see performance degradation if subsetting is done repeatedly on the same object without caching.
- Some backend implementations (e.g., read-only backends like MsBackendCached) may not support extractByIndex() if they do not implement data replacement methods; check backend documentation for supported operations.
- On-disk backends (e.g., MsBackendMzR) may perform subsetting lazily; actual file I/O may not occur until peak data is accessed, so validation of correctness should include a call to peaksData() or intensity() / mz() to force evaluation.

## Evidence

- [intro] extractByIndex() and subsetting enable partition of backends: "The `extractByIndex()` and `[` methods allows to subset `MsBackend` objects."
- [intro] backendMerge() combines multiple backends of the same type: "The `backendMerge()` method merges (combines) `MsBackend` objects (of the same type!) into a single instance."
- [intro] peaksData() preserves m/z and intensity during subsetting/merging: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum."
- [intro] m/z values must remain sorted after operations: "m/z values within each spectrum are expected to be sorted increasingly."
- [intro] MsBackend API enables seamless integration into Spectra workflows: "this separation allows to define new, alternative, data representations and integrate them seamlessly into a `Spectra`-based data analysis workflow."
