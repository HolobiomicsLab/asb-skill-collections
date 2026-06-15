---
name: multiple-testing-correction-visualization
description: 'Use when after running fgsea() on a preranked gene list and obtaining a results table with raw pval, padj, ES, NES, and size columns, use this skill to: (1) subset results to top enriched pathways (e.g., top 10 upregulated ES > 0 and top 10 downregulated ES < 0 by adjusted p-value);'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_0092
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

# multiple-testing-correction-visualization

## Summary

Visualize corrected P-values and effect sizes from gene set enrichment analysis results as a ranked table plot, enabling rapid assessment of pathway significance across multiple simultaneous hypothesis tests. This skill applies multiple-testing correction (adjusted P-values) alongside enrichment effect sizes (ES, NES) to identify the most robust and biologically meaningful gene set associations.

## When to use

After running fgsea() on a preranked gene list and obtaining a results table with raw pval, padj, ES, NES, and size columns, use this skill to: (1) subset results to top enriched pathways (e.g., top 10 upregulated ES > 0 and top 10 downregulated ES < 0 by adjusted p-value); (2) generate a combined ranked visualization; (3) inspect effect size direction and magnitude alongside corrected significance. Particularly useful when you have many gene sets (e.g., >100 pathways) and need to distinguish statistical significance (padj) from biological effect magnitude (ES/NES).

## When NOT to use

- Input fgseaRes table is empty or contains no significant pathways (padj ≥ threshold) — visualization will be uninformative.
- Gene set collection is very small (< 10 total pathways) — multiple-testing correction is unnecessary and table plot becomes redundant with simple summary.
- You have not yet run fgsea() or lack a ranked gene list and pathway definitions — this skill assumes fgsea() has been executed and padj/ES have been computed.

## Inputs

- fgseaRes data.table (output from fgsea with columns: pathway, pval, padj, log2err, ES, NES, size)
- examplePathways list (named character list of gene sets / pathways)
- exampleRanks named numeric vector (preranked gene-level statistics, e.g., t-statistics or log fold-change)

## Outputs

- plotGseaTable ggplot object (combined table visualization of top enriched pathways with ES profiles and p-value ranks)
- subsetted pathway names vector (character vector of selected top pathways for visualization)

## How to apply

Extract the top 10 upregulated pathways (ES > 0, lowest padj) and top 10 downregulated pathways (ES < 0, lowest padj) from the fgseaRes table. Combine these into a single vector of pathway names, reversing the order of downregulated pathways to arrange them visually. Call plotGseaTable() with the subset of examplePathways, the ranked gene statistics (exampleRanks), the full fgseaRes table, and gseaParam=0.5 (controls the weighting of the GSEA statistic visualization). The resulting plot displays pathways as rows, ranked by adjusted p-value significance, with barplots showing running enrichment scores and effect direction. Use this to confirm that pathways with lowest padj also have biologically meaningful ES magnitudes (typically |ES| > 0.5), validating the multiple-testing correction.

## Related tools

- **fgsea** (Preranked gene set enrichment analysis; computes raw pval, padj (via Benjamini-Hochberg), ES, NES, and size for each pathway to feed downstream visualization) — https://github.com/ctlab/fgsea
- **ggplot2** (Graphics engine underlying plotGseaTable() for rendering table and enrichment profiles)
- **data.table** (Efficient subsetting and sorting of fgseaRes by ES and padj to extract top upregulated and downregulated pathways)

## Examples

```
topPathwaysUp <- fgseaRes[ES > 0][head(order(padj), n=10), pathway]
topPathwaysDown <- fgseaRes[ES < 0][head(order(padj), n=10), pathway]
topPathways <- c(topPathwaysUp, rev(topPathwaysDown))
plotGseaTable(examplePathways[topPathways], exampleRanks, fgseaRes, gseaParam=0.5)
```

## Evaluation signals

- Resulting plotGseaTable shows ≥1 pathway with padj < 0.05 and |ES| > 0.4 (indicating statistical and biological significance after multiple-testing correction)
- Pathways are ranked left-to-right (or top-to-bottom) by increasing padj, confirming adjusted P-values drive the sort order
- Upregulated (ES > 0) and downregulated (ES < 0) pathways are visually separated and directional consistency is maintained across the plot
- Running enrichment score curves (barplots in rows) display coherent peaks aligned with top-ranked genes in exampleRanks, validating ES calculation
- Comparison of raw pval vs. padj columns shows inflation of padj (conservative adjustment), confirming Benjamini-Hochberg correction was applied

## Limitations

- plotGseaTable visualization becomes crowded if >20 pathways are plotted simultaneously; selection of top pathways is manual and may miss moderately significant pathway clusters.
- Multiple-testing correction via Benjamini-Hochberg controls FDR but may be overly conservative for very large pathway collections (>1000); consider alternative correction schemes if needed.
- Effect size (ES) and adjusted P-value can diverge: a pathway may have low padj but small |ES|, or high |ES| but marginal padj if sample/pathway size is small — visual inspection required to reconcile.
- gseaParam=0.5 is a default; users should validate that this weighting parameter is appropriate for their data and adjust if enrichment profiles appear distorted.

## Evidence

- [methods] Multiple-testing correction via adjusted P-values and ranked visualization: "Sort the resulting fgseaRes table by pval and display the top enriched pathways. Identify top 10 upregulated pathways (ES > 0) and top 10 downregulated pathways (ES < 0) ordered by p-value. Create a"
- [intro] fgsea allows accurate GSEA P-value estimation and correction: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
- [readme] Practical workflow for table plot visualization with gseaParam tuning: "topPathwaysUp <- fgseaRes[ES > 0][head(order(pval), n=10), pathway]
topPathwaysDown <- fgseaRes[ES < 0][head(order(pval), n=10), pathway]
topPathways <- c(topPathwaysUp,"
- [readme] Effect size and normalized effect size as interpretation metrics: "pathway pval padj log2err ES NES size"
