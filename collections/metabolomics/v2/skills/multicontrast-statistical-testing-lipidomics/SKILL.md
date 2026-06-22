---
name: multicontrast-statistical-testing-lipidomics
description: Use when after removing outlier samples and confirming data quality through PCA or TIC plots, apply this skill when you need to quantify statistical significance of lipid abundance differences across defined sample groups (e.g., disease vs. control, treatment vs. untreated, cancer stages).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3668
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
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

# multicontrast-statistical-testing-lipidomics

## Summary

Perform two-group and multi-group differential expression analysis on lipidomics data using the limma package to identify lipid classes with significant regulation patterns across biological contrasts (e.g., cancer vs. benign, cancer vs. metastasis). This skill detects which lipid molecular species and classes are systematically up- or down-regulated between sample groups.

## When to use

After removing outlier samples and confirming data quality through PCA or TIC plots, apply this skill when you need to quantify statistical significance of lipid abundance differences across defined sample groups (e.g., disease vs. control, treatment vs. untreated, cancer stages). Use it specifically when comparing two or more groups defined by clinical variables stored in the LipidomicsExperiment sample annotations.

## When NOT to use

- Input has not undergone outlier removal or quality control assessment; remove obvious outliers first via PCA or boxplot review.
- Sample groups are not well-defined in the annotation table; ensure clinical variables are complete and unambiguous.
- Data are not logged and normalized; lipidr requires set_logged() and set_normalized() to be true for Area measurements before de_analysis().

## Inputs

- LipidomicsExperiment object with logged and normalized Area measurements
- Sample annotation table with clinical variables (e.g., SampleType, Stage, Race)
- Outlier-filtered sample set (outlier samples removed via column subsetting)

## Outputs

- Differential expression results table with log2-fold-change, test statistic, and adjusted p-values per lipid
- Volcano plot(s) visualizing log2-fold-change vs. adjusted p-value
- List of significantly regulated lipid classes (PCs, PGs, CLs, TGs, etc.) with direction and magnitude

## How to apply

Load the quality-controlled LipidomicsExperiment object with logged and normalized Area measurements. For two-group comparisons, call de_analysis() specifying contrasts (e.g., Cancer-Benign, Cancer-Metastasis); the function leverages the limma package for empirical Bayes-moderated t-statistics and adjusted p-values across all measured lipids. For multi-group comparisons, use de_design() with ANOVA-style formulas (e.g., ~ Stage) to test for global differences. Generate volcano plots using plot_results_volcano() to visualize log2-fold-change (x-axis) against adjusted p-values (y-axis), highlighting lipid classes (PCs, PGs, CLs, TGs, etc.) with significant differential regulation. Interpret results by examining which lipid classes cluster together in the volcano plot and cross-reference with biological phenotypes.

## Related tools

- **lipidr** (Core R package providing de_analysis(), de_design(), and plot_results_volcano() functions for differential expression and visualization of lipidomics datasets) — https://github.com/ahmohamed/lipidr
- **limma** (Underlying statistical package used by lipidr for empirical Bayes-moderated t-tests and ANOVA in differential expression analysis)
- **R** (Programming environment for executing lipidr workflows and statistical testing)

## Examples

```
two_group <- de_analysis(d, Cancer-Benign, Cancer-Metastasis); plot_results_volcano(two_group)
```

## Evaluation signals

- Volcano plot shows clear separation of regulated lipids with log2-fold-change thresholds and adjusted p-value cutoffs (e.g., p < 0.05, |log2FC| > 1).
- Lipid classes cluster consistently by biological phenotype (e.g., PCs and PGs up-regulated in cancer, CLs and TGs down-regulated), matching known biology.
- Adjusted p-values are properly calculated and multiple-testing correction (e.g., Benjamini-Hochberg) is reflected in reported q-values.
- Number of significantly regulated lipids is reasonable relative to sample size and effect magnitude; extreme numbers may indicate batch effects or confounders.
- Results replicate across independent contrasts when applicable (e.g., Cancer-Benign and Cancer-Metastasis comparisons show consistent lipid class directionality).

## Limitations

- Outlier samples must be identified and removed manually or via external QC metrics before de_analysis(); the skill does not auto-detect outliers.
- Small sample sizes per group may yield underpowered contrasts and inflated false discovery rates despite multiple-testing correction.
- Cancer Stage does not appear to affect lipid molecules profiled in some datasets, limiting the utility of stage-based contrasts in certain biological contexts.
- Race and other confounding variables may introduce small but detectable effects that can be corrected for in multi-group models but require explicit formula specification.

## Evidence

- [intro] Differential expression statistical method applied to lipidomics: "Perform two-group differential expression analysis using de_analysis() with Cancer-Benign and Cancer-Metastasis contrasts, leveraging the limma package for statistical testing."
- [intro] Expected outcome: lipid class regulation patterns: "Phosphatidylcholines (PCs) and phosphatidylglycerols (PGs) are up-regulated while cardiolipins (CLs) and triglycerides (TGs) are down-regulated in cancer tissues compared to benign samples."
- [intro] Visualization and interpretation method: "Generate volcano plots using plot_results_volcano() to visualize log2-fold-change and adjusted p-values, highlighting lipid classes with differential regulation."
- [intro] Multi-group comparison methodology: "Perform multi-group differential expression analysis using ANOVA-style design"
- [intro] Tool requirement and integration: "This step of the workflow requires the limma package to be installed."
- [intro] Data input requirements: "Load the lipidr library and the pre-processed LipidomicsExperiment object for ST001111 with logged and normalized Area measurements."
- [readme] Univariate analysis capabilities: "Univariate analysis can be performed using any of the loaded clinical variables, which can be readily visualized as volcano plots. Multi-group comparisons and adjusting for confounding variables is"
