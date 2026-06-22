---
name: peak-data-integrity-checks
description: Use when implementing or modifying a writable MsBackend subclass (e.g., MsBackendMemory, MsBackendDataFrame) and need to replace peak data (m/z values, intensity values, or peaksData).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - S4Vectors
  - Spectra
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-data-integrity-checks

## Summary

Validate m/z and intensity peak data in mass spectrometry backends to enforce data integrity constraints before replacement or storage. This skill ensures that writable MsBackend implementations maintain sortedness, length consistency, and type safety across spectral datasets.

## When to use

Apply this skill when implementing or modifying a writable MsBackend subclass (e.g., MsBackendMemory, MsBackendDataFrame) and need to replace peak data (m/z values, intensity values, or peaksData). Specifically trigger on: (1) invocation of replacement methods (`$<-`, `[<-`, or `replaceChromsData()`), (2) before updating internal DataFrame or matrix storage, (3) when accepting external m/z or intensity vectors that must be assigned to spectra.

## When NOT to use

- Backend is read-only (e.g., MsBackendMzR retrieving data from immutable raw files, or MsBackendCached extending read-only resources) — use data accessor methods instead.
- Input peak data is already stored in an external mzML/mzXML/CDF file managed by mzR or similar on-disk backend — validation must occur at import time, not on replacement.
- Modifying only spectra variables (non-peak metadata like retention time or precursor m/z) — use simpler type checks without m/z ordering constraints.

## Inputs

- NumericList of m/z values
- NumericList of intensity values
- list of numerical matrices (peaksData)
- character vector (spectra variable names)
- numeric vector (scalar spectra variables)
- MsBackend subclass instance (target backend)

## Outputs

- validated NumericList (m/z or intensity)
- validated peaksData (list of matrices)
- boolean or error status (validation success/failure)
- updated MsBackend internal data structure

## How to apply

Implement four sequential validation steps in each replacement method: (1) **Length matching**: use `.match_length()` to verify that replacement vector length equals spectrum count in the backend; (2) **Data type validation**: confirm m/z and intensity values are NumericList objects and check scalar spectra variables match expected types; (3) **M/z ordering**: apply `is.unsorted()` on each spectrum's m/z values to enforce increasing order, reject if unsorted; (4) **Peak-count preservation and NA exclusion**: verify replacement NumericLists maintain identical peak counts per spectrum as originals, and confirm m/z values contain no NA entries. Apply these checks before assigning validated values to the internal data structure (DataFrame or list of matrices). Test all replacement methods on a concrete backend instance to confirm writable functionality.

## Related tools

- **Spectra** (R package that defines the MsBackend virtual class and implements core replacement method signatures ($<-, [<-); also provides NumericList and DataFrame data structures for validation) — https://github.com/RforMassSpectrometry/Spectra
- **S4Vectors** (provides DataFrame and NumericList container classes used internally by MsBackend to store and validate peak and spectra variable data)
- **R** (language and runtime for implementing S4 methods, validation logic (is.unsorted, match_length), and data structure updates)

## Evaluation signals

- Replacement vector length equals spectrum count: `.match_length()` returns TRUE and no length mismatch error is raised.
- M/z values are strictly increasing within each spectrum: `is.unsorted()` returns FALSE for all spectra, confirming sorted order.
- Data types conform to schema: m/z and intensity are NumericList objects; scalar variables match expected types (numeric, character); no type coercion warnings.
- Peak counts unchanged after replacement: length of m/z equals length of intensity for each spectrum; number of peaks per spectrum before and after replacement are identical.
- No NA values in m/z data: `anyNA(mz_values)` returns FALSE; validation rejects replacement if NAs are present.

## Limitations

- M/z ordering validation assumes a single sort order (increasing) and does not support spectra with duplicate m/z values (which may arise in high-resolution instruments with closely spaced isotopologues but are typically forbidden by the Spectra design).
- Peak-count preservation constraint prevents data restructuring workflows where spectra are merged or filtered at the peak level; use backend-level filtering (extractByIndex) instead.
- Validation is performed in-memory and may become slow for very large backends with millions of spectra or peaks; no streaming or chunked validation is described in the article.
- The skill applies only to writable backends; read-only backends (MsBackendMzR, MsBackendMassbankSql) do not support replacement methods and thus do not require these checks.

## Evidence

- [other] Replacement methods for writable backends enforce four key constraints: (1) length matching via `.match_length()` to ensure value length equals spectrum count, (2) data type validation checking that m/z and intensity are NumericList objects, (3) peak-count preservation requiring that replacement values maintain the same number of peaks per spectrum, and (4) m/z ordering validation using `is.unsorted()` to verify m/z values are increasingly sorted within each spectrum.: "Replacement methods for writable backends enforce four key constraints: (1) length matching via `.match_length()` to ensure value length equals spectrum count, (2) data type validation checking that"
- [intro] m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported.: "m/z values within each spectrum are expected to be sorted increasingly. Missing values (`NA`) for m/z values are not supported."
- [intro] MsBackend implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods.: "MsBackend implementations can also represent purely *read-only* data resources. In this case only data accessor methods need to be implemented but not data replacement methods."
- [other] Implement input validation in each replacement method to check that replacement vectors match the length of the backend (number of spectra) or individual spectrum peak counts.: "Implement input validation in each replacement method to check that replacement vectors match the length of the backend (number of spectra) or individual spectrum peak counts."
- [other] For peak data replacement, verify that m/z values remain sorted in increasing order within each spectrum and that intensity vector length equals m/z vector length.: "For peak data replacement, verify that m/z values remain sorted in increasing order within each spectrum and that intensity vector length equals m/z vector length."
