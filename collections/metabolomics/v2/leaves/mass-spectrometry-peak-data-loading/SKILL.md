---
name: mass-spectrometry-peak-data-loading
description: Use when when you have raw or parsed MS spectra data (m/z values, intensity
  values, and spectral metadata) and need to integrate it into a Spectra object for
  downstream processing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - S4Vectors
  - R
  - Spectra
  - MsBackendMemory
  - MsBackendMzR
  techniques:
  - mass-spectrometry
  license_tier: open
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

# mass-spectrometry-peak-data-loading

## Summary

Initialize a mass spectrometry backend by loading spectra variables, m/z, and intensity peak data into a structured NumericList representation. This skill implements the backendInitialize() method to populate MsBackend instances that mediate between raw MS data and the Spectra analysis framework.

## When to use

When you have raw or parsed MS spectra data (m/z values, intensity values, and spectral metadata) and need to integrate it into a Spectra object for downstream processing. Specifically, when creating or populating a custom MsBackend implementation, or when wrapping an existing data source (files, databases, in-memory structures) to expose it as a Spectra-compatible backend.

## When NOT to use

- When the input m/z values are not sorted increasingly or contain missing (NA) values — preprocessing or sorting must occur before peak data loading.
- When the input data already conforms to an existing, fully initialized backend (e.g., MsBackendMemory, MsBackendMzR) — use that backend directly instead of reimplementing.
- When only analyzing or querying spectra without modifying or creating a new backend — use the Spectra class accessor methods (mz(), intensity(), spectraData()) directly.

## Inputs

- data.frame or DataFrame with spectra variables (metadata columns)
- list or vector of m/z values (one per spectrum, each sorted and no NA)
- list or vector of intensity values (one per spectrum, matching m/z length)
- optional: complete DataFrame containing all peak and spectra variable data

## Outputs

- initialized MsBackend instance with populated spectraData() and peaksData()
- NumericList of m/z values (one per spectrum, sorted increasingly)
- NumericList of intensity values (one per spectrum, aligned to m/z)
- spectra variables including dataStorage and dataOrigin

## How to apply

Implement the backendInitialize() method to accept input parameters: a data.frame or DataFrame containing spectra variables (metadata), two lists or vectors containing m/z and intensity values for each spectrum, and optionally a complete DataFrame parameter. Extract and store m/z values as a NumericList, verifying they are sorted increasingly with no missing (NA) values per spectrum. Extract and store intensity values as a corresponding NumericList. Set the dataStorage spectra variable to indicate where peak data is located (e.g., 'memory', 'file', 'database'). Set the dataOrigin spectra variable to indicate the source of the data. Call a validation helper function to verify all core spectra variable data types match MsBackend API requirements (e.g., numeric, character, integer types). Return the initialized backend instance ready for use with Spectra objects.

## Related tools

- **Spectra** (High-level interface for MS spectra analysis; accepts initialized backends to provide data access and manipulation) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame and NumericList data structures used to store and validate spectra variables and peak data)
- **MsBackendMemory** (Default in-memory backend implementation; reference for implementing backendInitialize() and core accessor methods) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMzR** (On-disk backend that retrieves peaks on-the-fly; exemplifies partial read-only backends and backendInitialize() for file-based data) — https://github.com/RforMassSpectrometry/Spectra

## Evaluation signals

- m/z values in each spectrum are sorted increasingly with no NA values (verified by internal validation helper and mz() accessor)
- NumericList objects returned by mz() and intensity() have matching lengths (one element per spectrum in the backend)
- dataStorage and dataOrigin spectra variables are set and non-empty (verified via spectraData() DataFrame)
- All core spectra variable data types conform to MsBackend requirements (validated by helper function; no type mismatches)
- Backend instance is usable with Spectra class methods: spectraData(), peaksData(), spectraVariables(), and subsetting operations (extractByIndex) succeed without error

## Limitations

- Missing (NA) values for m/z are not supported; input m/z data must be complete for each spectrum.
- m/z values must be sorted increasingly within each spectrum; unsorted input will fail validation or produce incorrect results.
- Backends can be read-only (e.g., MsBackendMzR) or support partial modification (spectra variables but not peaks); backendInitialize() design depends on the backend's mutability contract.
- Large datasets may require on-disk backends (e.g., MsBackendMzR, MsBackendSql) rather than in-memory storage to avoid memory exhaustion; backendInitialize() must account for data source type.

## Evidence

- [other] Finding: core spectra variable data types validation: "validates core spectra variable data types via a helper function"
- [intro] Finding: m/z sorting and NA requirement: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [other] Workflow: NumericList conversion: "Extract and store m/z values as NumericList, verifying they are sorted increasingly with no missing values."
- [intro] Workflow: dataStorage and dataOrigin: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [intro] Finding: backendInitialize purpose: "The `backendInitialize()` method is expected to be called after creating an instance of the backend class and should prepare (initialize) the backend"
- [intro] Finding: spectraData DataFrame structure: "The `spectraData()` method should return the **full** spectra data within a `DataFrame` object"
- [intro] Finding: peaksData method: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum"
