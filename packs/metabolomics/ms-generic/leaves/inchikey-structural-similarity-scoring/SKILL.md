---
name: inchikey-structural-similarity-scoring
description: Use when you have candidate library matches from MS2Deepscore ranking
  (top 2000 spectra per query) with InChIKey annotations, and need to quantify structural
  similarity between query and candidate compounds to inform downstream match ranking
  and filtering by MS2Query's random forest model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - MS2Query
  - MS2Deepscore
  - Python
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# inchikey-structural-similarity-scoring

## Summary

Compute average InChIKey-based structural similarity scores for candidate library matches in MS2Query by aggregating similarity metrics across matched InChIKey layers. This score is one of five features combined by a random forest to re-rank and select the best analogue or exact match from top spectral candidates.

## When to use

Apply this skill when you have candidate library matches from MS2Deepscore ranking (top 2000 spectra per query) with InChIKey annotations, and need to quantify structural similarity between query and candidate compounds to inform downstream match ranking and filtering by MS2Query's random forest model.

## When NOT to use

- Query spectra or library compounds lack InChIKey or SMILES/InChI annotations; structural similarity cannot be computed without chemical structure metadata.
- Input is already a filtered and ranked result set from MS2Query; the random forest model has already combined InChIKey scoring with four other features.
- Precursor m/z-based filtering is the primary matching criterion; InChIKey scoring is designed for analogue and exact match re-ranking after broad MS2Deepscore pre-selection, not for initial candidate selection.

## Inputs

- Candidate match records with library spectrum identifiers
- InChIKey annotations for query and library spectra
- Structural similarity metrics computed per InChIKey layer

## Outputs

- Scored candidate records with standardized InChIKey similarity scores [0, 1]
- Candidate ranking metadata for downstream random forest re-ranking

## How to apply

Load candidate matches from the library-matching step, each annotated with InChIKey metadata. For each candidate, aggregate structural similarity metrics computed across matched InChIKey layers (e.g., full InChIKey, first block, second block, and third block comparisons) into a single average InChIKey score. Standardize the score to a [0, 1] range compatible with downstream random forest re-ranking. Validate output using unit tests via Python pytest to ensure score ranges are correct and all candidates have assigned scores. Store scores in a structured output record with candidate ID, InChIKey score, and metadata for integration into the five-feature scoring pipeline.

## Related tools

- **MS2Query** (Orchestrates full library matching and re-ranking workflow; uses InChIKey structural similarity as one of five input features for random forest model) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Pre-ranks top 2000 spectral candidates by deep learning similarity; InChIKey scoring operates on this filtered candidate set) — https://github.com/iomega/ms2query
- **Python** (Implementation language for score computation, aggregation, and pytest-based validation)

## Evaluation signals

- All candidate records have InChIKey scores in the range [0, 1]; no missing or out-of-range values.
- Unit tests pass via `python setup.py test` or pytest, validating score computation logic and output structure.
- InChIKey scores correlate positively with manual curation of match quality (higher scores for verified correct matches); score distributions differ between true positives and false positives.
- Candidates with identical InChIKeys to the query receive consistently high scores; candidates with dissimilar InChIKeys receive lower scores.
- Output record structure matches standardized schema (candidate ID, InChIKey score, neighbourhood score, metadata fields) and integrates cleanly into downstream random forest feature vectors.

## Limitations

- InChIKey scoring depends on accurate chemical structure annotation (SMILES, InChI, or InChIKey) in library metadata; compounds without structures are excluded from scoring.
- InChIKey similarity alone does not distinguish between exact matches and structurally similar analogues; neighbourhood scoring and random forest re-ranking are required for final match discrimination.
- No preselection on precursor m/z is performed before InChIKey scoring; scoring is applied to all top 2000 candidates regardless of m/z distance, which may include false positives from mass-unrelated compounds with superficial structural similarity.
- README documents installation and usage but does not detail the technical implementation of InChIKey layer aggregation, score normalization method, or the weights assigned to individual InChIKey block comparisons.

## Evidence

- [other] Compute average InChIKey score for each candidate by aggregating structural similarity metrics across matched InChIKey layers.: "Compute average InChIKey score for each candidate by aggregating structural similarity metrics across matched InChIKey layers."
- [readme] The workflow for running MS2Query first uses MS2Deepscore to calculate spectral similarity scores between all library spectra and a query spectrum. By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly. The top 2000 spectra with the highest MS2Deepscore are selected.: "The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed."
- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features."
- [readme] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [readme] It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library.: "It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library."
