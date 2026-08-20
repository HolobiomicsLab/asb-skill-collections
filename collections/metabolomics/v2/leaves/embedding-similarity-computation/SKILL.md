---
name: embedding-similarity-computation
description: Use when when you have pre-computed embeddings (from MSBERT, Spec2Vec,
  or other deep learning models) for a query spectrum dataset and a reference library,
  and need to measure how well the embedding space ranks correct library matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Anaconda
  - Git
  - MSBERT
  - PyTorch
  - matchms
  - SciPy / NumPy
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c02426
  title: MSBERT
evidence_spans:
- '[Anaconda](https://www.anaconda.com) for Python 3.12'
- Install [Git](https://git-scm.com/downloads)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msbert_cq
    doi: 10.1021/acs.analchem.4c02426
    title: MSBERT
  dedup_kept_from: coll_msbert_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c02426
  all_source_dois:
  - 10.1021/acs.analchem.4c02426
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# embedding-similarity-computation

## Summary

Compute pairwise cosine-similarity scores between query and reference spectrum embeddings to retrieve ranked library matches, then evaluate ranking accuracy (top-1, top-5, top-10 hit rates) against a ground-truth reference library. This skill enables quantitative comparison of embedding models on library matching performance.

## When to use

When you have pre-computed embeddings (from MSBERT, Spec2Vec, or other deep learning models) for a query spectrum dataset and a reference library, and need to measure how well the embedding space ranks correct library matches. Apply this skill when comparing multiple embedding methods or validating whether an embedding model ranks true library hits in the top-k retrieved results.

## When NOT to use

- Query or reference spectra are not yet represented as embeddings; generate embeddings first using an embedding model.
- Ground-truth library annotations or query-to-library mappings are unavailable or ambiguous; rank-based accuracy metrics cannot be computed.
- The embedding model was trained on a different instrument type or chemical domain (e.g., model trained on Q-TOF but applied to Orbitrap); model generalization may be poor.

## Inputs

- Pre-trained embedding model (PyTorch .pkl file, e.g., model/MSBERT.pkl)
- Query spectra dataset (MSP format or pickle; example: example/demo.msp)
- Reference library spectra (MSP format; same source as query, e.g., GNPS Orbitrap set)
- Ground-truth annotations mapping each query to its correct reference library entry

## Outputs

- Ranked list of library matches per query (with cosine-similarity scores)
- Top-1, top-5, top-10 hit rate accuracies (numeric; range 0–1)
- Summary table with accuracy scores and p-values for each embedding method
- Embedding vectors for all query and reference spectra (optional, for downstream analysis)

## How to apply

Load the pre-trained embedding model (e.g., MSBERT) and the test spectra and reference library MSP/pickle files from GNPS or Zenodo. Generate embedding vectors for all query and reference spectra using the model encoder. Compute cosine-similarity scores between each query embedding and all reference embeddings to rank library matches. For each query, extract the rank of the true library match and determine whether it falls in the top-1, top-5, and top-10 positions. Aggregate these binary indicators across all queries to calculate hit rates (e.g., 0.7871 for top-1). Repeat this workflow for baseline methods (e.g., Spec2Vec, raw cosine similarity without embeddings) to enable statistical comparison (paired t-test or chi-squared). Report accuracy scores and p-values in a summary table.

## Related tools

- **MSBERT** (Pre-trained transformer encoder model that generates chemical-rational embeddings of tandem mass spectra for similarity computation) — https://github.com/zhanghailiangcsu/MSBERT
- **PyTorch** (Deep learning framework used to load the model, generate embeddings, and compute tensor-based cosine similarity) — https://pytorch.org/
- **matchms** (Optional workflow integration library for filtering spectra and computing MSBERT similarity scores within a standardized pipeline) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/matchms_workflow
- **SciPy / NumPy** (Compute pairwise cosine similarity matrices and ranking statistics)

## Examples

```
import torch
from model.MSBERTModel import MSBERT
from model.utils import ModelEmbed, ProcessMSP, MSBERTSimilarity

model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
demo_data, demo_smiles = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
cos = MSBERTSimilarity(demo_arr, demo_arr)
```

## Evaluation signals

- Top-k hit rates (top-1, top-5, top-10) for the embedding method must be ≥ baseline methods (e.g., Spec2Vec top-1 ≤ MSBERT top-1 = 0.7871)
- Statistical significance (p-value) from paired t-test or chi-squared test must be < 0.05 to confirm one method outperforms another
- Embedding vectors must have consistent dimensionality (512 for MSBERT) and finite norm across all queries and references
- Cosine-similarity scores must be bounded in [−1, 1] for normalized embeddings; verify no NaN or inf values exist
- Reproducibility check: recomputing rankings on a held-out fold of the same dataset should yield ±2–3% variation in hit rates due to randomness in embedding generation

## Limitations

- Embedding models are instrument-specific; retraining on filtered GNPS subsets by instrument type (Orbitrap, Q-TOF, etc.) is required for best performance on new instruments.
- Top-k accuracy metrics assume exactly one correct library match per query; ambiguous or multiple valid matches may bias evaluation downward.
- Computational cost scales quadratically with library size; very large libraries (> 1 million spectra) may require approximate nearest-neighbor methods (e.g., FAISS) instead of exhaustive search.
- No evaluation of chemical rationality (structural similarity, clustering quality) is performed by this skill alone; separate dimensionality reduction and clustering analyses are needed to validate embedding interpretability.

## Evidence

- [readme] MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset.: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset."
- [other] Compute cosine-similarity matching scores between test and library embeddings, retrieving top-1, top-5, and top-10 ranked matches.: "Compute cosine-similarity matching scores between test and library embeddings, retrieving top-1, top-5, and top-10 ranked matches."
- [other] Calculate rank-based accuracy metrics (top-1, top-5, top-10 hit rates) for all three methods.: "Calculate rank-based accuracy metrics (top-1, top-5, top-10 hit rates) for all three methods."
- [other] Perform statistical significance testing (e.g., paired t-test or chi-squared) to confirm MSBERT outperforms both baselines.: "Perform statistical significance testing (e.g., paired t-test or chi-squared) to confirm MSBERT outperforms both baselines."
- [other] Generate embeddings for all test spectra and reference library spectra using the MSBERT encoder.: "Generate embeddings for all test spectra and reference library spectra using the MSBERT encoder."
- [readme] Calculate the similarity after MSBERT embedding: "Calculate the similarity after MSBERT embedding"
