---
name: spectral-peak-data-extraction
description: Use when when you need to retrieve m/z–intensity pairs from a MsBackend-backed Spectra object for visualization, comparison, or processing; particularly when the backend stores peak data separately (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  tools:
  - S4Vectors
  - R
  - Spectra
  - MsBackendMemory
  - MsBackendMzR
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-data-extraction

## Summary

Extract m/z and intensity peak data from mass spectrometry spectra stored in a MsBackend, returning them as a list of numerical matrices with one matrix per spectrum. This is a core operation for accessing and validating MS peak data before downstream analysis.

## When to use

When you need to retrieve m/z–intensity pairs from a MsBackend-backed Spectra object for visualization, comparison, or processing; particularly when the backend stores peak data separately (e.g., in distinct m/z and intensity slots) and you need them merged into matrix form, or when validating that peaks are correctly sorted and dimensioned.

## When NOT to use

- When you only need aggregated statistics (e.g., total ion current, maximum intensity) without the full peak list—use intensity() or mz() accessors instead.
- When peaks are already stored as pre-merged matrices in your backend and you do not need subsetting—direct access is faster.
- When working with a read-only backend (e.g., MsBackendMzR) that does not support peak replacement—query peaksData() for read access, but do not attempt to modify and re-insert.

## Inputs

- MsBackend object with populated m/z and intensity data slots or list
- Integer indices (for subsetting operations within peaksData)
- Spectrum identifiers to access individual peak data

## Outputs

- List of numerical matrices, one per spectrum
- Each matrix has 2 columns: m/z values (sorted increasingly) and intensity values
- Matrices preserve order and can support duplicated spectra if extracted via extractByIndex()

## How to apply

Implement a peaksData() method in your MsBackend subclass that iterates over the m/z and intensity slots for each spectrum and merges them into numerical matrices (one per spectrum) with two columns: m/z (first column, sorted increasingly) and intensity (second column). The method should return a list of these matrices, preserving spectrum order and supporting subsetting by index. If your backend pre-stores data as a list of matrices (like MsBackendMemory), the implementation is more efficient because it can return data directly without looping. Always validate that m/z values are sorted increasingly within each spectrum and that no NA values appear in m/z columns, as the Spectra design requires this.

## Related tools

- **Spectra** (Primary package providing the MsBackend virtual class and peaksData() generic; manages spectrum objects and delegates peak retrieval to backend implementations) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame and NumericList classes used to store and return spectra variables and peak data in structured form)
- **MsBackendMemory** (Reference backend implementation that stores peaks as a list of matrices, demonstrating the most efficient peaksData() approach) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMzR** (Example of a partially read-only backend that retrieves peaks on-the-fly from raw MS files; illustrates peaksData() for lazy-loaded backends) — https://github.com/RforMassSpectrometry/Spectra

## Examples

```
setMethod("peaksData", "MyMsBackend", function(object, ...) { mapply(function(mz, intensity) { cbind(mz = mz, intensity = intensity) }, object@mz, object@intensity, SIMPLIFY = FALSE) })
```

## Evaluation signals

- peaksData() returns a list with length equal to the number of spectra in the backend.
- Each element of the list is a numerical matrix with exactly 2 columns (m/z and intensity) and number of rows equal to the peak count for that spectrum.
- m/z values in each matrix are sorted in strictly increasing order with no NA values; intensity values are non-negative.
- extractByIndex() followed by peaksData() returns matrices in the same order as the indices, allowing duplicates and reordering.
- backendMerge() on two backends followed by peaksData() returns a concatenated list with no data loss or duplicate rows within each spectrum.

## Limitations

- peaksData() performance depends on whether the backend pre-stores data as matrices (fast, like MsBackendMemory) or must loop and merge from separate m/z and intensity slots (slower); backends retrieving data on-the-fly from external files (e.g., MsBackendMzR) may have additional I/O overhead.
- m/z values must be sorted increasingly and NA values are not supported; spectra with unsorted or missing m/z will violate the Spectra design contract.
- For very large datasets or read-only backends, calling peaksData() on the entire Spectra object may be memory-intensive; subsetting via extractByIndex() first is recommended.
- Some backends are partially or fully read-only and do not support peak data modification after extraction; peaksData() is for reading only in such cases.

## Evidence

- [intro] peaksData() design and return format: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum"
- [intro] m/z sorting requirement: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [intro] MsBackendMemory efficiency: "The `MsBackendMemory` backend for example stores the MS data already as a `list` of matrices"
- [intro] Implementation workflow for peaksData(): "peaksData() must loop over m/z and intensity slots to merge them into matrices for each spectrum; storing m/z and intensity in separate slots requires this looping but is less efficient than"
- [intro] extractByIndex() behavior with peaksData(): "The `extractByIndex()` and `[` methods allows to subset `MsBackend` objects. This operation is expected to reduce a `MsBackend` object to the selected spectra."
