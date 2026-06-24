---
name: metabolite-column-filtering-by-missing-rate
description: Use when apply this filter when raw metabolomics data contains metabolite
  columns with varying amounts of missing values and you aim to conduct statistical
  analysis or imputation. The trigger is the presence of column-wise NA prevalence
  >10% in metabolite features;
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
  license_tier: restricted
derived_from:
- doi: 10.1093/bioadv/vbae178
  title: MeTEor
- doi: 10.1007/978-3-319-47656-8_6
  title: ''
evidence_spans:
- library(VIM)
- library(tidyverse) library(VIM) library(laeken) library(MeTEor)
- library(MeTEor)
- 'You can perform binary classification using three different algorithms: logistic
  regression (LR), random forest (RF), and XGBoost (XGB).'
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

# metabolite-column-filtering-by-missing-rate

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter out metabolite columns with excessive missing data before imputation to reduce noise and improve data quality in metabolomics preprocessing. This step removes uninformative metabolite features that exceed a prevalence threshold of missingness, typically >10%, to focus downstream analysis on well-measured analytes.

## When to use

Apply this filter when raw metabolomics data contains metabolite columns with varying amounts of missing values and you aim to conduct statistical analysis or imputation. The trigger is the presence of column-wise NA prevalence >10% in metabolite features; removing these columns prevents imputation bias and improves statistical power by excluding sparse measurements.

## When NOT to use

- Data is already preprocessed and imputed; filtering post-imputation may remove valid imputed values.
- Metabolite features are rare/sparse by design (e.g., biomarker discovery where low-abundance analytes are of interest) and >10% missingness may be expected.
- Missing data is not missing-at-random (MCAR) but systematic (e.g., below detection limit); filtering by rate alone does not address this mechanism.

## Inputs

- raw metabolomics data (wide format with metabolite columns)
- column-wise NA prevalence (proportions or counts per metabolite)

## Outputs

- filtered metabolomics data with sparse metabolite columns removed
- metadata on removed columns and their NA rates

## How to apply

After loading raw metabolomics data into R, compute the proportion of missing values (NA count / total rows) for each metabolite column. Remove any metabolite column where this proportion exceeds 10%. This column-wise filtering occurs before imputation of remaining missing values in retained columns. The rationale is that columns with >10% missing data are too sparse to impute reliably and may introduce noise; retaining only well-measured metabolites ensures the subsequent imputation step (e.g., k-nearest neighbor) operates on columns with sufficient information density. The 10% threshold balances data retention against data quality.

## Related tools

- **R** (Statistical computing environment for column-wise NA counting and filtering logic)
- **tidyverse** (Data manipulation and filtering of metabolite columns by NA proportion)
- **MeTEor** (R package integrating this filtering step as part of the preprocessing workflow) — github.com/scibiome/meteor

## Examples

```
# Load data and compute NA proportion per metabolite column
library(tidyverse)
data("raw_example_data")
na_rate <- colSums(is.na(raw_example_data)) / nrow(raw_example_data)
filtered_data <- raw_example_data[, na_rate <= 0.10]
```

## Evaluation signals

- All retained metabolite columns have ≤10% missing values; all removed columns have >10% missing values.
- The count and identity of removed columns match the NA prevalence threshold criterion.
- Dimensions of filtered data (number of rows unchanged; number of metabolite columns reduced) are consistent with the filtering rate.
- Subsequent imputation step successfully completes on the filtered dataset without errors due to sparse data.
- Comparison of statistical test results (e.g., p-value distributions, effect sizes) before/after filtering shows improved power or reduced false positives if attributable to better data density.

## Limitations

- The 10% threshold is heuristic and may not suit all metabolomics studies; some applications may require stricter (<5%) or more permissive (>15%) cutoffs depending on the analyte platform and study design.
- Filtering does not address non-random missingness mechanisms (e.g., below-detection-limit metabolites); it only removes columns by rate, potentially discarding informative rare features.
- Filtering is applied independently to each column; it does not account for correlations between metabolites or biological relevance of sparse features.

## Evidence

- [other] Remove columns with more than 10% NA: "Remove columns with more than 10% NA"
- [other] Identify metabolite columns with missing values and filter out any metabolite with >10% missing data using column-wise NA prevalence checks.: "Identify metabolite columns with missing values and filter out any metabolite with >10% missing data using column-wise NA prevalence checks."
- [other] The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor.: "The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor."
