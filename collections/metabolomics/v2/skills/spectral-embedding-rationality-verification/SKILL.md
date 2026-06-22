---
name: spectral-embedding-rationality-verification
description: Use when after training a transformer-encoder-based mass spectrometry embedding model (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - Python
  - Anaconda
  - Git
  - PyTorch
  - scikit-learn
  - matplotlib / seaborn
  - RDKit
  - MSBERT
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
---

# spectral-embedding-rationality-verification

## Summary

Verify that learned mass spectral embeddings preserve chemical and structural meaning by validating dimensionality reduction patterns, structural similarity metrics, and spectral clustering coherence. This skill confirms that the embedding space encodes biologically and chemically rational relationships rather than arbitrary numerical distributions.

## When to use

After training a transformer-encoder-based mass spectrometry embedding model (e.g., MSBERT) on masked contrastive learning, use this skill to validate that the learned representation space meaningfully encodes chemical structure and mass spectral properties before deploying the model for library matching or similarity search tasks.

## When NOT to use

- Embeddings have not yet been trained or validated for basic reconstruction loss—use this skill only after confirming the model converges and produces stable representations.
- Input spectra are uncharacterized or lack reliable structural annotations; rationality verification requires ground-truth chemical labels for comparison.
- The goal is to evaluate raw model performance on library matching (e.g., top-k accuracy)—use direct similarity benchmarking instead; rationality verification is a complementary diagnostic, not a replacement for task-specific metrics.

## Inputs

- trained transformer encoder model weights
- test set of tandem mass spectra (MS/MS)
- molecular structures or SMILES strings for test compounds
- metadata: compound class, precursor m/z, instrument type

## Outputs

- 2D/3D dimensionality-reduced embedding visualization
- structural-similarity vs. embedding-similarity correlation coefficient
- cluster purity and adjusted Rand index scores
- verification report confirming chemical rationality

## How to apply

Apply three complementary validation approaches in sequence: (1) reduce the embedding vectors to 2D or 3D space (e.g., t-SNE or UMAP) and visually inspect whether spectra cluster by molecular structure, instrument type, or known chemical families rather than randomly; (2) compute pairwise structural similarity (e.g., Tanimoto similarity from molecular fingerprints) and correlate it with cosine similarity in the embedding space—higher correlation indicates rationality; (3) perform unsupervised clustering on the embeddings (e.g., k-means or hierarchical clustering) and compare cluster membership against ground-truth chemical annotations (compound class, precursor m/z range, instrument type) using adjusted Rand index or purity metrics. Rationality is demonstrated when visualizations show coherent chemical grouping, structural–embedding similarity correlation is strong (e.g., r > 0.7), and clustering purity exceeds baseline models like Spec2Vec.

## Related tools

- **PyTorch** (Load trained MSBERT model weights and compute embedding vectors from MS/MS input) — https://pytorch.org/
- **scikit-learn** (Perform dimensionality reduction (t-SNE, UMAP), clustering (k-means), and compute metrics (adjusted Rand index, silhouette score))
- **matplotlib / seaborn** (Visualize 2D/3D embedding space with chemical annotations and cluster assignments)
- **RDKit** (Compute molecular fingerprints and pairwise structural similarity (Tanimoto) from SMILES)
- **MSBERT** (Reference implementation demonstrating embedding rationality verification on GNPS Orbitrap test dataset) — https://github.com/zhanghailiangcsu/MSBERT

## Examples

```
from model.MSBERTModel import MSBERT
from model.utils import ModelEmbed, ProcessMSP, MSBERTSimilarity
import torch
model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
demo_data, demo_smiles = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
cos = MSBERTSimilarity(demo_arr, demo_arr)
```

## Evaluation signals

- Dimensionality-reduced visualization (t-SNE/UMAP) shows well-separated clusters corresponding to chemical structure families or instrument types, rather than random or linear scatter.
- Pearson or Spearman correlation between pairwise structural similarity (e.g., Tanimoto from RDKit fingerprints) and cosine similarity in embedding space is statistically significant and > 0.5, indicating embeddings preserve structural information.
- Clustering purity (fraction of spectra in each cluster assigned the correct chemical class) and adjusted Rand index against ground-truth labels exceed corresponding values from baseline models (e.g., Spec2Vec cosine similarity or random embeddings).
- Spectra with high structural similarity (Tanimoto > 0.7) map to nearby regions in embedding space (cosine similarity > 0.6), demonstrating local preservation of chemical relationships.
- MSBERT achieves superior library matching performance (top-1, top-5, top-10 accuracy) compared to non-learned baselines on the same test set, validating that rationality translates to downstream utility.

## Limitations

- Verification relies on ground-truth chemical annotations (molecular structures, SMILES, or compound classes); spectra lacking reliable metadata cannot be validated.
- Structural similarity metrics (e.g., Tanimoto fingerprint similarity) depend on the fingerprint representation chosen; different fingerprints may yield different correlation strengths.
- Rationality is instrument-dependent: embeddings trained on one mass spectrometry platform (e.g., Orbitrap) may not transfer to another (e.g., Q-TOF) without retraining, and verification should be performed per-instrument cohort.
- Visual clustering in low-dimensional space (t-SNE, UMAP) is informative but non-quantitative; t-SNE in particular can create artificial clusters due to perplexity and learning rate tuning; complement with quantitative metrics.

## Evidence

- [readme] The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering.: "The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering."
- [readme] MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset. The results are significantly better than Spec2Vec and cosine similarity.: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset. The results are significantly better than Spec2Vec and cosine"
- [readme] MSBERT used the transformer encoder as the backbone and take advantage of the randomness of the mask to construct positive samples for contrastive learning.: "MSBERT used the transformer encoder as the backbone and take advantage of the randomness of the mask to construct positive samples for contrastive learning."
