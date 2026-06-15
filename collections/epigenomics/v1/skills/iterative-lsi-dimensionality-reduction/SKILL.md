---
name: iterative-lsi-dimensionality-reduction
description: Use when when you have aligned paired scATAC-seq and scRNA-seq data from the same cells (multiome data) and need to create a single reduced-dimension coordinate space that integrates both chromatin accessibility and gene expression signals for joint clustering, trajectory analysis, or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0654
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

# iterative-lsi-dimensionality-reduction

## Summary

Iterative latent semantic indexing (LSI) is a dimensionality reduction technique that jointly compresses scATAC-seq chromatin accessibility peaks and scRNA-seq gene expression data into a unified low-dimensional embedding for integrated multimodal analysis. This approach enables visualization, clustering, and downstream analysis of paired single-cell multiome datasets.

## When to use

When you have aligned paired scATAC-seq and scRNA-seq data from the same cells (multiome data) and need to create a single reduced-dimension coordinate space that integrates both chromatin accessibility and gene expression signals for joint clustering, trajectory analysis, or visualization.

## When NOT to use

- Input data are unimodal (scATAC-seq only or scRNA-seq only) — use standard LSI or PCA on the single modality instead.
- Cells in the peak matrix and gene expression matrix are not aligned or do not represent the same cells — addIterativeLSI requires matched cell identities across modalities.
- Peak matrix and expression matrix have already been independently dimensionality-reduced without joint integration in mind — joint LSI requires the raw or lightly-processed feature tables as input.

## Inputs

- ArchR project object with imported scATAC-seq peak matrix (from importFeatureMatrix)
- ArchR project object with appended scRNA-seq gene expression matrix (from addGeneExpressionMatrix)
- Aligned cell barcodes across both modalities

## Outputs

- ArchR project object with computed iterative LSI dimensions
- Latent semantic indexing coordinates integrating both scATAC-seq and scRNA-seq variance
- Input for addCombinedDims to produce unified reduced-dimension embedding

## How to apply

After ingesting the scATAC-seq peak matrix via importFeatureMatrix and appending the scRNA-seq gene expression matrix via addGeneExpressionMatrix to the same ArchR project object, execute addIterativeLSI on the combined project to perform latent semantic indexing jointly across both modalities. This function computes iterative dimensionality reduction that treats accessibility peaks and gene expression features together, producing latent dimensions that capture variance explained by both data types. The resulting LSI coordinates form the basis for downstream integration via addCombinedDims, which generates a unified embedding. Key rationale: iterative LSI avoids the bias of treating modalities separately and ensures that the reduced-dimension space reflects the joint signal of chromatin and transcriptomic state.

## Related tools

- **ArchR** (Primary toolkit for ingesting, storing, and reducing paired multimodal single-cell data; provides importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, and addCombinedDims functions) — https://github.com/GreenleafLab/ArchR

## Examples

```
archRProj <- addIterativeLSI(ArchRProj = archRProj, useMatrix = "GeneExpressionMatrix", name = "LSI_multiome")
```

## Evaluation signals

- LSI dimensions are successfully added to the ArchR project object metadata with non-zero variance explained by both modalities.
- The resulting latent dimensions separate known cell types or biological states visible in either the accessibility or expression data, or both.
- addCombinedDims successfully executes on the LSI-reduced project and produces a unified low-dimensional embedding without errors.
- UMAP or t-SNE visualization of the combined dimensions shows coherent clustering consistent with known biology (e.g., cell type markers from either modality co-localize in the joint space).
- Iterative LSI captures variance from both peak accessibility and gene expression — examine scree plot or variance explained to confirm both modalities contribute meaningfully.

## Limitations

- ArchR is currently in beta and actively under development; reproducibility across versions may vary until formal peer review completion.
- Iterative LSI requires pre-aligned cell barcodes across modalities; mismatched or incomplete alignment will produce biased or noisy embeddings.
- The method assumes cells in both modalities are of comparable quality and sequencing depth; cells with extremely sparse expression or accessibility may introduce noise and should be filtered before LSI.
- No changelog available in repository; parameter defaults and algorithm details may change between versions without explicit documentation.

## Evidence

- [other] The paired multiome workflow in ArchR operates through a four-step process: importFeatureMatrix ingests the feature matrix, addGeneExpressionMatrix adds the scRNA-seq gene expression data, addIterativeLSI performs iterative dimensionality reduction, and addCombinedDims produces the joint reduced-dimension embedding integrating both modalities.: "Execute addIterativeLSI on the combined project to compute latent semantic indexing of accessibility peaks and gene expression jointly."
- [readme] ArchR now supports paired scATAC-seq and scRNA-seq Analysis with functions including importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, and addCombinedDims.: "ArchR now supports paired scATAC-seq and scRNA-seq Analysis! See updates with importFeatureMatrix, addGeneExpressionMatrix, addIterativeLSI, addCombinedDims"
- [other] Load scRNA-seq gene expression matrix and call addGeneExpressionMatrix to append gene expression data to the same project, aligning cells across modalities.: "call addGeneExpressionMatrix to append gene expression data to the same project, aligning cells across modalities."
- [readme] ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data and now supports multimodal analysis.: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data."
