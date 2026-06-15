---
name: sparse-matrix-verification-and-validation
description: Use when after calling squidpy.gr.spatial_neighbors or any graph-building operation that outputs sparse matrices to adata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3306
  - http://edamontology.org/topic_0634
  tools:
  - scanpy
  - pip
  - Squidpy
  - anndata
  - scipy.sparse
derived_from:
- doi: 10.1038/s41592-021-01358-2
  title: squidpy
evidence_spans:
- It builds on scanpy and anndata
- pip install squidpy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_squidpy
    doi: 10.1038/s41592-021-01358-2
    title: squidpy
  dedup_kept_from: coll_squidpy
schema_version: 0.2.0
---

# Sparse Matrix Verification and Validation

## Summary

Verify that spatial graph construction in an AnnData object correctly produces CSR sparse matrices with expected dimensions, sparsity structure, and diagonal constraints. This skill ensures the integrity of adjacency and distance matrices used for downstream spatial statistics in single-cell and spatial omics workflows.

## When to use

After calling squidpy.gr.spatial_neighbors or any graph-building operation that outputs sparse matrices to adata.obsp, to confirm that the resulting adjacency and distance matrices have the correct shape (n_obs × n_obs), are stored in CSR format, satisfy expected sparsity patterns, and respect diagonal constraints (e.g., zero diagonal for distances, identity or zero for adjacency depending on set_diag parameter).

## When NOT to use

- Input matrices are already validated or come from a trusted, production-quality pipeline with built-in checks.
- The spatial graph has not yet been computed; run gr.spatial_neighbors first.
- Working with dense matrices rather than sparse matrices; convert to CSR first or use dense-specific validation.

## Inputs

- AnnData object with spatial coordinates in obsm
- CSR sparse matrix (adjacency or distance) stored in adata.obsp

## Outputs

- Validation report: shape confirmation (n_obs × n_obs)
- Sparsity structure validation (matching non-zero counts and pattern)
- Diagonal constraint validation (zero or identity as appropriate)
- Boolean flag indicating pass/fail for each constraint

## How to apply

After spatial graph construction, retrieve the adjacency and distance matrices from adata.obsp (typically with keys 'spatial_neighbors' and 'spatial_distances'). Check that both matrices are scipy.sparse CSR matrices, verify their shape matches the observation count in adata.n_obs, confirm matching sparsity structure and non-zero counts between the two, and validate that diagonal elements satisfy the expected constraints: distance matrix diagonal should be zero, and adjacency matrix diagonal depends on the set_diag parameter used during graph construction. The rationale is that CSR format enables scalable operations on large spatial graphs, matching shape ensures consistency with observation metadata, and diagonal constraints reflect the semantic meaning of self-loops (a cell is not its own neighbor).

## Related tools

- **Squidpy** (Spatial graph construction via gr.spatial_neighbors; provides the sparse matrices to validate) — https://github.com/scverse/squidpy
- **anndata** (AnnData data structure storing spatial graphs in obsp slot as CSR matrices)
- **scipy.sparse** (CSR sparse matrix format verification and shape/diagonal inspection)
- **scanpy** (Upstream pipeline component; Squidpy builds on scanpy for compatibility)

## Examples

```
import squidpy as sq; import anndata; adata = sq.datasets.visium(); sq.gr.spatial_neighbors(adata); assert adata.obsp['spatial_neighbors'].shape == (adata.n_obs, adata.n_obs); assert adata.obsp['spatial_distances'].diagonal().sum() == 0
```

## Evaluation signals

- Both adjacency and distance matrices have shape (n_obs, n_obs) matching adata.n_obs
- Both matrices are scipy.sparse._matrix.csr_matrix or csr_array instances (CSR format)
- Non-zero element counts and sparsity patterns match between adjacency and distance matrices
- Distance matrix diagonal is all zeros (no self-loops in distance)
- Adjacency matrix diagonal matches expected value from set_diag parameter (typically zero or 1)

## Limitations

- Validation only checks structural integrity, not semantic correctness of edge weights or distances; if coordinates are malformed upstream, correct matrices may still reflect incorrect spatial relationships.
- Does not verify that the spatial_neighbors and spatial_distances matrices correspond to the same k-nearest-neighbor or radius parameter; mismatches could occur if constructed separately.
- Diagonal constraints assume standard spatial graph semantics; custom applications with intentional self-loops will fail validation.

## Evidence

- [other] Call squidpy.gr.spatial_neighbors on the AnnData object to compute spatial graph using coordinate data from obsm.: "Call squidpy.gr.spatial_neighbors on the AnnData object to compute spatial graph using coordinate data from obsm."
- [other] Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances'.: "Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances'."
- [other] Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints (diagonal zero for distance, identity or zero for adjacency depending on set_diag parameter).: "Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints (diagonal zero for distance, identity or zero for"
- [other] Squidpy provides streamlined APIs for spatial statistics and interactive exploration, building on anndata as the underlying data structure.: "Squidpy provides streamlined APIs for spatial statistics and interactive exploration, building on anndata as the underlying data structure."
