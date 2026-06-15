---
name: spatial-statistics-interpretation
description: Use when when you have a spatial molecular dataset (e.g., Visium, MERFISH) with categorical cell-type or feature annotations and want to test whether specific categories are preferentially located near or away from each other in tissue space, beyond what random spatial distribution would predict.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0091
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

# spatial-statistics-interpretation

## Summary

Compute and interpret neighborhood enrichment scores for categorical annotations in spatial omics data by building a spatial neighbor graph and applying statistical tests to identify which cell types or features are spatially co-enriched or depleted relative to their global frequencies.

## When to use

When you have a spatial molecular dataset (e.g., Visium, MERFISH) with categorical cell-type or feature annotations and want to test whether specific categories are preferentially located near or away from each other in tissue space, beyond what random spatial distribution would predict. Neighborhood enrichment reveals tissue organization and cell-type spatial relationships.

## When NOT to use

- Input data lacks spatial coordinates or neighbor graph (run spatial_neighbors() first).
- Categorical annotation is missing or contains >95% of cells in a single category (no meaningful co-enrichment patterns).
- Sample size is very small (<100 cells) per category, yielding unstable enrichment estimates.
- You need to assess continuous features (e.g., gene expression intensity) instead of discrete categories—use continuous spatial statistics instead.

## Inputs

- AnnData object with spatial coordinates (adata.obsm['spatial'] or equivalent)
- Pre-built spatial neighbor graph (adata.obsp containing adjacency or distances)
- Categorical annotation column in adata.obs (e.g., cell_type, cluster)

## Outputs

- Enrichment score matrix stored in adata.uns['nhood_enrichment']
- Rows and columns indexed by unique categories in the annotation
- Cell values representing enrichment/depletion statistics (z-scores or log-odds)

## How to apply

First, load your spatial dataset into an AnnData object and build a spatial neighbor graph using squidpy.gr.spatial_neighbors() with radius-based or k-NN neighborhood detection. Then apply squidpy.gr.nhood_enrichment() specifying a categorical annotation (e.g., cell type or condition) to compute enrichment statistics that test whether observed co-occurrence frequencies in neighborhoods differ significantly from expected values under a null model. The result is stored in .uns['nhood_enrichment'] as a matrix of enrichment scores (typically z-scores or log-fold-change) indexed by category pairs. Interpret positive values as categories that co-localize more than expected and negative values as repulsion. Verify statistical significance (typically p < 0.05) and effect size thresholds appropriate to your biological question before drawing conclusions about tissue architecture.

## Related tools

- **Squidpy** (Provides spatial neighbor graph construction and neighborhood enrichment statistical testing functions) — https://github.com/scverse/squidpy
- **anndata** (Data structure for storing spatial coordinates, annotations, and enrichment results as AnnData.obs and .uns)
- **scanpy** (Provides data preprocessing and annotation workflows that feed into spatial statistics)
- **pynndescent** (Underlying library for efficient k-NN graph construction in spatial_neighbors()) — https://github.com/lmcinnes/pynndescent

## Examples

```
import squidpy as sq
import anndata as ad
adata = sq.datasets.visium()
sq.gr.spatial_neighbors(adata, radius=50)
sq.gr.nhood_enrichment(adata, cluster_key='cluster')
print(adata.uns['nhood_enrichment'])
```

## Evaluation signals

- Enrichment result is successfully written to adata.uns['nhood_enrichment'] with shape (n_categories, n_categories)
- Enrichment scores are symmetric (category A vs B equals B vs A) or appropriately oriented based on method
- Score magnitude is bounded (e.g., z-scores within ±10 for typical biological samples)
- Statistical p-values or q-values are computed and stored alongside scores; FDR-corrected significance threshold (typically q < 0.05) shows meaningful enrichment patterns
- Categorical distributions of enriched vs. depleted pairs are concordant with known or expected tissue organization (validated by domain experts or visualization overlays)

## Limitations

- Enrichment depends critically on choice of neighborhood radius or k-NN parameter; results may vary substantially with parameter tuning.
- Method assumes independence of neighborhoods, which is violated in dense tissues; local spatial autocorrelation can inflate false positives.
- Categorical imbalance (e.g., 90% of cells are type A, 5% type B) biases enrichment estimates toward dominant categories.
- Enrichment does not establish directionality or causality—high co-enrichment may reflect shared niche preference rather than cell–cell interaction.

## Evidence

- [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images: "providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images"
- [other] Build a spatial neighbor graph using squidpy.gr.spatial_neighbors() with radius-based neighborhood detection, then execute squidpy.gr.nhood_enrichment() on the AnnData object with a specified categorical annotation to compute neighborhood enrichment statistics: "Build a spatial neighbor graph using squidpy.gr.spatial_neighbors() with radius-based neighborhood detection. 3. Execute squidpy.gr.nhood_enrichment() on the AnnData object with a specified"
- [other] Verify that the enrichment result is written to the AnnData object's .uns dictionary at the key 'nhood_enrichment' and inspect the output matrix structure: "Verify that the enrichment result is written to the AnnData object's .uns dictionary at the key 'nhood_enrichment' and inspect the output matrix structure."
- [other] Squidpy provides streamlined APIs for spatial statistics, which includes the capability to compute neighborhood enrichment analysis on spatial molecular data: "Squidpy provides streamlined APIs for spatial statistics, which includes the capability to compute neighborhood enrichment analysis on spatial molecular data."
