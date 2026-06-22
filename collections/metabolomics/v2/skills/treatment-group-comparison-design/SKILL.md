---
name: treatment-group-comparison-design
description: Use when you have paired metabolomics count data and metadata with at least two treatment groups (e.g., Strep vs Mock), a clear Factor column identifying group membership, and a research question about which metabolites differ significantly in abundance between treatments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - omu (omu_summary function)
  - assign_hierarchy
  - omu_summary
  - read.metabo
  - omu_anova
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00129-19
  all_source_dois:
  - 10.1128/mra.00129-19
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# treatment-group-comparison-design

## Summary

Design and execute univariate statistical comparisons between treatment groups in metabolomics count data using the omu package. This skill applies t-tests or Welch's test to identify metabolites with significant abundance differences across experimental conditions.

## When to use

Apply this skill when you have paired metabolomics count data and metadata with at least two treatment groups (e.g., Strep vs Mock), a clear Factor column identifying group membership, and a research question about which metabolites differ significantly in abundance between treatments. The omu_summary function is appropriate for two-group comparisons; use omu_anova instead if you have >2 groups within a single Factor.

## When NOT to use

- Input is already a statistics table or pre-filtered feature set — omu_summary requires raw count data
- You have >2 treatment groups and wish to test all pairwise or omnibus differences — use omu_anova for multi-group Factor analysis
- Metadata lacks a clearly labeled Factor column mapping samples to treatment groups

## Inputs

- count_data: metabolomics abundance matrix (rows=metabolites, columns=samples)
- metadata: data frame with Sample column and Factor column(s) indicating group membership
- numerator: character string naming the treatment group
- denominator: character string naming the reference/control group

## Outputs

- statistics data frame with columns: padj, log2FoldChange, standard_error, standard_deviation
- one row per metabolite tested

## How to apply

Load count data (e.g., c57_nos2KO_mouse_countDF) and metadata (with Sample column and Factor columns) into R using read.metabo or read.csv. Optionally assign hierarchical metabolite class data using assign_hierarchy with identifier='KEGG'. Call omu_summary with parameters: count_data, metadata, numerator (treatment group name), denominator (control/reference group), Factor (metadata column name), response_variable='Metabolite', log_transform=TRUE for normalized abundances, p_adjust='BH' for multiple-testing correction, and test_type='welch' for unequal-variance t-tests. The function returns a statistics data frame with padj, log2FoldChange, standard error, and standard deviation columns. Verify that output contains no missing values in statistical columns and that p-adjusted values are bounded [0,1].

## Related tools

- **omu_summary** (Univariate statistical testing function that performs t-tests or Welch's tests between two treatment groups and returns padj, log2FoldChange, and standard error columns) — https://github.com/connor-reid-tiffany/Omu
- **assign_hierarchy** (Assigns hierarchical metabolite classification (KEGG, KO_Number, Prokaryote, or Eukaryote) to count data frame prior to statistical testing) — https://github.com/connor-reid-tiffany/Omu
- **read.metabo** (Wrapper around read.csv that ensures metabolomics data has proper R class structure for input to omu functions) — https://github.com/connor-reid-tiffany/Omu
- **omu_anova** (Alternative statistical testing function for >2 treatment groups within a single Factor; measures variance across all groups) — https://github.com/connor-reid-tiffany/Omu

## Examples

```
omu_summary(count_data=c57_nos2KO_mouse_countDF, metadata=c57_nos2KO_mouse_metadata, numerator='Strep', denominator='Mock', Factor='Treatment', response_variable='Metabolite', log_transform=TRUE, p_adjust='BH', test_type='welch')
```

## Evaluation signals

- Output data frame has exactly one row per input metabolite and four statistical columns (padj, log2FoldChange, standard_error, standard_deviation)
- All p-adjusted values are in the valid range [0, 1] with no NAs in statistical columns
- log2FoldChange sign is consistent with numerator/denominator direction (positive if numerator > denominator on log2 scale)
- Benjamini–Hochberg adjusted p-values are ≥ unadjusted p-values (monotonicity check)
- Metabolites ranked by padj and log2FoldChange match domain expectation (known biomarkers of treatment should appear in top hits)

## Limitations

- omu_summary is designed for two-group comparisons; multi-group Factor analysis requires omu_anova
- The function assumes count data are compositional; log_transform=TRUE is recommended but practitioners must ensure this is appropriate for their platform and preprocessing
- No explicit support for paired/longitudinal designs; samples are treated as independent
- P-value adjustment methods are limited to those available in R; 'BH' is the recommended default but other methods are not documented in the article

## Evidence

- [other] Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively: "Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively"
- [other] Call omu_summary with count_data, metadata, numerator='Strep', denominator='Mock', Factor='Treatment', response_variable='Metabolite', log_transform=TRUE, p_adjust='BH', and test_type='welch' to compute statistics.: "Call omu_summary with count_data, metadata, numerator='Strep', denominator='Mock', Factor='Treatment', response_variable='Metabolite', log_transform=TRUE, p_adjust='BH', and test_type='welch' to"
- [other] Verify the output data frame contains columns for padj, log2FoldChange, standard error, and standard deviation.: "Verify the output data frame contains columns for padj, log2FoldChange, standard error, and standard deviation"
- [other] To assign hierarchical class data, use the ```assign_hierarchy``` function and pick the correct identifier, either 'KEGG', 'KO_Number', 'Prokaryote', or 'Eukaryote': "To assign hierarchical class data, use the ```assign_hierarchy``` function and pick the correct identifier, either "KEGG", "KO_Number", "Prokaryote", or "Eukaryote""
- [other] An alternative option to ```omu_summary``` is the ```omu_anova```, which can be used to measure the variance of all groups within a factor: "An alternative option to ```omu_summary``` is the ```omu_anova```, which can be used to measure the variance of all groups within a factor"
