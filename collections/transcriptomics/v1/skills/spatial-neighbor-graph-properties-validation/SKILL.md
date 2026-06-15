---
name: spatial-neighbor-graph-properties-validation
description: Use when after calling squidpy.gr.spatial_neighbors on an AnnData object containing spatial coordinates in obsm.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0080
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

# spatial-neighbor-graph-properties-validation

## Summary

Verify that a spatial neighbor graph constructed via squidpy.gr.spatial_neighbors has been correctly stored as CSR sparse matrices in an AnnData object with expected dimensionality, sparsity structure, and diagonal properties. This validation ensures the graph is suitable for downstream spatial statistics.

## When to use

After calling squidpy.gr.spatial_neighbors on an AnnData object containing spatial coordinates in obsm. Use this skill to confirm that the resulting adjacency and distance matrices have the expected shape, sparse format, and mathematical properties before proceeding to spatial analysis or statistics.

## When NOT to use

- The spatial graph has not yet been computed; use squidpy.gr.spatial_neighbors first.
- You are working with pre-computed distance or similarity matrices not intended as spatial neighbor graphs.
- The coordinate data in obsm is missing, incomplete, or contains NaN values.

## Inputs

- AnnData object with spatial coordinates in obsm (e.g., from squidpy.datasets)
- Keys identifying adjacency and distance matrices in adata.obsp

## Outputs

- Validation report confirming CSR sparse matrix format
- Shape and sparsity structure equivalence confirmation
- Diagonal constraint verification (zero or identity)

## How to apply

Retrieve the adjacency and distance matrices from adata.obsp using keys 'spatial_neighbors' and 'spatial_distances' (or user-specified equivalents). Check that both matrices are scipy.sparse.csr_matrix instances with shape (n_obs, n_obs) matching the observation count in adata. Verify they have identical sparsity structure (same non-zero indices). For the distance matrix, confirm the diagonal is zero (no self-loops). For the adjacency matrix, check the diagonal according to the set_diag parameter used during construction (typically zero for undirected graphs). Inspect the matrices' data types and confirm values are numeric and finite.

## Related tools

- **Squidpy** (Computes spatial neighbor graph; provides spatial_neighbors function) — https://github.com/scverse/squidpy
- **anndata** (Stores adjacency and distance matrices in .obsp attribute; defines AnnData object structure)
- **scanpy** (Provides foundational single-cell analysis utilities; AnnData is built on scanpy conventions)
- **scipy.sparse** (Provides CSR sparse matrix format for efficient storage and computation)

## Examples

```
import squidpy as sq; adata = sq.datasets.visium(); sq.gr.spatial_neighbors(adata); assert adata.obsp['spatial_neighbors'].shape == (adata.n_obs, adata.n_obs); assert adata.obsp['spatial_distances'].diagonal().sum() == 0
```

## Evaluation signals

- Both 'spatial_neighbors' and 'spatial_distances' keys exist in adata.obsp
- Both matrices are scipy.sparse._arrays.csr_array or scipy.sparse.csr_matrix instances
- Shape of both matrices is (n_obs, n_obs) where n_obs = adata.n_obs
- Sparsity pattern (indices of non-zero entries) is identical between adjacency and distance matrices
- Distance matrix diagonal contains all zeros; adjacency matrix diagonal matches the set_diag parameter (typically zero for undirected graphs)
- All matrix values are finite (no NaN or inf entries)

## Limitations

- Validation only checks structural properties; it does not verify that the graph was computed with the correct neighborhood radius or k parameter.
- Different coordinate systems (obsm keys) or distance metrics may produce structurally valid but semantically incorrect graphs; domain knowledge of tissue layout is needed.
- Extremely sparse or extremely dense graphs may indicate suboptimal parameter choices but will still pass structural validation.

## Evidence

- [other] Call squidpy.gr.spatial_neighbors on the AnnData object to compute spatial graph using coordinate data from obsm.: "Call squidpy.gr.spatial_neighbors on the AnnData object to compute spatial graph using coordinate data from obsm."
- [other] Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances'.: "Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances'."
- [other] Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints (diagonal zero for distance, identity or zero for adjacency depending on set_diag parameter).: "Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints (diagonal zero for distance, identity or zero for"
- [intro] It builds on scanpy and anndata: "It builds on scanpy and anndata"
- [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images: "Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images"
