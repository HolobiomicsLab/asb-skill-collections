---
name: identity-search-spectrum-annotation
description: Use when you have experimental MS/MS spectra and need to assign definitive molecular identities by matching against a curated spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing
- masscube is an integrated Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  dedup_kept_from: coll_masscube_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-60640-5
  all_source_dois:
  - 10.1038/s41467-025-60640-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# identity-search-spectrum-annotation

## Summary

Annotate experimental MS/MS spectra by matching them against a spectral library using exact or high-confidence similarity scoring to assign molecular identities. This is the direct-match component of spectrum annotation, complementary to fuzzy/analog search for discovering structurally related compounds.

## When to use

Apply this skill when you have experimental MS/MS spectra and need to assign definitive molecular identities by matching against a curated spectral library. Use identity search as your primary annotation strategy when you expect the compound to be represented in your reference library or when high-confidence, unambiguous identity assignments are required for downstream analysis (e.g., targeted validation, metabolite confirmation).

## When NOT to use

- The compound you are looking for is not represented in your spectral library — use fuzzy/analog search instead to find structurally similar analogs.
- You are performing untargeted discovery and need to discover novel or structurally divergent compounds — identity search will not detect these; prioritize fuzzy search.
- Your spectral library is incomplete or poorly curated — low-quality references will produce false-negative identity misses; consider library curation or augmentation before applying identity search.

## Inputs

- experimental MS/MS spectra (mz-intensity pairs with precursor mass)
- spectral library reference data (library spectra with annotated identities, molecular formulas, and metadata)

## Outputs

- annotated spectrum records containing original spectrum data, assigned molecular identity, match type ('identity'), and confidence scores
- high-confidence identity assignments with associated library reference metadata

## How to apply

Load both experimental MS/MS spectra and spectral library reference data into memory. Perform pairwise comparison of experimental spectra against library spectra using similarity-based scoring (e.g., cosine similarity or spectral dot product) with a defined confidence threshold. Accept matches that exceed the threshold as high-confidence identity assignments. Retain the original spectrum data, assigned molecular identity, match confidence score, and metadata (molecular formula, mass, etc.) for each match. Prioritize identity search results over fuzzy search in merged output when both methods return hits, since identity matches carry higher specificity.

## Related tools

- **masscube** (integrated Python package that implements MS/MS spectrum annotation via identity search against spectral library references with similarity scoring) — https://github.com/huaxuyu/masscube/

## Evaluation signals

- All returned identity assignments have confidence scores above the predefined threshold (verify no low-confidence matches are emitted).
- Each annotated spectrum record contains both the original experimental spectrum data and the matched library reference spectrum for manual inspection or visualization.
- Identity search results are reproducible when run against the same library and experimental data (deterministic scoring and ranking).
- Merged identity and fuzzy search results correctly prioritize identity matches over analog matches in the final output (identity records appear first or are explicitly flagged as higher priority).
- Comparison of identity search output against ground-truth metabolite identities shows high recall and precision within the library scope (e.g., >90% correct assignment for compounds known to be in the library).

## Limitations

- Identity search is constrained by library completeness — compounds absent from the reference library will not be identified, even if structurally similar analogs are present.
- Confidence scoring depends on spectral quality and library reference quality; low-resolution or noisy spectra or poorly annotated library entries will reduce sensitivity and specificity.
- Identity search alone cannot discover novel or structurally divergent compounds; it is most effective for re-identifying known metabolites in well-characterized biochemical systems.

## Evidence

- [abstract] identity search and fuzzy search (analog search) methods: "masscube implements MS/MS spectrum annotation through two complementary search strategies: identity search for direct spectral library matching and fuzzy search (analog search) for similarity-based"
- [other] identity search matching process: "Perform identity search by matching experimental spectra against library spectra using exact or high-confidence similarity scoring."
- [other] annotation output structure: "Emit annotated spectrum records containing original spectrum data, assigned identities, match type (identity or analog), and confidence scores."
- [readme] masscube MS/MS annotation capability: "Annotation of MS/MS spectra via identity search and fuzzy search (i.e. analog search)."
- [readme] masscube Python package overview: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
