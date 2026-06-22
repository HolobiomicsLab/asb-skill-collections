---
name: dataframe-construction-from-backend-sources
description: Use when when implementing a new MsBackend subclass that stores only a subset of core spectra variables (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - S4Vectors
  - R
  - Spectra
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

# dataframe-construction-from-backend-sources

## Summary

Construct a DataFrame object containing complete spectra variables by implementing a spectraData() method that retrieves user-supplied variables from a backend storage slot and fills missing core spectra variables with NA values. This ensures uniform access to all expected spectra metadata across heterogeneous MsBackend implementations.

## When to use

When implementing a new MsBackend subclass that stores only a subset of core spectra variables (e.g., msLevel, rtime, polarity) and you need to expose all core spectra variables through a single accessor method without breaking downstream Spectra workflows that expect complete variable coverage.

## When NOT to use

- The backend already stores and returns all core spectra variables explicitly; fillCoreSpectraVariables() is redundant.
- The analysis only requires a subset of spectra variables; using fillCoreSpectraVariables() adds unnecessary NA columns and memory overhead.
- The backend is read-only but does not extend MsBackendCached or a similar framework; core variable injection may conflict with immutability contracts.

## Inputs

- MsBackend subclass instance with spectra variables slot (data.frame, DataFrame, or similar columnar structure)
- User-supplied spectra variables (minimum: msLevel, rtime, or other non-core metadata)
- Peak data (m/z and intensity values as NumericList or matrix-like structure)

## Outputs

- DataFrame object with columns for all core spectra variables (centroided, polarity, precursorMz, etc.) and user-supplied variables
- NA-filled columns for any core spectra variables not explicitly stored in the backend

## How to apply

Implement spectraData() to return a DataFrame by first extracting user-supplied spectra variables stored in the backend's dedicated slot (e.g., data.frame or DataFrame). Then invoke fillCoreSpectraVariables() internally, passing the extracted variables and the backend instance. fillCoreSpectraVariables() will identify which core spectra variables are absent from the user-supplied set and inject them as columns filled with NA values. The resulting DataFrame will contain both the original user-supplied variables and all missing core variables at NA, ensuring the returned object matches the schema expected by Spectra workflows without requiring the backend to explicitly pre-populate every core variable.

## Related tools

- **Spectra** (Framework providing the MsBackend virtual class, fillCoreSpectraVariables() utility function, and Spectra object infrastructure that consumes the constructed DataFrame) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides the DataFrame class used to store and return spectra variables in tabular form)

## Evaluation signals

- Returned DataFrame contains all core spectra variables (centroided, polarity, precursorMz, dataStorage, dataOrigin, etc.) as columns.
- Columns corresponding to core variables not supplied by the user are present and filled entirely with NA values (not absent or empty).
- User-supplied spectra variables retain their original values and data types in the returned DataFrame.
- spectraVariables() method returns the union of user-supplied and core variable names, matching the column names of the DataFrame returned by spectraData().
- Downstream Spectra workflows consuming spectraData() output do not raise 'missing variable' or schema mismatch errors.

## Limitations

- fillCoreSpectraVariables() does not infer or populate missing core variable values from peak data or other backend sources; it only inserts NA. Backends requiring actual core variable values must provide them explicitly.
- The approach scales linearly with the number of core spectra variables; very large backends may incur memory overhead from the NA-filled columns if not using lazy evaluation or sparse representations.
- Core spectra variables are defined statically by the Spectra package; custom user-defined variables are not automatically recognized as 'core' and will not be filled in by fillCoreSpectraVariables().

## Evidence

- [intro] The spectraData() method should return the **full** spectra data within a backend as a `DataFrame` object: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [other] spectraData() implementation uses fillCoreSpectraVariables() to ensure all core spectra variables are returned with NA for missing ones: "The spectraData() implementation for MsBackendTest uses fillCoreSpectraVariables() to ensure that all core spectra variables are returned, filling missing ones with NA values"
- [intro] Core spectra variables must be provided by each backend with dataStorage and dataOrigin as special required variables: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [other] Workflow step for implementing spectraData() with fillCoreSpectraVariables(): "Implement spectraData() method to return spectra variables as a DataFrame, invoking fillCoreSpectraVariables() internally to populate missing core variables with NA values"
