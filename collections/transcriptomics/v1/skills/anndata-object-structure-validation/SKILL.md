---
name: anndata-object-structure-validation
description: Use when after applying Scanpy preprocessing functions (e.g., pp.normalize_total, pp.pca) to a Dask-backed AnnData object, or when performing any operation that could alter matrix dimensions, data types, or backing storage (dense, sparse, or lazy).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0654
  tools:
  - anndata
  - Python
  - Scanpy
  - pytest
  - Dask
  - Hatch
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

# anndata-object-structure-validation

## Summary

Validate that an AnnData object retains correct structure and dimensional integrity after preprocessing operations, particularly when using lazy evaluation with Dask-backed arrays. This skill ensures that obs and var DataFrames remain consistent with the expression matrix and that lazy or sparse materialization states are preserved as intended.

## When to use

After applying Scanpy preprocessing functions (e.g., pp.normalize_total, pp.pca) to a Dask-backed AnnData object, or when performing any operation that could alter matrix dimensions, data types, or backing storage (dense, sparse, or lazy). Validate before downstream analysis steps that depend on specific array formats or metadata consistency.

## When NOT to use

- Input is a raw expression matrix or numpy array without AnnData wrapper — use anndata.AnnData() constructor first.
- Validation is performed on in-memory, fully materialized arrays where memory constraints are not a concern and lazy evaluation is not required.
- The preprocessing function is known to intentionally reshape or subset the object and you are explicitly testing for those changes rather than structural consistency.

## Inputs

- AnnData object with potentially modified expression matrix (X)
- obs DataFrame (cell/observation metadata)
- var DataFrame (gene/variable metadata)
- Dask-backed or sparse-backed expression matrix
- Preprocessed layers or derived slots (obsm, varm)

## Outputs

- Validated AnnData object with confirmed structural integrity
- Boolean or assertion result indicating schema compliance
- Diagnostic report of shape, dtype, and materialization state
- Confirmation that obs/var dimensions match X dimensions

## How to apply

Inspect the returned AnnData object by (1) confirming that the obs (observations/cells) and var (variables/genes) DataFrames retain expected row and column counts and match the expression matrix dimensions; (2) verifying the dtype and shape of the main expression matrix X and any derived matrices (e.g., from PCA); (3) checking that Dask arrays remain lazily evaluated or that sparse matrices remain partially materialized rather than being eagerly loaded into memory; (4) examining layer metadata and obsm/varm slots if applicable to ensure no unexpected data loss or corruption; (5) running a minimal computation (e.g., triggering a small slice or computing summary statistics) to confirm the lazy array is functional without forcing full materialization. Use pytest or assertion-based checks to automate these verifications in test workflows.

## Related tools

- **anndata** (Provides the AnnData data structure and object validation methods; inspects obs/var/X consistency and metadata integrity) — https://github.com/scverse/anndata
- **Scanpy** (Supplies preprocessing functions (pp module) that operate on AnnData objects and may trigger structural changes requiring post-hoc validation) — https://github.com/scverse/scanpy
- **pytest** (Test framework for automating structural validation assertions and continuous validation in CI pipelines)
- **Dask** (Lazy array backend; validation must confirm that lazy evaluation is preserved or appropriately materialized)
- **Hatch** (Development environment manager used to run test suites that include validation checks)

## Examples

```
import anndata as ad
import dask.array as da
adata = ad.AnnData(X=da.from_delayed(...))
assert adata.X.shape[0] == adata.obs.shape[0], 'obs count mismatch'
assert adata.X.shape[1] == adata.var.shape[1], 'var count mismatch'
assert isinstance(adata.X, da.Array), 'X is not lazy'
```

## Evaluation signals

- obs and var DataFrames have row/column counts matching the first and second dimensions of X, respectively
- Dask-backed arrays remain as dask.array.Array after preprocessing, or sparse matrices remain scipy.sparse.csr_matrix, not eagerly converted to dense numpy arrays
- No rows or columns are dropped unintentionally; X.shape[0] == adata.obs.shape[0] and X.shape[1] == adata.var.shape[1]
- Derived matrices in obsm and varm slots have correct first dimension (matching obs) and maintain expected dtypes (e.g., float32 for PCA embeddings)
- A small lazy slice or summary computation (e.g., compute() on a subset or .mean(axis=0)) completes without memory errors, proving the lazy graph is valid

## Limitations

- Validation does not detect semantic errors in preprocessing logic (e.g., incorrect normalization factors), only structural consistency.
- Some Scanpy preprocessing functions may not yet support Dask arrays; validation cannot enforce lazy evaluation if the underlying function forces materialization.
- Large obs/var DataFrames may themselves consume memory if fully loaded for inspection; defer detailed validation to lazy summary statistics where possible.
- Sparse matrix format changes (e.g., csr to csc) during preprocessing are not caught by simple shape/dtype checks; inspect .format attribute explicitly if format preservation is critical.

## Evidence

- [other] Verify operation completion without forcing full matrix into memory by inspecting the returned AnnData object. 4. Check that obs and var DataFrames retain expected structure and dimensions. 5. Confirm Dask array or sparse matrix output remains lazy or partially materialized as appropriate.: "Verify operation completion without forcing full matrix into memory by inspecting the returned AnnData object. Check that obs and var DataFrames retain expected structure and dimensions. Confirm Dask"
- [other] Load or construct an AnnData object with Dask-backed expression matrix (X as dask.array.Array). 2. Call a pp module function (e.g., pp.normalize_total with appropriate parameters such as target_sum or pp.pca with n_comps) on the Dask-backed AnnData.: "Load or construct an AnnData object with Dask-backed expression matrix (X as dask.array.Array). Call a pp module function on the Dask-backed AnnData."
- [other] Scanpy includes preprocessing capabilities as part of its toolkit for single-cell gene expression analysis, designed to work with the anndata data structure.: "Scanpy includes preprocessing capabilities as part of its toolkit for single-cell gene expression analysis, designed to work with the anndata data structure."
- [other] We use pytest to test scanpy. To run the tests, simply run `hatch test`: "We use pytest to test scanpy. To run the tests, simply run `hatch test`"
