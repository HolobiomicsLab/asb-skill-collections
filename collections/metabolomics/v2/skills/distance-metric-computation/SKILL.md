---
name: distance-metric-computation
description: Use when after obtaining CNN-predicted embeddings for query mass spectra and having loaded pre-computed embeddings from a reference database, you need to identify which reference molecules are most similar to each query.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0208
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0602
  tools:
  - Convolutional Neural Network (CNN)
  - cosine similarity / Euclidean distance
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

# distance-metric-computation

## Summary

Compute pairwise similarity or distance scores between query molecular embeddings and a reference database of embeddings to rank candidate molecules for metabolite identification. This skill bridges CNN predictions and candidate ranking by quantifying embedding proximity.

## When to use

After obtaining CNN-predicted embeddings for query mass spectra and having loaded pre-computed embeddings from a reference database, you need to identify which reference molecules are most similar to each query. Apply this skill when the goal is to rank candidate molecules by embedding similarity for subsequent filtering and reporting.

## When NOT to use

- Input embeddings have not been generated or validated by the CNN model — apply CNN prediction first.
- Reference database is empty or has not been preprocessed into the required embedding format.
- Candidate ranking is not the intended next step; if you only need raw distances for other purposes, this skill's ranking and filtering context may be unnecessary.

## Inputs

- CNN-predicted molecular embeddings for query spectra (vector or tensor format)
- Reference database embeddings (vector or tensor format, pre-computed from trained CNN)
- Query-reference pairs or full cross-product of query and reference sets

## Outputs

- Pairwise similarity/distance matrix (query × reference dimensions)
- Ranked candidate list sorted by similarity score in descending order per query
- Match scores (similarity values) paired with reference molecule identifiers

## How to apply

Load the CNN-predicted embeddings for query molecules and reference database embeddings from the trained model output. Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric such as cosine similarity or Euclidean distance. The choice of metric depends on the embedding space geometry: cosine similarity is recommended for high-dimensional normalized embeddings, while Euclidean distance is suitable for unnormalized spaces. Rank reference molecules in descending order by similarity score for each query. This ranking forms the basis for downstream candidate filtering by similarity threshold.

## Related tools

- **Convolutional Neural Network (CNN)** (Generates the molecular embeddings (query and reference) that serve as input to distance metric computation) — https://github.com/faizanurv/ChemEmbed
- **cosine similarity / Euclidean distance** (Distance metric for computing pairwise similarity scores between embeddings in the reference-matching step) — https://github.com/faizanurv/ChemEmbed

## Examples

```
from scipy.spatial.distance import cdist; import numpy as np; query_embeddings = np.load('query_embeddings.npy'); ref_embeddings = np.load('reference_embeddings.npy'); similarity_matrix = 1 - cdist(query_embeddings, ref_embeddings, metric='cosine'); ranked_indices = np.argsort(-similarity_matrix, axis=1)
```

## Evaluation signals

- Verify that all query embeddings have been matched against the full reference database (no queries or references skipped).
- Check that similarity/distance scores are within expected numerical ranges for the chosen metric (e.g., cosine similarity ∈ [−1, 1], Euclidean distance ≥ 0).
- Confirm that ranked candidate lists are sorted in descending order of similarity and that the top-ranked candidate has the highest score.
- Validate that the number of candidate scores per query equals the size of the reference database before filtering.
- Spot-check at least one query–reference pair distance calculation by manual computation to ensure metric implementation is correct.

## Limitations

- Distance metric computation assumes embeddings are already in a comparable vector space; misaligned or differently-scaled embeddings will produce misleading rankings.
- High-dimensional embeddings may suffer from the curse of dimensionality, making distance metrics less discriminative; this is a property of the embedding space, not the distance computation itself.
- Cosine similarity treats all dimensions equally and ignores magnitude; if magnitude carries semantic information, alternative metrics should be considered.
- The README does not specify whether embeddings are L2-normalized before cosine similarity computation, which affects numerical stability and interpretation.
- No threshold or filtering is applied during metric computation itself; high-scoring but low-confidence matches will be ranked highly until a downstream filter is applied.

## Evidence

- [other] Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric (e.g., cosine similarity or Euclidean distance).: "Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric (e.g., cosine similarity or Euclidean distance)."
- [other] Rank reference molecules by similarity score in descending order for each query.: "Rank reference molecules by similarity score in descending order for each query."
- [readme] Matches predicted embeddings with a reference database to find top candidate molecules based on cosine similarity.: "Matches predicted embeddings with a reference database to find top candidate molecules based on cosine similarity."
- [other] Load CNN-predicted embeddings for query molecules and reference database embeddings from the trained model output.: "Load CNN-predicted embeddings for query molecules and reference database embeddings from the trained model output."
