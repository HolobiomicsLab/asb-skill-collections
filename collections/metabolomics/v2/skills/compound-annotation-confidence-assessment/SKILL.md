---
name: compound-annotation-confidence-assessment
description: Use when you have MS/MS spectra matched to a reference library via both
  identity search (exact or high-similarity matches) and fuzzy/analog search (structurally
  related compounds with similar fragmentation), and you need to prioritize which
  annotations to trust for downstream reporting, validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: huaxuyu/masscube
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-annotation-confidence-assessment

## Summary

Evaluate and rank MS/MS spectral annotations produced by identity and fuzzy search methods, assigning confidence scores that distinguish high-confidence direct matches from lower-confidence analog/structural analogs. This skill is essential for prioritizing validated compound identities in nontargeted metabolomics workflows.

## When to use

Apply this skill when you have MS/MS spectra matched to a reference library via both identity search (exact or high-similarity matches) and fuzzy/analog search (structurally related compounds with similar fragmentation), and you need to prioritize which annotations to trust for downstream reporting, validation, or structural inference. Use it when multiple candidate compounds are returned per spectrum and you must rank them by match reliability.

## When NOT to use

- Input spectra have not yet been searched against a reference library or no library is available; use spectral search first.
- You require only a single 'best match' without confidence quantification or uncertainty communication to end users.
- All spectra are known to be already validated or curated; confidence assessment adds no new value.

## Inputs

- MS/MS experimental spectra (m/z and intensity pairs, typically in mzML or similar LC-MS format)
- MS/MS reference spectral library (indexed collection of known fragmentation patterns with compound metadata)
- Identity search results (matched spectra with similarity scores from library lookup)
- Fuzzy/analog search results (structurally similar compounds with cross-referenced fragmentation patterns)

## Outputs

- Annotated spectrum records with assigned compound identities
- Confidence scores per match (numeric similarity metric)
- Match-type assignments ('identity' or 'analog' search origin)
- Ranked candidate list per spectrum (prioritized by confidence and match type)
- Feature group annotations including isotopes, adducts, and in-source fragments where applicable

## How to apply

After performing identity search and fuzzy search against a spectral library, merge the two result sets and compute or extract confidence scores for each match. Prioritize identity search results (direct spectral matches) over fuzzy search results (analog matches) in the output ranking. Confidence scores should reflect the similarity metric used (e.g., cosine similarity or spectral dot product) between experimental and library spectra. Assign match-type metadata ('identity' vs 'analog') to each candidate so downstream users can filter by certainty. Emit annotated records that include the original spectrum data, assigned compound identity, match type, and confidence score; this enables filtering and validation steps to accept only high-confidence annotations (e.g., cosine > 0.8) or to flag analog-only matches for manual review.

## Related tools

- **masscube** (Implements MS/MS spectrum annotation via identity and fuzzy search, merges results with confidence scoring, and emits annotated records with match type and confidence metadata.) — https://github.com/huaxuyu/masscube/
- **Python** (Language in which masscube is implemented; used to orchestrate spectral matching, score computation, and result ranking logic.)

## Evaluation signals

- Confidence scores are numeric, bounded (e.g., 0–1 or 0–100), and internally consistent within and across match types.
- All annotated spectra include metadata fields: match_type ∈ {'identity', 'analog'}, confidence_score (numeric), and assigned_compound_name.
- Identity search results rank higher (appear earlier in candidate lists) than fuzzy search results when confidence scores are equal or comparable.
- High-confidence matches (e.g., cosine similarity > 0.8) are clearly distinguishable from low-confidence or analog-only matches in the output.
- Original spectrum data (m/z, intensity, retention time) is preserved and linked to every annotation record for traceability.

## Limitations

- Confidence scores depend on the quality and completeness of the reference spectral library; sparse or biased libraries may inflate scores for mediocre matches.
- Fuzzy/analog search may return structurally unrelated compounds if fragmentation patterns happen to overlap; confidence scores alone cannot eliminate false positives.
- No changelog is documented for the masscube package, limiting visibility into changes to confidence scoring logic or annotation thresholds across versions.

## Evidence

- [other] masscube implements MS/MS spectrum annotation through two complementary search strategies: identity search for direct spectral library matching and fuzzy search (analog search) for similarity-based matching against reference spectra.: "masscube implements MS/MS spectrum annotation through two complementary search strategies: identity search for direct spectral library matching and fuzzy search (analog search) for similarity-based"
- [other] Merge identity and fuzzy search results, prioritizing high-confidence matches.: "Merge identity and fuzzy search results, prioritizing high-confidence matches."
- [other] Emit annotated spectrum records containing original spectrum data, assigned identities, match type (identity or analog), and confidence scores.: "Emit annotated spectrum records containing original spectrum data, assigned identities, match type (identity or analog), and confidence scores."
- [intro] Annotation of MS/MS spectra via identity search and fuzzy search (i.e. analog search).: "Annotation of MS/MS spectra via identity search and fuzzy search (i.e. analog search)."
- [readme] masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
