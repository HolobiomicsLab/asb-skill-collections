---
name: coefficient-and-standard-error-interpretation
description: Use when after fitting a linear model to expression data using limma's lmFit function on a design matrix encoding experimental groups, inspect the resulting MArrayLM object to retrieve coefficient estimates (log-fold-changes) and standard errors needed to assess which genes show meaningful.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3672
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

# coefficient-and-standard-error-interpretation

## Summary

Extracting and validating linear model coefficient estimates and residual standard errors from microarray or RNA-seq differential expression analyses to quantify effect sizes and measurement precision. These values form the foundation for downstream statistical testing and fold-change interpretation.

## When to use

After fitting a linear model to expression data using limma's lmFit function on a design matrix encoding experimental groups, inspect the resulting MArrayLM object to retrieve coefficient estimates (log-fold-changes) and standard errors needed to assess which genes show meaningful differential expression and with what confidence.

## When NOT to use

- If the design matrix is misspecified or does not correctly encode the experimental groups of interest—coefficient estimates will be uninterpretable.
- If expression data have not been normalized and background-corrected—standard errors will reflect technical noise rather than biological variability.
- If interpreting coefficients from a single replicate per group—empirical Bayes moderation cannot stabilize estimates without multiple replicates to estimate the prior variance.

## Inputs

- expression matrix (microarray or RNA-seq log₂ intensity/counts)
- design matrix (encoding experimental groups/conditions)
- MArrayLM object (output from lmFit)

## Outputs

- coefficient estimates (log₂ fold-changes per contrast)
- standard errors (residual standard deviations per gene)
- moderated t-statistics (after eBayes)
- posterior probability estimates

## How to apply

Apply limma's lmFit function to an expression matrix and design matrix, then extract the coefficients (log₂ fold-changes between groups) and standard errors (stdev_unscaled and sigma estimates) from the returned MArrayLM object. The standard errors quantify the precision of each coefficient estimate; smaller standard errors indicate more stable effect size estimates, particularly important when analyzing microarray experiments with few biological replicates. Use empirical Bayes moderation (eBayes function) to stabilize standard errors across genes by borrowing information from the empirical variance distribution, especially when sample size is limited. Verify that coefficient estimates align with your contrast matrix and that standard errors are positive and non-zero.

## Related tools

- **limma** (Performs linear model fitting and empirical Bayes moderation to compute and stabilize coefficient estimates and standard errors across genes) — https://github.com/bioc/limma
- **R** (Host language for limma; used to load data, construct design matrix, execute lmFit and eBayes, and extract/inspect coefficient and standard error tables)

## Examples

```
library(limma); fit <- lmFit(expr_matrix, design); fit <- eBayes(fit); coef_table <- data.frame(Coefficient=fit$coefficients[,1], StdError=fit$stdev.unscaled[,1]*fit$sigma)
```

## Evaluation signals

- MArrayLM object contains non-null coefficients and stdev.unscaled fields with dimensions matching the contrast matrix and number of genes
- Standard errors are positive, finite, and non-zero for all genes; no NaN or Inf values
- After eBayes moderation, posterior variance and moderated t-statistics are present and monotonically stabilized relative to unmoderated t-statistics
- Coefficient estimates and standard errors show expected directionality and magnitude relative to the experimental design (e.g., upregulated genes have positive log-fold-change coefficients in the expected direction)
- Coefficients and standard errors remain consistent across replicate analyses, indicating reproducibility and absence of random fitting failures

## Limitations

- Empirical Bayes moderation is most effective with multiple replicates per group; single-replicate designs lack the variance information needed to stabilize standard errors.
- Linear model assumptions (homoscedasticity, independence, normality of residuals) must hold; severe outliers or batch effects can inflate standard errors and mask true effects.
- Standard errors quantify uncertainty in the point estimate but do not capture systematic bias from model misspecification, unmeasured confounders, or hidden batch effects.
- Coefficients and standard errors are scale-dependent: for log₂ transformed data they represent log₂ fold-changes; for untransformed counts they reflect linear scale differences, requiring careful interpretation.

## Evidence

- [other] Empirical Bayesian methods provide stable results even when the number of arrays is small: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] lmFit produces coefficient estimates and residual standard errors encoded in MArrayLM object: "Apply limma's lmFit function to fit a linear model to the expression matrix using the design matrix, obtaining coefficient estimates and residual standard errors."
- [other] Linear models apply across multiple expression technologies for assessing differential expression: "the use of linear models for analysing designed experiments and the assessment of differential expression"
