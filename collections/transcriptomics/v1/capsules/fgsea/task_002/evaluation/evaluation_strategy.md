# Evaluation Strategy

## Direct Checks

- verify file exists: GSE200250 can be retrieved via GEOquery::getGEO()
- verify GEOquery script runs: library(GEOquery); gse200250 <- getGEO('GSE200250', AnnotGPL = TRUE) executes without error
- verify limma script runs: library(limma); normalized_exprs <- normalizeBetweenArrays(log2(exprs(es)), method='quantile') executes without error
- verify fgsea script runs: library(fgsea); gesecaRes <- geseca(normalized_expression_matrix, hallmark_gene_sets, minSize=15, maxSize=500) executes without error
- verify output structure: gesecaRes contains columns 'pathway', 'NES', 'pval', 'padj' with numeric values
- verify top pathway identification: HALLMARK_E2F_TARGETS appears in gesecaRes pathways at 24h timepoint, robust to minor ranking shifts
- verify top pathway identification: HALLMARK_HYPOXIA appears in gesecaRes pathways at 48h timepoint, robust to minor ranking shifts
- verify NES and p-value retrieval: extract NES and pval for HALLMARK_E2F_TARGETS at 24h and HALLMARK_HYPOXIA at 48h, any of the following numeric formats acceptable

## Expert Review

- assess whether reported NES and p-values for HALLMARK_E2F_TARGETS (24h) and HALLMARK_HYPOXIA (48h) align with computed scores from geseca() on normalized GSE200250 data within acceptable tolerance (parameter-sensitive: tolerance bounds require domain judgment)
- assess whether limma normalization (log2 + quantile) is the appropriate preprocessing for GSE200250 gene expression matrix prior to GESECA analysis
- assess biological plausibility: whether E2F_TARGETS activation at 24h and HYPOXIA activation at 48h are consistent with the experimental design and known biology of GSE200250
