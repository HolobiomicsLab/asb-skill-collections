---
name: adaptive-prior-distribution-selection
description: Use when after running DESeq() and extracting raw results with results(), when you have log fold change estimates with high variance and wish to improve their precision.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3563
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - ashr
  - apeglm
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

# adaptive-prior-distribution-selection

## Summary

Select and apply an adaptive prior distribution (apeglm, normal, or ashr) to shrink log fold change estimates in DESeq2 differential expression analysis. This skill determines which shrinkage estimator best matches the empirical characteristics of your data, improving precision of effect size estimates while controlling for estimation uncertainty.

## When to use

After running DESeq() and extracting raw results with results(), when you have log fold change estimates with high variance and wish to improve their precision. Apply this skill when comparing treatment-vs-control or multi-level contrasts where effect sizes span a wide range and you need to borrow information across genes to reduce noise in small-effect estimates.

## When NOT to use

- Input count matrix has not been normalized by DESeq() or variance stabilization has not been performed.
- Contrast has fewer than ~10–20 genes with measurable signal; adaptive priors require sufficient empirical data to learn the effect size distribution.
- Your biological question requires unbiased (unshrunk) log fold changes for downstream meta-analysis or publication of raw effect sizes; shrinkage trades bias for precision.

## Inputs

- DESeqDataSet object (after DESeq() normalization and dispersion estimation)
- results object from results() containing raw log fold changes and standard errors
- contrast specification (coef or name parameter identifying which design coefficient to shrink)

## Outputs

- shrunken results object with lfcSE and adjusted log fold changes
- summary statistics comparing shrinkage across estimator types
- MA-plots visualizing the degree and distribution of shrinkage per estimator

## How to apply

Extract the base results table using results() for your contrast of interest. Then apply lfcShrink() with one of three type parameters: type='apeglm' uses an adaptive t-prior estimator suitable for robust shrinkage with outliers; type='normal' uses the original adaptive normal prior assuming symmetric, unimodal effect size distribution; type='ashr' uses adaptive shrinkage with a flexible mixture-of-normals prior that automatically learns the effect size distribution from the data. Compare the three shrunken LFC results using MA-plots and summary statistics (number of genes crossing significance thresholds, shrinkage magnitude) to assess which estimator best stabilizes your estimates without over-shrinking true signals.

## Related tools

- **DESeq2** (Provides DESeqDataSet construction, normalization, dispersion estimation, and the lfcShrink() function for applying adaptive priors to shrink log fold changes.) — https://github.com/thelovelab/DESeq2
- **ashr** (Supplies the adaptive shrinkage estimator with mixture-of-normals prior (type='ashr' option in lfcShrink); implements empirical Bayes shrinkage of effect sizes using flexible, unimodal distributions.) — https://github.com/stephens999/ashr
- **apeglm** (Provides the adaptive t-prior shrinkage estimator (type='apeglm' in lfcShrink); robust to outlier effect sizes and heavy-tailed distributions.)

## Examples

```
res <- lfcShrink(dds, coef="dex_treated_vs_untreated", type="apeglm")
```

## Evaluation signals

- MA-plots show expected shrinkage pattern: log fold changes near zero are shrunk toward zero more aggressively than large-magnitude changes, and the shrinkage magnitude differs meaningfully across the three estimator types.
- Comparison of summary statistics (e.g., number of genes with |log2FC| > 1 and padj < 0.05) reveals that each estimator produces distinct, interpretable results; extreme disagreement suggests model misfit or data quality issues.
- The shrunken log fold changes have reduced standard error (lfcSE field) compared to raw estimates, indicating successful information borrowing; lfcSE should be substantially smaller than the raw standard errors.
- Visual inspection of the results object confirms that the 'log2FoldChange' and 'lfcSE' columns have been updated by lfcShrink() and differ from the raw results() output.
- Check that the results object retains all original metadata (gene names, base mean counts, p-values) while adding shrinkage-specific columns; no genes should be lost in the shrinkage step.

## Limitations

- apeglm, normal, and ashr estimators assume that effect sizes follow a unimodal, symmetric distribution centered near zero; severe departures (e.g., bimodal or heavy-tailed distributions) may lead to suboptimal shrinkage.
- Adaptive priors require sufficient sample size and number of genes to learn the effect size distribution empirically; small studies (< 10 genes or < 2–3 replicates per condition) may show unstable or over-regularized estimates.
- The ashr estimator is computationally more expensive than apeglm or normal and may be slow on very large gene counts (> 20,000); apeglm offers a faster, robust alternative.
- Shrinkage reduces the variance of estimates at the cost of introducing bias; if your downstream analysis requires unbiased point estimates or precise confidence intervals, shrinkage may not be appropriate.

## Evidence

- [other] lfcShrink() application with apeglm estimator: "Apply lfcShrink() with type='apeglm' to shrink log fold changes using the adaptive t-prior estimator."
- [other] lfcShrink() application with normal and ashr estimators: "Apply lfcShrink() with type='normal' to shrink log fold changes using the original adaptive normal prior. 6. Apply lfcShrink() with type='ashr' to shrink log fold changes using the adaptive shrinkage"
- [other] Comparison and visualization of shrinkage results: "Compare and visualize the three shrunken LFC results using MA-plots and summary statistics."
- [readme] ashr package description of adaptive shrinkage methodology: "The ashr ('Adaptive SHrinkage') package aims to provide simple, generic, and flexible methods to derive 'shrinkage-based' estimates and credible intervals for unknown quantities, given only estimates"
- [readme] Adaptive nature of ashr shrinkage: "The 'adaptive' nature of the shrinkage is two-fold. First, the appropriate amount of shrinkage is determined from the data, rather than being pre-specified. Second, the amount of shrinkage undergone"
