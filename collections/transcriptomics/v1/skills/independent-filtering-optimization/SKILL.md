---
name: independent-filtering-optimization
description: Use when you have completed DESeq differential expression analysis on a DESeqDataSet and obtained raw results with p-values across all genes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - IHW
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

# independent-filtering-optimization

## Summary

Automatically filter low-signal genes in RNA-seq differential expression analysis by applying independent filtering based on mean normalized counts, reducing multiple testing burden and improving statistical power while controlling false discovery rate. This skill optimizes the results() function's built-in filtering mechanism in DESeq2, and can be further refined using data-adaptive approaches like Independent Hypothesis Weighting (IHW).

## When to use

You have completed DESeq differential expression analysis on a DESeqDataSet and obtained raw results with p-values across all genes. Apply this skill when you want to remove genes with negligible expression (low mean normalized counts) before multiple testing correction, since these genes have inherently low power to detect fold changes and add noise to FDR estimation. Use when your goal is to maximize the number of discoveries at a fixed FDR threshold or to improve the calibration of adjusted p-values.

## When NOT to use

- Your input is a pre-filtered gene list or feature table — independent filtering is designed to work on the full set of genes tested
- You have already manually removed low-count genes prior to DESeq() — applying automatic filtering after manual pre-filtering may remove additional genes unexpectedly
- Your analysis uses a custom statistical test or external p-values not produced by DESeq() — the independent filtering method is calibrated for negative binomial GLM results

## Inputs

- DESeqDataSet (dds) after DESeq() analysis with estimated dispersions and negative binomial GLM fits
- Raw count matrix and sample metadata (colData)

## Outputs

- DESeqResults object with log2 fold changes, p-values, and adjusted p-values for filtered genes
- Summary statistics documenting filtering threshold and number of genes retained
- Filtered results table with independent filtering or IHW-adjusted p-values

## How to apply

The results() function in DESeq2 automatically performs independent filtering based on the mean of normalized counts for each gene, removing genes below a data-driven threshold and thereby reducing the multiple testing burden. Call results(dds) with default alpha=0.1 to apply this filtering and obtain log2 fold changes, p-values, and adjusted p-values on the filtered gene set. For enhanced filtering, alternatively invoke results(dds, filterFun=ihw) to apply Independent Hypothesis Weighting, which generates IHW-adjusted p-values and a rejection set controlled at your specified FDR level. Compare the filtered gene counts and adjusted p-value distributions between the standard independent filtering and IHW approaches to verify that filtering behavior matches expectations (fewer genes retained, improved calibration of remaining p-values). Document the number of genes retained after filtering and the filtering threshold applied, as these metrics confirm correct application.

## Related tools

- **DESeq2** (Core package providing the results() function, automatic independent filtering based on mean normalized counts, and negative binomial GLM framework for differential expression testing) — https://github.com/thelovelab/DESeq2
- **IHW** (Data-adaptive filtering and multiple testing correction method invoked via filterFun=ihw parameter in results() to optimize the rejection set by weighting hypotheses)

## Examples

```
library(DESeq2); dds <- DESeq(dds); res <- results(dds, alpha=0.1); summary(res)
```

## Evaluation signals

- Verify that the number of genes retained after filtering is lower than the total number of input genes, confirming that low-expression genes were removed
- Check that adjusted p-values for filtered genes follow the expected uniform distribution under the null hypothesis, indicating proper FDR calibration
- Confirm that the filtering threshold (stored in results metadata) is a positive value corresponding to the mean normalized count cutoff applied
- Compare independent filtering results to IHW results and verify that IHW retains the same or fewer genes (since it applies additional weighting), with adjusted p-values that show improved or equivalent FDR control
- Inspect the results summary table (e.g., from summary(res)) to confirm the number of genes with p < alpha and the number removed by independent filtering match expectations

## Limitations

- Independent filtering's threshold is data-driven and may vary across datasets; the filtering cutoff is not user-specified and depends on the mean-variance relationship of the data
- Filtering assumes that genes with low mean normalized counts are uninformative — this assumption may fail for rare but real biological signals (e.g., genes expressed in a small subset of samples)
- The method is calibrated for negative binomial GLM results from DESeq2; application to other test statistics or count distributions requires separate validation
- IHW-adjusted results require additional computational cost and may be sensitive to the choice of filtering function; standard independent filtering is simpler but less adaptive

## Evidence

- [other] Automatic independent filtering based on mean normalized counts: "the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene"
- [other] Default alpha and filtering behavior: "Extract results using results(dds) with default alpha=0.1 to obtain log2 fold changes, p-values, and automatically applied independent filtering based on mean normalized count threshold"
- [other] IHW as alternative filtering approach: "Separately apply Independent Hypothesis Weighting using results(dds, filterFun=ihw) to generate IHW-adjusted p-values and FDR-controlled rejection set"
- [other] Comparison and validation of filtering methods: "Compare filtered gene counts between standard independent filtering and IHW approaches, and verify adjusted p-value distributions match expected behavior"
