---
name: spatial-gene-ranking-computation
description: Use when when working with spatial transcriptomics datasets (e.g., Slide-seq v2, MERFISH) stored in AnnData format and you need to identify genes whose expression shows significant spatial patterns or enrichment within tissue regions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0203
  tools:
  - scanpy
  - Squidpy
  - anndata
  - pynndescent
derived_from:
- doi: 10.1038/s41592-021-01358-2
  title: squidpy
evidence_spans:
- It builds on scanpy and anndata
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

# Spatial Gene Ranking Computation

## Summary

Compute spatial enrichment patterns and gene ranking scores using squidpy.gr.sepal on spatial transcriptomics data, integrating spatial statistics directly into AnnData objects. This skill enables identification of genes with significant spatial localization patterns in tissue sections.

## When to use

When working with spatial transcriptomics datasets (e.g., Slide-seq v2, MERFISH) stored in AnnData format and you need to identify genes whose expression shows significant spatial patterns or enrichment within tissue regions. Apply this skill when your research question requires ranking genes by their spatial statistics rather than univariate expression levels alone.

## When NOT to use

- Input data lacks spatial coordinates or coordinate metadata is missing/corrupted—sepal requires valid (x, y) positions for every observation
- Working with non-spatial single-cell or bulk RNA-seq data where spatial relationships are undefined or irrelevant
- Gene expression matrix is already pre-ranked by alternative spatial statistics—applying sepal would duplicate effort without additional biological insight

## Inputs

- AnnData object containing spatial transcriptomics data with expression matrix and spatial coordinates
- Gene expression counts matrix (genes × cells/spots)
- Spatial coordinate annotations (x, y coordinates per observation)

## Outputs

- AnnData.var: gene ranking scores and metadata columns
- AnnData.uns: spatial enrichment parameters and metadata
- AnnData.obsm: enrichment score matrices (optional, depending on method)
- Gene ranking table with spatial statistics

## How to apply

Load a spatial transcriptomics dataset into an AnnData object using squidpy.datasets (e.g., slideseqv2 or merfish). Execute squidpy.gr.sepal with default or specified parameters to compute spatial enrichment scores and attach gene ranking metadata to the AnnData object. The function integrates spatial coordinates with gene expression to produce ranking columns and score matrices. Inspect the resulting AnnData object's .var, .uns, or .obsm attributes to extract computed rankings and enrichment scores. Validate output by confirming expected field names, data types, dimensionality, and presence of ranking columns in the appropriate AnnData slots before downstream analysis.

## Related tools

- **Squidpy** (Primary framework providing gr.sepal function for spatial enrichment computation and gene ranking) — https://github.com/scverse/squidpy
- **scanpy** (Core dependency for single-cell/spatial analysis utilities and AnnData manipulation)
- **anndata** (Data structure for storing expression matrices, spatial coordinates, and computed rankings in a unified object)
- **pynndescent** (Approximate nearest neighbor search library used internally by squidpy for spatial graph construction) — https://github.com/lmcinnes/pynndescent

## Examples

```
import squidpy as sq; import scanpy as sc; adata = sq.datasets.slideseqv2(); sq.gr.sepal(adata); print(adata.var.head())
```

## Evaluation signals

- Presence of expected gene ranking columns in AnnData.var (e.g., gene score, rank index, enrichment p-value)
- Ranking score matrix dimensions match input gene count (n_genes) and spatial statistics computed correctly
- All gene identifiers in output match input AnnData.var_names with no missing or duplicated entries
- Spatial enrichment scores fall within expected numerical ranges (e.g., 0–1 for normalized scores, reasonable p-values for statistical tests)
- AnnData object structure remains valid and downstream analyses (e.g., filtering by top-ranked genes) execute without errors

## Limitations

- sepal performance scales with dataset size—very large spatial datasets (>1M spots) may require subsampling or parallelization strategies not covered in the core API
- Results depend on spatial graph construction parameters (e.g., neighborhood size); sensitivity analysis across parameters is recommended but not automated
- Gene ranking reflects spatial localization patterns but does not account for technical confounds (e.g., tissue heterogeneity, batch effects) unless pre-normalized
- No built-in changelog or versioning guidance provided in the article—users should verify API stability across squidpy releases before production pipelines

## Evidence

- [other] squidpy.gr.sepal successfully compute spatial statistics and attach gene ranking scores to an AnnData object with the expected field names when applied to spatial transcriptomics datasets: "Does squidpy.gr.sepal successfully compute spatial statistics and attach gene ranking scores to an AnnData object"
- [intro] Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images: "Squidpy provides streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images"
- [other] Execute squidpy.gr.sepal with default or specified parameters to compute spatial enrichment patterns and gene scores: "Execute squidpy.gr.sepal with default or specified parameters to compute spatial enrichment patterns and gene scores"
- [other] Inspect the AnnData object's .var, .uns, or .obsm attributes to locate the output fields (gene rankings, spatial enrichment scores): "Inspect the AnnData object's .var, .uns, or .obsm attributes to locate the output fields (gene rankings, spatial enrichment scores)"
- [intro] It builds on scanpy and anndata: "It builds on scanpy and anndata"
