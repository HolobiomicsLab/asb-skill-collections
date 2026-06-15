---
name: euclidean-distance-computation-approximation
description: Use when when constructing k-nearest neighbor graphs from spatial coordinates (e.g., microscopy x,y positions or tissue section coordinates) and exact neighbor discovery is computationally prohibitive;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0634
  tools:
  - numpy
  - pytest
  - pynndescent
  - scipy.sparse
  - Squidpy
derived_from:
- doi: 10.1038/s41592-021-01358-2
  title: squidpy
evidence_spans:
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

# Euclidean Distance Computation & Approximation

## Summary

Approximate k-nearest neighbor graph construction using Euclidean distance metrics via the pynndescent library integrated into GraphBuilderCSR subclasses. This skill enables scalable nearest-neighbor discovery for spatial coordinate data in spatial omics workflows.

## When to use

When constructing k-nearest neighbor graphs from spatial coordinates (e.g., microscopy x,y positions or tissue section coordinates) and exact neighbor discovery is computationally prohibitive; pynndescent's approximate nearest neighbor descent algorithm trades strict exactness for speed while maintaining practical accuracy for downstream spatial statistics (neighborhood enrichment, spatial autocorrelation, clustering).

## When NOT to use

- Input coordinates are already in a pre-computed distance or similarity matrix format (use direct sparse matrix construction instead).
- Exact nearest neighbors with strict distance guarantees are required for downstream statistical testing or publication (approximate methods may yield different neighbor sets, affecting significance results).
- Spatial data is extremely high-dimensional (>100 features); pynndescent performs well in moderate dimensions but alternative metrics or dimensionality reduction may be more suitable.

## Inputs

- Spatial coordinates (numpy array or pandas DataFrame with n_obs × 2+ dimensions: x, y, [z])
- n_neighbors parameter (integer: target number of approximate nearest neighbors per observation)
- set_diag parameter (boolean: whether to set adjacency matrix diagonal to 1.0)

## Outputs

- Adjacency matrix (scipy.sparse.csr_matrix, float32, shape (n_obs, n_obs))
- Distance matrix (scipy.sparse.csr_matrix, float64, shape (n_obs, n_obs), Euclidean distances)

## How to apply

Instantiate a PynndescentKNNBuilder subclass of GraphBuilderCSR, configuring NNDescent with Euclidean metric on input spatial coordinates. Query the fitted NNDescent model for k-nearest neighbors with a specified k parameter (n_neighs), extracting both indices and distance values from the approximate search. Construct two CSR sparse matrices: an adjacency matrix (float32, indicator values of 1.0) and a distance matrix (float64, raw Euclidean distances). Set diagonal values according to the set_diag flag (adjacency diagonal = 1.0 if True; distance diagonal always = 0.0). Return the (adj, dst) tuple and implement the uns_params method to store n_neighbors and set_diag hyperparameters for reproducibility. Validate output matrices by checking shape (n_obs, n_obs), verifying sparsity pattern consistency between adj and dst, and confirming CSR format compliance.

## Related tools

- **pynndescent** (Approximate nearest neighbor descent backend for k-neighbor-graph construction and distance-based neighbor search using Euclidean metric) — https://github.com/lmcinnes/pynndescent
- **scipy.sparse** (CSR sparse matrix construction and manipulation for efficient storage and computation of adjacency and distance matrices) — https://docs.scipy.org/doc/scipy/reference/sparse.html
- **numpy** (Handling and transforming coordinate arrays, flattening indices, and distance value management) — https://numpy.org
- **Squidpy** (Integration framework providing GraphBuilderCSR base class and spatial analysis context for neighbor graph construction) — https://github.com/scverse/squidpy
- **pytest** (Automated testing of builder output shape, sparsity patterns, CSR format compliance, and diagonal value correctness) — https://github.com/pytest-dev/pytest

## Examples

```
builder = PynndescentKNNBuilder(n_neighs=15, set_diag=True); adj, dst = builder.build_graph(coordinates); assert adj.shape == (n_obs, n_obs) and scipy.sparse.issparse(adj) and adj.format == 'csr'
```

## Evaluation signals

- Output adjacency matrix shape equals (n_obs, n_obs) and distance matrix shape matches.
- Sparsity pattern is consistent between adjacency and distance matrices (same indices and row-column structure).
- Both matrices are in scipy.sparse.csr_matrix format verified by type and format attribute checks.
- Adjacency matrix diagonal values equal 1.0 when set_diag=True, or retain original sparse values when False; distance matrix diagonal equals 0.0.
- Euclidean distance values in the distance matrix are non-negative and finite (no NaN or Inf); adjacency matrix contains only indicator values (0.0 or 1.0).

## Limitations

- Approximate nearest neighbor search may yield different neighbor sets than exact methods (e.g., brute-force scipy.spatial.distance.cdist), potentially affecting reproducibility and statistical sensitivity in downstream analyses.
- Performance gains are most pronounced on moderate-dimensional spatial data (2–50 dimensions); higher dimensions may see diminishing returns or increased computational cost.
- Euclidean metric assumes isotropy and may not be appropriate for anisotropic tissue structures or weighted coordinate systems; alternative metrics would require extending the builder interface.
- The set_diag parameter does not affect distance matrix diagonal (always 0.0), which may be counterintuitive for some applications expecting self-distances.

## Evidence

- [other] Create PynndescentKNNBuilder class inheriting from GraphBuilderCSR, implementing the build_graph method to instantiate NNDescent with Euclidean metric on input coordinates.: "Create PynndescentKNNBuilder class inheriting from GraphBuilderCSR, implementing the build_graph method to instantiate NNDescent with Euclidean metric on input coordinates."
- [other] Query the NNDescent model for k-nearest neighbors (with k=n_neighs parameter) and extract indices and distances.: "Query the NNDescent model for k-nearest neighbors (with k=n_neighs parameter) and extract indices and distances."
- [other] Construct CSR sparse matrices for adjacency (adj, using float32 indicator values of 1.0) and distance (dst, using float64 distance values) from the flattened row/column indices and distances.: "Construct CSR sparse matrices for adjacency (adj, using float32 indicator values of 1.0) and distance (dst, using float64 distance values) from the flattened row/column indices and distances."
- [other] Set diagonal values: adj diagonal to 1.0 if set_diag is True else existing values; dst diagonal to 0.0.: "Set diagonal values: adj diagonal to 1.0 if set_diag is True else existing values; dst diagonal to 0.0."
- [other] Test the builder on sample spatial coordinates and verify adjacency matrix shape matches (n_obs, n_obs), sparsity pattern is consistent between adj and dst, and matrices are in CSR format.: "Test the builder on sample spatial coordinates and verify adjacency matrix shape matches (n_obs, n_obs), sparsity pattern is consistent between adj and dst, and matrices are in CSR format."
- [readme] PyNNDescent is a Python nearest neighbor descent for approximate nearest neighbors. It provides a python implementation of Nearest Neighbor Descent for k-neighbor-graph construction and approximate nearest neighbor search: "PyNNDescent is a Python nearest neighbor descent for approximate nearest neighbors. It provides a python implementation of Nearest Neighbor Descent for k-neighbor-graph construction"
- [intro] Squidpy builds on scanpy and anndata, providing streamlined APIs for feature extraction and spatial statistics that enable scalable analysis of spatial molecular data.: "It builds on scanpy and anndata, providing streamlined APIs for feature extraction and spatial statistics"
