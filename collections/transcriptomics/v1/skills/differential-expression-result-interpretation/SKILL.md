---
name: differential-expression-result-interpretation
description: Use when you have fitted a linear model to gene expression data (microarray, RNA-seq, qPCR, or proteomics) across multiple samples and need to compute gene-level test statistics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0625
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

# differential-expression-result-interpretation

## Summary

Empirical Bayesian shrinkage of gene-wise variance estimates to compute moderated t-statistics and B-statistics that remain stable even with small sample sizes, enabling robust ranking and significance assessment of differential expression. This skill applies posterior inference to stabilize variance estimates across the genome before hypothesis testing.

## When to use

You have fitted a linear model to gene expression data (microarray, RNA-seq, qPCR, or proteomics) across multiple samples and need to compute gene-level test statistics. Use this skill when: (1) your sample size is small (fewer than ~10 arrays per group), making ordinary t-statistics unstable; (2) you need both point estimates of fold-change and probabilistic rankings (log-odds) of differential expression; or (3) you are comparing across many genes and want variance estimates borrowed from the genome-wide distribution rather than estimated independently per gene.

## When NOT to use

- Input is a pre-computed results table from another DE tool (e.g., DESeq2, edgeR) — use this skill only on raw fitted model objects.
- Sample size is very large (>100 arrays per group) — empirical Bayes shrinkage provides negligible benefit and ordinary t-statistics are already stable.
- You have no replicate samples within groups — variance cannot be estimated and eBayes will fail.

## Inputs

- lmFit object (fitted linear model from limma)
- gene expression matrix (rows=genes, columns=samples; microarray intensities, RNA-seq counts, or normalized log-scale data)

## Outputs

- eBayes-fitted object containing moderated t-statistics and B-statistics per gene
- results table with gene identifiers, log-fold changes, moderated t-statistics, adjusted p-values, and B-statistics
- ranked gene list (by B-statistic or adjusted p-value)

## How to apply

After fitting a linear model with lmFit, apply empirical Bayes hyperparameter estimation via eBayes to fit a prior distribution over gene-wise variances. This step shrinks each gene's variance estimate toward the genome-wide mean, stabilizing the posterior variance. Extract the resulting moderated t-statistics (which use the shrunk variance in the denominator) and B-statistics (log-odds of differential expression under the empirical Bayes posterior). The moderated statistics are more stable and have better power than ordinary t-statistics, especially with few replicates. Generate a results table ranked by B-statistic (most confident differential expression first) or adjusted p-value, including gene identifiers, log-fold changes, moderated t-statistics, adjusted p-values, and B-statistics. Interpret B-statistics as posterior log-odds: B > 0 favors differential expression, with magnitude indicating confidence.

## Related tools

- **limma** (R package providing lmFit (linear model fitting), eBayes (empirical Bayes hyperparameter estimation), and topTable (results extraction); core tool for this skill) — https://github.com/bioc/limma
- **R** (Statistical computing environment in which limma operates)

## Examples

```
library(limma); fit <- eBayes(fit); results <- topTable(fit, adjust.method='BH', number=Inf); head(results[order(results$B, decreasing=TRUE),])
```

## Evaluation signals

- Moderated variances should be shrunk toward the genome-wide mean: compare gene-wise variance estimates before and after eBayes; shrinkage should be more pronounced for genes with few replicates or high within-group variance.
- B-statistics should exhibit expected ordering: genes ranked by B-statistic should align with biological expectation (e.g., known DE genes ranked first) and should be monotonic with statistical significance when sorted.
- Adjusted p-values (e.g., Benjamini–Hochberg FDR) should reflect the moderated t-statistics: genes with more extreme moderated t-values and smaller B-statistics should have smaller adjusted p-values.
- Results table should be complete: all genes present in the input model should appear in the output; no missing values in log-fold change, moderated t-statistic, adjusted p-value, or B-statistic columns.
- Stability check: re-run eBayes on a subset of genes or with leave-one-out sample removal; moderated statistics should be more stable than ordinary t-statistics, especially for small-sample groups.

## Limitations

- Empirical Bayes assumes a common prior distribution over gene-wise variances; genes with atypical variance structures (e.g., bimodal distributions across groups) may be poorly shrunk.
- B-statistics are on the log-odds scale and require specification of the prior probability of differential expression; limma uses a data-dependent prior that may not reflect your hypothesis.
- Results depend on the quality of the linear model fit: if design matrix is misspecified or confounders are unaccounted for, eBayes will amplify those errors.
- Small sample sizes (e.g., n=2 per group) limit the accuracy of hyperparameter estimation; the empirical Bayes prior may be unstable even after shrinkage.

## Evidence

- [other] Empirical Bayesian hyperparameter estimation for variance stabilization: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] eBayes function computes moderated t-statistics and B-statistics: "Empirical Bayes hyperparameter estimation using limma's eBayes function to fit the prior distribution over gene-wise variances and stabilize variance estimates."
- [other] Results table structure and content: "Generate a results table containing gene identifiers, log-fold changes, moderated t-statistics, adjusted p-values, and B-statistics, sorted by significance."
- [other] Applicability across multiple omics platforms: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or"
- [other] Moderated t-statistics and B-statistics computation rationale: "Empirical Bayes methods in limma estimate hyperparameters of the prior distribution over gene-wise variances, enabling computation of moderated t-statistics and B-statistics that remain stable even"
