---
name: factorial-design-anova
description: Use when you have a LipidomicsExperiment object with samples grouped by a categorical variable (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3668
  edam_topics:
  - http://edamontology.org/topic_3407
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
---

# Perform multi-group differential expression analysis using factorial ANOVA-style design

## Summary

Apply ANOVA-style multi-group differential expression analysis to lipidomics data using formula-based design matrices to test whether categorical variables (e.g., cancer stage, sample type) significantly affect lipid molecular profiles. This skill enables comparison across ≥2 groups while controlling for confounding variables.

## When to use

You have a LipidomicsExperiment object with samples grouped by a categorical variable (e.g., cancer stage, treatment, race) and you want to test whether that variable significantly affects the abundance of individual lipid molecules across all groups simultaneously, rather than performing pairwise comparisons. Use this when you need to account for multiple grouping factors or adjust for confounding variables.

## When NOT to use

- Input data has only 2 groups — use two-group differential analysis (de_analysis()) instead, which is simpler and more statistically efficient
- Samples are already aggregated or summarized by group — de_design() requires individual sample-level measurements
- Data are not normalized or have not been quality-controlled — pre-filtering and normalization are prerequisite steps

## Inputs

- LipidomicsExperiment object with normalized lipid abundance data
- Sample annotations containing categorical grouping variable(s)

## Outputs

- Differential expression results table with per-lipid test statistics, p-values, and adjusted p-values
- List of significantly affected lipid molecules (or confirmation of no significant molecules)
- Model coefficients and fold-changes for each group comparison

## How to apply

Load the prepared LipidomicsExperiment object and call de_design() with a formula specifying the grouping variable and any confounders (e.g., ~ Stage or ~ SampleType + Race). The function internally uses the limma package to fit a linear model for each lipid molecule and perform ANOVA-style testing across groups. Extract the results table and filter for lipids with adjusted p-value thresholds (commonly p_adj > 0.05 for non-significant, p_adj < 0.05 for significant). Examine the results to determine whether any lipid molecules show statistically significant association with the grouping variable. If no significant molecules are identified, conclude that the variable does not substantially affect the lipid profile.

## Related tools

- **lipidr** (Provides de_design() function and LipidomicsExperiment container for multi-group differential expression analysis) — https://github.com/ahmohamed/lipidr
- **limma** (Underlying statistical package used by de_design() to fit linear models and perform ANOVA-style testing)
- **R** (Programming environment for executing lipidr and limma workflows)

## Examples

```
multi_group <- de_design(d, ~ Stage)
```

## Evaluation signals

- Output table contains one row per lipid molecule with columns for test statistic (t or F), p-value, and adjusted p-value
- Adjusted p-values are properly calibrated (e.g., via Benjamini-Hochberg FDR correction) and range from 0 to 1
- Number of significant lipids is sensible relative to total number of lipids profiled and expected effect size; a finding of 'no significant molecules' should be explicitly confirmed by examining the p-value distribution (e.g., histogram or Q-Q plot showing uniform or near-flat distribution under null)
- Results are reproducible: re-running de_design() with identical inputs and formula produces identical p-values and test statistics
- Effect sizes and directions for group comparisons are biologically plausible (e.g., consistent with known lipid class differences between tissue types if applicable)

## Limitations

- Assumes linear relationship between predictors and lipid abundance; violations of normality or homoscedasticity may inflate Type I or Type II error rates
- ANOVA tests for overall effect of grouping variable but does not specify which pairwise group contrasts drive significance — post-hoc pairwise tests are needed to identify specific group differences
- Multiple testing correction (e.g., FDR) reduces power; with thousands of lipids tested, true effects of small-to-moderate size may not meet adjusted significance threshold
- No significant molecules identified does not prove absence of effect — may indicate insufficient power, high within-group variance, or true null effect depending on sample size and variance structure

## Evidence

- [intro] Perform multi-group differential expression analysis using ANOVA-style design: "Perform multi-group differential expression analysis using ANOVA-style design"
- [intro] de_design() function with formula ~ Stage to perform ANOVA-style multi-group differential expression analysis using limma: "Apply de_design() function with formula ~ Stage to perform ANOVA-style multi-group differential expression analysis using limma"
- [intro] Cancer Stage does not appear to affect lipid molecules profiled in this experiment: "Cancer Stage does not appear to affect lipid molecules profiled in this experiment"
- [intro] This step of the workflow requires the limma package to be installed: "This step of the workflow requires the limma package to be installed"
- [readme] Multi-group comparisons and adjusting for confounding variables is also supported: "Multi-group comparisons and adjusting for confounding variables is also supported"
