---
name: fuzzy-analog-search-fragmentation
description: Use when when you have experimental MS/MS spectra and want to discover structurally similar compounds beyond exact spectral library matches—particularly useful for identifying chemical analogs, homologs, or isomers that share fragmentation logic but differ in molecular structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
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

# fuzzy-analog-search-fragmentation

## Summary

Identify structurally related compounds with similar MS/MS fragmentation patterns but different molecular identities by performing fuzzy (analog) search against a spectral library. This complements identity search to discover chemical analogs and detect novel compounds with known fragmentation signatures.

## When to use

When you have experimental MS/MS spectra and want to discover structurally similar compounds beyond exact spectral library matches—particularly useful for identifying chemical analogs, homologs, or isomers that share fragmentation logic but differ in molecular structure. Apply this after or alongside identity search when nontargeted metabolomics seeks comprehensive annotation coverage.

## When NOT to use

- When only exact compound identification is required and false-positive analog matches would confound downstream analysis.
- When spectral library quality is poor or lacks comprehensive coverage, as fuzzy search relies on reference spectrum reliability.
- When computational resources are severely limited, as fuzzy search against large libraries is more expensive than simple identity lookup.

## Inputs

- Experimental MS/MS spectra (mass-to-charge ratios and intensities)
- Spectral library reference data (library spectra with known molecular identities and fragmentation patterns)

## Outputs

- Annotated spectrum records with assigned analog identities
- Match type labels ('identity' vs. 'analog')
- Confidence scores for each match
- Merged identity and fuzzy search results ranked by confidence

## How to apply

Load experimental MS/MS spectra and a reference spectral library into masscube. Execute fuzzy search (analog search) by comparing experimental spectra against library spectra using similarity-based scoring rather than exact matching. The method identifies reference compounds whose fragmentation patterns exhibit high cosine similarity or other spectral similarity metrics to the experimental spectrum, even when molecular identities differ. Merge fuzzy search results with identity search results, prioritizing high-confidence matches. Fuzzy search results are tagged with match type 'analog' and assigned confidence scores to distinguish them from direct identity matches, enabling downstream filtering and validation.

## Related tools

- **masscube** (Integrated Python package that implements fuzzy/analog search for MS/MS spectral annotation alongside identity search strategies) — https://github.com/huaxuyu/masscube/
- **Python** (Programming language substrate for masscube implementation and fuzzy search workflow orchestration)

## Evaluation signals

- All experimental spectra receive annotated records with assigned analog identities and 'analog' match type labels.
- Fuzzy search results correctly prioritize high-confidence matches (e.g., cosine similarity scores above an explicit threshold) when merged with identity results.
- Analog matches correspond to compounds with similar fragmentation patterns but distinct molecular structures relative to the experimental spectrum.
- Confidence score distributions for analog matches are lower or non-overlapping with identity match distributions, reflecting the reduced specificity of similarity-based matching.
- No spectrum is left unannotated unless it falls below the minimum similarity threshold; coverage should be tracked and reported.

## Limitations

- Fuzzy search efficacy depends critically on spectral library completeness and quality; sparse or biased libraries may miss true analogs or return false-positive matches.
- Similarity scoring thresholds (e.g., cosine similarity cutoffs) must be empirically tuned; overly permissive thresholds inflate false positives, while overly stringent thresholds miss valid analogs.
- Computational cost scales with library size; large spectral libraries or high-resolution spectra may impose performance bottlenecks.
- Chemical meaning of 'analog' varies by fragmentation mechanism; spectra with coincidentally similar peaks may be flagged as analogs despite lacking structural relevance.

## Evidence

- [other] Perform fuzzy/analog search to identify structurally related compounds with similar fragmentation patterns but different molecular identities.: "Perform fuzzy/analog search to identify structurally related compounds with similar fragmentation patterns but different molecular identities."
- [readme] Annotation of MS/MS spectra via identity search and fuzzy search (i.e. analog search).: "Annotation of MS/MS spectra via identity search and fuzzy search (i.e. analog search)."
- [other] Merge identity and fuzzy search results, prioritizing high-confidence matches. Emit annotated spectrum records containing original spectrum data, assigned identities, match type (identity or analog), and confidence scores.: "Merge identity and fuzzy search results, prioritizing high-confidence matches. Emit annotated spectrum records containing original spectrum data, assigned identities, match type (identity or analog),"
