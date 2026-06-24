---
name: storage-origin-metadata-assignment
description: Use when when implementing or initializing an MsBackend subclass to handle
  mass spectrometry data, you must assign dataStorage and dataOrigin variables after
  loading m/z and intensity values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - S4Vectors
  - R
  - Spectra
  - MsBackendMemory
  - MsBackendMzR
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

# storage-origin-metadata-assignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assign dataStorage and dataOrigin spectra variables to each spectrum in an MsBackend instance to document where peak data is physically stored and from which source it was derived. This metadata is essential for backend initialization and enables Spectra objects to track data provenance and access patterns.

## When to use

When implementing or initializing an MsBackend subclass to handle mass spectrometry data, you must assign dataStorage and dataOrigin variables after loading m/z and intensity values. This is required during backendInitialize() to document whether data resides in memory, on disk, or in a database, and to record the original data source (e.g., raw MS file, database, or computational result).

## When NOT to use

- Backend is read-only and dataStorage/dataOrigin are already embedded in the data source (e.g., MsBackendMzR retrieving live data from mzML files may set these at data access time rather than initialization)
- Working with a Spectra object that has already been fully initialized; metadata assignment occurs at the backend level, not on instantiated Spectra objects
- Data source does not require tracking provenance or the analysis workflow does not need to distinguish between multiple storage backends

## Inputs

- data.frame with spectra variables (metadata properties)
- list of m/z values (numeric vectors, sorted increasingly)
- list of intensity values (numeric vectors, corresponding to m/z)
- optional: complete DataFrame containing all peak and spectra variable data

## Outputs

- initialized MsBackend instance with dataStorage and dataOrigin assigned
- internal spectra variables DataFrame/list with populated dataStorage and dataOrigin columns

## How to apply

Within the backendInitialize() method, after extracting and validating m/z and intensity data as NumericList objects, explicitly set the dataStorage spectra variable to indicate the physical storage location (e.g., 'memory', 'hdf5file', 'mzML') and the dataOrigin variable to indicate the source from which the data derived (e.g., file path, database name, or processing method). These are special spectra variables that apply per-spectrum and must be assigned before returning the initialized backend. Use a helper validation function to verify that all core spectra variable data types, including these two, conform to MsBackend requirements. The assignment typically occurs as part of populating the internal data storage slots (e.g., a DataFrame or list structure) that the spectraData() method will later retrieve.

## Related tools

- **Spectra** (S4 class framework that consumes MsBackend instances; backendInitialize() is called on backend instances to populate dataStorage and dataOrigin for Spectra objects) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame class used to store and organize spectra variables including dataStorage and dataOrigin columns)
- **MsBackendMemory** (Example backend implementation (in Spectra package) that stores all data in memory and must set dataStorage='memory' and dataOrigin appropriately during initialization) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMzR** (Example backend that retrieves peak data on-the-fly from mzML/mzXML/CDF files; sets dataStorage to file path and dataOrigin to source file during initialization) — https://github.com/RforMassSpectrometry/Spectra

## Examples

```
# R example: initialize a custom MsBackend subclass with dataStorage and dataOrigin
setMethod('backendInitialize', 'MyMsBackend',
  function(object, data, mz, intensity, ...) {
    object@data <- DataFrame(data, dataStorage='memory', dataOrigin='custom_source')
    object@mz <- IRanges::NumericList(mz)
    object@intensity <- IRanges::NumericList(intensity)
    return(object)
  }
)
```

## Evaluation signals

- dataStorage column exists in backend's spectraData() output and contains valid storage location identifiers for each spectrum (e.g., 'memory', 'hdf5file', file path)
- dataOrigin column exists in backend's spectraData() output and contains source identifiers for each spectrum (e.g., file name, database connection string, processing method)
- Helper validation function confirms dataStorage and dataOrigin data types match MsBackend core spectra variable requirements (typically character/factor)
- Spectra object successfully accesses and displays dataStorage and dataOrigin values via spectraData() without errors or missing values
- Backend can be merged with other initialized backends of the same type and dataStorage/dataOrigin values are preserved or updated appropriately in the merged result

## Limitations

- m/z values must be sorted increasingly and contain no missing (NA) values; dataStorage/dataOrigin assignment does not validate this constraint—it must be enforced before or alongside these assignments
- If dataStorage and dataOrigin are not set during backendInitialize(), downstream operations (subsetting, merging, parallel processing) may fail or produce misleading metadata
- Partially read-only backends (e.g., MsBackendMzR) may allow modification of spectra variables including dataOrigin after initialization, which can create inconsistency if the actual data location has not changed
- The article provides design rationale but does not specify canonical values for dataStorage or dataOrigin; different backend implementations may use inconsistent naming conventions

## Evidence

- [intro] dataStorage and dataOrigin are two special spectra variables that define for each spectrum where the data is stored and from where the data derived: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [intro] backendInitialize() is expected to be called after creating an instance of the backend class and should prepare (initialize) the backend, setting required spectra variables: "The `backendInitialize()` method is expected to be called after creating an instance of the backend class and should prepare (initialize) the backend"
- [other] Core spectra variables validation must occur during initialization via a helper function: "Call a helper validation function to verify all core spectra variable data types match MsBackend requirements"
- [results] backendInitialize() accepts spectra variables, m/z/intensity lists, and optional full DataFrame; automatically sets dataStorage and dataOrigin if missing: "backendInitialize() accepts a data.frame with spectra variables and two lists with m/z and intensity values, automatically sets dataStorage and dataOrigin if missing"
- [intro] Spectra variables are properties of spectra that must include a minimum required set: "Properties of a spectrum are called *spectra variables*. While backends can define their own properties, a minimum required set of spectra variables **must** be provided by each backend"
