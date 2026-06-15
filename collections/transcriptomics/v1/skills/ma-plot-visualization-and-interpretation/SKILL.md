---
name: ma-plot-visualization-and-interpretation
description: Use when after obtaining shrunken or unshrunken log fold change estimates from DESeq2 results objects, particularly when comparing multiple shrinkage estimator types (apeglm, normal, ashr) or evaluating the effect of shrinkage on fold change estimates across genes with varying expression levels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - ashr
  - ggplot2 / base R plotting
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

# MA-plot visualization and interpretation

## Summary

MA-plots display the relationship between mean normalized count (A-axis) and log fold change (M-axis) for each gene, enabling visual assessment of the magnitude, direction, and variability of differential expression across the dynamic range. This skill is essential for comparing shrinkage estimators and detecting systematic biases in fold change estimates.

## When to use

After obtaining shrunken or unshrunken log fold change estimates from DESeq2 results objects, particularly when comparing multiple shrinkage estimator types (apeglm, normal, ashr) or evaluating the effect of shrinkage on fold change estimates across genes with varying expression levels. Use MA-plots to identify whether shrinkage is working appropriately and whether fold changes are being over- or under-corrected.

## When NOT to use

- Input is already a visualization (e.g., pre-rendered PNG/PDF plot) — re-plotting is unnecessary
- Analyzing non-count-based data (e.g., microarray intensities, proteomics) where baseMean has a different interpretation
- When fold changes have not been extracted from a fitted DESeq2 model — MA-plots require both expression level and effect size estimates

## Inputs

- DESeqResults object with baseMean and log2FoldChange columns
- Multiple shrunken DESeqResults objects (one per estimator type: apeglm, normal, ashr)

## Outputs

- MA-plot(s) with genes plotted as points (baseMean vs. log2FoldChange)
- Comparative visualizations of shrunken vs. unshrunken fold changes
- Summary statistics comparing fold change distributions across estimators

## How to apply

Extract the results object from DESeq2 containing baseMean (mean normalized counts) and log2FoldChange columns. Plot baseMean on the x-axis (typically log10-scaled) and log2FoldChange on the y-axis, with each point representing one gene. Add a horizontal line at y=0 to mark the null effect. When comparing shrinkage estimators, create side-by-side or overlaid MA-plots for results from lfcShrink(..., type='apeglm'), lfcShrink(..., type='normal'), and lfcShrink(..., type='ashr') to visualize how each estimator pulls fold changes toward zero differently. Genes with low mean counts typically show larger shrinkage (smaller vertical spread near y=0), while highly expressed genes retain larger fold changes. Summary statistics (mean shrunken vs. unshrunken LFC, proportion of genes with |LFC| > threshold) should accompany the visual comparison.

## Related tools

- **DESeq2** (Generates DESeqResults objects with baseMean and log2FoldChange; lfcShrink() produces shrunken estimates for comparison) — https://github.com/thelovelab/DESeq2
- **ashr** (Provides shrinkage estimator type 'ashr' for lfcShrink(), using adaptive shrinkage with mixture of normals prior) — https://github.com/stephens999/ashr
- **ggplot2 / base R plotting** (Standard tools for rendering MA-plots; not explicitly named but required for visualization)

## Examples

```
res_apeglm <- lfcShrink(dds, coef="dex_treated_vs_untreated", type="apeglm"); res_normal <- lfcShrink(dds, coef="dex_treated_vs_untreated", type="normal"); res_ashr <- lfcShrink(dds, coef="dex_treated_vs_untreated", type="ashr"); par(mfrow=c(1,3)); plotMA(res_apeglm, main="apeglm"); plotMA(res_normal, main="normal"); plotMA(res_ashr, main="ashr")
```

## Evaluation signals

- Verify that genes with low baseMean show tighter clustering around y=0 (stronger shrinkage) compared to high-baseMean genes
- Confirm that unshrunken and shrunken fold changes coincide for highly expressed genes but diverge for low-count genes
- Check that all three estimator types (apeglm, normal, ashr) produce visually distinct patterns of shrinkage, reflecting their different prior assumptions
- Ensure the horizontal reference line at y=0 is clearly marked to identify the null hypothesis
- Compare summary statistics: proportion of genes with |log2FC| > 1 or > 2 should decrease after shrinkage, and the effect should be inversely correlated with baseMean

## Limitations

- MA-plots are inherently 2D and cannot simultaneously display p-values, adjusted significance, or confidence intervals; additional annotations or linked plots are needed for complete assessment
- The effectiveness of shrinkage visualization depends on the number of genes and the distribution of baseMean values; sparse or highly skewed datasets may obscure patterns
- Different shrinkage estimators (apeglm, normal, ashr) make different assumptions about the prior distribution of true fold changes; visual comparison alone cannot determine which is most appropriate without downstream validation (e.g., validation qPCR, replication, known true positives)
- Overlaying or side-by-side plotting of multiple estimators can become visually cluttered with large numbers of genes; filtering to top DE genes or using faceted plots is recommended

## Evidence

- [other] Compare and visualize the three shrunken LFC results using MA-plots and summary statistics: "Compare and visualize the three shrunken LFC results using MA-plots and summary statistics."
- [other] lfcShrink() can be applied with three different shrinkage estimator types (apeglm, normal, ashr) to produce shrunken log fold change estimates from DESeq2 results objects: "lfcShrink() can be applied with three different shrinkage estimator types (apeglm, normal, ashr) to produce shrunken log fold change estimates from DESeq2 results objects."
- [other] Apply lfcShrink() with type='apeglm' to shrink log fold changes using the adaptive t-prior estimator; type='normal' using the original adaptive normal prior; type='ashr' using the adaptive shrinkage estimator with mixture of normals: "Apply lfcShrink() with type='apeglm' to shrink log fold changes using the adaptive t-prior estimator. Apply lfcShrink() with type='normal' to shrink log fold changes using the original adaptive"
- [other] Extract results with log2 fold changes and p-values: "Extract results with log2 fold changes and p-values"
- [other] Shrink log fold changes using lfcShrink with specified coefficient and estimator type: "res <- lfcShrink(dds, coef="condition_trt_vs_untrt", type="apeglm")"
