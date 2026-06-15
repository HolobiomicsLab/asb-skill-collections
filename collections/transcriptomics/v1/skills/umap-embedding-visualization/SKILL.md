---
name: umap-embedding-visualization
description: Use when after completing PCA and k-nearest neighbor graph construction on preprocessed, log-normalized, highly-variable-gene-filtered single-cell RNA-seq data (stored in an AnnData object), compute UMAP embeddings when you need a 2-D visualization for cluster inspection, cell-type annotation, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3573
  tools:
  - Python
  - Scanpy
  - anndata
  - matplotlib
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- Single-Cell Analysis in Python
- type annotations on function parameters
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scanpy
    doi: 10.1186/s13059-017-1382-0
    title: scanpy
  dedup_kept_from: coll_scanpy
schema_version: 0.2.0
---

# umap-embedding-visualization

## Summary

Compute and visualize a 2-D UMAP embedding of single-cell transcriptomic data after preprocessing and dimensionality reduction (PCA and k-NN graph construction). UMAP provides an interpretable, low-dimensional representation suitable for identifying and visualizing cell clusters in large-scale datasets.

## When to use

After completing PCA and k-nearest neighbor graph construction on preprocessed, log-normalized, highly-variable-gene-filtered single-cell RNA-seq data (stored in an AnnData object), compute UMAP embeddings when you need a 2-D visualization for cluster inspection, cell-type annotation, or publication-ready plots of single-cell heterogeneity.

## When NOT to use

- Input data has not been preprocessed (normalized, log-transformed, highly-variable-gene-filtered) or does not contain a precomputed k-NN graph — run pp.normalize_total, pp.log1p, pp.highly_variable_genes, pp.scale, pp.pca, and pp.neighbors first.
- Dataset is very small (< 100 cells) or very sparse; UMAP may produce unstable or uninformative layouts.
- You need a quantitative distance metric for downstream analysis (e.g., trajectory inference, differential expression testing); UMAP is a visualization tool, not a distance metric. Use PCA coordinates or graph-based metrics instead.

## Inputs

- AnnData object with preprocessed, log-normalized, scaled gene expression matrix (adata.X)
- Precomputed k-nearest neighbor graph (adata.obsp['distances'] and adata.obsp['connectivities'])
- Leiden or other cluster assignments in adata.obs (for coloring visualization, optional)

## Outputs

- 2-D UMAP embedding coordinates stored in adata.obsm['X_umap'] (n_obs × 2 array)
- AnnData object with updated obsm dictionary
- Visualization plots (scatter plots colored by cluster label, gene expression, or metadata)

## How to apply

Call tl.umap() on an AnnData object that already contains a precomputed k-nearest neighbor graph (from pp.neighbors, typically with n_neighbors=15 by default). UMAP reduces the k-NN graph to 2 dimensions using a force-directed layout algorithm optimized for preserving both local and global neighborhood structure. The resulting 2-D coordinates are stored in the obsm['X_umap'] slot of the AnnData object. No hyperparameter tuning is required for the basic workflow; default parameters are suitable for standard datasets like PBMC3k. Verify successful execution by checking that obsm contains the 'X_umap' key and that the coordinate array matches the number of cells (observations) in the dataset.

## Related tools

- **Scanpy** (Core single-cell toolkit providing tl.umap() function and AnnData object container) — https://github.com/scverse/scanpy
- **anndata** (Data structure (AnnData) for storing gene expression matrices, embeddings (obsm), and metadata) — https://github.com/scverse/anndata
- **Python** (Programming environment for executing Scanpy tl.umap() and visualization code)
- **matplotlib** (Plotting library used by Scanpy for rendering scatter plots of UMAP coordinates)

## Examples

```
import scanpy as sc
adata = sc.datasets.pbmc3k()
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata)
sc.pp.scale(adata)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
sc.pl.umap(adata, color='leiden')
```

## Evaluation signals

- obsm dictionary of AnnData object contains 'X_umap' key after tl.umap() execution
- X_umap array has shape (n_obs, 2) matching the number of cells in the dataset
- X_umap coordinates are numeric (float64), finite (no NaN or Inf values), and occupy a reasonable range (typically [-20, 20] or similar)
- UMAP scatter plot visualization shows distinct, separated clusters when colored by known cell-type labels (Leiden clusters, cell annotation, or ground truth)
- No warning or error messages are raised during tl.umap() execution; successful completion is silent

## Limitations

- UMAP is a stochastic algorithm; results vary slightly between runs due to random initialization. Use set_random_state parameter if reproducibility across runs is critical.
- UMAP layout is not invariant to the choice of k-NN parameters (n_neighbors). Small k values emphasize local structure; large k values emphasize global structure. Default k=15 is a heuristic suitable for typical datasets but may require adjustment for very large or very small datasets.
- UMAP is a visualization tool optimized for interpretability; it does not preserve distances or density in the high-dimensional space. Do not use UMAP coordinates for quantitative downstream analysis (e.g., distance-based clustering, trajectory inference). Use PCA or graph-based metrics for such purposes.
- Performance degrades on very large datasets (> 1 million cells); consider subsampling or using approximate nearest-neighbor methods for computational efficiency.

## Evidence

- [other] Compute 2-D UMAP embedding using tl.umap for visualization.: "Compute 2-D UMAP embedding using tl.umap for visualization"
- [other] Verify that the output AnnData object contains 'leiden' cluster labels in obs and 'X_umap' coordinates in obsm.: "Verify that the output AnnData object contains 'leiden' cluster labels in obs and 'X_umap' coordinates in obsm"
- [intro] Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata.: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata"
- [intro] It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing.: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
- [other] Compute k-nearest neighbor graph using pp.neighbors with default parameters (n_neighbors=15).: "Compute k-nearest neighbor graph using pp.neighbors with default parameters (n_neighbors=15)"
