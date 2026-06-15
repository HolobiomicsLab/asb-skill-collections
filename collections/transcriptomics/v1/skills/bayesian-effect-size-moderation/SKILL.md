---
name: bayesian-effect-size-moderation
description: Use when after running DESeq2 differential expression analysis and extracting results with raw log fold changes, apply this skill when you observe high variance in effect size estimates across genes—particularly when many genes have small counts, unreliable variance estimates, or when you want.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3308
  tools:
  - DESeq2
  - ashr
  - vicar
  - DEvis
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

# Bayesian Effect Size Moderation

## Summary

Apply empirical Bayes shrinkage to log fold change estimates from RNA-seq differential expression analysis, reducing noise in effect size estimates while preserving genuine signal through adaptive priors. This skill uses DESeq2's lfcShrink() function with multiple estimator types (apeglm, normal, ashr) to moderate fold changes toward zero according to data-driven shrinkage strength.

## When to use

After running DESeq2 differential expression analysis and extracting results with raw log fold changes, apply this skill when you observe high variance in effect size estimates across genes—particularly when many genes have small counts, unreliable variance estimates, or when you want credible intervals in addition to point estimates. Use it to compare shrinkage-based estimates across estimator types (apeglm adaptive t-prior, normal adaptive prior, ashr mixture-of-normals) to assess robustness of effect size inference.

## When NOT to use

- Input is already a shrunken effect size table from another tool (e.g., limma-voom shrinkage, edgeR empirical Bayes)—do not double-shrink.
- You have only a few samples per group or extreme imbalance in group sizes, which may lead to unreliable dispersion estimates that lfcShrink() depends on.
- Your study design includes many covariates and interactions where the mean-variance relationship assumed by DESeq2 may be violated; validate assumptions first.
- You require fixed, pre-specified shrinkage strength rather than data-driven adaptation—lfcShrink() determines shrinkage automatically and does not allow manual tuning of the prior.

## Inputs

- DESeqDataSet with fitted dispersions and GLM coefficients (output from DESeq())
- results object from results() containing raw log fold changes, standard errors, and p-values for a given contrast

## Outputs

- DESeqResults object with shrunken log fold changes (lfcShrink output with type='apeglm')
- DESeqResults object with shrunken log fold changes (lfcShrink output with type='normal')
- DESeqResults object with shrunken log fold changes (lfcShrink output with type='ashr')
- Comparative visualizations (MA-plots, effect size distributions) across estimator types

## How to apply

Begin with a DESeqDataSet on which you have run DESeq() to estimate dispersions and fit the negative binomial GLM. Extract the base results table using results() for your contrast of interest (e.g., treated vs. untreated). Apply lfcShrink() with type='apeglm' to shrink log fold changes using an adaptive t-prior, which provides strong shrinkage for low-information genes while preserving estimates for high-count genes with low dispersion. For comparison, also apply lfcShrink() with type='normal' (the original adaptive normal prior) and type='ashr' (adaptive shrinkage with a mixture of normals fitted using the ashr package). The shrinkage amount is determined automatically from the data by maximum likelihood estimation of the prior, rather than being pre-specified. Compare the three shrunken LFC results using MA-plots and summary statistics (e.g., log2 fold change distributions, proportion of genes with large effect sizes) to assess stability and choose the estimator most appropriate for your downstream inference goals.

## Related tools

- **DESeq2** (Provides lfcShrink() function for Bayesian moderation of log fold changes; generates DESeqResults objects that serve as input to shrinkage estimators.) — https://github.com/thelovelab/DESeq2
- **ashr** (Implements adaptive shrinkage with mixture-of-normals prior; used as type='ashr' estimator within DESeq2's lfcShrink() workflow.) — https://github.com/stephens999/ashr
- **vicar** (Provides related empirical Bayes shrinkage methods (mouthwash, backwash) that use ashr methodology for confounder-adjusted effect size estimation in omics data.) — https://github.com/dcgererd/vicar
- **DEvis** (Offers visualization and aggregation tools for differential expression results, including shrunken effect sizes; useful for comparative MA-plots and effect size distributions across estimator types.) — https://github.com/price0416/DEvis

## Examples

```
res <- results(dds, name='dex_treated_vs_untreated')
res_apeglm <- lfcShrink(dds, coef='dex_treated_vs_untreated', type='apeglm')
res_ashr <- lfcShrink(dds, coef='dex_treated_vs_untreated', type='ashr')
```

## Evaluation signals

- Shrunken log fold changes are substantially smaller in magnitude than raw estimates (especially for low-count genes) while large-effect genes show minimal shrinkage; compare MA-plots before and after lfcShrink().
- Posterior standard errors (stored in the results object) are reduced relative to original standard errors, reflecting gained information from the empirical Bayes prior.
- The three estimator types (apeglm, normal, ashr) produce consistent rankings of effect sizes and broadly similar top differentially expressed genes, indicating robust shrinkage.
- Genes with low normalized counts show greater shrinkage than genes with high counts, consistent with the adaptive nature of the prior fitting the gene-level mean-variance relationship.
- No genes have NA or NaN values in shrunken LFC columns; inspect for numerical warnings or failures in the lfcShrink() output, which may occur if the prior cannot be fitted (e.g., too few genes or extreme coefficient estimates).

## Limitations

- Shrinkage accuracy depends critically on accurate dispersion estimates from DESeq(); pre-filtering very low-count genes (e.g., requiring ≥10 reads in at least smallest group size samples) is recommended to improve dispersion estimation.
- The apeglm and ashr estimators require maximum likelihood fitting of the prior, which may fail or produce unreliable results if the number of genes is very small, the effect size distribution is highly non-unimodal, or there are extreme outliers in the GLM coefficient estimates.
- Shrinkage is symmetric around zero by default (g is unimodal and symmetric), which may not be appropriate if the biological effect size distribution is skewed or multi-modal; ashr offers mode and symmetry parameters to relax this.
- The method assumes independence of log fold changes conditional on the prior, which may not hold if genes have been co-regulated by unmeasured confounders; control for major batch effects and covariates in the DESeq design first.
- lfcShrink() is most reliable for unbiased contrasts (e.g., condition main effects); interaction terms or complex contrast designs may produce less stable shrunken estimates.

## Evidence

- [other] lfcShrink() can be applied with three different shrinkage estimator types (apeglm, normal, ashr) to produce shrunken log fold change estimates from DESeq2 results objects.: "lfcShrink() with type='apeglm' to shrink log fold changes using the adaptive t-prior estimator. 5. Apply lfcShrink() with type='normal' to shrink log fold changes using the original adaptive normal"
- [readme] The ashr package performs adaptive shrinkage by determining shrinkage amount from data rather than pre-specification, and scales shrinkage by measurement precision.: "The "adaptive" nature of the shrinkage is two-fold. First, the appropriate amount of shrinkage is determined from the data, rather than being pre-specified. Second, the amount of shrinkage undergone"
- [other] Shrinkage workflow applies lfcShrink() function to DESeqResults after running DESeq() and extracting results with results().: "Run DESeq() to perform differential expression analysis and estimate dispersions. 3. Extract the base results table using results() for the dex variable (treated vs untreated). 4. Apply lfcShrink()"
- [other] Pre-filtering low-count genes improves performance of subsequent estimation.: "by removing rows in which there are very few reads, we reduce the memory size of the `dds` data object, and we increase the speed"
- [readme] The ashr methodology uses empirical Bayes with hierarchical modeling to estimate a unimodal prior from observed effect size estimates and standard errors.: "we assume that the true $\beta_j$ values are independent and identically distributed from some unimodal distribution $g$. By default we assume $g$ is unimodal about zero and symmetric. You can"
