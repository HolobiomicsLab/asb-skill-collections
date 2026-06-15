---
name: anndata-object-manipulation
description: Use when you have single-cell RNA-seq count matrices or processed expression data and need to store them alongside cluster assignments (e.g., leiden cluster labels), cell metadata, and computed analysis results (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3308
  tools:
  - anndata
  - Python
  - Scanpy
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- built jointly with anndata
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

# anndata-object-manipulation

## Summary

Construct and manipulate annotated data matrices (AnnData objects) to store single-cell gene expression data alongside cluster assignments, metadata, and analysis results. This skill enables flexible storage and retrieval of intermediate and final results across preprocessing, clustering, and differential expression workflows.

## When to use

You have single-cell RNA-seq count matrices or processed expression data and need to store them alongside cluster assignments (e.g., leiden cluster labels), cell metadata, and computed analysis results (e.g., differential expression rankings, neighborhood graphs, trajectory abstractions) in a unified, versioned object. Use this skill when transitioning between workflow steps (e.g., after leiden clustering, before rank_genes_groups, after paga computation) or when you need to verify that intermediate results (cluster assignments, connectivity matrices) have been correctly stored and can be retrieved.

## When NOT to use

- Input is already a flattened result table (e.g., CSV of marker genes per cluster); use anndata only if you need to preserve the full expression matrix and metadata alongside the results.
- You are working with bulk RNA-seq or non-single-cell data where per-cell resolution is not required; anndata is optimized for single-cell sparsity and cell-level metadata.
- Cluster assignments or differential expression results are not yet computed; first run clustering (sc.tl.leiden) or differential expression (sc.tl.rank_genes_groups) before storing them in .obs or .uns.

## Inputs

- Single-cell expression matrix (dense or sparse, e.g., counts or log-normalized data)
- Cell-level metadata (e.g., batch, cell type, sample ID)
- Gene annotations (e.g., gene names, Ensembl IDs)
- Cluster assignments (e.g., leiden, louvain, or manual labels)
- Precomputed neighborhood graphs or connectivity matrices (optional)

## Outputs

- AnnData object (.h5ad file or in-memory Python object) with expression data in .X
- Cell metadata stored in .obs (cluster assignments, cell type labels, batch info)
- Gene metadata stored in .var (gene names, IDs, QC metrics)
- Unstructured results in .uns (differential expression tables, PAGA connectivity matrix, nearest-neighbor graph)
- Dimension reduction embeddings in .obsm (PCA, UMAP, PAGA layout coordinates)

## How to apply

Load or initialize an AnnData object using the anndata library, which provides a standard format for storing high-dimensional single-cell data in `.X` (expression matrix), `.obs` (cell-level metadata), and `.var` (gene annotations). After clustering steps, verify cluster assignments are stored in `adata.obs` with the groupby key (e.g., `adata.obs['leiden']`). After computing differential expression or trajectory abstractions, confirm results are stored in `adata.uns` (unstructured data dictionary) with the expected key names (e.g., `adata.uns['rank_genes_groups']`, `adata.uns['paga']`) and that connectivity or ranking matrices have the correct dimensionality (clusters × clusters for PAGA, genes × samples for rank_genes_groups). Use `sc.get.rank_genes_groups_df()` or direct `.uns` access to extract and validate result tables before downstream use.

## Related tools

- **anndata** (Core library for constructing, storing, and manipulating AnnData objects that integrate expression matrices, metadata, and analysis results) — https://github.com/scverse/anndata
- **Scanpy** (Provides convenience functions (sc.get.rank_genes_groups_df, sc.tl.leiden, sc.tl.paga) that write results directly into AnnData .obs and .uns slots) — https://github.com/scverse/scanpy
- **Python** (Language in which AnnData objects are constructed and manipulated via dictionary-like access to .obs, .var, .uns, .obsm)

## Examples

```
import scanpy as sc; adata = sc.datasets.pbmc3k_processed(); sc.tl.leiden(adata, resolution=1.0); sc.tl.rank_genes_groups(adata, groupby='leiden', method='wilcoxon'); df = sc.get.rank_genes_groups_df(adata)
```

## Evaluation signals

- Verify that cluster assignments are present in adata.obs with the expected key name (e.g., adata.obs['leiden']) and have the correct number of unique values matching the number of clusters.
- Check that differential expression results are stored in adata.uns['rank_genes_groups'] and can be extracted as a DataFrame with correct shape (e.g., genes × clusters × metrics) using sc.get.rank_genes_groups_df(adata).
- Confirm that PAGA connectivity matrix exists in adata.uns['paga']['connectivities'] with dimensions n_clusters × n_clusters and non-zero entries corresponding to cluster adjacencies.
- Validate that expression matrix dimensions match: adata.n_obs equals the number of cells and adata.n_vars equals the number of genes.
- Ensure that any stored embeddings or graphs (e.g., PCA in .obsm, neighbors in .obsp) have been saved after their respective computation steps (sc.tl.pca, sc.pp.neighbors).

## Limitations

- AnnData objects store sparse matrices efficiently but dense matrices can consume significant memory; for large datasets (>100k cells), ensure sufficient RAM or use chunked I/O workflows.
- Unstructured results (.uns) lack schema validation; users must remember the exact key names (e.g., 'rank_genes_groups', 'paga') for retrieval and manual validation of dimensionality.
- When storing multiple versions of the same result (e.g., rank_genes_groups computed with different methods), users must manually manage key naming conventions or overwrite previous results.
- AnnData serialization to .h5ad format is tied to the installed anndata version; older versions may not read files created by newer versions without compatibility issues.

## Evidence

- [intro] Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata"
- [other] Extract the result DataFrame using sc.get.rank_genes_groups_df(adata) or access adata.uns['rank_genes_groups']: "Extract the result DataFrame using sc.get.rank_genes_groups_df(adata) or access adata.uns['rank_genes_groups']"
- [other] Verify that adata.uns['paga'] exists and contains a 'connectivities' matrix with dimensions matching n_clusters × n_clusters: "Verify that adata.uns['paga'] exists and contains a 'connectivities' matrix with dimensions matching n_clusters × n_clusters"
- [other] Verify that leiden cluster assignments are present in adata.obs: "Verify that leiden cluster assignments are present in adata.obs"
