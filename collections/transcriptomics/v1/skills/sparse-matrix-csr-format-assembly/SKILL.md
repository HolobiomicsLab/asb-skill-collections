---
name: sparse-matrix-csr-format-assembly
description: Use when when you have computed k-nearest neighbor indices and distances (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3792
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0769
  tools:
  - scipy.sparse
  - numpy
  - pytest
  - pynndescent
  - Squidpy
derived_from:
- doi: 10.1038/s41592-021-01358-2
  title: squidpy
evidence_spans:
- csr_matrix objects and should reuse Squidpy's CSR-specific postprocessors
- np.repeat(np.arange(n_obs), self.n_neighs); np.ones_like(row_indices, dtype=np.float32)
- This package uses [pytest][] for automated testing.
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

# sparse-matrix-csr-format-assembly

## Summary

Assemble adjacency and distance matrices into Compressed Sparse Row (CSR) format from flattened neighbor indices and distance arrays. This skill is essential for memory-efficient storage and fast linear algebra operations on large spatial graphs in bioinformatics workflows.

## When to use

When you have computed k-nearest neighbor indices and distances (e.g., from pynndescent NNDescent queries) and need to construct sparse adjacency and distance matrices for subsequent graph algorithms, community detection, or spatial statistics on cohorts with >1000 observations where dense matrices would be prohibitive.

## When NOT to use

- If your observation count is <100 and memory is not a constraint; dense numpy arrays may be simpler and faster for small graphs.
- If you need to frequently modify matrix entries after construction; CSR format is optimized for read/iteration, not incremental updates.
- If your neighbor data is already in a different sparse format (e.g., COO, CSC) that you will reuse directly without conversion overhead.

## Inputs

- k-nearest neighbor indices array (shape: n_obs × k, dtype: int)
- corresponding distance values array (shape: n_obs × k, dtype: float64)
- number of observations (n_obs: int)
- k value (number of neighbors per observation: int)
- set_diag parameter (whether to set adjacency diagonal to 1.0: bool)

## Outputs

- adjacency matrix (scipy.sparse._matrix.csr_matrix, shape: n_obs × n_obs, dtype: float32, values ∈ {0.0, 1.0})
- distance matrix (scipy.sparse._matrix.csr_matrix, shape: n_obs × n_obs, dtype: float64, values ≥ 0.0)

## How to apply

Extract row and column indices from the flattened k-nearest neighbor query results and the corresponding distance values. Instantiate scipy.sparse CSR matrices using the (row, column, data) triplet format, where the adjacency matrix uses float32 indicator values (typically 1.0 for edges) and the distance matrix uses float64 distance values. Set diagonal entries: adjacency diagonal to 1.0 if set_diag parameter is True (self-loops), otherwise preserve existing values; distance diagonal to 0.0 (zero self-distance). Verify that both matrices share the same sparsity pattern (same row/column indices) and confirm the output shape matches (n_obs, n_obs) where n_obs is the number of observations.

## Related tools

- **scipy.sparse** (Provides CSR sparse matrix construction and linear algebra primitives for assembly from (row, col, data) triplets)
- **pynndescent** (Computes k-nearest neighbor indices and distances via NNDescent.query() that feed directly into CSR matrix construction) — https://github.com/lmcinnes/pynndescent
- **numpy** (Handles index flattening, array reshaping, and diagonal value assignment before CSR instantiation)
- **Squidpy** (Provides GraphBuilderCSR base class and build_graph interface that encapsulates CSR assembly as part of spatial graph construction) — https://github.com/scverse/squidpy

## Examples

```
from scipy.sparse import csr_matrix; import numpy as np; neighbor_indices, distances = nn_model.query(coords, k=15); rows = np.repeat(np.arange(len(coords)), k); cols = neighbor_indices.ravel(); adj = csr_matrix((np.ones(len(distances.ravel()), dtype=np.float32), (rows, cols)), shape=(len(coords), len(coords))); dst = csr_matrix((distances.ravel(), (rows, cols)), shape=(len(coords), len(coords)), dtype=np.float64); adj.setdiag(1.0); dst.setdiag(0.0)
```

## Evaluation signals

- Output adjacency matrix has shape (n_obs, n_obs) and sparsity pattern matches distance matrix (same non-zero positions).
- Adjacency matrix contains only float32 values of 0.0 or 1.0; distance matrix contains float64 values ≥ 0.0.
- Both matrices are stored in CSR format (confirmed by isinstance(adj, scipy.sparse.csr_matrix) and isinstance(dst, scipy.sparse.csr_matrix)).
- Adjacency diagonal equals 1.0 (if set_diag=True) or matches input indices (if set_diag=False); distance diagonal equals 0.0.
- Matrix density (nnz / size) is consistent with expected sparsity: ≈ k / n_obs for exact k-neighbors, slightly higher for deduplication or boundary effects.

## Limitations

- CSR format assumes immutable structure after construction; frequent edge insertions/deletions require conversion to COO, modification, and conversion back.
- Distance matrix diagonal must be explicitly set to 0.0; some downstream algorithms may interpret missing diagonal entries as infinity rather than zero.
- Memory savings are modest if k is close to n_obs (approaching dense regime); benefit is significant only when k ≪ n_obs (sparse regime, typically k < 50).
- Floating-point precision: float32 adjacency values lose precision for weighted edges with magnitude variation; consider float64 if edge weights span orders of magnitude.

## Evidence

- [other] Construct CSR sparse matrices for adjacency (adj, using float32 indicator values of 1.0) and distance (dst, using float64 distance values) from the flattened row/column indices and distances.: "Construct CSR sparse matrices for adjacency (adj, using float32 indicator values of 1.0) and distance (dst, using float64 distance values) from the flattened row/column indices and distances."
- [other] Set diagonal values: adj diagonal to 1.0 if set_diag is True else existing values; dst diagonal to 0.0.: "Set diagonal values: adj diagonal to 1.0 if set_diag is True else existing values; dst diagonal to 0.0."
- [other] verify adjacency matrix shape matches (n_obs, n_obs), sparsity pattern is consistent between adj and dst, and matrices are in CSR format: "verify adjacency matrix shape matches (n_obs, n_obs), sparsity pattern is consistent between adj and dst, and matrices are in CSR format"
- [intro] providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images: "providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections"
