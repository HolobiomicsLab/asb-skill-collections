---
name: p-value-interpretation-metabolomics
description: Use when after fitting repeated measures ANOVA models to long-format imputed metabolomics data with a grouping variable (e.g., treatment, disease state) and subject-level random effects.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - MeTEor
  - R
  - tidyverse
derived_from:
- doi: 10.1093/bioadv/vbae178
  title: MeTEor
- doi: 10.1007/978-3-319-47656-8_6
  title: ''
evidence_spans:
- library(MeTEor)
- 'You can perform binary classification using three different algorithms: logistic regression (LR), random forest (RF), and XGBoost (XGB).'
- library(tidyverse) library(VIM) library(laeken) library(MeTEor)
- library(tidyverse)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_meteor_cq
    doi: 10.1093/bioadv/vbae178
    title: MeTEor
  dedup_kept_from: coll_meteor_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbae178
  all_source_dois:
  - 10.1093/bioadv/vbae178
  - 10.1007/978-3-319-47656-8_6
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# p-value-interpretation-metabolomics

## Summary

Interpret p-values from repeated measures ANOVA applied to imputed metabolomics trajectories to identify and rank metabolites by statistical significance. This skill bridges model output to feature prioritization in longitudinal metabolomic studies.

## When to use

After fitting repeated measures ANOVA models to long-format imputed metabolomics data with a grouping variable (e.g., treatment, disease state) and subject-level random effects. Use this skill when you have p-values and F-statistics from ANOVA tests on individual metabolites and need to rank them by evidence of between-group difference to support downstream feature selection.

## When NOT to use

- Input is already a feature table with pre-selected metabolites; this skill is for ranking, not post-hoc refinement.
- ANOVA assumptions are violated (e.g., non-normal residuals, heterogeneous variances); consider non-parametric alternatives such as Friedman test.
- Sample size per group is very small (n < 3–5 per group); p-values may be unreliable due to low statistical power.

## Inputs

- Long-format imputed metabolomics dataset with columns: id (subject identifier), time (measurement timepoint), grouping variable (categorical), metabolite name, and numeric metabolite abundance values
- Repeated measures ANOVA model output containing F-statistics and p-values for each metabolite

## Outputs

- Ranked feature table (CSV) with columns: metabolite name, F-statistic, p-value, rank
- Prioritized metabolite list for downstream statistical or pathway analysis

## How to apply

Extract the p-value for each metabolite from the repeated measures ANOVA model output (fixed effect test for the grouping variable). Sort metabolites in ascending order by p-value (or equivalently, descending by F-statistic) to rank by statistical significance. Apply a significance threshold (commonly α = 0.05) to identify metabolites with strong evidence of difference across groups. Document the ranking with metabolite name, F-statistic, p-value, and rank position in a tabular format. The rationale is that lower p-values indicate stronger evidence against the null hypothesis of no group difference, making them candidates for prioritization in feature selection and subsequent pathway or biomarker analysis.

## Related tools

- **MeTEor** (R Shiny application implementing repeated measures ANOVA and statistical model output for metabolomics; generates p-values and F-statistics used for p-value interpretation and metabolite ranking) — https://github.com/scibiome/meteor
- **R** (Programming language for extracting, sorting, and tabulating p-values and F-statistics from ANOVA model objects)
- **tidyverse** (R package suite for data manipulation and ranking of ANOVA results by p-value)

## Evaluation signals

- Ranked feature table is non-empty and sorted in ascending order by p-value (or descending by F-statistic); spot-check the first and last entries.
- All p-values in output range from 0 to 1 and metabolites are unique (no duplicates).
- Metabolites with p-value < 0.05 appear at the top of the rank; those with p > 0.05 appear lower.
- The number of ranked metabolites matches the number of unique metabolites in the input ANOVA output.
- Summary statistics (e.g., number of significant metabolites at α = 0.05) are consistent with the p-value distribution and total metabolite count.

## Limitations

- p-value interpretation assumes ANOVA model assumptions are met (normality of residuals, sphericity, homogeneity of variance); violations can inflate false positive or false negative rates.
- p-values reflect statistical significance, not biological effect size or magnitude; a small p-value does not guarantee large or clinically meaningful metabolite changes.
- Multiple comparisons across many metabolites increase family-wise error rate; consider applying multiple testing correction (e.g., Bonferroni, FDR) if not already applied upstream.
- Ranking by p-value alone does not account for metabolite stability, measurement variability, or biological plausibility; should be combined with effect size and domain knowledge.

## Evidence

- [other] For each metabolite, fit a repeated measures ANOVA model with the grouping variable as the fixed effect and id as the random effect (subject). Extract the F-statistic and p-value for each metabolite from the ANOVA output.: "For each metabolite, fit a repeated measures ANOVA model with the grouping variable as the fixed effect and id as the random effect (subject). Extract the F-statistic and p-value for each metabolite"
- [other] Rank all metabolites by p-value (ascending) or F-statistic (descending) to prioritize those with strongest evidence of difference across groups.: "Rank all metabolites by p-value (ascending) or F-statistic (descending) to prioritize those with strongest evidence of difference across groups."
- [other] Export the ranked feature table as a CSV file with columns: metabolite name, F-statistic, p-value, and rank.: "Export the ranked feature table as a CSV file with columns: metabolite name, F-statistic, p-value, and rank."
- [readme] Statistical models: Linear Mixed Models, Repeated Measures ANOVA, Mixed ANOVA, Friedman test: "Statistical models: Linear Mixed Models, Repeated Measures ANOVA, Mixed ANOVA, Friedman test"
