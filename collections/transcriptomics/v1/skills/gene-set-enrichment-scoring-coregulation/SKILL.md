---
name: gene-set-enrichment-scoring-coregulation
description: Use when you have a normalized gene expression matrix (log2-quantile normalized, filtered to high-variance genes) and a collection of annotated gene sets (e.g., Reactome, MSigDB pathways), and need to test whether specific pathways show significant coordinated expression shifts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0085
  - http://edamontology.org/topic_3391
  tools:
  - GEOquery
  - limma
  - fgsea
  - R
  - ggplot2
  - msigdbr
  - data.table
derived_from:
- doi: 10.1101/060012
  title: fgsea
evidence_spans:
- library(GEOquery)
- exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method="quantile")
- '`fgsea` is an R-package for fast preranked gene set enrichment analysis (GSEA)'
- gesecaRes <- geseca(pathways, exprs(es), minSize = 15, maxSize = 500)
- R-package for fast preranked gene set enrichment analysis
- fgsea is an R-package for fast preranked gene set enrichment analysis
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

# gene-set-enrichment-scoring-coregulation

## Summary

Score pathway enrichment and co-regulation patterns using fast preranked GSEA (fgsea) to quantify whether gene sets show coordinated expression changes across samples or conditions. This skill enables rapid calculation of pathway-level statistics and p-values to assess biological pathway activation and validate that dimensionality reduction preserves enrichment signals.

## When to use

Apply this skill when you have a normalized gene expression matrix (log2-quantile normalized, filtered to high-variance genes) and a collection of annotated gene sets (e.g., Reactome, MSigDB pathways), and need to test whether specific pathways show significant coordinated expression shifts. Use it particularly when comparing enrichment results across different data representations (e.g., full-dimensional vs. PCA-reduced matrices) to validate that pathway signals are preserved.

## When NOT to use

- Input expression matrix is not normalized (raw counts); use limma::normalizeBetweenArrays or similar first.
- Gene set collection contains very small (<15 genes) or very large (>500 genes) sets without filtering; adjust minSize and maxSize parameters or filter the collection.
- Input data is already a precomputed pathway score matrix rather than a raw or normalized expression matrix.

## Inputs

- normalized log2 expression matrix (genes × samples/cells)
- filtered to top genes by mean expression (e.g., 12,000 genes)
- gene set collection (pathways as list of character vectors, e.g., from msigdbr or examplePathways)

## Outputs

- pathway enrichment table with columns: pathway name, ES (enrichment score), NES (normalized ES), p-value, adjusted p-value, log2err, pathway size
- log10-transformed p-value vectors for correlation/comparison
- enrichment plots (ggplot2 objects) showing pathway activation patterns

## How to apply

Load a pre-normalized, filtered expression matrix and gene set collection. Center the expression matrix to zero mean by row using scale(). Run geseca() with parameters minSize=15, maxSize=500, center=FALSE to compute pathway scores and enrichment p-values. For validation across dimensionalities, compute Pearson correlation of log10-transformed p-values between full and reduced matrices; a correlation ≥0.95 indicates negligible information loss. Use an adaptive multi-level split Monte-Carlo scheme (the default in fgsea) for accurate low p-value estimation. Visualize results using log10(pval) plots (ggplot2) to compare enrichment patterns between conditions or matrix representations.

## Related tools

- **fgsea** (Core R package for fast preranked GSEA and geseca() pathway enrichment scoring with adaptive Monte-Carlo p-value estimation) — https://github.com/ctlab/fgsea
- **limma** (Normalize expression matrices (log2 and quantile normalization) prior to enrichment analysis)
- **msigdbr** (Retrieve standardized gene set collections (Reactome, KEGG, hallmark pathways) for enrichment testing)
- **ggplot2** (Visualize log10 p-value correlations and enrichment results across conditions or dimensionalities)
- **data.table** (Efficiently organize and filter enrichment result tables by pathway, p-value, or ES)
- **GEOquery** (Load public expression datasets (e.g., GSE200250) and metadata for enrichment analysis)

## Examples

```
gesecaRes <- geseca(exprMatrix, pathways, minSize = 15, maxSize = 500, center = FALSE); corr <- cor(log10(full_results$pval), log10(reduced_results$pval), method = 'pearson')
```

## Evaluation signals

- Enrichment result table is non-empty with all required columns (pathway, ES, NES, pval, padj, size) and sorted by p-value.
- Pathway sizes respect minSize (≥15) and maxSize (≤500) constraints; no pathways are excluded unexpectedly.
- When comparing full vs. reduced matrix results, Pearson correlation of log10 p-values is ≥0.95, confirming preservation of enrichment signal across dimensionalities.
- Log10 p-value plots show visual agreement between conditions (scatter points cluster near diagonal y=x).
- Top enriched pathways have biologically meaningful names and ES/NES values consistent with experimental design (e.g., cell-cycle pathways enriched in proliferating conditions).

## Limitations

- fgsea has a default lower p-value bound (eps=1e-10); set eps=0.0 to estimate arbitrarily low p-values, which may increase computational cost.
- Enrichment results depend strongly on gene filtering (top N genes by mean expression) and normalization method; different cutoffs (e.g., 8,000 vs. 12,000 genes) may yield different pathway rankings.
- The skill requires pre-centered expression matrices (scale() by row); failure to center before geseca() may yield invalid enrichment scores.
- Monte-Carlo p-value estimation is stochastic; results may vary slightly between runs unless a random seed is set for reproducibility.

## Evidence

- [readme] fgsea package capability and Monte-Carlo scheme: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets. P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme."
- [other] Validation criterion for dimensionality reduction preservation: "confirm that Pearson correlation of log10 p-values between full and reduced results is ≥0.95, indicating negligible information loss from dimensionality reduction"
- [other] Preprocessing workflow: normalization and centering: "apply log2 and quantile normalization using limma::normalizeBetweenArrays, filter to top 12,000 genes by mean expression, and subset to Th2 time-course samples. Center gene expression matrix (rows)"
- [other] geseca() function parameters and pathway size constraints: "Run geseca() on the reduced matrix with minSize=15, maxSize=500, center=FALSE, and capture pathway scores and p-values"
- [other] Visualization and comparison methodology: "Compare gesture results between full and reduced matrices by computing correlation of log10-transformed p-values and plotting log10(pval) from full matrix versus reduced matrix using ggplot2"
- [other] Finding about fgsea accuracy for pathway enrichment: "fgsea enables fast and accurate calculation of GSEA P-values for gene set collections, supporting the feasibility of comparing pathway enrichment results across different input dimensionalities"
