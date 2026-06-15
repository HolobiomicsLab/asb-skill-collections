---
name: graph-builder-subclassing-squidpy
description: Use when you have spatial molecular data (e.g., coordinates from microscopy or sequencing assays stored in an AnnData object), you need to compute a k-nearest-neighbor graph for spatial statistics (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_3678
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_2229
  tools:
  - Squidpy
  - numpy
  - pytest
  - pynndescent
  - scipy.sparse
derived_from:
- doi: 10.1038/s41592-021-01358-2
  title: squidpy
evidence_spans:
- Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data.
- gr.nhood_enrichment
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

# graph-builder-subclassing-squidpy

## Summary

Subclass Squidpy's GraphBuilderCSR to integrate a custom nearest-neighbor backend (such as pynndescent) for approximate k-NN graph construction on spatial coordinates. This skill enables scalable construction of sparse adjacency and distance matrices from coordinate data, essential for downstream spatial statistics and feature extraction in spatial omics workflows.

## When to use

You have spatial molecular data (e.g., coordinates from microscopy or sequencing assays stored in an AnnData object), you need to compute a k-nearest-neighbor graph for spatial statistics (e.g., neighborhood analysis, spatial autocorrelation), and you want to leverage a specialized approximate-NN library (e.g., pynndescent with Euclidean metric) to scale beyond exhaustive nearest-neighbor search.

## When NOT to use

- Input coordinates are already in a pre-computed graph or adjacency matrix format — use direct graph loading instead
- You require exact all-pairs nearest neighbors and cannot tolerate approximation error — use exact methods (e.g., scipy.spatial.distance.cdist) instead
- Your spatial data is already reduced to a pre-computed feature table without coordinate information — graph construction requires explicit (x, y) or (x, y, z) coordinates

## Inputs

- Spatial coordinate array (n_obs × n_features, typically float64 or float32)
- Integer k parameter (n_neighs, number of nearest neighbors to retrieve)
- Boolean flag set_diag (whether to set adjacency diagonal to 1.0)

## Outputs

- Adjacency CSR sparse matrix (n_obs × n_obs, float32, indicator values 1.0 for neighbors)
- Distance CSR sparse matrix (n_obs × n_obs, float64, pairwise neighbor distances)
- Tuple (adj, dst) returned from build_graph method

## How to apply

Create a new class inheriting from GraphBuilderCSR and override the build_graph method to: (1) instantiate your chosen NN backend (e.g., NNDescent from pynndescent) with the input coordinates and Euclidean metric; (2) query the model for k neighbors using the n_neighs parameter; (3) extract neighbor indices and distances, then flatten them into dense row/column coordinate arrays; (4) construct two CSR sparse matrices — adjacency (adj) with float32 indicator values of 1.0 for neighbor pairs and distance (dst) with float64 distance values — from the coordinate arrays and flattened distances; (5) optionally set diagonal values (adj to 1.0 if set_diag=True, dst to 0.0); (6) return (adj, dst) and implement uns_params to expose n_neighbors and set_diag as unseen parameters. Test on sample coordinates to verify matrix shapes, sparsity consistency, and CSR format compliance.

## Related tools

- **pynndescent** (Nearest-neighbor descent library used to build approximate k-NN graphs with pluggable distance metrics (e.g., Euclidean) on spatial coordinates) — https://github.com/lmcinnes/pynndescent
- **scipy.sparse** (Constructs and manipulates CSR sparse matrix objects for adjacency and distance matrices)
- **numpy** (Handles array flattening, coordinate indexing, and diagonal value assignment for sparse matrix construction)
- **Squidpy** (Provides the GraphBuilderCSR base class and integration framework for spatial graph construction within AnnData workflows) — https://github.com/scverse/squidpy
- **pytest** (Framework for unit and integration testing of the builder class, matrix properties, and shape/sparsity invariants)

## Examples

```
from squidpy.gr.neighbors import GraphBuilderCSR; import pynndescent; builder = PynndescentKNNBuilder(n_neighs=10, set_diag=True); adj, dst = builder.build_graph(coordinates); assert adj.shape == (n_obs, n_obs) and adj.format == 'csr'
```

## Evaluation signals

- Adjacency matrix shape equals (n_obs, n_obs) and distance matrix shape equals (n_obs, n_obs)
- Both matrices are in CSR (Compressed Sparse Row) format with matching sparsity patterns (same non-zero locations)
- Adjacency matrix values are all 1.0 (float32) except diagonal, which is 1.0 if set_diag=True else unchanged
- Distance matrix values are non-negative floats (float64) with diagonal set to 0.0
- Number of non-zero entries per row in adjacency matrix ≈ n_neighs (allowing for ties or boundary effects at edges of graph)
- build_graph returns a tuple (adj, dst) and uns_params returns dict with keys 'n_neighbors' and 'set_diag'
- Sparse matrices can be efficiently multiplied and sliced without dense materialization

## Limitations

- Pynndescent approximation may miss some true k-nearest neighbors; compare against exact methods if exact neighborhood membership is critical
- CSR matrices trade lookup speed for construction overhead; dense queries on sparse graphs can be slow
- Memory usage scales with sparsity (k × n_obs) but can still be substantial for very large n_obs; consider hierarchical or block-wise construction for extremely large datasets
- Diagonal handling (set_diag parameter) must be consistent across adjacency and distance matrices to avoid downstream analysis artifacts
- Distance metric is fixed at instantiation; switching metrics requires instantiating a new builder

## Evidence

- [other] How does the PynndescentKNNBuilder class implement graph construction by subclassing GraphBuilderCSR and integrating pynndescent as its nearest-neighbor backend?: "Reconstruct the PynndescentKNNBuilder as a GraphBuilderCSR subclass for approximate KNN graph construction"
- [other] Create PynndescentKNNBuilder class inheriting from GraphBuilderCSR, implementing the build_graph method to instantiate NNDescent with Euclidean metric on input coordinates.: "Create PynndescentKNNBuilder class inheriting from GraphBuilderCSR, implementing the build_graph method to instantiate NNDescent with Euclidean metric on input coordinates."
- [other] Query the NNDescent model for k-nearest neighbors and extract indices and distances.: "Query the NNDescent model for k-nearest neighbors (with k=n_neighs parameter) and extract indices and distances."
- [other] Construct CSR sparse matrices for adjacency and distance from flattened indices.: "Construct CSR sparse matrices for adjacency (adj, using float32 indicator values of 1.0) and distance (dst, using float64 distance values) from the flattened row/column indices and distances."
- [other] Test the builder on sample spatial coordinates and verify matrix properties.: "Test the builder on sample spatial coordinates and verify adjacency matrix shape matches (n_obs, n_obs), sparsity pattern is consistent between adj and dst, and matrices are in CSR format."
- [intro] Squidpy builds on scanpy and anndata for streamlined spatial analysis.: "Squidpy builds on scanpy and anndata, providing streamlined APIs for feature extraction and spatial statistics that enable scalable analysis of spatial molecular data."
- [other] The pynndescent library provides nearest-neighbor descent implementation.: "The [pynndescent](https://github.com/lmcinnes/pynndescent) library"
