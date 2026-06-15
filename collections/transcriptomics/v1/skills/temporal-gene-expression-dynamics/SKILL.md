---
name: temporal-gene-expression-dynamics
description: Use when you have time-ordered gene expression data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3512
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

# temporal-gene-expression-dynamics

## Summary

Quantify and validate time-dependent changes in gene expression across biological conditions using preranked gene set enrichment analysis (GSEA) on normalized, filtered expression matrices. This skill enables detection of pathway activation patterns and their temporal dynamics in response to experimental stimuli.

## When to use

Apply this skill when you have time-ordered gene expression data (e.g., a time-course microarray or RNA-seq experiment) and need to identify which biological pathways are consistently activated or repressed at specific timepoints, and to verify that enrichment scores and p-values match expected temporal patterns from prior publications or biological knowledge.

## When NOT to use

- Input is single-timepoint cross-sectional data with no temporal ordering
- Gene expression matrix is already aggregated to pathway-level scores rather than gene-level
- Experimental design lacks biological replicates or quality control within each timepoint

## Inputs

- time-ordered expression matrix (rows=genes, columns=samples ordered by timepoint)
- gene annotation table with Gene IDs and gene identifiers
- curated gene set collection (e.g., HALLMARK pathways from msigdbr)

## Outputs

- enrichment results table (pathways × {pathway, p-value, padj, ES, NES, size})
- temporal activation patterns for top pathways (pathway name × enrichment scores across timepoints)
- validation report comparing observed vs. expected pathway activation dynamics

## How to apply

First, load the time-course expression matrix (e.g., via getGEO from GEOquery) and select samples belonging to the condition of interest, ordering by time point. Apply log transformation followed by quantile normalization using normalizeBetweenArrays with method='quantile' to ensure comparability across samples. Filter the normalized matrix by removing duplicate gene IDs, excluding genes with missing or '///' identifiers, and retaining the top genes by mean expression (e.g., top 12,000). Load curated gene sets from a collection such as HALLMARK (via msigdbr) and convert to a named list split by pathway. Run geseca or fgsea on the filtered expression matrix with parameters minSize=15 and maxSize=500 to compute enrichment scores and p-values. Sort results by p-value and extract temporal activation patterns for top pathways. Validate that the reported pathway scores, p-values, and direction of enrichment (ES sign) match the expected temporal dynamics from biological priors or published findings.

## Related tools

- **fgsea** (fast preranked gene set enrichment analysis with adaptive multi-level Monte-Carlo p-value estimation; used to compute enrichment scores and significance for pathway activation at each timepoint) — https://github.com/ctlab/fgsea
- **limma** (quantile normalization of expression matrices across samples via normalizeBetweenArrays to remove technical variation before enrichment analysis)
- **GEOquery** (retrieve time-course expression data from public GEO repositories (e.g., GSE200250) and order samples by experimental timepoint)
- **msigdbr** (curated gene set collections (e.g., HALLMARK, Reactome) formatted as named lists for use in enrichment analysis)
- **data.table** (efficient sorting and filtering of enrichment results by p-value and pathway metadata)
- **ggplot2** (visualization of temporal pathway activation patterns and enrichment landscape across timepoints)

## Examples

```
gesecaRes <- geseca(exampleExpressionMatrix, examplePathways, minSize = 15, maxSize = 500); head(gesecaRes[order(pval), ])
```

## Evaluation signals

- Enrichment p-values are at or below stated Monte-Carlo precision floor (e.g., eps=1e-10 by default, lower when eps=0 is set); reported log2err values reflect multi-level split estimation accuracy
- Pathway enrichment scores (ES and NES) and direction match expected biology: e.g., E2F_TARGETS and HYPOXIA activated in expected timepoint windows, not uniformly across all timepoints
- Top enriched pathways at each timepoint cluster meaningfully by biological function (e.g., cell cycle genes enriched early, differentiation genes late)
- Pathway sizes and gene overlap are within specified bounds (minSize ≥ 15, maxSize ≤ 500); no pathways excluded due to filtering
- Validation report documents agreement between observed enrichment scores and temporal activation patterns reported in source publication or biological priors

## Limitations

- Results depend critically on expression matrix normalization method; quantile normalization assumes absence of global gene expression shifts and may mask real biology in some contexts
- Gene filtering to top 12,000 by mean expression may remove lowly expressed but biologically important genes from enrichment calculation
- GESECA and fgsea assume gene rankings or expression values are independent; strong technical batch effects within timepoints can inflate false positives
- P-value estimation relies on permutation/Monte-Carlo sampling and is subject to sampling noise; very low p-values (< 1e-20) require eps=0 and extended computation
- No changelog or versioning noted for fgsea; reproducing results from older publications may require fixing a specific package version or parameter set

## Evidence

- [other] Load GSE200250 dataset using getGEO from GEOquery, selecting Th2 samples and ordering by time point.: "Load GSE200250 dataset using getGEO from GEOquery, selecting Th2 samples and ordering by time point."
- [methods] Apply quantile normalization using normalizeBetweenArrays from limma with method='quantile'.: "exprs(es) <- normalizeBetweenArrays(log2(exprs(es)), method="quantile")"
- [other] Filter the expression matrix by removing duplicate genes, removing genes with missing or '///' identifiers, and retaining the top 12,000 genes by mean expression.: "Filter the expression matrix by removing duplicate genes based on Gene ID, removing genes with missing or '///' identifiers, and retaining the top 12,000 genes by mean expression."
- [other] Load HALLMARK gene sets from msigdbr with species='mouse' and collection='H', converting to a named list split by pathway name.: "Load HALLMARK gene sets from msigdbr with species='mouse' and collection='H', converting to a named list split by pathway name."
- [other] Run geseca on the filtered expression matrix with minSize=15 and maxSize=500, using default centering.: "Run geseca on the filtered expression matrix with minSize=15 and maxSize=500, using default centering."
- [intro] fgsea allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets: "This package allows to quickly and accurately calculate arbitrarily low GSEA P-values for a collection of gene sets"
- [intro] P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme: "P-value estimation is based on an adaptive multi-level split Monte-Carlo scheme"
- [readme] fgsea has a default lower bound eps=1e-10 for estimating P-values. If you need to estimate P-value more accurately, you can set the eps argument to zero in the fgsea function.: "fgsea has a default lower bound `eps=1e-10` for estimating P-values. If you need to estimate P-value more accurately, you can set the `eps` argument to zero"
