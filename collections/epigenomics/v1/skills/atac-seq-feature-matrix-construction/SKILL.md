---
name: atac-seq-feature-matrix-construction
description: Use when when you have processed scATAC-seq data (peak calling complete, cell-barcode matrix generated) and need to register it into ArchR for downstream multiome analysis alongside scRNA-seq gene expression data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0625
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

# atac-seq-feature-matrix-construction

## Summary

Construction and ingestion of scATAC-seq peak accessibility matrices into a unified project object for joint multiome analysis. This skill enables alignment of chromatin accessibility data with paired gene expression matrices to produce integrated reduced-dimension embeddings.

## When to use

When you have processed scATAC-seq data (peak calling complete, cell-barcode matrix generated) and need to register it into ArchR for downstream multiome analysis alongside scRNA-seq gene expression data. Specifically, apply this skill when initiating a paired scATAC-seq and scRNA-seq analysis workflow and the peak matrix has not yet been loaded into an ArchR project object.

## When NOT to use

- Input is already an ArchR project object with feature matrix loaded — use addGeneExpressionMatrix directly instead
- Peak matrix has not been quality-filtered or called — first perform peak calling and barcode filtering upstream
- Cell barcodes between scATAC-seq and scRNA-seq samples do not align or originate from different cell populations — resolve barcode mapping before import

## Inputs

- scATAC-seq peak-by-cell matrix (sparse or dense format)
- Cell metadata (barcodes, sample IDs, cluster assignments)
- ArchR project object (new or existing)

## Outputs

- ArchR project object with registered peak accessibility matrix
- Internal feature matrix representation aligned to cell barcodes
- Project metadata structure ready for multiome integration

## How to apply

Load your scATAC-seq peak matrix (rows = peaks, columns = cells with barcodes) and associated metadata (cell clusters, sample annotations) into R. Call importFeatureMatrix to register the feature matrix into a new or existing ArchR project object, which creates a standardized internal representation. The function ingests the peak-by-cell matrix and aligns cell identifiers across modalities. Verify that cells are successfully registered by checking project dimensionality and cell count. Once importFeatureMatrix completes, proceed to addGeneExpressionMatrix to append the scRNA-seq gene expression matrix to the same project, ensuring barcode alignment between modalities.

## Related tools

- **ArchR** (R package providing importFeatureMatrix function for ingesting scATAC-seq peak matrices and managing integrated multiome project objects) — https://github.com/GreenleafLab/ArchR

## Examples

```
importFeatureMatrix(ArrowFiles = arrow_files, seqnames = 'chr1')
```

## Evaluation signals

- ArchR project object is successfully created with non-zero cell count matching input matrix columns
- Cell barcodes in the registered project match input metadata exactly (no barcode collisions or loss)
- Feature matrix dimensions (peaks × cells) are preserved and accessible via project accessor methods
- importFeatureMatrix completes without barcode alignment errors or dropped cells
- Subsequent addGeneExpressionMatrix call can align scRNA-seq data to the same project without barcode mismatch errors

## Limitations

- importFeatureMatrix requires cell barcodes to be consistent across scATAC-seq and scRNA-seq inputs; mismatched or malformed barcodes will cause silent cell loss
- ArchR is currently in beta; active development may introduce API changes between versions
- The function does not perform quality control on the peak matrix itself — low-quality peaks or doublet-contaminated cells should be filtered before import
- Memory requirements scale with peak-by-cell matrix size; 1 million cells may require substantial RAM despite ArchR's efficiency claims

## Evidence

- [intro] importFeatureMatrix function for peak matrix ingestion: "importFeatureMatrix ingests the feature matrix, addGeneExpressionMatrix adds the scRNA-seq gene expression data"
- [intro] Four-step paired multiome workflow structure: "Load scATAC-seq peak matrix and metadata, then call importFeatureMatrix to register the feature matrix into an ArchR project object"
- [readme] ArchR supports paired scATAC-seq and scRNA-seq analysis: "ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims"
- [readme] ArchR multiome tutorial reference: "For a brief tutorial of these features : https://greenleaflab.github.io/ArchR_2020/Ex-Analyze-Multiome.html"
