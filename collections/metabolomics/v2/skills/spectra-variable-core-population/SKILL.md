---
name: spectra-variable-core-population
description: Use when when implementing a custom MsBackend and the spectraData() method needs to return all core spectra variables (e.g., centroided, polarity, collisionEnergy) regardless of which variables were explicitly stored during backend initialization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Spectra
  - S4Vectors
  - R
  - MsBackendMemory
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- The *Spectra* package defines an efficient infrastructure for storing and handling mass spectrometry spectra
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

# spectra-variable-core-population

## Summary

Populate missing core spectra variables with NA values in a backend's spectraData() output to ensure complete metadata structure. This ensures all required MS spectra variables are present in DataFrame results even when user-supplied data contains only a subset.

## When to use

When implementing a custom MsBackend and the spectraData() method needs to return all core spectra variables (e.g., centroided, polarity, collisionEnergy) regardless of which variables were explicitly stored during backend initialization. This is essential when a backend stores only user-supplied variables like msLevel and rtime but must advertise and return the full set of core variables required by the Spectra API.

## When NOT to use

- Your backend stores and manages all core spectra variables explicitly; fillCoreSpectraVariables() is unnecessary overhead in that case.
- You are implementing a read-only backend that intentionally exposes only a non-standard subset of variables and do not want to claim API compliance with MsBackend.
- You are working with an existing backend (e.g., MsBackendMzR, MsBackendMemory) that already implements this pattern; focus on your application logic instead.

## Inputs

- DataFrame containing user-supplied spectra variables (e.g., msLevel, rtime)
- MsBackend instance with populated user-supplied data slots

## Outputs

- DataFrame with all core spectra variables present, missing ones filled with NA
- Spectra object backed by the completed backend

## How to apply

Within the spectraData() method of your MsBackend subclass, invoke fillCoreSpectraVariables() on the DataFrame containing user-supplied spectra variables before returning. This helper function examines which core variables are missing from the current DataFrame and appends them as columns filled with NA values. The rationale is that the MsBackend API contract requires all backends to report the same set of core variables through spectraVariables(), so spectraData() must honor that contract by including those variables in its output, even if the backend does not actively manage all of them. Ensure spectraVariables() returns the union of both user-supplied and core variable names so that consumers know all variables will be present in the DataFrame.

## Related tools

- **Spectra** (R package providing the MsBackend virtual class, fillCoreSpectraVariables() helper, and DataFrame schema for core spectra variables) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame class used to store and return spectra variables with consistent schema)
- **MsBackendMemory** (Reference implementation of MsBackend showing how spectraData() and fillCoreSpectraVariables() are used together) — https://github.com/RforMassSpectrometry/Spectra

## Examples

```
# In MsBackendTest@spectraData() implementation:
setMethod("spectraData", "MsBackendTest", function(object, columns = NULL) {
  res <- DataFrame(msLevel = object@msLevel, rtime = object@rtime)
  res <- Spectra:::.fillCoreSpectraVariables(res)
  res
})
```

## Evaluation signals

- spectraData() return value contains all core variable names listed in spectraVariables() output
- Missing core variables appear in the returned DataFrame as columns with all NA values
- User-supplied variables retain their original data; no values are lost or overwritten
- Calling spectraData() on two backends with different sets of user-supplied variables produces DataFrames with identical column sets (all core variables present) but different row values
- The returned DataFrame passes as.data.frame() and retains proper column classes for NA-filled columns (logical for boolean cores, numeric for numeric cores, etc.)

## Limitations

- fillCoreSpectraVariables() only handles the predefined set of core variables recognized by the Spectra package; custom or domain-specific variables must be managed separately by the backend.
- NA-filling occurs at the DataFrame level; if your backend needs to support lazy-loading of missing variables on-demand, you must override this behavior.
- The function does not validate or impute sensible defaults; all missing cores become NA, which may not be appropriate for backends wrapping external data sources that have implicit defaults (e.g., polarity = 1 by convention).

## Evidence

- [other] The spectraData() implementation for MsBackendTest uses fillCoreSpectraVariables() to ensure that all core spectra variables are returned, filling missing ones with NA values even when only user-supplied variables like msLevel and rtime are stored.: "The spectraData() implementation for MsBackendTest uses fillCoreSpectraVariables() to ensure that all core spectra variables are returned, filling missing ones with NA values"
- [intro] The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
- [intro] The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables of the backend.: "The `spectraVariables()` method should return a `character` vector with the names of all available spectra variables"
- [intro] Core spectra variables must be provided by each backend with dataStorage and dataOrigin as special required variables: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [intro] The `Spectra` package separates the code for the analysis of MS data from the code needed to import, represent and provide the data.: "The `Spectra` package separates the code for the analysis of MS data from the code needed to import, represent and provide the data"
