---
name: paga-graph-abstraction
description: Use when you have clustered single-cell RNA-seq data (via Leiden, Louvain, or equivalent) and a k-nearest neighbor graph computed in PCA space, and you want to abstract cell-level connectivity into cluster-level connectivity to infer developmental trajectories, lineage relationships, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3308
  tools:
  - Python
  - Scanpy
  - anndata
  - PAGA
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

# paga-graph-abstraction

## Summary

PAGA (Partition-based Graph Abstraction) constructs a coarse-grained connectivity matrix from clustered single-cell data by abstracting the neighborhood graph into a graph where nodes represent cell clusters and edges encode partition-based connectivity. Use this skill to infer high-level trajectory structure and developmental relationships from clustered scRNA-seq data.

## When to use

You have clustered single-cell RNA-seq data (via Leiden, Louvain, or equivalent) and a k-nearest neighbor graph computed in PCA space, and you want to abstract cell-level connectivity into cluster-level connectivity to infer developmental trajectories, lineage relationships, or coarse-grained manifold structure without trajectory inference on individual cells.

## When NOT to use

- Your clusters are biologically meaningless or only partially overlapping with true cell states; PAGA assumes clusters represent coherent biological entities.
- You are analyzing time-series or perturbation data where directionality matters; PAGA produces undirected graphs unless you apply directional post-hoc methods.
- Your data has very few clusters (< 3) or extreme imbalance in cluster sizes; the abstraction may not capture meaningful inter-cluster structure.

## Inputs

- anndata.AnnData object with preprocessed log-transformed gene expression (adata.X)
- PCA representation (adata.obsm['X_pca'])
- k-nearest neighbors graph (adata.obsp['distances'] and adata.obsp['connectivities'])
- cluster labels (adata.obs['leiden'] or equivalent categorical column)

## Outputs

- adata.uns['paga']['connectivities']: sparse n_clusters × n_clusters connectivity matrix
- adata.uns['paga']['transitions_confidence']: edge weights quantifying cluster connectivity strength
- adata.obsm['X_paga']: cluster-level coordinates for visualization

## How to apply

After computing a k-nearest neighbors graph (sc.pp.neighbors with n_neighbors=15 and use_rep='X_pca' by default) and partitioning cells into clusters using Leiden clustering (sc.tl.leiden), execute sc.tl.paga on the annotated data object. The algorithm computes a connectivity matrix where each entry [i,j] quantifies the strength of connection between clusters i and j based on the proportion of edges in the k-NN graph that cross between those clusters. The resulting partition-based graph abstraction is stored in adata.uns['paga']['connectivities'], a sparse n_clusters × n_clusters matrix. Verify the output by confirming that connectivities dimensions match the number of clusters and that values reflect inter-cluster edge density.

## Related tools

- **Scanpy** (Scalable toolkit housing sc.tl.paga trajectory inference method and neighborhood graph computation (sc.pp.neighbors, sc.tl.leiden)) — https://github.com/scverse/scanpy
- **anndata** (Data structure (AnnData) that stores clustered single-cell data, k-NN graphs, and PAGA outputs) — https://github.com/scverse/anndata
- **PAGA** (Original partition-based graph abstraction algorithm; integrated into Scanpy as sc.tl.paga) — https://github.com/theislab/paga

## Examples

```
import scanpy as sc
adata = sc.datasets.paul15()
sc.pp.neighbors(adata, n_neighbors=15, use_rep='X_pca')
sc.tl.leiden(adata)
sc.tl.paga(adata)
print(adata.uns['paga']['connectivities'].shape)
```

## Evaluation signals

- adata.uns['paga'] dictionary exists and contains 'connectivities' and 'transitions_confidence' keys
- connectivities matrix has shape (n_clusters, n_clusters) matching the unique values in the cluster column
- connectivities matrix is sparse and non-negative; values typically in [0, 1] range reflecting edge density fractions
- Visualization of the PAGA graph (via sc.pl.paga) shows meaningful cluster-level topology consistent with known biology (e.g., branching lineages for hematopoiesis)
- Connectivity strength between biologically related clusters is substantially higher than between unrelated clusters; no spurious long-range edges

## Limitations

- PAGA abstraction quality depends critically on the input clustering; poor or over/under-clustered data produces uninformative partitions.
- The method is fundamentally undirected; it does not infer direction of differentiation without additional directional cues or time-series labels.
- PAGA loses cell-level resolution; subtle within-cluster heterogeneity or intermediate cells may be compressed in the cluster-level graph.
- Results are sensitive to k-nearest neighbor parameter (n_neighbors); the default k=15 may require tuning for datasets with different cell density or dimensionality.

## Evidence

- [other] How does PAGA compute connectivity: "PAGA (Partition-based Graph Abstraction) algorithm construct a connectivity matrix from clustered single-cell data, and what is the expected dimensionality of the resulting abstraction"
- [intro] Scanpy trajectory inference: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data that includes trajectory inference capabilities, which encompasses methods like PAGA"
- [other] Workflow for PAGA execution: "Compute k-nearest neighbors graph using sc.pp.neighbors with default parameters (n_neighbors=15, use_rep='X_pca'). 3. Run Leiden clustering via sc.tl.leiden to partition cells into clusters. 4."
- [other] PAGA output structure: "nodes represent clusters. 5. Verify that adata.uns['paga'] exists and contains a 'connectivities' matrix with dimensions matching n_clusters × n_clusters"
- [readme] PAGA availability in Scanpy: "PAGA is available within Scanpy through: [`tl.paga`] | [`pl.paga`] | [`pl.paga_path`] | [`pl.paga_compare`]"
