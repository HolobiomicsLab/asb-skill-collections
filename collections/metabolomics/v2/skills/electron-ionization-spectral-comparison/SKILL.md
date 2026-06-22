---
name: electron-ionization-spectral-comparison
description: Use when you have a query electron ionization (EI) mass spectrum in msp format and wish to identify it by matching against a reference spectral library. Apply this skill when you need ranked similarity scores between the query and each library entry to prioritize candidate identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - mssearchr
  - R
  - NIST API
derived_from:
- doi: 10.1021/jasms.5c00322
  title: mspepsearchr
evidence_spans:
- The primary goal of the `mssearchr` package is to enhance the capabilities of R users for conducting library searches against electron ionization mass spectral databases.
- The primary goal of the `mssearchr` package is to enhance the capabilities of R users
- enhance the capabilities of R users for conducting library searches
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspepsearchr_cq
    doi: 10.1021/jasms.5c00322
    title: mspepsearchr
  dedup_kept_from: coll_mspepsearchr_cq
schema_version: 0.2.0
---

# electron-ionization-spectral-comparison

## Summary

Compare an unknown electron ionization mass spectrum against a library of reference spectra using the Similarity (EI Simple) algorithm to rank and identify likely matches. This skill enables rapid spectral annotation in R without requiring external NIST infrastructure.

## When to use

You have a query electron ionization (EI) mass spectrum in msp format and wish to identify it by matching against a reference spectral library. Apply this skill when you need ranked similarity scores between the query and each library entry to prioritize candidate identifications.

## When NOT to use

- Input spectra are not in electron ionization mode (e.g., ESI, APCI, or other soft ionization methods)
- Reference library is not in msp format or is corrupt/incompletely parsed
- Query spectrum has insufficient peak data or signal-to-noise ratio for reliable matching

## Inputs

- Query electron ionization mass spectrum (msp format)
- Reference spectral library (msp file format)

## Outputs

- Ranked list of library matches with similarity scores
- Table of matched library entries sorted by descending similarity

## How to apply

Load the query EI mass spectrum and reference msp library file using mssearchr's msp reading functionality. Parse both spectra to extract m/z and intensity pairs. Implement the Similarity (EI Simple) algorithm to compute pairwise similarity scores between the query spectrum and each library entry, accounting for matched peaks and their intensity ratios. Return a ranked list or table of library matches with their corresponding similarity scores, ordered from highest to lowest score to prioritize the most likely identifications.

## Related tools

- **mssearchr** (Provides custom implementation of Similarity (EI Simple) algorithm and msp file I/O for spectral library searching) — https://github.com/AndreySamokhin/mssearchr
- **R** (Execution environment for mssearchr package and spectral data manipulation)
- **NIST API** (Alternative library search interface; mssearchr can call nistms$.exe for comparison)

## Examples

```
library(mssearchr); query <- read_msp('unknown_spectrum.msp'); library <- read_msp('reference_library.msp'); results <- similarity_ei_simple(query, library); head(results[order(results$score, decreasing=TRUE), ])
```

## Evaluation signals

- Returned similarity scores fall within the expected range [0, 1] or [0, 100] depending on algorithm normalization
- Top-ranked match has documented experimental validation (e.g., known compound in library or independent confirmation)
- Similarity score for true positive match exceeds a domain-appropriate threshold (e.g., >0.7 or >70%)
- m/z and intensity pairs from query and library spectra are correctly parsed and aligned before scoring
- Query spectrum that is identical to a library entry returns a maximum similarity score (1.0 or 100%)

## Limitations

- The Similarity (EI Simple) algorithm may not account for isomeric spectra that produce nearly identical fragmentation patterns, leading to ambiguous top matches
- Performance depends on library completeness; rare or newly synthesized compounds absent from the reference library will not be identified
- Peak intensity normalization and m/z tolerance thresholds are algorithm-dependent; the specific parameters used by Similarity (EI Simple) are not fully detailed in available documentation

## Evidence

- [intro] Algorithm definition and msp parsing: "custom implementation of the Similarity (EI Simple) algorithm; reading/writing *msp* files"
- [other] Workflow steps: "Load the query EI mass spectrum and msp library file using mssearchr's msp file reading functionality. 2. Parse both spectra to extract m/z and intensity pairs. 3. Implement the Similarity (EI"
- [readme] Primary purpose: "The primary goal of the `mssearchr` package is to enhance the capabilities of R users for conducting library searches against electron ionization mass spectral databases."
- [readme] Core tool offerings: "The `mssearchr` package offers the following tools: - custom implementation of the Identity (EI Normal) algorithm; - custom implementation of the Similarity (EI Simple) algorithm"
