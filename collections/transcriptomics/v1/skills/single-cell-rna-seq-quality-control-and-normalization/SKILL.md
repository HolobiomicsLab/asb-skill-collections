---
name: single-cell-rna-seq-quality-control-and-normalization
description: Use when when you have a raw or minimally processed scRNA-seq dataset (e.g., a Seurat object loaded from GEO) and need to prepare it for pathway enrichment or coregulation analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0092
  tools:
  - R
  - fgsea
  - msigdbr
  - ggplot2
  - Seurat
  - SCTransform
  - GEOquery
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

# single-cell-rna-seq-quality-control-and-normalization

## Summary

Apply variance-stabilizing normalization and feature selection to single-cell RNA-seq count matrices, then perform dimensionality reduction on the normalized feature space to prepare data for downstream enrichment analysis. This skill bridges raw expression data to gene set analysis by stabilizing heteroscedastic count distributions and identifying the most informative genes.

## When to use

When you have a raw or minimally processed scRNA-seq dataset (e.g., a Seurat object loaded from GEO) and need to prepare it for pathway enrichment or coregulation analysis. Specifically, use this skill when your input is an unnormalized count matrix with high variance heterogeneity across genes and cell types, and your goal is to extract stable feature loadings for cross-cell-type comparisons (e.g., GESECA or reverse PCA analysis).

## When NOT to use

- Input is already a normalized expression matrix or feature loadings matrix — skip directly to enrichment analysis.
- Your analysis goal is cell-type clustering or cell-state discovery, not pathway enrichment — use standard PCA instead of reverse PCA.
- Dataset has <100 cells or <5000 genes — variance stabilization and 10,000-feature selection may overfit or provide no benefit.
- Count matrix is sparse (>90% zeros) and from highly specialized protocols (e.g., spatial transcriptomics with <1% detection) — SCTransform assumes sufficient depth per cell.

## Inputs

- Seurat object with raw counts (or pre-loaded from GEO via GEOquery)
- Cell type annotations or cluster assignments (e.g., from RenameIdents)
- Target variable.features.n threshold (e.g., 10000)
- Target number of PCs (npcs, e.g., 50)

## Outputs

- SCTransform-normalized Seurat assay (SCT)
- Feature loadings matrix E (genes × components)
- List of selected variable features (10000 genes)
- Reverse PCA reduction object (stored in reductions slot)

## How to apply

Load the scRNA-seq object (e.g., GSE116240 atherosclerosis Seurat object) and apply SCTransform normalization with variable.features.n=10000 to stabilize variance across genes and select the top 10,000 most variable features for the downstream universe. Then run reverse PCA (rev.pca=TRUE) with npcs=50 on the SCTransform-normalized assay to extract the feature loadings matrix, which represents gene contributions across principal components. This loadings matrix becomes the input for gene set coregulation analysis (GESECA). The rationale: SCTransform removes count-depth artifacts via Pearson residuals, and reverse PCA shifts from cell-by-gene space to gene-by-component space, enabling gene-level enrichment scoring without aggregating over cells.

## Related tools

- **Seurat** (Core framework for loading, normalizing (SCTransform), and dimensionality reduction (PCA) of scRNA-seq Seurat objects)
- **SCTransform** (Variance-stabilizing normalization applied to raw counts to remove depth effects and select top variable genes)
- **fgsea** (Downstream tool that consumes the feature loadings matrix from reverse PCA to calculate gene set enrichment scores (GESECA) and p-values) — https://github.com/ctlab/fgsea
- **GEOquery** (Retrieve scRNA-seq objects and metadata from GEO accessions (e.g., GSE116240))
- **ggplot2** (Visualization of pathway scores and enrichment results (e.g., plotCoregulationProfileReduction))

## Examples

```
obj <- SCTransform(obj, verbose = FALSE, variable.features.n = 10000); obj <- RunPCA(obj, assay = "SCT", verbose = FALSE, rev.pca = TRUE, reduction.name = "pca.rev", reduction.key="PCR_", npcs = 50); E <- obj@reductions$pca.rev@feature.loadings
```

## Evaluation signals

- SCTransform normalization completes without divergence warnings; check that the SCT assay is populated in the Seurat object and variable.features slot contains 10,000 gene names.
- Reverse PCA runs with npcs=50 and rev.pca=TRUE; verify that the feature loadings matrix E has dimensions (number_of_genes, 50), e.g., (18000, 50) for typical datasets.
- Downstream GESECA call succeeds with the E matrix as input and produces pathway enrichment scores and p-values with no NaN or infinite values.
- Enrichment plots (e.g., plotCoregulationProfileReduction) show clear cell-type stratification of pathway scores; e.g., KEGG_LYSOSOME ranks high in foamy macrophages and low in non-foamy macrophages.
- Principal component loadings show interpretable gene-component relationships (e.g., top genes in PC1 are known macrophage markers or atherosclerosis-related genes).

## Limitations

- SCTransform assumes cells have sufficient sequencing depth (minimum ~1000 UMIs per cell); shallow scRNA-seq libraries may produce unreliable Pearson residuals.
- Reverse PCA extracts covariation at the feature level across all cells pooled together; it does not preserve cell-type-specific coregulation patterns unless the model is run separately per cluster.
- Choice of variable.features.n=10000 is empirical and not validated for all organism sizes or experimental designs; smaller genomes (e.g., C. elegans) may not benefit from 10,000 features.
- Reverse PCA with npcs=50 assumes 50 components sufficiently capture gene-gene relationships; choosing too few npcs may lose gene covariation signal, and too many may introduce noise.
- The workflow requires a Seurat object and is tightly coupled to the Seurat ecosystem; other frameworks (scanpy, AnnData) require analogous but non-identical normalization and PCA pipelines.

## Evidence

- [methods] SCTransform normalization stabilizes variance and selects genes: "Apply SCTransform normalization with variable.features.n=10000 to stabilize variance and select genes for universe."
- [methods] Reverse PCA extracts feature loadings for gene set analysis: "Run reverse PCA (rev.pca=TRUE) on SCTransform-normalized matrix with npcs=50, extracting feature loadings matrix E."
- [methods] fgsea package accepts feature loadings for enrichment: "Run geseca(pathways, E, minSize=5, maxSize=500, center=FALSE, eps=1e-100) on reduced feature space"
- [methods] Downstream enrichment plots stratify pathways by cell type: "Generate plotCoregulationProfileReduction plots (reduction='tsne') to visualize pathway scores by cell type"
- [readme] fgsea enables rapid, accurate P-value calculation: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
- [readme] P-value estimation uses adaptive Monte-Carlo scheme: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme."
