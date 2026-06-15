---
name: pathway-set-enrichment-analysis
description: Use when you have normalized gene expression data (log-transformed, quantile-normalized) from a time-course or case-control experiment, a ranked gene statistic (e.g., mean expression, differential expression score), and a collection of curated gene sets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_2269
  tools:
  - GEOquery
  - limma
  - fgsea
  - msigdbr
  - ggplot2
  - R
  - data.table
derived_from:
- doi: 10.1101/060012
  title: fgsea
evidence_spans:
- library(GEOquery)
- exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method="quantile")
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

# pathway-set-enrichment-analysis

## Summary

Fast preranked gene set enrichment analysis (GSEA) using adaptive Monte-Carlo P-value estimation to quantify whether predefined gene sets show significant coordinated expression changes in time-course or comparative transcriptomics experiments. Apply this skill when you have a ranked list of genes (by fold-change, t-statistic, or log2 expression) and curated pathway/gene set collections, and need to identify which biological processes or molecular signatures are significantly activated or repressed.

## When to use

You have normalized gene expression data (log-transformed, quantile-normalized) from a time-course or case-control experiment, a ranked gene statistic (e.g., mean expression, differential expression score), and a collection of curated gene sets (e.g., HALLMARK pathways from MSigDB, Reactome). Use this skill to test whether specific pathways show significant enrichment in your ranked genes, especially when you need to estimate very low P-values (< 1e-10) with high accuracy using Monte-Carlo estimation.

## When NOT to use

- Input gene expression matrix has not been log-transformed or quantile-normalized; fgsea requires pre-normalized, comparable expression values across samples.
- You have <5,000 genes or >50,000 genes in your filtered expression matrix; fgsea works optimally on moderately-sized ranked lists (typical range 10,000–20,000 genes).
- Your gene sets are very small (<15 genes) or very large (>500 genes); these are filtered out by minSize and maxSize parameters and will not be tested.

## Inputs

- Normalized log-transformed gene expression matrix (rows=genes, columns=samples)
- Gene annotation table with Gene IDs and identifiers
- Ranked gene statistics (e.g., mean expression per gene, t-statistic, or log2 fold-change)
- Named list of gene sets (e.g., HALLMARK pathways from msigdbr converted to list split by pathway)

## Outputs

- fgsea/geseca results table with columns: pathway, pval, padj, log2err, ES (enrichment score), NES (normalized ES), size
- Sorted results by P-value with top enriched pathways and their temporal activation patterns
- Enrichment plots and GSEA table visualizations for selected pathways

## How to apply

Load preprocessed gene expression matrix and filter to remove duplicates (by Gene ID), empty or '///' identifiers, and retain top genes by mean expression (e.g., top 12,000). Load curated gene set collections (e.g., HALLMARK from msigdbr with species and collection parameters) and convert to a named list split by pathway name. Run fgsea or geseca with parameters minSize=15 and maxSize=500 to exclude very small or very large pathways that may be statistically unstable. Set eps=0.0 if you require arbitrarily low P-values; the default eps=1e-10 is sufficient for most applications. Sort results by adjusted P-value and extract enrichment scores (ES), normalized ES (NES), and temporal activation patterns for top pathways. Validate that reported pathway scores and p-values match expected ranges and temporal patterns from literature or prior experiments.

## Related tools

- **fgsea** (Core R package for fast preranked GSEA using adaptive multi-level split Monte-Carlo scheme to estimate arbitrarily low P-values) — https://github.com/ctlab/fgsea
- **limma** (Provides quantile normalization via normalizeBetweenArrays() to normalize log-transformed expression matrices before ranking)
- **msigdbr** (Retrieves curated gene set collections (e.g., HALLMARK, Reactome) filtered by species and collection type; converts to named list split by pathway)
- **GEOquery** (Loads public gene expression datasets (e.g., GSE200250) via getGEO() and extracts sample metadata and expression matrices)
- **data.table** (Efficient data manipulation for sorting results by p-value and extracting top pathways)
- **ggplot2** (Visualization of enrichment plots (plotEnrichment) and GSEA table plots (plotGseaTable) for publication-quality figures)

## Examples

```
fgseaRes <- fgsea(pathways = examplePathways, stats = exampleRanks, eps = 0.0, minSize = 15, maxSize = 500); head(fgseaRes[order(pval), ])
```

## Evaluation signals

- Reported P-values and adjusted P-values (padj) are consistent with expected significance thresholds (e.g., padj < 0.05) for known pathway activations documented in the original publication.
- Enrichment scores (ES) and normalized enrichment scores (NES) match expected ranges and temporal patterns; e.g., HALLMARK_E2F_TARGETS and HALLMARK_HYPOXIA show expected activation at specific time points in Th2 differentiation.
- Results remain reproducible across multiple runs with identical parameters (fgsea uses pseudo-random number generation; set seed for deterministic results).
- Top enriched pathways are biologically relevant to the experimental context (e.g., cell cycle pathways in proliferating cells, immune pathways in Th2 cells); unexpected top pathways may indicate insufficient filtering or confounding signals.
- Gene set size distribution in results is balanced (minSize and maxSize are respected); no pathways appear below minSize=15 or above maxSize=500.

## Limitations

- P-value estimation depends on Monte-Carlo sampling; very low P-values (< 1e-20) require setting eps=0.0, which increases computation time significantly.
- Results are sensitive to gene filtering thresholds (e.g., top 12,000 genes by mean expression); different cutoffs may yield different top pathways.
- fgsea assumes genes in the input ranked list are independent; gene sets with strong within-set correlation may have inflated or deflated enrichment scores.
- P-value accuracy requires that the number of permutations be sufficient; adaptive multi-level splitting may terminate early if adaptive thresholds are not well-tuned, leading to less precise P-value estimates.
- No changelog tracking available for reproducibility; version control and explicit parameter documentation are essential for replication.

## Evidence

- [intro] fgsea allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
- [intro] P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme"
- [methods] geseca analysis workflow includes loading expression matrix, applying log and quantile normalization, filtering genes by duplication and expression, loading pathways, and running geseca with minSize and maxSize parameters: "Apply log and quantile normalization using normalizeBetweenArrays from limma with method='quantile'. 3. Filter the expression matrix by removing duplicate genes based on Gene ID, removing genes with"
- [readme] fgsea default P-value lower bound is 1e-10; setting eps=0.0 estimates P-values more accurately: "fgsea has a default lower bound `eps=1e-10` for estimating P-values. If you need to estimate P-value more accurately, you can set the `eps` argument to zero in the `fgsea` function"
- [readme] Visualization of enrichment results using plotEnrichment and plotGseaTable functions for selected pathways: "One can make an enrichment plot for a pathway: plotEnrichment(examplePathways, exampleRanks) + labs(title=...). Or make a table plot for a bunch of selected pathways:"
