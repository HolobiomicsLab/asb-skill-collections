---
name: memory-efficient-single-cell-computation
description: Use when your input is a single-cell gene expression matrix too large to fit in RAM, or you are working in a resource-constrained environment (e.g., shared compute cluster, laptop with limited memory). You have constructed or loaded an AnnData object with X as a dask.array.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  tools:
  - Python
  - Scanpy
  - anndata
  - Dask
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

# memory-efficient-single-cell-computation

## Summary

Apply lazy-evaluation preprocessing and analysis operations to Dask-backed AnnData objects to process large single-cell gene expression matrices without forcing the entire expression matrix into memory. This skill enables scalable workflows on systems with constrained RAM by leveraging distributed array semantics and deferred computation.

## When to use

Your input is a single-cell gene expression matrix too large to fit in RAM, or you are working in a resource-constrained environment (e.g., shared compute cluster, laptop with limited memory). You have constructed or loaded an AnnData object with X as a dask.array.Array or sparse matrix, and you need to apply preprocessing operations (normalization, PCA, filtering) without materializing the full matrix.

## When NOT to use

- Input is already a dense in-memory NumPy array or fully materialized matrix; eager computation is appropriate and memory-efficient lazy evaluation offers no benefit.
- Your downstream analysis requires repeated random access to arbitrary matrix elements; Dask is optimized for sequential/block-wise access, not scattered indexing.
- You are performing iterative algorithms (e.g., optimization loops) that would materialize the Dask graph on every iteration; consider eager computation or algorithmic restructuring instead.

## Inputs

- AnnData object with X as dask.array.Array or sparse matrix
- Target sum or normalization parameters (numeric)
- Number of principal components (integer)
- Observation and variable metadata (obs, var DataFrames)

## Outputs

- AnnData object with lazily-computed or partially-materialized expression matrix
- Updated obs DataFrame (cell-level metadata preserved)
- Updated var DataFrame (gene-level metadata preserved)
- Dask array or sparse matrix representation of transformed/normalized data

## How to apply

Construct an AnnData object with the expression matrix X as a dask.array.Array rather than a dense NumPy array. Call preprocessing functions from the scanpy.pp module (e.g., pp.normalize_total with target_sum parameter, pp.pca with n_comps) directly on the Dask-backed AnnData; these functions are designed to operate lazily or on-demand without forcing full materialization. After each operation, verify that the returned AnnData object retains its lazy structure by inspecting the type of the X attribute and confirming it remains a dask.array.Array or sparse matrix. Inspect the obs and var DataFrames to confirm they maintain expected structure and dimensions; these metadata operations are not memory-constrained. Only trigger eager evaluation (e.g., .compute() in Dask) when you explicitly need results for downstream analysis or visualization, not during preprocessing steps.

## Related tools

- **Scanpy** (Provides preprocessing (pp) module functions that operate on Dask-backed AnnData objects without eager materialization; includes normalization, PCA, and dimensionality reduction) — https://github.com/scverse/scanpy
- **anndata** (Data structure for storing single-cell expression matrices and metadata; natively supports Dask arrays as the X attribute for lazy evaluation) — https://github.com/scverse/anndata
- **Dask** (Provides distributed array (dask.array.Array) semantics for lazy, out-of-core array computation; enables chunk-wise operations without full materialization)
- **pytest** (Unit testing framework used to verify lazy evaluation behavior and confirm operations do not trigger unwanted eager computation) — https://github.com/scverse/scanpy
- **Hatch** (Development environment and test runner; used to validate preprocessing functions in isolated environments with controlled memory constraints) — https://github.com/scverse/scanpy

## Examples

```
import scanpy as sc; import dask.array as da; X = da.from_delayed(..., shape=(n_obs, n_vars), dtype=float); adata = sc.AnnData(X=X); sc.pp.normalize_total(adata, target_sum=1e4); sc.pp.pca(adata, n_comps=50); print(type(adata.X), adata.shape)
```

## Evaluation signals

- Verify that X remains a dask.array.Array or sparse matrix after each preprocessing operation (not converted to dense NumPy array); inspect type(adata.X) and confirm it is not np.ndarray.
- Monitor system memory usage during preprocessing; confirm that peak RAM consumption does not scale with full matrix size, only with chunk size and temporary intermediate arrays.
- Confirm that obs and var DataFrames match expected dimensions and structure before and after preprocessing; check adata.n_obs, adata.n_vars, and obs/var column presence.
- Run a lazy operation and inspect the Dask task graph without calling .compute(); confirm that the graph accumulates operations without forcing evaluation until explicitly requested.
- For validation workflows, selectively materialize a small subset of the matrix (e.g., .compute() on a single chunk or row) to spot-check values; do not compute the entire matrix unless necessary.

## Limitations

- Not all Scanpy functions are optimized for Dask backends; some operations may still require eager computation or may fall back to loading the entire matrix into memory.
- Dask arrays are best suited for block-wise, sequential access patterns; operations requiring random access to scattered matrix elements or complex integer indexing may be slow or memory-inefficient.
- Metadata operations (obs, var DataFrames) must still fit in memory; memory efficiency applies only to the expression matrix X, not to annotation tables.
- Checkpoint and serialization of intermediate Dask graphs can become complex in long workflows; consider periodic explicit computation and re-serialization if workflow length is very large.

## Evidence

- [other] Can preprocessing functions in the scanpy pp module operate on Dask-backed AnnData objects without eagerly loading the entire expression matrix into memory?: "Can preprocessing functions in the scanpy pp module operate on Dask-backed AnnData objects without eagerly loading the entire expression matrix into memory?"
- [other] Load or construct an AnnData object with Dask-backed expression matrix (X as dask.array.Array). Call a pp module function (e.g., pp.normalize_total with appropriate parameters such as target_sum or pp.pca with n_comps) on the Dask-backed AnnData.: "Load or construct an AnnData object with Dask-backed expression matrix (X as dask.array.Array). Call a pp module function (e.g., pp.normalize_total with appropriate parameters such as target_sum or"
- [other] Verify operation completion without forcing full matrix into memory by inspecting the returned AnnData object. Check that obs and var DataFrames retain expected structure and dimensions.: "Verify operation completion without forcing full matrix into memory by inspecting the returned AnnData object. Check that obs and var DataFrames retain expected structure and dimensions."
- [intro] Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata"
- [intro] It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
