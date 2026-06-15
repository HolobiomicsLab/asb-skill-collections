---
name: pathway-enrichment-statistical-ranking
description: Use when you have a preranked gene list (e.g., genes sorted by log2 fold-change, t-statistic, or other continuous metric) and a collection of gene sets or biological pathways, and you need to determine which pathways are significantly over-represented among highly-ranked genes (positive enrichment).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0203
  tools:
  - fgsea
  - R
  - ggplot2
  - data.table
  - reactome.db
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

# pathway-enrichment-statistical-ranking

## Summary

Rank gene pathways by statistical significance using fast preranked gene set enrichment analysis (GSEA) to identify which biological pathway gene sets are most enriched at the top or bottom of a ranked gene list. This skill enables computation of arbitrarily low P-values for pathway collections using an adaptive multi-level Monte Carlo scheme.

## When to use

You have a preranked gene list (e.g., genes sorted by log2 fold-change, t-statistic, or other continuous metric) and a collection of gene sets or biological pathways, and you need to determine which pathways are significantly over-represented among highly-ranked genes (positive enrichment) or lowly-ranked genes (negative enrichment). Use this skill when standard GSEA P-value bounds (default eps=1e-10) are insufficient and you need to estimate P-values more accurately.

## When NOT to use

- Your input is an unranked gene list or unranked expression matrix; you need to compute ranking scores first (e.g., via differential expression analysis).
- Your gene sets are not well-defined or have extreme size distributions (most pathways much smaller than minSize or larger than maxSize).
- You need pathway analysis on raw count data without prior ranking; use GESECA (gene set enrichment from expression counts analysis) instead.

## Inputs

- preranked gene statistics (named numeric vector: gene IDs → ranking scores)
- pathway collection (list of character vectors, each containing gene identifiers for one pathway)
- minSize threshold (integer, e.g. 15)
- maxSize threshold (integer, e.g. 500)
- eps parameter (numeric: 1e-10 for default lower bound, 0 for adaptive refinement)

## Outputs

- fgseaRes data.table with columns: pathway, pval, padj, log2err, ES, NES, size
- enrichment plot (ggplot2 object showing running sum for one pathway)
- GSEA table plot (heatmap of top pathways ranked by statistical significance)

## How to apply

Load the fgsea R package along with your preranked gene statistics (a named vector where names are gene identifiers and values are ranking scores) and pathway definitions (a list of gene sets). Call fgsea() with parameters: pathways, stats, minSize (typically 15), maxSize (typically 500), and eps (default 1e-10 for speed, or eps=0 for adaptive multi-level Monte Carlo refinement to estimate lower P-values). The function returns a data.table with enrichment scores (ES), normalized enrichment scores (NES), P-values, and adjusted P-values for each pathway. Sort results by pval to identify top-ranked pathways. Use plotEnrichment() to visualize a single pathway's running sum, and plotGseaTable() to create a summary heatmap of top upregulated (ES > 0) and downregulated (ES < 0) pathways. The adaptive scheme adjusts Monte Carlo sampling precision automatically; setting eps=0 disables the lower bound and enables exact refinement for pathways with very significant signals.

## Related tools

- **fgsea** (Primary R package that computes fast preranked gene set enrichment with adaptive multi-level Monte Carlo P-value estimation) — https://github.com/ctlab/fgsea
- **data.table** (Used for fast manipulation and sorting of enrichment results)
- **ggplot2** (Used for generating enrichment plots and GSEA table visualizations)
- **reactome.db** (Optional source of curated biological pathway definitions for enrichment analysis)

## Examples

```
library(fgsea); data(examplePathways); data(exampleRanks); fgseaRes <- fgsea(pathways=examplePathways, stats=exampleRanks, minSize=15, maxSize=500); head(fgseaRes[order(pval),])
```

## Evaluation signals

- P-values are monotonically decreasing when sorted by pval column; no NaN or negative P-values are present.
- Adjusted P-values (padj) are ≥ corresponding pval (Benjamini-Hochberg correction monotonicity).
- Enrichment scores (ES) range from -1 to +1; normalized enrichment scores (NES) scale ES by phenotype label shuffling permutation variance.
- Pathways with identical ES values between eps=1e-10 and eps=0 runs have consistent rankings; eps=0 produces lower (more significant) P-values without changing ES or NES.
- Enrichment plots show running sum crossing the x-axis only at ES extrema; pathway size (number of genes) matches the count of matching genes in the input statistics vector.

## Limitations

- Default eps=1e-10 lower bound means pathways with extremely strong signals may report pval=1e-10 rather than true lower values; use eps=0 for more precise P-values at computational cost.
- Results depend critically on the ranking metric used; poor quality ranking scores (e.g., from underpowered differential expression) yield unreliable enrichment statistics.
- Pathway definitions are external; results are only as accurate as the gene set annotations provided (e.g., species mismatch, outdated pathway databases).
- Tied ranks in the input statistics can affect ES estimation; consider adding small random noise or using continuous scores where possible.

## Evidence

- [readme] fgsea allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
- [readme] P-value estimation uses adaptive multi-level split Monte-Carlo scheme: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme"
- [readme] fgsea has a default lower bound eps=1e-10; setting eps=0 enables adaptive refinement: "fgsea has a default lower bound eps=1e-10 for estimating P-values. If you need to estimate P-value more accurately, you can set the eps argument to zero"
- [methods] Workflow includes running fgsea with minSize and maxSize, sorting by pval, and creating enrichment plots: "Run fgsea() with pathways=examplePathways, stats=exampleRanks, minSize=15, maxSize=500, and default eps=1e-10. Sort the resulting fgseaRes table by pval and display the top enriched pathways."
- [methods] Results distinguish upregulated (ES > 0) and downregulated (ES < 0) pathways ordered by p-value: "Identify top 10 upregulated pathways (ES > 0) and top 10 downregulated pathways (ES < 0) ordered by p-value. Create a GSEA table plot using plotGseaTable()"
