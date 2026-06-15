---
name: dask-array-lazy-evaluation-verification
description: Use when when applying Scanpy preprocessing functions (e.g., pp.normalize_total, pp.pca) to AnnData objects where the expression matrix X is backed by a dask.array.Array, you need to verify that the operation completed without eagerly loading the full matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_3673
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

# dask-array-lazy-evaluation-verification

## Summary

Verify that preprocessing operations on Dask-backed AnnData objects maintain lazy evaluation and do not force the entire expression matrix into memory. This skill ensures memory-efficient processing of large single-cell RNA-seq datasets by confirming that the returned data structures preserve Dask arrays or sparse matrices in their lazy or partially materialized state.

## When to use

When applying Scanpy preprocessing functions (e.g., pp.normalize_total, pp.pca) to AnnData objects where the expression matrix X is backed by a dask.array.Array, you need to verify that the operation completed without eagerly loading the full matrix. This is critical when working with datasets too large to fit in RAM.

## When NOT to use

- The input expression matrix is already a dense NumPy array or has been pre-materialized; lazy evaluation is not applicable.
- The preprocessing function is known to require eager computation (e.g., functions that inherently need full matrix access); verify function documentation first.
- You need immediate numerical results; lazy evaluation defers computation and returns task graphs rather than final values.

## Inputs

- AnnData object with dask.array.Array as expression matrix (X)
- Preprocessing function call with appropriate parameters (target_sum, n_comps, etc.)

## Outputs

- AnnData object with Dask-backed or sparse expression matrix (not eagerly materialized)
- obs DataFrame with retained structure and dimensions
- var DataFrame with retained structure and dimensions
- Verification report indicating lazy evaluation was preserved

## How to apply

After calling a pp module function on a Dask-backed AnnData object, inspect the returned AnnData to confirm that (1) the expression matrix remains a Dask array or sparse matrix and has not been materialized into a dense NumPy array, (2) the obs and var DataFrames retain their expected structure and dimensions, and (3) the array chunks are still defined (e.g., via dask.array.Array.chunks). Check for materialization by examining the type of the X attribute and verifying it is not a dense ndarray. Use assertions or logging to confirm that intermediate computations were deferred rather than executed immediately.

## Related tools

- **Scanpy** (Provides preprocessing functions (pp module) that operate on AnnData objects; must be tested for Dask compatibility) — https://github.com/scverse/scanpy
- **anndata** (Data structure (AnnData) that can wrap Dask-backed expression matrices; essential for lazy evaluation support) — https://github.com/scverse/anndata
- **Dask** (Provides lazy array computation framework; expression matrices use dask.array.Array for deferred evaluation)
- **pytest** (Test framework used to verify preprocessing functions work correctly with Dask-backed inputs)
- **Hatch** (Build and test environment manager for running test suites)

## Examples

```
import anndata as ad; import dask.array as da; import scanpy as sc; X_dask = da.from_delayed(delayed_expr, shape=(n_obs, n_vars), dtype=float); adata = ad.AnnData(X=X_dask); adata_norm = sc.pp.normalize_total(adata, target_sum=1e6); assert isinstance(adata_norm.X, da.Array), 'Expression matrix was materialized'
```

## Evaluation signals

- Returned AnnData.X is a dask.array.Array or sparse matrix, not a dense NumPy ndarray
- dask.array.Array.chunks attribute is defined and non-empty, confirming task graph structure is intact
- AnnData.obs and AnnData.var DataFrames have the same dimensions and columns as before the operation
- No RuntimeWarning or explicit materialization call (e.g., .compute()) was issued during preprocessing
- Memory profiler or task graph inspection shows the operation did not load the full matrix into RAM

## Limitations

- Not all Scanpy preprocessing functions may support Dask-backed inputs; compatibility depends on the specific function implementation.
- Some operations inherently require full matrix access and will force materialization; these functions should document their eagerness.
- Verifying lazy evaluation requires introspection of object types and chunk metadata; indirect or implicit materialization may be missed by simple type checks.
- Performance gains from lazy evaluation are only realized when subsequent operations also defer computation; premature evaluation breaks the lazy chain.

## Evidence

- [other] Load or construct an AnnData object with Dask-backed expression matrix (X as dask.array.Array). Call a pp module function (e.g., pp.normalize_total with appropriate parameters such as target_sum or pp.pca with n_comps) on the Dask-backed AnnData.: "1. Load or construct an AnnData object with Dask-backed expression matrix (X as dask.array.Array). 2. Call a pp module function (e.g., pp.normalize_total with appropriate parameters such as"
- [other] Verify operation completion without forcing full matrix into memory by inspecting the returned AnnData object. Check that obs and var DataFrames retain expected structure and dimensions. Confirm Dask array or sparse matrix output remains lazy or partially materialized as appropriate.: "3. Verify operation completion without forcing full matrix into memory by inspecting the returned AnnData object. 4. Check that obs and var DataFrames retain expected structure and dimensions. 5."
- [other] Scanpy includes preprocessing capabilities as part of its toolkit for single-cell gene expression analysis, designed to work with the anndata data structure.: "Scanpy includes preprocessing capabilities as part of its toolkit for single-cell gene expression analysis, designed to work with the anndata data structure."
- [other] Can preprocessing functions in the scanpy pp module operate on Dask-backed AnnData objects without eagerly loading the entire expression matrix into memory?: "Can preprocessing functions in the scanpy pp module operate on Dask-backed AnnData objects without eagerly loading the entire expression matrix into memory?"
