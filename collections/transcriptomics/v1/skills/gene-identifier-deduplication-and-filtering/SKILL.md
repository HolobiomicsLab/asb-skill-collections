---
name: gene-identifier-deduplication-and-filtering
description: Use when when loading gene expression data (e.g., from GEO via getGEO or microarray ExpressionSet objects) that contains duplicate rows mapped to the same Gene ID, missing gene identifiers, or identifiers encoded with placeholder strings ('///') that indicate failed or ambiguous annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3170
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

# gene-identifier-deduplication-and-filtering

## Summary

Remove duplicate gene identifiers and filter genes with missing or malformed identifiers from expression matrices prior to pathway enrichment analysis. This preprocessing step ensures that downstream GSEA calculations operate on a clean, non-redundant gene annotation space.

## When to use

When loading gene expression data (e.g., from GEO via getGEO or microarray ExpressionSet objects) that contains duplicate rows mapped to the same Gene ID, missing gene identifiers, or identifiers encoded with placeholder strings ('///') that indicate failed or ambiguous annotation.

## When NOT to use

- Input expression matrix is already deduplicated and annotation-validated (confirmed via row uniqueness check)
- Gene identifiers are intentionally multi-mapped (e.g., representing isoforms or splice variants that should be retained as separate rows)
- Downstream analysis requires preservation of all probe-level measurements without aggregation (e.g., probe-set analysis in affymetrix data where multiple probes map to one gene)

## Inputs

- ExpressionSet object with gene expression data (exprs slot) and gene annotation (fData slot containing 'Gene ID' column)
- Gene expression matrix (rows = genes, columns = samples) with rownames as gene identifiers

## Outputs

- Filtered ExpressionSet or expression matrix with unique, non-missing gene identifiers
- Reduced feature count (number of genes) after deduplication and removal of malformed identifiers

## How to apply

After loading and log-transforming the expression matrix, apply three sequential filter operations: (1) remove rows with duplicate Gene ID values, keeping the first occurrence; (2) remove rows with empty rownames or rownames containing '///' (standard Bioconductor placeholder for failed gene annotation); (3) optionally filter to the top N genes by mean expression (e.g., top 12,000) to reduce computational cost for downstream GSEA while retaining signal-rich genes. These operations are applied in the ExpressionSet object before normalization and pathway analysis, ensuring that the gene set membership queries in fgsea match against a single, unambiguous set of gene identifiers per gene symbol.

## Related tools

- **limma** (Provides normalizeBetweenArrays() for quantile normalization applied after gene filtering; used in same workflow stage)
- **GEOquery** (Loads microarray ExpressionSet objects from GEO that require deduplication and identifier cleaning before downstream analysis)
- **fgsea** (Accepts cleaned gene expression matrix as input; requires non-redundant gene identifiers for accurate pathway membership matching) — https://github.com/ctlab/fgsea

## Examples

```
es <- es[!duplicated(fData(es)$`Gene ID`), ]; es <- es[!grepl("///", rownames(es)), ]; es <- es[rownames(es) != "", ]; es <- es[head(order(rowMeans(exprs(es)), decreasing=TRUE), 12000), ]
```

## Evaluation signals

- Number of rows in filtered matrix matches expected count after removing duplicates and malformed identifiers (e.g., 12,000 genes from ~18,000 raw probes)
- No rownames contain '///' or empty strings post-filtering; all remaining rownames are non-empty and unique (checked via nrow(es) == length(unique(rownames(es))))
- fgsea pathway enrichment results show stable, reproducible p-values and enrichment scores matching published findings when compared to original analysis
- Gene set membership in pathway collections (e.g., HALLMARK from msigdbr) matches correctly without ambiguous or null gene identifier lookups

## Limitations

- Deduplication by first occurrence is arbitrary; if multiple probes map to the same gene with different expression patterns, information is lost
- Filtering to top N genes by mean expression may discard low-abundance genes that are genuinely part of relevant pathways, reducing sensitivity for pathway detection in small gene sets
- No validation of whether removed identifiers ('///') correspond to actual annotation failure versus legitimate placeholder genes in the original data source; manual inspection of fData recommended
- Assumes Gene ID column exists and is correctly populated in fData; will silently fail or produce unexpected results if annotation structure differs from Bioconductor conventions

## Evidence

- [other] Remove duplicated genes based on Gene ID, removing genes with missing or '///' identifiers, and retaining the top 12,000 genes by mean expression: "Filter the expression matrix by removing duplicate genes based on Gene ID, removing genes with missing or '///' identifiers, and retaining the top 12,000 genes by mean expression."
- [methods] R code demonstrating removal of duplicated genes and malformed identifiers: "es <- es[!duplicated(fData(es)$`Gene ID`), ]
es <- es[!grepl("///", rownames(es)), ]
es <- es[rownames(es) != "", ]"
- [methods] Filtering to top genes by mean expression: "es <- es[head(order(rowMeans(exprs(es)), decreasing=TRUE), 12000), ]"
- [other] Context of use in workflow prior to GESECA pathway analysis: "Extract and log-transform gene expression, then apply quantile normalization using normalizeBetweenArrays from limma with method='quantile'. 3. Filter the expression matrix by removing duplicate"
