---
name: dimensionality-reduction-via-reverse-pca
description: Use when you have a normalized single-cell expression matrix (e.g., after SCTransform) and need to compute gene-level covariance structure for pathway enrichment analysis (e.g., GESECA) rather than cell-level dimensionality reduction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - R
  - fgsea
  - msigdbr
  - ggplot2
  - Seurat
derived_from:
- doi: 10.1101/060012
  title: fgsea
evidence_spans:
- R-package for fast preranked gene set enrichment analysis
- fgsea is an R-package for fast preranked gene set enrichment analysis
- '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'
- gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)
- pathwaysDF <- msigdbr(species="mouse", collection="H")
- library(msigdbr) pathwaysDF <- msigdbr(species="mouse", collection="C2", subcollection = "CP:KEGG_LEGACY")
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fgsea
    doi: 10.1101/060012
    title: fgsea
  dedup_kept_from: coll_fgsea
schema_version: 0.2.0
---

# dimensionality-reduction-via-reverse-pca

## Summary

Reverse PCA extracts gene (feature) loadings from a normalized expression matrix to reduce dimensionality for downstream pathway analysis in single-cell RNA-seq workflows. Unlike standard PCA which projects cells into reduced space, reverse PCA produces a feature-space embedding suitable for GESECA and other coregulation-based enrichment methods.

## When to use

You have a normalized single-cell expression matrix (e.g., after SCTransform) and need to compute gene-level covariance structure for pathway enrichment analysis (e.g., GESECA) rather than cell-level dimensionality reduction. Reverse PCA is specifically indicated when you want to identify pathways whose member genes co-vary together across the normalized feature space.

## When NOT to use

- You need to project cells into reduced space for clustering or visualization—use standard PCA (rev.pca=FALSE) instead.
- Input is already a feature loadings matrix or gene-level covariance matrix—reverse PCA will not add value.
- Your analysis goal is cell-type classification or quality control metrics (e.g., nCount, nFeature)—cell-space embeddings are more appropriate.

## Inputs

- normalized expression matrix (SCTransform output, [n_genes × n_cells])
- Seurat object with SCTransform-normalized assay
- gene set pathways (MSigDB format, e.g., KEGG_LEGACY)

## Outputs

- feature loadings matrix E ([n_genes × n_pcs])
- GESECA enrichment results (pathway scores, p-values, coregulation profiles)
- plotCoregulationProfileReduction visualization (tsne/umap reduction showing pathway scores per cell type)

## How to apply

After applying SCTransform normalization with a fixed set of variable features (e.g., variable.features.n=10000), run PCA with rev.pca=TRUE and a moderate number of components (e.g., npcs=50). Extract the feature loadings matrix E from the PCA reduction object (typically obj@reductions$pca.rev@feature.loadings). This matrix has dimensions [n_genes × n_pcs] and encodes how each gene loads onto the principal components. Pass this loadings matrix directly to GESECA with eps=1e-100 (or lower for more precise p-values) to compute pathway enrichment scores based on coregulation patterns in the feature space.

## Related tools

- **Seurat** (SCTransform normalization and PCA computation with rev.pca parameter)
- **fgsea** (GESECA function accepts feature loadings matrix to compute pathway enrichment and p-values) — https://github.com/ctlab/fgsea
- **msigdbr** (Retrieve KEGG_LEGACY and other pathway gene sets for input to GESECA)
- **ggplot2** (Visualize pathway scores and coregulation profiles via plotCoregulationProfileReduction)

## Examples

```
obj <- SCTransform(obj, verbose = FALSE, variable.features.n = 10000); obj <- RunPCA(obj, assay = "SCT", verbose = FALSE, rev.pca = TRUE, reduction.name = "pca.rev", npcs = 50); E <- obj@reductions$pca.rev@feature.loadings; gesecaRes <- geseca(pathways, E, minSize = 5, maxSize = 500, center = FALSE, eps = 1e-100)
```

## Evaluation signals

- Feature loadings matrix E has correct dimensions [n_genes × n_pcs] with n_pcs ≤ 50 and matches the variable feature set.
- GESECA produces pathway p-values down to the specified eps threshold (e.g., eps=1e-100); p-values should be non-zero and ordered by enrichment strength.
- Top-ranked pathways are biologically coherent with cell type annotations (e.g., KEGG_LEISHMANIA_INFECTION in non-foamy macrophages, KEGG_LYSOSOME in foamy macrophages).
- plotCoregulationProfileReduction plots show clear separation of pathway scores across cell types or clusters, confirming pathway-cell-type association.
- Feature loadings are centered or scaled consistently with the choice of center=FALSE in GESECA call (verify consistency between SCTransform and GESECA parameters).

## Limitations

- Reverse PCA assumes linear relationships among genes; highly nonlinear coregulation structures may be missed.
- Results are sensitive to the choice of variable.features.n and npcs; no universal default exists across tissues or conditions.
- GESECA p-value estimation uses Monte-Carlo sampling and remains stochastic; eps parameter trades off precision for computational cost.
- Reverse PCA feature loadings are orthogonal within the PCA space but do not directly represent biological correlation; interpretation requires downstream validation (e.g., co-expression checks).

## Evidence

- [methods] Run reverse PCA on SCTransform-normalized matrix: "Run reverse PCA (rev.pca=TRUE) on SCTransform-normalized matrix with npcs=50, extracting feature loadings matrix E."
- [methods] GESECA input and parameter specification: "Run geseca(pathways, E, minSize=5, maxSize=500, center=FALSE, eps=1e-100) on reduced feature space, producing enrichment scores and p-values."
- [methods] Reverse PCA produces feature-space enrichment: "Extract top-ranked pathways and generate plotCoregulationProfileReduction plots (reduction='tsne') to visualize pathway scores by cell type, confirming KEGG_LEISHMANIA_INFECTION prominence in"
- [intro] P-value computation method via Monte-Carlo: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme."
