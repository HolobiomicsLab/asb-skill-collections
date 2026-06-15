---
name: rna-seq-differential-expression-analysis
description: Use when you have RNA-seq read count data (from alignment tools, transcript quantification, or feature counting) organized in a count matrix with samples as columns and genes as rows, paired with sample metadata (condition, batch, treatment), and you want to test which genes show statistically.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
  tools:
  - DESeq2
  - ashr
  - tximport
  - tximeta
  - Salmon
  - kallisto
  - RSEM
  - featureCounts
  - HTSeq
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

# rna-seq-differential-expression-analysis

## Summary

Apply DESeq2's negative binomial generalized linear models to quantify differential gene expression between experimental conditions, producing shrunken log fold change estimates and significance tests. This skill combines count normalization, dispersion estimation, hypothesis testing, and log fold change shrinkage to identify genes with condition-dependent expression changes.

## When to use

You have RNA-seq read count data (from alignment tools, transcript quantification, or feature counting) organized in a count matrix with samples as columns and genes as rows, paired with sample metadata (condition, batch, treatment), and you want to test which genes show statistically significant expression differences between two or more experimental conditions while controlling for multiple testing and shrinking noisy estimates.

## When NOT to use

- Input data is already normalized or log-transformed (DESeq2 expects raw integer counts and performs its own normalization).
- You are analyzing single-cell RNA-seq data without aggregation to pseudo-bulk (DESeq2 is designed for bulk RNA-seq; single-cell requires specialized methods like edgeR-LRT or pseudobulk strategies).
- Your count matrix is very sparse (>90% zeros) or has extreme zero-inflation beyond biological dropout (alternative zero-inflated or hurdle models may be more appropriate).

## Inputs

- count matrix (genes × samples, integer counts)
- sample metadata with condition/treatment assignments and covariates
- DESeqDataSet object (after construction and DESeq() run)
- DESeq results object from results() call

## Outputs

- DESeqDataSet object with estimated size factors and dispersions
- results table with log2 fold changes, p-values, and adjusted p-values
- shrunken log fold change estimates (after lfcShrink)
- MA-plot visualizations comparing shrunk and unshrunk estimates

## How to apply

First, construct a DESeqDataSet from your count matrix and sample metadata using DESeqDataSetFromMatrix() (or DESeqDataSetFromTximport() if you have transcript-level quantification from Salmon, kallisto, or RSEM). Set the design formula to include all relevant covariates (e.g., design ~ batch + condition). Pre-filter genes with fewer than ~10 reads in the smallest group size to reduce memory and increase speed. Run DESeq() to estimate size factors (sequencing depth normalization), dispersions, and fit the negative binomial GLM. Extract base results using results() for your contrast of interest, which produces log2 fold changes, standard errors, p-values, and adjusted p-values. Apply lfcShrink() with type='apeglm' (or 'normal' or 'ashr') to shrink the log fold change estimates toward zero using an empirical Bayes prior, which reduces noise in estimates with high standard error while preserving strong signals. The choice of shrinkage type depends on your preference: apeglm uses an adaptive t-prior, normal uses the original adaptive normal prior, and ashr uses a mixture of normals and provides more flexible uncertainty quantification. Order results by adjusted p-value and visualize using MA-plots to compare shrunken vs. unshrunk estimates and identify the magnitude and significance of expression changes across the genome.

## Related tools

- **DESeq2** (Primary tool for negative binomial GLM-based differential expression analysis, normalization, dispersion estimation, and log fold change shrinkage) — https://github.com/thelovelab/DESeq2
- **ashr** (Provides adaptive shrinkage estimator (type='ashr') for log fold change shrinkage using mixture-of-normals prior, integrated into DESeq2's lfcShrink()) — https://github.com/stephens999/ashr
- **tximport** (Imports transcript-level quantification from Salmon, kallisto, or RSEM and aggregates to gene level before DESeq2 analysis)
- **tximeta** (Extends tximport by adding automatic metadata annotation to quantified transcript data)
- **Salmon** (Upstream tool for transcript quantification; output imported via tximport for DESeq2 analysis)
- **kallisto** (Upstream tool for transcript quantification; output imported via tximport for DESeq2 analysis)
- **RSEM** (Upstream tool for transcript quantification; output imported via tximport for DESeq2 analysis)
- **featureCounts** (Fast method for producing count matrices directly from alignment files, alternative to HTSeq)
- **HTSeq** (Generates gene count matrices from alignment files; output can be imported as DESeqDataSet)
- **DEvis** (Visualization and aggregation tool for differential expression results, supports downstream exploration of DESeq2 output) — https://github.com/price0416/DEvis

## Examples

```
dds <- DESeqDataSetFromMatrix(countData=cts, colData=coldata, design=~batch+condition); dds <- DESeq(dds); res <- results(dds, name='condition_trt_vs_untrt'); res <- lfcShrink(dds, coef='condition_trt_vs_untrt', type='apeglm')
```

## Evaluation signals

- DESeqDataSet object contains estimated size factors (visible via sizeFactors(dds)) indicating successful normalization.
- Dispersion estimates are reasonable (typically <1 for well-powered experiments); MA-plots show mean-variance relationship captured by the model.
- Shrunken log fold change estimates show shrinkage toward zero compared to unshrunk estimates, with stronger shrinkage for high-standard-error genes.
- Adjusted p-values (padj) are properly calibrated with expected FDR control; independent filtering by mean normalized count is applied automatically.
- Results ordered by p-value show top DE genes with both large effect size and strong statistical support; visualization confirms biological plausibility (e.g., known treatment-responsive genes rank highly).

## Limitations

- DESeq2 assumes negative binomial distribution and may underestimate dispersion in very low-count regimes or with extreme batch effects; pre-filtering helps but does not eliminate this issue.
- Log fold change shrinkage assumes a shared prior across genes; highly variable gene-specific effects (e.g., in very heterogeneous tissues) may be over-shrunk.
- The method requires biological replicates (at least 2–3 per condition) for reliable dispersion estimation; pseudoreplicates (technical replicates, lane-level samples) can inflate degrees of freedom artificially.
- Results depend critically on design formula specification; omitted or misspecified covariates (batch, patient, cell type) lead to inflated type I error or loss of power.
- Independent filtering threshold and shrinkage type (apeglm vs. normal vs. ashr) are data-dependent choices; no single default suits all datasets.

## Evidence

- [other] The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models: "The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models"
- [other] lfcShrink() can be applied with three different shrinkage estimator types to produce shrunken log fold change estimates from DESeq2 results objects.: "lfcShrink() can be applied with three different shrinkage estimator types (apeglm, normal, ashr) to produce shrunken log fold change estimates from DESeq2 results objects."
- [other] Run DESeq() to perform differential expression analysis and estimate dispersions.: "Run DESeq() to perform differential expression analysis and estimate dispersions."
- [other] by removing rows in which there are very few reads, we reduce the memory size of the dds data object, and we increase the speed: "by removing rows in which there are very few reads, we reduce the memory size of the `dds` data object, and we increase the speed"
- [other] the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene: "the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene"
- [other] you could import the data with tximport, which produces a list, and then you can use DESeqDataSetFromTximport(): "you could import the data with *tximport*, which produces a list, and then you can use `DESeqDataSetFromTximport()`"
