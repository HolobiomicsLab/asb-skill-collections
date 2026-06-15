---
name: precision-weight-calculation-rna-seq
description: Use when you have raw RNA-seq read counts and a set of normalization factors (e.g., TMM-computed library size scales from edgeR's calcNormFactors), and you plan to fit a linear model to detect differential expression.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3308
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

# precision-weight-calculation-rna-seq

## Summary

Compute precision weights for RNA-seq count data that model the mean-variance relationship and stabilize variance estimates across genes before linear model fitting. This skill bridges normalization (e.g., TMM scaling factors) and differential expression modeling by transforming raw counts to a log-scale metric suitable for least-squares regression.

## When to use

Apply this skill when you have raw RNA-seq read counts and a set of normalization factors (e.g., TMM-computed library size scales from edgeR's calcNormFactors), and you plan to fit a linear model to detect differential expression. The skill is essential when sample sizes are small or when mean-variance trends are pronounced and could bias downstream statistical inference.

## When NOT to use

- Input counts are already log-transformed or normalized to a continuous scale (e.g., already CPM, TPM, or Affymetrix-processed expression values); voom is designed for raw count-level data.
- Sample sizes are very large (n > 100 per group); precision weights become less critical because empirical Bayes shrinkage is stable with abundant degrees of freedom.
- Analysis goal is gene-set or pathway enrichment rather than per-gene differential expression ranking; precision weighting does not materially change the set of significant pathways.

## Inputs

- raw RNA-seq read count matrix (genes × samples)
- sample metadata (phenotype, group assignment)
- design matrix (samples × contrasts)
- normalization factors (e.g., TMM library size scales from edgeR::calcNormFactors)

## Outputs

- voom object containing log2-transformed count matrix
- precision weight matrix (genes × samples)
- fitted mean-variance curve parameters

## How to apply

Load the raw count matrix, sample metadata, and design matrix into limma's voom function along with the pre-computed normalization factors (e.g., TMM library sizes extracted from a DGEList object). voom applies a log2 transformation (with a small pseudocount offset to stabilize low counts), fits a loess curve to the mean-variance relationship across genes, and computes precision weights (inverse variances) for each gene-sample pair. These weights are stored alongside the log-transformed expression matrix and passed directly to lmFit. The precision weights downweight genes with high within-group variance and upweight stable genes, improving the robustness of empirical Bayes variance moderation in eBayes.

## Related tools

- **limma** (provides voom function to compute precision weights from raw counts and mean-variance trend) — https://github.com/bioconductor/limma
- **edgeR** (computes normalization factors (e.g., TMM) that are passed to voom as offsets) — https://github.com/bioconductor/edgeR
- **R** (runtime environment for limma and edgeR workflows)

## Examples

```
v <- voom(dge, design, lib.size = dge$samples$lib.size * dge$samples$norm.factors); fit <- lmFit(v, design); efit <- eBayes(fit); topTable(efit, adjust.method = 'BH', p.value = 0.05)
```

## Evaluation signals

- voom output object contains non-zero, positive precision weights for all genes; weights should be ≥ 0 and typically in range [0.1, 10] on log scale.
- Mean-variance trend is visually smooth and monotonic (decreasing weight with increasing mean log-count); inspect plot(voom_object) for deviations or outliers.
- Linear model fits from lmFit on voom-transformed data with weights produce lower residual variances and narrower confidence intervals than unweighted fits on the same data.
- Empirical Bayes moderation (eBayes) applied after lmFit yields stable posterior variance estimates (df.posterior > 1) and adjusted p-values that rank genes consistently with known positive controls.
- Precision weights reduce the influence of high-variance genes in topTable rankings; compare gene rankings before/after voom to confirm down-ranking of noisy genes.

## Limitations

- voom assumes counts follow a Poisson or negative-binomial distribution; heavily zero-inflated or over-dispersed data may not be well modeled by the fitted trend.
- The method is sensitive to outlier samples or genes with extreme mean-variance behavior; genes with zero counts in many samples may distort the loess fit.
- Small library sizes or imbalanced experimental designs can inflate variance estimates; precision weights are most reliable when samples are similarly sequenced and biological replication is adequate (≥3 per group).
- voom does not explicitly model gene-level technical effects (e.g., GC content bias); pre-filtering low-abundance genes (e.g., <1 CPM in ≥n samples) is recommended to reduce noise.

## Evidence

- [other] voom applies a loess curve to mean-variance relationship and computes precision weights: "Extract the TMM-normalized library sizes and pass them to voom along with the design matrix to compute precision weights accounting for mean-variance relationship."
- [other] voom weights are passed to lmFit for linear model fitting: "Fit a linear model using lmFit on the voom-transformed expression matrix with the design matrix."
- [other] Empirical Bayesian methods stabilize variance estimates with small sample sizes: "Empirical Bayesian methods are used to provide stable results even when the number of arrays is small."
- [other] Linear models apply across RNA-seq and microarray technologies: "The linear model and differential expression functions apply to a wide variety of gene expression technologies including microarrays (single-channel or two-color), quantitative PCR, RNA-seq or"
