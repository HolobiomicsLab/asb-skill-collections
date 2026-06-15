---
name: gene-set-enrichment-analysis
description: Use when when you have a ranked list of gene-level statistics (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1834
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_0219
  - http://edamontology.org/topic_3518
  tools:
  - fgsea
  - R
  - ggplot2
  - msigdbr
  - data.table
  - geseca
  - Seurat
derived_from:
- doi: 10.1101/060012
  title: fgsea
evidence_spans:
- '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'
- gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)
- R-package for fast preranked gene set enrichment analysis
- fgsea is an R-package for fast preranked gene set enrichment analysis
- library(ggplot2)
- ggplot(data=merge(...)) + geom_point(aes(x=logPvalFull, y=logPvalRed))
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

# gene-set-enrichment-analysis

## Summary

Fast preranked gene set enrichment analysis (GSEA) using adaptive multi-level split Monte-Carlo P-value estimation to calculate arbitrarily low GSEA P-values for gene set collections. This skill enables rapid identification of significantly enriched or depleted pathways in ranked gene lists across arbitrarily precise P-value thresholds.

## When to use

When you have a ranked list of gene-level statistics (e.g., log fold-change, t-statistic, or other continuous score per gene) and a collection of gene sets (pathways, gene ontology terms, or custom gene lists), and need to test whether genes in each set are randomly distributed in the ranking or clustered toward high or low values. Use this skill when P-value precision matters (e.g., eps=0 for exact mode vs. eps=1e-10 for 10 decimal places) or when comparing enrichment across multiple conditions or cell types.

## When NOT to use

- Input gene statistics are not ranked or continuous (e.g., binary presence/absence matrix); use ORA (over-representation analysis) instead.
- Gene sets are very small (< 15 genes by default) or very large (> 500 genes by default) and filtering is not appropriate for your biology.
- You need to account for gene expression covariance or direction-agnostic pathway scoring; use GESECA (Gene Set Expression Change Analysis) instead, which operates on feature loadings from dimensionality reduction.

## Inputs

- ranked gene statistics (named numeric vector with gene identifiers as names)
- gene set collection (named list of character vectors, each vector listing gene members of a pathway)
- minimum pathway size threshold (integer, e.g., 15)
- maximum pathway size threshold (integer, e.g., 500)
- P-value precision parameter eps (numeric, e.g., 1e-10 or 0)

## Outputs

- fgseaRes data.table with columns: pathway, pval, padj, log2err, ES, NES, size
- enrichment plot (ggplot object) showing position of pathway members in ranked list
- GSEA table plot (ggplot object) visualizing enrichment scores and NES across multiple pathways

## How to apply

Load ranked gene statistics (e.g., exampleRanks: a named numeric vector sorted by score) and gene set pathways (e.g., examplePathways: a named list of character vectors, one per pathway). Call fgsea() with pathways, stats, minSize (e.g., 15), maxSize (e.g., 500), and eps parameter (default 1e-10 for speed; set to 0 for arbitrarily low P-values via adaptive refinement). The adaptive multi-level split Monte-Carlo scheme automatically adjusts sampling depth to achieve the requested precision. Sort results by pval and filter by effect size direction (ES > 0 for upregulated, ES < 0 for downregulated pathways). Visualize top pathways using plotEnrichment() for single pathways or plotGseaTable() for multiple pathways with gseaParam controlling the visualization resolution.

## Related tools

- **fgsea** (Core R package implementing fast preranked GSEA with adaptive multi-level Monte-Carlo P-value estimation) — https://github.com/ctlab/fgsea
- **data.table** (Efficient data manipulation and sorting of enrichment results)
- **ggplot2** (Visualization of enrichment plots and GSEA tables)
- **geseca** (Variant of fgsea for gene set analysis on reduced dimensionality spaces (e.g., PCA loadings) without rank assumption) — https://github.com/ctlab/fgsea
- **msigdbr** (Retrieve curated pathway collections (e.g., KEGG, Reactome) for use as input gene sets)
- **Seurat** (Optional: normalize scRNA-seq expression, run dimensionality reduction for GESECA variant)

## Examples

```
library(fgsea); data(examplePathways); data(exampleRanks); fgseaRes <- fgsea(pathways = examplePathways, stats = exampleRanks, minSize = 15, maxSize = 500, eps = 1e-10); head(fgseaRes[order(pval)])
```

## Evaluation signals

- Returned fgseaRes table contains valid pval column with values ≥ 0 and ≤ 1, and padj (adjusted P-values) also in [0, 1] with padj ≥ pval
- Effect size (ES) values in fgseaRes are bounded in [-1, 1] and NES values reflect normalized enrichment relative to pathway permutations
- log2err column in fgseaRes is NA or zero for eps=1e-10 (fixed lower bound) and contains positive values (log2 fold-change in precision) when eps=0 for top pathways
- Pathways with small size (e.g., < minSize) or large size (e.g., > maxSize) do not appear in results; minSize and maxSize filtering is enforced
- Enrichment plots generated by plotEnrichment() show cumulative distribution of ranked statistics with a clear peak/valley at the location of pathway members, matching the sign of ES
- Top 10 upregulated (ES > 0) and top 10 downregulated (ES < 0) pathways in plotGseaTable() visualization are visually distinct and ordered by ascending pval

## Limitations

- Default eps=1e-10 provides a lower bound on P-value precision; arbitrarily low P-values require eps=0, which increases runtime (can take seconds to minutes for large gene set collections).
- P-value estimation is based on Monte-Carlo sampling, so small differences in results across runs are expected unless a random seed is explicitly set.
- Requires minimum pathway size (default minSize=15) to avoid noise; very small pathways may be filtered out even if biologically relevant.
- Results assume gene-level statistics are independently distributed and ranked; violations (e.g., correlated genes, tied ranks) may inflate or deflate enrichment scores.
- No built-in multiple-testing correction beyond Benjamini-Hochberg FDR; users should consider domain-specific significance thresholds (e.g., padj < 0.01).

## Evidence

- [readme] fgsea is an R-package for fast preranked gene set enrichment analysis (GSEA): "fgsea is an R-package for fast preranked gene set enrichment analysis (GSEA). This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets."
- [readme] Adaptive multi-level split Monte-Carlo enables arbitrarily low P-values: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme."
- [readme] Default eps=1e-10 provides lower-bound precision; eps=0 enables exact refinement: "fgsea has a default lower bound eps=1e-10 for estimating P-values. If you need to estimate P-value more accurately, you can set the eps argument to zero in the fgsea function."
- [readme] fgsea() function signature and parameter ranges: "fgsea(pathways = examplePathways, stats = exampleRanks, minSize = 15, maxSize = 500)"
- [readme] Enrichment plots and GSEA table plots for visualization: "plotEnrichment(examplePathways[["5991130_Programmed_Cell_Death"]], exampleRanks) ... Or make a table plot for a bunch of selected pathways: plotGseaTable(examplePathways[topPathways], exampleRanks,"
- [readme] Filtering by effect size direction identifies upregulated vs downregulated pathways: "topPathwaysUp <- fgseaRes[ES > 0][head(order(pval), n=10), pathway]; topPathwaysDown <- fgseaRes[ES < 0][head(order(pval), n=10), pathway]"
- [other] Task 004 demonstrates GESECA variant for scRNA-seq analysis on PCA-reduced feature space: "Run geseca(pathways, E, minSize=5, maxSize=500, center=FALSE, eps=1e-100) on reduced feature space, producing enrichment scores and p-values."
