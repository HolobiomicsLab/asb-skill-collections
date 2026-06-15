---
name: moderated-t-statistic-computation
description: Use when you have a fitted linear model (lmFit object) from microarray, RNA-seq, qPCR, or proteomics data and need to test for differential expression across genes while maintaining statistical stability despite having few biological replicates or arrays.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
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

# moderated-t-statistic-computation

## Summary

Compute moderated t-statistics and B-statistics for differential expression by applying empirical Bayes hyperparameter estimation to stabilize gene-wise variance estimates. This skill is essential when analyzing gene expression data with small sample sizes, where ordinary t-statistics are unstable.

## When to use

Apply this skill when you have a fitted linear model (lmFit object) from microarray, RNA-seq, qPCR, or proteomics data and need to test for differential expression across genes while maintaining statistical stability despite having few biological replicates or arrays. Use it especially when sample size is small and you need both moderated t-statistics (for hypothesis testing) and B-statistics (log-odds of differential expression).

## When NOT to use

- Input expression data has not been normalized or background-corrected; apply normalization first.
- Sample size is very large (>100 arrays/samples); empirical Bayes borrowing of strength provides minimal benefit and ordinary t-statistics may suffice.
- You need raw p-values rather than adjusted p-values; moderated statistics inherently involve multiple-testing adjustment through the prior.

## Inputs

- lmFit object (fitted linear model with gene-wise variance estimates)
- design matrix (experimental design specification)
- expression matrix (normalized gene expression data, any technology: microarray, RNA-seq, qPCR, proteomics)

## Outputs

- eBayes object (containing moderated t-statistics, B-statistics, posterior variance estimates)
- results table (gene identifiers, log-fold changes, moderated t-statistics, adjusted p-values, B-statistics)

## How to apply

Begin with a pre-fitted lmFit object containing gene-wise variance estimates from your experimental design. Apply the eBayes function to estimate hyperparameters of the prior distribution over gene-wise variances using empirical Bayes methods; this shrinks individual gene variances toward a common distribution, stabilizing variance estimates across genes. Extract the moderated t-statistics and B-statistics from the resulting eBayes object. Generate a results table sorted by significance (adjusted p-value or B-statistic) containing gene identifiers, log-fold changes, moderated t-statistics, adjusted p-values, and B-statistics. The moderated variances replace the ordinary gene-wise variances in the t-statistic denominator, preventing inflated test statistics from genes with accidentally small sample variances.

## Related tools

- **limma** (R package providing eBayes function for empirical Bayes hyperparameter estimation, lmFit for linear model fitting, and functions to extract and organize moderated t-statistics and B-statistics) — https://github.com/bioconductor/limma
- **R** (Programming environment in which limma functions are executed)

## Examples

```
fit <- lmFit(eset, design); efit <- eBayes(fit); results <- topTable(efit, adjust.method='BH', number=Inf)
```

## Evaluation signals

- Moderated t-statistics have smaller magnitude than ordinary t-statistics (variance shrinkage toward prior mean), especially for genes with low variance estimates.
- Posterior variance estimates (from eBayes) are all positive and bounded (no genes have inflated or zero variances).
- B-statistics (log-odds) and adjusted p-values are concordant: genes with high B-statistics have low adjusted p-values and vice versa.
- Results table is sorted by significance metric (e.g., adjusted p-value < 0.05 or B-statistic > 0) and contains no missing values in moderated t-statistics or B-statistics columns.
- Number of genes with adjusted p-value < 0.05 is smaller than the number of genes with unadjusted p-value < 0.05 (evidence of multiple-testing correction inherent in B-statistics).

## Limitations

- Empirical Bayes estimation assumes a common prior distribution over gene-wise variances; genes with highly atypical variances may not be well-represented by this prior.
- Performance relies on having enough genes (typically hundreds) to estimate hyperparameters reliably; transcriptome studies generally satisfy this, but targeted panels may not.
- The method does not account for gene-level batch effects or hidden confounders; these must be addressed in the design matrix or prior normalization steps.
- B-statistics are log-odds and their absolute magnitude is sensitive to the prior variance of the log-fold-change distribution; interpretation requires domain knowledge of expected effect sizes.

## Evidence

- [other] Empirical Bayesian methods in limma estimate hyperparameters of the prior distribution over gene-wise variances, enabling computation of moderated t-statistics and B-statistics that remain stable even with small numbers of arrays.: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] The linear model and differential expression functions apply to microarrays, quantitative PCR, RNA-seq and proteomics.: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or"
- [other] limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments and assessment of differential expression.: "Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments"
