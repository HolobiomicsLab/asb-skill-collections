---
name: neighborhood-enrichment-computation
description: Use when when you have spatial transcriptomics or imaging data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0769
  tools:
  - Squidpy
  - anndata
  - scanpy
  - pynndescent
derived_from:
- doi: 10.1038/s41592-021-01358-2
  title: squidpy
evidence_spans: []
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

# neighborhood-enrichment-computation

## Summary

Compute neighborhood enrichment scores for categorical cell annotations in spatial omics data using pre-built neighbor graphs. This identifies statistically enriched or depleted cell types in spatial neighborhoods, revealing local tissue organization and cell-type co-localization patterns.

## When to use

When you have spatial transcriptomics or imaging data (e.g., Visium, MERFISH) with a pre-constructed spatial neighbor graph and categorical cell-type or cluster annotations, and you wish to quantify whether specific cell types are significantly overrepresented or underrepresented in the spatial neighborhoods of other cell types.

## When NOT to use

- Spatial neighbor graph has not yet been computed—use spatial_neighbors() first to build the graph.
- Categorical annotation is continuous or lacks discrete cell-type labels; enrichment requires discrete group membership.
- Spatial coordinates are missing or the dataset lacks inherent spatial structure (e.g., dissociated single-cell data without spatial recovery).

## Inputs

- AnnData object with spatial coordinates in .obsm['spatial']
- Pre-built spatial neighbor graph (adjacency matrix or neighbor indices)
- Categorical annotation column in .obs (e.g., cell type labels)

## Outputs

- Enrichment matrix in .uns['nhood_enrichment']
- Enrichment scores (log-odds ratio or z-score per cell-type pair)
- Statistical test results (p-values if applicable)

## How to apply

Load your spatial omics dataset into an AnnData object and construct a radius-based spatial neighbor graph using squidpy.gr.spatial_neighbors() with appropriate radius parameter for your technology (e.g., 100 µm for Visium). Then execute squidpy.gr.nhood_enrichment() with your categorical annotation column (e.g., cell type labels) to compute neighborhood enrichment statistics. The function performs statistical testing (typically log-odds ratio or z-score based) comparing observed vs. expected cell-type co-localization patterns. Results are stored in .uns['nhood_enrichment'] as a matrix where rows are source cell types, columns are target cell types, and values represent enrichment significance. Interpret positive values as enrichment (overrepresentation) and negative values as depletion (underrepresentation) of the target cell type in neighborhoods of the source type.

## Related tools

- **Squidpy** (Primary API for neighborhood enrichment computation; provides gr.nhood_enrichment() function and spatial graph construction via gr.spatial_neighbors()) — https://github.com/scverse/squidpy
- **anndata** (Data structure container; stores spatial coordinates, neighbor graphs, annotations, and enrichment results in standardized .obs, .obsm, .uns, and .obsp attributes)
- **scanpy** (Underlying framework for graph construction and statistical computations; inherited by Squidpy for modularity and scalability)
- **pynndescent** (Optional nearest-neighbor search engine for accelerated spatial graph construction when building neighbor graphs) — https://github.com/lmcinnes/pynndescent

## Examples

```
import squidpy as sq; adata = sq.datasets.visium(); sq.gr.spatial_neighbors(adata); sq.gr.nhood_enrichment(adata, cluster_key='cluster'); enrichment_matrix = adata.uns['nhood_enrichment']
```

## Evaluation signals

- Enrichment matrix is present in .uns['nhood_enrichment'] with shape (n_cell_types, n_cell_types) and contains finite numeric values
- Enrichment scores span a reasonable range (e.g., -2 to +2 for z-scores, or similar for log-odds ratios) without extreme outliers suggesting numerical failure
- Diagonal values (self-enrichment) are typically positive and higher than off-diagonal values, indicating cells are enriched in neighborhoods of their own type
- Symmetry or asymmetry of the enrichment matrix aligns with biological expectations (e.g., mutual enrichment between epithelial and stromal niches may be asymmetric)
- Results are reproducible when re-run on the same dataset with identical parameters and random seed

## Limitations

- Enrichment scores depend critically on the choice of radius or k for neighbor graph construction; changing spatial neighborhood definition changes results.
- Statistical power is reduced for rare cell types with few instances, leading to unstable or unreliable enrichment estimates.
- Categorical annotations must be discrete and non-overlapping; fuzzy or probabilistic cell-type labels require preprocessing to hard assignments.
- Results reflect correlation (co-localization patterns) not causation; enrichment does not imply functional interaction or direct biological dependency.

## Evidence

- [other] Execute squidpy.gr.nhood_enrichment() on the AnnData object with a specified categorical annotation to compute neighborhood enrichment statistics.: "Execute squidpy.gr.nhood_enrichment() on the AnnData object with a specified categorical annotation to compute neighborhood enrichment statistics."
- [other] Build a spatial neighbor graph using squidpy.gr.spatial_neighbors() with radius-based neighborhood detection.: "Build a spatial neighbor graph using squidpy.gr.spatial_neighbors() with radius-based neighborhood detection."
- [other] Verify that the enrichment result is written to the AnnData object's .uns dictionary at the key 'nhood_enrichment' and inspect the output matrix structure.: "Verify that the enrichment result is written to the AnnData object's .uns dictionary at the key 'nhood_enrichment' and inspect the output matrix structure."
- [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images: "Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images"
- [intro] It builds on scanpy and anndata: "It builds on scanpy and anndata"
