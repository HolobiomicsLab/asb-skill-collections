---
name: empirical-bayes-variance-estimation
description: Use when you have a fitted linear model (lmFit object) from microarray or RNA-seq count data and need to compute stable variance estimates and differential expression statistics despite having few biological replicates or small numbers of arrays.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_2269
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

# empirical-bayes-variance-estimation

## Summary

Empirical Bayesian hyperparameter estimation stabilizes gene-wise variance estimates by fitting a prior distribution over variances, enabling computation of moderated t-statistics and B-statistics that remain robust even with small sample sizes in microarray and RNA-seq studies.

## When to use

Apply this skill when you have a fitted linear model (lmFit object) from microarray or RNA-seq count data and need to compute stable variance estimates and differential expression statistics despite having few biological replicates or small numbers of arrays. Use it as a post-hoc step after linear model fitting to borrow information across genes and stabilize per-gene variance estimates before hypothesis testing.

## When NOT to use

- Input expression data has not yet been fitted to a linear model; use lmFit first.
- You require raw, unadjusted per-gene variance estimates without prior regularization; empirical Bayes shrinkage is inappropriate for variance-only inference.
- Sample size is very large (e.g., >100 arrays per group); shrinkage will be minimal and standard t-statistics may be preferable for computational efficiency.

## Inputs

- lmFit object (fitted linear model from limma)
- gene expression matrix (microarray intensity or RNA-seq counts)
- design matrix specifying experimental conditions

## Outputs

- eBayes object containing moderated t-statistics
- B-statistics (log-odds of differential expression)
- adjusted p-values (e.g., Benjamini-Hochberg FDR)
- results table with gene identifiers, log-fold changes, moderated t-statistics, and significance metrics

## How to apply

After fitting a linear model using lmFit on your expression data, apply the eBayes function to estimate hyperparameters (prior mean and degrees of freedom) of a conjugate prior distribution over gene-wise variances. This pooled variance estimate is then used to compute moderated t-statistics by combining the observed gene-specific variance with the prior estimate, weighted by degrees of freedom. The resulting posterior estimates remain stable even when individual genes have few observations. Extract the moderated t-statistics, B-statistics (log-odds of differential expression), and adjusted p-values from the fitted eBayes object. The method is most effective when array numbers are small, as the prior becomes stronger relative to observed variance and shrinkage is more pronounced.

## Related tools

- **limma** (R package providing lmFit for linear model fitting and eBayes for empirical Bayesian variance estimation and moderated t-statistic computation) — https://github.com/bioc/limma
- **R** (Statistical programming environment in which limma functions are executed)

## Examples

```
library(limma); fit <- lmFit(expressionMatrix, designMatrix); efit <- eBayes(fit); results <- topTable(efit, adjust.method='BH', number=Inf)
```

## Evaluation signals

- eBayes object contains non-null s2.prior (prior variance estimate) and df.prior (prior degrees of freedom) fields, indicating successful hyperparameter estimation.
- Moderated t-statistics have smaller magnitudes and larger p-values than ordinary t-statistics due to variance shrinkage, reflecting increased stability.
- B-statistics (log posterior odds) are computed and finite for all genes, with ranking of genes by B-statistic reflecting combined evidence from log-fold change and variance stability.
- Adjusted p-values (e.g., using p.adjust on $p.value column) are monotonically non-decreasing when genes are sorted by significance, meeting FDR control requirements.
- Genes with large log-fold changes but high variance shrink less; genes with small fold changes but low variance shrink more, demonstrating correct weighting by both effect size and reliability.

## Limitations

- Empirical Bayes assumes a common prior distribution across all genes; genes with fundamentally different variance structures may be mis-estimated.
- Method requires at least 2 arrays per group to estimate degrees of freedom; with very few replicates the prior becomes dominated by the marginal distribution and may over-regularize.
- Moderated t-statistics and B-statistics are less interpretable than classical t-statistics when the prior assumptions are violated (e.g., heavy-tailed or multi-modal variance distributions).
- eBayes does not account for gene-specific technical covariates (e.g., GC content, transcript length) that may affect variance; separate variance modeling may be needed for such structured heterogeneity.

## Evidence

- [other] Empirical Bayesian methods in limma estimate hyperparameters of the prior distribution over gene-wise variances, enabling computation of moderated t-statistics and B-statistics that remain stable even with small numbers of arrays.: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] Moderated t-statistics and B-statistics are extracted from the eBayes fitted object.: "Extract moderated t-statistics and B-statistics (log-odds of differential expression) from the fitted eBayes object."
- [other] The linear model and differential expression functions apply to microarrays, quantitative PCR, RNA-seq and proteomics.: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or"
- [other] Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments.: "Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments"
- [other] A results table is generated containing gene identifiers, log-fold changes, moderated t-statistics, adjusted p-values, and B-statistics, sorted by significance.: "Generate a results table containing gene identifiers, log-fold changes, moderated t-statistics, adjusted p-values, and B-statistics, sorted by significance."
