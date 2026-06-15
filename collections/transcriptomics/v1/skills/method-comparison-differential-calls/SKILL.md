---
name: method-comparison-differential-calls
description: 'Use when you have applied two or more competing analysis workflows to the same RNA-seq or microarray dataset and need to assess whether they yield consistent or divergent differential expression results. Typical triggers: (1) comparing a new normalization method (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3308
  tools:
  - edgeR
  - limma
  - R
  - voom
derived_from:
- doi: 10.1186/gb-2014-15-2-r29
  title: limmavoom
- doi: 10.1093/nar/gkv007
  title: ''
evidence_spans:
- calcNormFactors [TMM normalization]
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments
- Limma is an R package for the analysis of gene expression data, especially the use of linear models for analysing designed experiments and the assessment of differential expression
- Limma is an R package for the analysis of gene expression data
- Limma is an R package
- 'Voom: precision weights unlock linear model analysis tools for RNA-seq read counts'
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

# method-comparison-differential-calls

## Summary

Compare ranked lists of differentially expressed genes across two analysis pipelines (e.g., TMM-normalized voom versus limma-only, or different normalization strategies) to quantify how methodological choices affect differential expression calls, gene rankings, and statistical significance. This skill is essential when evaluating whether upstream normalization or preprocessing steps meaningfully alter downstream biological conclusions.

## When to use

You have applied two or more competing analysis workflows to the same RNA-seq or microarray dataset and need to assess whether they yield consistent or divergent differential expression results. Typical triggers: (1) comparing a new normalization method (e.g., edgeR's calcNormFactors + TMM) against a baseline (e.g., limma-only); (2) evaluating the effect of precision-weight estimation (voom) on gene rankings; (3) validating that an optimization step (e.g., empirical Bayes moderation) does not inadvertently change biological conclusions. Apply this skill when reproducibility and method justification are critical for publication or when the choice of normalization or statistical framework is under debate.

## When NOT to use

- You are comparing methods on fundamentally different datasets or different sample cohorts—concordance metrics will conflate biological differences with methodological ones. Use only when the same input samples, phenotypes, and design are held constant across pipelines.
- You have not yet fit linear models or applied statistical testing to either pipeline. This skill assumes lmFit + eBayes have been completed; if you are still in the normalization or QC stage, defer comparison until both pipelines reach topTable output.
- The two methods are designed for different assay types (e.g., one optimized for microarrays, one for RNA-seq). While limma functions apply to both, you should justify and document such cross-platform comparisons explicitly rather than assuming concordance metrics are directly interpretable.

## Inputs

- Two or more fitted lmFit model objects from parallel pipelines (e.g., voom + TMM vs. limma baseline)
- Design matrices used in each pipeline (may be identical or differ)
- Count or expression matrices pre-processed by each method
- Sample metadata and experimental design specification

## Outputs

- Comparison tables: gene IDs, log-fold-changes, p-values, adjusted p-values (FDR), moderated t-statistics from each pipeline side-by-side
- Overlap/concordance metrics: set intersection, Jaccard index, rank correlation (Spearman/Kendall), percentage of top-N genes in common
- Ranked gene lists (topTable output) from each pipeline with consistent threshold (e.g., FDR < 0.05)
- Visualization: scatter plots of log-fold-changes and p-values across methods, Venn diagrams of significant gene sets, rank-correlation plots
- Summary statistics: number of genes called significant in each method, number switching significance status, median/mean rank shifts

## How to apply

Fit separate linear models using lmFit on each pipeline's pre-processed expression matrix (e.g., one with voom-transformed counts after TMM normalization, one with raw or alternatively normalized counts). Apply empirical Bayes moderation via eBayes to stabilize variance estimates in each model independently. Extract top differentially expressed genes from each model using topTable with an identical adjusted p-value threshold (e.g., FDR < 0.05) and log-fold-change cutoff. Then systematically compare: (1) the overlap in gene sets called as significant between pipelines (e.g., via Venn diagram or Jaccard index); (2) ranking differences for genes appearing in both lists (rank correlation, Spearman or Kendall's τ); (3) effect size discrepancies (log-fold-change scatter plot, correlation, and range); (4) p-value distributions and moderated t-statistic magnitudes. Document which genes switch significance status and by how much, and identify whether differences are systematic (e.g., consistently larger LFCs in one method) or stochastic. Use absolute agreement metrics (e.g., percentage of top-N genes in common) and rank-based metrics (e.g., Rank-Biased Overlap) to quantify concordance.

## Related tools

- **limma** (Fits linear models (lmFit) and applies empirical Bayes moderation (eBayes) for each pipeline; extracts ranked gene lists (topTable) for comparison) — https://github.com/bioc/limma
- **edgeR** (Computes library-size normalization factors (calcNormFactors with TMM method) to be passed to voom for one pipeline variant)
- **voom** (Transforms read counts and computes precision weights accounting for mean-variance relationship using TMM-normalized library sizes; output fed to lmFit)
- **R** (Programming environment in which limma, edgeR, voom, and comparison visualizations (ggplot2, base graphics) are executed)

## Examples

```
# Fit two pipelines and compare
library(limma); library(edgeR)
# Pipeline 1: TMM-voom
dge <- DGEList(counts=raw_counts); dge <- calcNormFactors(dge, method='TMM')
v <- voom(dge, design); fit1 <- lmFit(v, design); fit1 <- eBayes(fit1); top1 <- topTable(fit1, adjust.method='BH', p.value=0.05, number=Inf)
# Pipeline 2: limma-only
fit2 <- lmFit(raw_counts, design); fit2 <- eBayes(fit2); top2 <- topTable(fit2, adjust.method='BH', p.value=0.05, number=Inf)
# Compare
cor(top1$logFC[match(rownames(top2), rownames(top1))], top2$logFC, use='complete.obs', method='spearman')
```

## Evaluation signals

- Rank correlation (Spearman or Kendall's τ) of log-fold-changes across the top 500–1000 significant genes should be ≥ 0.85 if methods are concordant; values < 0.70 suggest substantial disagreement and warrant investigation.
- Percentage of top-N genes (e.g., top 100, top 500) appearing in both pipelines should be reported; >70% overlap is typical for closely related methods; <50% suggests methodological differences are substantial.
- Scatter plot of log-fold-changes from each pipeline should cluster tightly around the diagonal; systematic offset or slope changes indicate bias (e.g., voom+TMM producing uniformly higher or lower effect sizes).
- Distribution of adjusted p-values (FDR) and number of genes reaching significance at a fixed threshold (e.g., FDR < 0.05) must be reported for each pipeline; if one method calls >2× as many genes significant, examine whether this reflects true power gain or inflated false-discovery rate.
- Genes that switch significance status (e.g., significant in one pipeline but not the other) should be examined for biological plausibility and checked for confounding factors (e.g., low counts, extreme library sizes, or high dispersion); if systematic, this indicates the pipelines are making different statistical assumptions.

## Limitations

- Empirical Bayes moderation stabilizes variance estimates even with small sample sizes, but comparison outcomes depend critically on study design balance and sufficient replication; underpowered studies may show large differences even if methods are sound.
- Linear model and differential expression functions apply to microarrays, quantitative PCR, RNA-seq, and proteomics, but each assay type may have technology-specific biases (e.g., microarray background effects, RNA-seq GC content bias); comparisons across technologies are not supported by this article.
- TMM normalization and voom precision weights assume that the majority of genes are not differentially expressed and that the mean-variance relationship follows a specific functional form; violations (e.g., in highly perturbed systems or when many genes are DE) may cause concordance metrics to misrepresent method validity.
- Comparison metrics (overlap, rank correlation) are sensitive to the choice of significance threshold and gene filtering criteria; results may not generalize if thresholds are changed post-hoc or if filters (e.g., minimum count cutoffs) differ between pipelines.

## Evidence

- [other] Compare gene rankings, log-fold-changes, and adjusted p-values between the TMM-voom pipeline and limma-only baseline to quantify changes in differential expression calls.: "Compare gene rankings, log-fold-changes, and adjusted p-values between the TMM-voom pipeline and limma-only baseline to quantify changes in differential expression calls."
- [other] Fit a linear model using lmFit on the voom-transformed expression matrix with the design matrix. Apply empirical Bayes moderation using eBayes to stabilize variance estimates across genes.: "Fit a linear model using lmFit on the voom-transformed expression matrix with the design matrix. Apply empirical Bayes moderation using eBayes to stabilize variance estimates across genes."
- [other] Empirical Bayesian methods are used to provide stable results even when the number of arrays is small.: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays, quantitative PCR, RNA-seq or proteomics"
