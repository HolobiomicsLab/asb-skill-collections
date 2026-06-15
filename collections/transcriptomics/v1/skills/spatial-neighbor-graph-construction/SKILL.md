---
name: spatial-neighbor-graph-construction
description: Use when when you have spatial molecular data (e.g., Visium, imaging-based cytometry) stored in an AnnData object with coordinate information in .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3676
  - http://edamontology.org/topic_3577
  tools:
  - scanpy
  - pip
  - Squidpy
  - anndata
  - pynndescent
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

# spatial-neighbor-graph-construction

## Summary

Construct a spatial neighbor graph from coordinate data in an AnnData object using radius-based or k-nearest-neighbor detection, storing adjacency and distance matrices as sparse CSR structures. This is a foundational step for spatial statistics and downstream neighborhood enrichment analyses.

## When to use

When you have spatial molecular data (e.g., Visium, imaging-based cytometry) stored in an AnnData object with coordinate information in .obsm, and you need to define which observations are spatial neighbors for downstream analyses such as neighborhood enrichment, spatial autocorrelation, or clustering. Required before any spatial statistic that depends on a neighbor graph.

## When NOT to use

- Input data lacks spatial coordinates or adata.obsm is empty — construct coordinates first.
- Neighbor graph already exists in adata.obsp — reuse the existing graph rather than recomputing.
- Spatial scale is undefined or inappropriate for the tissue type — clarify neighborhood radius or k before calling the function.

## Inputs

- AnnData object with spatial coordinates in adata.obsm
- Coordinate array (typically shape n_obs × 2 for 2D data)

## Outputs

- Sparse CSR adjacency matrix stored at adata.obsp['spatial_neighbors']
- Sparse CSR distance matrix stored at adata.obsp['spatial_distances']

## How to apply

Load a spatial dataset into AnnData using squidpy.datasets (e.g., visium(), imc()) to ensure coordinate data is populated in adata.obsm. Call squidpy.gr.spatial_neighbors() on the AnnData object, specifying the coordinate key (typically 'spatial') and a neighborhood detection method (radius-based with radius parameter or k-nearest neighbors). The function computes pairwise spatial distances from the coordinate matrix and constructs a neighbor graph, storing both the adjacency matrix and distance matrix as CSR sparse matrices in adata.obsp with keys 'spatial_neighbors' and 'spatial_distances'. Verify that both matrices have shape (n_obs, n_obs) matching the observation count, exhibit matching sparsity structure, satisfy diagonal constraints (distance matrix diagonal = 0, adjacency diagonal depends on set_diag parameter), and that the neighborhood structure reflects your intended spatial scale.

## Related tools

- **Squidpy** (Provides streamlined spatial_neighbors() API for graph construction from coordinate data in AnnData) — https://github.com/scverse/squidpy
- **anndata** (Underlying data structure (AnnData) that stores coordinates in .obsm and graphs in .obsp)
- **scanpy** (Foundational toolkit on which Squidpy builds, used for general single-cell data handling)
- **pynndescent** (Nearest neighbor descent library used internally for efficient neighbor search) — https://github.com/lmcinnes/pynndescent

## Examples

```
import squidpy as sq
adata = sq.datasets.visium()
sq.gr.spatial_neighbors(adata, radius=50)
print(adata.obsp['spatial_neighbors'].shape, adata.obsp['spatial_distances'].shape)
```

## Evaluation signals

- Both sparse matrices exist in adata.obsp with expected keys: 'spatial_neighbors' and 'spatial_distances'.
- Matrices have identical shape (n_obs, n_obs) and matching sparsity patterns — same non-zero entries.
- Distance matrix diagonal contains only zeros; adjacency matrix diagonal is zero (or matches set_diag parameter).
- Sparsity level reflects the specified neighborhood size (k or radius); fully dense or near-empty graphs suggest parameter mismatch.
- Symmetric or expected asymmetry pattern in adjacency (depending on whether graph is mutual or directed nearest neighbors).

## Limitations

- Assumes coordinate data is continuous and exists in a 2D or 3D Euclidean space; non-Euclidean or highly non-linear spatial domains may not be well-represented.
- Radius-based neighborhoods are sensitive to absolute coordinate scale — threshold must be chosen carefully for the tissue resolution.
- k-nearest-neighbor mode creates all-or-nothing boundaries (exactly k neighbors per observation) and does not account for variable local density.
- Very high-dimensional coordinate spaces (e.g., >10 dimensions) or large datasets (>100k observations) may incur computational overhead; spatial_neighbors uses approximate nearest neighbor methods for scalability.

## Evidence

- [other] Build a spatial neighbor graph using squidpy.gr.spatial_neighbors() with radius-based neighborhood detection: "Build a spatial neighbor graph using squidpy.gr.spatial_neighbors() with radius-based neighborhood detection."
- [other] Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances': "Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances'."
- [other] Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints: "Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints (diagonal zero for distance, identity or zero for"
- [intro] Squidpy provides streamlined APIs for spatial statistics and interactive exploration, building on anndata as the underlying data structure: "Squidpy provides streamlined APIs for spatial statistics and interactive exploration, building on anndata as the underlying data structure."
- [other] Load a bundled example dataset using squidpy.datasets (e.g., datasets.visium or datasets.imc) into an AnnData object: "Load a bundled example dataset using squidpy.datasets (e.g., datasets.visium or datasets.imc) into an AnnData object."
