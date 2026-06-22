---
name: numeric-list-construction-validation
description: Use when implementing a backendInitialize() method for a custom MsBackend class and you have raw m/z and intensity vectors (from files, data frames, or lists) that must be converted into the internal NumericList representation required by the Spectra package.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - S4Vectors
  - R
  - Spectra
  - IRanges
  techniques:
  - mass-spectrometry
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

# numeric-list-construction-validation

## Summary

Construct NumericList objects from m/z and intensity vector pairs extracted from mass spectrometry data, and validate that m/z values are sorted increasingly with no missing values to ensure compliance with Spectra backend requirements. This skill is essential during backend initialization to prepare peak data for efficient storage and retrieval within the MsBackend infrastructure.

## When to use

Apply this skill when implementing a backendInitialize() method for a custom MsBackend class and you have raw m/z and intensity vectors (from files, data frames, or lists) that must be converted into the internal NumericList representation required by the Spectra package. Trigger conditions include: (1) you are loading peak data from external sources (mzML, mzXML, CDF, or custom formats) into a new backend; (2) m/z and intensity values are initially stored as separate lists or matrix columns; (3) you need to enforce the core constraint that m/z values are sorted increasingly within each spectrum with no NA values.

## When NOT to use

- Input peak data is already stored as a NumericList and has already been validated in a prior initialization step.
- You are implementing a read-only backend (e.g., MsBackendMzR or MsBackendSql) that retrieves m/z and intensity on-the-fly and does not store copies in memory; skip internal NumericList construction and implement peaksData() or mz()/intensity() accessors instead.
- m/z values are unsorted or contain NA values and your use case cannot tolerate reordering or filtering; instead, implement custom error handling or preprocessing before applying this skill.

## Inputs

- data.frame or DataFrame containing spectra variables and optionally list columns with m/z and intensity values
- list of m/z vectors (one per spectrum)
- list of intensity vectors (one per spectrum, corresponding to m/z vectors)
- optional complete DataFrame with all peak and spectra variable data

## Outputs

- NumericList object containing m/z values for each spectrum (sorted increasingly, no NA)
- NumericList object containing intensity values for each spectrum
- validated backend instance with peaksData or mz/intensity slots populated
- boolean or diagnostic report confirming validation success

## How to apply

Extract m/z and intensity vectors for each spectrum from the input data structure (e.g., from a data.frame with list columns, separate list objects, or a DataFrame). Convert each pair of m/z and intensity vectors into a NumericList object using the S4Vectors package. Before conversion, validate that each m/z vector is sorted in increasing order and contains no missing (NA) values; reject spectra that violate these constraints or reorder/filter as appropriate. Store the resulting NumericList objects in the backend's internal slots (typically peaksData or separate mz/intensity slots). Finally, call a helper validation function to confirm that the resulting NumericList objects conform to the data type expectations defined by the MsBackend class definition.

## Related tools

- **Spectra** (defines the MsBackend virtual class API and Spectra class for storing and accessing mass spectrometry spectra; provides the backendInitialize() framework and spectra variable system) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (provides the NumericList class and DataFrame class for storing and manipulating peak data and spectra variables)
- **IRanges** (optional dependency used alongside S4Vectors for interval and range operations on spectral data)

## Examples

```
be_mem <- backendInitialize(MsBackendMemory(), data = spectra_df, mz = mz_list, intensity = intensity_list); stopifnot(all(!is.na(unlist(mz(be_mem)))), all(vapply(mz(be_mem), function(x) all(diff(x) > 0), logical(1))))
```

## Evaluation signals

- NumericList object structure is valid: verify using is(result, 'NumericList') and class(result[[1]]) == 'numeric'
- m/z values are sorted increasingly within each spectrum: confirm via all(diff(x) > 0) for each element x in the NumericList
- No NA values present in m/z vectors: verify using !anyNA(result) or lapply(result, anyNA) returns all FALSE
- Length consistency: length(mz_list) == length(intensity_list) and each list is length-1 equal to number of spectra in backend
- Core spectra variables pass type validation: call helper validation function and confirm return status is TRUE or warning-free; dataStorage and dataOrigin are set as character vectors

## Limitations

- NumericList construction assumes input m/z and intensity vectors are already numeric; non-numeric input will raise type conversion errors.
- The skill enforces the strict requirement that m/z values must be sorted increasingly with no NA values; spectra failing this constraint cannot be added without preprocessing (sorting or filtering).
- Memory footprint grows linearly with the number of spectra and peaks per spectrum; very large datasets may require on-the-fly backends (e.g., MsBackendMzR) instead of in-memory NumericList storage.
- NumericList validation does not check intensity vector properties (sign, magnitude, or monotonicity); intensity vectors can be in any order and may contain NA or zero values unless the backend implementation adds additional constraints.

## Evidence

- [intro] m/z values within each spectrum must be sorted increasingly; missing values for m/z are not supported.: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [other] Extract and store m/z values as NumericList, verifying they are sorted increasingly with no missing values.: "Extract and store m/z values as NumericList, verifying they are sorted increasingly with no missing values."
- [intro] Implement peaksData() to extract m/z and intensity values as list of numerical matrices; intensity() to return NumericList of intensity values; mz() to return NumericList of m/z values ordered increasingly.: "Extract the m/z values for each spectrum in the backend. The result is expected to be a `NumericList`. Also, the m/z values are expected to be ordered increasingly for each element"
- [other] backendInitialize() accepts data.frame with spectra variables and two lists with m/z and intensity values, converts lists to NumericList objects, validates core spectra variable data types.: "backendInitialize() accepts a data.frame with spectra variables and two lists with m/z and intensity values, automatically sets dataStorage and dataOrigin if missing, converts lists to NumericList"
- [intro] The `spectraData()` method should return the full spectra data within a backend as a `DataFrame` object with m/z and intensity as NumericList columns.: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object"
