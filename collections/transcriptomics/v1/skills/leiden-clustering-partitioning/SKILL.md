---
name: leiden-clustering-partitioning
description: Use when apply Leiden clustering after constructing a k-nearest neighbor (kNN) graph from single-cell expression data when you need to partition cells into discrete, biologically meaningful clusters for downstream trajectory inference, differential expression testing, or graph abstraction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0092
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

# Leiden clustering partitioning

## Summary

Leiden clustering partitions cells in a neighborhood graph into discrete clusters using modularity optimization, enabling downstream abstraction and trajectory inference on single-cell gene expression data. This skill is essential for identifying cell types and populations before constructing coarse-grained representations like PAGA graphs.

## When to use

Apply Leiden clustering after constructing a k-nearest neighbor (kNN) graph from single-cell expression data when you need to partition cells into discrete, biologically meaningful clusters for downstream trajectory inference, differential expression testing, or graph abstraction. Use it when the input is an annotated data matrix (AnnData object) with a computed neighborhood graph (stored in adata.obsp['distances'] or adata.obsp['connectivities']) and you require cluster assignments that will serve as nodes in subsequent partition-based abstractions.

## When NOT to use

- Input does not yet have a k-nearest neighbor graph computed; first run sc.pp.neighbors()
- Cells are already assigned to biologically validated, non-overlapping clusters from external annotation; Leiden would redundantly repartition them
- Goal is unsupervised dimensionality reduction only (not clustering); use UMAP or t-SNE instead

## Inputs

- AnnData object with preprocessed gene expression matrix (X)
- Precomputed k-nearest neighbor graph (adata.obsp['distances'] or adata.obsp['connectivities'])
- PCA representation (adata.obsm['X_pca']) used to construct the kNN graph

## Outputs

- Cluster assignments (adata.obs['leiden'])
- Updated AnnData object with leiden key in obs
- Cluster-level metadata for downstream abstraction

## How to apply

Run Leiden clustering via `sc.tl.leiden()` on an AnnData object that already contains a precomputed k-nearest neighbor graph (obtained from `sc.pp.neighbors()` with default parameters: n_neighbors=15, use_rep='X_pca'). The algorithm optimizes modularity across the graph to partition cells into clusters. Key parameters include `resolution` (controls granularity; higher values yield more clusters) and `random_state` (for reproducibility). The resulting cluster assignments are stored in `adata.obs['leiden']` and serve as the partition for downstream methods like PAGA. Verify clustering quality by confirming the cluster assignments are present in the obs DataFrame and that the number of clusters is biologically interpretable for your dataset.

## Related tools

- **Scanpy** (Provides the sc.tl.leiden() function for clustering and sc.pp.neighbors() for kNN graph construction) — https://github.com/scverse/scanpy
- **anndata** (Stores the AnnData object structure (obs, obsp, obsm) needed to hold cluster assignments and neighborhood graphs) — https://github.com/scverse/anndata
- **Python** (Execution language for Scanpy workflows)

## Examples

```
import scanpy as sc
adata = sc.datasets.paul15()
sc.pp.neighbors(adata, n_neighbors=15, use_rep='X_pca')
sc.tl.leiden(adata, resolution=1.0, random_state=42)
print(adata.obs['leiden'].value_counts())
```

## Evaluation signals

- Cluster assignments exist in adata.obs['leiden'] with no missing values
- Number of unique clusters is > 1 and biologically plausible (typically 3–20+ for diverse tissues)
- Cluster cardinality distribution is reasonable (no single cluster dominates; no singleton clusters unless expected)
- Downstream partition-based graph abstraction (PAGA) produces a connectivities matrix with dimensions n_clusters × n_clusters matching the number of unique leiden assignments
- Cluster-level gene expression profiles (via sc.tl.rank_genes_groups or similar) show enrichment for cell-type-specific markers

## Limitations

- Leiden clustering result is stochastic unless random_state is fixed; results may vary between runs on the same data
- Clustering quality depends critically on kNN graph quality (n_neighbors=15 may be suboptimal for very large or sparse datasets)
- The resolution parameter requires manual tuning; no automatic method to determine optimal granularity is provided in Scanpy
- Leiden partitions based solely on connectivity structure; it does not directly incorporate biological metadata or gene-level information, potentially missing known cell-type boundaries

## Evidence

- [other] Run Leiden clustering via sc.tl.leiden to partition cells into clusters.: "Run Leiden clustering via sc.tl.leiden to partition cells into clusters."
- [other] Compute k-nearest neighbors graph using sc.pp.neighbors with default parameters (n_neighbors=15, use_rep='X_pca').: "Compute k-nearest neighbors graph using sc.pp.neighbors with default parameters (n_neighbors=15, use_rep='X_pca')."
- [other] Scanpy is a scalable toolkit for analyzing single-cell gene expression data that includes trajectory inference capabilities, which encompasses methods like PAGA for constructing partition-based graph abstractions from clustered data.: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data that includes trajectory inference capabilities, which encompasses methods like PAGA for constructing partition-based graph"
- [intro] It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
- [other] nodes represent clusters: "nodes represent clusters"
