---
name: statistical-hypothesis-testing-rna-seq
description: Use when you have RNA-seq count matrices (from alignment, transcript quantification, or HTSeq-count files) and need to test for differential expression between two or more conditions while controlling for batch effects or other covariates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - tximport
  - tximeta
  - featureCounts
  - HTSeq
  - ashr
  - DEvis
derived_from:
- doi: 10.1186/s13059-014-0550-8
  title: deseq2
evidence_spans:
- The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models
- library("DESeq2") ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deseq2
    doi: 10.1186/s13059-014-0550-8
    title: deseq2
  dedup_kept_from: coll_deseq2
schema_version: 0.2.0
---

# Statistical hypothesis testing for RNA-seq differential expression

## Summary

Perform statistical significance testing on RNA-seq count data using negative binomial generalized linear models to identify differentially expressed genes between experimental conditions. This skill applies moderated estimation of dispersion and fold change to control false discovery rates while accounting for the overdispersion inherent in count data.

## When to use

You have RNA-seq count matrices (from alignment, transcript quantification, or HTSeq-count files) and need to test for differential expression between two or more conditions while controlling for batch effects or other covariates. Use this when your primary goal is to identify which genes show statistically significant changes in expression (adjusted p-value < 0.1 by default) rather than estimate effect sizes alone.

## When NOT to use

- Your input is already a pre-filtered list of significant genes and you need no further statistical testing.
- You have continuous normalized expression data (e.g., log2-transformed or TPM) rather than raw counts; DESeq2 requires raw count input to model the count distribution correctly.
- Your experimental design has no clear condition variable or lacks replication; hypothesis testing requires at least 2 samples per group to estimate variance.

## Inputs

- count matrix (rows=genes, columns=samples; from DESeqDataSetFromMatrix, tximport, HTSeq, or featureCounts)
- sample metadata/colData (data frame with condition, batch, and covariate columns)
- design formula (e.g., ~condition, ~batch+condition)

## Outputs

- results table with log2 fold changes, p-values, and adjusted p-values (padj)
- list of significantly differentially expressed genes (padj < alpha)
- ordered results by adjusted p-value

## How to apply

Construct a DESeqDataSet with a design formula specifying your condition of interest and any batch or covariate terms (e.g., ~cell+dex). Call DESeq() to estimate gene-wise dispersions and fit negative binomial GLMs, which borrows strength across genes to obtain stable dispersion estimates. Extract results using results(dds) with your chosen alpha threshold (default 0.1 for FDR control); the function automatically applies independent filtering based on mean normalized counts to remove uninformative genes with low counts. Order results by adjusted p-value (padj) to rank genes by significance. Genes with padj < your alpha threshold are declared statistically significant. The negative binomial framework accounts for count-level overdispersion and the shrinkage of log-fold-change estimates reduces noise when sample sizes are small.

## Related tools

- **DESeq2** (Core tool for constructing DESeqDataSet, estimating dispersions, fitting negative binomial GLMs, and computing p-values and adjusted p-values for differential expression testing.) — https://github.com/thelovelab/DESeq2
- **tximport** (Import transcript abundance quantification (from Salmon, kallisto, RSEM) and aggregate to gene level; produces count-like input compatible with DESeqDataSetFromTximport().)
- **tximeta** (Import transcript quantification with automatic metadata and produce a SummarizedExperiment for DESeqDataSet construction.)
- **featureCounts** (Generate count matrices from alignment BAM files for direct DESeq2 input.)
- **HTSeq** (Produce HTSeq-count files from alignments; counts can be loaded via DESeqDataSetFromHTSeq() for DESeq2 analysis.)
- **ashr** (Optional: post-hoc shrinkage of log fold changes using Adaptive Shrinkage after DESeq2 testing to improve effect-size estimates.) — https://github.com/stephens999/ashr
- **DEvis** (Visualization and aggregation tool for exploring and presenting differential expression results from DESeq2.) — https://github.com/price0416/DEvis

## Examples

```
library(DESeq2); library(airway); data(airway); dds <- DESeqDataSet(airway, design=~cell+dex); dds <- DESeq(dds); res <- results(dds, alpha=0.1); resOrdered <- res[order(res$padj),]; sum(resOrdered$padj < 0.1, na.rm=TRUE)
```

## Evaluation signals

- Verify that the DESeqDataSet has been constructed with correct design formula and all samples are present in colData; check dimensions match input count matrix.
- Confirm that DESeq() ran without error and that dispersion estimates are reasonable (plot with plotDispEsts); genes should show decreasing dispersion with increasing mean count.
- Check that results table includes baseMean, log2FoldChange, stat (Wald statistic), pvalue, and padj columns; verify that padj values are monotonically increasing when ordered by rank.
- Verify that independent filtering has reduced the number of tested genes compared to the total input (rowSums(counts(dds)) > threshold); this is automatic but should be visible in the filtered-out genes.
- Validate results by visual inspection (MA plot or p-value histogram); the MA plot should show fold-change estimates tightening toward zero for low-count genes, and the p-value histogram should show an enrichment of small p-values for true signal genes.

## Limitations

- DESeq2 requires raw count data and is not appropriate for pre-normalized or log-transformed expression values; using it on already-transformed data will violate the negative binomial assumption.
- The method assumes that the negative binomial distribution with a single dispersion parameter per gene adequately models the count variance; extreme departures from this (e.g., zero-inflation) may require alternative approaches.
- Independent filtering removes genes with very low mean counts to reduce false positives, but this also reduces power for lowly-expressed genes and makes results conditional on the observed count distribution; filtering thresholds are data-dependent.
- Small sample sizes (n < 3 per group) lead to unstable dispersion estimates and reduced power; the method relies on borrowing strength across genes to mitigate this, but is not a substitute for adequate replication.
- Design formulas must be carefully specified; confounding or missing batch/covariate terms can lead to spurious or underpowered results.

## Evidence

- [other] negative binomial generalized linear models: "The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models"
- [other] design formula construction: "dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition)"
- [other] results extraction and p-value computation: "res <- results(dds, name="condition_trt_vs_untrt")"
- [other] independent filtering by mean normalized count: "the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene"
- [other] ordered results by p-value: "resOrdered <- res[order(res$pvalue),]"
- [other] airway dataset example task: "Load the airway SummarizedExperiment dataset and construct a DESeqDataSet with design formula ~cell+dex. Run DESeq() to estimate dispersions and fit negative binomial generalized linear models for"
