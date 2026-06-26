---
name: spectral-similarity-scoring-ei-simple
description: Use when you have a query electron ionization (EI) mass spectrum and
  need to search it against a library of known EI mass spectra to identify unknown
  compounds. Use it when exact identity matching (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - mssearchr
  - R
  - NIST API
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.5c00322
  title: mspepsearchr
evidence_spans:
- The primary goal of the `mssearchr` package is to enhance the capabilities of R
  users for conducting library searches against electron ionization mass spectral
  databases.
- The primary goal of the `mssearchr` package is to enhance the capabilities of R
  users
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00322
  all_source_dois:
  - 10.1021/jasms.5c00322
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Similarity Scoring (EI Simple)

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

The Similarity (EI Simple) algorithm computes pairwise similarity scores between a query electron ionization mass spectrum and library entries to identify and rank matching compounds. It is a core method for unbiased library searching in mass spectrometry when the query spectrum is not an exact match to any library entry.

## When to use

Apply this skill when you have a query electron ionization (EI) mass spectrum and need to search it against a library of known EI mass spectra to identify unknown compounds. Use it when exact identity matching (e.g., via the Identity/EI Normal algorithm) fails or when you want ranked similarity scores across all library entries rather than only perfect matches.

## When NOT to use

- When you need to identify a spectrum that matches a known library entry exactly — use the Identity (EI Normal) algorithm instead.
- When your input spectra are not electron ionization (EI) spectra (e.g., ESI, APCI, or other ionization modes).
- When the query spectrum is already preprocessed into a pre-computed feature or similarity vector — this skill operates on raw m/z and intensity data.

## Inputs

- Query electron ionization mass spectrum (m/z and intensity pairs)
- MSP library file (mass spectrum database in msp format)

## Outputs

- Ranked list of library matches with similarity scores
- Pairwise similarity score matrix (query vs. library entries)

## How to apply

Load the query EI mass spectrum and an msp library file using mssearchr's msp file reading functionality. Parse both spectra to extract m/z and intensity pairs. Implement or invoke the Similarity (EI Simple) algorithm to compute pairwise similarity scores between the query spectrum and each library entry. The algorithm compares spectral peaks (m/z and intensity) according to the EI Simple scoring scheme; higher scores indicate greater spectral resemblance. Return a ranked list or table of library matches ordered by similarity score (descending). Evaluate the quality of matches by examining the top-ranked candidates and their similarity scores to determine confidence in the assignment.

## Related tools

- **mssearchr** (Provides custom implementation of the Similarity (EI Simple) algorithm and msp file parsing for library search workflows in R) — https://github.com/AndreySamokhin/mssearchr
- **R** (Computational environment for executing mssearchr workflows and manipulating similarity score results)
- **NIST API** (Alternative library search backend for electron ionization mass spectra accessible via mssearchr)

## Evaluation signals

- Similarity scores are returned for all library entries (no missing values for valid spectra pairs).
- Scores are numeric and bounded in the expected range for the EI Simple metric (typically 0–1 or 0–999 depending on implementation); inspect raw output to confirm normalization.
- Top-ranked library matches align with expected compound identification based on experimental context (e.g., retention time, sample history, known constituents).
- The ranked list is ordered in descending order of similarity score with no ties or inversions that violate the ordering.
- Query spectrum and at least one library entry produce non-zero similarity scores (confirming algorithm executed and scored matches).

## Limitations

- The Similarity (EI Simple) algorithm is specific to electron ionization mass spectra; it is not applicable to spectra from other ionization modes.
- Similarity scores depend on the quality and completeness of the library database; missing or poorly annotated library entries can reduce match reliability.
- The algorithm does not account for retention time, isotope patterns, or other orthogonal information; it scores only on m/z and intensity.
- No changelog is available for the mssearchr package, limiting visibility into algorithm refinements or bug fixes across versions.

## Evidence

- [intro] custom implementation of the Similarity (EI Simple) algorithm: "The mssearchr package offers the following tools: - custom implementation of the Similarity (EI Simple) algorithm"
- [intro] library searches against electron ionization mass spectral databases: "The primary goal of the `mssearchr` package is to enhance the capabilities of R users for conducting library searches against electron ionization mass spectral databases."
- [other] Parse both spectra to extract m/z and intensity pairs; Implement the Similarity (EI Simple) algorithm to compute pairwise similarity scores: "Parse both spectra to extract m/z and intensity pairs. 3. Implement the Similarity (EI Simple) algorithm to compute pairwise similarity scores between the query spectrum and each library entry."
- [other] Return a ranked list or table of library matches with their corresponding similarity scores: "Return a ranked list or table of library matches with their corresponding similarity scores."
- [readme] reading/writing *msp* files: "- reading/writing *msp* files."
