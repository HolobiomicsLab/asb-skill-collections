---
name: results-table-extraction-and-comparison
description: Use when after running DESeq() on a DESeqDataSet and obtaining initial results via results(), use this skill when you need to (1) extract base results tables for specific contrasts (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3741
  edam_topics:
  - http://edamontology.org/topic_3168
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - ashr
  - ggplot2 / base R graphics
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

# results-table-extraction-and-comparison

## Summary

Extract differential expression results tables from DESeq2 analysis objects and compare shrinkage estimator outputs (apeglm, normal, ashr) using log fold change values, p-values, and adjusted p-values across conditions. This skill enables systematic evaluation of how different shrinkage priors modulate effect size estimates and statistical significance in RNA-seq differential expression studies.

## When to use

After running DESeq() on a DESeqDataSet and obtaining initial results via results(), use this skill when you need to (1) extract base results tables for specific contrasts (e.g., treated vs. untreated), (2) apply multiple shrinkage estimators to the same results object to compare their shrunken log fold change estimates, or (3) generate ranked or filtered results tables for downstream interpretation (e.g., MA-plots, volcano plots, or gene set enrichment). This is particularly valuable when the magnitude and credibility of fold change estimates must be compared across different prior assumptions.

## When NOT to use

- Input is already a shrunken results table from a previous lfcShrink() call and no re-shrinkage or comparison with other estimators is needed.
- Sample size is very small (n < 3 per group) and shrinkage estimation becomes unstable; base results may be more reliable than shrunken estimates.
- Analysis goal is only to identify genes with extreme p-values without regard for effect size credibility; base results() output suffices.

## Inputs

- DESeqDataSet object (fitted with DESeq())
- contrast or coefficient name (character string for results() call)
- base results table from results(dds, name=...)

## Outputs

- results table with base log2 fold changes, p-values, padj
- shrunken log fold change results table(s) from lfcShrink()
- ordered/filtered results table (by p-value, padj, or |log2FC|)
- MA-plot or comparison visualization

## How to apply

First, call results(dds, name="contrast_name") on your fitted DESeqDataSet to extract the base results table, which contains log2 fold changes, standard errors, test statistics, p-values, and adjusted p-values. Next, apply lfcShrink() to the same DESeqDataSet using at least one shrinkage type (type='apeglm', type='normal', or type='ashr'), specifying the coefficient or contrast name. The apeglm estimator uses an adaptive t-prior suitable for single-contrast shrinkage; the normal estimator uses the original adaptive normal prior; and the ashr estimator uses a non-parametric mixture of normals for greater flexibility. Extract and compare the shrunken log fold change columns across all results tables. Order or filter results by p-value, adjusted p-value (padj < 0.05 is typical), or log fold change magnitude (|log2FC| > 1 is common). Visualize differences using MA-plots (mean count vs. log fold change) or side-by-side summary statistics to assess how much shrinkage each estimator applied and whether ranking or significance calls change across estimators.

## Related tools

- **DESeq2** (Core package for differential expression analysis; provides results() to extract results tables and lfcShrink() to apply shrinkage estimators (apeglm, normal, ashr) and compare shrunken log fold changes) — https://github.com/thelovelab/DESeq2
- **ashr** (Implements adaptive shrinkage with mixture-of-normals prior; invoked via lfcShrink(type='ashr') to produce non-parametric shrunken log fold change estimates for comparison with apeglm and normal methods) — https://github.com/stephens999/ashr
- **ggplot2 / base R graphics** (Visualization of results-table comparisons via MA-plots, volcano plots, and summary statistics across estimators)

## Examples

```
res_base <- results(dds, name="dex_treated_vs_untreated"); res_apeglm <- lfcShrink(dds, coef="dex_treated_vs_untreated", type="apeglm"); res_ashr <- lfcShrink(dds, coef="dex_treated_vs_untreated", type="ashr"); head(res_base); head(res_apeglm); head(res_ashr)
```

## Evaluation signals

- Base results table from results() contains non-null log2FoldChange, stat, pvalue, and padj columns for all genes.
- Shrunken results tables from lfcShrink() show reduced magnitude of log2FoldChange estimates compared to base results, especially for genes with high standard error; effect is more pronounced with apeglm and ashr than with normal.
- Gene rankings by adjusted p-value or log fold change magnitude are identical or nearly identical across estimators (minor reordering only at boundary cases); no estimator should produce qualitatively different significance calls for genes with padj << 0.05 or >> 0.05.
- MA-plots for each estimator show shrunken fold changes pulled toward zero relative to unshrunk values; the degree and pattern of shrinkage differ visibly between apeglm, normal, and ashr.
- Summary statistics (e.g., mean, sd, range of shrunken log2FC) differ meaningfully between estimators; mean absolute shrunken fold change is typically smaller than unshrunk mean absolute fold change.

## Limitations

- lfcShrink() with apeglm or ashr can be computationally intensive for large data sets (many genes) due to fitting of prior parameters; normal prior is faster but less adaptive.
- Shrinkage assumes a unimodal prior on effect sizes; if the true distribution of log fold changes is multimodal or has heavy tails, ashr (mixture of normals) is more flexible than apeglm (t-prior) or normal (single normal prior).
- lfcShrink() is designed for single-contrast shrinkage; interaction or multi-level contrasts may require manual specification of the coefficient and careful interpretation.
- Comparison across estimators assumes the same experimental design and same genes are present in all results tables; pre-filtering (e.g., removal of very-low-count genes) must be applied consistently before extraction.

## Evidence

- [other] lfcShrink() can be applied with three different shrinkage estimator types (apeglm, normal, ashr): "lfcShrink() can be applied with three different shrinkage estimator types (apeglm, normal, ashr) to produce shrunken log fold change estimates from DESeq2 results objects."
- [other] Extract results table and apply multiple shrinkage estimators: "Extract the base results table using results() for the dex variable (treated vs untreated). Apply lfcShrink() with type='apeglm' to shrink log fold changes using the adaptive t-prior estimator. Apply"
- [other] Compare results using MA-plots and summary statistics: "Compare and visualize the three shrunken LFC results using MA-plots and summary statistics."
- [other] Base results extraction workflow: "res <- results(dds, name="condition_trt_vs_untrt")"
- [other] Shrinkage application workflow: "res <- lfcShrink(dds, coef="condition_trt_vs_untrt", type="apeglm")"
- [readme] ashr enables non-parametric shrinkage with mixture priors: "The ashr ("Adaptive SHrinkage") package aims to provide simple, generic, and flexible methods to derive "shrinkage-based" estimates and credible intervals for unknown quantities"
