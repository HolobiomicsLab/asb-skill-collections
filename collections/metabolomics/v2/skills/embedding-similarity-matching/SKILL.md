---
name: embedding-similarity-matching
description: Use when after a CNN model has generated predicted molecular embeddings from mass spectrometry data, and you need to identify the most likely candidate molecules from a reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3765
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - Convolutional Neural Network (CNN)
  - ChemEmbed
  techniques:
  - mass-spectrometry
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

# embedding-similarity-matching

## Summary

Match CNN-predicted molecular embeddings against a reference database using pairwise similarity metrics to rank and filter candidate molecules by confidence score. This skill bridges model predictions to actionable molecular identification in mass spectrometry metabolite workflows.

## When to use

After a CNN model has generated predicted molecular embeddings from mass spectrometry data, and you need to identify the most likely candidate molecules from a reference database. Applies when query embeddings and reference database embeddings are both available in numeric vector form and a ranked candidate list with match confidence scores is the desired output.

## When NOT to use

- Query or reference embeddings are not in a comparable vector space (e.g., from different model architectures or training sets).
- Reference database is empty or contains fewer molecules than the minimum threshold needed for meaningful ranking.
- Input data are already pre-filtered candidate lists rather than embeddings—re-ranking is not necessary.

## Inputs

- CNN-predicted embeddings for query molecules (numeric vectors, typically from spectra data)
- Reference database embeddings (pre-computed numeric vectors from reference molecules)
- Query metadata (molecule identifiers, precursor m/z, adduct type)
- Reference database metadata (molecule identifiers, SMILES or structure information)

## Outputs

- Ranked candidate list (CSV or structured table)
- Match similarity scores (cosine similarity or distance metric values)
- Reference molecule identifiers paired with each candidate
- Top-N candidate molecules per query compound

## How to apply

Load the CNN-predicted embeddings for query molecules and reference database embeddings from trained model outputs. Compute pairwise similarity scores between each query embedding and all reference embeddings using cosine similarity (or Euclidean distance). Rank reference molecules by descending similarity score for each query. Apply a similarity threshold to filter matches and retain only high-confidence candidates—typical thresholds depend on the embedding space properties but the README examples suggest filtering by top-N ranking (e.g., top 5). Generate a ranked candidate list with match scores and reference molecule identifiers. The rationale is that structurally and spectroscopically similar molecules will cluster in embedding space, so high similarity scores indicate plausible molecular identifications.

## Related tools

- **Convolutional Neural Network (CNN)** (Generates predicted molecular embeddings from mass spectrometry spectra data before similarity matching) — https://github.com/massspecdl/ChemEmbed
- **ChemEmbed** (Complete pipeline integrating data preprocessing, CNN prediction, and embedding-based candidate matching for metabolite identification) — https://github.com/massspecdl/ChemEmbed

## Examples

```
# After loading query and reference embeddings:
from scipy.spatial.distance import cdist
similarity_scores = 1 - cdist(query_embeddings, reference_embeddings, metric='cosine')
top_indices = np.argsort(similarity_scores, axis=1)[:, ::-1][:, :5]
results = pd.DataFrame({'query_id': query_ids, 'top_candidates': [reference_ids[idx] for idx in top_indices]})
```

## Evaluation signals

- Similarity scores fall within the expected range for the chosen metric (e.g., 0–1 for cosine similarity, 0–∞ for Euclidean distance).
- Top-ranked candidates have higher similarity scores than lower-ranked candidates for each query (monotonic rank-score alignment).
- Number of candidates returned per query does not exceed the configured top_n_candidates threshold.
- Candidate match results include both similarity scores and reference molecule identifiers for traceability.
- Threshold filtering removes candidates below the similarity cutoff and retains only high-confidence matches (validate by spot-checking a sample of results against known metabolites if available).

## Limitations

- Matching quality depends entirely on CNN embedding quality; poor embeddings will produce false candidates regardless of similarity metric.
- Cosine similarity and Euclidean distance may not equally weight structural features; choice of metric should be validated for the specific metabolite domain.
- Reference database coverage affects recall—candidate identification fails for query molecules with no structurally similar compound in the reference database.
- Threshold selection is user-configurable but not data-driven; inappropriate thresholds can either over-filter (missing true candidates) or under-filter (returning too many false positives).
- The skill does not account for adduct state or ionization mode differences; query and reference embeddings must be from the same ionization polarity.

## Evidence

- [other] Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric (e.g., cosine similarity or Euclidean distance).: "Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric (e.g., cosine similarity or Euclidean distance)."
- [other] Rank reference molecules by similarity score in descending order for each query.: "Rank reference molecules by similarity score in descending order for each query."
- [other] Filter candidate matches by applying a similarity threshold to retain only high-confidence matches.: "Filter candidate matches by applying a similarity threshold to retain only high-confidence matches."
- [readme] Matches predicted embeddings with a reference database to find top candidate molecules based on cosine similarity.: "Matches predicted embeddings with a reference database to find top candidate molecules based on cosine similarity."
- [readme] top_n_candidates: Number of top candidate molecules to retrieve from the reference database. (default: 5): "top_n_candidates: Number of top candidate molecules to retrieve from the reference database. (default: 5)"
