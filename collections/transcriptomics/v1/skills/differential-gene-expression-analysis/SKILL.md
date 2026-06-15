---
name: differential-gene-expression-analysis
description: Use when when you have RNA-seq count matrices (from HTSeq, featureCounts, Salmon, kallisto, or RSEM quantification) and need to test for differential expression between two or more treatment groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0080
  tools:
  - DESeq2
  - IHW
  - tximport
  - tximeta
  - ashr
  - DEvis
  - Python
  - Scanpy
  - anndata
derived_from:
- doi: 10.1186/s13059-014-0550-8
  title: deseq2
- doi: 10.1186/s13059-017-1382-0
  title: ''
evidence_spans:
- The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models
- library("DESeq2") ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)
- A Bioconductor package, [IHW](http://bioconductor.org/packages/IHW), is available that implements the method of *Independent Hypothesis Weighting*
- Single-Cell Analysis in Python
- type annotations on function parameters
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deseq2
    doi: 10.1186/s13059-014-0550-8
    title: deseq2
  - build: coll_scanpy
    doi: 10.1186/s13059-017-1382-0
    title: scanpy
  dedup_kept_from: coll_deseq2
schema_version: 0.2.0
---

# differential-gene-expression-analysis

## Summary

Identify statistically significant differences in gene expression between biological conditions using negative binomial generalized linear models (DESeq2). This skill quantifies log2 fold changes and adjusted p-values for each gene, with automatic independent filtering to improve statistical power and FDR control.

## When to use

When you have RNA-seq count matrices (from HTSeq, featureCounts, Salmon, kallisto, or RSEM quantification) and need to test for differential expression between two or more treatment groups. Specifically, apply this skill when: (1) you have replicated samples across conditions with count data per gene; (2) your research question asks 'which genes change between conditions' with a target significance threshold (e.g., adjusted p-value < 0.1); (3) you want to account for sample-level covariates (batch, cell type) in the design formula.

## When NOT to use

- Input is already a normalized expression matrix (TPM, RPKM, log2-transformed) rather than raw counts — DESeq2 requires unnormalized count data.
- You have unpaired, observational data without a clear experimental design or condition assignment.
- Your primary goal is clustering or visualization rather than hypothesis testing for differential expression.

## Inputs

- count matrix (genes × samples)
- sample metadata (colData) with condition and covariate columns
- design formula specifying model structure (e.g., ~condition, ~batch+condition)

## Outputs

- results table with log2 fold change, p-value, and adjusted p-value per gene
- filtered gene list (adjusted p-value < threshold)
- summary statistics (number of genes up-regulated, down-regulated, filtered)

## How to apply

First, construct a DESeqDataSet by providing a count matrix, sample metadata (colData), and a design formula (e.g., ~cell+dex) that specifies the experimental structure and variables of interest. Run DESeq(dds) to estimate gene-level dispersions and fit negative binomial generalized linear models for each gene. Extract results using results(dds) with your target alpha threshold (default alpha=0.1 for FDR control); this function automatically performs independent filtering based on mean normalized counts to remove low-count genes and improve power. Order the results table by adjusted p-value (padj) to identify genes meeting your significance threshold. Consider applying shrinkage estimation (lfcShrink) to moderate log fold change estimates, especially for genes with high dispersion or low counts. Optionally, compare independent filtering results with alternative filtering methods (e.g., Independent Hypothesis Weighting via filterFun=ihw) to validate findings.

## Related tools

- **DESeq2** (Core tool for negative binomial modeling, dispersion estimation, and statistical testing of differential expression) — https://github.com/thelovelab/DESeq2
- **tximport** (Imports transcript quantification from Salmon, kallisto, or RSEM and aggregates to gene-level counts for DESeq2)
- **tximeta** (Imports transcript quantification and automatically adds metadata (gene names, ranges) as a SummarizedExperiment)
- **ashr** (Adaptive shrinkage of log fold change estimates using empirical Bayes methods to improve estimation stability) — https://github.com/stephens999/ashr
- **IHW** (Independent Hypothesis Weighting for improved multiple testing correction alternative to standard independent filtering)
- **DEvis** (Visualization and aggregation of DESeq2 differential expression results across multiple comparisons) — https://github.com/price0416/DEvis

## Examples

```
library(DESeq2); library(airway); data(airway); dds <- DESeqDataSet(airway, design = ~cell+dex); dds <- DESeq(dds); res <- results(dds, alpha=0.1); resOrdered <- res[order(res$padj),]; sum(resOrdered$padj < 0.1, na.rm=TRUE)
```

## Evaluation signals

- The adjusted p-value distribution is right-skewed with a spike near 1.0 (excess of non-significant genes), indicating proper FDR control.
- The number of genes retained after independent filtering is consistent with the mean count threshold applied (genes with low mean counts are removed).
- MA plot (log fold change vs. mean normalized count) shows symmetric cloud of points around y=0 with minimal bias across the x-axis.
- Comparison of filtered gene counts between standard filtering and alternative methods (e.g., IHW) shows similar power and FDR control.
- Log fold change shrinkage estimates (lfcShrink output) show reduced variance relative to unshrunk estimates, especially for low-count genes.

## Limitations

- DESeq2 assumes a negative binomial distribution; violations (zero-inflation, overdispersion beyond NB) may inflate false positives.
- Independent filtering threshold is data-dependent and automatic; it may remove true signal genes with legitimately low counts if their condition-specific expression is high.
- The design formula must correctly specify all relevant covariates; unmeasured confounding or batch effects not in the model will bias results.
- Results depend on choice of reference level for factor variables; comparisons are directional (e.g., treated vs. untreated, not symmetric).

## Evidence

- [other] The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models: "The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models"
- [other] dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition): "dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition)"
- [other] dds <- DESeq(dds) ... res <- results(dds, name="condition_trt_vs_untrt"): "dds <- DESeq(dds) ... res <- results(dds, name="condition_trt_vs_untrt")"
- [other] the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene: "the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene"
- [other] resOrdered <- res[order(res$pvalue),]: "resOrdered <- res[order(res$pvalue),]"
