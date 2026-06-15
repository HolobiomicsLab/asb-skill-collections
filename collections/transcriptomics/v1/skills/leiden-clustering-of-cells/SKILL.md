---
name: leiden-clustering-of-cells
description: Use when after constructing a kNN graph (via pp.neighbors) on preprocessed, scaled, and PCA-reduced single-cell expression data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
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

# leiden-clustering-of-cells

## Summary

Apply the Leiden community detection algorithm to a k-nearest neighbor (kNN) graph of single-cell transcriptomes to partition cells into discrete clusters without requiring a priori specification of cluster number. This scalable method is used after dimensionality reduction and neighbor graph construction to identify cell types or states in AnnData objects.

## When to use

After constructing a kNN graph (via pp.neighbors) on preprocessed, scaled, and PCA-reduced single-cell expression data. Use when you need to discover discrete cell populations in an AnnData object without specifying cluster count in advance, or when comparing against other clustering methods. Essential before visualization (e.g., UMAP) and differential expression testing.

## When NOT to use

- Input lacks a precomputed neighbors graph (run pp.neighbors first).
- Gene expression matrix is not scaled (pp.scale must be applied before neighbor construction).
- Data is already assigned to known cell types or clusters and you need only to validate or refine existing labels; use differential expression or annotation tools instead.

## Inputs

- AnnData object with .X containing normalized, log-transformed, scaled gene expression
- Precomputed k-nearest neighbor graph in .obsp['distances'] and .obsp['connectivities'] and metadata in .uns['neighbors']

## Outputs

- AnnData object with cluster assignments in .obs['leiden'] (categorical dtype)
- Leiden clustering metadata in .uns['leiden']

## How to apply

Call tl.leiden on an AnnData object that already contains a neighbors graph (stored in .obsp and .uns). The method partitions cells by optimizing modularity on the kNN graph using the Leiden algorithm, which is more efficient than Louvain for large datasets. Results are stored as categorical labels in obs['leiden']. The resolution parameter (default ~1.0) controls cluster granularity: higher values yield finer partitions. Run on the full feature space after scaling (pp.scale) to ensure that variance differences do not bias neighbor weights. Verify output by checking that obs['leiden'] contains unique cluster labels and that cluster size distribution is reasonable (typically 10–10,000 cells per cluster for typical single-cell datasets).

## Related tools

- **Scanpy** (Python library providing tl.leiden method for Leiden clustering on single-cell graphs) — https://github.com/scverse/scanpy
- **anndata** (Data structure (AnnData) storing expression matrix, neighbors graph, and cluster labels) — https://github.com/scverse/anndata
- **Python** (Programming language for executing Scanpy clustering workflow)

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
sc.tl.leiden(adata)
```

## Evaluation signals

- obs['leiden'] contains no NaN values and is of categorical dtype with ≥2 unique cluster identities.
- All cells are assigned to exactly one cluster; cluster sizes are >0 and distributed reasonably (no cluster contains <1% or >95% of cells unless biologically justified).
- Cluster markers (highly expressed genes per cluster) are distinct across clusters, verifiable by differential expression testing (tl.rank_genes_groups).
- UMAP or t-SNE visualization (tl.umap, tl.tsne) shows spatial separation of cluster assignments, with minimal overlap between clusters.
- .uns['leiden'] metadata contains the resolution parameter and algorithm version used.

## Limitations

- Leiden clustering does not specify cluster count a priori; resolution tuning is required to achieve desired granularity, and no single 'correct' resolution exists.
- Results depend strongly on the kNN graph construction (n_neighbors, metric, PCA dimensionality); poorly chosen neighbors will propagate to poor clusters.
- Method assumes that cell similarity is well-captured by Euclidean distance in PCA space; highly non-Euclidean or highly sparse data may require alternative distance metrics or preprocessing.
- Cluster labels are arbitrary strings; biological interpretation requires downstream annotation (e.g., differential expression, marker genes) and domain knowledge.

## Evidence

- [other] Leiden clustering performed on kNN graph: "Perform Leiden clustering using tl.leiden to identify cell clusters."
- [other] Cluster labels stored in AnnData obs: "Verify that the output AnnData object contains 'leiden' cluster labels in obs"
- [intro] Scanpy includes clustering capability: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
- [other] kNN graph prerequisite: "Compute k-nearest neighbor graph using pp.neighbors with default parameters (n_neighbors=15)."
- [other] Full workflow context: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata"
