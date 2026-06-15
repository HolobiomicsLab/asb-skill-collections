---
name: categorical-annotation-handling-in-omics-data
description: Use when you have (1) spatial omics data loaded in AnnData format with a pre-built spatial neighbor graph (from squidpy.gr.spatial_neighbors() or similar), (2) a categorical variable in the AnnData object (e.g., cell type, tissue compartment, annotation stored as .obs or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3306
  - http://edamontology.org/topic_0625
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

# categorical-annotation-handling-in-omics-data

## Summary

Use categorical cell-type, tissue-region, or other discrete biological annotations stored in AnnData metadata to compute neighborhood enrichment statistics and assess whether spatial neighborhoods are significantly enriched or depleted for specific categories. This skill is essential for understanding spatial organization and cell-type colocalization patterns in tissue sections.

## When to use

Apply this skill when you have (1) spatial omics data loaded in AnnData format with a pre-built spatial neighbor graph (from squidpy.gr.spatial_neighbors() or similar), (2) a categorical variable in the AnnData object (e.g., cell type, tissue compartment, annotation stored as .obs or .var metadata), and (3) a research question about whether specific categories cluster together or avoid each other in space.

## When NOT to use

- Input annotation is continuous (e.g., gene expression level or spatial coordinate) rather than discrete categorical — use correlation or regression instead.
- Spatial neighbor graph has not yet been computed — build the graph first with squidpy.gr.spatial_neighbors().
- Annotation column contains too many categories (>50) or very sparse categories with <5 cells — enrichment estimates become unreliable.

## Inputs

- AnnData object with spatial coordinates
- Pre-built spatial neighbor graph (in .obsp['spatial_neighbors'] or similar)
- Categorical annotation column in .obs (e.g., cell_type, tissue_region)

## Outputs

- Enrichment score matrix stored in .uns['nhood_enrichment']
- Matrix shape: (n_categories, n_categories) with enrichment values per category pair

## How to apply

First, ensure the categorical annotation (e.g., cell type) is stored in the AnnData object's .obs dictionary as a column. Then call squidpy.gr.nhood_enrichment() with the AnnData object and specify the categorical annotation key (e.g., 'cell_type'). The function computes enrichment scores by comparing the observed frequency of each category in spatial neighborhoods against the null expectation, and stores the result matrix in .uns['nhood_enrichment']. Inspect the output matrix to identify which category pairs show significant enrichment (positive values indicate co-enrichment, negative values indicate depletion). The enrichment scores can be visualized and interpreted to reveal spatial organization principles in the tissue.

## Related tools

- **Squidpy** (Core library providing gr.nhood_enrichment() function and spatial statistics APIs for neighbor enrichment computation) — https://github.com/scverse/squidpy
- **anndata** (Data container and API for storing categorical annotations in .obs and enrichment results in .uns)
- **scanpy** (Foundation library providing AnnData structure and basic metadata handling)
- **pynndescent** (Underlying nearest-neighbor descent library used for efficient spatial neighbor graph construction) — https://github.com/lmcinnes/pynndescent

## Examples

```
import squidpy as sq; import anndata; adata = sq.datasets.visium(); sq.gr.spatial_neighbors(adata, radius=100); sq.gr.nhood_enrichment(adata, cluster_key='cell_type'); enr = adata.uns['nhood_enrichment']
```

## Evaluation signals

- Enrichment result matrix is present in .uns['nhood_enrichment'] with expected shape (n_categories × n_categories)
- Diagonal of the enrichment matrix should show positive values (self-enrichment), indicating each category is enriched within its own neighborhoods
- Matrix is symmetric or near-symmetric, reflecting bidirectional pairwise relationships between categories
- Enrichment values are bounded (typically in a reasonable statistical range such as −1 to +1 or log-odds), not inf or NaN
- Known biological co-localizations (e.g., immune cells enriched near vasculature) appear as positive off-diagonal enrichment scores

## Limitations

- Enrichment scores can be unstable for very sparse categories or those with few neighbors; results should be validated with permutation tests or sufficient sample size per category.
- The method assumes the spatial neighbor graph is already correctly built; errors in graph construction (wrong radius, wrong metric) propagate into enrichment computation.
- Enrichment analysis is sensitive to the choice of neighborhood definition (radius, k-nearest neighbors); different neighborhood parameters may yield different biological conclusions.
- High-dimensional tissue sections with multiple overlapping cell populations may show apparent enrichment due to random spatial clustering rather than true biological interaction.

## Evidence

- [other] Does squidpy's nhood_enrichment function correctly compute and store neighborhood enrichment scores in an AnnData object when applied to spatial data with a pre-built neighbor graph?: "Does squidpy's nhood_enrichment function correctly compute and store neighborhood enrichment scores in an AnnData object when applied to spatial data with a pre-built neighbor graph?"
- [other] Squidpy provides streamlined APIs for spatial statistics, which includes the capability to compute neighborhood enrichment analysis on spatial molecular data.: "Squidpy provides streamlined APIs for spatial statistics, which includes the capability to compute neighborhood enrichment analysis on spatial molecular data."
- [other] Build a spatial neighbor graph using squidpy.gr.spatial_neighbors() with radius-based neighborhood detection. Execute squidpy.gr.nhood_enrichment() on the AnnData object with a specified categorical annotation to compute neighborhood enrichment statistics.: "Build a spatial neighbor graph using squidpy.gr.spatial_neighbors() with radius-based neighborhood detection. Execute squidpy.gr.nhood_enrichment() on the AnnData object with a specified categorical"
- [other] Verify that the enrichment result is written to the AnnData object's .uns dictionary at the key 'nhood_enrichment' and inspect the output matrix structure.: "Verify that the enrichment result is written to the AnnData object's .uns dictionary at the key 'nhood_enrichment' and inspect the output matrix structure."
- [intro] providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images: "providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images"
