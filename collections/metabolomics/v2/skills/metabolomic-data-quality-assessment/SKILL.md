---
name: metabolomic-data-quality-assessment
description: Use when when you have raw metabolomics data with missing values in metabolite columns and need to prepare the dataset for downstream statistical analysis (linear mixed models, ANOVA, dimensionality reduction, or prediction models).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - VIM
  - R
  - MeTEor
  - tidyverse
derived_from:
- doi: 10.1093/bioadv/vbae178
  title: MeTEor
- doi: 10.1007/978-3-319-47656-8_6
  title: ''
evidence_spans:
- library(VIM)
- library(tidyverse) library(VIM) library(laeken) library(MeTEor)
- library(MeTEor)
- 'You can perform binary classification using three different algorithms: logistic regression (LR), random forest (RF), and XGBoost (XGB).'
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

# metabolomic-data-quality-assessment

## Summary

Assessment and remediation of missing data patterns in raw metabolomics datasets before statistical analysis. This skill identifies metabolite columns with excessive missingness and applies k-nearest neighbor imputation to preserve data integrity while handling missing values in metabolite concentrations.

## When to use

When you have raw metabolomics data with missing values in metabolite columns and need to prepare the dataset for downstream statistical analysis (linear mixed models, ANOVA, dimensionality reduction, or prediction models). Specifically, apply this skill when you encounter metabolite concentration tables with incomplete measurements that must be handled before analysis in MeTEor or other statistical workflows.

## When NOT to use

- Input dataset contains >50% missing data across all metabolite columns—imputation becomes unreliable and alternative missing data mechanism analysis is needed.
- Metabolite columns are already complete (no missing values)—filtering and imputation steps are unnecessary.
- Missing data is not random (MNAR) and represents actual non-detection due to instrumental sensitivity limits—imputation may introduce bias; consider alternative approaches such as imputation to the limit of detection (LOD).

## Inputs

- raw metabolomics dataset with metabolite columns and sample rows
- metabolite concentration matrix with missing values (NA/NaN)
- sample metadata (optional, for stratification)

## Outputs

- imputed metabolomics dataset with all remaining missing values filled
- list of removed metabolite columns (those with >10% NA)
- summary statistics of missingness before and after imputation

## How to apply

First, load the raw metabolomics dataset (e.g., raw_example_data) and perform column-wise NA prevalence checks to identify metabolite columns with missing values. Filter out any metabolite column where missing data exceeds 10% of observations. For the remaining metabolites with missing values below this threshold, apply k-nearest neighbor imputation using the VIM package's kNN function with weighted mean aggregation (weightedMean, weightDist=TRUE) to estimate missing values based on the k nearest neighbors in the feature space. The rationale is that metabolites with >10% missingness lack sufficient observed data for reliable imputation, while KNN with distance weighting leverages the multivariate correlation structure of metabolomic profiles to impute sparse missing values more accurately than simple mean imputation.

## Related tools

- **VIM** (Provides the kNN function for distance-weighted k-nearest neighbor imputation of missing metabolite values)
- **MeTEor** (R Shiny application framework for exploration of preprocessed longitudinal metabolomics data after quality assessment and imputation) — https://github.com/scibiome/meteor
- **R** (Statistical computing environment for executing data quality checks, filtering, and imputation workflows)
- **tidyverse** (R package suite for data manipulation and quality assessment (column filtering, NA prevalence checks))

## Examples

```
library(VIM); library(MeTEor); data(raw_example_data); imputed_data <- kNN(raw_example_data, variable = colnames(raw_example_data)[sapply(raw_example_data, function(x) sum(is.na(x)) / length(x) <= 0.1)], k = 5, weightDist = TRUE, numFactor = 2)
```

## Evaluation signals

- Verify that all metabolite columns remaining in the output have ≤10% missing data before imputation; columns above this threshold are absent from the output.
- Confirm that no NA/NaN values remain in metabolite columns of the imputed dataset—all previously missing values should be filled with numeric estimates.
- Check that imputed values fall within the expected range (minimum and maximum of observed values for each metabolite, or within biological/instrumental bounds).
- Verify that the k-nearest neighbor distance weighting was applied; metabolites with similar profiles should have been used to estimate missing values.
- Cross-validate: run the same imputation with different random seeds or k values and ensure results are stable and consistent.

## Limitations

- KNN imputation assumes missing data is missing completely at random (MCAR) or missing at random (MAR); if missingness depends on unobserved metabolite values themselves (MNAR), estimates may be biased.
- The 10% NA threshold is a heuristic and may not be appropriate for all metabolomics studies; datasets with sparse metabolite coverage or rare compounds may require threshold adjustment.
- KNN imputation performs poorly when the number of metabolite features is very small (few predictors for neighbors); high-dimensional metabolomics data (hundreds to thousands of metabolites) is preferred.
- Distance-weighted KNN is sensitive to the choice of k (number of neighbors); the article does not specify the k value used, and results may vary with different k selections.
- No changelog or version history is available for the MeTEor package, making it difficult to track changes to the imputation implementation over time.

## Evidence

- [other] The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor.: "The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor."
- [other] Remove columns with more than 10% NA as a filter step in preprocessing.: "Remove columns with more than 10% NA"
- [other] KNN imputation is applied to remaining metabolite columns with missing values.: "impute columns using KNN"
- [other] The workflow applies k-nearest neighbor imputation with weighted mean aggregation to handle missing metabolite values.: "Apply k-nearest neighbor imputation using VIM's kNN function with weighted mean aggregation (weightedMean, weightDist=TRUE)"
- [readme] MeTEor is an R Shiny application that explores longitudinal metabolomics data with statistical analysis and visualization methods.: "MeTEor is an R Shiny application that offers the possibility to explore longitudinal metabolomics data. For this purpose, a variety of statistical analysis and visualization methods are implemented"
