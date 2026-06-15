---
name: hypothesis-weighting-statistical-control
description: Use when when you have completed DESeq2 differential expression analysis on RNA-seq count data and obtained p-values for each gene, use IHW if you want to improve power to detect true positives beyond standard independent filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - IHW
  - IHW (Independent Hypothesis Weighting)
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

# Hypothesis-Weighting Statistical Control

## Summary

Independent Hypothesis Weighting (IHW) is a data-driven filtering and multiple-testing correction method that weights p-values according to informative covariates (such as mean normalized counts) to increase statistical power while controlling false discovery rate. It is applied after differential expression testing to improve gene discovery by adaptively allocating α-level to genes where statistical power is highest.

## When to use

When you have completed DESeq2 differential expression analysis on RNA-seq count data and obtained p-values for each gene, use IHW if you want to improve power to detect true positives beyond standard independent filtering. IHW is particularly valuable when genes exhibit heterogeneous statistical power due to differences in baseline expression (mean normalized counts), sequencing depth, or dispersion—situations where some genes are inherently easier to test than others.

## When NOT to use

- When your design matrix is saturated (number of coefficients ≥ number of samples); IHW still filters but cannot reliably estimate power without independent replication structure.
- When mean normalized counts do not vary substantially across genes (e.g., highly uniform coverage), IHW gains will be minimal and standard independent filtering may be simpler.
- When your primary goal is confirmatory hypothesis testing of a pre-specified gene set; IHW is most beneficial for exploratory discovery where power heterogeneity is high.

## Inputs

- DESeqDataSet object (dds) after DESeq() has been run
- Raw p-values and test statistics from results(dds)
- Mean of normalized counts per gene (automatically computed by DESeq2)

## Outputs

- DESeqResults object with IHW-adjusted p-values (padj)
- FDR-controlled rejection set at specified α threshold
- IHW weights assigned to each gene based on mean normalized count
- Filtered results table documenting genes retained after IHW procedure

## How to apply

After running DESeq() and extracting results with results(dds), apply IHW by passing a filterFun=ihw argument to the results() function. IHW automatically uses mean normalized counts as a covariate to weight hypotheses: genes with higher mean counts (higher power) receive more of the multiple-testing budget, while genes with lower counts (lower power) are downweighted. The method estimates weights from the data itself, then applies weighted multiple-testing correction (e.g., Benjamini-Hochberg) to generate FDR-controlled adjusted p-values. Compare the number of genes passing the significance threshold (typically α=0.1) between standard independent filtering and IHW to assess the gain in discovery. Verify that adjusted p-value distributions are properly calibrated and that the method is not inflating false positives by checking the proportion of genes rejected at your chosen α level.

## Related tools

- **DESeq2** (Performs negative binomial GLM fitting and generates raw p-values and test statistics; required upstream step before IHW filtering) — https://github.com/thelovelab/DESeq2
- **IHW (Independent Hypothesis Weighting)** (Core method integrated into DESeq2's results() function via filterFun parameter; adaptively weights hypotheses by informative covariate to improve power)
- **ashr** (Related adaptive shrinkage method for effect size estimation; complements IHW by providing shrunk log fold changes via lfcShrink()) — https://github.com/stephens999/ashr

## Examples

```
res_ihw <- results(dds, filterFun=ihw); summary(res_ihw)
```

## Evaluation signals

- Number of genes passing adjusted p-value threshold (α=0.1 by default) is strictly ≥ standard independent filtering results, reflecting power gain from weighting.
- IHW-adjusted p-values are properly calibrated: the empirical rejection proportion at α should not exceed α (checking inflation of false positives).
- Mean normalized counts of rejected genes are skewed toward higher values compared to standard filtering, confirming that IHW reallocates detection budget toward high-power genes.
- Summary output from results(dds, filterFun=ihw) includes 'numRej' and 'threshold' fields documenting the FDR-controlling threshold and number of genes rejected.
- Comparison of filtered gene counts: document both the count and identity of genes retained under standard vs. IHW filtering to assess discovery gain.

## Limitations

- IHW assumes that the covariate (mean normalized counts) is independent of the test statistic under the null hypothesis; violation can bias weight estimation.
- Power of IHW depends on variance of the covariate; if mean counts are nearly uniform across genes, IHW offers little advantage over standard filtering.
- IHW does not account for batch effects or hidden confounders; pre-filtering and design specification remain critical.
- Computational cost increases with sample size and number of genes; large datasets may require optimized BLAS/LAPACK libraries (as noted for vicar/mouthwash packages that use similar hierarchical methods).
- The method is most effective when biological signal is sparse; in experiments with very high signal-to-noise ratios, gains are modest.

## Evidence

- [other] Separately apply Independent Hypothesis Weighting using results(dds, filterFun=ihw) to generate IHW-adjusted p-values and FDR-controlled rejection set.: "Separately apply Independent Hypothesis Weighting using results(dds, filterFun=ihw) to generate IHW-adjusted p-values and FDR-controlled rejection set."
- [other] The results() function automatically performs independent filtering based on the mean of normalized counts for each gene.: "the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene"
- [other] Compare filtered gene counts between standard independent filtering and IHW approaches, and verify adjusted p-value distributions match expected behavior.: "Compare filtered gene counts between standard independent filtering and IHW approaches, and verify adjusted p-value distributions match expected behavior."
