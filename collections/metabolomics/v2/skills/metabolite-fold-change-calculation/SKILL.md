---
name: metabolite-fold-change-calculation
description: Use when you have paired count data and metadata from a two-group metabolomics experiment (e.g., Strep vs Mock treatment) and need to identify which metabolites show significant abundance shifts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - R
  - omu (omu_summary function)
  - assign_hierarchy
  - omu_summary
  - read.metabo
  - count_fold_changes
derived_from:
- doi: 10.1128/mra.00129-19
  title: omu metabolomics count data tool
evidence_spans:
- Omu is an R package that enables rapid analysis of Metabolomics data sets
- Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively
- To assign hierarchical class data, use the ```assign_hierarchy``` function and pick the correct identifier, either "KEGG", "KO_Number", "Prokaryote", or "Eukaryote"
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
---

# metabolite-fold-change-calculation

## Summary

Calculate log2 fold changes and statistical measures (p-values, adjusted p-values, standard error, standard deviation) for metabolites across treatment groups in metabolomics datasets. This skill quantifies the magnitude and significance of metabolite abundance differences between experimental conditions.

## When to use

Apply this skill when you have paired count data and metadata from a two-group metabolomics experiment (e.g., Strep vs Mock treatment) and need to identify which metabolites show significant abundance shifts. Use it after loading count matrices and metadata but before visualization or pathway enrichment analysis.

## When NOT to use

- Input count data is already log-transformed or normalized to relative abundance without access to raw counts; log_transform=TRUE will distort the fold-change calculation.
- Experimental design has >2 treatment groups; use omu_anova instead to model variance across all groups within the factor.
- Metadata lacks a clear binary grouping or Factor column is missing or contains >2 unique values for the comparison.

## Inputs

- count data frame (metabolite abundances × samples, numeric matrix or data.frame)
- metadata data frame (samples × factors, with 'Sample' column and factor columns)
- factor name (string, e.g., 'Treatment')
- numerator group label (string, e.g., 'Strep')
- denominator group label (string, e.g., 'Mock')

## Outputs

- statistics data frame (metabolites × columns: padj, log2FoldChange, standard error, standard deviation, and optional hierarchical metadata)
- log2FoldChange values (numeric vector, positive = increased in numerator group)
- adjusted p-values (numeric vector, BH-corrected)

## How to apply

Load the metabolomics count data frame and corresponding metadata using read.metabo or read.csv. Optionally assign hierarchical metabolite classification (KEGG, KO_Number, Prokaryote, or Eukaryote identifiers) using assign_hierarchy to enrich the output. Call omu_summary with the count_data, metadata, specifying numerator and denominator groups (e.g., numerator='Strep', denominator='Mock'), the Factor column name (e.g., Factor='Treatment'), response_variable='Metabolite', and test parameters including log_transform=TRUE for log-scale fold changes, p_adjust='BH' for Benjamini-Hochberg multiple testing correction, and test_type='welch' for the t-test variant. The function returns a statistics data frame with log2FoldChange, adjusted p-value (padj), standard error, and standard deviation for each metabolite, enabling ranking by effect size and significance.

## Related tools

- **omu_summary** (Primary function that performs univariate t-test or Welch's t-test on log-transformed metabolite abundances and outputs fold changes and p-values) — github.com/connor-reid-tiffany/Omu
- **assign_hierarchy** (Optionally annotates metabolites with hierarchical classification (KEGG, KO_Number, Prokaryote, Eukaryote) prior to fold-change calculation to enable downstream pathway analysis) — github.com/connor-reid-tiffany/Omu
- **read.metabo** (Wrapper function for loading metabolomics count data and ensuring proper class structure before fold-change analysis) — github.com/connor-reid-tiffany/Omu
- **count_fold_changes** (Post-processing function that consumes omu_summary output to summarize the number of metabolites with significant up- or down-regulation) — github.com/connor-reid-tiffany/Omu
- **R** (Language and runtime environment for executing omu functions and statistical tests)

## Examples

```
omu_summary(count_data=c57_nos2KO_mouse_countDF, metadata=c57_nos2KO_mouse_metadata, numerator='Strep', denominator='Mock', Factor='Treatment', response_variable='Metabolite', log_transform=TRUE, p_adjust='BH', test_type='welch')
```

## Evaluation signals

- Output data frame contains one row per metabolite with non-null values in padj, log2FoldChange, standard error, and standard deviation columns.
- log2FoldChange values are symmetrical around zero (e.g., log2FC=2.0 for up-regulation, log2FC=-2.0 for down-regulation), confirming correct directionality relative to numerator/denominator specification.
- Adjusted p-values (padj) are monotonically increasing when sorted by unadjusted p-value, and all padj ≥ unadjusted p-value, confirming BH correction was applied.
- Standard deviation and standard error are non-negative and SE ≤ SD for all metabolites, confirming valid statistical calculation.
- Metabolites with padj < 0.05 show visible clustering in a volcano plot (log2FC vs -log10(padj)), separating significant from non-significant results.

## Limitations

- omu_summary assumes normally distributed metabolite abundances (or log-normality when log_transform=TRUE); severe departures may inflate type I/II error.
- Welch's t-test requires independent samples within each group; paired designs or repeated measures require alternative analysis (not mentioned in article).
- Multiple testing correction (BH) is conservative for small sample sizes (n < 10 per group); power to detect true fold changes decreases.
- Fold-change magnitude alone does not reflect biological importance; metabolites with low absolute abundance may show large fold changes due to variance in small numbers.
- The function does not automatically filter low-abundance metabolites; practitioners should pre-filter or interpret results from rare metabolites cautiously.

## Evidence

- [other] Call omu_summary with count_data, metadata, numerator='Strep', denominator='Mock', Factor='Treatment', response_variable='Metabolite', log_transform=TRUE, p_adjust='BH', and test_type='welch' to compute statistics.: "Call omu_summary with count_data, metadata, numerator='Strep', denominator='Mock', Factor='Treatment', response_variable='Metabolite', log_transform=TRUE, p_adjust='BH', and test_type='welch'"
- [other] Verify the output data frame contains columns for padj, log2FoldChange, standard error, and standard deviation.: "Verify the output data frame contains columns for padj, log2FoldChange, standard error, and standard deviation"
- [other] Omu supports two univariate statistical models, t test and anova, using the functions omu_summary and anova_function respectively: "Omu supports two univariate statistical models, t test and anova, using the functions omu_summary and anova_function respectively"
- [other] An alternative option to omu_summary is the omu_anova, which can be used to measure the variance of all groups within a factor: "An alternative option to omu_summary is the omu_anova, which can be used to measure the variance of all groups within a factor"
- [other] This can be done using the output from omu_summary as an input for the function count_fold_changes, to make a data frame with the number of compounds that significantly increased or: "the output from omu_summary as an input for the function count_fold_changes"
