---
name: metabolite-overdispersion-correction
description: Use when working with untransformed metabolomics count data (e.g., c57_nos2KO_mouse_countDF)
  that will be input to variance-sensitive methods such as random forest classification
  or univariate statistical tests.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - transform_samples
  - random_forest
  - randomForest
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1128/mra.00129-19
  title: omu metabolomics count data tool
evidence_spans:
- Omu is an R package that enables rapid analysis of Metabolomics data sets
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omu_metabolomics_count_data_tool_cq
    doi: 10.1128/mra.00129-19
    title: omu metabolomics count data tool
  dedup_kept_from: coll_omu_metabolomics_count_data_tool_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00129-19
  all_source_dois:
  - 10.1128/mra.00129-19
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-overdispersion-correction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Log-transform metabolomics count data column-wise to stabilize variance and address overdispersion before applying statistical or machine-learning methods. This preprocessing step is particularly useful when count data exhibits heteroscedasticity that could bias downstream analyses.

## When to use

Apply this skill when working with untransformed metabolomics count data (e.g., c57_nos2KO_mouse_countDF) that will be input to variance-sensitive methods such as random forest classification or univariate statistical tests. Overdispersion—where variance increases with the mean—is common in metabolomics count data and can inflate type I error rates or distort variable importance estimates if left uncorrected.

## When NOT to use

- Data is already normalized or log-transformed (e.g., TPM, RPKM, or other variance-stabilizing transformation already applied).
- Analytical method is robust to heteroscedasticity (e.g., non-parametric tests, median-based statistics).
- Count data contains zeros or near-zero values that cannot be meaningfully log-transformed without pseudocount addition (use with caution; the article does not discuss pseudocount handling).

## Inputs

- metabolomics count data frame (e.g., c57_nos2KO_mouse_countDF)
- row labels: metabolites; column labels: samples

## Outputs

- log-transformed count data frame (same shape as input)
- column-wise natural log of each count value

## How to apply

Use the transform_samples function from Omu, specifying the natural log function as the transformation operator to be applied column-wise (i.e., across samples) to the count data frame. This stabilizes variance across the range of metabolite abundances. Log transformation is optional but recommended before invoking the random_forest wrapper or other statistical methods that assume homogeneity of variance. The choice of natural log (versus, e.g., square-root or Tukey's ladder of powers) should be justified by exploratory plots of mean vs. variance before and after transformation.

## Related tools

- **transform_samples** (Omu function that performs column-wise transformations (e.g., natural log) on metabolomics count data to address overdispersion) — github.com/connor-reid-tiffany/Omu
- **random_forest** (Omu wrapper around randomForest package; downstream consumer of log-transformed count data) — github.com/connor-reid-tiffany/Omu
- **randomForest** (R package that benefits from variance-stabilized input data; called internally by Omu's random_forest wrapper)

## Examples

```
transformed_data <- transform_samples(c57_nos2KO_mouse_countDF, log)
```

## Evaluation signals

- Output data frame has identical dimensions (rows, columns) to input; no samples or metabolites are dropped.
- All output values are ≤ input values (log transformation is monotonically increasing and compresses the scale).
- Variance-vs-mean plot of log-transformed data shows reduced heteroscedasticity compared to untransformed data (visual check).
- Subsequent random_forest or statistical test results are stable and interpretable; variable importance rankings are not dominated by high-abundance metabolites due to inflated variance.
- No NaN or Inf values introduced (potential issue if zeros or negative counts exist in input; check for warning messages from log function).

## Limitations

- Natural log transformation is undefined for zero or negative values; the article does not document pseudocount strategies. Count data with excess zeros may require alternative transformations (e.g., centered log-ratio or compositional data methods).
- Log transformation assumes multiplicative errors; if errors are additive, alternative variance-stabilizing transformations (e.g., square root, Tukey ladder) may be more appropriate.
- Transformation is applied uniformly to all samples; if subgroups (e.g., treatment vs. control) have substantially different variance structures, consider group-specific transformations or weighted methods.

## Evidence

- [other] transform_samples recommendation: "Optionally log-transform the count data column-wise using transform_samples with the natural log function to address overdispersion."
- [other] transform_samples function description: "```transform_samples``` will perform column-wise transformations across the data using the supplied function. This is useful for operations such as log transformation, or transforming by the square"
- [other] overdispersion context: "Included with Omu is an example metabolomics dataset of data from fecal samples collected from a two factor experiment with wild type c57B6J mice and c57B6J mice with a knocked out nos2 gene"
