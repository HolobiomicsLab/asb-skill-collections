---
name: single-cell-graph-construction-neighborhood
description: Use when you have preprocessed single-cell RNA-seq data (normalized and dimensionality-reduced via PCA) and need to establish cell-to-cell connectivity for trajectory inference, clustering validation, or graph-based visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3957
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_2885
  tools:
  - Python
  - Scanpy
  - anndata
  - PAGA
  - SPRING
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

# single-cell-graph-construction-neighborhood

## Summary

Construct a k-nearest neighbor graph from single-cell gene expression data to represent cell-to-cell similarity in reduced dimensionality space. This graph serves as the foundation for downstream trajectory inference, clustering refinement, and manifold exploration in single-cell analysis.

## When to use

Apply this skill when you have preprocessed single-cell RNA-seq data (normalized and dimensionality-reduced via PCA) and need to establish cell-to-cell connectivity for trajectory inference, clustering validation, or graph-based visualization. Specifically required as a prerequisite step before running partition-based graph abstraction (PAGA) or other neighborhood-dependent algorithms.

## When NOT to use

- Input data has not been normalized and log-transformed; kNN on raw counts will conflate sequencing depth with biology.
- PCA or other dimensionality reduction has not been performed; using raw high-dimensional space is computationally prohibitive and noisy.
- The dataset contains strong batch effects not corrected prior to graph construction; neighborhood structure will be driven by technical variation rather than biology.

## Inputs

- AnnData object with normalized gene expression matrix and X_pca (PCA-reduced representation)
- Preprocessed single-cell RNA-seq count data

## Outputs

- adata.obsp['connectivities']: sparse matrix of kNN graph connectivity (n_cells × n_cells)
- adata.obsp['distances']: sparse matrix of Euclidean distances in PCA space (n_cells × n_cells)
- adata.uns['neighbors']: dictionary containing metadata (n_neighbors, params, distances_key)

## How to apply

Using Scanpy, compute a k-nearest neighbor (kNN) graph by calling `sc.pp.neighbors()` on the annotated data matrix with default parameters (n_neighbors=15, use_rep='X_pca'). This identifies the 15 nearest neighbors for each cell in PCA space and stores the connectivity and distance matrices in the .obsp and .obsm slots of the AnnData object. The choice of n_neighbors=15 balances local structure preservation with noise robustness; larger values smooth over finer topology while smaller values risk isolating rare cell types. Verify construction by checking that `adata.obsp['distances']` and `adata.obsp['connectivities']` exist and have shape (n_cells, n_cells).

## Related tools

- **Scanpy** (Primary toolkit; provides sc.pp.neighbors() function to compute k-nearest neighbor graph from PCA-reduced single-cell data) — https://github.com/scverse/scanpy
- **anndata** (Data container; stores the kNN graph matrices (connectivities, distances) in obsp slots of AnnData object) — https://github.com/scverse/anndata
- **PAGA** (Downstream consumer; partition-based graph abstraction method that requires kNN graph as input to infer coarse-grained trajectory structure) — https://github.com/theislab/paga
- **SPRING** (Alternative visualization tool; constructs k-nearest neighbor graph for force-directed layout and interactive 2D exploration of single-cell data) — https://github.com/AllonKleinLab/SPRING

## Examples

```
import scanpy as sc; adata = sc.datasets.paul15(); sc.pp.neighbors(adata, n_neighbors=15, use_rep='X_pca'); print(adata.obsp['connectivities'].shape)
```

## Evaluation signals

- Verify adata.obsp['connectivities'] and adata.obsp['distances'] exist and have shape (n_cells, n_cells), are sparse matrices, and contain no NaN or Inf values.
- Check that the kNN graph is symmetric or near-symmetric (connectivity matrix should reflect mutual neighborhood relationships); extreme asymmetry indicates data quality issues.
- Visualize the neighborhood graph via `sc.pl.umap()` on the nearest-neighbor graph; cells within tight clusters should exhibit strong local connectivity; isolated cells suggest potential artifacts.
- Confirm that adata.uns['neighbors'] contains recorded metadata (n_neighbors=15, use_rep='X_pca'); this allows reproducibility and upstream tracking.
- Run downstream PAGA abstraction (sc.tl.paga); successful convergence and interpretable cluster-level graph structure indicates kNN graph is appropriate for trajectory inference.

## Limitations

- Fixed n_neighbors=15 is a heuristic that may be suboptimal for very rare populations (< 15 cells) or highly imbalanced datasets; consider sensitivity analysis or adaptive k selection for heterogeneous cell type compositions.
- kNN graph construction in PCA space inherits limitations of linear dimensionality reduction; complex non-linear structures (e.g., sharp branching points in differentiation) may be smoothed or misrepresented.
- Euclidean distance in PCA space is sensitive to the number of PCs retained; insufficient PCs lose biological signal whereas excessive PCs retain noise. Default downstream use assumes prior selection of appropriate n_pcs.
- The method is deterministic and fully connected; no explicit handling of technical outliers or ambient RNA; such artifacts should be filtered before kNN construction.

## Evidence

- [other] Compute k-nearest neighbors graph using sc.pp.neighbors with default parameters (n_neighbors=15, use_rep='X_pca'): "Compute k-nearest neighbors graph using sc.pp.neighbors with default parameters (n_neighbors=15, use_rep='X_pca')"
- [intro] Scanpy is a scalable toolkit for analyzing single-cell gene expression data that includes trajectory inference capabilities: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data that includes trajectory inference capabilities"
- [intro] preprocessing, visualization, clustering, trajectory inference and differential expression testing: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
- [readme] a k-nearest neighbor (kNN) graph of data points and visualize the graph in 2D using a force-directed layout: "The core of SPRING is to create a k-nearest neighbor (kNN) graph of data points and visualize the graph in 2D using a force-directed layout"
- [other] abstracts the neighborhood graph into a coarse-grained graph where nodes represent clusters: "which abstracts the neighborhood graph into a coarse-grained graph where nodes represent clusters"
