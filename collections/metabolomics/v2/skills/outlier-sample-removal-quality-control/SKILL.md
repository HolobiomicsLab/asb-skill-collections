---
name: outlier-sample-removal-quality-control
description: Use when visual inspection (PCA plots, TIC plots, or boxplots) reveals samples with aberrant lipid abundance profiles, or when domain knowledge suggests specific samples are technical replicates, biological outliers, or failed QC metrics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - lipidr
  - limma
  - R
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr` provides an easy way to re-analyze and visualize these datasets.'
- This step of the workflow requires the `limma` package to be installed.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# outlier-sample-removal-quality-control

## Summary

Identify and remove anomalous samples from a LipidomicsExperiment object prior to differential analysis to improve statistical power and reliability of lipid biomarker discovery. This quality control step prevents outlier samples from inflating variance and obscuring genuine lipid class regulation patterns.

## When to use

Apply this skill when visual inspection (PCA plots, TIC plots, or boxplots) reveals samples with aberrant lipid abundance profiles, or when domain knowledge suggests specific samples are technical replicates, biological outliers, or failed QC metrics. Use before proceeding to two-group or multi-group differential expression analysis with de_analysis() or de_design().

## When NOT to use

- When sample removal would reduce group size below the statistical minimum (e.g., n<3 per group for differential analysis)
- When outliers are biologically relevant (e.g., disease progression extremes or rare phenotypes that are the subject of investigation)
- When the input is already a processed feature table and raw QC metrics (TIC, boxplot distributions) are unavailable

## Inputs

- LipidomicsExperiment object with logged and normalized Area measurements
- Sample annotation table with clinical/experimental metadata

## Outputs

- Filtered LipidomicsExperiment object with outlier samples removed
- PCA and boxplot visualizations showing improved sample clustering
- List of removed sample identifiers for documentation

## How to apply

First, perform quality control assessment using plot_samples(d, 'tic') and plot_samples(d, 'boxplot') to visualize total ion current and lipid abundance distributions across samples. Generate a PCA multivariate analysis using mva(d, measure='Area', method='PCA') and plot_mva() to identify samples with extreme scores that deviate from the main cluster. Document suspected outlier sample identifiers (e.g., samples 18 and 42 in ST001111). Remove flagged samples using column subsetting: keep_samples <- !colnames(d) %in% c('outlier_id_1', 'outlier_id_2'); d <- d[, keep_samples]. Verify removal by re-running PCA or boxplots to confirm improved homogeneity before statistical testing.

## Related tools

- **lipidr** (Primary framework for LipidomicsExperiment object manipulation, visualization (plot_samples, plot_mva), and outlier flagging via multivariate analysis) — https://github.com/ahmohamed/lipidr
- **limma** (Required for downstream differential expression analysis after outlier removal; supports proper variance estimation on filtered samples)

## Examples

```
keep_samples <- !colnames(d) %in% c("18", "42"); d <- d[, keep_samples]
```

## Evaluation signals

- PCA plot shows tighter clustering of retained samples with reduced PC1/PC2 spread compared to pre-filtered data
- Boxplot median and interquartile range of lipid abundances become more consistent across samples after removal
- Removed samples had extreme TIC values or lipid class abundance distributions visually distinct from the main cohort
- Subsequent de_analysis() volcano plots show more significant lipid class associations (lower adjusted p-values, larger log2-fold-changes) due to reduced noise
- Sample count and identifiers in the filtered LipidomicsExperiment match documented outlier list

## Limitations

- No automated statistical outlier detection algorithm is provided; removal relies on visual inspection and domain judgment, introducing subjectivity
- Removing samples reduces statistical power; excessive removal may eliminate true biological variation and limit generalizability
- lipidr does not report detection of batch effects or technical confounders; outliers due to instrument drift may not be visually apparent in PCA alone
- The article demonstrates removal on a single dataset (ST001111); optimal outlier thresholds may vary across lipidomics platforms and tissue types

## Evidence

- [intro] Remove outlier samples using column subsetting: "Remove outlier samples  [section=intro; evidence='keep_samples <- !colnames(d) %in% c("18", "42")
d <- d[, keep_samples]']"
- [intro] QC visualization supports outlier identification: "Quality control assessment using TIC plots and boxplots  [section=intro; evidence='plot_samples(d, "tic")
plot_samples(d, "boxplot")']"
- [intro] PCA reveals sample separation patterns that guide removal decisions: "Perform PCA multivariate analysis  [section=intro; evidence='mvaresults = mva(d, measure="Area", method="PCA")
plot_mva(mvaresults, color_by="SampleType", components = c(1,2))']"
- [intro] Outlier removal improves downstream differential analysis results: "A fairly large difference is observed between cancer and benign samples, with PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues."
- [readme] README documents column subsetting as the removal mechanism: "Lipids can be filtered by their %CV.  Normalization methods with and without internal standards are also supported."
