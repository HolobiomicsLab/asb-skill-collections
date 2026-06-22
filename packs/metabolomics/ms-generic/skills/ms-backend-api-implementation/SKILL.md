---
name: ms-backend-api-implementation
description: Use when you have MS data in a new format or storage system (e.g., a custom database, HDF5 file, or proprietary raw file) and need to make it accessible to Spectra-based analysis workflows without forking the Spectra package itself.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - S4Vectors
  - R
  - Spectra
  - MsBackendMemory
  - MsBackendMzR
  - MsBackendSql
  techniques:
  - mass-spectrometry
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

# ms-backend-api-implementation

## Summary

Implement a custom MsBackend subclass to integrate new mass spectrometry data representations into the Spectra framework. This skill enables seamless access to MS peaks and spectra variables from diverse sources (in-memory, on-disk, database) by conforming to the virtual MsBackend API.

## When to use

You have MS data in a new format or storage system (e.g., a custom database, HDF5 file, or proprietary raw file) and need to make it accessible to Spectra-based analysis workflows without forking the Spectra package itself. You need either read-only access (implementing only accessor methods) or read-write capability (implementing replacement methods as well).

## When NOT to use

- You are building an analysis pipeline that only uses existing backends (MsBackendMemory, MsBackendMzR, MsBackendSql, etc.); implementing a new backend is unnecessary overhead.
- Your MS data is already in mzML, mzXML, or CDF format; use MsBackendMzR instead.
- You need a purely read-only backend for a database or spectral library; consider extending MsBackendCached instead to reduce boilerplate.

## Inputs

- S4 class skeleton extending MsBackend
- MS data source (file, database, or in-memory structure)
- User-supplied spectra variables (msLevel, rtime, etc.)
- Peak data arrays (m/z and intensity values per spectrum)

## Outputs

- Functional MsBackend subclass instance
- DataFrame with all spectra variables (core + user-supplied)
- NumericList of m/z values (one list element per spectrum)
- NumericList of intensity values (one list element per spectrum)
- Spectra object capable of downstream analysis

## How to apply

Define an S4 class extending the virtual MsBackend with three slots: spectraVars (data.frame for general spectra variables), mz (NumericList for m/z values), and intensity (NumericList for intensity values). Implement the 9 required accessor methods: spectraData() to return a DataFrame combining all variables, spectraVariables() to list available variable names, backendInitialize() to load data, peaksData() to extract m/z–intensity matrices, extractByIndex() to subset by spectrum index, backendMerge() to combine backends, intensity() and mz() to return peak NumericLists, and spectraNames() for optional spectrum identifiers. For read-write backends, also implement replacement methods (intensity<-, mz<-, spectraData<-, peaksData<-) with validation—e.g., using is.unsorted() to ensure m/z values are strictly increasing within each spectrum. Use fillCoreSpectraVariables() internally to populate missing core spectra variables (e.g., centroided, polarity) with NA values when not provided by the user.

## Related tools

- **Spectra** (Core package providing the virtual MsBackend class and Spectra container; implements spectraData(), peaksData(), and other high-level accessor methods that dispatch to backend implementations) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides the DataFrame and NumericList container classes used to store and return spectra data and peak values)
- **R** (Language and runtime for implementing S4 methods and backend class definitions)
- **MsBackendMemory** (Reference in-memory backend implementation; shows patterns for implementing spectraData(), intensity(), mz(), and replacement methods) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMzR** (Reference on-disk backend implementation; demonstrates how to retrieve peaks data on-the-fly from files while keeping general spectra variables in memory) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendSql** (Reference SQL-based backend; illustrates database-backed storage and lazy loading patterns) — https://github.com/rformassspectrometry/MsBackendSql

## Examples

```
# Define and initialize a custom MsBackendTest backend
library(Spectra)
setClass('MsBackendTest', contains='MsBackend', slots=c(spectraVars='data.frame', mz='NumericList', intensity='NumericList'))
myBackend <- new('MsBackendTest')
myBackend <- backendInitialize(myBackend, msLevel=c(2L, 2L), rtime=c(123.4, 456.7), mz=list(c(100.1, 200.2), c(150.3, 250.4)), intensity=list(c(10, 20), c(30, 40)))
spectra_data <- spectraData(myBackend)
print(spectra_data)
```

## Evaluation signals

- spectraData() returns a DataFrame containing all core spectra variables (centroided, polarity, etc.) plus user-supplied variables, with missing core variables filled as NA values.
- spectraVariables() returns a character vector listing all available variable names, including both core and user-supplied ones.
- mz<- and intensity<- replacement methods accept only increasingly sorted values and raise a stop error with message 'values need to be increasingly sorted within each spectrum' when validation fails.
- extractByIndex() subsets the backend correctly by spectrum index and preserves the correspondence between spectraVars rows and mz/intensity list elements.
- backendMerge() combines multiple backend instances of the same type and returns a single merged backend with concatenated spectraVars and mz/intensity lists.

## Limitations

- Each spectrum's m/z values must be strictly increasingly sorted; backends that cannot guarantee this constraint must sort or reject data at initialization time.
- Core spectra variables (dataStorage, dataOrigin, centroided, polarity, etc.) must be provided by every backend; if not supplied by the user, they are filled with NA, which may cause issues downstream if NA is not a valid value for analysis.
- Read-write backends require validation in replacement methods (e.g., is.unsorted() for m/z) which adds computational overhead; read-only backends avoid this cost.
- The NumericList structure assumes each spectrum has a variable number of peaks; backends must adapt this structure to their underlying data representation, which may introduce conversion overhead.

## Evidence

- [intro] The MsBackend virtual class defines the API that new backend classes need to implement to be used with the Spectra object.: "The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object."
- [intro] Slots must include spectraVars (data.frame), mz (NumericList), and intensity (NumericList) where each row in spectraVars represents one spectrum.: "slots = c(
             spectraVars = "data.frame",
             mz = "NumericList",
             intensity = "NumericList"
         )"
- [intro] spectraData() should return the full spectra data within a backend as a DataFrame object.: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] spectraVariables() method should return a character vector with the names of all available spectra variables of the backend.: "The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables of the backend."
- [other] fillCoreSpectraVariables() is used internally to ensure all core spectra variables are present with NA for missing ones.: "The spectraData() implementation for MsBackendTest uses fillCoreSpectraVariables() to ensure that all core spectra variables are returned, filling missing ones with NA values"
- [intro] mz values within each spectrum are expected to be sorted increasingly.: "m/z values within each spectrum are expected to be sorted increasingly."
- [other] mz<- uses efficient vectorised is.unsorted() on NumericList rather than vapply.: "The mz<- replacement method uses the efficient is.unsorted() implementation for NumericList rather than vapply, and raises a stop error when any spectrum has unsorted m/z values"
- [other] Nine required accessor methods and seven data replacement methods must be implemented.: "MsBackendTest requires implementation of 9 required accessor methods (spectraData, spectraVariables, backendInitialize, peaksData, extractByIndex, backendMerge, intensity, mz, spectraNames) plus 7"
- [intro] This separation allows defining new alternative data representations integrated seamlessly into Spectra-based analysis workflows.: "this separation allows to define new, alternative, data representations and integrate them seamlessly into a `Spectra`-based data analysis workflow."
- [intro] Read-only backends need only implement accessor methods, not data replacement methods.: "`MsBackend` implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods."
