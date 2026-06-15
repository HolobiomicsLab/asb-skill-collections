---
name: scanpy-preprocessing-pipeline-execution
description: Use when you have raw or minimally processed single-cell RNA-seq expression data loaded into an AnnData object (dense, sparse, or Dask-backed array as X), and you need to apply standardized preprocessing transformations (normalization, filtering, PCA) before downstream analysis such as clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0769
  tools:
  - Scanpy
  - Python
  - anndata
  - Dask
  - pytest
  - Hatch
  - scipy.sparse
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata
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

# scanpy-preprocessing-pipeline-execution

## Summary

Execute preprocessing workflows on single-cell gene expression data using Scanpy's pp module, including normalization, quality control, and dimensionality reduction on AnnData objects. This skill enables lazy evaluation on Dask-backed expression matrices to avoid eagerly loading entire datasets into memory.

## When to use

You have raw or minimally processed single-cell RNA-seq expression data loaded into an AnnData object (dense, sparse, or Dask-backed array as X), and you need to apply standardized preprocessing transformations (normalization, filtering, PCA) before downstream analysis such as clustering or trajectory inference. Use this skill especially when working with large datasets where memory constraints require avoiding full materialization of the expression matrix.

## When NOT to use

- Input data is already a precomputed feature table or distance matrix (use trajectory inference or clustering directly instead)
- Expression matrix is already normalized and filtered (use dimensionality reduction or visualization directly)
- Data requires domain-specific preprocessing not provided by Scanpy pp (e.g., batch correction, alignment with external reference)

## Inputs

- AnnData object with expression matrix X (numpy array, scipy.sparse matrix, or dask.array.Array)
- Optional: gene annotation DataFrame (.var)
- Optional: cell metadata DataFrame (.obs)

## Outputs

- AnnData object with normalized/filtered expression data and updated metadata
- Updated .obs DataFrame with QC metrics (e.g., n_counts, n_genes)
- Updated .var DataFrame with gene-level statistics (e.g., highly_variable, means, dispersions)
- .obsm slot containing reduced-dimension embeddings (e.g., X_pca, X_umap)
- Dask array or sparse matrix in .X (lazy, not fully materialized)

## How to apply

Load or construct an AnnData object with the expression matrix in the .X attribute, which may be a numpy array, scipy sparse matrix, or dask.array.Array for lazy evaluation. Call appropriate pp module functions sequentially—for example, pp.normalize_total(adata, target_sum=1e4) to normalize library sizes, followed by pp.log1p(adata) for log transformation, then pp.highly_variable_genes(adata) to select genes, and finally pp.pca(adata, n_comps=50) for dimensionality reduction. Inspect the returned AnnData object to confirm that preprocessing completed without forcing the full matrix into memory: check that the .X attribute remains a dask.array.Array or sparse matrix (not eagerly materialized), verify that .obs and .var DataFrames retain expected structure and new columns (e.g., 'highly_variable', 'means', 'dispersions'), and confirm that dimensional reduction results appear in .obsm (e.g., .obsm['X_pca']). Use pytest to validate that memory consumption stays bounded and that intermediate Dask computations remain lazy.

## Related tools

- **Scanpy** (Core library providing pp module functions for preprocessing single-cell expression data) — https://github.com/scverse/scanpy
- **anndata** (Data structure (AnnData) for storing and manipulating annotated single-cell data with expression matrix and metadata) — https://github.com/scverse/anndata
- **Dask** (Lazy array backend for out-of-core preprocessing on large expression matrices without eager loading)
- **pytest** (Testing framework to validate preprocessing pipeline correctness and memory efficiency)
- **Hatch** (Development environment manager for running preprocessing tests and validation workflows)
- **scipy.sparse** (Sparse matrix support for efficient storage and computation on high-dimensional, sparse expression data)

## Examples

```
import scanpy as sc; adata = sc.read_h5ad('data.h5ad'); sc.pp.normalize_total(adata, target_sum=1e4); sc.pp.log1p(adata); sc.pp.highly_variable_genes(adata); sc.pp.pca(adata, n_comps=50); print(adata.X, adata.obs, adata.obsm['X_pca'])
```

## Evaluation signals

- Returned AnnData object .X remains a dask.array.Array or sparse matrix (not eagerly materialized into a dense numpy array)
- .obs and .var DataFrames retain original dimensions and structure, with new QC columns added (e.g., 'n_counts', 'n_genes', 'highly_variable', 'means', 'dispersions')
- .obsm slot contains expected reduced-dimension embeddings with correct shape (e.g., X_pca shape is [n_obs, n_comps])
- Memory usage during preprocessing remains proportional to metadata size, not full matrix size, confirming lazy evaluation
- Preprocessing functions complete without raising exceptions related to matrix format incompatibility or dimension mismatch

## Limitations

- Some pp functions may not support Dask-backed arrays and will force materialization; verify compatibility in Scanpy documentation for each function
- Sparse matrix operations may be slower than dense arrays in some preprocessing steps due to algorithmic constraints
- Preprocessing assumes data is organized as cells-in-rows, genes-in-columns; transposed matrices will produce incorrect results
- Large-scale Dask operations may still exhaust memory if downstream operations trigger full matrix materialization (e.g., certain clustering or visualization routines)

## Evidence

- [other] Can preprocessing functions in the scanpy pp module operate on Dask-backed AnnData objects without eagerly loading the entire expression matrix into memory?: "Can preprocessing functions in the scanpy pp module operate on Dask-backed AnnData objects without eagerly loading the entire expression matrix into memory?"
- [intro] Scanpy includes preprocessing, visualization, clustering, trajectory inference and differential expression testing capabilities: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
- [other] Load or construct an AnnData object with Dask-backed expression matrix (X as dask.array.Array). Call a pp module function (e.g., pp.normalize_total with appropriate parameters such as target_sum or pp.pca with n_comps) on the Dask-backed AnnData.: "Load or construct an AnnData object with Dask-backed expression matrix (X as dask.array.Array). Call a pp module function (e.g., pp.normalize_total with appropriate parameters such as target_sum or"
- [other] Verify operation completion without forcing full matrix into memory by inspecting the returned AnnData object. Check that obs and var DataFrames retain expected structure and dimensions. Confirm Dask array or sparse matrix output remains lazy or partially materialized as appropriate.: "Verify operation completion without forcing full matrix into memory by inspecting the returned AnnData object. Check that obs and var DataFrames retain expected structure and dimensions. Confirm Dask"
- [intro] Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata"
- [other] We use pytest to test scanpy. To run the tests, simply run `hatch test`: "We use pytest to test scanpy. To run the tests, simply run `hatch test`"
