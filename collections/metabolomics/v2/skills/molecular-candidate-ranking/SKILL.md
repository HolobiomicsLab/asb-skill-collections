---
name: molecular-candidate-ranking
description: Use when after a trained CNN model has generated molecular embeddings
  for query spectra, and you need to retrieve the most likely candidate molecules
  from a reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  tools:
  - Convolutional Neural Network (CNN)
  - ChemEmbed
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2025.02.07.637102v1
  title: ChemEmbed
evidence_spans:
- perform predictions using a trained Convolutional Neural Network (CNN) model
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemembed_cq
    doi: 10.1101/2025.02.07.637102v1
    title: ChemEmbed
  dedup_kept_from: coll_chemembed_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.02.07.637102v1
  all_source_dois:
  - 10.1101/2025.02.07.637102v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-candidate-ranking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Rank reference database molecules by similarity to CNN-predicted molecular embeddings to identify the most likely candidate structures. This skill bridges model prediction and molecule identification by filtering and ordering matches using distance metrics.

## When to use

After a trained CNN model has generated molecular embeddings for query spectra, and you need to retrieve the most likely candidate molecules from a reference database. Use this skill when you have both predicted embeddings (from MS/MS spectra) and pre-computed reference database embeddings, and similarity scores alone are insufficient—you need a ranked, filtered list ordered by match confidence.

## When NOT to use

- Query embeddings have not been generated or validated—embedding quality directly determines ranking validity.
- Reference database embeddings are stale or incompatible with the query embedding space (e.g., from a different CNN architecture or training run).
- The number of candidates required is extremely large (>1000) or the database is too small (<10 reference compounds), making ranking less discriminative.

## Inputs

- CNN-predicted molecular embeddings for query spectra (vector format)
- Reference database embeddings (pre-computed vector representations)
- Similarity threshold parameter (float, typically 0.5–0.95 depending on metric)
- Distance metric specification (e.g., 'cosine_similarity' or 'euclidean')

## Outputs

- Ranked candidate list (molecules sorted by decreasing similarity score)
- Match scores for each candidate (numeric, 0–1 or distance units)
- Reference molecule identifiers (e.g., InChI, compound names, database IDs)
- Filtered candidates CSV or structured table with top-N results

## How to apply

Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric such as cosine similarity or Euclidean distance. Rank reference molecules in descending order by similarity score for each query compound. Apply a similarity threshold to retain only high-confidence matches, filtering out weak matches below the threshold. Generate a ranked candidate list annotated with match scores and reference molecule identifiers. The ranking and filtering steps are interdependent: the distance metric choice (cosine vs. Euclidean) directly affects which molecules rank highest, and the threshold acts as a hard cutoff to control candidate set size and false-positive rate.

## Related tools

- **Convolutional Neural Network (CNN)** (Generates molecular embeddings from MS/MS spectra that serve as query vectors for similarity computation) — https://github.com/massspecdl/ChemEmbed
- **ChemEmbed** (End-to-end framework implementing the full pipeline from spectra preprocessing through CNN prediction to candidate matching and ranking) — https://github.com/massspecdl/ChemEmbed

## Examples

```
python main.py --config config.yaml
# where config.yaml specifies top_n_candidates: 5, distance metric: cosine_similarity, similarity_threshold: 0.7
```

## Evaluation signals

- Ranked list is sorted in descending order by similarity score with no inversions or ties inconsistently ordered.
- All candidates in the output exceed the specified similarity threshold; no candidates below threshold are retained.
- Reference molecule identifiers in output match valid entries in the reference database pickle file (no orphaned or corrupted IDs).
- Match scores are within expected range (0–1 for cosine similarity, or non-negative for Euclidean distance) and are mathematically consistent with the distance metric used.
- Top-N candidates returned does not exceed the configured `top_n_candidates` parameter; list is truncated or padded consistently if fewer high-scoring matches exist.

## Limitations

- Ranking quality depends critically on the quality and representativeness of reference database embeddings; sparse or biased reference databases will produce poor candidate sets even with high similarity scores.
- The choice of distance metric (cosine vs. Euclidean) significantly impacts ranking order; no universal metric works optimally across all embedding spaces or chemical domains.
- Threshold selection is data- and model-dependent; a fixed threshold may be too stringent on small databases or too permissive on large ones, and the README does not provide principled guidance for threshold tuning.
- The framework matches embeddings without considering chemical feasibility, synthetic accessibility, or domain-specific priors; a highly ranked candidate may be chemically implausible or unavailable.

## Evidence

- [other] Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric (e.g., cosine similarity or Euclidean distance).: "Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric (e.g., cosine similarity or Euclidean distance)."
- [other] Rank reference molecules by similarity score in descending order for each query.: "Rank reference molecules by similarity score in descending order for each query."
- [other] Filter candidate matches by applying a similarity threshold to retain only high-confidence matches.: "Filter candidate matches by applying a similarity threshold to retain only high-confidence matches."
- [readme] Matches predicted embeddings with a reference database to find top candidate molecules based on cosine similarity.: "Matches predicted embeddings with a reference database to find top candidate molecules based on cosine similarity."
- [readme] top_n_candidates: Number of top candidate molecules to retrieve from the reference database. (default: 5): "top_n_candidates: Number of top candidate molecules to retrieve from the reference database. (default: 5)"
