---
name: spectra-variable-and-peak-data-storage
description: Use when when building a new mass spectrometry data backend for the Spectra
  package that must store and serve multiple spectra with their associated m/z and
  intensity peaks. Use this when you need a backend that combines efficient metadata
  lookup (via data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Spectra
  - S4Vectors
  - IRanges
  - MSnbase
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- library(Spectra) library(IRanges)
- The *Spectra* package defines an efficient infrastructure for storing and handling
  mass spectrometry spectra
- '`DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)'
- DataFrame` object (defined in the `r Biocpkg("S4Vectors")` package)
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

# spectra-variable-and-peak-data-storage

## Summary

Design and implement an S4 class extending MsBackend to store mass spectrometry spectral data, separating spectrum metadata (spectra variables) in a data.frame from peak data (m/z and intensity) in NumericList objects, with validity constraints ensuring consistency. This skill enables creation of custom backend implementations for the Spectra infrastructure.

## When to use

When building a new mass spectrometry data backend for the Spectra package that must store and serve multiple spectra with their associated m/z and intensity peaks. Use this when you need a backend that combines efficient metadata lookup (via data.frame spectra variables) with flexible peak data storage (via NumericList), and must enforce invariants that m/z values are sorted increasingly within each spectrum with no missing values.

## When NOT to use

- Input is already a valid Spectra object or MsBackend instance ready for use; implement accessor/transformation methods instead.
- Peak data is not mass spectrometry spectra (e.g., chromatographic, imaging, or non-m/z-sorted data); this design assumes sorted m/z within each spectrum.
- You require mutable peak data storage but only read-only access is needed; consider MsBackendCached or similar read-only backends instead.

## Inputs

- Mass spectrometry spectral data (peaks with m/z and intensity values)
- Spectrum metadata (spectra variables: retention time, precursor m/z, scan number, etc.)
- Data in any format that can be converted to data.frame and NumericList structures

## Outputs

- S4 MsBackend subclass instance with valid spectraVars, mz, and intensity slots
- Spectra object backed by the custom MsBackend implementation
- DataFrame (via spectraData() method) combining spectra variables with NumericList peak data

## How to apply

Define an S4 class extending the virtual MsBackend using setClass() with three primary slots: a data.frame (spectraVars) storing spectrum-level properties like retention time and precursor m/z, and NumericList objects (mz, intensity) storing the corresponding peak data for each spectrum. Implement a constructor (initialize method) that accepts input data and populates all three slots consistently. Define a setValidity() method that enforces the core constraint: the number of rows in spectraVars must equal the length of both mz and intensity slots, that all m/z values within each spectrum are sorted increasingly with no NA elements, and that m/z and intensity have matching lengths per spectrum. Instantiate the class and verify that validity checks correctly reject objects with mismatched slot lengths or unsorted/missing m/z values. This separation of concerns allows backends to implement different access strategies (e.g., on-disk vs. in-memory) while maintaining a consistent interface.

## Related tools

- **Spectra** (Provides the virtual MsBackend class to extend and the Spectra wrapper class that uses backend instances to store and process spectral data) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame and NumericList data structures used for storing spectra variables and peak data with efficient memory representation)
- **IRanges** (Used with S4Vectors for efficient range and list operations on spectral data)
- **MSnbase** (Predecessor package providing in-memory and on-disk data representation design patterns that informed MsBackend architecture)

## Examples

```
setClass('MsBackendTest', contains='MsBackend', slots=list(spectraVars='data.frame', mz='NumericList', intensity='NumericList')); setValidity('MsBackendTest', function(object) { if(nrow(object@spectraVars) != length(object@mz)) return('Mismatch: nrow(spectraVars) != length(mz)'); TRUE }); obj <- new('MsBackendTest', spectraVars=data.frame(id=1:2), mz=NumericList(c(100, 200), c(150, 250)), intensity=NumericList(c(10, 20), c(15, 25)))
```

## Evaluation signals

- Class instantiation succeeds without error; object contains populated spectraVars (data.frame), mz (NumericList), and intensity (NumericList) slots.
- Validity check passes for well-formed objects: nrow(spectraVars) == length(mz) == length(intensity); each mz element is sorted increasingly with no NA values.
- Validity check correctly rejects mismatched objects: nrow(spectraVars) ≠ length(mz), or mz values contain NA, or mz values are not sorted increasingly within a spectrum.
- spectraData() method returns a DataFrame with spectra variable columns plus mz and intensity as NumericList columns with matching row/element counts.
- Backend can be passed to Spectra() constructor and used in analysis workflows (e.g., subsetting, filtering) without errors.

## Limitations

- m/z values must be sorted increasingly within each spectrum and cannot contain missing (NA) values; data preprocessing to enforce this constraint is required before slot assignment.
- The data.frame spectraVars slot stores only tabular metadata; S4 objects as spectra variables require MsBackendDataFrame instead.
- Performance depends on NumericList implementation and the chosen data access strategy (in-memory vs. on-disk); lazy loading of peaks requires additional backend methods.
- Parallel processing may be limited if the backend does not implement backendParallelFactor() to suggest a preferred splitting strategy.

## Evidence

- [intro] Class design structure: "An MsBackend extension class (MsBackendTest) uses three slots: a data.frame (spectraVars) storing spectra variable properties, and NumericList objects (mz, intensity) storing peak data."
- [intro] Validity constraint rationale: "A setValidity method enforces that the number of rows in spectraVars matches the length of both mz and intensity slots, ensuring data consistency across the backend."
- [intro] m/z ordering requirement: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (NA) for m/z values are not supported."
- [intro] Backend virtual class role: "The MsBackend virtual class defines the API that new backend classes need to implement in order to be used with the Spectra object."
- [intro] Spectra variables definition: "Properties of a spectrum are called spectra variables. While backends can define their own properties, a minimum required set of spectra variables must be provided by each backend."
