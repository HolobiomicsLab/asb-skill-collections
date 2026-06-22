---
name: metabolite-feature-ranking
description: Use when you have an imputed, long-format metabolomics dataset with repeated measurements across subjects and a grouping variable (e.
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

# metabolite-feature-ranking

## Summary

Rank metabolites in imputed longitudinal metabolomics datasets by statistical significance using repeated measures ANOVA to enable prioritized feature selection for downstream analysis. This skill applies ANOVA models to identify metabolites with the strongest evidence of difference across experimental groups.

## When to use

Apply this skill when you have an imputed, long-format metabolomics dataset with repeated measurements across subjects and a grouping variable (e.g., treatment arm, disease status), and you need to identify and prioritize metabolites that show statistically significant variation between groups for feature selection before multivariate or predictive modeling.

## When NOT to use

- Dataset contains unimputed missing values — imputation must be completed first (via KNN or other methods)
- Data is not in long format with repeated measurements per subject — repeated measures ANOVA requires within-subject structure
- No grouping variable or categorical contrast of interest exists in the design

## Inputs

- Imputed long-format metabolomics dataset (columns: id, time, grouping_variable, metabolite_name, numeric_value)
- Experimental design metadata (subject identifiers, group assignments)

## Outputs

- Ranked metabolite feature table (CSV: metabolite_name, F_statistic, p_value, rank)
- ANOVA model objects (F-statistics and p-values per metabolite)

## How to apply

Load the imputed long-format metabolomics dataset containing subject ID, timepoint, grouping variable, metabolite names, and numeric values. For each metabolite independently, fit a repeated measures ANOVA model with the grouping variable as a fixed effect and subject ID as a random effect to account for within-subject correlation. Extract the F-statistic and p-value from each ANOVA model output. Rank all metabolites by ascending p-value (or descending F-statistic) to prioritize those with the strongest statistical evidence of group differences. Export the ranked metabolite table as a CSV file containing metabolite name, F-statistic, p-value, and rank position for downstream interpretation and feature selection.

## Related tools

- **MeTEor** (R Shiny application implementing repeated measures ANOVA, linear mixed models, and metabolite ranking for longitudinal metabolomics exploration and statistical analysis) — https://github.com/scibiome/meteor
- **R** (Statistical computing environment for implementing ANOVA models and ranking computations)
- **tidyverse** (R package suite for data manipulation, transformation, and export of ranked metabolite tables)

## Examples

```
library(MeTEor); library(tidyverse); # Load imputed long-format data; anova_results <- metabolomics_data %>% group_by(metabolite_name) %>% summarize(f_stat = anova(lmer(value ~ group_var + (1|id)))$'F value', p_val = anova(lmer(value ~ group_var + (1|id)))$'Pr(>F)', .groups='drop') %>% arrange(p_val) %>% mutate(rank = row_number()); write.csv(anova_results, 'ranked_metabolites.csv', row.names=FALSE)
```

## Evaluation signals

- Ranked metabolite table is non-empty and contains all metabolites from input dataset with no duplicates
- All p-values are between 0 and 1; F-statistics are non-negative; ranks are sequential integers starting from 1
- Metabolites are sorted by p-value ascending (or F-statistic descending); ties are handled consistently
- CSV export includes all required columns (metabolite_name, F_statistic, p_value, rank) with correct data types and no missing values
- Top-ranked metabolites (lowest p-values) show biological plausibility or concordance with known group-discriminating features from the study context

## Limitations

- Repeated measures ANOVA assumes compound symmetry or sphericity of the covariance structure; violations may inflate Type I error — consider Greenhouse-Geisser correction if covariance assumptions are violated
- Ranking by p-value alone does not account for effect size; biologically important metabolites with small p-values may differ minimally between groups
- Missing data remaining after imputation will bias ANOVA estimates; imputation method (e.g., KNN) quality affects downstream ranking
- Multiple testing correction (e.g., Bonferroni, FDR) is not applied in the basic workflow; practitioners should apply correction for large-scale feature selection

## Evidence

- [other] For each metabolite, fit a repeated measures ANOVA model with the grouping variable as the fixed effect and id as the random effect (subject).: "For each metabolite, fit a repeated measures ANOVA model with the grouping variable as the fixed effect and id as the random effect (subject)."
- [other] Extract the F-statistic and p-value for each metabolite from the ANOVA output. Rank all metabolites by p-value (ascending) or F-statistic (descending) to prioritize those with strongest evidence of difference across groups.: "Extract the F-statistic and p-value for each metabolite from the ANOVA output. Rank all metabolites by p-value (ascending) or F-statistic (descending) to prioritize those with strongest evidence of"
- [other] Repeated measures ANOVA operates on imputed metabolomics data to identify and rank metabolites by their statistical significance, enabling prioritization of features for downstream statistical analysis.: "Repeated measures ANOVA operates on imputed metabolomics data to identify and rank metabolites by their statistical significance, enabling prioritization of features for downstream statistical"
- [readme] Statistical models: Linear Mixed Models, Repeated Measures ANOVA, Mixed ANOVA, Friedman test: "Statistical models: Linear Mixed Models, Repeated Measures ANOVA, Mixed ANOVA, Friedman test"
- [other] The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor.: "The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor."
