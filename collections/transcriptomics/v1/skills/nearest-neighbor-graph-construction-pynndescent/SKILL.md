---
name: nearest-neighbor-graph-construction-pynndescent
description: Use when when analyzing spatial molecular data (e.g., from tissue sections or microscopy) where you need to build k-nearest neighbor graphs on high-dimensional coordinate arrays (n_obs × n_dims) and exact nearest neighbor computation is too slow or memory-intensive;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3361
  tools:
  - pynndescent
  - numpy
  - pytest
  - scipy.sparse
  - Squidpy
derived_from:
- doi: 10.1038/s41592-021-01358-2
  title: squidpy
evidence_spans:
- The [pynndescent](https://github.com/lmcinnes/pynndescent) library provides an approximate nearest-neighbor search backend
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

# nearest-neighbor-graph-construction-pynndescent

## Summary

Construct k-nearest neighbor graphs from spatial coordinates using pynndescent's approximate nearest neighbor descent algorithm, producing sparse adjacency and distance matrices in CSR format. This skill enables scalable graph-based spatial analysis by replacing exact KNN with fast approximate methods.

## When to use

When analyzing spatial molecular data (e.g., from tissue sections or microscopy) where you need to build k-nearest neighbor graphs on high-dimensional coordinate arrays (n_obs × n_dims) and exact nearest neighbor computation is too slow or memory-intensive; pynndescent is particularly suited when n_obs is large (>10k cells) and you can tolerate approximate rather than exact neighbors.

## When NOT to use

- Input coordinates are already a precomputed sparse adjacency matrix—use build_graph only on raw coordinate arrays.
- Your analysis requires exact nearest neighbors and cannot tolerate approximation error; use exact KNN (e.g., scipy.spatial.KDTree) instead.
- Coordinates are very low-dimensional (d < 3) or n_obs < 1000; exact methods may be faster and more accurate.

## Inputs

- spatial coordinates array (n_obs × n_dims, float32/float64)
- n_neighs parameter (integer, typically 5–50)
- set_diag parameter (boolean, whether to include self-loops)

## Outputs

- adjacency matrix (CSR sparse, float32, shape (n_obs, n_obs))
- distance matrix (CSR sparse, float64, shape (n_obs, n_obs))

## How to apply

Instantiate a PynndescentKNNBuilder subclass that inherits from GraphBuilderCSR and implements build_graph() to: (1) initialize an NNDescent model with the Euclidean metric on input coordinates; (2) query it for k-nearest neighbors using the n_neighs parameter; (3) extract neighbor indices and distances; (4) construct two CSR sparse matrices—adjacency (adj) with float32 indicator values of 1.0 for each edge, and distance (dst) with float64 distance values; (5) set diagonal: adj diagonal to 1.0 if set_diag=True, dst diagonal to 0.0; (6) return the (adj, dst) tuple. Implement uns_params() to return n_neighbors and set_diag for reproducibility. The CSR format is chosen for memory efficiency and compatibility with downstream graph operations in the scverse ecosystem.

## Related tools

- **pynndescent** (Provides NNDescent class for approximate nearest neighbor search and graph construction via Euclidean metric queries) — https://github.com/lmcinnes/pynndescent
- **scipy.sparse** (Constructs and manipulates CSR sparse matrices for adjacency and distance outputs)
- **numpy** (Handles array operations for flattening indices and distances, setting diagonal values)
- **Squidpy** (Provides GraphBuilderCSR base class and integrates KNN graph construction into spatial analysis workflows) — https://github.com/scverse/squidpy

## Examples

```
from squidpy.gr.neighbors import GraphBuilderCSR; from pynndescent import NNDescent; builder = PynndescentKNNBuilder(n_neighs=15, set_diag=True); adj, dst = builder.build_graph(coordinates)
```

## Evaluation signals

- Adjacency and distance matrices have shape (n_obs, n_obs) and are in CSR sparse format
- Sparsity pattern is consistent: dst has nonzero entries at exactly the same positions as adj (except possibly diagonal)
- Each row of adj contains exactly n_neighs nonzero entries (excluding self-loops if set_diag=False)
- Distance values in dst are non-negative floats; diagonal is 0.0 and adj diagonal is 1.0 when set_diag=True
- Matrix construction is reproducible: calling build_graph with identical coordinates and parameters yields identical matrices

## Limitations

- pynndescent returns approximate, not exact, nearest neighbors; neighbor sets may differ from exact KNN, especially for borderline (k+1)-th neighbors
- Euclidean metric is hard-coded; extensions to other metrics (cosine, Manhattan) would require modifying the NNDescent instantiation
- Performance and accuracy depend on pynndescent's internal parameters (tree degree, leaf size); no tuning interface is exposed in the workflow description
- Large n_dims (>100) may degrade neighbor quality due to curse of dimensionality; preprocessing (PCA) may be needed

## Evidence

- [other] Reconstruct the PynndescentKNNBuilder as a GraphBuilderCSR subclass for approximate KNN graph construction: "Create PynndescentKNNBuilder class inheriting from GraphBuilderCSR, implementing the build_graph method to instantiate NNDescent with Euclidean metric on input coordinates."
- [other] Query and CSR matrix construction: "Query the NNDescent model for k-nearest neighbors (with k=n_neighs parameter) and extract indices and distances. Construct CSR sparse matrices for adjacency (adj, using float32 indicator values of"
- [other] Diagonal and return logic: "Set diagonal values: adj diagonal to 1.0 if set_diag is True else existing values; dst diagonal to 0.0. Return (adj, dst) tuple from build_graph and implement uns_params method returning n_neighbors"
- [other] Testing and validation: "Test the builder on sample spatial coordinates and verify adjacency matrix shape matches (n_obs, n_obs), sparsity pattern is consistent between adj and dst, and matrices are in CSR format."
- [intro] Squidpy ecosystem and spatial analysis context: "Squidpy builds on scanpy and anndata, providing streamlined APIs for feature extraction and spatial statistics that enable scalable analysis of spatial molecular data."
- [readme] PyNNDescent algorithm foundation: "PyNNDescent is a Python nearest neighbor descent for approximate nearest neighbors. It provides a python implementation of Nearest Neighbor Descent for k-neighbor-graph construction and approximate"
