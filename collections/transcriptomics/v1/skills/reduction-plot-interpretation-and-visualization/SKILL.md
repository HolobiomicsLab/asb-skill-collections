---
name: reduction-plot-interpretation-and-visualization
description: Use when after computing gene set enrichment scores (e.g., via GESECA on reverse PCA feature loadings) on a single-cell or bulk dataset with an existing dimensionality reduction (tSNE, UMAP, PCA).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0092
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

# reduction-plot-interpretation-and-visualization

## Summary

Generate and interpret dimensionality reduction plots (e.g., tSNE, PCA) to visualize pathway enrichment scores or gene set activity across cell types or samples. This skill enables identification of cell-type-specific pathway dependencies by overlaying continuous enrichment metrics onto low-dimensional projections.

## When to use

After computing gene set enrichment scores (e.g., via GESECA on reverse PCA feature loadings) on a single-cell or bulk dataset with an existing dimensionality reduction (tSNE, UMAP, PCA). Use this skill when you need to (1) detect which cell types or clusters are enriched for specific pathways, (2) validate that pathway scores co-vary with annotated cell identity, or (3) visually distinguish functional subpopulations within a heterogeneous cell type.

## When NOT to use

- Pathway enrichment scores have not yet been computed; run GESECA or GSEA first.
- No dimensionality reduction is available in the object; compute tSNE, UMAP, or PCA before plotting.
- Cell type annotations are missing or unreliable; validation or manual curation is required.
- The pathway set is very large (>>1000 pathways) without pre-filtering; focus on top-ranked or biologically relevant pathways to avoid visual clutter.

## Inputs

- Seurat object with SCT normalization and reverse PCA reduction
- GESECA enrichment result (data frame with pathway names and enrichment scores)
- Cell type annotations (factor or character vector)
- Dimensionality reduction coordinates (tSNE, UMAP, or PCA; embedded in Seurat object)

## Outputs

- ggplot2 plot object(s) with pathway scores overlaid on dimensionality reduction
- Visual evidence of cell-type-specific pathway enrichment patterns
- Annotated feature plot or coregulation profile visualization

## How to apply

After SCTransform normalization and reverse PCA (rev.pca=TRUE, npcs=50) on a Seurat object, extract the feature loadings matrix E and run GESECA on pathways of interest with minSize=5, maxSize=500, center=FALSE to produce enrichment scores per pathway. Extract pathway scores from the GESECA result and add them as metadata to the Seurat object. Generate plotCoregulationProfileReduction plots using the 'tsne' (or alternative) reduction, coloring by pathway score and faceting by cell type annotation. Inspect the resulting plots to confirm that expected pathways show strong signal in predicted cell populations (e.g., KEGG_LEISHMANIA_INFECTION in non-foamy intimal macrophages, KEGG_LYSOSOME in foamy intimal macrophages). Use color intensity and spatial clustering as qualitative evidence of pathway activity; pathways with minimal variation across clusters or no spatial coherence may indicate weak or artifact enrichment.

## Related tools

- **fgsea** (Compute GESECA enrichment scores on feature loadings matrix to be visualized on the reduction) — https://github.com/ctlab/fgsea
- **Seurat** (Host the single-cell object, store dimensionality reductions, manage cell metadata and annotations for faceting)
- **ggplot2** (Generate publication-quality reduction plots with continuous color scales and faceting by cell type)
- **msigdbr** (Retrieve pathway gene sets (e.g., KEGG_LEGACY) for input to GESECA)

## Examples

```
E <- obj@reductions$pca.rev@feature.loadings; gesecaRes <- geseca(pathways, E, minSize=5, maxSize=500, center=FALSE, eps=1e-100); plotCoregulationProfileReduction(obj, features=rownames(gesecaRes)[1:10], reduction='tsne')
```

## Evaluation signals

- Pathway scores show clear spatial or categorical variation across cell types; expected pathways cluster in predicted cell populations with high color intensity.
- tSNE/reduction coordinates are concordant with cell type annotations (i.e., cells of the same type occupy nearby regions in the plot).
- Pathways with known biology in the cell type (e.g., lysosomal pathways in foamy macrophages) display strong signal; pathways unrelated to the cell type show minimal or random signal.
- No visual artifacts such as uniform coloring, extreme outliers, or bleeding of scores across unrelated cell populations that would suggest normalization or filtering issues.
- Consistent ranking of top pathways across replicates or independent datasets of the same cell type, if available.

## Limitations

- Visual interpretation is qualitative; spatial overlap does not prove causal dependency. Statistical testing (e.g., correlation between pathway score and cell-type marker expression) is recommended for validation.
- Reverse PCA and GESECA assume linear relationships in the feature loading space; non-linear pathway interactions may not be captured.
- Dimensionality reduction (tSNE, UMAP) is itself lossy and parameter-dependent; changing perplexity, n_neighbors, or random seed can alter apparent spatial relationships.
- Large pathway sets or overlapping pathways can produce busy or difficult-to-interpret plots; pre-filtering by significance or functional relevance is advisable.
- Cell type annotations affect interpretation; misannotated or mixed cell clusters will produce misleading pathway-to-type associations.

## Evidence

- [methods] Extract feature loadings from reverse PCA, run GESECA on pathways, generate plotCoregulationProfileReduction plots colored by pathway score, faceted by cell type.: "Run reverse PCA (rev.pca=TRUE) on SCTransform-normalized matrix with npcs=50, extracting feature loadings matrix E. Load KEGG_LEGACY pathways from MSigDB using msigdbr. Run geseca(pathways, E,"
- [methods] Validation: KEGG_LEISHMANIA_INFECTION enriched in non-foamy intimal macrophages, KEGG_LYSOSOME in foamy intimal macrophages.: "confirming KEGG_LEISHMANIA_INFECTION prominence in non-foamy intimal macrophages and KEGG_LYSOSOME in foamy intimal macrophages"
- [readme] fgsea README: P-value estimation uses adaptive multi-level split Monte-Carlo scheme for accurate pathway enrichment.: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme"
- [intro] fgsea allows accurate calculation of arbitrarily low GSEA P-values.: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
