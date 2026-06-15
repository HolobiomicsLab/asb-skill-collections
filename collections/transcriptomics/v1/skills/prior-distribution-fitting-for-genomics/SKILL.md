---
name: prior-distribution-fitting-for-genomics
description: Use when you have a fitted linear model (lmFit object) from microarray or RNA-seq count data and need to compute differential expression statistics, especially when the number of biological replicates is small (fewer than ~5–10 arrays/samples per group) and you want to avoid inflated variance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
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

# prior-distribution-fitting-for-genomics

## Summary

Empirical Bayesian estimation of hyperparameters in the prior distribution over gene-wise variances, enabling computation of moderated t-statistics and B-statistics that remain stable even with small sample sizes in microarray and RNA-seq studies. This skill stabilizes variance estimates across genes by pooling information through a shared prior.

## When to use

Apply this skill when you have a fitted linear model (lmFit object) from microarray or RNA-seq count data and need to compute differential expression statistics, especially when the number of biological replicates is small (fewer than ~5–10 arrays/samples per group) and you want to avoid inflated variance estimates for genes with low expression or high technical noise.

## When NOT to use

- Input is already a feature table or count matrix without a fitted linear model; eBayes requires an lmFit object as input.
- Sample size is very large (>100 samples per group) and individual gene variances are well-estimated; the stabilization benefit of the prior becomes marginal.
- Data are already adjusted or normalized using external Bayesian shrinkage methods that independently estimate gene-wise variances; double-shrinking may reduce power.

## Inputs

- lmFit object (fitted linear model from limma's lmFit function)
- design matrix (specifying experimental groups or conditions)
- expression matrix (gene × sample, normalized counts or log-intensity values)

## Outputs

- eBayes object containing moderated t-statistics
- B-statistics (log-odds of differential expression)
- adjusted p-values (e.g., Benjamini–Hochberg)
- results table with gene IDs, log-fold changes, moderated t-stats, p-values, and B-statistics

## How to apply

Load a pre-fitted lmFit object into R and apply the eBayes function from limma to estimate the parameters (mean, variance, and degrees of freedom) of a scaled inverse-chi-squared prior distribution over gene-wise variances. The function uses a robust empirical Bayesian algorithm to shrink individual gene variances toward a common estimate, stabilizing variance estimates especially for genes with few degrees of freedom. Extract the resulting moderated t-statistics (which use the shrunken variances in the denominator) and B-statistics (log-odds of differential expression under the null vs. alternative hypothesis). The moderated statistics remain valid even when the number of arrays is small because they borrow strength across genes through the shared prior. Sort results by adjusted p-value or B-statistic magnitude to identify genes with the strongest evidence of differential expression.

## Related tools

- **limma** (R package providing lmFit and eBayes functions for fitting linear models and empirical Bayesian hyperparameter estimation on microarray and RNA-seq data) — https://github.com/bioconductor/limma
- **R** (Runtime environment for executing limma package and statistical analysis)

## Examples

```
fit <- lmFit(eset, design); efit <- eBayes(fit); top <- topTable(efit, number=Inf, adjust.method='BH')
```

## Evaluation signals

- Moderated t-statistics and B-statistics are present in the output object and differ from ordinary t-statistics due to variance shrinkage (inspect via topTable() or decideTests()).
- Gene-wise variance estimates in the eBayes object are more stable and less extreme than those from lmFit alone, especially for genes with low counts or few replicates.
- Adjusted p-values are well-calibrated (e.g., inflation/deflation plots show reasonable quantile–quantile correspondence) and reflect the degrees-of-freedom adjustment from the prior.
- B-statistics increase for genes with strong effect sizes and low variance, indicating improved log-odds estimates under the prior.
- Results remain consistent across different random seeds if fitting uses robust variance estimation (robust=TRUE in eBayes).

## Limitations

- The method assumes the prior distribution (scaled inverse-chi-squared) is appropriate; severe departures from this assumption (e.g., multimodal variance distributions) may bias hyperparameter estimates.
- When sample size is very small (n < 3 per group), hyperparameter estimation can be unstable; consider using trend=TRUE in eBayes to fit a trend in variance with mean expression.
- B-statistics depend on the specification of log-odds priors for alternative vs. null hypotheses; the default settings may not suit all biological questions.
- The empirical Bayes approach pools variance information across genes; genes with genuinely outlier variances may be over-shrunk toward the common estimate.

## Evidence

- [other] Empirical Bayesian methods provide stable results even when the number of arrays is small: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] eBayes estimates hyperparameters of prior distribution over gene-wise variances for moderated statistics: "Empirical Bayesian methods in limma estimate hyperparameters of the prior distribution over gene-wise variances, enabling computation of moderated t-statistics and B-statistics that remain stable"
- [other] limma applies to microarrays, RNA-seq, and related technologies: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or"
- [other] Limma is an R package for analysis of gene expression data using linear models: "Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments"
