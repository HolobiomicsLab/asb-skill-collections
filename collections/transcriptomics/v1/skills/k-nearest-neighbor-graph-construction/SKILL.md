---
name: k-nearest-neighbor-graph-construction
description: Use when after PCA dimensionality reduction and scaling of normalized, log-transformed gene expression data, when you need to identify local cell neighborhoods (typically with k=15 neighbors) before applying clustering algorithms like Leiden or computing UMAP embeddings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
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

# k-nearest-neighbor-graph-construction

## Summary

Construct a k-nearest neighbor (kNN) graph from preprocessed single-cell gene expression data to capture local neighborhood structure in the principal component space. This graph serves as the foundation for downstream clustering, trajectory inference, and visualization tasks in single-cell analysis.

## When to use

After PCA dimensionality reduction and scaling of normalized, log-transformed gene expression data, when you need to identify local cell neighborhoods (typically with k=15 neighbors) before applying clustering algorithms like Leiden or computing UMAP embeddings. Use this skill when your input is an AnnData object with computed PCA coordinates and you require a graph-based representation of cell similarities.

## When NOT to use

- Input data has not been normalized for sequencing depth (pp.normalize_total must precede this step)
- PCA has not been computed; kNN construction requires dimensionality-reduced coordinates as input
- You are working with pre-computed distances or similarity matrices that should be provided directly rather than recomputed

## Inputs

- AnnData object with computed PCA (X_pca in obsm)
- Normalized and log-transformed gene expression matrix (X in AnnData)
- Scaled gene expression data

## Outputs

- AnnData object with kNN graph stored in obsp['distances']
- AnnData object with connectivity matrix stored in obsp['connectivities']
- Neighborhood information used by downstream clustering and embedding methods

## How to apply

Apply `pp.neighbors()` to the AnnData object after PCA computation, using the default k=15 parameter to identify each cell's 15 nearest neighbors in PCA space (or adjust k based on dataset size and biological question). The function computes distances between cells in the dimensionality-reduced space and stores both the distance matrix and the kNN graph structure in the AnnData object's `obsp` attribute. The resulting graph captures local manifold structure and is essential for subsequent Leiden clustering and UMAP computation, which both rely on this neighborhood information. Verify successful computation by checking that the AnnData object contains 'distances' and 'connectivities' matrices in `obsp` after execution.

## Related tools

- **Scanpy** (Primary toolkit containing pp.neighbors() function for kNN graph construction) — https://github.com/scverse/scanpy
- **anndata** (Data structure (AnnData) that stores the kNN graph in obsm and obsp attributes) — https://github.com/scverse/anndata
- **Python** (Programming language in which Scanpy is implemented)

## Examples

```
import scanpy as sc; adata = sc.datasets.pbmc3k(); sc.pp.normalize_total(adata); sc.pp.log1p(adata); sc.pp.pca(adata); sc.pp.neighbors(adata, n_neighbors=15)
```

## Evaluation signals

- AnnData object contains 'distances' key in obsp after pp.neighbors() execution
- AnnData object contains 'connectivities' key in obsp with sparse matrix representation
- Downstream Leiden clustering (tl.leiden) executes without error, indicating valid graph structure
- UMAP embedding (tl.umap) completes successfully using the constructed kNN graph
- Graph contains expected number of edges (approximately k × n_cells for undirected representation)

## Limitations

- Graph construction uses Euclidean distance in PCA space; results are sensitive to the number of PCs retained and may not capture all biological variation if PCA is under-dimensioned
- Default k=15 may be suboptimal for very small datasets (< 100 cells) or very large datasets (> 100,000 cells) where k should be scaled appropriately
- kNN graphs are local approximations and may miss global structure; trajectory inference and broader topology exploration require additional methods like PAGA
- Distance computation is performed in the PCA-reduced space only; gene-level similarity structure is lost after dimensionality reduction

## Evidence

- [other] Compute k-nearest neighbor graph using pp.neighbors with default parameters (n_neighbors=15): "Compute k-nearest neighbor graph using pp.neighbors with default parameters (n_neighbors=15)"
- [other] Verify that the output AnnData object contains 'leiden' cluster labels in obs and 'X_umap' coordinates in obsm: "Verify that the output AnnData object contains 'leiden' cluster labels in obs and 'X_umap' coordinates in obsm"
- [intro] It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
- [readme] The core of SPRING is to create a k-nearest neighbor (kNN) graph of data points and visualize the graph in 2D using a force-directed layout: "The core of SPRING is to create a k-nearest neighbor (kNN) graph of data points and visualize the graph in 2D using a force-directed layout"
