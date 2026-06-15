---
name: single-cell-atac-seq-dimensionality-reduction
description: Use when after loading and preprocessing raw scATAC-seq data into an ArchR project object when you need to compute low-dimensional embeddings for clustering, UMAP/tSNE visualization, or integrated multi-omic analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0091
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

# single-cell-atac-seq-dimensionality-reduction

## Summary

Reduce the dimensionality of scATAC-seq data using iterative latent semantic indexing (LSI) in ArchR to enable downstream clustering, visualization, and trajectory analysis. This skill is essential for handling the high-dimensional, sparse peak-by-cell matrices typical of single-cell chromatin accessibility data.

## When to use

Apply this skill after loading and preprocessing raw scATAC-seq data into an ArchR project object when you need to compute low-dimensional embeddings for clustering, UMAP/tSNE visualization, or integrated multi-omic analysis. Use it as a prerequisite before trajectory analysis (Monocle3 or Slingshot), gene expression matrix integration, or any downstream analysis that requires dimensionality-reduced cell representations.

## When NOT to use

- Input data is already a low-dimensional embedding or has been previously dimensionality-reduced by another method—apply this skill only on raw or minimally processed peak-by-cell matrices.
- scATAC-seq data has not been quality-filtered or peak-called; LSI performance depends on upstream preprocessing.
- Analysis goal is restricted to single-cell gene expression only without chromatin accessibility component; use gene expression-specific dimensionality reduction methods instead.

## Inputs

- ArchR project object (with imported scATAC-seq peak matrix)
- Peak-by-cell count matrix (sparse, typically filtered for quality control)

## Outputs

- ArchR project object with LSI embedding (addIterativeLSI result)
- Low-dimensional cell representation (LSI dimensions)
- Optional: combined LSI embedding (if using addCombinedDims for multiome data)

## How to apply

Invoke the addIterativeLSI function on your ArchR project object to compute iterative latent semantic indexing across the peak-by-cell matrix. This function performs dimensionality reduction while accounting for sparsity inherent in scATAC-seq data. For paired scATAC-seq and scRNA-seq analysis, compute LSI embeddings for both modalities separately, then use addCombinedDims to integrate the reduced dimensions from both datasets into a unified embedding space suitable for joint clustering and downstream analysis.

## Related tools

- **ArchR** (Primary package providing addIterativeLSI and addCombinedDims functions for scATAC-seq dimensionality reduction and multiome integration) — https://github.com/GreenleafLab/ArchR
- **monocle3** (Downstream trajectory analysis tool that depends on dimensionality-reduced embeddings from LSI) — https://github.com/cole-trapnell-lab/monocle3
- **Slingshot** (Alternative downstream trajectory analysis tool that accepts LSI embeddings for pseudotime inference)
- **R** (Programming language and environment for executing ArchR functions)

## Examples

```
library(ArchR); proj <- addIterativeLSI(ArchRProj = proj, useMatrix = 'TileMatrix', name = 'Iterative LSI')
```

## Evaluation signals

- ArchR project object successfully contains LSI embedding(s) accessible via getReducedDims() or equivalent accessor.
- Dimensionality is reduced from tens of thousands of peaks to tens of LSI dimensions (typically 30–50 dimensions retained).
- Subsequent UMAP or tSNE visualization using the LSI embedding produces distinct cell clusters with biological meaning.
- If multiome: combined LSI embedding reflects both scATAC-seq and scRNA-seq signal without one modality dominating; validate via markers specific to each modality.
- Trajectory analysis (Monocle3 or Slingshot) downstream of LSI embedding converges and produces biologically coherent pseudotime ordering.

## Limitations

- LSI assumes approximate low-rank structure in the peak-by-cell matrix; highly noisy or unfiltered datasets may produce poor embeddings.
- Iterative LSI is computationally intensive for >1 million cells, though ArchR is designed to handle this on standard laptops.
- Combined dimensionality reduction (addCombinedDims) may mask dataset-specific signals if the two modalities (scATAC and scRNA) have strong batch effects; batch correction before combination is recommended.
- ArchR is currently in beta with active development, so interface and behavior may change.

## Evidence

- [intro] ArchR supports trajectory analysis using both monocle3 and Slingshot functions including addIterativeLSI as a prerequisite step: "ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims"
- [readme] addIterativeLSI is a core dimensionality reduction workflow step in ArchR: "See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims"
- [readme] ArchR excels in speed and resource usage for large scATAC-seq datasets: "ArchR excels in both speed and resource usage, making it possible to analyze 1 million cells in 8 hours on a MacBook Pro laptop."
- [readme] ArchR is a comprehensive R package for scATAC-seq analysis: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data."
