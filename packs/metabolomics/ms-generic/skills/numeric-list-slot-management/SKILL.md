---
name: numeric-list-slot-management
description: Use when when extending the MsBackend virtual class to create a custom backend for mass spectrometry data, and you need to store peak m/z and intensity values as variable-length numeric vectors indexed by spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - S4Vectors
  - Spectra
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.3390/metabo12020173
  title: spectra
evidence_spans:
- library(Spectra) library(IRanges)
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

# numeric-list-slot-management

## Summary

Design and implement S4 class slots using NumericList containers to store peak data (m/z and intensity values) in MsBackend subclasses, ensuring consistency between spectra metadata and peak vectors through validity constraints. This skill is essential for building custom mass spectrometry backends that efficiently represent multiple spectra with varying numbers of peaks.

## When to use

When extending the MsBackend virtual class to create a custom backend for mass spectrometry data, and you need to store peak m/z and intensity values as variable-length numeric vectors indexed by spectrum. Specifically: (1) you have multiple spectra, each with a different number of m/z–intensity pairs; (2) you want to keep peak data in memory or cache it; (3) you need m/z values within each spectrum sorted increasingly with no NA values; (4) you require validation that the number of spectra in your metadata (data.frame) matches the length of your peak containers.

## When NOT to use

- Input peak data is already stored in external files (mzML, mzXML, CDF) — use MsBackendMzR or on-disk backends instead to minimize memory footprint.
- You need to support read-only access to SQL or HDF5 databases — use MsBackendSql, MsBackendOfflineSql, or MsBackendHdf5Peaks, which handle lazy loading.
- Peak data is heterogeneous across spectra in a way that NumericList cannot represent uniformly (e.g., custom metadata per peak) — consider a more flexible container or different slot design.

## Inputs

- data.frame with spectra metadata (one row per spectrum; must include core spectra variables)
- list or NumericList of m/z numeric vectors (one per spectrum)
- list or NumericList of intensity numeric vectors (one per spectrum)

## Outputs

- S4 MsBackend subclass instance with validated spectraVars, mz, and intensity slots
- Validity check results confirming slot length consistency and m/z sorting

## How to apply

Define an S4 class extending MsBackend with at least three slots: a data.frame (e.g., spectraVars) holding one row per spectrum and columns for core spectra variables, and two NumericList slots (mz and intensity) where each element corresponds to one spectrum's peaks. In the class definition, use setClass() with Prototype and Representation to initialize these slots. Write a setValidity() method that enforces three constraints: (1) nrow(spectraVars) == length(mz) == length(intensity); (2) each mz element is sorted increasingly (via is.sorted() or equivalent); (3) no NA values appear in any mz element. Implement an initialize or new method that accepts raw peak data and populates slots, calling new() at the end to trigger validity checking. Test instantiation with valid and intentionally invalid objects to confirm that the validity method correctly rejects mismatched or unsorted data. Document the constraints in slot documentation so downstream users understand the invariants being enforced.

## Related tools

- **Spectra** (Provides the MsBackend virtual class API that the custom backend must extend; defines the Spectra class that uses the backend to access peak and spectra variable data.) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Supplies the NumericList class used to store peak data (m/z and intensity) as a list-like container optimized for variable-length numeric vectors.)
- **R** (Language and environment for defining S4 classes using setClass(), implementing validity via setValidity(), and testing class instantiation.)

## Examples

```
setClass("MsBackendTest", contains="MsBackend", slots=c(spectraVars="data.frame", mz="NumericList", intensity="NumericList")); setValidity("MsBackendTest", function(object) { if(nrow(object@spectraVars) != length(object@mz) || nrow(object@spectraVars) != length(object@intensity)) return("Slot lengths must match") }); new("MsBackendTest", spectraVars=data.frame(msLevel=c(2L, 2L)), mz=NumericList(c(100, 200), c(150, 250)), intensity=NumericList(c(10, 20), c(15, 25)))
```

## Evaluation signals

- Instantiation of a valid object succeeds and passes setValidity() checks without warnings or errors.
- Instantiation with mismatched slot lengths (e.g., nrow(spectraVars) ≠ length(mz)) fails with a validation error message.
- Instantiation with unsorted or NA-containing m/z values fails with a validation error message.
- Subsetting or extracting a spectrum via extractByIndex() or peaksData() returns peak data where mz and intensity NumericList elements remain aligned and sorted.
- The spectraData() method returns a DataFrame where the mz and intensity columns are NumericList objects with no length mismatches relative to spectraVars rows.

## Limitations

- NumericList assumes all peaks within a spectrum are numeric; non-numeric metadata per peak (e.g., annotations, quality scores) requires additional slots or a different design.
- Validity checking is performed only at instantiation and assignment; if slots are modified directly in memory (e.g., via @), consistency is not automatically re-checked.
- Large in-memory NumericList objects can consume significant RAM; for very large datasets, consider lazy-loading backends (MsBackendMzR, MsBackendSql) instead.
- The current design assumes m/z values are pre-sorted; if input data has unsorted m/z, you must sort before population or add a sorting step in the initialize method.

## Evidence

- [intro] Class structure and slot design: "An MsBackend extension class uses three slots: a data.frame storing spectra variable properties, and NumericList objects storing peak data"
- [intro] Validity constraint enforcement: "A setValidity method enforces that the number of rows in spectraVars matches the length of both mz and intensity slots"
- [intro] M/z sorting requirement: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (NA) for m/z values are not supported."
- [intro] MsBackend virtual class definition: "The MsBackend virtual class defines the API that new backend classes need to implement to be used with Spectra objects"
- [intro] spectraData method output type: "The spectraData() method should return the full spectra data within a backend as a DataFrame object"
