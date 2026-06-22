---
name: similarity-ranking-and-retrieval-evaluation
description: Use when after training contrastive embeddings that unify MS/MS spectra and molecular structures into a shared embedding space.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - rdkit
  - PyTorch
  - PyTorch Geometric
  - matchms
  - Python
  - conda
  - pip
  - pandas
  - numpy
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01594
  title: CSU-MS2
evidence_spans:
- '- [rdkit](https://rdkit.org/)'
- '- [pytorch](https://pytorch.org/)'
- '- [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/en/latest/)'
- '- [matchms](https://matchms.readthedocs.io/en/latest/)'
- '- [python3](https://www.python.org/)'
- We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_csu_ms2_cq
    doi: 10.1021/acs.analchem.5c01594
    title: CSU-MS2
  dedup_kept_from: coll_csu_ms2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01594
  all_source_dois:
  - 10.1021/acs.analchem.5c01594
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# similarity-ranking-and-retrieval-evaluation

## Summary

This skill evaluates cross-modal retrieval performance by computing cosine similarity between query embeddings and candidate embeddings, ranking results by score, and returning top-k matches with confidence scores. It is essential for assessing whether learned contrastive embeddings correctly align spectral and structural feature spaces for compound identification.

## When to use

Apply this skill after training contrastive embeddings that unify MS/MS spectra and molecular structures into a shared embedding space. Use it when you have encoded query spectra and candidate molecular structures as feature vectors and need to retrieve the most similar structures for a given spectrum, ranked by relevance.

## When NOT to use

- Embeddings have not been learned or trained—run contrastive training first.
- Query spectrum or candidate structures are not yet encoded into the embedding space—encode them using the trained model first.
- Candidate library contains only structural metadata without corresponding embeddings—compute embeddings for all candidates before retrieval.

## Inputs

- query MS/MS spectrum embeddings (real-valued vectors in learned embedding space)
- candidate molecular structure embeddings (real-valued vectors in learned embedding space)
- integer k (number of top matches to return)
- reference library with molecular structures and metadata (CSV or pandas DataFrame with SMILES column)

## Outputs

- ranked list of candidate structures with cosine similarity scores
- top-k matches with confidence scores
- retrieval result table (SMILES, similarity score, rank)

## How to apply

Encode query MS/MS spectra into the learned embedding space using the trained encoder. Encode all candidate molecular structures (provided as SMILES strings or SDF files converted to graph representations) into the same embedding space. Compute cosine similarity between each query spectrum embedding and all candidate structure embeddings. Rank candidates by descending similarity score. Return the top-k candidates with their similarity scores as confidence measures. The ranking directly reflects the alignment quality learned during contrastive training—higher scores indicate stronger spectral-structural correspondence.

## Related tools

- **PyTorch** (Compute cosine similarity between embedding vectors) — https://pytorch.org/
- **pandas** (Organize and manipulate retrieval results (SMILES, scores, rankings))
- **numpy** (Vectorized similarity computation and ranking operations)

## Examples

```
ms_feature = model_inference.ms2_encode(ms_list[i:i+1]); smiles_feature, smiles_list = get_feature(smiles_lst, model_inference=model_inference); indice, score, candidate = get_topK_result(library=smiles_list, ms_feature=ms_feature, smiles_feature=smiles_feature, topK=100)
```

## Evaluation signals

- Top-k retrieval results are ranked in descending order by cosine similarity score (scores monotonically decrease)
- All returned similarity scores fall in the range [−1, 1] (valid cosine similarity range)
- Number of returned candidates equals k or is less than k if candidate library is smaller
- Returned SMILES strings are valid and parseable by rdkit
- Similarity scores for known true matches (ground truth structure for a query spectrum) rank higher than those for random or mismatched structures in benchmark evaluation

## Limitations

- Retrieval quality is bounded by the quality and convergence of contrastive embedding training—poorly trained embeddings produce uninformative rankings.
- Cosine similarity is sensitive to embedding vector magnitude; normalization of embeddings is critical for fair ranking.
- Ranking depends on the completeness and representativeness of the candidate library—absent or rare structures cannot be retrieved.
- Cross-modal retrieval assumes sufficient spectral and structural diversity in the training set; out-of-distribution queries may rank low-confidence candidates highest.

## Evidence

- [other] Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings. Rank candidates by similarity score and output ranked retrieval results with top-k matches and confidence scores.: "Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings. Rank candidates by similarity score and output ranked retrieval results with top-k matches and"
- [readme] Searching in a smiles library with search_library.py function. users Users can load the different collision energy level model according to the collision energy setting, or load three energy level models, and use the weighted scores of different energy levels as the final score: "Searching in a smiles library with search_library.py function. users Users can load the different collision energy level model according to the collision energy setting"
- [readme] indice, score, candidate = get_topK_result(library=smiles_list,ms_feature=ms_feature, smiles_feature=smiles_feature, topK=100): "indice, score, candidate = get_topK_result(library=smiles_list,ms_feature=ms_feature, smiles_feature=smiles_feature, topK=100)"
