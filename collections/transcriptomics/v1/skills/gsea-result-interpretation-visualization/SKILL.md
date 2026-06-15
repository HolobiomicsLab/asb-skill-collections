---
name: gsea-result-interpretation-visualization
description: 'Use when after running fgsea() on a preranked gene list when you need to: (1) identify which pathways are most significantly enriched or depleted (lowest p-values), (2) distinguish between upregulated pathways (ES > 0) and downregulated pathways (ES < 0) within your gene set collection, (3).'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3518
  tools:
  - fgsea
  - R
  - ggplot2
  - data.table
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

# GSEA Result Interpretation and Visualization

## Summary

Interpret and visualize gene set enrichment analysis (GSEA) results by sorting pathways by statistical significance, identifying directional enrichment patterns (upregulated vs. downregulated), and generating publication-quality enrichment plots and GSEA tables. This skill transforms raw fgsea output into actionable biological insights through selective pathway ranking and comparative visualization.

## When to use

Apply this skill after running fgsea() on a preranked gene list when you need to: (1) identify which pathways are most significantly enriched or depleted (lowest p-values), (2) distinguish between upregulated pathways (ES > 0) and downregulated pathways (ES < 0) within your gene set collection, (3) communicate results through publication-ready figures, or (4) prioritize pathways for downstream biological validation or mechanistic investigation.

## When NOT to use

- Input gene statistics are not preranked (not in descending order by effect size or statistical significance) — use rank conversion first
- Gene set collection contains <5 pathways or pathways with <15 genes each — fgsea requires minSize and maxSize filtering; visualization benefit is limited with very small collections
- Goal is gene-level interpretation rather than pathway-level summary — use alternative tools for individual gene ranking or network visualization

## Inputs

- fgseaRes table (output from fgsea() with columns: pathway, pval, padj, ES, NES, size, log2err)
- exampleRanks or equivalent named numeric vector (gene-level statistics, typically log2 fold-change or t-statistic, sorted in descending order)
- examplePathways or equivalent list of character vectors (gene set collection, where each element is a pathway name and value is a vector of gene symbols)

## Outputs

- Sorted fgseaRes table (ranked by pval, stratified by ES sign)
- Enrichment plot (ggplot2 object showing running sum curve for a single pathway)
- GSEA table plot (ggplot2 object showing top pathways with running sums and statistics arranged as rows)

## How to apply

Sort the fgseaRes table by pval (ascending) to identify the top statistically significant pathways, then stratify by enrichment score (ES) sign to separate upregulated (ES > 0) from downregulated (ES < 0) pathways. Select top 10 pathways from each direction ordered by p-value to create a balanced, focused view of directional pathway activity. For individual pathway validation, use plotEnrichment() to visualize the running sum of the enrichment score across the preranked gene list, which shows where genes in that pathway cluster relative to the ranked statistics. For a comprehensive summary, generate a GSEA table plot using plotGseaTable() with the combined top pathways, the original gene-level statistics, the fgsea results table, and gseaParam=0.5, which displays normalized enrichment scores (NES), p-values, and per-pathway running sum curves side-by-side for visual comparison. These visualizations provide both statistical (p-value, NES) and visual (enrichment curve position) evidence of pathway activity strength and direction.

## Related tools

- **fgsea** (Computes GSEA statistics (pval, ES, NES) on preranked gene lists; output table is the input to interpretation and visualization) — https://github.com/ctlab/fgsea
- **ggplot2** (Rendering engine for enrichment plots and GSEA table plots returned by plotEnrichment() and plotGseaTable())
- **data.table** (Efficient sorting and subsetting of fgseaRes table by pval and ES for pathway stratification and selection)

## Examples

```
fgseaRes <- fgsea(pathways = examplePathways, stats = exampleRanks, minSize = 15, maxSize = 500); topPathwaysUp <- fgseaRes[ES > 0][head(order(pval), n=10), pathway]; topPathwaysDown <- fgseaRes[ES < 0][head(order(pval), n=10), pathway]; plotGseaTable(examplePathways[c(topPathwaysUp, rev(topPathwaysDown))], exampleRanks, fgseaRes, gseaParam=0.5)
```

## Evaluation signals

- fgseaRes table is sorted by pval (ascending) with smallest p-values at top; spot-check that first row has pval ≤ 1e-10 or lower (depending on eps parameter used)
- Top upregulated pathways (ES > 0) and top downregulated pathways (ES < 0) are clearly distinct and non-overlapping in the selected pathway list
- plotEnrichment() output shows a clearly defined peak (positive ES) or valley (negative ES) in the running sum curve, indicating non-random gene clustering in that pathway
- plotGseaTable() output displays all selected pathways as rows with consistent x-axis (rank position) and visual alignment of running sum curves; NES and pval columns are readable and correctly ordered
- The combined top pathway list contains exactly 10 upregulated + 10 downregulated pathways (or fewer if fewer than 10 in each direction exist in the original table)

## Limitations

- fgsea uses adaptive multi-level Monte-Carlo p-value estimation with default eps=1e-10; very small p-values (< 1e-10) are reported as '1e-10' unless eps is set to 0, which increases computational cost
- Visualization clarity degrades if >20 pathways are plotted simultaneously in plotGseaTable(); the skill assumes selection of top pathways per direction to maintain readability
- ES and NES are relative to the gene set collection and preranking method; interpretation requires biological knowledge of pathway function and context (e.g., cell type, treatment, disease state)
- The skill does not address multiple testing correction beyond padj; practitioners must decide on FDR threshold (e.g., padj < 0.05) independently

## Evidence

- [methods] Sort the resulting fgseaRes table by pval and display the top enriched pathways: "Sort the resulting fgseaRes table by pval and display the top enriched pathways."
- [methods] Identify top 10 upregulated and downregulated pathways stratified by ES sign: "Identify top 10 upregulated pathways (ES > 0) and top 10 downregulated pathways (ES < 0) ordered by p-value."
- [methods] Generate enrichment plot for individual pathway validation: "Generate an enrichment plot for the 5991130_Programmed_Cell_Death pathway using plotEnrichment() with exampleRanks."
- [methods] Create a GSEA table plot for multi-pathway summary: "Create a GSEA table plot using plotGseaTable() with the combined top pathways, exampleRanks, fgseaRes, and gseaParam=0.5."
- [readme] fgsea allows quick and accurate GSEA P-value calculation: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets."
- [readme] ES stratification for directional pathway interpretation: "topPathwaysUp <- fgseaRes[ES > 0][head(order(pval), n=10), pathway]
topPathwaysDown <- fgseaRes[ES < 0][head(order(pval), n=10), pathway]"
