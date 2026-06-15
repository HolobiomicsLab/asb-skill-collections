---
name: principal-component-analysis-dimensionality-reduction
description: Use when your input is a normalized, centered gene expression matrix with many genes (e.g., 12,000+) and you need to validate whether reducing to a smaller number of principal components (e.g., 10) preserves pathway enrichment statistics (pathway scores and p-values from geseca or fgsea).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3517
  tools:
  - GEOquery
  - limma
  - fgsea
  - R
  - ggplot2
  - msigdbr
  - prcomp
  - scale
  - geseca
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

# principal-component-analysis-dimensionality-reduction

## Summary

Apply PCA to reduce a high-dimensional gene expression matrix to a smaller number of principal components, enabling faster downstream pathway enrichment analysis while preserving statistical signal. This skill is used to validate whether dimensionality reduction preserves pathway enrichment results by comparing correlation of p-values between full and reduced matrices.

## When to use

Your input is a normalized, centered gene expression matrix with many genes (e.g., 12,000+) and you need to validate whether reducing to a smaller number of principal components (e.g., 10) preserves pathway enrichment statistics (pathway scores and p-values from geseca or fgsea). Specifically, apply this skill when you want to test if PCA-reduced analysis yields Pearson correlation ≥0.95 for log10-transformed p-values compared to full-matrix results.

## When NOT to use

- Input expression matrix is already low-dimensional (e.g., <100 genes) — PCA will not provide computational benefit.
- You need to interpret individual gene contributions per pathway — PCA components are linear combinations and obscure single-gene effects.
- Your downstream analysis requires original gene identities for annotation or reporting — reduced PCs are abstract and not interpretable as named genes.

## Inputs

- Gene expression matrix (genes × cells), log2 and quantile-normalized
- Centered expression matrix (zero mean per gene row)
- Gene set collection (e.g., from msigdbr)

## Outputs

- PCA-reduced matrix (cells × principal components, e.g., 10 PCs)
- Pathway enrichment results table (pathway, p-value, NES, ES)
- Correlation plot (log10 p-values: full vs. reduced matrix)
- Validation metric (Pearson r ≥0.95 for log10 p-values)

## How to apply

First, ensure the expression matrix is normalized (e.g., via log2 and quantile normalization using limma::normalizeBetweenArrays) and centered row-wise to zero mean using scale(). Run base::prcomp() with center=FALSE to perform standard PCA and extract the first k principal components (e.g., k=10), which are linear combinations of genes across cells. Pass the PCA-reduced matrix (cells × k components) to geseca() with parameters minSize=15, maxSize=500, center=FALSE to obtain pathway scores and p-values. Compare results to the full matrix by computing Pearson correlation of log10-transformed p-values and plotting them with ggplot2. Validation succeeds when correlation is ≥0.95, confirming negligible information loss from dimensionality reduction.

## Related tools

- **prcomp** (Perform standard PCA on centered expression matrix with center=FALSE to extract principal components)
- **limma** (Apply log2 and quantile normalization to raw expression matrix via normalizeBetweenArrays()) — https://bioconductor.org/packages/release/bioc/html/limma.html
- **scale** (Center gene expression matrix (rows) to zero mean before PCA)
- **geseca** (Run Gene Set Enrichment analysis on PCA-reduced matrix to obtain pathway scores and p-values) — https://github.com/ctlab/fgsea
- **fgsea** (Fast preranked GSEA for accurate p-value calculation to compare full vs. reduced results) — https://github.com/ctlab/fgsea
- **ggplot2** (Visualize correlation of log10 p-values between full and PCA-reduced matrices)
- **data.table** (Efficient data manipulation and merging of pathway results tables)
- **msigdbr** (Retrieve curated gene set collections for enrichment analysis)

## Examples

```
# Center expression matrix
X_centered <- scale(X, center=TRUE, scale=FALSE)
# Apply PCA
pca_result <- prcomp(t(X_centered), center=FALSE, scale.=FALSE)
# Extract first 10 PCs
X_reduced <- pca_result$x[, 1:10]
# Run geseca on reduced matrix
geseca_reduced <- geseca(X_reduced, examplePathways, minSize=15, maxSize=500, center=FALSE)
# Compare with full matrix results using Pearson correlation of log10 p-values
cor(log10(geseca_full$pval), log10(geseca_reduced$pval), method='pearson')
```

## Evaluation signals

- Pearson correlation of log10-transformed p-values between full-matrix and PCA-reduced geseca results is ≥0.95, confirming preservation of statistical signal.
- PCA output dimensions match specification: (number of cells) × (k principal components, e.g., 10), and cumulative variance explained by first k PCs is inspected.
- Scatter plot of log10(pval_full) vs. log10(pval_reduced) shows tight linear alignment with minimal outliers, visually confirming correlation threshold.
- geseca() on reduced matrix completes without errors, returning pathway table with non-NA p-values, scores, and sizes matching expected range (minSize=15, maxSize=500).
- Comparison table documents pathway rank concordance (e.g., top 20 pathways by p-value), showing minimal re-ranking between full and reduced analyses.

## Limitations

- PCA preserves global variance structure but does not guarantee preservation of rare or weak pathway signals; low-abundance pathways may show greater p-value shifts.
- Correlation threshold (≥0.95) is dataset-specific; very sparse or highly structured expression matrices may require validation on a per-dataset basis.
- Interpretation of principal components is limited to variance explained per PC; individual gene contributions are weighted combinations and not directly interpretable.
- No changelog available for tracking reproducibility of fgsea versions and parameter stability across software updates.

## Evidence

- [other] Center gene expression matrix (rows) to zero mean using scale(). 3. Perform standard PCA using base::prcomp() with center=FALSE and extract the first 10 principal components corresponding to linear combinations of cells.: "Center gene expression matrix (rows) to zero mean using scale(). 3. Perform standard PCA using base::prcomp() with center=FALSE and extract the first 10 principal components"
- [other] Does dimensionality reduction via PCA to 10 dimensions preserve the pathway enrichment results (pathway scores and p-values) obtained from geseca() analysis on the full-dimensional GSE200250 expression matrix?: "Does dimensionality reduction via PCA to 10 dimensions preserve the pathway enrichment results (pathway scores and p-values) obtained from geseca() analysis"
- [other] 4. Run geseca() on the reduced matrix with minSize=15, maxSize=500, center=FALSE, and capture pathway scores and p-values. 5. Compare gesture results between full and reduced matrices by computing correlation of log10-transformed p-values and plotting log10(pval) from full matrix versus reduced matrix using ggplot2.: "Run geseca() on the reduced matrix with minSize=15, maxSize=500, center=FALSE, and capture pathway scores and p-values. 5. Compare gesture results between full and reduced matrices by computing"
- [other] 6. Validation: confirm that Pearson correlation of log10 p-values between full and reduced results is ≥0.95, indicating negligible information loss from dimensionality reduction.: "Validation: confirm that Pearson correlation of log10 p-values between full and reduced results is ≥0.95, indicating negligible information loss from dimensionality reduction"
- [readme] fgsea allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets: "fgsea allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
