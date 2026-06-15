---
name: dispersion-estimation-negative-binomial
description: Use when you have raw RNA-seq count data (from HTSeq, featureCounts, Salmon, or similar quantification tools) organized in a count matrix with samples as columns and genes as rows, and you need to test for differential expression between conditions using a negative binomial model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - edgeR
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

# dispersion-estimation-negative-binomial

## Summary

Estimate gene-wise dispersion parameters for negative binomial generalized linear models in RNA-seq count data using DESeq2. This is a foundational step in differential expression analysis that accounts for the mean-variance relationship inherent in RNA-seq data.

## When to use

You have raw RNA-seq count data (from HTSeq, featureCounts, Salmon, or similar quantification tools) organized in a count matrix with samples as columns and genes as rows, and you need to test for differential expression between conditions using a negative binomial model. Dispersion estimation is mandatory before statistical inference on fold changes or p-values.

## When NOT to use

- Your data are already normalized (e.g., log2-transformed, FPKM, or TPM values); DESeq2 requires raw integer counts.
- You have fewer than ~3 biological replicates per condition; dispersion sharing across genes relies on sufficient sample size to fit a robust trend.
- Your experimental design is purely observational with no clear grouping variable; the design formula requires at least one categorical factor.

## Inputs

- count matrix (genes × samples, integer counts)
- sample metadata (colData with condition/factor assignments)
- design formula (e.g., ~condition or ~batch+condition)

## Outputs

- DESeqDataSet with estimated gene-wise dispersions (accessible via dispersions() function)
- fitted mean-dispersion trend curve
- per-gene negative binomial GLM coefficients and standard errors

## How to apply

Construct a DESeqDataSet object from your count matrix using a design formula that specifies the experimental factors (e.g., ~cell+dex for cell type and treatment effects). Call the DESeq() function, which internally estimates gene-wise dispersions in three stages: (1) compute a per-gene maximum-likelihood estimate, (2) fit a smooth curve (mean-dispersion trend) across all genes to share information, and (3) use the fitted curve as a prior to shrink individual gene estimates toward the trend. The degree of shrinkage is data-driven and stronger for genes with high variance or low counts. This moderated dispersion estimate improves statistical power by borrowing strength across genes while protecting against overfitting.

## Related tools

- **DESeq2** (Core package that implements dispersion estimation via moderated maximum-likelihood and empirical Bayes shrinkage toward a fitted trend) — https://github.com/thelovelab/DESeq2
- **edgeR** (Alternative package for negative binomial dispersion estimation (not discussed in this article but a common competitor))

## Examples

```
library(DESeq2); library(airway); data(airway); dds <- DESeqDataSet(airway, design = ~cell+dex); dds <- DESeq(dds); head(dispersions(dds))
```

## Evaluation signals

- Dispersion values should be positive and typically range from 0.01 to 10 for well-behaved RNA-seq data; very large dispersions (>100) suggest outliers or model misspecification.
- The fitted dispersion trend should be smooth and monotonically decreasing as a function of mean normalized count (higher-abundance genes have lower relative variance).
- Genes with similar mean expression should have similar shrunk dispersions due to the trend curve, whereas the per-gene ML estimates may be highly variable.
- Comparison of dispersions before and after shrinkage: shrunk values should be less extreme and more stable than raw ML estimates, especially for low-count genes.
- Post-estimation p-value distributions should be approximately uniform under the null (no differential expression); heavy right-skew suggests under-estimated dispersions.

## Limitations

- Dispersion estimation assumes negative binomial distribution; violations (e.g., zero-inflation, spatial correlation in sequencing artifacts) are not modeled.
- The smooth trend is fit using all genes; if a large fraction are truly differentially expressed, the trend may be biased upward.
- Very small sample sizes (<3 replicates per group) lead to unstable trend estimates and poor shrinkage; the article does not formally specify a minimum.
- Outlier samples or genes with extreme counts can distort the trend; pre-filtering of very low-count genes is recommended but not automatic.

## Evidence

- [other] The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models: "The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models"
- [other] Run DESeq() to estimate dispersions and fit negative binomial generalized linear models for each gene: "Run DESeq() to estimate dispersions and fit negative binomial generalized linear models for each gene"
- [other] Construct DESeqDataSet from count matrix with design formula: "dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition)"
- [other] the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene: "the *results* function automatically performs independent filtering based on the mean of normalized counts for each gene"
