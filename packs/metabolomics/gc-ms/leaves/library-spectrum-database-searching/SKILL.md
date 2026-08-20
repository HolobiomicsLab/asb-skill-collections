---
name: library-spectrum-database-searching
description: Use when you have an unknown electron ionization (EI) mass spectrum and need to identify the compound by comparing it against a reference library (msp file format).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - mssearchr
  - R
  - NIST API
  techniques:
  - GC-MS
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

# library-spectrum-database-searching

## Summary

Search electron ionization mass spectra against reference libraries using spectral similarity algorithms to identify unknown compounds. This skill compares a query mass spectrum against library entries using standardized matching algorithms, returning ranked candidate identifications with quantitative similarity scores.

## When to use

You have an unknown electron ionization (EI) mass spectrum and need to identify the compound by comparing it against a reference library (msp file format). Use this skill when you want rapid, automated matching of query spectra to library entries ranked by similarity, rather than manual peak comparison.

## When NOT to use

- Input spectra are from ionization methods other than electron ionization (EI)—use method-specific algorithms for ESI, APCI, or other soft ionization techniques.
- You require sub-parts structural matching or fragmentation tree comparison rather than overall spectral similarity scoring.
- The msp library file is malformed or contains spectra that lack m/z and intensity values.

## Inputs

- Query electron ionization (EI) mass spectrum (m/z and intensity pairs)
- MSP library file (msp format) containing reference spectra

## Outputs

- Ranked table of library matches with similarity scores
- Library entry metadata for top-ranked candidates

## How to apply

Load the query EI mass spectrum and msp library file into mssearchr using its msp file reading functionality. Parse both spectra to extract m/z and intensity pairs. Select an appropriate similarity algorithm: use the Identity (EI Normal) algorithm for high-confidence exact matches, or the Similarity (EI Simple) algorithm for more permissive matching that tolerates minor peak differences. Compute pairwise similarity scores between the query spectrum and each library entry. Return a ranked list or table of library matches sorted by similarity score in descending order. Evaluate matches by inspecting the top-ranked candidates and their corresponding scores to judge whether the match quality is sufficient for your analytical confidence threshold.

## Related tools

- **mssearchr** (R package providing custom implementations of Identity (EI Normal) and Similarity (EI Simple) algorithms, msp file I/O, and library search orchestration) — https://github.com/AndreySamokhin/mssearchr
- **NIST API** (Alternative library search backend accessed via mssearchr by calling the nistms$.exe file for remote spectral matching)

## Evaluation signals

- Returned similarity scores lie in the expected range (typically 0–1 or 0–1000, depending on algorithm); extreme values suggest parsing or algorithmic errors.
- Top-ranked match(es) have reasonable chemical interpretation: the proposed compound's known fragmentation pattern aligns visually with the query spectrum's major peaks.
- Ranked list is sorted in descending order of similarity; identity of top match is reproducible when the same query and library are re-run.
- Number of returned matches equals or approximates the number of library entries (accounting for any filtering); missing or duplicate results indicate msp file reading or iteration failure.
- Query spectrum m/z and intensity values are correctly extracted and compared (spot-check a few library entries by independent manual similarity calculation).

## Limitations

- Performance and accuracy depend on the completeness and quality of the msp reference library; sparse or poorly-annotated libraries yield unreliable matches.
- Similarity (EI Simple) algorithm is permissive and may produce false positives if the query spectrum is noisy or contaminated with background peaks.
- The package does not handle non-EI ionization methods; MS/MS or soft-ionization spectra require different algorithms.
- No built-in visualization or statistical significance testing (e.g., p-values or confidence intervals) for match quality; users must interpret raw scores subjectively.

## Evidence

- [readme] The primary goal of the `mssearchr` package is to enhance the capabilities of R users for conducting library searches against electron ionization mass spectral databases.: "The primary goal of the `mssearchr` package is to enhance the capabilities of R users for conducting library searches against electron ionization mass spectral databases."
- [other] The mssearchr package offers a custom implementation of the Similarity (EI Simple) algorithm as one of its core tools for library searches against electron ionization mass spectral databases.: "custom implementation of the Similarity (EI Simple) algorithm as one of its core tools for library searches"
- [readme] The package implements custom versions of both the Identity (EI Normal) and Similarity (EI Simple) algorithms, as well as support for msp file I/O.: "custom implementation of the Identity (EI Normal) algorithm; custom implementation of the Similarity (EI Simple) algorithm; reading/writing *msp* files."
- [other] The workflow for reconstructing the similarity algorithm involves loading spectra, parsing m/z and intensity pairs, computing pairwise similarity scores, and returning ranked matches.: "1. Load the query EI mass spectrum and msp library file using mssearchr's msp file reading functionality. 2. Parse both spectra to extract m/z and intensity pairs. 3. Implement the Similarity (EI"
