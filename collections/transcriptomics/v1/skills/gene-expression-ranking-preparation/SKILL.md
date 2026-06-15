---
name: gene-expression-ranking-preparation
description: Use when you have a gene expression matrix (RNA-seq counts, microarray intensities, or normalized expression values) and need to perform gene set enrichment analysis on preranked gene lists. Use this skill when you want to rank genes by a univariate statistic (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0203
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

# gene-expression-ranking-preparation

## Summary

Prepare ranked gene statistics from expression data for preranked gene set enrichment analysis (GSEA). This skill transforms raw or normalized expression matrices into per-gene summary statistics (typically log fold-change or t-statistics) suitable for input to fast GSEA algorithms like fgsea.

## When to use

You have a gene expression matrix (RNA-seq counts, microarray intensities, or normalized expression values) and need to perform gene set enrichment analysis on preranked gene lists. Use this skill when you want to rank genes by a univariate statistic (e.g., mean expression, log fold-change, or t-statistic) before testing pathway or gene set enrichment, rather than performing rank-free enrichment.

## When NOT to use

- Gene expression data is already ranked and validated for GSEA input — skip directly to fgsea() function call.
- You need rank-free enrichment (e.g., Fisher's exact test on gene sets without pre-ranking) — use alternative enrichment methods.
- Input is a precomputed ranked gene list from a prior GSEA run — validate and use directly rather than re-ranking.

## Inputs

- gene expression matrix (numeric matrix, ExpressionSet, or data frame with genes as rows, samples as columns)
- sample metadata or group labels (optional, for computing contrasts)
- gene annotations or identifier mapping (optional, for handling duplicates or cross-references)

## Outputs

- ranked gene statistics (named numeric vector: gene identifiers → ranking statistic)
- filtered gene list (genes passing expression/quality thresholds)
- summary statistics (e.g., mean expression per gene, log fold-change)

## How to apply

Load the gene expression matrix (e.g., exampleExpressionMatrix or a normalized ExpressionSet object) and compute a per-gene ranking statistic. Common approaches include: (1) computing mean expression across samples, (2) calculating log fold-change between conditions, or (3) deriving t-statistics from differential expression. Remove or filter lowly expressed genes (e.g., retain the top 12,000 by mean expression) and remove duplicated gene identifiers. The resulting ranked vector (gene names as names, numeric statistic as values) is then passed to fgsea() as the `stats` parameter alongside a pathway collection (examplePathways or custom pathways list). Set fgsea parameters such as minSize=15, maxSize=500 to filter out pathways by member count, and eps=1e-10 (or eps=0 for higher precision) to control P-value estimation accuracy.

## Related tools

- **fgsea** (Accepts ranked gene statistics as input (stats parameter) for fast preranked GSEA) — https://github.com/ctlab/fgsea
- **data.table** (Efficient manipulation and filtering of gene expression matrices and statistics tables)
- **R** (Programming environment for expression data processing and ranking workflows)

## Examples

```
data(exampleExpressionMatrix); data(examplePathways); es <- es[!duplicated(fData(es)$`Gene ID`), ]; es <- es[head(order(rowMeans(exprs(es)), decreasing=TRUE), 12000), ]; fgseaRes <- fgsea(pathways = examplePathways, stats = exampleRanks, minSize = 15, maxSize = 500)
```

## Evaluation signals

- Ranked vector has unique gene identifiers as names and numeric ranking statistics as values (no duplicates, no empty names).
- All genes in the ranked vector are present in the pathway collection or pathway members are a subset of the ranked genes (no 'gene not found' warnings from fgsea).
- Distribution of ranking statistic is continuous and spans a reasonable range (not all zeros, not all identical); verify with summary() or hist().
- After fgsea() execution with the ranked vector, p-values and normalized enrichment scores (NES) are computed and sorted; top pathways have p-val < 0.05 and NES magnitude > 1 (typical thresholds).
- Pathway size (number of members in pathway that overlap the ranked gene list) falls within the specified minSize and maxSize bounds for all reported pathways.

## Limitations

- Gene duplicate handling must be explicit: duplicated gene identifiers must be resolved (e.g., by summing expression or selecting highest-mean isoform) before ranking; fgsea will use only the first occurrence if passed a named vector.
- Ranking statistic sensitivity depends on sample size and experimental design; low-power studies may produce unreliable ranks. No formal power calculation is provided in the fgsea package.
- Genes with zero or very low expression across all samples contribute noise to the ranking; filtering (e.g., retaining top 12,000 genes by mean expression) is recommended but the cutoff is dataset-dependent.
- Gene identifier format must match pathway collection (e.g., if pathways use Entrez IDs, the ranked vector must use Entrez IDs, not gene symbols), otherwise pathway members will not be found.

## Evidence

- [readme] Loading example pathways and gene-level statistics: "Loading example pathways and gene-level statistics:
```{r}
data(examplePathways)
data(exampleRanks)
```"
- [methods] Filter to top genes by mean expression: "Filter to top genes by mean expression  [section=methods; evidence='es <- es[head(order(rowMeans(exprs(es)), decreasing=TRUE), 12000), ]']"
- [methods] Remove duplicated genes: "Remove duplicated genes  [section=methods; evidence='es <- es[!duplicated(fData(es)$`Gene ID`), ]']"
- [readme] fgsea P-value estimation capability: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
- [readme] fgsea function call with ranked statistics: "fgseaRes <- fgsea(pathways = examplePathways, 
                  stats    = exampleRanks,
                  minSize  = 15,
                  maxSize  = 500)"
