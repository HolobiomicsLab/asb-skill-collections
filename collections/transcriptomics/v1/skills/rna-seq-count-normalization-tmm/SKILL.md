---
name: rna-seq-count-normalization-tmm
description: Use when apply TMM normalization when you have raw RNA-seq read counts from multiple samples and suspect differences in library composition (e.g., one sample over-represents a highly-expressed gene or transcript class relative to others).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
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

# RNA-seq count normalization using Trimmed Mean of M-values (TMM)

## Summary

TMM normalization computes scale factors that account for RNA composition bias in RNA-seq count data, enabling fair comparison of gene expression across samples with different sequencing depths and transcript abundance distributions. This normalization is typically applied via edgeR's calcNormFactors before downstream differential expression analysis with limma-voom or other methods.

## When to use

Apply TMM normalization when you have raw RNA-seq read counts from multiple samples and suspect differences in library composition (e.g., one sample over-represents a highly-expressed gene or transcript class relative to others). This is especially critical before combining normalization with limma's voom precision-weighting, where composition bias can distort the mean-variance relationship and downstream fold-change rankings.

## When NOT to use

- Input counts are already normalized (e.g., already log2-transformed CPM, RPKM, or TPM); re-normalizing will distort the scale.
- Library sizes differ negligibly across samples (< 10% variation); composition bias is likely minimal, and TMM may introduce noise rather than correct bias.
- Sample groups have fundamentally different transcript repertoires (e.g., tissue-specific isoforms); TMM's assumption of a set of unchanged genes may be violated, yielding misleading scale factors.

## Inputs

- Raw RNA-seq read counts (genes × samples matrix, e.g., integer counts from featureCounts or HTSeq)
- Sample metadata and experimental design matrix
- Reference genome annotation (optional, for QC)

## Outputs

- DGEList object with TMM-normalized library sizes and scale factors
- Precision weights from voom reflecting the mean-variance relationship of normalized counts
- Fitted linear model coefficients and residuals
- Moderated t-statistics and adjusted p-values for each gene
- Ranked list of differentially expressed genes with log-fold-changes

## How to apply

Load raw RNA-seq read counts into a DGEList object in edgeR and apply calcNormFactors with the TMM method to compute normalization scale factors that adjust for library-size differences and RNA composition effects. TMM identifies a set of genes assumed to be unchanged between samples, then computes a weighted average of log-fold-changes on these genes to derive per-sample scale factors. These factors are then used to rescale library sizes; the rescaled sizes are passed to voom (along with the design matrix) to compute precision weights that model the mean-variance relationship of the normalized data. The precision-weighted expression matrix is then fitted with lmFit, followed by empirical Bayes moderation (eBayes) and statistical testing. Compare resulting log-fold-changes and adjusted p-values (e.g., FDR < 0.05) against a limma-only baseline to assess the impact of composition normalization on differential expression calls.

## Related tools

- **edgeR** (Computes TMM normalization factors via calcNormFactors and creates DGEList objects to store count matrices and per-sample scale factors)
- **limma** (Applies voom to generate precision weights from normalized library sizes and mean-variance estimates; fits linear models with lmFit; applies empirical Bayes shrinkage with eBayes) — https://github.com/bioc/limma
- **voom** (Transforms TMM-normalized counts to log2-CPM scale with precision weights that account for mean-variance relationship, enabling linear modeling on normalized RNA-seq data)
- **R** (Execution environment for edgeR and limma workflows)

## Examples

```
library(edgeR); dge <- DGEList(counts=raw_counts, group=sample_groups); dge <- calcNormFactors(dge, method='TMM'); v <- voom(dge, design=design_matrix); fit <- lmFit(v, design_matrix); fit <- eBayes(fit); topTable(fit, coef=2, adjust.method='BH', n=100)
```

## Evaluation signals

- TMM scale factors are close to 1.0 for most samples (indicating minimal composition bias) or systematically > or < 1.0 for biased samples; verify they span a reasonable range (typically 0.5–2.0).
- Precision weights from voom increase with mean expression level (reflecting the mean-variance relationship), with no negative weights and reasonable dynamic range.
- Ranked list of differentially expressed genes shows consistent effect sizes (log-fold-changes) and p-value distributions when compared to a limma-only baseline; genes with strong biological signal should rank similarly in both pipelines.
- Adjusted p-values (FDR) are well-calibrated; the number of significant genes at a threshold (e.g., FDR < 0.05) should be reproducible across technical replicates and stable under reasonable parameter perturbations.
- Linear model residuals (from lmFit) show no obvious systematic trends with fitted values or with TMM scale factors, indicating that composition bias has been adequately corrected.

## Limitations

- TMM assumes that most genes are not differentially expressed between samples; if a large proportion of the genome is DE, scale factors may be biased and should be validated with alternative methods (e.g., DESeq2's median-of-ratios).
- TMM does not account for technical biases unrelated to composition (e.g., batch effects, GC content bias); these must be detected and corrected separately (e.g., via limma's removeBatchEffect or explicit batch terms in the design matrix).
- Small sample sizes (n < 3 per group) can lead to unstable empirical Bayes variance estimates in limma; consider using robust methods or informative priors if sample numbers are very limited.
- TMM scale factors are computed only from genes with adequate counts; genes with very low or zero counts across all samples are excluded from the calculation and may not benefit equally from normalization.

## Evidence

- [other] Empirical Bayesian methods are used to provide stable results even when the number of arrays is small.: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] Linear model and differential expression functions apply to microarrays, quantitative PCR, RNA-seq and proteomics: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or"
- [other] Normalization and background correction are provided for microarrays and related technologies: "The normalization and background correction functions are provided for microarrays and similar technologies."
- [other] TMM normalization factors and voom precision weights are computed and passed to linear model fitting: "Create a DGEList object in edgeR and apply calcNormFactors with TMM method to compute normalization factors and scale library sizes. ... Extract the TMM-normalized library sizes and pass them to voom"
- [other] Linear model fitting with empirical Bayes moderation stabilizes variance estimates for differential expression: "Fit a linear model using lmFit on the voom-transformed expression matrix with the design matrix. Apply empirical Bayes moderation using eBayes to stabilize variance estimates across genes."
