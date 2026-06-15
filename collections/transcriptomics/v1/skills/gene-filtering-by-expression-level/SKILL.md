---
name: gene-filtering-by-expression-level
description: Use when you have a large gene expression matrix (e.g., thousands of genes) from normalized microarray or RNA-seq data and need to reduce computational burden before running pathway enrichment analysis (e.g., GSEA or GESECA).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0203
  tools:
  - GEOquery
  - limma
  - fgsea
  - R
  - ggplot2
  - msigdbr
  - R base functions
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

# gene-filtering-by-expression-level

## Summary

Filter a gene expression matrix to retain only the highest-expressed genes by mean expression rank, reducing dimensionality while preserving the most informative signal for downstream pathway enrichment analysis. This pre-processing step improves computational efficiency and can preserve pathway enrichment results across different matrix dimensionalities.

## When to use

Apply this skill when you have a large gene expression matrix (e.g., thousands of genes) from normalized microarray or RNA-seq data and need to reduce computational burden before running pathway enrichment analysis (e.g., GSEA or GESECA). Use it particularly when validating whether dimensionality reduction preserves pathway scores and p-values, or when working with memory-constrained systems.

## When NOT to use

- Input is already a pre-filtered or curated feature table (e.g., a manually selected pathway gene set).
- Analysis requires detection of rare transcripts or lowly-expressed disease-associated genes that fall below the expression threshold.
- You need to preserve all genes for variance-stabilizing normalization or for building a background distribution for statistical testing.

## Inputs

- normalized gene expression matrix (genes × samples)
- normalized expression values (log2 and quantile-normalized)
- integer threshold for top-N genes to retain

## Outputs

- filtered gene expression matrix (subset of top genes × samples)
- subset of gene identifiers retained after filtering

## How to apply

After log2 and quantile normalization of the expression matrix using limma::normalizeBetweenArrays(), calculate the mean expression level for each gene (row-wise mean). Rank genes by descending mean expression and subset to retain the top N genes (e.g., 12,000 genes in the referenced study). The rationale is that lowly-expressed genes contribute noise rather than signal to pathway enrichment; filtering to highly-expressed genes reduces the input dimensionality while maintaining correlation of pathway p-values (≥0.95 Pearson correlation of log10-transformed p-values) between full and reduced matrices, demonstrating negligible information loss for downstream analysis.

## Related tools

- **limma** (Apply log2 and quantile normalization to expression matrix before filtering)
- **fgsea** (Perform pathway enrichment analysis on filtered matrix and validate score/p-value preservation) — https://github.com/ctlab/fgsea
- **R base functions** (Calculate rowMeans() for mean expression per gene and order() to rank genes)
- **ggplot2** (Visualize correlation of log10 p-values between full and reduced matrices)

## Examples

```
es <- es[head(order(rowMeans(exprs(es)), decreasing=TRUE), 12000), ]
```

## Evaluation signals

- Verify that the number of retained genes equals the specified threshold (e.g., 12,000).
- Confirm that retained genes have non-zero mean expression and are ranked in descending order of mean expression.
- Compute Pearson correlation of log10-transformed pathway p-values from GESECA analysis on full vs. filtered matrices and confirm ≥0.95 correlation, indicating preservation of pathway enrichment signal.
- Check that filtering reduces matrix memory footprint and improves computational runtime for downstream GSEA/GESECA without substantial loss of significance rankings.
- Validate that gene identifiers in filtered matrix match the original annotation (no duplicates, no 'empty' or '///' identifiers)

## Limitations

- Filtering by mean expression alone may inadvertently remove genes with strong but context-specific (e.g., time-point or condition-dependent) expression patterns.
- The optimal threshold (e.g., 12,000 genes) is data-dependent and may not generalize across different tissues, platforms, or sample sizes.
- Filtering is performed after normalization; biases introduced during normalization (e.g., platform batch effects) are not corrected by this step alone.
- The skill assumes that lowly-expressed genes contribute primarily noise to pathway enrichment; this assumption may not hold for rare cell populations or rare transcript detection.

## Evidence

- [methods] Filter to top genes by mean expression: "es <- es[head(order(rowMeans(exprs(es)), decreasing=TRUE), 12000), ]"
- [methods] Filtering preserves pathway enrichment signal across dimensionalities: "apply log2 and quantile normalization using limma::normalizeBetweenArrays, filter to top 12,000 genes by mean expression"
- [methods] Validation threshold for filtering effectiveness: "confirm that Pearson correlation of log10 p-values between full and reduced results is ≥0.95, indicating negligible information loss from dimensionality reduction"
- [other] Rationale: fgsea enables comparison across dimensionalities: "fgsea enables fast and accurate calculation of GSEA P-values for gene set collections, supporting the feasibility of comparing pathway enrichment results across different input dimensionalities"
