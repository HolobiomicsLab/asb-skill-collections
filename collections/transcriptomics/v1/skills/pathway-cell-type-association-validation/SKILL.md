---
name: pathway-cell-type-association-validation
description: Use when you have a multi-cluster single-cell RNA-seq dataset with cell-type annotations and you want to test whether known biological pathways (e.g., KEGG or MSigDB gene sets) show significantly elevated or differential enrichment across cell types.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3308
  tools:
  - R
  - fgsea
  - msigdbr
  - ggplot2
  - Seurat
  - data.table
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

# pathway-cell-type-association-validation

## Summary

Validate pathway enrichment associations across annotated cell types using gene set enrichment analysis on dimensionality-reduced feature spaces. This skill combines cell-type annotation, variance-stabilizing normalization, reverse PCA projection, and GESECA analysis to confirm that specific pathways exhibit elevated enrichment in biologically expected cell populations.

## When to use

Apply this skill when you have a multi-cluster single-cell RNA-seq dataset with cell-type annotations and you want to test whether known biological pathways (e.g., KEGG or MSigDB gene sets) show significantly elevated or differential enrichment across cell types. Specific triggers include: (1) you have manually or computationally assigned cell-type labels to clusters; (2) you have prior biological hypotheses about which pathways should activate in specific cell types (e.g., leishmania infection genes in pathogenic macrophage subtypes); (3) you need p-value estimates at arbitrarily low thresholds (below 1e-10) to discriminate subtle enrichment differences across populations.

## When NOT to use

- Input gene sets are already pre-ranked by a sample-level statistic (use standard fgsea() instead of GESECA, which requires a feature loadings matrix).
- Cell-type annotations are not yet assigned or are uninformative (the skill validates associations with known populations; without meaningful labels, results cannot be interpreted biologically).
- Gene expression data has not been normalized or variance-stabilized (SCTransform or equivalent preprocessing is required for the loadings matrix to be interpretable).
- Pathway database contains predominantly non-human gene symbols or does not overlap substantially with your gene universe (msigdbr filtering and ortholog mapping should be performed first).

## Inputs

- Seurat object or single-cell RNA-seq matrix (rows=genes, columns=cells, values=log-normalized counts or SCT residuals)
- Cell-type annotation vector or Seurat metadata column (one label per cell)
- Gene set collection (list of character vectors, each named pathway containing gene symbols)

## Outputs

- GESECA enrichment results table (rows=pathways, columns=pathway name, enrichment score ES, p-value, adjusted p-value padj, log2err, normalized enrichment score NES, pathway size)
- Pathway scores per cell (matrix or data.frame: rows=cells, columns=top pathways)
- Visualization plots (e.g., tSNE scatter plots colored by pathway enrichment score, faceted by cell type)

## How to apply

First, load the single-cell expression matrix (e.g., as a Seurat object) and annotate cell clusters with biologically meaningful identities (e.g., macrophage subtypes) using tools like RenameIdents. Apply SCTransform normalization with a fixed number of variable features (e.g., 10,000) to stabilize variance and establish a consistent gene universe across all samples. Run reverse PCA (rev.pca=TRUE) with a sufficient number of principal components (e.g., 50) to capture gene-level loadings in a reduced feature space; extract the feature loadings matrix E from the PCA reduction object. Load pathway annotations from a reference database (e.g., KEGG_LEGACY from MSigDB via msigdbr) filtered to human and matched to your gene identifiers. Execute GESECA (Gene Set Enrichment analysis on the Coregulation structure of Expressions) on E with conservative size filters (minSize=5, maxSize=500), center=FALSE to preserve loadings scale, and eps=1e-100 to enable precise p-value estimation via the adaptive multi-level split Monte-Carlo scheme. Extract top-ranked pathways by p-value and visualize enrichment scores by cell type using dimensionality reduction plots (e.g., tSNE); confirm that pathways co-localize with expected cell populations. The skill succeeds when a priori biological hypotheses (e.g., 'KEGG_LEISHMANIA_INFECTION should be high in pathogenic macrophages') are supported by the enrichment landscape.

## Related tools

- **fgsea** (Executes GESECA (gene set enrichment on coregulation structure) and computes arbitrarily low p-values via adaptive multi-level split Monte-Carlo scheme) — https://github.com/ctlab/fgsea
- **Seurat** (Loads single-cell RNA-seq data, performs SCTransform normalization, runs reverse PCA, and manages cell-type annotations via RenameIdents)
- **msigdbr** (Retrieves and filters pathway gene sets (e.g., KEGG_LEGACY) from MSigDB by species and category)
- **ggplot2** (Generates publication-quality tSNE or dimensionality reduction plots colored by pathway enrichment scores and faceted by cell type)
- **data.table** (Efficiently sorts, filters, and manipulates enrichment results tables by p-value and pathway ranking)

## Examples

```
gesecaRes <- geseca(pathways, E, minSize=5, maxSize=500, center=FALSE, eps=1e-100); plotCoregulationProfileReduction(seurat_obj, features=topPathways, reduction='tsne')
```

## Evaluation signals

- P-value distribution: Top enriched pathways should have p-values well below 1e-6 if signal is strong; check that eps=1e-100 setting produces non-uniform log10(pval) across pathways (not capped at default 1e-10).
- Biological coherence: Manually confirm that the top 5–10 enriched pathways for each major cell type align with known biology (e.g., KEGG_LYSOSOME in foamy macrophages, KEGG_LEISHMANIA_INFECTION in ISG+ or pathogenic subtypes).
- Cell-type localization: Examine plotCoregulationProfileReduction plots and verify that pathway enrichment scores form spatially coherent clusters on the tSNE/UMAP that co-localize with annotated cell-type identities; enrichment should not be uniformly distributed across unrelated populations.
- Pathway size filters: Confirm that all returned pathways respect minSize and maxSize constraints; pathways outside this range should be absent from results.
- Numerical stability: Check for NaN or Inf values in ES, NES, or p-value columns; if present, investigate whether gene-loading scaling or feature normalization failed.

## Limitations

- GESECA operates on a reduced feature space (PCA loadings), so results are sensitive to the number of PCs retained (e.g., npcs=50); overly few PCs lose information, while too many risk noise. The optimal choice depends on data dimensionality and batch structure.
- Pathway enrichment scores reflect coregulation patterns in the feature space, not direct expression abundance; pathways with low absolute expression but coordinated variation across cells may still show strong enrichment. Interpretation requires biological context.
- MSigDB pathway collections (KEGG_LEGACY, Reactome, etc.) reflect curated but incomplete knowledge; genes newly linked to pathways post-curation will not be captured, and tissue- or disease-specific pathway rewiring may differ from generic definitions.
- Multiple testing burden increases with pathway database size; even with FDR correction (padj), interpreting hundreds of significant pathways requires careful ranking and manual filtering by effect size and biological plausibility.
- Cell-type annotation quality directly impacts validity: misannotated or ambiguous cells will blur enrichment signals. Annotations should be validated independently (e.g., via marker gene expression) before drawing biological conclusions.

## Evidence

- [intro] P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme.: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme."
- [methods] SCTransform normalization with variable.features.n=10000 to stabilize variance and select genes for universe.: "Apply SCTransform normalization with variable.features.n=10000 to stabilize variance and select genes for universe."
- [methods] Run reverse PCA (rev.pca=TRUE) on SCTransform-normalized matrix with npcs=50, extracting feature loadings matrix E.: "Run reverse PCA (rev.pca=TRUE) on SCTransform-normalized matrix with npcs=50, extracting feature loadings matrix E."
- [methods] Run geseca(pathways, E, minSize=5, maxSize=500, center=FALSE, eps=1e-100) on reduced feature space, producing enrichment scores and p-values.: "Run geseca(pathways, E, minSize=5, maxSize=500, center=FALSE, eps=1e-100) on reduced feature space, producing enrichment scores and p-values."
- [methods] plotCoregulationProfileReduction plots (reduction='tsne') to visualize pathway scores by cell type, confirming KEGG_LEISHMANIA_INFECTION prominence in non-foamy intimal macrophages and KEGG_LYSOSOME in foamy intimal macrophages.: "generate plotCoregulationProfileReduction plots (reduction='tsne') to visualize pathway scores by cell type, confirming KEGG_LEISHMANIA_INFECTION prominence in non-foamy intimal macrophages and"
- [readme] This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets.: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets."
- [readme] As you can see `fgsea` has a default lower bound `eps=1e-10` for estimating P-values. If you need to estimate P-value more accurately, you can set the `eps` argument to zero in the `fgsea` function.: "If you need to estimate P-value more accurately, you can set the `eps` argument to zero in the `fgsea` function."
