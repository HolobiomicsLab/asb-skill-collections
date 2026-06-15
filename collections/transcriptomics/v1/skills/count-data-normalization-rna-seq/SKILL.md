---
name: count-data-normalization-rna-seq
description: Use when you have raw read count matrices from RNA-seq quantification (e.g., from featureCounts, HTSeq, Salmon, or kallisto) and need to prepare them for differential expression analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - tximport
  - featureCounts
  - Salmon
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

# Count-data normalization for RNA-seq

## Summary

Normalize raw RNA-seq read counts to account for sequencing depth and library composition differences before differential expression testing. This normalization step is essential for making counts comparable across samples in DESeq2 analysis, enabling accurate estimation of fold changes and statistical significance.

## When to use

You have raw read count matrices from RNA-seq quantification (e.g., from featureCounts, HTSeq, Salmon, or kallisto) and need to prepare them for differential expression analysis. The raw counts reflect both true biological differences and technical artifacts (sequencing depth variation, composition bias); normalization is required before fitting the negative binomial generalized linear model.

## When NOT to use

- Count data has already been normalized (e.g., TMM, quantile normalization, or log-transformed counts provided); applying DESeq2 normalization on pre-normalized data will distort fold-change estimates.
- Input is transcript-level abundance (TPM, FPKM) rather than raw counts; DESeq2 assumes count data with a negative binomial distribution, not normalized abundance.
- Sample sizes or experimental designs require specialized normalization (e.g., extreme batch effects, single-cell RNA-seq with high sparsity); DESeq2's built-in normalization may be insufficient without additional batch-correction methods.

## Inputs

- count matrix (rows=genes, columns=samples) from featureCounts, HTSeq, Salmon/tximport, or kallisto
- sample metadata (colData) with design variables (e.g., treatment, cell type)
- design formula specifying the statistical model structure

## Outputs

- DESeqDataSet object with estimated size factors and normalized counts
- results table with log2 fold changes, p-values, and adjusted p-values for each gene

## How to apply

DESeq2 implements median-of-ratios normalization as part of the DESeq() workflow. First, construct a DESeqDataSet from your count matrix with the appropriate design formula (e.g., ~cell+dex). The DESeq() function automatically estimates size factors that account for differences in sequencing depth and library composition by computing the median ratio of observed counts to geometric mean counts across samples. These size factors are then used to scale the raw counts internally during dispersion estimation and statistical testing. Optionally, pre-filter genes with very low counts (e.g., rowSums(counts) < 10) before DESeq() to reduce memory usage and improve computational speed; the results() function subsequently applies independent filtering based on mean normalized counts to improve detection power at a chosen significance threshold (default alpha=0.1).

## Related tools

- **DESeq2** (performs median-of-ratios normalization via size factor estimation and differential expression testing on normalized counts) — https://github.com/thelovelab/DESeq2
- **tximport** (imports transcript-level quantification from Salmon, kallisto, or RSEM and aggregates to gene-level counts suitable for DESeq2 normalization)
- **featureCounts** (generates raw gene-level count matrices from aligned reads that serve as input to DESeq2 normalization)
- **Salmon** (performs transcript quantification whose counts can be imported and aggregated for DESeq2 normalization)
- **DEvis** (provides downstream visualization and aggregation tools for exploring normalized and differential expression results) — https://github.com/price0416/DEvis

## Examples

```
library(DESeq2); library(airway); data(airway); dds <- DESeqDataSet(airway, design= ~cell+dex); dds <- DESeq(dds); res <- results(dds, alpha=0.1); resOrdered <- res[order(res$padj),]; sum(resOrdered$padj < 0.1, na.rm=TRUE)
```

## Evaluation signals

- Size factors computed for each sample should be close to 1.0 on average and reflect sequencing depth; check with sizeFactors(dds) and verify they are not extreme outliers or all identical.
- Normalized counts (obtained via counts(dds, normalized=TRUE)) should be comparable across samples without the strong depth-dependent bias visible in raw counts; MA-plot or boxplot of log-normalized counts should show centered, symmetric distributions.
- The number of genes passing independent filtering (reported in results() summary) should be substantially lower than the total number of genes, confirming that low-count genes were automatically removed to improve power.
- Reproducibility: re-running DESeq() on the same DESeqDataSet should produce identical results (same size factors, p-values, log fold changes) to within floating-point precision.
- Differential expression results should show expected biological patterns (e.g., known treatment-responsive genes are significant, housekeeping genes show low fold changes) and sensible adjusted p-value distribution (histogram showing enrichment near 0 and 1, not uniform).

## Limitations

- Median-of-ratios normalization assumes that the majority of genes are not differentially expressed between samples; severe global expression shifts (e.g., whole-genome upregulation in one condition) can lead to inflated or deflated size factors.
- Independent filtering is conservative and reduces sensitivity for genes with low mean counts; the automatic filtering threshold depends on the number of tests and desired FDR, which may not be optimal for all study designs.
- DESeq2 normalization does not account for complex batch effects, composition bias from a few highly abundant transcripts (e.g., rRNA contamination), or unwanted variation from hidden confounders; such issues require additional pre-processing (e.g., RUV methods, surrogate variable analysis) or post-hoc adjustment.
- Pre-filtering at a fixed count threshold (e.g., rowSums ≥ 10) is arbitrary and can discard lowly expressed but genuinely significant genes; the threshold should be chosen relative to smallest group size and sequencing depth.

## Evidence

- [other] dds <- DESeq(dds): "dds <- DESeq(dds) to estimate dispersions and fit negative binomial generalized linear models for each gene"
- [other] size factor estimation via median-of-ratios: "The *results* function automatically performs independent filtering based on the mean of normalized counts for each gene"
- [other] pre-filtering low-count genes rationale: "by removing rows in which there are very few reads, we reduce the memory size of the `dds` data object, and we increase the speed"
- [other] DESeqDataSet construction from counts: "dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition)"
- [other] negative binomial GLM framework: "The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models"
