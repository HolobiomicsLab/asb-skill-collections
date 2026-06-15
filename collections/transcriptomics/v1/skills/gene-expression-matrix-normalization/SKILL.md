---
name: gene-expression-matrix-normalization
description: Use when when you have raw or unnormalized gene expression data from microarray experiments (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  tools:
  - GEOquery
  - limma
  - fgsea
  - msigdbr
  - ggplot2
  - R
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

# gene-expression-matrix-normalization

## Summary

Normalize microarray gene expression matrices using log transformation and quantile normalization to remove technical variation and enable consistent downstream pathway enrichment analysis. This skill prepares raw expression data for reliable GSEA calculations by standardizing distributions across samples.

## When to use

When you have raw or unnormalized gene expression data from microarray experiments (e.g., GSE200250 Th2 time-course samples) that will be used for gene set enrichment analysis or pathway scoring, and you need to remove technical batch effects and ensure comparability across samples before calculating enrichment statistics.

## When NOT to use

- Expression data is already log-transformed and quantile-normalized (e.g., from a processed GEO dataset marked as 'normalized')
- Input is pre-ranked gene statistics (log fold-change or t-statistic vectors) rather than a raw expression matrix—use preranked GSEA instead
- Single-sample analysis where cross-sample normalization is not applicable

## Inputs

- ExpressionSet object from GEO (containing raw or background-corrected intensity values)
- Numeric expression matrix with genes as rows and samples as columns

## Outputs

- Log2-transformed and quantile-normalized expression matrix
- Normalized ExpressionSet object with standardized intensities across samples

## How to apply

Load the ExpressionSet object from GEO using GEOquery::getGEO(), extract expression values with exprs(), apply log2 transformation to stabilize variance, then apply quantile normalization using limma::normalizeBetweenArrays() with method='quantile'. This two-step approach (log transform followed by quantile normalization) ensures that the distribution of expression values is comparable across all samples, which is critical for downstream GSEA/GESECA analysis where enrichment scores depend on consistent gene-level rankings. Verify that normalized values fall within expected ranges (typically log2-transformed intensities between 0–16 for microarray data) and that sample distributions are visually aligned in density plots.

## Related tools

- **GEOquery** (Load GSE microarray data and extract ExpressionSet objects from NCBI GEO)
- **limma** (Apply quantile normalization via normalizeBetweenArrays() with method='quantile')
- **fgsea** (Downstream tool that requires normalized expression matrices or ranked statistics for GESECA pathway analysis) — https://github.com/ctlab/fgsea

## Examples

```
library(limma); library(GEOquery); gse <- getGEO('GSE200250', AnnotGPL=TRUE); es <- gse[[1]]; exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method='quantile')
```

## Evaluation signals

- Normalized expression values are log2-transformed (typically in the range 0–16 for microarray microarray intensities after background correction)
- Quantile–quantile plots show aligned distributions across all samples after normalization
- Mean and variance of expression distributions are consistent across samples (verifiable via boxplots or density plots grouped by sample)
- Downstream GESECA enrichment scores for known pathway activations (e.g., HALLMARK_E2F_TARGETS, HALLMARK_HYPOXIA) fall within published ranges and show expected temporal activation patterns
- Duplicated genes and genes with missing or '///' identifiers have been removed before GSEA to avoid rank ties and invalid gene symbols

## Limitations

- Quantile normalization assumes that the majority of genes are not differentially expressed across samples; it may not be appropriate for highly polarized comparisons (e.g., tumor vs. normal tissue with large-scale expression shifts)
- Log transformation requires positive expression values; background correction must be applied first to avoid undefined log values
- Quantile normalization can obscure global expression changes if a large fraction of genes are genuinely dysregulated; validation against spike-in controls or housekeeping genes is recommended
- The method is optimized for microarray data; RNA-seq data typically requires different normalization strategies (e.g., TMM, DESeq2 variance stabilization)

## Evidence

- [methods] log-transform gene expression, then apply quantile normalization: "Extract and log-transform gene expression, then apply quantile normalization using normalizeBetweenArrays from limma with method='quantile'."
- [methods] quantile normalization enables consistent GSEA P-values: "exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method="quantile")"
- [methods] GESECA requires filtered and normalized expression matrices: "Run geseca on the filtered expression matrix with minSize=15 and maxSize=500, using default centering."
- [intro] fgsea enables reproducible pathway enrichment with normalized data: "fgsea enables fast and accurate calculation of arbitrarily low GSEA P-values for gene set collections, supporting reproducible pathway enrichment analysis."
