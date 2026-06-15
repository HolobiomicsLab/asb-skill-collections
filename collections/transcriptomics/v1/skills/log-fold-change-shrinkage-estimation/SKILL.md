---
name: log-fold-change-shrinkage-estimation
description: Use when after running DESeq() and extracting base results with results(), apply shrinkage when you have differential expression estimates and want to reduce the variance of log fold change estimates while preserving signal.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - ashr
  - airway
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

# log-fold-change-shrinkage-estimation

## Summary

Apply empirical Bayes shrinkage to log fold change estimates from RNA-seq differential expression analysis using DESeq2's lfcShrink() function with multiple estimator types (apeglm, normal, ashr). Shrinkage reduces noise in fold change estimates, particularly for genes with high dispersion or low counts, improving interpretability and reducing false positives.

## When to use

After running DESeq() and extracting base results with results(), apply shrinkage when you have differential expression estimates and want to reduce the variance of log fold change estimates while preserving signal. This is especially important for RNA-seq count data where estimates for lowly-expressed genes or genes with high biological variability are unreliable without borrowing strength across the genome.

## When NOT to use

- Input count matrix has not yet been normalized and dispersion-estimated via DESeq(); run DESeq() first.
- You require unshrunk log fold changes for variance component estimation or method benchmarking; use the base results() output instead.
- Sample size is very small (n < 3 per group); shrinkage priors may over-regularize and mask real effects.

## Inputs

- DESeqDataSet object (with design matrix and dispersions estimated from DESeq())
- results object from results() function containing base log fold changes and standard errors

## Outputs

- DESeqResults object with shrunken log2FoldChange estimates
- comparison of shrinkage results across estimator types (apeglm, normal, ashr)

## How to apply

Extract the base results table from a DESeqDataSet using results() for your contrast of interest. Then apply lfcShrink() by specifying the DESeqDataSet object, the coefficient name (e.g., 'dex' for treated-vs-untreated), and the shrinkage estimator type: type='apeglm' for the adaptive t-prior (recommended for speed and accuracy), type='normal' for the original adaptive normal prior, or type='ashr' for the adaptive shrinkage estimator with mixture of normals (more flexible but computationally slower). The function returns a results object with shrunken log fold changes in the log2FoldChange column. Choose the estimator based on your data characteristics: apeglm works well for most RNA-seq studies, normal provides classical Bayesian regularization, and ashr offers maximum flexibility for non-normal effect distributions. Compare MA-plots and summary statistics across estimator types to evaluate shrinkage strength and choose the most appropriate for downstream interpretation.

## Related tools

- **DESeq2** (Core package providing DESeqDataSet class, DESeq() normalization/dispersion estimation, results() extraction, and lfcShrink() function for shrinkage) — https://github.com/thelovelab/DESeq2
- **ashr** (Provides adaptive shrinkage estimator (type='ashr' option in lfcShrink); implements mixture-of-normals shrinkage with adaptive prior learning from data) — https://github.com/stephens999/ashr
- **airway** (Example SummarizedExperiment dataset used to demonstrate lfcShrink() workflow on treated-vs-untreated contrast)

## Examples

```
res <- lfcShrink(dds, coef='dex', type='apeglm'); resNorm <- lfcShrink(dds, coef='dex', type='normal'); resAshr <- lfcShrink(dds, coef='dex', type='ashr')
```

## Evaluation signals

- Shrunken log2FoldChange values are closer to zero than base estimates (particularly for lowly-expressed or high-variance genes), reflecting appropriate regularization.
- MA-plots show reduced scatter in fold changes for genes with low mean normalized count, without systematic bias toward zero for strongly-expressed, high-signal genes.
- Summary statistics (e.g., histogram of shrunken vs. unshrunken LFC) demonstrate that the three estimator types (apeglm, normal, ashr) produce quantitatively similar results for well-behaved data, with minor differences reflecting prior flexibility.
- Results object contains valid numeric shrunken log2FoldChange column with no NaN or Inf values (after filtering for sufficient coverage).
- Downstream false discovery rate control (via padj) should improve relative to unshrunk results because shrinkage reduces the variance of test statistics.

## Limitations

- Shrinkage assumes a unimodal prior on true log fold changes; if the true effect distribution is multimodal or heavily skewed, ashr may fit better than normal or apeglm.
- apeglm type requires specification of a one-parameter family (default is 'betaprior'); misspecification can lead to suboptimal shrinkage.
- ashr can be computationally expensive for large numbers of genes (>30,000); apeglm is recommended for routine RNA-seq analysis.
- Shrinkage strength depends on the global distribution of effect sizes across the genome; datasets with few strongly-expressed genes or atypical dispersion patterns may require manual prior tuning.

## Evidence

- [other] Shrinkage reduces noise in fold change estimates: "lfcShrink() can be applied with three different shrinkage estimator types (apeglm, normal, ashr) to produce shrunken log fold change estimates from DESeq2 results objects."
- [other] Workflow requires DESeq and results extraction before shrinkage: "Run DESeq() to perform differential expression analysis and estimate dispersions. 3. Extract the base results table using results() for the dex variable (treated vs untreated). 4. Apply lfcShrink()"
- [other] Three distinct estimator types with different properties: "Apply lfcShrink() with type='apeglm' to shrink log fold changes using the adaptive t-prior estimator. 5. Apply lfcShrink() with type='normal' to shrink log fold changes using the original adaptive"
- [readme] ashr implements adaptive shrinkage with mixture of normals: "The ashr ('Adaptive SHrinkage') package aims to provide simple, generic, and flexible methods to derive 'shrinkage-based' estimates and credible intervals for unknown quantities"
- [readme] Shrinkage strength depends on measurement precision: "the amount of shrinkage undergone by each $\hat\beta_j$ will depend on the standard error $s_j$: measurements with high standard error will undergo more shrinkage than measurements with low standard"
