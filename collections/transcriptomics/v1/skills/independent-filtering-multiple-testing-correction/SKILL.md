---
name: independent-filtering-multiple-testing-correction
description: Use when analyzing RNA-seq count data from a DESeq2 workflow where you have fitted negative binomial generalized linear models and need to extract final results. Use it specifically when you want to identify genes with adjusted p-value below a predetermined significance threshold (e.g., α=0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
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

# independent-filtering-multiple-testing-correction

## Summary

Automatically filter low-abundance genes before multiple-testing correction in RNA-seq differential expression analysis to improve statistical power and control false discovery rate. This skill combines independent filtering (removing genes with low mean normalized counts) with FDR-based multiple-testing correction to identify significantly differentially expressed genes.

## When to use

Apply this skill when analyzing RNA-seq count data from a DESeq2 workflow where you have fitted negative binomial generalized linear models and need to extract final results. Use it specifically when you want to identify genes with adjusted p-value below a predetermined significance threshold (e.g., α=0.1 for FDR) while maximizing statistical power by removing genes unlikely to show differential expression due to low abundance.

## When NOT to use

- Input data has already been pre-filtered by external count threshold—independent filtering will apply an additional, data-driven filter that may not align with your prior cutoff.
- You require gene-level p-values without multiple-testing correction (e.g., for visualization or hypothesis generation only).
- Your experimental design involves a very small number of genes (e.g., targeted panel <100 genes), where independent filtering may remove too many genes and compromise power.

## Inputs

- DESeqDataSet object (dds) after DESeq() analysis
- design formula (e.g., ~cell+dex)
- normalized count matrix
- sample metadata (cell type, treatment condition)

## Outputs

- results table with log2 fold changes, p-values, and adjusted p-values
- filtered gene list with padj < alpha
- count of significantly differentially expressed genes

## How to apply

After running DESeq(dds) to estimate dispersions and fit models, call results(dds) with your chosen alpha threshold (default alpha=0.1 implements FDR control). The results() function automatically performs independent filtering based on the mean of normalized counts for each gene—genes below a data-driven quantile cutoff are excluded before p-value adjustment. This reduces multiple-testing burden, increases sensitivity for the remaining genes, and avoids inflating type I error. Order the results table by adjusted p-value (padj) and extract genes meeting your padj < alpha threshold. The independent filtering step is performed internally by the results function and does not require manual specification of a count threshold.

## Related tools

- **DESeq2** (Performs negative binomial GLM fitting, independent filtering, and multiple-testing correction via results() function) — https://github.com/thelovelab/DESeq2
- **ashr** (Provides adaptive shrinkage methods for improved effect size estimation that can follow independent filtering and FDR correction) — https://github.com/stephens999/ashr
- **DEvis** (Visualizes and aggregates differential expression results including filtered gene sets) — https://github.com/price0416/DEvis

## Examples

```
dds <- DESeq(dds); res <- results(dds, alpha=0.1); res_ordered <- res[order(res$pvalue),]; sig_genes <- res_ordered[res_ordered$padj < 0.1,]; nrow(sig_genes)
```

## Evaluation signals

- Verify that the number of genes returned matches the reported count of genes with padj < alpha (e.g., in task_001, reproducibility of the exact count confirms correct filtering and correction).
- Check that the results table contains columns for baseMean, log2FoldChange, pvalue, padj, and padj values are strictly ≥ pvalue (indicating multiple-testing correction was applied).
- Confirm that independent filtering was active by verifying that very low-abundance genes (e.g., baseMean < 1) are absent from the results table, even if their raw p-value was significant.
- Validate that adjusted p-values are monotonically non-decreasing when results are ordered by p-value (property of independent filtering with Benjamini-Hochberg correction).
- Cross-check reproducibility: re-running results(dds, alpha=0.1) on the same dds object should yield identical gene counts and adjusted p-values.

## Limitations

- Independent filtering is automatic and uses a default quantile cutoff determined from the data; no user control over the exact count threshold unless manually pre-filtering before DESeq().
- The filter is designed for data with a wide range of counts; highly uniform or heavily pre-filtered datasets may not benefit from independent filtering.
- Results are sensitive to the alpha threshold chosen; no consensus exists on whether alpha=0.05, 0.1, or other values is appropriate for a given study, and FDR control assumes independence or weak dependence among tests.

## Evidence

- [other] the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene: "the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene"
- [other] Extract results using results(dds) with default alpha=0.1, which automatically performs independent filtering based on mean normalized counts.: "Extract results using results(dds) with default alpha=0.1, which automatically performs independent filtering based on mean normalized counts."
- [other] by removing rows in which there are very few reads, we reduce the memory size of the `dds` data object, and we increase the speed: "by removing rows in which there are very few reads, we reduce the memory size of the `dds` data object, and we increase the speed"
- [other] The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models: "The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models"
