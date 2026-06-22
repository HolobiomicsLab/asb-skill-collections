---
name: metabolite-count-normalization-and-transformation
description: Use when you have a raw metabolite count data frame (e.g., c57_nos2KO_mouse_countDF) and need to prepare it for univariate statistical testing (e.g., omu_summary with log_transform=TRUE), multivariate analysis (e.g., PCA), or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - omu (omu_summary function)
  - assign_hierarchy
  - omu
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

# metabolite-count-normalization-and-transformation

## Summary

Normalize and transform metabolite abundance counts in a data frame to prepare them for statistical testing or visualization. This skill applies column-wise (sample) or row-wise (metabolite) transformations such as log transformation, mean-centering, Pareto scaling, or relative abundance conversion to meet assumptions of downstream analyses.

## When to use

Apply this skill when you have a raw metabolite count data frame (e.g., c57_nos2KO_mouse_countDF) and need to prepare it for univariate statistical testing (e.g., omu_summary with log_transform=TRUE), multivariate analysis (e.g., PCA), or visualization. Use it when raw counts violate distributional assumptions (e.g., non-normality, heteroscedasticity) or when you need to standardize abundance values across samples or metabolites for fair comparison.

## When NOT to use

- Input is already a statistical output (e.g., padj, log2FoldChange columns from omu_summary). Transform raw counts before statistical testing, not after.
- Data contains negative or zero values and you intend to apply log transformation without pseudocount offset (log1p handles zeros; plain log does not).
- Relative abundance conversion is applied when you need to preserve absolute abundance differences for effect-size estimation or when samples differ substantially in sequencing depth and you need depth-normalized comparisons.

## Inputs

- metabolite count data frame (e.g., c57_nos2KO_mouse_countDF) with metabolites as rows and samples as columns
- numeric transformation function (e.g., log2, log1p, or user-defined scaling function)

## Outputs

- transformed metabolite count data frame with same row and column structure but updated numeric values
- relative abundance table (ra_table output) with percentage or frequency values suitable for visualization

## How to apply

Use the omu package functions `transform_samples` (column-wise) or `transform_metabolites` (row-wise) to apply a user-supplied transformation function to the count data frame. For sample-level transformations, supply a function such as `log2` or `log1p` to normalize count distributions across samples. For metabolite-level transformations, supply functions like mean-centering or Pareto scaling to standardize abundance profiles across metabolites. Alternatively, use the `ra_table` function to convert raw counts to relative abundance (percentage values) before visualization (e.g., pie_chart, plot_bar). The choice of transformation depends on downstream analysis: log transformation is critical for t-tests or ANOVA via omu_summary; relative abundance is suitable for compositional visualization; Pareto or mean-centering supports PCA. Verify the transformed output has the expected column names, row names, and numeric ranges before passing it to statistical or plotting functions.

## Related tools

- **omu** (Provides transform_samples and transform_metabolites functions for column-wise and row-wise transformations, and ra_table for relative abundance conversion) — github.com/connor-reid-tiffany/Omu
- **R** (Programming environment for executing transformation functions and data frame operations)

## Examples

```
transform_samples(c57_nos2KO_mouse_countDF, function(x) log2(x + 1)); ra_table(c57_nos2KO_mouse_countDF) %>% pie_chart()
```

## Evaluation signals

- Output data frame has identical row and column names to input, confirming no samples or metabolites were dropped.
- Output numeric values fall within expected ranges: log-transformed counts are typically 0–15; relative abundance values sum to 100% per sample; mean-centered values cluster near zero with both positive and negative values.
- Downstream statistical tests (omu_summary) or visualizations (plot_bar, PCA_plot) execute without error and produce results consistent with the transformation intent (e.g., log-transformed data satisfies t-test normality assumptions better than raw counts).
- Transformed data matches the input data structure: same number of metabolites (rows) and samples (columns) as the raw count data frame.

## Limitations

- Log transformation of counts with zeros requires pseudocount offset (log1p) to avoid undefined values; plain log will fail.
- Pareto scaling and mean-centering assume metabolite-level standardization; they alter absolute abundance information and may reduce effect sizes in downstream tests.
- Relative abundance transformation (ra_table) removes information about absolute metabolite counts and total sample sequencing depth, making it unsuitable for differential abundance testing; use only for exploratory visualization.
- No automatic guidance is provided on which transformation to select; the choice depends on downstream analysis (statistical test assumptions, visualization type, effect-size preservation).

## Evidence

- [other] transform_samples and transform_metabolites rationale: "```transform_samples``` will perform column-wise transformations across the datausing the supplied function. This is useful for operations such as log transformation, or transforming by the square"
- [other] transform_metabolites for row-wise scaling: "```transform metabolites``` transforms the data using the supplied function across rows. This is useful for operations like mean-centering and pareto scaling"
- [other] ra_table for relative abundance conversion: "First, a frequency data frame (percentage values) must be made from the count data frame using the ```ra_table``` function"
- [other] log_transform parameter in omu_summary: "Call omu_summary with count_data, metadata, numerator='Strep', denominator='Mock', Factor='Treatment', response_variable='Metabolite', log_transform=TRUE, p_adjust='BH', and test_type='welch' to"
- [other] Statistical testing support context: "Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively"
