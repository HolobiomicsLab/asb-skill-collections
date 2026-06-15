---
name: rna-seq-expression-alignment-across-cells
description: Use when you have paired scATAC-seq and scRNA-seq data from the same cells (multiome experiment) and want to perform integrated analysis that leverages both chromatin accessibility and gene expression signals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3308
  tools:
  - R
  - ArchR
derived_from:
- doi: 10.1038/s41588-021-00790-6
  title: archr
evidence_spans:
- ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_archr
    doi: 10.1038/s41588-021-00790-6
    title: archr
  dedup_kept_from: coll_archr
schema_version: 0.2.0
---

# rna-seq-expression-alignment-across-cells

## Summary

Integrate scRNA-seq gene expression data with scATAC-seq chromatin accessibility data in ArchR by aligning cells across modalities and creating a unified reduced-dimension embedding. This skill enables joint analysis of paired multiome datasets where the same cells have been profiled for both gene expression and chromatin accessibility.

## When to use

You have paired scATAC-seq and scRNA-seq data from the same cells (multiome experiment) and want to perform integrated analysis that leverages both chromatin accessibility and gene expression signals. This is appropriate when you need to correlate regulatory DNA accessibility with transcriptional output in a unified coordinate space.

## When NOT to use

- Data are unpaired — scATAC-seq and scRNA-seq were generated from different cell populations or tissues.
- Cell identifiers do not match across modalities or alignment is ambiguous.
- You only have scATAC-seq data without accompanying scRNA-seq gene expression.

## Inputs

- scATAC-seq peak matrix with metadata
- scRNA-seq gene expression matrix
- Aligned cell identifiers across modalities
- ArchR project object

## Outputs

- ArchR project with integrated gene expression data
- Joint reduced-dimension embedding (combined dims)
- Unified single-cell coordinate space for both modalities

## How to apply

Load the scATAC-seq peak matrix into an ArchR project object using importFeatureMatrix. Next, load the scRNA-seq gene expression matrix and append it to the same project using addGeneExpressionMatrix, which aligns cells across both modalities based on cell identifiers. Execute addIterativeLSI on the combined project to compute latent semantic indexing jointly on accessibility peaks and gene expression. Finally, call addCombinedDims to generate a single reduced-dimension embedding that integrates both scATAC-seq and scRNA-seq signal into a unified coordinate space for downstream integrated clustering, visualization, and interpretation.

## Related tools

- **ArchR** (Core framework for ingesting, aligning, and integrating paired scATAC-seq and scRNA-seq multiome data via importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, and addCombinedDims functions) — https://github.com/GreenleafLab/ArchR
- **R** (Programming language in which ArchR is implemented and invoked)

## Examples

```
library(ArchR); proj <- importFeatureMatrix(ArrowFiles = 'atac.arrow', seqnames = 'hg38'); proj <- addGeneExpressionMatrix(input = proj, seExpressionMatrix = gex_matrix); proj <- addIterativeLSI(ArchRProj = proj, useMatrix = 'TileMatrix', name = 'LSI'); proj <- addCombinedDims(ArchRProj = proj, reduction = 'LSI', name = 'Combined')
```

## Evaluation signals

- ArchR project object successfully contains both scATAC-seq and scRNA-seq data layers with no errors during addGeneExpressionMatrix execution.
- Cell count and identifiers are consistent across both modalities after alignment (inspect via project metadata and dimension).
- addIterativeLSI completes without errors, indicating successful joint dimensionality reduction on combined accessibility and expression data.
- addCombinedDims produces a valid reduced-dimension embedding; verify by checking that the combined dims slot exists in the ArchR project and has expected dimensionality (typically 2D or 3D for visualization).
- Visualization of the unified embedding (e.g., UMAP or t-SNE of combined dims) shows coherent clustering that reflects both accessibility and expression structure, with distinct cell populations separated in the joint space.

## Limitations

- Cell alignment requires matching identifiers across scATAC-seq and scRNA-seq datasets; mismatched or missing identifiers will cause alignment failure.
- The skill assumes cells are truly paired (same biological cells profiled by both modalities); if cells are only partially overlapping, alignment will succeed but the unified embedding may reflect an incomplete overlap.
- ArchR is currently in beta; the README notes active development through peer review, which may result in API changes or instability in multiome functions.

## Evidence

- [readme] importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims: "ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims"
- [other] Four-step multiome workflow with cell alignment: "Load scATAC-seq peak matrix and metadata, then call importFeatureMatrix to register the feature matrix into an ArchR project object. Load scRNA-seq gene expression matrix and call"
- [other] Joint dimensionality reduction and unified embedding: "Execute addIterativeLSI on the combined project to compute latent semantic indexing of accessibility peaks and gene expression jointly. Call addCombinedDims to generate a unified reduced-dimension"
- [readme] ArchR full-featured scATAC-seq package: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data."
