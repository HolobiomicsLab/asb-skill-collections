---
name: multi-conditional-data-coregulation-scoring
description: Use when you have a normalized gene expression matrix (bulk RNA-seq or microarray) from a time-course or multi-condition experiment and need to quantify whether known gene sets (pathways, functional modules) show statistically significant coordinated expression changes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3308
  tools:
  - GEOquery
  - limma
  - fgsea
  - msigdbr
  - data.table
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

# multi-conditional-data-coregulation-scoring

## Summary

Score pathway and gene set coregulation across time-course or multi-condition gene expression experiments using fast preranked GSEA with adaptive Monte-Carlo P-value estimation. This skill enables reproducible detection of coordinated pathway activation patterns in normalized bulk or single-cell expression matrices.

## When to use

Apply this skill when you have a normalized gene expression matrix (bulk RNA-seq or microarray) from a time-course or multi-condition experiment and need to quantify whether known gene sets (pathways, functional modules) show statistically significant coordinated expression changes. Use it to validate that pathway activations match expected temporal or condition-dependent patterns, or to discover which pathways are significantly enriched at specific timepoints or conditions.

## When NOT to use

- Expression matrix has not been quantile-normalized and log-transformed (use normalization skill first)
- Gene sets are organ- or tissue-specific but do not match the tissue/cell type in your expression data
- Input is unranked gene-level statistics without full expression values (use preranked fgsea() instead of geseca())

## Inputs

- Normalized log-transformed gene expression matrix (rows=genes, columns=samples; numeric, no missing values)
- Gene set collection as named list (names=pathway identifiers, elements=character vectors of gene symbols/IDs)
- Gene metadata table with Gene ID column for deduplication

## Outputs

- Data table with one row per pathway: pathway name, enrichment score (ES), normalized ES (NES), p-value, adjusted p-value, log2 error estimate, and gene set size
- Ranked pathway list sorted by p-value or effect size for downstream visualization or reporting

## How to apply

Load a log-transformed and quantile-normalized expression matrix; filter to remove duplicate genes by Gene ID, empty/slash-containing identifiers, and retain the top N genes (e.g., 12,000) by mean expression to reduce noise. Load gene sets from a curated collection (e.g., HALLMARK pathways from msigdbr) and convert to a named list split by pathway. Run fgsea's geseca() function on the filtered expression matrix with minSize=15 and maxSize=500 to compute enrichment scores and P-values across all pathways using an adaptive multi-level split Monte-Carlo scheme. Sort results by P-value (or set eps=0 for higher precision if very low P-values are critical) and extract enrichment scores and temporal/conditional activation patterns for top pathways. Validate by confirming that reported pathway scores and P-values match expected ranges and known activation patterns from the literature or prior experiments.

## Related tools

- **fgsea** (Core tool for fast preranked gene set enrichment analysis and geseca() function for multi-condition pathway scoring) — https://github.com/ctlab/fgsea
- **limma** (Provides quantile normalization via normalizeBetweenArrays() to prepare expression matrix for GSEA)
- **msigdbr** (Retrieves curated pathway and gene set collections (e.g., HALLMARK, KEGG) in R-friendly format)
- **GEOquery** (Loads public gene expression datasets (e.g., GSE200250) from NCBI GEO for reproducible analysis)
- **data.table** (Manipulates and sorts enrichment results table for efficient ranking and filtering by p-value)
- **ggplot2** (Visualizes pathway enrichment patterns and temporal/condition-dependent activation across time-course)

## Examples

```
gesecaRes <- geseca(exprMatrix, pathwayList, minSize=15, maxSize=500); top_pathways <- gesecaRes[order(pval)][1:10, .(pathway, ES, NES, pval, padj)]
```

## Evaluation signals

- Reported pathway p-values and enrichment scores fall within expected ranges (e.g., known activated pathways have p < 0.05 and concordant ES sign)
- Temporal activation patterns for top pathways match known biology from the publication or prior validation study (e.g., cell-cycle pathways active at expected timepoints)
- Normalized ES (NES) values show consistent directionality with biological expectations (positive ES for upregulated pathways, negative for downregulated)
- Gene set sizes after filtering fall within specified minSize (15) and maxSize (500) bounds
- P-value distribution is not uniformly flat (indicating real signal, not random noise) and reproducible across independent runs with same random seed

## Limitations

- Requires quantile-normalized, log-transformed input; raw or incompletely normalized data will produce unreliable P-values
- Default eps=1e-10 lower bound limits P-value precision; must set eps=0 explicitly for arbitrarily low P-values, which increases computation time
- Gene set definitions are fixed at analysis time; does not dynamically update if pathway annotations change between timepoints or conditions
- Assumes independence of samples and does not account for repeated-measures or hierarchical correlation structures in time-course designs
- Adaptive Monte-Carlo scheme may show minor P-value variability across runs; set seed and eps=0 for full reproducibility

## Evidence

- [other] fgsea enables fast and accurate calculation of arbitrarily low GSEA P-values for gene set collections, supporting reproducible pathway enrichment analysis.: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
- [methods] Quantile normalization and log transformation are essential preprocessing steps before GSEA.: "Extract and log-transform gene expression, then apply quantile normalization using normalizeBetweenArrays from limma with method='quantile'"
- [methods] Filtering duplicates, empty gene IDs, and low-abundance genes reduces noise in pathway scoring.: "Filter the expression matrix by removing duplicate genes based on Gene ID, removing genes with missing or '///' identifiers, and retaining the top 12,000 genes by mean expression"
- [methods] geseca() function is called with specific size and centering parameters on filtered expression matrices.: "Run geseca on the filtered expression matrix with minSize=15 and maxSize=500, using default centering"
- [readme] P-value estimation uses adaptive multi-level split Monte-Carlo scheme for statistical accuracy.: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme"
- [methods] Validation of results requires matching reported scores to expected temporal patterns from literature.: "Validate that reported pathway scores and p-values match expected ranges and temporal patterns from the publication"
