---
name: k-nearest-neighbor-algorithm-application
description: Use when your raw metabolomics dataset contains missing values scattered across metabolite columns, and you intend to perform statistical analysis (e.g., linear mixed models, ANOVA, or dimensionality reduction) that requires complete observations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2375
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

# k-nearest-neighbor-algorithm-application

## Summary

Apply k-nearest neighbor imputation to fill missing values in metabolite columns of raw metabolomics datasets after filtering out columns with excessive missingness. This preprocessing step enables downstream statistical analysis by handling data incompleteness while preserving the structure and relationships in the metabolite matrix.

## When to use

Your raw metabolomics dataset contains missing values scattered across metabolite columns, and you intend to perform statistical analysis (e.g., linear mixed models, ANOVA, or dimensionality reduction) that requires complete observations. Apply this skill after quality control steps like duplicate removal and column reordering, but before normalization or statistical modeling.

## When NOT to use

- Input metabolite data is already complete (0% missingness) — imputation is unnecessary and adds computational overhead
- More than 10% of values are missing in a given metabolite column — that column should be excluded rather than imputed to avoid unreliable reconstruction
- Missingness is systematic (e.g., below limit of detection with biological meaning) — mechanistic imputation methods or specialized censored-data approaches may be more appropriate than KNN

## Inputs

- raw metabolomics dataset (data.frame or tibble with metabolite columns and missing values)
- metabolite column identifiers
- numeric metabolite abundance/concentration values

## Outputs

- imputed metabolomics dataset with no missing values in metabolite columns
- column-wise missingness prevalence report (percentage NA per column)

## How to apply

First, load raw metabolomics data (e.g., raw_example_data from MeTEor) and identify metabolite columns with missing values. Filter out any metabolite column where missing data exceeds 10% to avoid imputing over sparse features. On the remaining columns with <10% missingness, apply k-nearest neighbor imputation using the VIM package's kNN function with weighted mean aggregation (weightedMean, weightDist=TRUE), which aggregates the k nearest complete neighbors weighted by distance. The weighted approach ensures that closer neighbors contribute more to the imputed value. Return the complete imputed dataset with all remaining missing values filled, ready for downstream analysis.

## Related tools

- **VIM** (Performs k-nearest neighbor imputation with weighted mean aggregation (kNN function with weightedMean, weightDist=TRUE parameters))
- **MeTEor** (R Shiny application that wraps preprocessing workflows including KNN imputation as part of data-cleaning pipeline for longitudinal metabolomics data) — https://github.com/scibiome/meteor
- **R** (Programming language runtime for loading data, filtering columns, and executing imputation functions)
- **tidyverse** (Data manipulation and column selection during metabolite filtering and preprocessing steps)

## Examples

```
library(VIM); library(MeTEor); data(raw_example_data); metabolite_cols <- raw_example_data[, sapply(raw_example_data, is.numeric)]; filtered_cols <- metabolite_cols[, colSums(is.na(metabolite_cols))/nrow(metabolite_cols) < 0.10]; imputed_data <- kNN(filtered_cols, k=5, weightedMean=TRUE, weightDist=TRUE);
```

## Evaluation signals

- All missing values in metabolite columns (that passed the 10% NA filter) are replaced with numeric values; no NA remains in the imputed dataset
- Columns with >10% initial missingness are completely removed; column count decreases accordingly
- Imputed values fall within the observed range of their respective metabolite columns, confirming neighborhood-based reconstruction
- Pairwise Euclidean or correlation distances between complete and imputed rows remain small, validating that neighbors were weighted appropriately
- Imputed dataset has the same number of rows as input and one fewer column per filtered metabolite

## Limitations

- KNN imputation assumes that missing values are missing at random (MAR) and that nearby samples in the feature space have similar metabolite profiles; violations of this assumption can introduce bias
- Performance degrades when metabolite columns have >10% missingness, necessitating removal rather than imputation; the 10% threshold is a practical heuristic and may vary by dataset
- The choice of k (number of neighbors) and distance metric are not explicitly discussed in the workflow; default VIM settings may not be optimal for all metabolomics datasets
- KNN imputation can propagate measurement error or systematic bias from neighbors to imputed values, especially in high-dimensional metabolomics data where the curse of dimensionality may reduce neighborhood relevance

## Evidence

- [other] Filter out any metabolite with >10% missing data using column-wise NA prevalence checks.: "Identify metabolite columns with missing values and filter out any metabolite with >10% missing data using column-wise NA prevalence checks."
- [other] Apply k-nearest neighbor imputation with weighted mean aggregation to remaining missing values.: "Apply k-nearest neighbor imputation using VIM's kNN function with weighted mean aggregation (weightedMean, weightDist=TRUE) to remaining missing values in metabolite columns."
- [other] Imputation is a necessary preprocessing step before statistical analysis in MeTEor.: "The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor."
- [readme] MeTEor is designed for longitudinal metabolomics data exploration with statistical and predictive models.: "MeTEor is an R Shiny application that offers the possibility to explore longitudinal metabolomics data. For this purpose, a variety of statistical analysis and visualization methods are implemented"
