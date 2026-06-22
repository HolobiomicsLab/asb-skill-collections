---
name: dataframe-and-numericlist-manipulation
description: Use when you are implementing a new MsBackend subclass and need to store spectra metadata (sample names, retention times, precursor m/z, etc.) separately from peak data (m/z and intensity pairs) while maintaining row-wise alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3365
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - S4Vectors
  - R
  - Spectra
  - IRanges
  techniques:
  - LC-MS
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

# dataframe-and-numericlist-manipulation

## Summary

Construct and manipulate parallel data structures (data.frame for spectra metadata, NumericList for peak m/z and intensity values) to implement custom MsBackend classes that integrate with the Spectra package infrastructure. This skill enables creation of new mass spectrometry data backends by coordinating tabular and list-based storage to meet the MsBackend API contract.

## When to use

You are implementing a new MsBackend subclass and need to store spectra metadata (sample names, retention times, precursor m/z, etc.) separately from peak data (m/z and intensity pairs) while maintaining row-wise alignment. Use this when your backend representation requires independent access to spectra variables as a DataFrame and peak data as corresponding NumericList elements, typically for in-memory or hybrid backends.

## When NOT to use

- Your backend data is stored in external files (mzML, mzXML, CDF) — use MsBackendMzR instead with on-the-fly retrieval
- Your backend is purely read-only and does not need data replacement methods — use MsBackendCached or similar minimal implementation
- Your data is already stored in a SQL database — use MsBackendSql or MsBackendOfflineSql instead

## Inputs

- S4 class definition extending MsBackend
- spectraVars: data.frame with one row per spectrum and columns for metadata variables
- mz: NumericList with one element per spectrum containing m/z values (sorted)
- intensity: NumericList with one element per spectrum containing intensity values

## Outputs

- MsBackend subclass instance with properly synchronized spectraVars, mz, and intensity slots
- DataFrame object from spectraData() method combining metadata and peaks information
- List of 2-column matrices from peaksData() method (m/z, intensity pairs per spectrum)
- NumericList objects from intensity() and mz() accessor methods

## How to apply

Define three slots in your MsBackend S4 class: spectraVars (data.frame for metadata), mz (NumericList for m/z arrays), and intensity (NumericList for intensity arrays), ensuring each row in spectraVars corresponds to one spectrum and the i-th element of mz and intensity NumericLists contains the peaks for spectrum i. Implement spectraData() to return a combined S4Vectors DataFrame that merges spectraVars with computed columns for peaksData; implement peaksData() to extract and align m/z and intensity pairs as a list of 2-column matrices; implement accessor methods (intensity(), mz()) to return the NumericList objects directly; and implement replacement methods (intensity<-, mz<-, spectraData<-) that maintain alignment by updating both the list slot and the corresponding row in spectraVars. Enforce the constraint that m/z values within each spectrum are sorted increasingly and that dataStorage and dataOrigin are always present in spectraVars.

## Related tools

- **Spectra** (Framework that consumes MsBackend implementations via the @backend slot; defines the virtual MsBackend class and API contract) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (Provides DataFrame class for returning spectraData() results and NumericList class for storing peak data aligned across spectra)
- **IRanges** (Underlying package providing NumericList container for efficient storage of variable-length numeric vectors per spectrum)

## Examples

```
setClass('MsBackendTest', contains='MsBackend', slots=c(spectraVars='data.frame', mz='NumericList', intensity='NumericList')); setMethod('spectraData', 'MsBackendTest', function(object) { DataFrame(object@spectraVars, mz=object@mz, intensity=object@intensity) })
```

## Evaluation signals

- spectraData() returns a DataFrame with number of rows equal to number of spectra and includes both metadata columns (from spectraVars) and peak metadata
- peaksData() output has length equal to number of spectra; each element is a 2-column matrix with m/z values sorted increasingly in the first column
- intensity() and mz() return NumericList objects with length equal to number of spectra and element-wise correspondence (i-th element contains peaks for spectrum i)
- Replacement methods (intensity<-, mz<-, spectraData<-) maintain row-column alignment after updates: number of rows in spectraVars, lengths of mz and intensity lists, and number of rows returned by spectraData() remain synchronized
- spectraVariables() returns a character vector that includes all column names from spectraVars plus 'mz' and 'intensity' to reflect available variables

## Limitations

- The parallel storage model requires manual synchronization during subsetting (extractByIndex) and merging (backendMerge) — operations on one slot must be reflected in all three to avoid orphaned data
- NumericList elements must strictly correspond by position to rows in spectraVars; no separate indexing or key-based lookup is enforced, so in-place slot modifications can silently break alignment
- All spectra variables stored in spectraVars must have length equal to the number of spectra; S4 objects as variable values are not supported in data.frame (use MsBackendDataFrame instead for full S4 object support)
- The in-memory design does not scale to very large datasets; backends needing to handle hundreds of millions of spectra should use on-disk (MsBackendMzR, MsBackendHdf5Peaks) or database backends (MsBackendSql)

## Evidence

- [other] Define an S4 class MsBackendTest extending MsBackend with slots for spectraVars (data.frame), mz (NumericList), and intensity (NumericList): "Define an S4 class MsBackendTest extending MsBackend with slots for spectraVars (data.frame), mz (NumericList), and intensity (NumericList)."
- [other] Each row in spectraVars represents one spectrum and corresponding elements in mz/intensity lists contain peak data: "where each row in spectraVars represents one spectrum and corresponding elements in mz/intensity lists contain peak data."
- [intro] The spectraData() method should return the full spectra data within a backend as a DataFrame object: "The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`"
- [intro] m/z values within each spectrum are expected to be sorted increasingly: "m/z values within each spectrum are expected to be sorted increasingly."
- [intro] dataStorage and dataOrigin are special spectra variables that define for each spectrum where the data is stored and from where the data derived: "`dataStorage` and `dataOrigin` are two special spectra variables that define for each spectrum where the data is stored and from where the data derived"
- [intro] The peaksData() method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum: "The `peaksData()` method extracts the MS peaks data from a backend, which includes the m/z and intensity values of each MS peak of a spectrum."
- [intro] Extract the intensity values for each spectrum in the backend. The result is expected to be a NumericList: "Extract the intensity values for each spectrum in the backend. The result is expected to be a `NumericList`"
- [intro] The MsBackendMemory backend for example stores the MS data already as a list of matrices: "The `MsBackendMemory` backend for example stores the MS data already as a `list` of matrices"
