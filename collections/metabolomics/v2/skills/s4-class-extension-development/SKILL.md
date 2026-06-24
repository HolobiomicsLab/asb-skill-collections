---
name: s4-class-extension-development
description: Use when you need to create a new backend for the Spectra package that
  provides MS data from a new source (file format, database, or computational resource)
  not covered by existing backends (MsBackendMzR, MsBackendMemory, MsBackendSql, etc.).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
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

# S4 Class Extension Development

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Developing custom S4 classes that extend virtual base classes (like MsBackend) to implement domain-specific data structures and accessor/replacement methods. This skill ensures that new backend implementations properly inherit the virtual API contract, validate data integrity, and integrate with existing analysis infrastructure.

## When to use

You need to create a new backend for the Spectra package that provides MS data from a new source (file format, database, or computational resource) not covered by existing backends (MsBackendMzR, MsBackendMemory, MsBackendSql, etc.). The trigger is: you have a data representation strategy (in-memory, on-disk, lazy-loaded from a database) and you need to expose m/z and intensity values through the standard Spectra API without modifying the analysis code.

## When NOT to use

- You are analyzing spectra using an existing, well-supported backend (MsBackendMemory, MsBackendMzR, MsBackendSql) without needing to support a new data source—use the existing backend instead.
- Your data is already in a Spectra object or compatible format; focus on analysis methods rather than backend development.
- You need only to filter, subset, or process spectra without implementing a new storage/retrieval strategy; use Spectra subsetting and processing functions instead.

## Inputs

- Virtual MsBackend class definition (from Spectra package)
- Data source (file format, database connection, in-memory structure) containing m/z and intensity values per spectrum
- Spectra variable metadata (names, IDs, precursor m/z, etc.) for each spectrum

## Outputs

- Concrete S4 class extending MsBackend with implemented accessor and (optionally) replacement methods
- Backend instance compatible with Spectra class for analysis workflows
- Validated DataFrame and peak data structures meeting Spectra API contracts

## How to apply

1. Define a new S4 class that formally extends the MsBackend virtual class, declaring slots for spectra variables (typically as a DataFrame) and peak data (as appropriate to your storage strategy—e.g., list of matrices for in-memory, file paths for on-disk, SQL queries for databases). 2. Implement all required virtual methods: `backendInitialize()` to load and prepare data, `spectraVariables()` to declare available variable names, `spectraData()` to return a DataFrame with m/z and intensity as NumericList objects, `peaksData()` to extract m/z–intensity matrices, `intensity()` and `mz()` as NumericList accessors, `extractByIndex()` to subset by integer indices, and `backendMerge()` to combine multiple backend instances. 3. For writable backends, implement replacement methods (`$<-`, `[<-`, `intensity<-`, `mz<-`, `peaksData<-`) that enforce four validation constraints: (a) length matching via `.match_length()` ensuring value count equals spectrum count, (b) data type validation (e.g., NumericList for m/z and intensity), (c) peak-count preservation so replacement values maintain peaks-per-spectrum cardinality, and (d) m/z ordering validation using `is.unsorted()` to verify increasing sort within each spectrum. 4. For read-only backends, implement only accessor methods and omit replacement methods or mark them as `VIRTUAL`. 5. Test the implementation on concrete data by creating a backend instance via `backendInitialize()`, verifying that `peaksData()` returns correctly dimensioned matrices, `extractByIndex()` preserves peak ordering and supports duplication, and `backendMerge()` concatenates all spectra without data loss.

## Related tools

- **Spectra** (Provides the virtual MsBackend class definition and analysis infrastructure that custom backends must integrate with; also defines the DataFrame and NumericList data structures used by backend accessors) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides the DataFrame and NumericList classes used to structure spectra variables and peak data in backend implementations)
- **MsBackendMemory** (Reference implementation (provided in Spectra package) storing data as list of matrices; exemplifies efficient peaksData() and replacement method implementations) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMzR** (Reference implementation for partially read-only backends that allow spectra variable modification but not peak data replacement) — https://github.com/RforMassSpectrometry/Spectra

## Examples

```
setClass('MyCustomBackend', contains = 'MsBackend', slots = c(data = 'DataFrame', peaks = 'list')); setMethod('peaksData', 'MyCustomBackend', function(object, ...) { lapply(object@peaks, function(x) as.matrix(x[, c('mz', 'intensity')])) }); setMethod('backendInitialize', 'MyCustomBackend', function(object, files, ...) { object@data <- read.csv(files); object@peaks <- lapply(seq_len(nrow(object@data)), function(i) data.frame(mz = ..., intensity = ...)); object })
```

## Evaluation signals

- peaksData() returns a list of numerical matrices with exactly 2 columns (m/z and intensity), one matrix per spectrum, with dimensionality matching spectrum count and declared peak counts
- extractByIndex() with integer indices correctly subsets the backend, preserves peak ordering within each spectrum, and supports duplicate indices without error
- backendMerge() combines two or more backend instances, concatenating all spectra and spectra variables without data loss or duplication, verified by comparing row counts before and after merge
- Replacement methods (mz<-, intensity<-, peaksData<-) reject inputs where m/z values are unsorted or contain NA, where peak counts differ from originals, or where length does not match spectrum count
- spectraData() returns a DataFrame with all spectra variables including m/z and intensity as NumericList columns, with row count matching declared spectrum count

## Limitations

- All backends must enforce m/z values sorted increasingly within each spectrum; NA values are not permitted in m/z. This constraint may require preprocessing for backends importing from unordered sources.
- Replacement methods for writable backends add significant validation overhead; read-only backends avoid this cost but sacrifice flexibility.
- Parallel processing requires backends to support backendParallelFactor() to suggest splitting strategies; backends that cannot parallelize efficiently may become bottlenecks in large-scale workflows.
- Peak-count preservation in replacement methods prevents dynamic expansion or contraction of peak counts per spectrum, limiting some data transformation scenarios.

## Evidence

- [intro] virtual_api_contract: "The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object."
- [intro] peaks_data_structure: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum"
- [intro] mz_ordering_constraint: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [intro] replacement_validation_constraints: "Replacement methods for writable backends enforce four key constraints: (1) length matching via `.match_length()` to ensure value length equals spectrum count, (2) data type validation checking that"
- [intro] backend_merge_operation: "The `backendMerge()` method merges (combines) `MsBackend` objects (of the same type!) into a single instance."
- [intro] read_only_backends_allowed: "`MsBackend` implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods."
- [intro] partially_read_only_example: "Backends can also be *partially* read-only, such as the `MsBackendMzR`. This backend allows for example to change spectra variables, but not the peaks data"
- [intro] spectra_variables_definition: "Properties of a spectrum are called *spectra variables*. While backends can define their own properties, a minimum required set of spectra variables **must** be provided by each backend"
- [methods] memory_backend_efficient_storage: "The `MsBackendMemory` backend stores data as a list of matrices instead, yielding more efficient peaksData() implementation with lower overhead for adding/replacing/checking MS data"
