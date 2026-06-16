# Evaluation Strategy

## Direct Checks

- verify that github:bioc__limma repository contains limma R package source code
- verify that the limma package includes functions for empirical Bayes hyperparameter estimation (e.g., eBayes function)
- verify that limma documentation or vignette describes the workflow: lmFit → eBayes → moderated t-statistics and B-statistics generation
- script_runs: execute a reproducible R script that loads a public GEO microarray dataset (e.g., via GEOquery), fits a linear model using lmFit, applies eBayes to estimate empirical Bayes hyperparameters, and outputs moderated t-statistics and B-statistics
- verify that the output table contains required columns: gene identifier, log-fold-change, moderated t-statistic, B-statistic, and adjusted p-value
- verify that B-statistic values are numeric and finite (no NaN or Inf entries)

## Expert Review

- assess whether the estimated prior variance (s2.prior) and degrees of freedom (df.prior) from eBayes are biologically plausible given the input dataset
- assess whether the moderated t-statistics show appropriate stabilization (shrinkage) compared to unmoderated t-statistics, particularly for genes with small sample sizes or high variance
- assess whether the ranking of genes by B-statistic aligns with expected differential expression patterns or with published results from the same GEO dataset (if available)
