---
name: peak-data-extraction-and-formatting
description: Use when when you have initialized an MsBackend subclass (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - S4Vectors
  - R
  - Spectra
  - IRanges
  - MsBackendMemory
  - MsBackendMzR
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- return the **full** spectra data within a backend as a `DataFrame` object (defined
  in the `r Biocpkg("S4Vectors")`
- library(Spectra) library(IRanges)
- library(Spectra)
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

# peak-data-extraction-and-formatting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract m/z and intensity peak values from mass spectrometry backend objects and format them as NumericList or matrix structures for downstream analysis. This skill bridges MsBackend data storage and Spectra-based processing by implementing standardized accessor methods that present raw peak data in expected formats.

## When to use

When you have initialized an MsBackend subclass (e.g., MsBackendTest, MsBackendMemory) containing spectral peak data stored as NumericList or matrix objects and need to retrieve, subset, or reformat m/z and intensity values for processing, visualization, or comparison within a Spectra workflow.

## When NOT to use

- Input backend is read-only (e.g., MsBackendMzR, MsBackendCached) and you need to modify peak values — use intensity<- and mz<- replacement methods instead, which are only implemented for writable backends.
- You need only summary statistics (e.g., precursor m/z, total intensity) rather than full peak arrays — use spectraData() or dedicated accessor methods instead.
- Peak data is already in expected format (NumericList or matrix) and you are not extracting from raw storage — skip this skill and work directly with the formatted peaks.

## Inputs

- MsBackend subclass instance (e.g., MsBackendTest) with populated intensity and mz slots
- spectrum indices or boolean mask for subsetting (optional)
- spectra variable names to filter by (optional)

## Outputs

- NumericList: peak m/z values, one element per spectrum
- NumericList: peak intensity values, one element per spectrum
- list of matrices: combined m/z and intensity as [mz, intensity] rows per spectrum (from peaksData())
- DataFrame: extracted peaks data integrated with spectrum metadata (from peaksData())

## How to apply

Implement the peaksData() method to extract m/z and intensity values from the backend's internal storage (NumericList slots or database) and return them as a list of matrices with one row per spectrum; implement the intensity() and mz() accessor methods to return NumericList objects preserving the one-spectrum-per-element structure; ensure m/z values are sorted increasingly within each spectrum as required by the API. Use extractByIndex() or [ subsetting to isolate specific spectra before peak extraction when processing subsets. Validate that output dimensionality matches the input spectrum count and that all m/z values are numeric and sorted.

## Related tools

- **Spectra** (Container package defining MsBackend virtual class and Spectra object that uses backend instances via @backend slot to provide peak data access) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides NumericList and DataFrame data structures for storing and returning peak m/z and intensity values with list-like semantics)
- **IRanges** (Imported by Spectra; provides underlying infrastructure for efficient range and list operations on peak data)
- **MsBackendMemory** (Reference in-memory backend implementation that stores peaks as list of matrices; serves as model for implementing peaksData(), intensity(), and mz() methods) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMzR** (Example on-the-fly backend that retrieves peaks from raw MS files; demonstrates lazy loading pattern in peaksData() without storing full NumericList in slots) — https://github.com/RforMassSpectrometry/Spectra

## Evaluation signals

- peaksData() returns a list with length equal to the number of spectra in the backend, with each element being a 2-row matrix (mz, intensity) or named list containing 'mz' and 'intensity' columns.
- intensity() and mz() each return a NumericList object with length equal to spectrum count, where each element is a numeric vector corresponding to one spectrum's peaks; all NumericList elements can be accessed via integer or logical indexing.
- All m/z values are numeric, finite, and increasingly sorted within each spectrum (checksum: min(diff(mz)) >= 0 for each spectrum).
- Subsetting via extractByIndex() or [ on the backend followed by peak extraction returns correctly reduced peak arrays matching the selected spectrum indices.
- Round-trip test: extract peaks, verify dimensions match input spectra count, verify no NAs or infinities in output, and verify spectra variable count is consistent before and after subsetting.

## Limitations

- Peak extraction assumes m/z and intensity data are already sorted and validated at backend initialization; no automatic sorting or duplicate-removal is performed by these accessor methods.
- For very large datasets or on-disk backends (e.g., MsBackendMzR), calling peaksData() on the entire backend may trigger full file I/O and consume significant memory; use extractByIndex() to process spectra in batches.
- Read-only backends (e.g., MsBackendMzR, MsBackendCached, MsBackendMassbankSql) do not implement intensity<-, mz<-, or peaksData<- replacement methods; peak modification requires copying data to a writable backend like MsBackendMemory.
- The API expects core variables 'dataStorage' and 'dataOrigin' to be present in every backend; peaks extraction will fail if these required variables are missing from spectraVars.

## Evidence

- [intro] The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum.: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum."
- [intro] Extract the intensity values for each spectrum in the backend. The result is expected to be a `NumericList`: "Extract the intensity values for each spectrum in the backend. The result is expected to be a `NumericList`"
- [intro] m/z values within each spectrum are expected to be sorted increasingly.: "m/z values within each spectrum are expected to be sorted increasingly."
- [intro] Each `Spectra` object contains an implementation of such a `MsBackend` within its `@backend` slot which provides the MS data to the `Spectra` object.: "Each `Spectra` object contains an implementation of such a `MsBackend` within its `@backend` slot which provides the MS data to the `Spectra` object."
- [intro] slots = c(
             spectraVars = "data.frame",
             mz = "NumericList",
             intensity = "NumericList"
         ): "slots = c(
             spectraVars = "data.frame",
             mz = "NumericList",
             intensity = "NumericList"
         )"
