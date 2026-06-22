---
name: mass-spectrum-peak-matching
description: Use when when you have a query electron ionization mass spectrum (as m/z and intensity pairs) and need to identify it against a spectral library stored in msp format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - mssearchr
  - R
  - NIST API
  techniques:
  - GC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-peak-matching

## Summary

Peak matching is the core operation in electron ionization (EI) mass spectral library search, where m/z values and intensity pairs from a query spectrum are compared against library entries using algorithm-specific scoring (Identity EI Normal or Similarity EI Simple) to rank candidate matches. This skill bridges raw spectral data to ranked library hits, enabling compound identification in metabolomics and analytical chemistry.

## When to use

When you have a query electron ionization mass spectrum (as m/z and intensity pairs) and need to identify it against a spectral library stored in msp format. Apply this skill when the goal is to find the most similar or identical library entries ranked by match score, rather than performing de novo structure elucidation or working with other ionization types (APCI, ESI).

## When NOT to use

- Input spectra are from non-EI ionization methods (ESI, APCI, MALDI, etc.) — the algorithms are tuned for EI fragmentation patterns.
- Library file is not in msp format or lacks properly formatted m/z–intensity pairs.
- Goal is to perform spectrum-spectrum comparison without ranking against a curated library.

## Inputs

- query electron ionization mass spectrum (m/z and intensity pairs)
- msp library file containing reference EI spectra

## Outputs

- ranked table of library matches with similarity or identity scores
- scored match table sorted by descending match score

## How to apply

Load the query EI mass spectrum and parse the msp library file using mssearchr's msp reader to extract m/z and intensity pairs from both. Select either the Identity (EI Normal) algorithm for strict normalized peak matching or the Similarity (EI Simple) algorithm for relaxed matching, depending on your tolerance for partial spectral matches. Compute pairwise similarity or identity scores between the query spectrum and each library entry by normalizing peak intensities and matching m/z values according to the algorithm specification. Rank all library entries by descending score and return the scored match table, with the highest-ranking entry as the primary match candidate.

## Related tools

- **mssearchr** (Provides custom implementations of Identity (EI Normal) and Similarity (EI Simple) algorithms, msp file readers, and the scoring pipeline for peak matching and ranking.) — https://github.com/AndreySamokhin/mssearchr
- **R** (Execution environment for mssearchr functions and workflow automation.)
- **NIST API** (Alternative route for library search against NIST electron ionization spectral databases via nistms$.exe.)

## Evaluation signals

- Output table is ranked by descending score and contains at least one match entry with a non-null similarity/identity score.
- All m/z values in both query and library spectra are positive numbers; intensity pairs are normalized (typically 0–999 or 0–100 scale).
- Top-ranked library match m/z values align with query spectrum peaks within algorithm tolerance; no m/z values are duplicated in a single spectrum row.
- Similarity or identity scores fall within the expected range for the chosen algorithm (e.g., 0–1000 for normalized EI algorithms).
- Query spectrum is successfully parsed and compared against all library entries without crashing or returning NaN/null scores for valid entries.

## Limitations

- Peak matching accuracy depends on msp library quality; corrupted or incomplete library entries may produce spurious matches.
- Identity (EI Normal) algorithm requires strict peak intensity normalization; if library or query spectra are unnormalized or use different intensity scales, scores may be misleading.
- Similarity (EI Simple) algorithm may produce high false-positive scores if library spectra are very similar but not identical; additional confirmation (e.g., retention index, molecular weight, complementary MS/MS) is recommended.
- Algorithm is optimized for EI spectra; non-EI spectra (ESI, APCI) will yield invalid or meaningless match scores.

## Evidence

- [readme] core algorithm definitions: "custom implementation of the Identity (EI Normal) algorithm"
- [readme] file format support: "reading/writing *msp* files"
- [other] workflow steps from task_001: "Apply the Identity (EI Normal) algorithm to compute similarity scores between the query spectrum and each library entry, normalizing peak intensities and matching m/z values according to the"
- [other] output format from task_002: "Return a ranked list or table of library matches with their corresponding similarity scores"
