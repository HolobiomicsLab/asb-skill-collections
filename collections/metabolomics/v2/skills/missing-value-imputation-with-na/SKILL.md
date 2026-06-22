---
name: missing-value-imputation-with-na
description: Use when you are implementing a custom MsBackend subclass for the Spectra package and need to ensure that spectraData() returns all core spectra variables (e.g., centroided, polarity, collisionEnergy) regardless of which ones are explicitly stored in your backend.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3391
  edam_topics:
  - http://edamontology.org/topic_0121
  tools:
  - S4Vectors
  - R
  - Spectra
  - MsBackendMemory
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

# missing-value-imputation-with-na

## Summary

Populate missing core spectra variables in a mass spectrometry backend by filling them with NA values, ensuring that spectraData() returns a complete DataFrame with all expected columns even when only a subset of user-supplied variables are stored. This technique maintains API consistency across heterogeneous backend implementations while preserving data integrity.

## When to use

You are implementing a custom MsBackend subclass for the Spectra package and need to ensure that spectraData() returns all core spectra variables (e.g., centroided, polarity, collisionEnergy) regardless of which ones are explicitly stored in your backend. This is especially necessary when your backend stores only a small set of user-supplied spectra variables (e.g., msLevel, rtime) but must present a uniform interface compatible with downstream Spectra workflows that expect a complete set of core variables.

## When NOT to use

- Your backend already stores all or nearly all core spectra variables in memory or on disk—use direct retrieval instead of filling with NA.
- The missing core variables are expected to be populated on-demand by a lazy-loading accessor; NA-filling is appropriate only for static, query-time variable completion.
- You are not extending MsBackend or are implementing a read-only backend that is not expected to conform to the Spectra API contract.

## Inputs

- MsBackend subclass instance with slots for storing user-supplied spectra variables (e.g., msLevel, rtime as data.frame or vector)
- spectra variable DataFrame constructed from stored backend data (columns correspond to variables explicitly provided by the backend)

## Outputs

- DataFrame (S4Vectors) with all core spectra variables present as columns; missing core variables filled with NA; row count unchanged from input DataFrame

## How to apply

Within your MsBackend subclass, call fillCoreSpectraVariables() from within the spectraData() method after constructing the initial DataFrame of stored variables. fillCoreSpectraVariables() inspects the DataFrame, identifies which core spectra variables are missing, and appends columns for those variables populated entirely with NA values. This ensures that the returned DataFrame schema matches the expected core schema without requiring your backend to allocate storage for columns that are uniformly unavailable. The key rationale is that NA is the correct representation for data that the backend cannot provide, and this pattern allows backends to be selective about what they store while maintaining a consistent output contract.

## Related tools

- **Spectra** (R package that defines the MsBackend virtual class and fillCoreSpectraVariables() utility; provides infrastructure for backend implementations to return spectra data via spectraData() method) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame class for structured column-based data storage; spectraData() returns a DataFrame with core variables as columns)
- **MsBackendMemory** (Reference implementation of MsBackend that stores all data in memory; demonstrates spectraData() and spectraVariables() method patterns) — https://github.com/RforMassSpectrometry/Spectra

## Examples

```
# In a custom MsBackend subclass:
setMethod("spectraData", "MsBackendTest", function(object, columns = spectraVariables(object)) {
  df <- data.frame(msLevel = object@spectraVars$msLevel, rtime = object@spectraVars$rtime)
  df <- fillCoreSpectraVariables(df)
  return(as(df, "DataFrame"))
})
```

## Evaluation signals

- Returned DataFrame from spectraData() contains all expected core spectra variable names (e.g., 'centroided', 'polarity', 'collisionEnergy') as columns.
- Columns corresponding to missing core variables are entirely NA (no non-NA values present).
- DataFrame row count equals the number of spectra in the backend; no rows are dropped or duplicated during NA-filling.
- spectraVariables() method returns a union of user-supplied variable names and core variable names, consistent with the columns in the DataFrame returned by spectraData().
- Downstream Spectra operations (e.g., subsetting via extractByIndex, filtering) continue to work without error, confirming that the NA-filled DataFrame is schema-compatible with other backend implementations.

## Limitations

- NA-filling applies only to core spectra variables defined in the Spectra package; custom or domain-specific variables not in the core list will not be auto-populated and must be handled separately.
- NA values for missing variables may cause unexpected behavior in downstream analyses that assume those variables contain real data; users should be aware that, for example, a polarity column full of NA means the backend does not provide polarity information.
- fillCoreSpectraVariables() is a helper utility specific to the Spectra package; backends for other MS data frameworks may not have an equivalent, limiting portability of this technique.
- If a backend later acquires new data for a previously missing variable, re-running spectraData() will still return NA for those rows unless the backend logic is updated to populate that variable.

## Evidence

- [other] The spectraData() implementation for MsBackendTest uses fillCoreSpectraVariables() to ensure that all core spectra variables are returned, filling missing ones with NA values even when only user-supplied variables like msLevel and rtime are stored.: "uses fillCoreSpectraVariables() to ensure that all core spectra variables are returned, filling missing ones with NA values even when only user-supplied variables like msLevel and rtime are stored"
- [intro] The spectraData() method should return the full spectra data within a backend as a DataFrame object: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] Core spectra variables must be provided by each backend with dataStorage and dataOrigin as special required variables: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [other] Implement spectraData() method to return full spectra data as DataFrame; invoke fillCoreSpectraVariables() internally to populate missing core variables with NA values.: "Implement spectraData() method to return spectra variables as a DataFrame, invoking fillCoreSpectraVariables() internally to populate missing core variables with NA values"
- [intro] The spectraVariables() method should return a character vector with the names of all available spectra variables of the backend.: "The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables of the backend"
