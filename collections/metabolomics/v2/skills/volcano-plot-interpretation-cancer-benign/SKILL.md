---
name: volcano-plot-interpretation-cancer-benign
description: Use when when you have performed two-group differential expression analysis on preprocessed LipidomicsExperiment objects (with logged and normalized Area measurements) and need to identify and visualize lipid molecules with statistically significant differential regulation between cancer and benign.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
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
---

# volcano-plot-interpretation-cancer-benign

## Summary

Generate and interpret volcano plots to visualize log2-fold-change and adjusted p-values in two-group differential lipidomics analysis comparing cancer to benign tissue samples. This skill identifies lipid classes with significant regulatory patterns (up- or down-regulation) that distinguish disease states.

## When to use

When you have performed two-group differential expression analysis on preprocessed LipidomicsExperiment objects (with logged and normalized Area measurements) and need to identify and visualize lipid molecules with statistically significant differential regulation between cancer and benign sample groups, particularly to highlight lipid class-level patterns.

## When NOT to use

- Input has not been filtered for outlier samples—remove outliers (e.g., samples 18 and 42 in ST001111) before differential analysis.
- Area measurements are not logged and normalized—set logged and normalized status using set_logged() and set_normalized() before proceeding.
- Comparing more than two groups—use multi-group ANOVA-style design (de_design) instead of two-group contrast.
- Raw or unnormalized intensity data—lipidr requires preprocessed, quality-controlled input.

## Inputs

- LipidomicsExperiment object with logged and normalized Area measurements
- Two-group differential analysis results object (from de_analysis)
- Outlier-filtered sample set

## Outputs

- Volcano plot visualization with log2-fold-change and adjusted p-values
- Identified lipid classes with significant up- or down-regulation
- Differential regulation pattern summary (e.g., 'PCs and PGs up-regulated, CLs and TGs down-regulated')

## How to apply

After performing de_analysis() with Cancer-Benign contrast using the limma package on outlier-cleaned LipidomicsExperiment data, generate volcano plots using plot_results_volcano() to simultaneously display log2-fold-change (x-axis) and adjusted p-values (y-axis). Identify lipid classes (e.g., phosphatidylcholines, phosphatidylglycerols, cardiolipins, triglycerides) that segregate into distinct quadrants: up-regulated classes appear in the right upper quadrant (positive log2-FC, low adjusted p-value), while down-regulated classes appear in the left upper quadrant (negative log2-FC, low adjusted p-value). Use the volcano plot to stratify lipid classes by both effect size and statistical significance, interpreting the patterns as markers of differential lipid metabolism between disease states.

## Related tools

- **lipidr** (Generates volcano plots and performs two-group differential expression analysis on LipidomicsExperiment objects; primary interface for this skill) — https://github.com/ahmohamed/lipidr
- **limma** (Provides statistical testing engine for two-group differential expression analysis; called internally by de_analysis())
- **R** (Programming environment for executing lipidr and limma functions)

## Examples

```
two_group <- de_analysis(d, Cancer~Benign, Cancer~Metastasis)
plot_results_volcano(two_group)
```

## Evaluation signals

- Volcano plot displays clear separation of log2-fold-change and adjusted p-value axes with distinct quadrant structure (up-reg upper-right, down-reg upper-left).
- Lipid classes identified as significantly regulated (adjusted p-value < 0.05) match known metabolic signatures (e.g., elevated PCs/PGs and reduced CLs/TGs in cancer tissues align with altered membrane synthesis and energy metabolism).
- Effect sizes (log2-FC magnitudes) are consistent across biological replicates and interpretable in context of tissue type comparison.
- No data points appear outside the plot bounds, indicating proper axis scaling and statistical range coverage.
- Volcano plot confirms outlier removal was effective—no isolated extreme points indicating residual batch effects or unmeasured confounders.

## Limitations

- Volcano plots require pre-removal of outlier samples; failing to do so produces biased fold-change estimates and inflated p-values.
- Two-group contrasts do not account for confounding variables (e.g., race, cancer stage); use factorial or multi-factor designs with adjusted analyses when such variables are present.
- Lipid class patterns may be obscured if individual lipid species have opposing regulation within a class; consider species-level resolution if class-level signal is weak.
- Statistical significance (adjusted p-value) depends on sample size and variance; small cohorts or high within-group heterogeneity reduce power to detect true differences.
- Interpretation assumes logged and normalized Area measurements; unnormalized or non-logged data will produce misleading fold-change and variance estimates.

## Evidence

- [intro] A fairly large difference is observed between cancer and benign samples, with PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues.: "A fairly large difference is observed between cancer and benign samples, with PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues."
- [intro] Perform two-group differential expression analysis using de_analysis() with Cancer-Benign and Cancer-Metastasis contrasts, leveraging the limma package for statistical testing. Generate volcano plots using plot_results_volcano() to visualize log2-fold-change and adjusted p-values.: "Perform two-group differential expression analysis using de_analysis() with Cancer-Benign and Cancer-Metastasis contrasts, leveraging the limma package for statistical testing. Generate volcano plots"
- [readme] Univariate analysis can be performed using any of the loaded clinical variables, which can be readily visualized as volcano plots.: "Univariate analysis can be performed using any of the loaded clinical variables, which can be readily visualized as volcano plots."
- [intro] Remove outlier samples (samples 18 and 42) using column subsetting.: "Remove outlier samples (samples 18 and 42) using column subsetting."
- [intro] d <- set_logged(d, "Area", TRUE) d <- set_normalized(d, "Area", TRUE): "d <- set_logged(d, "Area", TRUE) d <- set_normalized(d, "Area", TRUE)"
