---
name: gene-expression-statistical-testing
description: Use when you have fit a linear model to normalized gene expression data (microarray intensities or RNA-seq counts) and need to test for differential expression across experimental conditions or contrasts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  tools:
  - limma
  - R
derived_from:
- doi: 10.1186/gb-2014-15-2-r29
  title: limmavoom
- doi: 10.1093/nar/gkv007
  title: ''
evidence_spans:
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments and the assessment of differential expression
- Limma is an R package for the analysis of gene expression data
- Limma is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_limmavoom
    doi: 10.1186/gb-2014-15-2-r29
    title: limmavoom
  dedup_kept_from: coll_limmavoom
schema_version: 0.2.0
---

# gene-expression-statistical-testing

## Summary

Apply empirical Bayesian moderation to gene-wise variance estimates in order to compute stable moderated t-statistics and B-statistics (log-odds of differential expression) from linear model fits of microarray or RNA-seq count data. This approach yields robust significance assessments even when the number of arrays or replicates is small.

## When to use

You have fit a linear model to normalized gene expression data (microarray intensities or RNA-seq counts) and need to test for differential expression across experimental conditions or contrasts. Use this skill when sample size per group is limited (< 10) and you want variance estimates that borrow strength across genes to avoid inflated false positives from genes with spuriously low observed variance.

## When NOT to use

- Your input is already a matrix of p-values or test statistics from another tool; you would be double-testing.
- You have a very large sample size (n > 100 per group) and unmoderated t-tests would be sufficient; empirical Bayes is most beneficial when borrowing strength across genes matters.
- Your data have not been normalized and background-corrected; apply those preprocessing steps first.

## Inputs

- lmFit object (fitted linear model with gene-level coefficients and residual variances)
- normalized gene expression matrix (rows: genes, columns: arrays/samples)
- experimental design matrix or contrast specification

## Outputs

- moderated t-statistics per gene per contrast
- B-statistics (log-odds) per gene per contrast
- adjusted p-values per gene per contrast
- results table with gene identifiers, log-fold changes, moderated t-statistics, p-values, and B-statistics

## How to apply

Start with a pre-fitted lmFit object containing gene-level coefficients and residual variances from your experimental design. Apply the eBayes function to estimate hyperparameters of a prior distribution over gene-wise variances using empirical Bayes; this moderates each gene's variance estimate by shrinking it toward the genome-wide trend. Extract the resulting moderated t-statistics (which are t-distributed under the null) and B-statistics (log-posterior odds of non-zero log-fold change). Compute adjusted p-values from the moderated t-statistics using a multiple-testing correction method (e.g., Benjamini–Hochberg FDR). Sort results by adjusted p-value or B-statistic to prioritize the most significant genes. The moderation step is crucial because it stabilizes variance estimates for genes with few replicates, making the statistical tests more powerful and reliable than ordinary t-tests.

## Related tools

- **limma** (R package implementing empirical Bayes hyperparameter estimation (eBayes) and moderated t-statistic computation for linear models of gene expression) — https://github.com/bioconductor/limma
- **R** (Programming environment for running limma functions and statistical analyses)

## Examples

```
fit <- lmFit(eset, design); eb <- eBayes(fit); results <- topTable(eb, adjust.method='BH', number=Inf, sort.by='p')
```

## Evaluation signals

- Moderated variance estimates should be less extreme (closer to the genome-wide median) than unmoderated variances, especially for genes with few replicates.
- Moderated t-statistics should have a t-distribution under the null; check Q–Q plot of t-statistics against theoretical t quantiles.
- B-statistics should be symmetric around 0 for non-differentially expressed genes; negative B indicates genes favoring the null hypothesis.
- Adjusted p-values (e.g., FDR) should be ≥ unadjusted p-values and should not exceed 1.
- Results table should contain no missing values in moderated t-statistics or B-statistics columns; check for computational failures or singular fits.

## Limitations

- Empirical Bayes assumes a common prior distribution across genes, which may not hold if gene expression is highly heterogeneous (e.g., very highly expressed genes may have different variance structure).
- Results rely on the correctness of the upstream linear model fit; misspecification of the design matrix or presence of batch effects not accounted for will propagate into biased statistics.
- With very few replicates (n < 3 per group), prior hyperparameter estimates can be unstable; the method is designed for 'small n' but not 'tiny n'.
- The approach assumes variance is independent of the mean after appropriate transformation (log or voom); violations may require separate variance modeling by expression level.

## Evidence

- [other] Empirical Bayesian methods in limma estimate hyperparameters of the prior distribution over gene-wise variances, enabling computation of moderated t-statistics and B-statistics that remain stable even with small numbers of arrays.: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] The workflow applies empirical Bayes to fit the prior distribution over gene-wise variances and stabilize variance estimates.: "Apply empirical Bayes hyperparameter estimation using limma's eBayes function to fit the prior distribution over gene-wise variances and stabilize variance estimates."
- [other] Linear model and differential expression functions apply to microarrays, quantitative PCR, RNA-seq and proteomics.: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or"
- [other] Normalization and background correction functions are provided as a prerequisite step.: "The normalization and background correction functions are provided for microarrays and similar technologies."
