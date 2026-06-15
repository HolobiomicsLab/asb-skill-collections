---
name: anndata-object-manipulation-and-inspection
description: Use when after executing a Squidpy spatial analysis function (e.g., gr.spatial_neighbors, gr.nhood_enrichment, gr.sepal, im.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0637
  tools:
  - anndata
  - scanpy
  - pip
  - Squidpy
  - Python
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

# anndata-object-manipulation-and-inspection

## Summary

Programmatic inspection and modification of AnnData objects to store, retrieve, and verify spatial analysis results, graph structures, and feature matrices. This skill enables validation that computed outputs (enrichment scores, rankings, spatial neighbors, image features) are correctly written to the appropriate AnnData slots (.obsp, .obsm, .uns, .var) with expected schemas and dimensions.

## When to use

After executing a Squidpy spatial analysis function (e.g., gr.spatial_neighbors, gr.nhood_enrichment, gr.sepal, im.calculate_image_features) on an AnnData object, to verify that results have been stored in the correct attribute slots, inspect output dimensionality and structure, confirm field names match expected naming conventions, and validate that sparse matrices (adjacency, distance) or dense arrays satisfy structural constraints (sparsity patterns, diagonal properties, shape compatibility with observation count).

## When NOT to use

- Input is not an AnnData object (e.g., raw array, DataFrame, or sparse matrix without associated metadata)
- The upstream Squidpy function has not yet been called or the computation was interrupted/failed without raising an exception
- You are only interested in computing results and have no need to validate or document output schema and data structure

## Inputs

- AnnData object with coordinate data in .obsm (e.g., spatial coordinates, image coordinates)
- AnnData object with categorical annotation in .obs or .var (for enrichment analysis)
- AnnData object with pre-built graph in .obsp (for downstream statistics)
- Dask-backed computation task or lazy array reference (for image feature workflows)

## Outputs

- Verified AnnData object with spatial neighbor CSR matrices in .obsp['spatial_neighbors'] and .obsp['spatial_distances']
- Verified AnnData object with enrichment scores in .uns['nhood_enrichment'] (matrix structure)
- Verified AnnData object with gene rankings and spatial enrichment scores in .var or .uns slots
- Verified AnnData object with materialized image features in .obsm, .obsp, or .var slots
- Inspection report documenting field names, data types, dimensions, sparsity patterns, and constraint satisfaction

## How to apply

After running a Squidpy graph or feature-extraction function, systematically inspect the AnnData object's attribute dictionary slots: check .obsp for sparse graph matrices (CSR format), .obsm for dense feature matrices (e.g., image features), .var for gene-level rankings or scores, and .uns for summary dictionaries (e.g., 'nhood_enrichment', 'sepal'). For graph outputs, verify that adjacency and distance matrices are stored as CSR sparse matrices with matching shape (n_obs, n_obs), that both have identical sparsity structure, and that distance matrices respect zero-diagonal constraints while adjacency matrices follow expected set_diag behavior. For feature outputs, confirm dimensions align with the observation count (n_obs) and sample count (n_features or image spatial extent). Compare field names and data types against the function's documentation to ensure no renaming or type coercion has occurred. When dask-backed lazy computation is involved, check that intermediate results remain as dask arrays before explicit materialization/collection into the AnnData object.

## Related tools

- **anndata** (Data structure for storing spatial observations, features, metadata, and graph matrices; serves as the container inspected and validated after Squidpy computations) — https://github.com/scverse/anndata
- **Squidpy** (Spatial analysis library whose outputs are inspected and validated within AnnData object slots) — https://github.com/scverse/squidpy
- **scanpy** (Single-cell analysis library that AnnData builds upon; provides complementary inspection and manipulation utilities) — https://github.com/scverse/scanpy
- **Python** (Programming language used to write inspection and validation code)

## Examples

```
import squidpy as sq; import anndata; adata = sq.datasets.visium(); sq.gr.spatial_neighbors(adata); assert 'spatial_neighbors' in adata.obsp and 'spatial_distances' in adata.obsp; assert adata.obsp['spatial_neighbors'].shape == (adata.n_obs, adata.n_obs)
```

## Evaluation signals

- CSR sparse matrices (.obsp['spatial_neighbors'] and .obsp['spatial_distances']) have matching shape (n_obs, n_obs) where n_obs equals observation count in AnnData
- Distance matrix has zero diagonal (no self-loops) and symmetric sparsity pattern; adjacency matrix respects set_diag parameter constraint
- Enrichment result dictionary exists at .uns['nhood_enrichment'] with expected matrix dimensions (n_categories × n_categories or similar)
- Gene ranking scores and spatial enrichment statistics are present in .var or .uns with field names matching Squidpy function documentation (e.g., presence of score columns, correct dtype)
- Image feature outputs in .obsm or .obsp have dimensions compatible with observation count and image spatial extent; dask arrays materialize without error when explicitly collected

## Limitations

- Field names and slot locations depend on the specific Squidpy function and version; documentation must be consulted for each function to know where results are stored
- Lazy dask-backed computations are only partially materialized into AnnData until explicit collection is triggered; premature inspection may show dask task graphs rather than materialized arrays
- No automated schema validation is available in the provided context; inspection is manual and requires knowledge of expected output structure
- CSR sparse matrix structure and sparsity patterns are sensitive to distance metric, radius, and neighborhood parameters; constraint satisfaction depends on function-specific behavior

## Evidence

- [other] Verify that the enrichment result is written to the AnnData object's .uns dictionary at the key 'nhood_enrichment' and inspect the output matrix structure.: "Verify that the enrichment result is written to the AnnData object's .uns dictionary at the key 'nhood_enrichment' and inspect the output matrix structure."
- [other] Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances'.: "Verify that the resulting adjacency matrix and distance matrix are stored as CSR sparse matrices in adata.obsp with keys such as 'spatial_neighbors' and 'spatial_distances'."
- [other] Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints: "Check that both matrices have shape (n_obs, n_obs) matching the observation count, have matching sparsity structure, and satisfy diagonal constraints (diagonal zero for distance, identity or zero for"
- [other] Inspect the AnnData object's .var, .uns, or .obsm attributes to locate the output fields and Validate that field names and data structures match the expected schema: "Inspect the AnnData object's .var, .uns, or .obsm attributes to locate the output fields (gene rankings, spatial enrichment scores). 4. Validate that field names and data structures match the"
- [intro] It builds on scanpy and anndata, from which it inherits modularity and scalability: "It builds on scanpy and anndata, from which it inherits modularity and scalability."
- [other] Verify intermediate computation results remain as dask arrays before materialization. 5. Trigger collection/materialization of dask arrays into the AnnData object: "Verify intermediate computation results remain as dask arrays before materialization. 5. Trigger collection/materialization of dask arrays into the AnnData object and confirm feature outputs are"
