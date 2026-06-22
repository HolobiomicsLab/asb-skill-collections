---
name: embedding-space-rationality-validation
description: Use when after training a deep learning model (e.g. MSBERT) on mass spectra and obtaining embedding vectors, apply this skill to verify that the learned representations cluster chemically similar compounds together and that structural relationships are preserved in the embedding space.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3674
  tools:
  - Python
  - Anaconda
  - Git
  - t-SNE
  - UMAP
  - scikit-learn (k-means, hierarchical clustering)
  - PyTorch
  - MSBERT
  - GNPS dataset
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

# embedding-space-rationality-validation

## Summary

Validate that high-dimensional embedding vectors encode chemically meaningful structure through complementary visualization and clustering analyses. This skill demonstrates whether learned representations of mass spectra preserve chemical rationality by reducing dimensionality, computing structural similarity, and performing spectral clustering on the embedding space.

## When to use

After training a deep learning model (e.g. MSBERT) on mass spectra and obtaining embedding vectors, apply this skill to verify that the learned representations cluster chemically similar compounds together and that structural relationships are preserved in the embedding space. Use this when you need evidence that embeddings capture domain semantics rather than arbitrary patterns.

## When NOT to use

- Embeddings have not been trained or fine-tuned on domain-specific data — validation assumes learning has already occurred.
- Reference chemical classifications or ground truth labels are unavailable — cluster validation requires external chemical structure to compare against.
- Input data lacks chemical metadata (SMILES, known compound families, or structural descriptors) — without ground truth, coherence cannot be verified.

## Inputs

- Pre-trained embedding vectors (high-dimensional dense arrays from checkpoint)
- Mass spectra data (MSP or mzML format with chemical annotations or SMILES)
- Reference chemical classifications or structural families (from GNPS dataset or equivalent)

## Outputs

- 2D or 3D dimensionality-reduced embedding space visualization
- Pairwise structural similarity matrix (cosine similarity scores)
- Spectral clusters (cluster assignments for each spectrum)
- Cluster coherence validation report (agreement with chemical classifications)
- Visualization plots with chemical labels and similarity heatmaps

## How to apply

Load pre-trained embedding vectors and apply three complementary analyses: (1) Project high-dimensional embeddings to 2D or 3D using dimensionality reduction (t-SNE or UMAP) to visualize structure. (2) Compute pairwise cosine similarity between mass spectra in the reduced or original embedding space to quantify structural relationships. (3) Perform spectral clustering (k-means or hierarchical clustering) on embedding vectors to group chemically similar spectra, then validate cluster coherence against known chemical classifications or structural families in the reference dataset (e.g. GNPS). Generate visualization plots showing clustered spectra with chemical labels and similarity heatmaps to confirm that clusters align with chemical expectations.

## Related tools

- **t-SNE** (Dimensionality reduction for 2D/3D visualization of embedding vectors)
- **UMAP** (Dimensionality reduction for 2D/3D visualization of embedding vectors)
- **scikit-learn (k-means, hierarchical clustering)** (Spectral clustering of embedding vectors to group chemically similar spectra)
- **PyTorch** (Load and manipulate pre-trained embedding checkpoint tensors) — https://pytorch.org/
- **MSBERT** (Pre-trained transformer model that generates embedding vectors from mass spectra) — https://github.com/zhanghailiangcsu/MSBERT
- **GNPS dataset** (Reference chemical classifications and structural families for cluster coherence validation) — https://zenodo.org/records/13722644

## Examples

```
from model.MSBERTModel import MSBERT
from model.utils import ModelEmbed, ProcessMSP
import torch
model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
demo_data, demo_smiles = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
cos_sim = MSBERTSimilarity(demo_arr, demo_arr)
```

## Evaluation signals

- Clusters in reduced embedding space visually align with chemical structural families or known compound groupings from GNPS.
- Pairwise cosine similarity between spectra of the same chemical class is significantly higher than between different classes (quantifiable threshold e.g. within-class > 0.7, between-class < 0.5).
- Cluster coherence metrics (silhouette score, Davies-Bouldin index, or Calinski-Harabasz index) meet expected thresholds for well-separated, compact clusters.
- Chemical labels or structural annotations in visualization plots show no random mixing — compounds cluster by chemical family or functional group.
- Comparison of MSBERT embeddings against baseline methods (Spec2Vec, cosine similarity on raw spectra) shows superior cluster separation and higher library matching accuracy.

## Limitations

- Rationality validation is qualitative and depends on availability of chemical reference labels or ground truth classifications in the dataset.
- Dimensionality reduction (t-SNE, UMAP) introduces distortion; 2D/3D projections may not preserve all structure from the high-dimensional embedding space.
- Clustering quality is sensitive to hyperparameters (number of clusters k, linkage method, clustering algorithm); multiple runs with different seeds recommended.
- No changelog available to track changes in model or dataset versions that might affect validation results.
- Validation is limited to the chemical diversity present in the training/test dataset; generalization to out-of-domain compounds is not assessed.

## Evidence

- [intro] The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering.: "The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering."
- [other] Apply dimensionality reduction (t-SNE or UMAP) to project high-dimensional embeddings into 2D or 3D space for visualization. Compute pairwise structural similarity between mass spectra using cosine similarity on the reduced embeddings. Perform spectral clustering (e.g. k-means or hierarchical clustering) on the embedding vectors to group chemically similar spectra. Validate cluster coherence by comparing clusters against known chemical classifications or structural families in the GNPS dataset.: "Apply dimensionality reduction (t-SNE or UMAP) to project high-dimensional embeddings into 2D or 3D space for visualization. Compute pairwise structural similarity between mass spectra using cosine"
- [other] Load pre-trained MSBERT embedding vectors from the model checkpoint.: "Load pre-trained MSBERT embedding vectors from the model checkpoint."
- [other] Generate visualization plots showing clustered spectra in reduced embedding space with chemical labels or similarity heatmaps.: "Generate visualization plots showing clustered spectra in reduced embedding space with chemical labels or similarity heatmaps."
