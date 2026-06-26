---
name: similarity-score-computation
description: Use when when you have a query electron ionization mass spectrum (m/z
  and intensity pairs) and need to identify the most similar spectra from an MSP-formatted
  spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# Similarity-Score Computation for EI Mass Spectral Library Search

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute normalized similarity scores between a query electron ionization mass spectrum and library entries using the Identity (EI Normal) or Similarity (EI Simple) algorithm. This skill enables ranking of potential compound matches in spectral databases by their computed similarity to the query spectrum.

## When to use

When you have a query electron ionization mass spectrum (m/z and intensity pairs) and need to identify the most similar spectra from an MSP-formatted spectral library. Apply this skill when your research goal is to find candidate compound identifications ranked by spectral similarity rather than exact matching.

## When NOT to use

- Input library is not in MSP format or is already in a pre-parsed internal representation
- Query spectrum is from a different ionization method (e.g., ESI, APCI) — the Identity/Similarity algorithms are designed specifically for electron ionization
- You require exact nominal mass matches without intensity-weighted similarity scoring

## Inputs

- Query electron ionization mass spectrum (m/z-intensity pairs)
- MSP-formatted spectral library file

## Outputs

- Ranked table of library matches with computed similarity scores
- Match metadata (library entry identifier, compound name, score)

## How to apply

Load the query EI mass spectrum and parse the spectral library from an MSP file. Apply the Identity (EI Normal) algorithm or Similarity (EI Simple) algorithm to compute similarity scores between the query spectrum and each library entry. The algorithm normalizes peak intensities and matches m/z values according to its specification. Rank library entries by descending similarity score to produce a scored match table. Select the algorithm based on your matching stringency requirements: Identity (EI Normal) typically applies stricter criteria for peak matching than Similarity (EI Simple).

## Related tools

- **mssearchr** (Implements custom Identity (EI Normal) and Similarity (EI Simple) algorithms for spectral similarity scoring and MSP file I/O) — https://github.com/AndreySamokhin/mssearchr
- **R** (Host language and runtime environment for mssearchr package execution)
- **NIST API** (Alternative library search backend via external nistms$.exe integration)

## Evaluation signals

- Similarity scores are in a normalized range (typically 0–1 or 0–1000) with no missing or invalid values
- All library entries produce a score; no entries are silently skipped
- Ranked output is sorted in descending order by similarity score
- Top-ranked match has been manually verified against known reference spectra or a ground-truth compound identifier
- Score distributions and magnitude ranges match expected algorithm behavior (e.g., Identity scores are generally lower/stricter than Similarity scores for the same query-library pair)

## Limitations

- Algorithm is specific to electron ionization mass spectra; not applicable to other ionization techniques
- Similarity score alone does not guarantee correct compound identification; additional validation against retention time, molecular weight, or orthogonal methods is recommended
- Performance and accuracy depend on the quality and completeness of the MSP library; sparse or poorly-curated libraries will yield low-confidence matches
- No changelog is publicly available, limiting traceability of algorithm revisions or bug fixes between package versions

## Evidence

- [other] Task workflow step describing the core algorithm application: "Apply the Identity (EI Normal) algorithm to compute similarity scores between the query spectrum and each library entry, normalizing peak intensities and matching m/z values according to the"
- [readme] Tool capabilities statement from README: "custom implementation of the Identity (EI Normal) algorithm; custom implementation of the Similarity (EI Simple) algorithm; reading/writing *msp* files"
- [intro] Article finding on mssearchr purpose and scope: "The mssearchr package provides tools for conducting library searches against electron ionization mass spectral databases"
