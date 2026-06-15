---
name: rnaseq-count-matrix-analysis
description: Use when you have a count matrix (genes × samples) from HTSeq, featureCounts, or transcript abundance quantification (Salmon, kallisto), a sample metadata table with experimental design, and you need to test for differential expression while controlling false discovery rate via independent.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
  tools:
  - DESeq2
  - IHW
  - tximport
  - tximeta
  - HTSeq
  - featureCounts (Rsubread)
  - ashr
derived_from:
- doi: 10.1186/s13059-014-0550-8
  title: deseq2
evidence_spans:
- The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models
- library("DESeq2") ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)
- A Bioconductor package, [IHW](http://bioconductor.org/packages/IHW), is available that implements the method of *Independent Hypothesis Weighting*
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

# RNA-seq count matrix analysis

## Summary

Construct a DESeq2 data object from RNA-seq count matrices, estimate dispersions via negative binomial GLM, and extract differential expression results with automated independent filtering. This skill bridges raw count data to statistically rigorous fold-change and p-value inference.

## When to use

You have a count matrix (genes × samples) from HTSeq, featureCounts, or transcript abundance quantification (Salmon, kallisto), a sample metadata table with experimental design, and you need to test for differential expression while controlling false discovery rate via independent filtering on mean normalized counts.

## When NOT to use

- Input is already a feature table, normalized expression matrix, or continuous abundance (e.g., TPM, FPKM) — DESeq2 requires raw counts.
- Sample size is very small (n < 3 per group) — dispersion estimation becomes unreliable.
- Data are from a single sample or have no experimental grouping — differential expression testing requires at least two conditions.

## Inputs

- count matrix (genes × samples, integer values from HTSeq, featureCounts, or similar)
- sample metadata table with condition/batch covariates
- experimental design formula (e.g., ~cell + dex)
- optional: transcript quantification output (Salmon/kallisto) and tx2gene mapping

## Outputs

- DESeqDataSet object with estimated dispersions and fitted negative binomial coefficients
- results table with log2 fold change, standard error, p-value, padj, and baseMean per gene
- summary of independent filtering: number of genes passing filter, rejection threshold
- optional: shrunken log fold changes (via lfcShrink with apeglm type)

## How to apply

First, construct a DESeqDataSet object using DESeqDataSetFromMatrix() (for count matrices) or DESeqDataSetFromTximport() (for quantification outputs). Optionally pre-filter low-count genes (e.g., keeping rows with ≥10 reads in ≥smallestGroupSize samples) to reduce memory and computation time. Run DESeq() to estimate dispersions and fit negative binomial GLMs across your design formula. Extract results using results(dds) with default alpha=0.1; the function automatically performs independent filtering based on the mean of normalized counts for each gene, rejecting null hypotheses only for genes above an optimal count threshold. Order results by adjusted p-value (padj) and compare filtered gene counts to document filtering impact. Optionally apply IHW (Independent Hypothesis Weighting) via results(dds, filterFun=ihw) for improved power when filter statistics and test statistics are correlated.

## Related tools

- **DESeq2** (Core package for constructing DESeqDataSet, estimating dispersions, fitting negative binomial GLMs, and extracting differential expression results with independent filtering) — https://github.com/thelovelab/DESeq2
- **tximport** (Import transcript quantification output (Salmon, kallisto, RSEM) and convert to gene-level counts)
- **tximeta** (Import quantification with automatic metadata and produce SummarizedExperiment for DESeqDataSet construction)
- **IHW** (Alternative to DESeq2's default independent filtering; applies Independent Hypothesis Weighting for improved power)
- **HTSeq** (Generate count matrices from aligned BAM files (alternative input source))
- **featureCounts (Rsubread)** (Generate count matrices from aligned BAM files (alternative, faster input source))
- **ashr** (Adaptive Shrinkage for stabilizing fold-change estimates via empirical Bayes shrinkage) — https://github.com/stephens999/ashr

## Examples

```
library(DESeq2); dds <- DESeqDataSetFromMatrix(countData=cts, colData=coldata, design=~condition); dds <- DESeq(dds); res <- results(dds, alpha=0.1); res_ordered <- res[order(res$pvalue),]
```

## Evaluation signals

- DESeqDataSet object successfully loads with counts(dds) returning integer matrix, design matches formula, and colData matches sample metadata.
- DESeq() completes without error; dispersions are estimated for all genes (rowData(dds)$dispersion is not NA) and show reasonable shrinkage pattern (observed vs. fitted).
- results() table has nrow equal to filtered gene count (< nrow(dds)), with non-null baseMean, log2FoldChange, lfcSE, pvalue, and padj columns; no NAs in padj except for filtered genes.
- Independent filtering threshold is reported (e.g., 'independent filtering removed X genes'); compare retained gene count before/after filtering and verify baseMean distribution is shifted upward post-filter.
- Adjusted p-values (padj) show expected multiple-testing correction (padj ≥ pvalue for all tests); genes with padj < 0.1 (default alpha) represent controlled FDR rejection set.

## Limitations

- Dispersion estimation requires multiple replicates per condition; very small sample sizes lead to unreliable estimation and inflated Type I error.
- Independent filtering is automatic but data-driven; threshold varies by dataset and may not align with biological cutoffs (e.g., baseMean threshold is unrelated to fold-change magnitude).
- DESeq2 assumes negative binomial distribution; violations (e.g., zero-inflation, technical confounders) can invalidate inference unless addressed by pre-filtering or design adjustment.
- Log fold-change estimates are unshrunken by default; small-sample noise inflates effect sizes; use lfcShrink() with apeglm type for stability.
- Design formula must account for known confounders (batch, cell type); unmeasured confounding is not detected and biases results.

## Evidence

- [other] Core DESeq2 workflow and independent filtering rationale: "The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models"
- [other] Independent filtering mechanism in results() function: "the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene"
- [other] Pre-filtering low-count genes reduces memory and computation: "by removing rows in which there are very few reads, we reduce the memory size of the `dds` data object, and we increase the speed"
- [other] DESeqDataSet construction from count matrix: "dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition)"
- [other] Results with log fold changes and p-values: "res <- results(dds, name="condition_trt_vs_untrt")"
- [other] tximport for quantification-to-counts conversion: "txi <- tximport(files, type="salmon", tx2gene=tx2gene)"
- [other] DESeqDataSet from tximport output: "ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)"
