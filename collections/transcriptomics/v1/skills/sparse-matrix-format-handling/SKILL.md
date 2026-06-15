---
name: sparse-matrix-format-handling
description: Use when your input is an AnnData object with expression matrix X as a sparse scipy matrix or Dask-backed array, and you need to apply preprocessing functions (normalization, PCA, filtering) that could trigger eager materialization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3306
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_2640
  tools:
  - Python
  - Scanpy
  - anndata
  - Dask
  - scipy.sparse
  - pytest
  - Hatch
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

# sparse-matrix-format-handling

## Summary

Maintain sparse matrix representations (scipy.sparse or dask.array formats) throughout preprocessing and analysis workflows to avoid forcing large single-cell gene expression matrices into dense memory. This skill is essential for scaling Scanpy preprocessing functions to datasets that would otherwise exhaust RAM when fully materialized.

## When to use

Your input is an AnnData object with expression matrix X as a sparse scipy matrix or Dask-backed array, and you need to apply preprocessing functions (normalization, PCA, filtering) that could trigger eager materialization. Apply this skill when your dataset is large enough that dense representation would exceed available memory, or when you want to defer computation for lazy evaluation.

## When NOT to use

- Input is already a dense numpy array and memory is not a constraint—dense operations may be faster and simpler.
- Downstream analysis requires frequent random access or in-place modifications that sparse formats do not support efficiently.
- You are using third-party functions or older library versions that explicitly do not support sparse matrices or Dask arrays.

## Inputs

- AnnData object with X as scipy.sparse matrix (e.g., csr_matrix, csc_matrix)
- AnnData object with X as dask.array.Array backed by sparse or chunked data
- Gene expression count matrix (raw or log-normalized)
- Observation and variable metadata DataFrames (obs, var)

## Outputs

- AnnData object with sparse or lazy X representation preserved
- Preprocessed expression matrix in original sparse/Dask format
- Updated or new entries in .obsm (e.g., PCA coordinates) or .varm (e.g., loadings)
- Modified obs and var DataFrames with preprocessing metadata (e.g., n_counts, mean_counts)

## How to apply

Construct or load an AnnData object with X stored as scipy.sparse matrix or dask.array.Array rather than dense numpy array. When calling pp module functions (e.g., pp.normalize_total, pp.pca), verify that the function signature and implementation preserve sparsity or laziness—check the Scanpy source or documentation for lazy=True or out_type parameters. After function execution, inspect the returned AnnData.X to confirm it remains sparse or Dask-backed; do not force materialization via .toarray() or .compute() unless explicitly necessary for downstream steps. Monitor memory usage and task graph size to ensure computation remains deferred. For intermediate results requiring dense operations (e.g., certain linear algebra steps), consider materializing only the required subset (e.g., PC coordinates rather than the full matrix).

## Related tools

- **Scanpy** (Provides pp module preprocessing functions (normalize_total, pca, filter_genes, etc.) with sparse-aware implementations for operating on sparse or Dask-backed AnnData objects.) — https://github.com/scverse/scanpy
- **anndata** (Defines the AnnData data structure that encapsulates X as sparse or Dask array; handles lazy I/O and matrix format preservation across operations.) — https://github.com/scverse/anndata
- **Dask** (Provides lazy array abstraction (dask.array.Array) for chunked, out-of-core computation on large matrices without forcing full materialization.)
- **scipy.sparse** (Supplies sparse matrix formats (csr_matrix, csc_matrix, coo_matrix) used by Scanpy and anndata for memory-efficient storage of high-dimensional, low-density expression data.)
- **pytest** (Testing framework used to validate that preprocessing functions preserve sparsity and do not eagerly load matrices into memory.)
- **Hatch** (Provides development environments and test automation for verifying sparse matrix handling across Scanpy preprocessing functions.)

## Examples

```
import scanpy as sc; import dask.array as da; X_dask = da.from_delayed(delayed_load(), shape=(n_obs, n_vars), dtype=float); adata = sc.AnnData(X=X_dask, obs=obs_df, var=var_df); sc.pp.normalize_total(adata, target_sum=1e4); assert isinstance(adata.X, da.Array)
```

## Evaluation signals

- Returned AnnData.X remains a scipy.sparse matrix or dask.array.Array (inspect type(adata.X) and shape); not converted to dense numpy array.
- Memory usage does not spike proportionally to the full matrix size during preprocessing; confirm via task graph inspection (Dask) or sparse matrix nonzero counts.
- obs and var DataFrames retain expected structure and dimensions after preprocessing; verify via adata.obs.shape, adata.var.shape, and column presence.
- Downstream operations (e.g., clustering, visualization) accept the sparse/lazy output without triggering forced materialization; confirm by inspecting function logs and memory profiles.
- For Dask-backed arrays, task graph grows additively with function calls rather than expanding exponentially; inspect via adata.X.__dask_graph__() or equivalent.

## Limitations

- Not all Scanpy pp functions support sparse input; check function signature and documentation (e.g., some smoothing or highly-coupled operations may require dense matrices).
- Dask computation is deferred, so errors or data shape mismatches may not surface until .compute() is called, complicating debugging.
- Certain analyses (e.g., highly-connected neighborhood graphs, dense matrix factorizations) may benefit little from sparsity and could be slower due to overhead.
- Mixing sparse and dense operations in a workflow can trigger implicit conversions, negating memory savings; requires careful pipeline design.

## Evidence

- [other] Can preprocessing functions in the scanpy pp module operate on Dask-backed AnnData objects without eagerly loading the entire expression matrix into memory?: "Can preprocessing functions in the scanpy pp module operate on Dask-backed AnnData objects without eagerly loading the entire expression matrix into memory?"
- [other] Load or construct an AnnData object with Dask-backed expression matrix (X as dask.array.Array). Call a pp module function (e.g., pp.normalize_total with appropriate parameters such as target_sum or pp.pca with n_comps) on the Dask-backed AnnData.: "Load or construct an AnnData object with Dask-backed expression matrix (X as dask.array.Array). Call a pp module function (e.g., pp.normalize_total with appropriate parameters such as target_sum or"
- [other] Verify operation completion without forcing full matrix into memory by inspecting the returned AnnData object. Check that obs and var DataFrames retain expected structure and dimensions. Confirm Dask array or sparse matrix output remains lazy or partially materialized as appropriate.: "Verify operation completion without forcing full matrix into memory by inspecting the returned AnnData object. Check that obs and var DataFrames retain expected structure and dimensions. Confirm Dask"
- [intro] Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata"
- [intro] It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
