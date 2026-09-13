---
name: spectra-data-representation-backends
description: Use when you are creating a new backend to expose MS data (m/z, intensity,
  retention time, and other spectral properties) from a specific storage format or
  data source (e.g., mzML files, SQL databases, in-memory matrices, or spectral libraries)
  to Spectra objects.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Spectra
  - S4Vectors
  - R
  - MSnbase
  - MsBackendMzR
  - MsBackendSql
  - MsBackendMemory
  techniques:
  - LC-MS
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

# spectra-data-representation-backends

## Summary

Design and implement MsBackend classes that provide mass spectrometry data to Spectra objects while avoiding circular dependencies between spectraData() and spectraVariables() methods. This skill bridges MS data storage (in-memory, on-disk, or database) with the Spectra analysis framework.

## When to use

You are creating a new backend to expose MS data (m/z, intensity, retention time, and other spectral properties) from a specific storage format or data source (e.g., mzML files, SQL databases, in-memory matrices, or spectral libraries) to Spectra objects. The backend must handle multiple spectra with internally sorted m/z values and provide both accessor and optional replacement methods for spectra variables.

## When NOT to use

- You are not creating a new data source type — use an existing backend (MsBackendMemory, MsBackendMzR, MsBackendSql, etc.) if your MS data already fits a supported format.
- Your spectra have missing or unsorted m/z values — backends require m/z values to be sorted increasingly within each spectrum and do not support NA values for m/z.
- You need analysis-level functionality (filtering, processing, visualization) rather than data storage/provision — use the Spectra class directly instead of implementing a new backend.

## Inputs

- MS data source (mzML/mzXML/CDF files, SQL database, HDF5 file, in-memory matrix list, or spectral library file)
- Spectra variable metadata (retention time, scan index, precursor m/z, collision energy, etc.)
- Storage backend specification (read-only or read-write mode)

## Outputs

- MsBackend subclass instance with implemented spectraData(), spectraVariables(), peaksData(), mz(), and intensity() methods
- DataFrame object containing all spectra variables with m/z and intensity as NumericList columns
- Character vector of spectra variable names (union of core and backend-specific variables)

## How to apply

Extend the virtual MsBackend class and implement core methods in this order: (1) backendInitialize() to load/prepare MS data and populate dataStorage and dataOrigin variables; (2) spectraVariables() as a character vector returning the union of core variable names ('mz', 'intensity', 'rtime', 'scanIndex', etc.) and backend-specific column names — this method must NOT call spectraData() to prevent circularity; (3) spectraData() to call fillCoreSpectraVariables() to populate missing core spectra variables into a DataFrame, extract backend-specific columns from internal storage, and combine them using S4Vectors::DataFrame(), with m/z and intensity returned as NumericList columns when requested; (4) peaksData() to extract m/z and intensity as a list of numerical matrices with m/z values sorted increasingly; (5) intensity() and mz() as NumericList accessors; (6) extractByIndex() and backendMerge() for subsetting and combining backends. Ensure spectraData() and spectraVariables() do not call each other to prevent infinite recursion. For read-only backends, implement only accessor methods; for partially read-only backends (e.g., MsBackendMzR), implement replacement methods for spectra variables but not peaks data.

## Related tools

- **Spectra** (R package defining the virtual MsBackend class and providing fillCoreSpectraVariables(), Spectra class for analysis, and utility backends (MsBackendMemory, MsBackendMzR, MsBackendDataFrame)) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Bioconductor package providing DataFrame object for storing and returning combined spectra data with support for NumericList columns)
- **MsBackendMzR** (Example backend retrieving m/z and intensity on-the-fly from mzML/mzXML/CDF files using mzR package while keeping general spectra variables in memory)
- **MsBackendSql** (Example backend storing all MS data in SQL database with minimal memory footprint for large datasets) — https://github.com/rformassspectrometry/MsBackendSql
- **MsBackendMemory** (Example default backend keeping all data in-memory, optimized for fast processing of smaller datasets)

## Examples

```
setClass('MsBackendExample', contains = 'MsBackend', slots = c(data = 'data.frame', peaks = 'list')); setMethod('spectraVariables', 'MsBackendExample', function(object) union(c('mz', 'intensity', 'rtime', 'scanIndex'), names(object@data))); setMethod('spectraData', 'MsBackendExample', function(object, columns = spectraVariables(object)) { df <- fillCoreSpectraVariables(object@data[, intersect(names(object@data), columns)]); df$mz <- IRanges::NumericList(object@peaks[, 1]); df$intensity <- IRanges::NumericList(object@peaks[, 2]); df })
```

## Evaluation signals

- spectraData() returns a DataFrame with all core variables (mz, intensity, rtime, scanIndex) and backend-specific columns; m/z and intensity columns are NumericList objects; no NA values present in m/z columns
- spectraVariables() returns a character vector containing the union of core variable names and backend column names with no duplicates
- No circular function calls: spectraVariables() does not call spectraData() and spectraData() does not call spectraVariables()
- peaksData() returns a list of numerical matrices with m/z values sorted increasingly within each matrix; matrix row count matches spectrum peak count
- extractByIndex() correctly subsets backend to selected spectra; backendMerge() combines multiple backend instances without data loss or reordering

## Limitations

- m/z values within each spectrum must be sorted increasingly and cannot contain NA values — unsorted or incomplete peak data will violate backend contract
- Backends can be read-only (e.g., spectral libraries, database queries) or partially read-only (e.g., MsBackendMzR allows spectra variable modification but not peak data modification) — implement only the data accessor or replacement methods appropriate to your data source
- Circular dependencies between spectraData() and spectraVariables() cause infinite recursion — fillCoreSpectraVariables() must be called inside spectraData(), not spectraVariables()
- For parallel processing, backends may need to implement backendParallelFactor() to suggest a preferred splitting factor for load balancing

## Evidence

- [intro] core_api_definition: "The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object."
- [intro] spectra_data_representation: "One `Spectra` object is supposed to contain MS (spectral) data of multiple MS spectra. m/z values within each spectrum are expected to be sorted increasingly."
- [intro] core_variables_requirement: "Properties of a spectrum are called *spectra variables*. While backends can define their own properties, a minimum required set of spectra variables **must** be provided by each backend"
- [intro] mz_constraints: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [intro] spectraData_method_design: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] spectraVariables_method_design: "The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables of the backend"
- [intro] peaksData_method_design: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum"
- [intro] backend_read_only_flexibility: "`MsBackend` implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods."
- [intro] partially_read_only_example: "Backends can also be *partially* read-only, such as the `MsBackendMzR`. This backend allows for example to change spectra variables, but not the peaks data"
- [other] fillCoreSpectraVariables_usage: "spectraData() uses fillCoreSpectraVariables() to populate missing core spectra variables into a DataFrame, while spectraVariables() returns the union of core variable names and backend column names"
- [other] circularity_prevention: "Verify that spectraVariables() does not call spectraData() and that spectraData() does not call spectraVariables() to prevent circular dependencies."
