---
name: spectra-variable-metadata-handling
description: Use when when designing a new MsBackend subclass or extending an existing
  backend to support mass spectrometry data import or representation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Spectra
  - S4Vectors
  - R
  - MsBackendMemory
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- The *Spectra* package defines an efficient infrastructure for storing and handling
  mass spectrometry spectra
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

# spectra-variable-metadata-handling

## Summary

Implement and manage spectra variables—core and custom metadata properties of individual mass spectrometry spectra—within MsBackend subclasses to enable consistent representation, validation, and access of spectral properties across different data storage backends. This skill is essential for ensuring that all spectra within a Spectra object expose a uniform API regardless of underlying data source (in-memory, on-disk, database, or streamed).

## When to use

When designing a new MsBackend subclass or extending an existing backend to support mass spectrometry data import or representation. You need this skill if you are creating a backend that must provide spectra variables (MS properties like retention time, precursor m/z, charge, collision energy, etc.) to Spectra objects, or if you need to validate that a backend correctly initializes and exposes core spectra variables with correct data types (character, numeric, integer, logical, or NumericList for m/z and intensity).

## When NOT to use

- If your input is already a complete Spectra object; use subsetting or merging methods instead of re-initializing backends.
- If you are implementing a read-only backend that retrieves all peak and variable data on-the-fly from an external resource (e.g., MsBackendMzR retrieving from mzML files); focus only on accessor methods, not storage slots.
- If m/z values are not sorted increasingly or contain missing values (NA); validate and sort input before passing to backendInitialize().

## Inputs

- data.frame or list containing spectra variables (retention time, MS level, polarity, precursor m/z, collision energy, etc.)
- list or NumericList of m/z values (one per spectrum, sorted increasingly, no NA)
- list or NumericList of intensity values (one per spectrum, corresponding to m/z)
- optional DataFrame parameter for complete spectra and peak data initialization
- metadata about data storage location (file path, database URI, memory indicator) and origin

## Outputs

- Initialized MsBackend instance with spectra variables and peak data stored in slots
- spectraData() DataFrame with columns for all spectra variables plus mz and intensity as NumericList
- spectraVariables() character vector listing all available variable names
- peaksData() list of numerical matrices (one per spectrum, with m/z and intensity columns)
- dataStorage and dataOrigin spectra variables set for each spectrum

## How to apply

First, define slots in your MsBackend subclass to store both general spectra variables (as a data.frame or DataFrame) and peak data (m/z and intensity). In backendInitialize(), load spectra variables from input sources and automatically set two special spectra variables: dataStorage (indicating storage mode: in-memory, file-based, database, etc.) and dataOrigin (indicating source file or resource). Extract and validate m/z and intensity values as NumericList objects, ensuring m/z values are sorted increasingly with no missing values. Call a helper validation function to verify that all core spectra variables (e.g., msLevel, polarity, precursorMz, precursorIntensity, rtime) conform to required data types. Implement spectraVariables() to return a character vector of all available variable names, and spectraData() to return a DataFrame containing all spectra variables plus m/z and intensity as NumericList columns. This architecture allows peaksData(), mz(), intensity(), and variable accessors to work uniformly across all backend implementations.

## Related tools

- **Spectra** (Main package providing the MsBackend virtual class API and Spectra class that consumes backend implementations; used to validate backend implementations and access spectra data uniformly) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame and NumericList classes for storing and manipulating spectra variables and peak data with type safety)
- **MsBackendMemory** (Reference in-memory backend implementation (within Spectra package) that stores peak data as list of matrices; demonstrates efficient spectraData() and peaksData() implementation) — https://github.com/RforMassSpectrometry/Spectra

## Evaluation signals

- spectraVariables() returns a character vector containing all core required variables (msLevel, polarity, precursorMz, precursorIntensity, rtime) and any custom variables, with no duplicates.
- spectraData() returns a DataFrame with correct number of rows (equal to number of spectra) and columns (one per variable plus mz and intensity); mz and intensity columns are NumericList objects.
- dataStorage and dataOrigin are present for every spectrum and correctly reflect the storage backend type and data source.
- mz() returns a NumericList with each element sorted increasingly and no NA values; intensity() returns a NumericList with same structure as mz().
- peaksData() returns a list of matrices with identical dimensions to mz/intensity pairs (one matrix per spectrum, two columns for m/z and intensity).
- Validation helper confirms all core spectra variable data types match MsBackend requirements (character, numeric, integer, logical, or NumericList).

## Limitations

- m/z values must be sorted increasingly with no missing values; backends cannot represent out-of-order or sparse peak data without pre-processing.
- Every spectrum must have the same set of spectra variables; irregular or ragged data structures require normalization before backend initialization.
- Spectra variables stored as data.frame or DataFrame may have memory overhead compared to specialized columnar storage; use on-disk or database backends (MsBackendMzR, MsBackendSql) for very large datasets to reduce memory footprint.
- Custom spectra variables beyond the core set are supported but may not be recognized by all downstream analysis functions; stick to core variables for maximum compatibility.

## Evidence

- [intro] Core spectra variables requirement: "a minimum required set of spectra variables **must** be provided by each backend"
- [intro] dataStorage and dataOrigin definition: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [intro] backendInitialize method purpose: "The `backendInitialize()` method is expected to be called after creating an instance of the backend class and should prepare (initialize) the backend"
- [intro] spectraData output format: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] spectraVariables return type: "The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables of the backend"
- [intro] m/z sorting and NA constraint: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [other] Task 003 validation workflow: "backendInitialize() accepts a data.frame with spectra variables and two lists with m/z and intensity values, automatically sets dataStorage and dataOrigin if missing, converts lists to NumericList"
