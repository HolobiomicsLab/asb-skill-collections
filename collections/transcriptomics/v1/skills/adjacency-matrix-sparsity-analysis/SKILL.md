---
name: adjacency-matrix-sparsity-analysis
description: Use when immediately after calling squidpy.gr.spatial_neighbors() or similar spatial graph construction methods on an AnnData object. It is essential when validating that the computed spatial graph has been correctly stored in adata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_3673
  tools:
  - scanpy
  - pip
  - Squidpy
  - AnnData
  - SciPy
  - NumPy
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

# adjacency-matrix-sparsity-analysis

## Summary

Verify the structural integrity and sparsity properties of adjacency and distance matrices stored as CSR sparse matrices in AnnData objects after spatial graph construction. This skill ensures that the resulting spatial graphs are correctly formatted, maintain expected sparsity patterns, and satisfy domain constraints (diagonal zeros for distance, consistent structure across paired matrices).

## When to use

Apply this skill immediately after calling squidpy.gr.spatial_neighbors() or similar spatial graph construction methods on an AnnData object. It is essential when validating that the computed spatial graph has been correctly stored in adata.obsp with the expected keys ('spatial_neighbors', 'spatial_distances') and matrix properties. Use it as a correctness checkpoint before downstream spatial statistics or visualization operations that depend on the graph structure.

## When NOT to use

- The adjacency or distance matrices are already verified and will not be used in downstream analysis—verification becomes redundant
- Working with dense distance or adjacency matrices from external sources not produced by Squidpy—sparsity structure assumptions may not hold
- Graph construction has already failed or raised an exception—structural validation cannot recover from upstream computational errors

## Inputs

- AnnData object with obsm['spatial'] or obsm containing spatial coordinates
- Computed adjacency matrix (CSR sparse format) stored in adata.obsp
- Computed distance matrix (CSR sparse format) stored in adata.obsp

## Outputs

- Validation report confirming matrix shape, format, sparsity structure, and diagonal constraints
- Boolean/status indicator of structural correctness
- Optional: visualizations of sparsity patterns or statistical summaries of non-zero element distributions

## How to apply

After spatial neighbor computation, retrieve the adjacency and distance matrices from adata.obsp using their standard keys. Verify that both matrices are stored as scipy.sparse CSR (Compressed Sparse Row) format objects, which is the efficient sparse representation used by Squidpy. Check that both matrices have identical shape (n_obs, n_obs) matching the number of observations in the AnnData object. Examine the sparsity structure: the distance matrix should have zeros only on the diagonal (or as specified by set_diag parameter), while the adjacency matrix should follow the same sparsity pattern as the distance matrix. Confirm that non-zero elements are present and reasonable, indicating that neighbors were actually identified. Compare the two matrices' sparsity patterns to ensure they share the same connectivity structure, as they represent the same neighborhood graph with different information (distances vs. binary adjacency).

## Related tools

- **Squidpy** (Provides the spatial graph construction API (gr.spatial_neighbors) whose outputs are validated; defines the CSR sparse matrix storage convention in adata.obsp) — https://github.com/scverse/squidpy
- **AnnData** (Provides the data structure (obsp slots) in which adjacency and distance matrices are stored and accessed)
- **SciPy** (Provides sparse matrix (CSR) format and operations for inspecting matrix shape, sparsity, and element structure)
- **NumPy** (Used to inspect and compare matrix structures, shapes, and diagonal properties)

## Examples

```
import squidpy as sq; import anndata as ad; adata = sq.datasets.visium(); sq.gr.spatial_neighbors(adata); assert adata.obsp['spatial_neighbors'].format == 'csr' and adata.obsp['spatial_distances'].shape == (adata.n_obs, adata.n_obs)
```

## Evaluation signals

- Both matrices retrieved from adata.obsp are scipy.sparse._matrix.csr_matrix or csr_array objects, not dense arrays
- Both matrices have identical shape (n_obs, n_obs) equal to the number of rows in adata.obs and columns in adata.var
- Distance matrix diagonal is either all zeros or satisfies the set_diag constraint; no diagonal elements are NaN or infinite
- Adjacency and distance matrices have identical nonzero sparsity patterns (same (row, col) indices with nonzeros), confirming they represent the same neighborhood graph
- Nonzero elements in distance matrix are non-negative and finite; nonzero elements in adjacency matrix are positive (typically 1 for unweighted or weights > 0 for weighted)

## Limitations

- This skill validates structural properties only; it does not verify that the spatial coordinates themselves are correct, normalized, or on the expected scale
- Sparsity analysis assumes Squidpy's standard storage convention (CSR format in adata.obsp with keys 'spatial_neighbors' and 'spatial_distances'); graphs stored elsewhere or in alternative formats may not be detected
- The skill does not validate the underlying nearest-neighbor algorithm's correctness (e.g., whether k neighbors were truly found, whether distance metrics are appropriate); it only checks that the output structure is well-formed
- Very large graphs (millions of observations) may consume significant memory during full sparsity pattern comparison; sampling or statistical summaries may be necessary for performance

## Evidence

- [other] Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances'.: "Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances'"
- [other] Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints.: "Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints (diagonal zero for distance, identity or zero for"
- [other] Squidpy provides streamlined APIs for spatial statistics and interactive exploration, building on anndata as the underlying data structure.: "Squidpy provides streamlined APIs for spatial statistics and interactive exploration, building on anndata as the underlying data structure"
- [readme] It builds on scanpy and anndata, from which it inherits modularity and scalability.: "It builds on top of `scanpy`_ and `anndata`_, from which it inherits modularity and scalability"
