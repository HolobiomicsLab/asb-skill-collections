---
name: multiome-data-ingestion-paired-modalities
description: Use when you have independently generated or received both scATAC-seq peak count matrices and scRNA-seq gene expression matrices from the same set of cells (multiome experiment), and you need to perform joint analysis such as co-clustering, trajectory inference, or regulatory inference that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3170
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

# Multiome Data Ingestion for Paired Modalities

## Summary

Ingest and align paired scATAC-seq chromatin accessibility and scRNA-seq gene expression data into a unified ArchR project object, establishing the foundation for joint downstream analysis. This skill bridges two single-cell modalities by registering feature matrices and gene expression data in the same coordinate space before dimensionality reduction.

## When to use

You have independently generated or received both scATAC-seq peak count matrices and scRNA-seq gene expression matrices from the same set of cells (multiome experiment), and you need to perform joint analysis such as co-clustering, trajectory inference, or regulatory inference that requires both accessibility and expression signals in the same reduced-dimension space.

## When NOT to use

- Input cells come from different experiments or individuals — alignment across modalities requires shared cell identity
- Gene expression matrix is already a pre-computed embedding or dimensionality-reduced object rather than a raw/normalized count matrix
- You only have data from one modality (scATAC-seq or scRNA-seq alone) — this skill specifically requires paired data

## Inputs

- scATAC-seq peak count matrix (cells × peaks)
- scATAC-seq cell metadata (barcodes, cluster assignments, quality metrics)
- scRNA-seq gene expression matrix (cells × genes, typically log-normalized counts)
- scRNA-seq cell barcodes or metadata aligned to scATAC-seq cells

## Outputs

- ArchR project object with both scATAC-seq and scRNA-seq data registered
- Joint reduced-dimension embedding (addCombinedDims output)
- Integrated latent semantic indexing model across both modalities

## How to apply

Begin by loading the scATAC-seq peak matrix and associated metadata, then call importFeatureMatrix to register the peak feature matrix into an ArchR project object. Next, load the scRNA-seq gene expression matrix (as a feature matrix) and call addGeneExpressionMatrix to append gene expression data to the same project, aligning cells across modalities by cell barcode. Execute addIterativeLSI on the combined project to jointly compute latent semantic indexing over both accessibility peaks and gene expression counts. Finally, call addCombinedDims to generate a unified reduced-dimension embedding that integrates both scATAC-seq and scRNA-seq signal into a single coordinate space suitable for downstream analysis.

## Related tools

- **ArchR** (Primary R package that provides importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, and addCombinedDims functions for multiome data ingestion and integration) — https://github.com/GreenleafLab/ArchR
- **monocle3** (Optional downstream tool for trajectory analysis on the combined multiome embedding produced by addCombinedDims)
- **Slingshot** (Optional downstream tool for trajectory inference on the integrated multiome reduced-dimension space)

## Examples

```
# Load library and create ArchR project with scATAC-seq
library(ArchR)
proj <- ArchRProject(inputFiles = "fragments.tsv.gz", outputDirectory = "ArchRProject")
# Ingest scRNA-seq gene expression matrix
proj <- addGeneExpressionMatrix(input = proj, seRNA = geneExpressionMatrix)
# Perform joint latent semantic indexing
proj <- addIterativeLSI(ArchRProj = proj, useMatrix = "TileMatrix", name = "LSI_Combined")
# Generate unified reduced-dimension embedding
proj <- addCombinedDims(ArchRProj = proj, reducedDims = "LSI_Combined")
```

## Evaluation signals

- The resulting ArchR project object contains both scATAC-seq and scRNA-seq data without errors or data loss; verify via getAvailableMatrices()
- Cell barcodes are properly aligned across modalities — each cell in the project has both accessibility and expression measurements
- The addCombinedDims output produces a single coordinate system (e.g., UMAP or t-SNE) where cells cluster coherently by both modality signals, not dominated by one
- The joint reduced-dimension embedding can serve as input to downstream analysis (trajectory, clustering, regulatory inference) without requiring additional alignment steps
- No cells are dropped or duplicated during the ingestion pipeline; cell count is consistent across importFeatureMatrix → addGeneExpressionMatrix → addIterativeLSI → addCombinedDims

## Limitations

- Cell barcode alignment is exact — if barcodes differ slightly between scATAC-seq and scRNA-seq (e.g., due to demultiplexing artifacts), manual harmonization is required before ingestion
- ArchR is optimized for scATAC-seq; scRNA-seq ingestion via addGeneExpressionMatrix is best used as a complementary modality rather than for primary gene expression analysis
- The addIterativeLSI and addCombinedDims steps assume reasonable data quality from both modalities; highly noisy or low-depth data in one modality may distort the joint embedding

## Evidence

- [other] The paired multiome workflow in ArchR operates through a four-step process: importFeatureMatrix ingests the feature matrix, addGeneExpressionMatrix adds the scRNA-seq gene expression data, addIterativeLSI performs iterative dimensionality reduction, and addCombinedDims produces the joint reduced-dimension embedding integrating both modalities.: "The paired multiome workflow in ArchR operates through a four-step process: importFeatureMatrix ingests the feature matrix, addGeneExpressionMatrix adds the scRNA-seq gene expression data,"
- [readme] ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims: "ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims"
- [other] Load scATAC-seq peak matrix and metadata, then call importFeatureMatrix to register the feature matrix into an ArchR project object. Load scRNA-seq gene expression matrix and call addGeneExpressionMatrix to append gene expression data to the same project, aligning cells across modalities.: "Load scATAC-seq peak matrix and metadata, then call importFeatureMatrix to register the feature matrix into an ArchR project object. Load scRNA-seq gene expression matrix and call"
- [other] Execute addIterativeLSI on the combined project to compute latent semantic indexing of accessibility peaks and gene expression jointly. Call addCombinedDims to generate a unified reduced-dimension embedding that integrates both scATAC-seq and scRNA-seq signal into a single coordinate space.: "Execute addIterativeLSI on the combined project to compute latent semantic indexing of accessibility peaks and gene expression jointly. Call addCombinedDims to generate a unified reduced-dimension"
- [readme] ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data.: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data."
