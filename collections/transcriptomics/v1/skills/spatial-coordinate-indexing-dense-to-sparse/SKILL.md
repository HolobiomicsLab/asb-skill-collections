---
name: spatial-coordinate-indexing-dense-to-sparse
description: Use when you have computed k-nearest neighbors for spatial coordinates (e.g., via pynndescent or another NN backend) and need to store the resulting adjacency and distance information in a memory-efficient format compatible with downstream graph algorithms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3444
  edam_topics:
  - http://edamontology.org/topic_3473
  - http://edamontology.org/topic_0654
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

# spatial-coordinate-indexing-dense-to-sparse

## Summary

Convert dense spatial coordinate matrices into sparse CSR (Compressed Sparse Row) format adjacency and distance matrices for memory-efficient k-nearest-neighbor graph storage and retrieval. This skill is essential for scalable spatial analysis when working with large numbers of observations where most pairwise distances are irrelevant.

## When to use

You have computed k-nearest neighbors for spatial coordinates (e.g., via pynndescent or another NN backend) and need to store the resulting adjacency and distance information in a memory-efficient format compatible with downstream graph algorithms. Specifically, when k << n_obs (number of observations), sparse representations dramatically reduce memory footprint while preserving sparsity patterns needed for spatial statistics.

## When NOT to use

- Input coordinates are already indexed as a sparse matrix — this skill assumes dense indices and distances from a nearest-neighbor query.
- You need dense pairwise distance matrix for all observation pairs, not just k-nearest neighbors — sparse indexing discards non-neighbor distances intentionally.
- Downstream analysis requires random access to arbitrary (i,j) entries; CSR format is optimized for row-wise iteration, not column-wise or random lookups.

## Inputs

- k-nearest neighbor indices (array of shape [n_obs, k])
- k-nearest neighbor distances (array of shape [n_obs, k])
- n_obs: total number of observations (integer)
- k / n_neighs: number of neighbors per observation (integer)
- set_diag: boolean flag indicating whether to set diagonal entries

## Outputs

- adj: CSR sparse matrix (float32, shape [n_obs, n_obs]) — adjacency indicator matrix
- dst: CSR sparse matrix (float64, shape [n_obs, n_obs]) — distance matrix
- (adj, dst) tuple ready for graph-based spatial analysis

## How to apply

After querying a nearest-neighbor index (e.g., NNDescent with Euclidean metric) for k-nearest neighbors on spatial coordinates, extract the flattened row indices, column indices, and distance values. Construct two CSR sparse matrices: (1) an adjacency matrix (float32) with indicator values of 1.0 at (i, j) positions for each k-neighbor pair, and (2) a distance matrix (float64) with the actual distance values. Set diagonal entries to 1.0 and 0.0 respectively if set_diag=True. Verify that both matrices have shape (n_obs, n_obs), share identical sparsity patterns (same row/column indices), and are stored in CSR format for efficient row-wise access during subsequent spatial operations.

## Related tools

- **pynndescent** (Nearest-neighbor descent backend that queries spatial coordinates and returns k-neighbor indices and distances for input to sparse matrix construction) — https://github.com/lmcinnes/pynndescent
- **scipy.sparse** (CSR matrix construction and manipulation; provides csr_matrix class for efficient sparse storage)
- **numpy** (Array operations for flattening indices, creating sparse matrix data arrays, and setting diagonal entries)
- **Squidpy** (Spatial omics framework that integrates k-NN graph construction via GraphBuilderCSR and PynndescentKNNBuilder subclasses) — https://github.com/scverse/squidpy

## Examples

```
from scipy.sparse import csr_matrix; import numpy as np; indices_flat = np.repeat(np.arange(n_obs), k); cols = knn_indices.flatten(); data_adj = np.ones(len(indices_flat), dtype=np.float32); adj = csr_matrix((data_adj, (indices_flat, cols)), shape=(n_obs, n_obs), dtype=np.float32); dst = csr_matrix((knn_distances.flatten(), (indices_flat, cols)), shape=(n_obs, n_obs), dtype=np.float64)
```

## Evaluation signals

- Adjacency and distance matrices have identical shape (n_obs, n_obs) and identical sparsity patterns (same row/column indices).
- Both matrices are in CSR format (scipy.sparse.csr_matrix); verify via .format property and .has_sorted_indices.
- Adjacency matrix contains only 1.0 values (and 0.0 on diagonal if set_diag=False); distance matrix contains non-negative floats.
- Number of non-zero entries equals n_obs * k (plus n_obs if set_diag=True), reflecting k neighbors per observation.
- Diagonal entries of adj are 1.0 and diagonal entries of dst are 0.0 when set_diag=True; row-wise iteration produces k+1 neighbors per observation.

## Limitations

- Sparse indexing discards global distance information; only k-nearest distances are preserved, limiting global distance-based analyses.
- CSR format is optimized for row-wise access; column-wise or random (i,j) lookups require conversion or transposition, incurring overhead.
- Large k relative to n_obs reduces sparsity gains; trade-off between neighborhood completeness and memory efficiency must be evaluated per dataset.

## Evidence

- [other] Construct CSR sparse matrices for adjacency (adj, using float32 indicator values of 1.0) and distance (dst, using float64 distance values) from the flattened row/column indices and distances.: "Construct CSR sparse matrices for adjacency (adj, using float32 indicator values of 1.0) and distance (dst, using float64 distance values) from the flattened row/column indices and distances."
- [other] Query the NNDescent model for k-nearest neighbors (with k=n_neighs parameter) and extract indices and distances.: "Query the NNDescent model for k-nearest neighbors (with k=n_neighs parameter) and extract indices and distances."
- [other] Set diagonal values: adj diagonal to 1.0 if set_diag is True else existing values; dst diagonal to 0.0.: "Set diagonal values: adj diagonal to 1.0 if set_diag is True else existing values; dst diagonal to 0.0."
- [other] verify adjacency matrix shape matches (n_obs, n_obs), sparsity pattern is consistent between adj and dst, and matrices are in CSR format.: "verify adjacency matrix shape matches (n_obs, n_obs), sparsity pattern is consistent between adj and dst, and matrices are in CSR format."
- [other] Squidpy builds on scanpy and anndata, providing streamlined APIs for feature extraction and spatial statistics that enable scalable analysis of spatial molecular data.: "Squidpy builds on scanpy and anndata, providing streamlined APIs for feature extraction and spatial statistics that enable scalable analysis of spatial molecular data."
