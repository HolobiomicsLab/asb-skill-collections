---
name: outlier-sample-identification-pca
description: Use when after normalizing and log-transforming a LipidomicsExperiment object, when you need to detect samples with aberrant lipid profiles before differential expression or multivariate analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - lipidr
  - R
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr` provides an easy way to re-analyze and visualize these datasets.'
- Data Mining and Analysis of Lipidomics Datasets in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidr_cq
    doi: 10.1021/acs.jproteome.0c00082
    title: lipidr
  dedup_kept_from: coll_lipidr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00082
  all_source_dois:
  - 10.1021/acs.jproteome.0c00082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# outlier-sample-identification-pca

## Summary

Identify anomalous samples in lipidomics datasets by performing PCA on normalized and log-transformed lipid abundance data, then visually inspecting score plots for samples with large dispersion relative to the primary sample grouping (e.g., SampleType). Outlier samples are those with unusual PC scores that may warrant removal prior to downstream statistical analysis.

## When to use

After normalizing and log-transforming a LipidomicsExperiment object, when you need to detect samples with aberrant lipid profiles before differential expression or multivariate analysis. Apply this skill when the research question requires confidence that sample cohorts are homogeneous and that no technical or biological outliers will bias downstream comparisons (e.g., benign vs. cancer classification).

## When NOT to use

- Input data has not been normalized and log-transformed; apply quality control and normalization first.
- Sample size is very small (n < 10 per group); PCA may not reveal stable structure and visual inspection becomes unreliable.
- Research question does not require homogeneous sample cohorts; if outliers are scientifically interesting (e.g., treatment responders vs. non-responders), retain them and use stratified or robust statistical methods instead.

## Inputs

- LipidomicsExperiment object (normalized and log-transformed on Area measure)
- Sample metadata with phenotype annotations (e.g., SampleType, Cancer Stage)

## Outputs

- PCA score plot (PC1 vs PC2, colored by sample phenotype)
- List of outlier sample IDs (e.g., sample 18, sample 42)
- Rationale for outlier flagging (e.g., PC score ranges, visual inspection notes)

## How to apply

Load a normalized and logged LipidomicsExperiment object (e.g., ST001111), then invoke mva() with method='PCA' on the Area measure to compute principal components. Generate a score plot via plot_mva() with color_by set to the primary phenotype of interest (e.g., SampleType) and components=(1,2) to visualize samples in PC1–PC2 space. Visually inspect the plot for samples that deviate substantially from their expected phenotype cluster—samples with markedly larger dispersion or isolation from their cohort group are flagged as outliers. In the ST001111 example, samples 18 and 42 showed significantly large dispersion in PC space and were identified for removal. Document the outlier sample IDs and rationale (e.g., extreme PC scores, separation from expected cluster), then optionally exclude them using subsetting operations before proceeding to statistical testing.

## Related tools

- **lipidr** (Compute PCA via mva() function and generate score plots via plot_mva(); manages LipidomicsExperiment object and phenotype annotations) — https://github.com/ahmohamed/lipidr
- **R** (Execution environment for lipidr package and data manipulation)

## Examples

```
mvaresults <- mva(d, measure="Area", method="PCA")
plot_mva(mvaresults, color_by="SampleType", components=c(1,2))
# Inspect plot; visually identify outlier samples (e.g., 18, 42)
keep_samples <- !colnames(d) %in% c("18", "42")
d_filtered <- d[, keep_samples]
```

## Evaluation signals

- Score plot visually shows clear clustering by SampleType (or other primary phenotype) with minimal within-group scatter for non-outlier samples.
- Identified outliers have PC1 and/or PC2 scores that deviate >2 standard deviations from their expected phenotype cluster mean.
- Removal of flagged outliers (e.g., samples 18 and 42) does not introduce missing data or unbalanced group sizes below acceptable thresholds (typically n ≥ 3 per group).
- Post-removal PCA shows improved phenotype separation (increased visual clustering and reduced within-group variance) compared to pre-removal PCA.
- Outlier samples are documented in methods/results with their PC scores and justification for removal; reproducible via recorded sample IDs.

## Limitations

- PCA-based outlier detection is unsupervised and relies on visual inspection; subjective interpretation of 'large dispersion' may vary between analysts. Consider establishing a priori thresholds (e.g., >2 SD from group center) to reduce bias.
- PCA assumes that the first 1–2 components capture the dominant variance; if separation is driven by higher-order PCs, score plots on (PC1, PC2) alone may miss outliers or misidentify them. Inspect multiple component pairs or use alternative methods (PCoA, OPLS-DA) if warranted.
- Mild separation between sample groups (e.g., benign vs. cancer in ST001111) makes it difficult to distinguish outliers from legitimate samples on the periphery of a diffuse cluster; biological validation is recommended before removal.
- Removing outliers reduces statistical power and may introduce bias if outliers are non-random (e.g., correlated with batch, site, or unrecorded metadata). Document and justify all removals.

## Evidence

- [other] PCA revealed mild separation between benign and cancer samples but not between cancer and metastasis, with samples 18 and 42 identified as outliers with significantly large dispersion warranting consideration for removal.: "PCA revealed mild separation between benign and cancer samples but not between cancer and metastasis, with samples 18 and 42 identified as outliers with significantly large dispersion warranting"
- [intro] mvaresults = mva(d, measure="Area", method="PCA")
plot_mva(mvaresults, color_by="SampleType", components = c(1,2)): "mvaresults = mva(d, measure="Area", method="PCA")
plot_mva(mvaresults, color_by="SampleType", components = c(1,2))"
- [readme] lipidr implements PCA, PCoA and OPLS(DA) to reveal patterns in data and discover variables related to an outcome of interest. Top associated lipids as well as scores and loadings plots can be interactively investigated using `lipidr`.: "lipidr implements PCA, PCoA and OPLS(DA) to reveal patterns in data and discover variables related to an outcome of interest."
- [intro] keep_samples <- !colnames(d) %in% c("18", "42")
d <- d[, keep_samples]: "keep_samples <- !colnames(d) %in% c("18", "42")
d <- d[, keep_samples]"
- [readme] lipidr generates various plots, such as box plots or PCA, for quality control of samples and measured lipids.: "lipidr generates various plots, such as box plots or PCA, for quality control of samples and measured lipids."
