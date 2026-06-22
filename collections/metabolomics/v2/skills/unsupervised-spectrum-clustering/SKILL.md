---
name: unsupervised-spectrum-clustering
description: Use when when you have high-dimensional embedding vectors from pretrained models (e.g., MSBERT) and need to verify that the learned representation space groups spectra by chemical similarity without labeled training data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Anaconda
  - Git
  - PyTorch
  - scikit-learn
  - t-SNE / UMAP
  - MSBERT
  - GNPS
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unsupervised-spectrum-clustering

## Summary

Group tandem mass spectra into chemically coherent clusters by applying spectral clustering (k-means or hierarchical methods) to embedding vectors, validating cluster assignments against known chemical classifications to assess embedding rationality.

## When to use

When you have high-dimensional embedding vectors from pretrained models (e.g., MSBERT) and need to verify that the learned representation space groups spectra by chemical similarity without labeled training data. Apply this skill to validate whether embeddings capture structural rationality before using them for library matching or similarity scoring.

## When NOT to use

- Input spectra are already pre-clustered or from a single known chemical family; clustering will not validate embedding rationality across structural diversity.
- Embedding vectors have not been validated for dimensionality or numerical stability; clustering may produce spurious groups in degenerate or high-noise embeddings.
- Ground-truth chemical classifications are unavailable or unreliable; validation against known families cannot be performed, limiting interpretation of cluster coherence.

## Inputs

- Pretrained embedding vectors (high-dimensional tensor, e.g., from MSBERT checkpoint)
- Tandem mass spectra metadata with known chemical classifications or structural families
- Reference dataset with labeled chemical structures or compound families (e.g., GNPS)

## Outputs

- Cluster assignments (integer labels per spectrum)
- Cluster coherence metrics (e.g., silhouette score, Davies-Bouldin index)
- 2D/3D visualization plots showing clustered spectra in reduced embedding space
- Similarity heatmaps or dendrograms overlaid with chemical labels

## How to apply

Load pretrained embedding vectors from the model checkpoint (e.g., MSBERT.pkl). Apply spectral clustering (k-means or hierarchical clustering) directly on the embedding vectors to partition spectra into groups. Validate cluster coherence by comparing cluster assignments against known chemical classifications or structural families in the reference dataset (e.g., GNPS chemical annotations). Generate visualization plots (optionally after dimensionality reduction via t-SNE or UMAP) showing clustered spectra with chemical labels or similarity heatmaps to inspect whether clusters correspond to expected chemical or structural relationships. High agreement between predicted clusters and ground-truth chemical families indicates the embeddings have captured chemically rational structure.

## Related tools

- **PyTorch** (Load pretrained model checkpoints and compute embedding vectors for clustering) — https://pytorch.org/
- **scikit-learn** (Perform k-means and hierarchical clustering on embedding vectors and compute cluster coherence metrics)
- **t-SNE / UMAP** (Apply dimensionality reduction to project high-dimensional embeddings into 2D/3D space for visualization)
- **MSBERT** (Source pretrained embedding vectors for mass spectra) — https://github.com/zhanghailiangcsu/MSBERT
- **GNPS** (Reference dataset with labeled chemical structures and structural families for cluster validation)

## Examples

```
from sklearn.cluster import KMeans; import torch; model = torch.load('model/MSBERT.pkl'); embeddings = model.encode(spectra); kmeans = KMeans(n_clusters=10).fit(embeddings); labels = kmeans.labels_; print(f'Cluster assignments: {labels}')
```

## Evaluation signals

- Cluster assignments show high purity: >70% of spectra in each cluster belong to the same chemical family or structural class in ground truth.
- Silhouette score or Davies-Bouldin index indicates well-separated clusters (silhouette > 0.5 or DB index < 1.5 for chemically coherent groupings).
- 2D/3D visualization plots reveal tight spatial clustering of spectra with the same chemical label or structural family, with minimal overlap between distinct chemical groups.
- Comparison of predicted cluster assignments against GNPS chemical classifications shows agreement (normalized mutual information or adjusted Rand index > 0.6).
- Cluster centroids in embedding space are stable across re-runs and reflect meaningful chemical or spectroscopic differences between clusters.

## Limitations

- Clustering quality depends on the quality and interpretability of the underlying embedding vectors; poor embeddings will produce uninformative or arbitrary clusters.
- The choice of number of clusters (k in k-means) or linkage method (hierarchical) significantly affects results; no automatic method is provided in the article for optimal k selection.
- Validation is limited to reference datasets with complete and accurate chemical annotations (e.g., GNPS); missing or incorrect labels in ground truth will underestimate cluster coherence.
- Spectral clustering assumes Euclidean geometry in embedding space; if embeddings lie on a manifold or hypersphere, alternative distance metrics or clustering algorithms may be required.
- The method does not identify or handle outlier spectra well; noisy or atypical spectra may form small singleton clusters.

## Evidence

- [other] Perform spectral clustering (e.g., k-means or hierarchical clustering) on the embedding vectors to group chemically similar spectra.: "Perform spectral clustering (e.g., k-means or hierarchical clustering) on the embedding vectors to group chemically similar spectra."
- [other] Validate cluster coherence by comparing clusters against known chemical classifications or structural families in the GNPS dataset.: "Validate cluster coherence by comparing clusters against known chemical classifications or structural families in the GNPS dataset."
- [readme] The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering.: "The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering."
- [other] Generate visualization plots showing clustered spectra in reduced embedding space with chemical labels or similarity heatmaps.: "Generate visualization plots showing clustered spectra in reduced embedding space with chemical labels or similarity heatmaps."
- [readme] MSBERT was trained and tested on GNPS dataset.: "MSBERT was trained and tested on GNPS dataset."
