---
name: univariate-statistical-testing-for-metabolomics
description: Use when you have paired metabolomics count data (metabolite abundance matrix) and sample metadata with categorical treatment or experimental factor assignments, and you need to test for statistically significant differences in individual metabolite abundances between exactly two groups (t-test) or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - R
  - omu (omu_summary function)
  - assign_hierarchy
  - omu_summary
  - omu_anova
  - count_fold_changes
  - transform_samples
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# univariate-statistical-testing-for-metabolomics

## Summary

Apply univariate statistical tests (t-test or ANOVA) to metabolomics count data to quantify differences in metabolite abundance between treatment groups, producing effect sizes, p-values, and adjusted significance thresholds. This skill generates interpretable statistics tables for hypothesis-driven metabolomics comparisons.

## When to use

You have paired metabolomics count data (metabolite abundance matrix) and sample metadata with categorical treatment or experimental factor assignments, and you need to test for statistically significant differences in individual metabolite abundances between exactly two groups (t-test) or among multiple groups within a single factor (ANOVA). Use this when your research question targets univariate associations rather than multivariate patterns.

## When NOT to use

- Input count data lacks a clear grouping factor or metadata (univariate tests require group labels)
- You seek multivariate patterns or dimensionality reduction (use PCA_plot or random_forest instead)
- Count data are already normalized or transformed by an external pipeline incompatible with omu's log-transformation step
- Sample size is extremely small (<3 per group) and you lack biological or technical replicates to estimate variance

## Inputs

- metabolomics count data frame (metabolites × samples, numeric abundance values)
- sample metadata data frame (rows = samples, columns = factors including Sample name and experimental Factor)
- optional: hierarchical class annotation (KEGG identifiers, KO numbers, or taxon assignments)

## Outputs

- statistics data frame with rows for each metabolite and columns: padj (adjusted p-value), log2FoldChange, standard error, standard deviation, test statistic, raw p-value
- optional: fold-change summary table via count_fold_changes (number of significantly increased/decreased metabolites)

## How to apply

Load count data and metadata into R using read.metabo or read.csv, ensuring the metadata includes a Sample column and a column for your Factor of interest. Optionally assign hierarchical taxonomic or functional class data using assign_hierarchy with identifier='KEGG', 'KO_Number', 'Prokaryote', or 'Eukaryote'. Call omu_summary (for t-test comparisons) or omu_anova (for multi-group ANOVA) with count_data, metadata, specifying numerator and denominator groups (for t-test), Factor name, response_variable='Metabolite', and set log_transform=TRUE to normalize skewed metabolite distributions. Choose p_adjust='BH' (Benjamini–Hochberg) for multiple-testing correction and test_type='welch' (Welch's t-test) to account for unequal variances. Verify the output data frame contains columns for padj (adjusted p-value), log2FoldChange, standard error, and standard deviation before downstream interpretation.

## Related tools

- **omu_summary** (Performs univariate t-test statistical testing on metabolomics count data, computing log2FoldChange, p-values, and adjusted significance thresholds between two treatment groups) — github.com/connor-reid-tiffany/Omu
- **omu_anova** (Alternative univariate test for measuring variance and significance of metabolite abundance across all groups within a single factor (ANOVA generalization of t-test)) — github.com/connor-reid-tiffany/Omu
- **assign_hierarchy** (Annotates count data rows with hierarchical functional or taxonomic classification (KEGG, KO_Number, Prokaryote, Eukaryote) to enable post-hoc functional interpretation of significant metabolites) — github.com/connor-reid-tiffany/Omu
- **count_fold_changes** (Summarizes omu_summary output into contingency tables (number of metabolites with significant fold-change increases/decreases per factor)) — github.com/connor-reid-tiffany/Omu
- **transform_samples** (Applies column-wise transformations (e.g., log transformation, square root) across samples prior to or within omu_summary to normalize skewed metabolite distributions) — github.com/connor-reid-tiffany/Omu
- **R** (Host language and runtime environment for omu package and statistical functions)

## Examples

```
omu_summary(count_data = c57_nos2KO_mouse_countDF, metadata = c57_nos2KO_mouse_metadata, numerator = 'Strep', denominator = 'Mock', Factor = 'Treatment', response_variable = 'Metabolite', log_transform = TRUE, p_adjust = 'BH', test_type = 'welch')
```

## Evaluation signals

- Output data frame has one row per metabolite and columns for log2FoldChange, padj, standard error, and standard deviation with no missing values
- padj column contains only values in [0, 1] and padj ≥ p-value (raw) for all rows, confirming multiple-testing correction was applied
- Number of metabolites with padj < 0.05 is reasonable relative to total metabolite count and prior biological expectation (not zero or near 100%)
- log2FoldChange values are symmetric around zero if control and treatment groups have similar distributions (sanity check for directionality)
- Standard error values are non-negative and scale inversely with sample size per group (larger n → smaller SE)

## Limitations

- Univariate tests ignore correlations and co-abundance patterns among metabolites; multivariate methods (PCA, random forest) may be more powerful for some discoveries
- Multiple-testing correction (BH or Bonferroni) becomes conservative with very large metabolite panels (>1000), potentially masking real signals
- Log-transformation assumes metabolite abundances are approximately lognormal; heavily zero-inflated or bimodal distributions may violate test assumptions
- Welch's t-test and ANOVA assume approximate normality after transformation; non-parametric alternatives (Mann–Whitney U, Kruskal–Wallis) are not mentioned in omu but may be preferable for small n or severe non-normality
- Statistical significance (padj < 0.05) does not imply biological or clinical significance; effect size (log2FoldChange) and biological context must be considered

## Evidence

- [other] Omu supports two univariate statistical models, t test and anova, using the functions omu_summary and anova_function respectively: "Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively"
- [other] Call omu_summary with count_data, metadata, numerator='Strep', denominator='Mock', Factor='Treatment', response_variable='Metabolite', log_transform=TRUE, p_adjust='BH', and test_type='welch' to compute statistics. Verify the output data frame contains columns for padj, log2FoldChange, standard error, and standard deviation.: "Call omu_summary with count_data, metadata, numerator='Strep', denominator='Mock', Factor='Treatment', response_variable='Metabolite', log_transform=TRUE, p_adjust='BH', and test_type='welch' to"
- [other] To assign hierarchical class data, use the assign_hierarchy function and pick the correct identifier, either KEGG, KO_Number, Prokaryote, or Eukaryote: "To assign hierarchical class data, use the ```assign_hierarchy``` function and pick the correct identifier, either "KEGG", "KO_Number", "Prokaryote", or "Eukaryote""
- [other] An alternative option to omu_summary is the omu_anova, which can be used to measure the variance of all groups within a factor: "An alternative option to ```omu_summary``` is the ```omu_anova```, which can be used to measure the variance of all groups within a factor"
- [other] For end users metabolomics data, it is recommended to use the read.metabo function to load it into R: "For end users metabolomics data, it is recommended to use the ```read.metabo``` function to load it into R"
- [other] Included with Omu is an example metabolomics dataset of data from fecal samples collected from a two factor experiment with wild type c57B6J mice and c57B6J mice with a knocked out nos2 gene: "Included with Omu is an example metabolomics dataset of data from fecal samples collected from a two factor experiment with wild type c57B6J mice and c57B6J mice with a knocked out nos2 gene"
