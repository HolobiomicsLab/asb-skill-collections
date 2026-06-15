---
name: spatial-omics-dataset-loading
description: Use when you have a spatial transcriptomics experiment (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0092
  tools:
  - scanpy
  - squidpy
  - anndata
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

# spatial-omics-dataset-loading

## Summary

Load bundled spatial transcriptomics datasets into AnnData objects using squidpy.datasets, preparing them for downstream spatial analysis workflows. This skill establishes the foundational data structure that integrates spatial coordinates, gene expression, and optional microscopy images.

## When to use

You have a spatial transcriptomics experiment (e.g., Slide-seq v2, MERFISH, or other spatial molecular assay) and need to initialize an AnnData object with spatial metadata, expression matrices, and coordinate information before applying spatial statistics, feature extraction, or visualization methods like squidpy.gr.sepal or interactive tissue exploration.

## When NOT to use

- Your spatial data is already loaded into an AnnData object with verified spatial coordinates — use this skill only for initial data ingestion from bundled sources.
- You are working with custom or private spatial datasets not available in squidpy.datasets — use alternative loaders (e.g., manual .h5ad import, custom parsing) instead.
- Your data is in a non-AnnData format (e.g., raw coordinate/expression CSV files) — preprocess to AnnData structure first or use format-specific loaders.

## Inputs

- Dataset identifier string (e.g., 'slideseqv2', 'merfish')
- Optional sample/tissue specification parameter

## Outputs

- AnnData object with expression matrix (.X)
- Spatial coordinates in .obsm['spatial'] or similar key
- Cell/spot metadata in .obs
- Gene metadata in .var
- Optionally, tissue image data in .uns

## How to apply

Call squidpy.datasets with the target dataset name (e.g., 'slideseqv2' or 'merfish') to download and instantiate a bundled spatial dataset. The function returns an AnnData object with expression data in .X, cell/spot metadata in .obs, gene metadata in .var, spatial coordinates typically stored in .obsm (e.g., 'spatial' for 2D coordinates), and optionally tissue images in .uns. Verify that the returned object contains the expected slots: non-empty .X (expression matrix), .obs with coordinate or metadata columns, .obsm with spatial key, and .uns with image or microscopy data if applicable. This initialization step is critical because downstream methods like squidpy.gr.sepal expect the spatial coordinate key and standard AnnData structure.

## Related tools

- **squidpy** (Provides squidpy.datasets function to load bundled spatial transcriptomics datasets and downstream spatial analysis APIs) — https://github.com/scverse/squidpy
- **anndata** (Defines the AnnData object structure that stores expression, spatial coordinates, and metadata)
- **scanpy** (Provides foundational single-cell analysis methods and data structure conventions inherited by squidpy)

## Examples

```
import squidpy as sq; adata = sq.datasets.slideseqv2()
```

## Evaluation signals

- Returned object is an AnnData instance with non-empty .X (expression matrix) of expected dimensions (n_obs × n_vars)
- Spatial coordinates are present in .obsm with key 'spatial' or similar, with shape (n_obs, 2) for 2D or (n_obs, 3) for 3D
- Cell/spot metadata (.obs) contains expected columns (e.g., 'cell_type', 'batch', or assay-specific fields) with correct dtypes
- Gene metadata (.var) contains expected columns (e.g., 'gene_names', 'highly_variable') matching n_vars
- Tissue image or microscopy data is present in .uns if applicable to the dataset (e.g., 'images', 'hires_image')

## Limitations

- squidpy.datasets only provides a curated set of bundled examples; users with custom or unpublished datasets must implement custom loaders.
- Coordinate systems and units (e.g., pixel coordinates vs. physical microns) vary by dataset and assay; users must verify coordinate interpretation before spatial analysis.
- Large datasets may require significant memory; users should check available RAM and consider data subsetting strategies if needed.

## Evidence

- [other] Load a bundled spatial dataset using squidpy.datasets (slideseqv2 or merfish) into an AnnData object.: "Load a bundled spatial dataset using squidpy.datasets (slideseqv2 or merfish) into an AnnData object."
- [intro] Squidpy builds on scanpy and anndata, providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images: "It builds on scanpy and anndata providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images"
- [intro] Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data.: "Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data."
