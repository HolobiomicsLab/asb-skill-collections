---
name: mass-spectrometry-data-representation
description: Use when you need to store or retrieve mass spectrometry spectra (m/z and intensity pairs) from a novel data source or storage medium (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - S4Vectors
  - R
  - Spectra
  - MsBackendMemory
  - MsBackendMzR
  - MsBackendDataFrame
  - MsBackendMgf
  - MsBackendSql
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`
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
---

# mass-spectrometry-data-representation

## Summary

Design and implement custom MsBackend subclasses to represent mass spectrometry spectral data in memory, on-disk, or from external sources, decoupling data storage from analysis workflows. This skill enables extension of the Spectra package ecosystem with new backend implementations for diverse MS data formats and storage strategies.

## When to use

You need to store or retrieve mass spectrometry spectra (m/z and intensity pairs) from a novel data source or storage medium (e.g., a proprietary file format, a SQL database, HDF5 files, or an API), and want to integrate it seamlessly into Spectra-based analysis workflows without rewriting downstream analysis code.

## When NOT to use

- You are working with standard mzML, mzXML, or CDF files: use MsBackendMzR instead.
- Your data is already in memory as a simple list of matrices and you need only basic accessor methods: MsBackendMemory may be sufficient without custom implementation.
- You require only read-only access to a remote database (SQL, MassBank): existing backends like MsBackendMassbankSql, MsBackendOfflineSql, or MsBackendSql already implement this pattern.

## Inputs

- MsBackend virtual class definition (S4 template)
- Raw mass spectrometry data from custom source (file, database, API, or memory structure)
- Spectrum-level metadata (retention time, precursor m/z, scan number, etc.)
- Peak data (m/z-intensity pairs per spectrum)

## Outputs

- Custom MsBackend subclass instance
- Spectra object wrapping the backend
- DataFrame of full spectra data (via spectraData())
- NumericList of m/z values per spectrum
- NumericList of intensity values per spectrum
- List of matrices (m/z × intensity pairs) via peaksData()

## How to apply

Define an S4 class extending the virtual MsBackend with three slots: spectraVars (data.frame for spectrum-level metadata), mz (NumericList for m/z values), and intensity (NumericList for peak intensities). Implement the nine required accessor methods (spectraData, spectraVariables, backendInitialize, peaksData, extractByIndex, backendMerge, intensity, mz, spectraNames) to expose your data representation through the standard Spectra API. For read-write backends, also implement seven replacement methods (intensity<-, mz<-, peaksData<-, spectraData<-, selectSpectraVariables, dataStorage<-, spectraNames<-) to enable data modification. Ensure m/z values within each spectrum are sorted in increasing order, and include mandatory spectra variables dataStorage and dataOrigin to track storage location and data provenance. The backendInitialize() method should prepare and load your specific data format upon backend instantiation.

## Related tools

- **Spectra** (Core package defining the MsBackend virtual class API and Spectra container; provides infrastructure to load, manipulate, and analyze MS spectra using any conformant backend.) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame and NumericList classes required to store and return spectra metadata and peak data from backend methods.)
- **MsBackendMemory** (Reference in-memory backend implementation in Spectra; serves as example for slots, required methods, and data replacement patterns.) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMzR** (On-the-fly file access backend; demonstrates lazy loading of peaks data from external files while keeping spectra variables in memory.) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendDataFrame** (Alternative in-memory backend using DataFrame for variable storage; shows how to support S4 objects as spectra variables.) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMgf** (Reference for import/export backend; extends MsBackendDataFrame to read/write MGF format, demonstrating file parsing integration.) — https://github.com/RforMassSpectrometry/MsBackendMgf
- **MsBackendSql** (Database-backed backend; illustrates how to implement on-demand data retrieval from SQL databases to minimize memory footprint.) — https://github.com/RforMassSpectrometry/MsBackendSql

## Examples

```
setClass('MsBackendTest', contains = 'MsBackend', slots = c(spectraVars = 'data.frame', mz = 'NumericList', intensity = 'NumericList')); setMethod('backendInitialize', 'MsBackendTest', function(object, data, ...) { object@spectraVars <- data$metadata; object@mz <- data$mz; object@intensity <- data$intensity; validObject(object); object })
```

## Evaluation signals

- Instantiate a custom backend with sample data and confirm spectraData() returns a valid DataFrame with all spectra variables and correct row count (one row per spectrum).
- Call spectraVariables() and verify it returns a character vector including at least the mandatory dataStorage and dataOrigin variables.
- Execute peaksData() on a subset and confirm it returns a list of numeric matrices where each matrix has two columns (m/z and intensity) with m/z values in increasing order.
- Subset the backend using extractByIndex() or [ operator and verify the resulting object contains only the selected spectra with consistent metadata and peak data.
- Wrap the backend in a Spectra object and run standard Spectra operations (filtering, plotting, spectral similarity) without errors; confirm the object integrates seamlessly into downstream workflows.

## Limitations

- The MsBackend API requires careful implementation of all nine accessor methods and seven replacement methods for full read-write functionality; incomplete or inconsistent implementations will cause subtle data loss or corruption when using Spectra operations.
- m/z values within each spectrum must be strictly sorted in increasing order; backends that fail to enforce this constraint will produce incorrect results in mass accuracy calculations and spectral matching.
- The dataStorage and dataOrigin variables are mandatory: backends that omit these will not conform to the Spectra specification and may break downstream tools that depend on provenance tracking.
- Memory-resident backends (those storing all data in the backend slots) do not scale to very large datasets; SQL, HDF5, or on-the-fly file access backends are preferable for multi-gigabyte MS experiments.
- The backendMerge() method must correctly handle merging of backends with different or overlapping spectra variables; incorrect implementations can introduce NA values or misaligned peak data across merged objects.

## Evidence

- [intro] The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object.: "The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object."
- [intro] Each `Spectra` object contains an implementation of such a `MsBackend` within its `@backend` slot which provides the MS data to the `Spectra` object.: "Each `Spectra` object contains an implementation of such a `MsBackend` within its `@backend` slot which provides the MS data to the `Spectra` object."
- [intro] this separation allows to define new, alternative, data representations and integrate them seamlessly into a `Spectra`-based data analysis workflow.: "this separation allows to define new, alternative, data representations and integrate them seamlessly into a `Spectra`-based data analysis workflow."
- [intro] m/z values within each spectrum are expected to be sorted increasingly.: "m/z values within each spectrum are expected to be sorted increasingly."
- [intro] `dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [intro] The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables of the backend.: "The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables of the backend."
- [intro] The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum.: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum."
- [readme] The *Spectra* package separates the code for the analysis of MS data from the code needed to import, represent and provide the data.: "The *Spectra* package separates the code for the analysis of MS data from the code needed to import, represent and provide the data."
- [readme] *Spectra* provides different implementations (backends) to store mass spectrometry data. These comprise backends tuned for fast data access and processing and backends for very large data sets ensuring a small memory footprint.: "*Spectra* provides different implementations (backends) to store mass spectrometry data. These comprise backends tuned for fast data access and processing and backends for very large data sets"
