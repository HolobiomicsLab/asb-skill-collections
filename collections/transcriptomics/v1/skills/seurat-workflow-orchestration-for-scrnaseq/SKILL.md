---
name: seurat-workflow-orchestration-for-scrnaseq
description: 'Use when you have a raw or Seurat object-backed scRNA-seq expression matrix and need to: (1) stabilize variance across genes with SCTransform normalization, (2) extract feature loadings in reduced dimensionality space via reverse PCA to use as input for GESECA or other coregulation-based enrichment.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3391
  tools:
  - R
  - fgsea
  - Seurat
  - msigdbr
  - ggplot2
  - data.table
derived_from:
- doi: 10.1101/060012
  title: fgsea
evidence_spans:
- R-package for fast preranked gene set enrichment analysis
- fgsea is an R-package for fast preranked gene set enrichment analysis
- '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'
- gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)
- suppressMessages(library(Seurat)) obj <- readRDS(url("https://alserglab.wustl.edu/files/fgsea/GSE116240.rds"))
- pathwaysDF <- msigdbr(species="mouse", collection="H")
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

# seurat-workflow-orchestration-for-scRNAseq

## Summary

A Seurat-based orchestration workflow for preprocessing and analyzing single-cell RNA-seq data through normalization, dimensionality reduction, and reverse PCA to enable downstream pathway enrichment analysis. Use this skill when your input is raw or minimally processed scRNA-seq expression matrices (e.g., from GEO datasets like GSE116240) and you need to extract normalized feature loadings for gene set enrichment or cell-type annotation.

## When to use

You have a raw or Seurat object-backed scRNA-seq expression matrix and need to: (1) stabilize variance across genes with SCTransform normalization, (2) extract feature loadings in reduced dimensionality space via reverse PCA to use as input for GESECA or other coregulation-based enrichment analyses, or (3) annotate and visualize cell clusters with biological subtypes before downstream pathway analysis. Typical trigger: you are working with atherosclerosis, immune, or other tissue-level scRNA-seq datasets and want to correlate pathway activity with cell state.

## When NOT to use

- Input is already a normalized feature table or pathway enrichment matrix — you do not need Seurat orchestration if data has been preprocessed to gene-level statistics.
- Your goal is standard differential expression testing, not coregulation-based pathway enrichment — use standard GSEA or limma instead of reverse PCA.
- Cell cluster annotations are already definitive and you only need visualization — skip RenameIdents and move directly to pathway analysis.

## Inputs

- Seurat object (in-memory or from URL/GEO)
- Raw or log-normalized scRNA-seq expression matrix (cells × genes)
- Cell metadata with clustering or cell-type assignments
- Gene pathway definitions (KEGG_LEGACY or other MSigDB collections)

## Outputs

- SCTransform-normalized Seurat assay (SCT slot)
- Reverse PCA reduction (pca.rev slot) with feature loadings matrix E (genes × npcs)
- Annotated cell cluster identities (RenameIdents output)
- GESECA enrichment results table (pathways × p-values, NES, coregulation scores)
- plotCoregulationProfileReduction visualization (pathway scores by cell type and 2D reduction)

## How to apply

Load a scRNA-seq Seurat object (from URL, .h5ad, or local file), then: (1) Apply SCTransform normalization with variable.features.n=10000 to stabilize variance and identify the gene universe. (2) Run reverse PCA (rev.pca=TRUE, npcs=50) on the SCTransform-normalized assay to obtain a feature loadings matrix E in reduced feature space. (3) Extract the feature.loadings matrix from the PCA reduction slot. (4) Annotate cell clusters using RenameIdents with reference-based or marker-driven subtypes (e.g., macrophage subtypes). (5) Pass the loadings matrix E to geseca() with minSize=5, maxSize=500, center=FALSE, and low eps (e.g., 1e-100) to estimate enrichment p-values on the coregulation structure. (6) Visualize results using plotCoregulationProfileReduction with reduction='tsne' to confirm pathway prominence by cell type. The rationale: reverse PCA rotates the data into a space where genes are rows and PCs are columns, allowing pathway enrichment to be calculated on gene coregulation patterns rather than individual expression levels, improving sensitivity in sparse scRNA-seq.

## Related tools

- **Seurat** (Core orchestration framework: loads scRNA-seq data, runs SCTransform normalization, reverse PCA, and cell cluster annotation via RenameIdents)
- **fgsea** (Performs GESECA (gene set enrichment on coregulation) on feature loadings matrix E to compute p-values and enrichment scores via adaptive multi-level Monte-Carlo) — https://github.com/ctlab/fgsea
- **msigdbr** (Retrieves KEGG_LEGACY and other pathway definitions from MSigDB as input to geseca())
- **ggplot2** (Generates plotCoregulationProfileReduction visualizations and supplementary plots)
- **data.table** (Efficiently sorts and manipulates GESECA results tables (p-values, pathways))

## Examples

```
obj <- SCTransform(obj, verbose=FALSE, variable.features.n=10000); obj <- RunPCA(obj, assay='SCT', verbose=FALSE, rev.pca=TRUE, reduction.name='pca.rev', npcs=50); E <- obj@reductions$pca.rev@feature.loadings; gesecaRes <- geseca(pathways, E, minSize=5, maxSize=500, center=FALSE, eps=1e-100)
```

## Evaluation signals

- SCTransform normalization reduces variance heterogeneity: variance.stabilized flag in Seurat is TRUE, and the distribution of log-transformed scaled counts is visually homogeneous across gene expression bins.
- Reverse PCA extraction succeeds: feature.loadings matrix E has shape (n_genes, npcs=50) with non-zero values and is distinct from standard PCA loadings (columns are in different order due to rev.pca=TRUE).
- GESECA p-values are sub-threshold and estimable: geseca() output table contains pval values below eps=1e-100 (not all pval == 1.0), and top pathways have NES scores consistent with known biology (e.g., KEGG_LEISHMANIA_INFECTION prominent in inflammatory macrophages).
- Cell type annotations are interpretable: RenameIdents output clusters match known marker genes (e.g., Adventitial MF, Intimal foamy MF subsets show distinct marker expression via FeaturePlot or DotPlot).
- Pathway scores correlate with cell type: plotCoregulationProfileReduction plot shows visual separation of pathway enrichment by cell cluster, and top pathways are biologically relevant to the tissue/disease context (atherosclerosis macrophage subtypes).

## Limitations

- Reverse PCA assumes linear gene-to-PC relationships; non-linear coregulation patterns may not be fully captured in the loadings space.
- GESECA p-value estimation is Monte-Carlo-based and stochastic; very low eps values (e.g., eps=1e-100) require high computational cost and may introduce numerical instability in edge cases.
- SCTransform with variable.features.n=10000 assumes sufficient gene diversity; sparse or low-quality datasets may have poor variance stabilization or feature selection.
- Cell cluster annotations (RenameIdents) are manual or reference-driven and depend on marker gene quality; misannotation will propagate to downstream pathway interpretation.
- No changelog tracking available for reproducibility: exact version dependencies of Seurat, fgsea, msigdbr are not formally versioned in typical workflows.

## Evidence

- [intro] P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme"
- [methods] SCTransform normalization stabilizes variance and selects feature universe: "Apply SCTransform normalization with variable.features.n=10000 to stabilize variance and select genes for universe"
- [methods] Reverse PCA extracts feature loadings for downstream enrichment: "Run reverse PCA (rev.pca=TRUE) on SCTransform-normalized matrix with npcs=50, extracting feature loadings matrix E"
- [methods] GESECA runs on reduced feature loadings space with adaptive p-value thresholds: "Run geseca(pathways, E, minSize=5, maxSize=500, center=FALSE, eps=1e-100) on reduced feature space, producing enrichment scores and p-values"
- [methods] Pathway visualization confirms biological relevance by cell type: "generate plotCoregulationProfileReduction plots (reduction='tsne') to visualize pathway scores by cell type, confirming KEGG_LEISHMANIA_INFECTION prominence in non-foamy intimal macrophages and"
- [readme] fgsea enables rapid and accurate low p-value calculation: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
