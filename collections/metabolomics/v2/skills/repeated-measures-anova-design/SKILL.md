---
name: repeated-measures-anova-design
description: Use when you have an imputed, long-format metabolomics dataset with repeated
  measurements (multiple time points) per subject, a categorical grouping variable
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MeTEor
  - R
  - tidyverse
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioadv/vbae178
  title: MeTEor
- doi: 10.1007/978-3-319-47656-8_6
  title: ''
evidence_spans:
- library(MeTEor)
- 'You can perform binary classification using three different algorithms: logistic
  regression (LR), random forest (RF), and XGBoost (XGB).'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# repeated-measures-anova-design

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Repeated measures ANOVA ranks metabolites in longitudinal metabolomics datasets by statistical significance, enabling prioritized feature selection for downstream analysis. This skill applies ANOVA with subject-level random effects to imputed long-format data to identify metabolites with strongest evidence of group differences across time.

## When to use

Apply this skill when you have an imputed, long-format metabolomics dataset with repeated measurements (multiple time points) per subject, a categorical grouping variable (e.g., treatment, phenotype), and you need to rank metabolites by statistical significance to prioritize features for validation or mechanistic studies.

## When NOT to use

- Input data is in wide format (metabolites as columns) without prior conversion to long format.
- Dataset contains missing values that have not been imputed prior to model fitting.
- No repeated measurements per subject exist, or subjects are measured only once.
- Grouping variable is continuous rather than categorical; use linear regression or mixed models instead.

## Inputs

- Long-format imputed metabolomics dataset (columns: subject_id, time_point, grouping_variable, metabolite_name, numeric_value)
- Subject identifier column
- Categorical grouping/treatment variable

## Outputs

- Ranked metabolite feature table (CSV: metabolite_name, F-statistic, p-value, rank)
- ANOVA model objects for each metabolite

## How to apply

Load the imputed long-format metabolomics data containing columns for subject ID, time point, grouping variable, metabolite names, and numeric values. For each metabolite, fit a repeated measures ANOVA model with the grouping variable as a fixed effect and subject ID as a random effect (blocking factor). Extract the F-statistic and p-value from each model's ANOVA table. Rank all metabolites in ascending order by p-value (or descending by F-statistic) to identify those with the strongest evidence of group differences. The ranking prioritizes metabolites most likely to reflect true biological effects rather than random variation. Export the results as a CSV table with columns for metabolite name, F-statistic, p-value, and rank for downstream interpretation.

## Related tools

- **MeTEor** (R Shiny application implementing repeated measures ANOVA, mixed ANOVA, and Friedman test for longitudinal metabolomics feature ranking and visualization) — https://github.com/scibiome/meteor
- **R** (Statistical computing environment for model fitting and ANOVA table extraction)
- **tidyverse** (Data wrangling and long-format manipulation prior to model fitting)

## Examples

```
library(tidyverse); library(MeTEor); data(example_data); long_data <- pivot_longer(example_data, cols=-c(id, time, group), names_to='metabolite', values_to='value'); anova_results <- long_data %>% group_by(metabolite) %>% do(broom::tidy(aov(value ~ group + Error(id/group), data=.))) %>% arrange(p.value)
```

## Evaluation signals

- ANOVA output includes valid F-statistics and p-values for all metabolites; no missing or infinite values.
- Ranked table is sorted in ascending order by p-value with no ties or duplicate ranks unless metabolites have identical p-values.
- P-value distribution shows expected right-skew with most metabolites near p=1 and a subset with p<0.05 for statistical significance.
- Model convergence: each fitted repeated measures ANOVA model converges without singular fit warnings or zero variance components.
- Subject ID is correctly specified as a random effect blocking factor; F-statistics reflect within-subject variation and between-group effects, not subject-level confounding.

## Limitations

- Repeated measures ANOVA assumes sphericity (homogeneity of variance across time differences); violations may inflate Type I error. Consider Mauchly's test or Greenhouse–Geisser correction.
- Unbalanced designs (missing measurements for some subjects at some time points) complicate analysis; balance across subjects and time is preferred.
- P-value ranking alone does not correct for multiple testing across metabolites; family-wise error rate control (e.g., Bonferroni, FDR) should be applied downstream.
- The method assumes metabolite values are normally distributed or can be approximated as such after imputation; highly skewed distributions may require transformation.
- Small sample sizes (few subjects) reduce statistical power; repeated measures ANOVA is most robust with ≥10–15 subjects per group.

## Evidence

- [other] Repeated measures ANOVA with grouping and random effects specification: "For each metabolite, fit a repeated measures ANOVA model with the grouping variable as the fixed effect and id as the random effect (subject)."
- [other] Long-format input data structure: "Load the imputed long-format metabolomics dataset (with id, time, categorical grouping variable, metabolite names, and numeric values)."
- [other] Ranking and export of results: "Rank all metabolites by p-value (ascending) or F-statistic (descending) to prioritize those with strongest evidence of difference across groups. Export the ranked feature table as a CSV file with"
- [readme] MeTEor implements repeated measures ANOVA for metabolomics: "Statistical models: Linear Mixed Models, Repeated Measures ANOVA, Mixed ANOVA, Friedman test"
- [other] Data format requirement for analysis: "The data format is being transformed from wide to long format to make it compatible with MeTEor."
