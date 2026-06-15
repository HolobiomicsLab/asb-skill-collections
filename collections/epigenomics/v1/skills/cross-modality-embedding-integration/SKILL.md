---
name: cross-modality-embedding-integration
description: Use when you have paired scATAC-seq peak matrices and scRNA-seq gene expression matrices from the same cells (multiome data) and need to perform joint clustering, visualization, or correlation analysis across both chromatin accessibility and gene expression in a single coordinate system.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3308
  tools:
  - R
  - ArchR
  - monocle3
  - Slingshot
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

# cross-modality-embedding-integration

## Summary

Integration of paired scATAC-seq chromatin accessibility and scRNA-seq gene expression data into a unified reduced-dimension embedding space using ArchR's multiome workflow. This skill enables joint analysis of epigenetic and transcriptomic modalities in the same cell population through sequential ingestion, alignment, and dimensionality reduction.

## When to use

You have paired scATAC-seq peak matrices and scRNA-seq gene expression matrices from the same cells (multiome data) and need to perform joint clustering, visualization, or correlation analysis across both chromatin accessibility and gene expression in a single coordinate system. Apply this skill when single-modality analysis is insufficient and you require integrated interpretation of regulatory and expression signals.

## When NOT to use

- Cells from scATAC-seq and scRNA-seq are not the same population or lack reliable alignment anchors
- Only single-modality data is available (scATAC-seq OR scRNA-seq, not both)
- Gene expression matrix is already embedded or summarized to a lower dimension incompatible with raw counts

## Inputs

- scATAC-seq peak feature matrix (rows=peaks, columns=cells)
- scRNA-seq gene expression feature matrix (rows=genes, columns=cells)
- Cell metadata with consistent cell identifiers across modalities

## Outputs

- ArchR project object with integrated gene expression data attached
- Unified reduced-dimension embedding (combined dimensions) integrating both modalities
- Joint iterative LSI components derived from peaks and gene expression

## How to apply

Begin by loading the scATAC-seq peak matrix and cell metadata, then call importFeatureMatrix to register the feature matrix into an ArchR project object. Next, load the scRNA-seq gene expression matrix (as a standard feature matrix) and call addGeneExpressionMatrix to append gene expression data to the same project while aligning cells across both modalities. Execute addIterativeLSI on the combined project to compute latent semantic indexing jointly across accessibility peaks and gene expression signals. Finally, call addCombinedDims to generate a unified reduced-dimension embedding that integrates both scATAC-seq and scRNA-seq signal into a single coordinate space suitable for downstream analysis (clustering, trajectory inference, or correlation studies).

## Related tools

- **ArchR** (Executes the complete multiome integration workflow via importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, and addCombinedDims functions) — https://github.com/GreenleafLab/ArchR
- **monocle3** (Optional downstream tool for trajectory analysis on the unified embedding produced by addCombinedDims)
- **Slingshot** (Optional downstream tool for trajectory analysis on the unified embedding produced by addCombinedDims)

## Examples

```
library(ArchR); proj <- importFeatureMatrix(proj, features=peakMatrix); proj <- addGeneExpressionMatrix(proj, geneExpressionMatrix); proj <- addIterativeLSI(proj); proj <- addCombinedDims(proj)
```

## Evaluation signals

- The ArchR project object contains both 'PeakMatrix' and 'GeneExpressionMatrix' assays with matching cell counts and identifiers
- addIterativeLSI completes without error and produces LSI components with non-zero variance across both modality types
- addCombinedDims successfully creates a joint embedding (typically 2D UMAP or t-SNE) where cells cluster by biological state rather than by modality origin, indicating successful integration
- Downstream analyses (e.g., cluster assignments, gene-peak correlations) show coherence between accessibility and expression signals—e.g., open peaks correspond to expressed genes in the same cluster
- Dimensionality of the combined embedding is lower than either modality alone while retaining biological signal (inspectable via silhouette width or biological marker validation)

## Limitations

- Requires strict cell alignment between scATAC-seq and scRNA-seq; misaligned or mismatched cells will corrupt the joint embedding.
- ArchR is in active beta development with potential API changes; users should verify compatibility with the master branch and check the installation documentation at www.ArchRProject.com.
- The integration is linear (LSI-based); non-linear or more flexible integration methods may be needed for highly divergent multiome modalities or complex batch effects.
- Quality of the combined embedding depends on the quality of input matrices; low-coverage or low-depth libraries in either modality will degrade joint signal.

## Evidence

- [readme] ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims: "ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims"
- [other] The paired multiome workflow in ArchR operates through a four-step process: importFeatureMatrix ingests the feature matrix, addGeneExpressionMatrix adds the scRNA-seq gene expression data, addIterativeLSI performs iterative dimensionality reduction, and addCombinedDims produces the joint reduced-dimension embedding integrating both modalities.: "importFeatureMatrix ingests the feature matrix, addGeneExpressionMatrix adds the scRNA-seq gene expression data, addIterativeLSI performs iterative dimensionality reduction, and addCombinedDims"
- [other] Load scATAC-seq peak matrix and metadata, then call importFeatureMatrix to register the feature matrix into an ArchR project object. Load scRNA-seq gene expression matrix and call addGeneExpressionMatrix to append gene expression data to the same project, aligning cells across modalities. Execute addIterativeLSI on the combined project to compute latent semantic indexing of accessibility peaks and gene expression jointly. Call addCombinedDims to generate a unified reduced-dimension embedding that integrates both scATAC-seq and scRNA-seq signal into a single coordinate space.: "Execute addIterativeLSI on the combined project to compute latent semantic indexing of accessibility peaks and gene expression jointly. Call addCombinedDims to generate a unified reduced-dimension"
- [readme] ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data.: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data"
