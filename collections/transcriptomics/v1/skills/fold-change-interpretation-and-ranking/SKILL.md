---
name: fold-change-interpretation-and-ranking
description: Use when after running DESeq() on a DESeqDataSet and extracting results with results(dds), you have a results table with log₂ fold changes, p-values, and adjusted p-values (padj). Use this skill when you need to (1) identify genes meeting a significance threshold (e.g., padj < 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_3673
  tools:
  - DESeq2
  - ashr (Adaptive Shrinkage)
  - vicar
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

# fold-change-interpretation-and-ranking

## Summary

Interpret and rank genes by log₂ fold change and adjusted p-value after DESeq2 differential expression analysis to prioritize biologically significant changes while controlling false discovery rate. This skill bridges raw statistical output to ranked candidate lists suitable for downstream validation.

## When to use

After running DESeq() on a DESeqDataSet and extracting results with results(dds), you have a results table with log₂ fold changes, p-values, and adjusted p-values (padj). Use this skill when you need to (1) identify genes meeting a significance threshold (e.g., padj < 0.1 for FDR control), (2) rank them by magnitude of effect to prioritize strong signals, or (3) create a filtered, ordered list for publication or functional validation.

## When NOT to use

- Input count data has not yet been normalized and tested for differential expression (DESeq() not yet run).
- You are working with pre-computed fold changes from other tools that do not report adjusted p-values or do not control for multiple testing.
- The study design is not a simple two-group comparison; more complex contrasts require explicit specification of the 'contrast' or 'name' parameter in results().
- You need to account for hidden confounders or unwanted variation not captured in the design formula; consider confounder adjustment packages like vicar or sva before DESeq().

## Inputs

- DESeqResults object from results(dds) with columns: log2FoldChange, pvalue, padj, baseMean
- integer threshold alpha for adjusted p-value cutoff (e.g., 0.1 for FDR ≤ 10%)

## Outputs

- Ordered results table (data.frame or DataFrame) filtered to padj < alpha, sorted by padj and/or |log2FoldChange|
- Integer count of significant genes meeting padj threshold
- Ranked candidate gene list for downstream validation or annotation

## How to apply

First, extract the results table from the DESeq2 object using results(dds), which automatically performs independent filtering based on mean normalized counts to maximize statistical power and reduce multiple testing burden. Then apply a threshold on adjusted p-value (padj) — the default alpha=0.1 corresponds to FDR control at 10% — to identify statistically significant genes. Finally, order the results table by padj (ascending) and optionally by |log₂FC| (descending) to rank genes by combined significance and effect size. The log₂ fold change values are shrunken estimates (optionally further improved using lfcShrink() with methods like 'apeglm') that balance statistical accuracy with biological interpretability, avoiding inflation of large fold changes in low-count genes.

## Related tools

- **DESeq2** (Core package that estimates dispersion, fits negative binomial GLM, and outputs log₂ fold changes with p-values and adjusted p-values (padj) for ranking and filtering) — https://github.com/thelovelab/DESeq2
- **ashr (Adaptive Shrinkage)** (Optional post-hoc shrinkage of log₂ fold changes to improve estimation stability and interpretability, especially for genes with high standard error; can be integrated via lfcShrink(type='ashr')) — https://github.com/stephens999/ashr
- **vicar** (Confounder adjustment package using methods like mouthwash/backwash; useful when hidden confounders may inflate fold changes before DESeq2 analysis) — https://github.com/dcgererd/vicar
- **DEvis** (Visualization and exploration tool for aggregating and visualizing differential expression results including fold change rankings and volcano plots) — https://github.com/price0416/DEvis

## Examples

```
res <- results(dds); resOrdered <- res[order(res$padj),]; sigGenes <- resOrdered[resOrdered$padj < 0.1,]; nrow(sigGenes)
```

## Evaluation signals

- Number of genes with padj < alpha matches expected FDR control (check count against independent filtering diagnostics).
- Log₂ fold changes are symmetric around zero (no systematic bias toward up- or down-regulation) unless biology predicts asymmetry.
- Top-ranked genes by padj have non-zero log₂FC values; verify shrinkage has not collapsed weak signals to zero.
- Volcano plot (log₂FC vs. -log₁₀(padj)) shows clear separation of significant (top) from non-significant genes; shape should reflect the gene count distribution.
- Independent filtering baseline threshold (mean normalized count cutoff) is reported; verify it was automatically applied and did not remove >50% of genes (sign of poor sample quality or incorrect design).

## Limitations

- Adjusted p-value threshold (alpha) is a statistical cutoff, not a biological one; genes just above padj=0.1 may have large fold changes and merit experimental follow-up.
- Log₂ fold change magnitude can be inflated in low-count genes even after shrinkage; prioritize genes with high baseMean (normalized count) for higher confidence in biological effect.
- Independent filtering is automatic but data-driven; if most genes have very low counts, the filtering threshold may be lenient, requiring manual pre-filtering (keep <- rowSums(counts(dds) >= 10) >= smallestGroupSize).
- Ranking by padj alone ignores effect size; a gene with padj=0.001 and log₂FC=0.1 ranks above padj=0.05 and log₂FC=2.0, so simultaneous consideration of both metrics is recommended.
- Design formula misspecification (e.g., omitting batch effects or cell type) can inflate fold changes and padj values; validate model assumptions before interpreting results.

## Evidence

- [other] results(dds) with default alpha=0.1, which automatically performs independent filtering based on mean normalized counts: "Extract results using results(dds) with default alpha=0.1, which automatically performs independent filtering based on mean normalized counts for each gene"
- [other] Negative binomial GLM for fold change and p-value estimation: "The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models"
- [other] Order results by adjusted p-value to identify significant genes: "Order the results table by adjusted p-value to identify significantly differentially expressed genes (padj < 0.1)"
- [other] Log₂ fold change shrinkage rationale: "Shrink log fold changes using lfcShrink(dds, coef='condition_trt_vs_untrt', type='apeglm')"
- [other] Independent filtering removes low-count genes to reduce false positives and improve power: "by removing rows in which there are very few reads, we reduce the memory size of the `dds` data object, and we increase the speed"
