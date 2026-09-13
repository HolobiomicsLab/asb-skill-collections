---
name: spectral-structural-similarity-computation
description: Use when when you have pre-trained embedding vectors (e.g., from MSBERT)
  for a collection of mass spectra and need to establish which spectra are chemically
  similar for validation, clustering, or library matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
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
  - scikit-learn
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

# Spectral-Structural Similarity Computation

## Summary

Compute pairwise structural similarity between tandem mass spectra by applying cosine similarity on learned embedding vectors. This skill validates whether embedding spaces capture chemical rationality by quantifying structural correspondence between spectra.

## When to use

When you have pre-trained embedding vectors (e.g., from MSBERT) for a collection of mass spectra and need to establish which spectra are chemically similar for validation, clustering, or library matching. Use this skill after dimensionality reduction if you want to validate that reduced embeddings preserve chemical structure relationships, or on full-dimensional embeddings for exhaustive pairwise comparisons.

## When NOT to use

- Raw, unaggregated mass spectra (m/z, intensity pairs) without pre-computed embeddings; use embedding generation first.
- Similarity computation on spectra from instruments not represented in the MSBERT training data (GNPS Orbitrap); retrain or validate applicability on instrument-specific test sets.
- When comparing spectra across vastly different chemical domains (e.g., metabolomics vs. proteomics fragments) without domain-specific embedding retraining or validation.

## Inputs

- Pre-trained embedding vectors (numpy array or PyTorch tensor, shape: [n_spectra, embedding_dim])
- MSBERT model checkpoint (.pkl file)
- Demo or test mass spectra in .msp format
- Reference chemical structure labels or GNPS dataset annotations (for validation)

## Outputs

- Pairwise similarity matrix (dense or sparse, shape: [n_spectra, n_spectra], values in [0, 1])
- Library matching rank scores (top-1, top-5, top-10 accuracy or matched candidate lists)
- Validated cluster coherence metrics (e.g., silhouette score, Davies-Bouldin index if clustering applied)

## How to apply

Load pre-trained embedding vectors from a trained model checkpoint (e.g., MSBERT.pkl). Compute cosine similarity between all pairs of embedding vectors to produce a similarity matrix. The cosine metric is chosen because embeddings are normalized vector representations where angular distance reflects chemical structure divergence. Validate the resulting similarity scores by cross-referencing clusters or pairs against known chemical classifications in the reference dataset (e.g., GNPS structural families). Score ranges near 1.0 indicate high structural similarity; scores near 0 indicate structural dissimilarity. Use the similarity matrix as input to downstream clustering (k-means, hierarchical) or for library matching rank ordering (e.g., top-1, top-5, top-10 matches).

## Related tools

- **MSBERT** (Provides pre-trained embedding model and similarity computation utilities (ModelEmbed, MSBERTSimilarity functions)) — https://github.com/zhanghailiangcsu/MSBERT
- **PyTorch** (Loads pre-trained model checkpoints and executes cosine similarity computations on GPU/CPU) — https://pytorch.org/
- **matchms** (Integrates MSBERT similarity calculation into spectral matching workflows for library searching) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/matchms_workflow
- **scikit-learn** (Optional: clustering (k-means, hierarchical) and cohesion validation on similarity matrices)

## Examples

```
from model.utils import ModelEmbed, ProcessMSP, MSBERTSimilarity
import torch
from model.MSBERTModel import MSBERT

model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
demo_data, demo_smiles = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
cos = MSBERTSimilarity(demo_arr, demo_arr)
```

## Evaluation signals

- Similarity matrix is symmetric and diagonal equals 1.0 (self-similarity)
- Top-1, top-5, top-10 library matching accuracy on Orbitrap test dataset matches or exceeds reported scores (0.7871, 0.8950, 0.9080 respectively)
- Cosine similarity scores between spectra with identical or near-identical chemical structure (same compound, different instrument runs) cluster near 1.0; unrelated compounds cluster near 0
- Spectral clustering (k-means, hierarchical) on similarity matrix produces coherent clusters matching known chemical families or compound classes in GNPS reference annotations
- Pairwise similarity substantially outperforms baseline methods (Spec2Vec, raw cosine similarity on unreduced spectra) in recall/precision metrics for known compound pairs

## Limitations

- Similarity computation assumes embeddings are derived from MSBERT or a compatible pre-trained model; embeddings from other methods or models may not preserve chemical rationality.
- MSBERT was trained and validated on GNPS Orbitrap data; transferability to other mass spectrometry instruments or spectral formats (e.g., MALDI, APCI) is not established.
- Cosine similarity on embeddings depends critically on the quality and dimensionality of the learned representation; poor embedding quality or dimension mismatch will yield uninformative or misleading similarity scores.
- No changelog is maintained for MSBERT model versions or training hyperparameters, limiting reproducibility and interpretation of changes across releases.

## Evidence

- [intro] Compute pairwise structural similarity between mass spectra using cosine similarity on the reduced embeddings.: "Compute pairwise structural similarity between mass spectra using cosine similarity on the reduced embeddings."
- [intro] MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset.: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset."
- [readme] The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering.: "The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering."
- [readme] Calculate the similarity after MSBERT embedding: cos = MSBERTSimilarity(demo_arr,demo_arr): "Calculate the similarity after MSBERT embedding: cos = MSBERTSimilarity(demo_arr,demo_arr)"
- [readme] MSBERT was trained and tested on GNPS dataset.: "MSBERT was trained and tested on GNPS dataset."
