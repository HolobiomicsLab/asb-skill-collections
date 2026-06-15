---
name: p-value-adjustment-methodology
description: Use when after running DESeq() to fit negative binomial GLMs and obtaining raw p-values from results(dds), when you need to reduce false positives from multiple testing across thousands of genes while maximizing statistical power.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3053
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - IHW
  - IHW (Independent Hypothesis Weighting)
  - ashr (Adaptive Shrinkage)
  - DEvis
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

# p-value-adjustment-methodology

## Summary

Systematic adjustment of p-values from differential expression tests to control false discovery rate and account for multiple hypothesis testing, using either independent filtering based on mean normalized counts or weighting-based approaches like Independent Hypothesis Weighting (IHW). This skill is essential for producing reliable, FDR-controlled gene lists from RNA-seq experiments.

## When to use

After running DESeq() to fit negative binomial GLMs and obtaining raw p-values from results(dds), when you need to reduce false positives from multiple testing across thousands of genes while maximizing statistical power. Use this skill when your DESeq2 results object contains unadjusted p-values and you want to filter genes with weak or uninformative power (very low mean normalized counts) before or during adjustment.

## When NOT to use

- Input p-values are already adjusted or come from a non-DESeq2 pipeline not designed for count data (use appropriate method for that pipeline instead).
- Your research question requires testing all genes including those with very low expression; independent filtering may be too aggressive for rare-gene discovery.

## Inputs

- DESeqDataSet object (dds) after DESeq() differential expression analysis
- Raw p-values and log2 fold changes from results(dds)
- Mean normalized counts per gene (computed internally by DESeq2)

## Outputs

- Adjusted p-value vector (padj) with independent filtering applied
- Filtered results table with genes passing threshold
- Summary statistics: count of genes retained/filtered at alpha=0.1
- IHW-adjusted p-values (optional alternative output)
- FDR-controlled rejection set

## How to apply

The results() function in DESeq2 automatically applies independent filtering based on the mean of normalized counts for each gene, removing genes below a data-driven threshold before multiple testing correction. This filtering improves power by reducing the multiple testing burden. Alternatively, apply Independent Hypothesis Weighting (IHW) via results(dds, filterFun=ihw) to generate IHW-adjusted p-values that weight hypotheses by their informativeness (based on mean counts), producing an FDR-controlled rejection set. Compare the number of genes retained and examine the distribution of adjusted p-values to verify that filtering is appropriate for your dataset and research question. Export summary statistics documenting genes retained after each filtering method for reproducibility.

## Related tools

- **DESeq2** (Performs differential expression analysis, computes raw p-values, and automatically applies independent filtering during results() call) — https://github.com/thelovelab/DESeq2
- **IHW (Independent Hypothesis Weighting)** (Optional alternative filtering strategy that weights p-values by informativeness to improve power while controlling FDR) — https://github.com/stephens999/ashr
- **ashr (Adaptive Shrinkage)** (Provides shrinkage-based estimates and credible intervals for fold changes; can be used with lfcShrink() for post-hoc estimation after p-value adjustment) — https://github.com/stephens999/ashr
- **DEvis** (Visualization and aggregation of differential expression results including adjusted p-values and filtered gene sets) — https://github.com/price0416/DEvis

## Examples

```
res <- results(dds, name="condition_trt_vs_untrt"); resFiltered <- res[!is.na(res$padj) & res$padj < 0.1, ]; summary(res)
```

## Evaluation signals

- Adjusted p-values (padj column) are equal to or larger than raw p-values, with padj values ≥ alpha threshold set to NA for filtered genes.
- Independent filtering threshold is automatically optimized and reproducible; verify it by inspecting the filtering cutoff used (available in metadata of results object).
- Number of genes with padj < alpha should be smaller than the number with pvalue < alpha, reflecting multiple testing correction.
- IHW-adjusted results (if used) show fewer rejections than standard Benjamini–Hochberg but higher power than non-weighted filtering on comparable datasets, as documented in comparison tables.
- Summary of filtered vs. retained gene counts should be reported and matches downstream analysis (e.g., gene lists for functional enrichment).

## Limitations

- Independent filtering assumes that genes with low mean normalized counts have low power to detect true signal; this may not hold for rare but highly expressed isoforms or tissue-specific genes.
- The data-driven threshold is optimized for a single test coefficient; users testing multiple contrasts must re-run results() and filtering separately for each comparison.
- IHW requires sufficient independent p-value distribution information; small sample sizes or highly correlated designs may produce unstable weighting.

## Evidence

- [other] The results() function automatically performs independent filtering based on the mean of normalized counts for each gene.: "the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene"
- [other] Independent filtering reduces multiple testing burden and improves power by removing low-information genes.: "by removing rows in which there are very few reads, we reduce the memory size of the `dds` data object, and we increase the speed"
- [other] IHW is an alternative weighting-based approach for p-value adjustment.: "Separately apply Independent Hypothesis Weighting using results(dds, filterFun=ihw) to generate IHW-adjusted p-values and FDR-controlled rejection set"
- [other] DESeq2 uses negative binomial generalized linear models for differential expression testing.: "The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models"
