---
name: archr-project-manipulation
description: 'Use when you have a processed ArchR project object (containing peak calls, cell barcodes, and quality control metadata) and need to: (1) reduce dimensionality of the peak matrix via iterative LSI; (2) integrate multimodal data by combining ATAC and RNA dimensions;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3179
  tools:
  - ArchR
  - R
  - monocle3
  - Slingshot
  - STREAM
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

# ArchR Project Manipulation

## Summary

Load, transform, and annotate single-cell ATAC-seq ArchR project objects using core functions like addIterativeLSI, addCombinedDims, and export routines. This skill enables reproducible manipulation of processed peak matrices and cell metadata for downstream trajectory and multimodal analysis.

## When to use

You have a processed ArchR project object (containing peak calls, cell barcodes, and quality control metadata) and need to: (1) reduce dimensionality of the peak matrix via iterative LSI; (2) integrate multimodal data by combining ATAC and RNA dimensions; (3) prepare the peak matrix for export to external trajectory tools (Monocle3, Slingshot, STREAM); or (4) add gene expression matrices from paired scRNA-seq experiments.

## When NOT to use

- Raw, unprocessed sequencing data (use ArchR QC functions first)
- If peak matrix has already been exported to another format and you do not need to re-integrate ArchR metadata or trajectory results
- If no paired scRNA-seq is available and gene expression integration is the sole goal

## Inputs

- ArchR project object (processed, with peak calls and cell annotations)
- Optional: scRNA-seq feature matrix (gene × cell counts)
- Optional: trajectory analysis method selection (character: 'monocle3' or 'slingshot')

## Outputs

- Modified ArchR project object (with LSI, combined dimensions, trajectory embedding, or gene expression matrix added)
- Peak-by-cell matrix file in STREAM-compatible format (CSV or TSV)
- Trajectory embedding coordinates (stored in ArchR project metadata)

## How to apply

Load the ArchR project object in R. If you have a paired scRNA-seq dataset, use importFeatureMatrix to ingest gene expression counts, then addGeneExpressionMatrix to integrate into the ArchR project. Run addIterativeLSI on the peak matrix to compute iterative LSI dimensionality reduction, which produces latent semantic components suitable for visualization and downstream analysis. If integrating both ATAC and RNA modalities, use addCombinedDims to create a joint embedding. For trajectory analysis, conditionally invoke addMonocleTrajectory (Monocle3) or addSlingShotTrajectories (Slingshot) based on user selection. For export to STREAM, invoke exportPeakMatrixForSTREAM to write the peak-by-cell matrix in STREAM-compatible CSV or TSV format. Verify that the project object is returned with updated assays and metadata slots reflecting each operation.

## Related tools

- **ArchR** (Core R package for loading, manipulating, and exporting single-cell ATAC-seq project objects with integrated trajectory and multimodal analysis functions) — https://github.com/GreenleafLab/ArchR
- **monocle3** (Optional downstream trajectory analysis algorithm conditionally invoked via addMonocleTrajectory)
- **Slingshot** (Optional alternative trajectory analysis algorithm conditionally invoked via addSlingShotTrajectories)
- **STREAM** (External trajectory tool that receives peak matrix exports via exportPeakMatrixForSTREAM)
- **R** (Runtime environment for executing ArchR package functions)

## Examples

```
library(ArchR); proj <- loadArchRProject('path/to/project'); proj <- addIterativeLSI(proj, useMatrix='TileMatrix', name='LSI'); exportPeakMatrixForSTREAM(proj, outputFile='peak_matrix_stream.csv')
```

## Evaluation signals

- ArchR project object returned contains non-empty 'iterativeLSI' or 'LSI' assay after addIterativeLSI is called
- Combined dimensions assay is populated in the project metadata after addCombinedDims (verifiable via getReducedDims or similar accessor)
- Exported STREAM file is valid CSV/TSV with peak rows, cell columns, and numeric accessibility/count values
- Trajectory embedding coordinates are present in the project object and have expected dimensionality (typically 2D or 3D) after addMonocleTrajectory or addSlingShotTrajectories
- Gene expression matrix dimensions (genes × cells) match the barcode set in the ArchR project after addGeneExpressionMatrix

## Limitations

- ArchR is in active beta development; some functions may change in interface or behavior between releases
- addIterativeLSI and addCombinedDims require sufficient memory and disk I/O; very large projects (>1M cells) may require tuning of LSI parameters (nIterations, seed) for stability
- Trajectory functions (addMonocleTrajectory, addSlingShotTrajectories) require pre-existing clusters or cell type annotations; results are sensitive to clustering quality
- exportPeakMatrixForSTREAM produces a single sparse or dense matrix; alternative export formats (HDF5, Loom) are not covered by this skill

## Evidence

- [readme] ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data.: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data."
- [readme] ArchR now supports paired scATAC-seq and scRNA-seq Analysis with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, and addCombinedDims: "ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims"
- [readme] ArchR directly supports both monocle3 and Slingshot based trajectory analysis with getMonocleTrajectories, addMonocleTrajectory, addSlingShotTrajectories: "ArchR now directly supports both monocle3 and Slingshot based trajectory analysis! See updates with getMonocleTrajectories, addMonocleTrajectory, addSlingShotTrajectories"
- [readme] ArchR enables export of a peak matrix that is compatible with STREAM via exportPeakMatrixForSTREAM: "ArchR now enables export of a peak matrix that is compatible with STREAM! See updates with exportPeakMatrixForSTREAM"
- [other] Call exportPeakMatrixForSTREAM on the ArchR project to generate a peak-by-cell matrix formatted for STREAM compatibility, writing to CSV or TSV.: "Call exportPeakMatrixForSTREAM on the ArchR project to generate a peak-by-cell matrix formatted for STREAM compatibility. Write the resulting matrix to a file in STREAM-compatible format (typically"
