---
name: dimensionality-reduction-via-pca
description: Use when apply PCA when you have a log-normalized, scaled gene expression matrix from highly variable genes and need to reduce dimensionality before constructing k-nearest neighbor graphs or other manifold-learning steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  tools:
  - Python
  - Scanpy
  - anndata
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

# Dimensionality reduction via PCA

## Summary

Principal component analysis (PCA) reduces the dimensionality of preprocessed single-cell gene expression matrices while preserving variance structure, enabling efficient downstream graph-based analysis and visualization. Applied after log-normalization and highly variable gene selection, PCA compresses scaled expression data into a lower-dimensional PC space suitable for neighbor graph construction and embedding.

## When to use

Apply PCA when you have a log-normalized, scaled gene expression matrix from highly variable genes and need to reduce dimensionality before constructing k-nearest neighbor graphs or other manifold-learning steps. Typical trigger: working with sparse single-cell data where full-rank gene space would be computationally expensive or noisy for downstream clustering and embedding.

## When NOT to use

- Input data has not been log-normalized and scaled; raw counts or non-normalized data will yield biased PC loadings.
- You require interpretability of individual gene contributions and cannot tolerate the loss of gene-space structure that PCA introduces.
- Dimensionality is already low (e.g., <100 genes remain after HVG selection) and PCA provides negligible computational benefit.

## Inputs

- AnnData object with scaled gene expression matrix (obs × highly_variable_genes)
- Preprocessed counts after normalize_total, log1p, and unit-variance scaling

## Outputs

- AnnData object with 'X_pca' embedding (obs × n_components)
- Variance explained per component (stored in varm or returned separately)

## How to apply

After preprocessing (normalize_total, log1p transformation, identification of highly variable genes via pp.highly_variable_genes, and unit-variance scaling via pp.scale), invoke pp.pca on the scaled AnnData object using default parameters. PCA decomposes the centered gene expression matrix into orthogonal principal components ranked by variance explained. The resulting reduced-rank representation (typically 10–50 components) captures the dominant variance structure and is stored in the 'X_pca' slot of the AnnData object, suitable for subsequent k-nearest neighbor graph construction (pp.neighbors) and graph-based clustering. Choose the number of components empirically: retain enough components to explain sufficient cumulative variance (often 80–90%) while avoiding overfitting to noise.

## Related tools

- **Scanpy** (Provides pp.pca function for principal component analysis on preprocessed single-cell gene expression matrices) — https://github.com/scverse/scanpy
- **anndata** (Data structure (AnnData) that stores PCA results in obsm slot ('X_pca')) — https://github.com/scverse/anndata
- **Python** (Programming language in which Scanpy and PCA workflow are implemented)

## Examples

```
import scanpy as sc; adata = sc.datasets.pbmc3k(); sc.pp.normalize_total(adata); sc.pp.log1p(adata); sc.pp.highly_variable_genes(adata); sc.pp.scale(adata); sc.pp.pca(adata)
```

## Evaluation signals

- AnnData object contains 'X_pca' key in obsm with shape (n_obs, n_components)
- Variance explained per component is monotonically decreasing and cumulative variance reaches ≥80% within chosen n_components
- Downstream pp.neighbors call on 'X_pca' completes successfully and produces consistent k-nearest neighbor graphs
- UMAP embedding computed from PCA space (tl.umap) shows distinct cluster separation matching biological cell types
- PC loadings reflect expected biology (e.g., PC1 correlates with known cell-cycle or cell-type markers)

## Limitations

- PCA is linear and may not capture complex nonlinear manifold structure; nonlinear methods (e.g., UMAP, t-SNE) should follow for visualization.
- Choice of n_components is empirical; too few components lose biological signal, too many retain noise and increase downstream computational cost.
- PCA assumes Gaussian-distributed data; highly skewed single-cell count distributions may benefit from additional variance-stabilizing transformations (e.g., log1p is applied beforehand).
- PCA is unsupervised and may emphasize technical variation (e.g., sequencing depth, batch effects) over biological signal if not adequately corrected in preprocessing.

## Evidence

- [other] Identity of PCA step in Scanpy pipeline: "Compute principal component analysis (PCA) using pp.pca with default parameters."
- [other] Position in workflow after scaling: "Scale gene expression to unit variance using pp.scale. 6. Compute principal component analysis (PCA)"
- [other] Output data structure: "Verify that the output AnnData object contains 'leiden' cluster labels in obs and 'X_umap' coordinates in obsm."
- [intro] Scanpy toolkit design: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata"
- [intro] Core workflow steps: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
