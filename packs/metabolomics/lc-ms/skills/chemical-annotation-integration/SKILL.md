---
name: chemical-annotation-integration
description: Use when after training a tandem mass spectrometry embedding model (such as MSBERT) on a reference spectral library (e.g., GNPS), apply this skill to confirm that the high-dimensional embedding vectors project into interpretable chemical space.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2422
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3407
  tools:
  - Python
  - Anaconda
  - Git
  - PyTorch
  - scikit-learn
  - t-SNE / UMAP
  - Matplotlib / Seaborn
  - matchms
  techniques:
  - LC-MS
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

# Chemical-Annotation Integration

## Summary

Validate that learned embedding vectors encode chemically rational structure by subjecting them to dimensionality reduction, pairwise structural similarity computation, and spectral clustering, then comparing cluster membership against known chemical classifications. This skill verifies that an embedding model has captured meaningful chemical relationships rather than learning spurious patterns.

## When to use

After training a tandem mass spectrometry embedding model (such as MSBERT) on a reference spectral library (e.g., GNPS), apply this skill to confirm that the high-dimensional embedding vectors project into interpretable chemical space. Use when you need to demonstrate that spectra cluster by chemical family, structural similarity, or instrument type, and when you have ground-truth chemical labels or structural classifications available for validation.

## When NOT to use

- You lack ground-truth chemical annotations or structural classifications to validate against; without reference labels, cluster coherence cannot be objectively assessed.
- Your embedding model has not yet been trained or the checkpoint file is missing or corrupt; this skill validates an already-learned representation, not the training process itself.
- Your input spectra lack sufficient diversity or your reference library is too small to produce meaningful clusters; weak clustering signals will result in inconclusive validation.

## Inputs

- Pre-trained embedding model checkpoint (.pkl or .pth file)
- Tandem MS spectra in MSP or mzML format
- High-dimensional embedding vectors (output from trained encoder)
- Ground-truth chemical annotations or structural family labels from reference library

## Outputs

- 2D or 3D dimensionality-reduced embedding coordinate matrix
- Pairwise cosine similarity matrix or distance matrix
- Cluster assignment labels (per spectrum)
- Cluster coherence metrics (e.g., silhouette score, within-cluster vs. between-cluster distance)
- Visualization plots (t-SNE/UMAP scatter with chemical labels, similarity heatmaps, cluster dendrograms)

## How to apply

First, load the pre-trained embedding vectors from the trained model checkpoint. Apply dimensionality reduction (t-SNE or UMAP) to project the high-dimensional embeddings into 2D or 3D visualization space. Compute pairwise structural similarity between spectra using cosine similarity on the reduced embeddings. Perform spectral clustering (k-means or hierarchical clustering) on the embedding vectors to group chemically similar spectra. Finally, validate cluster coherence by comparing cluster membership against known chemical classifications, structural families, or instrument types in your reference dataset (e.g., GNPS annotations), and generate visualization plots (scatter plots, similarity heatmaps) with chemical labels overlaid on the reduced embedding space.

## Related tools

- **PyTorch** (Load pre-trained MSBERT model checkpoint and compute embedding vectors from spectra) — https://pytorch.org/
- **scikit-learn** (Perform dimensionality reduction (t-SNE, UMAP wrapper) and spectral clustering (k-means, hierarchical clustering))
- **t-SNE / UMAP** (Project high-dimensional embeddings into 2D or 3D space for visualization and structural similarity assessment)
- **Matplotlib / Seaborn** (Generate scatter plots, heatmaps, and dendrograms to visualize clustered spectra in embedding space with chemical labels)
- **matchms** (Load and preprocess MSP/mzML spectra, compute similarity matrices, integrate MSBERT similarity scoring) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/matchms_workflow

## Examples

```
from model.MSBERTModel import MSBERT
from model.utils import ModelEmbed, ProcessMSP
import torch
model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
demo_data, demo_smiles = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
from sklearn.manifold import TSNE
embedding_2d = TSNE(n_components=2).fit_transform(demo_arr)
from sklearn.cluster import KMeans
clusters = KMeans(n_clusters=5).fit_predict(demo_arr)
```

## Evaluation signals

- Spectra annotated with the same chemical class (e.g., all flavonoids, all alkaloids) cluster tightly in reduced embedding space (high within-cluster cohesion).
- Spectra from different chemical families or structural classes separate into distinct clusters (high between-cluster separation).
- Cosine similarity values computed on the reduced embeddings correlate with ground-truth structural similarity or chemical relationship annotations (e.g., validated compound pairs show high similarity; non-related compounds show low similarity).
- Cluster assignments match known instrument types (Orbitrap vs. Q-TOF) or chemical subclasses at >70% agreement with reference labels.
- Dimensionality reduction plots show clear, visually interpretable separation of chemical families without excessive overlap or scattered outliers.

## Limitations

- Validation accuracy depends critically on the quality and completeness of ground-truth chemical annotations in the reference library; mislabeled or incomplete annotations will degrade coherence metrics.
- The number and type of clusters recovered are sensitive to hyperparameter choices (e.g., number of clusters k in k-means, eps in DBSCAN, perplexity in t-SNE); automatic selection of optimal k may be required.
- Dimensionality reduction (t-SNE, UMAP) introduces distortion and is stochastic; runs with different random seeds or parameter choices may yield qualitatively different visualizations, though cluster membership should be stable.
- The skill requires sufficient spectral diversity in the input dataset; sparse or heavily imbalanced chemical classes may result in weak or uninformative clustering patterns.

## Evidence

- [readme] The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering.: "The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering."
- [other] 1. Load pre-trained MSBERT embedding vectors from the model checkpoint. 2. Apply dimensionality reduction (t-SNE or UMAP) to project high-dimensional embeddings into 2D or 3D space for visualization. 3. Compute pairwise structural similarity between mass spectra using cosine similarity on the reduced embeddings. 4. Perform spectral clustering (e.g., k-means or hierarchical clustering) on the embedding vectors to group chemically similar spectra. 5. Validate cluster coherence by comparing clusters against known chemical classifications or structural families in the GNPS dataset.: "Apply dimensionality reduction (t-SNE or UMAP) to project high-dimensional embeddings into 2D or 3D space for visualization. Compute pairwise structural similarity between mass spectra using cosine"
- [readme] MSBERT was trained and tested on GNPS dataset.: "MSBERT was trained and tested on GNPS dataset."
- [other] Generate visualization plots showing clustered spectra in reduced embedding space with chemical labels or similarity heatmaps.: "Generate visualization plots showing clustered spectra in reduced embedding space with chemical labels or similarity heatmaps."
