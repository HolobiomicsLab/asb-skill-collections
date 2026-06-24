---
name: within-subject-correlation-modeling
description: Use when your metabolomics dataset is in long format with repeated measurements
  per subject (id), a grouping variable (e.g., disease status or treatment arm), and
  metabolite abundances measured across time or visits.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MeTEor
  - R
  - tidyverse
  - MetaboAnalyst
  license_tier: restricted
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

# within-subject-correlation-modeling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Repeated measures ANOVA with subject-level random effects applied to longitudinal metabolomics data to identify and rank metabolites by statistical significance of group differences across time or condition. This skill enables feature selection by isolating between-group variance while accounting for within-subject correlation structure.

## When to use

Your metabolomics dataset is in long format with repeated measurements per subject (id), a grouping variable (e.g., disease status or treatment arm), and metabolite abundances measured across time or visits. You need to prioritize metabolites showing strong evidence of difference between groups while controlling for repeated sampling of the same subjects. This is especially relevant when simple univariate tests would violate independence assumptions.

## When NOT to use

- Input is already a pre-computed feature table or ranked list — repeated measures ANOVA is a feature selection step, not a post-hoc validation tool.
- Data is in wide format (one row per subject) — the skill requires long format with one row per observation per subject.
- Samples are independent cross-sectional data with no repeated measurements — standard ANOVA or Kruskal-Wallis is more appropriate and avoids overparameterization.

## Inputs

- Imputed long-format metabolomics dataset (columns: id, time/visit, grouping_variable, metabolite_name, numeric_value)
- Subject-level identifiers (id column)
- Categorical grouping variable (treatment, phenotype, disease status)

## Outputs

- Ranked feature table (CSV: metabolite_name, F-statistic, p-value, rank)
- ANOVA model objects per metabolite (F-statistic, p-value, degrees of freedom)

## How to apply

Load the imputed long-format metabolomics dataset containing id (subject identifier), time or visit variable, categorical grouping variable, metabolite names, and numeric abundance values. For each metabolite, fit a repeated measures ANOVA model with the grouping variable as the fixed effect and id as the random effect (subject). Extract the F-statistic and p-value for each metabolite from the ANOVA model output. Rank all metabolites by ascending p-value or descending F-statistic to prioritize those with strongest evidence of group difference. The repeated measures structure accounts for within-subject correlation, reducing false positives from violations of independence. Export the ranked feature table as CSV with columns: metabolite name, F-statistic, p-value, and rank.

## Related tools

- **MeTEor** (R Shiny application implementing repeated measures ANOVA, mixed models, and ranked feature visualization for longitudinal metabolomics data) — https://github.com/scibiome/meteor
- **R** (Statistical programming environment for fitting repeated measures ANOVA models and extracting model statistics)
- **tidyverse** (R package for data wrangling, reshaping, and export of ranked feature tables)
- **MetaboAnalyst** (Optional downstream tool for ID conversion and pathway enrichment of top-ranked metabolites) — https://www.metaboanalyst.ca

## Examples

```
# In R with MeTEor/tidyverse: for each metabolite in long-format data, fit aov(metabolite_value ~ grouping_var + Error(id/grouping_var), data=long_df); extract F-stat and p-value; rank by p-value ascending
```

## Evaluation signals

- Ranked feature table contains all metabolites with non-null F-statistics and p-values; no missing values in rank column.
- P-values are in valid range [0, 1] and ranks are sequential integers without gaps or duplicates.
- Top-ranked metabolites have p-value < 0.05 and high F-statistic values relative to lower-ranked metabolites; monotonic relationship between rank and p-value (ascending).
- Model degrees of freedom reflect the repeated measures structure: df_between = (number of groups − 1), df_within = (total observations − number of subjects − groups + 1).
- Subject identifier (id) is present in the ANOVA random effect specification; comparison with standard ANOVA (treating subject as fixed or ignoring it) shows different rankings due to reduced error term.

## Limitations

- Assumes data are imputed before ANOVA; missing value imputation method (e.g., KNN) can influence p-values and rankings; sensitivity analysis across imputation methods is recommended.
- Repeated measures ANOVA assumes sphericity (homogeneity of within-subject variances across groups); violations may inflate or deflate test statistics; Mauchly's test or post-hoc corrections (Greenhouse-Geisser) may be needed.
- Model assumes linear relationships and normally distributed residuals; severe non-normality may require rank-based alternatives (Friedman test) available in MeTEor.
- Feature selection by p-value alone does not account for biological effect size or metabolite abundance magnitude; combined ranking (p-value + fold-change or F-statistic + effect size) is advisable.

## Evidence

- [other] Repeated measures ANOVA operates on imputed metabolomics data to identify and rank metabolites by their statistical significance, enabling prioritization of features for downstream statistical analysis.: "Repeated measures ANOVA operates on imputed metabolomics data to identify and rank metabolites by their statistical significance, enabling prioritization of features for downstream statistical"
- [other] For each metabolite, fit a repeated measures ANOVA model with the grouping variable as the fixed effect and id as the random effect (subject). Extract the F-statistic and p-value for each metabolite from the ANOVA output.: "For each metabolite, fit a repeated measures ANOVA model with the grouping variable as the fixed effect and id as the random effect (subject). Extract the F-statistic and p-value for each metabolite"
- [other] Rank all metabolites by p-value (ascending) or F-statistic (descending) to prioritize those with strongest evidence of difference across groups.: "Rank all metabolites by p-value (ascending) or F-statistic (descending) to prioritize those with strongest evidence of difference across groups."
- [readme] Statistical models: Linear Mixed Models, Repeated Measures ANOVA, Mixed ANOVA, Friedman test: "Statistical models: Linear Mixed Models, Repeated Measures ANOVA, Mixed ANOVA, Friedman test"
- [other] The data format is being transformed from wide to long format to make it compatible with MeTEor.: "The data format is being transformed from wide to long format to make it compatible with MeTEor."
