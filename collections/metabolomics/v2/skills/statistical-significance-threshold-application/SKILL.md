---
name: statistical-significance-threshold-application
description: Use when you have generated omu_summary or anova_function output (a dataframe with padj values for all tested metabolites) and need to subset compounds for class-specific frequency counting, fold-change analysis, or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - omu_summary
  - count_fold_changes
  - ra_table
  - pie_chart
  - ggplot2
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
---

# statistical-significance-threshold-application

## Summary

Apply adjusted p-value (padj) thresholds to metabolomics summary statistics to identify and isolate significantly altered metabolites for downstream analysis and visualization. This skill filters omu_summary output to retain only compounds meeting a user-defined statistical significance criterion, typically padj ≤ 0.05.

## When to use

You have generated omu_summary or anova_function output (a dataframe with padj values for all tested metabolites) and need to subset compounds for class-specific frequency counting, fold-change analysis, or visualization. Apply this skill when you want to focus downstream analyses only on metabolites that pass a predefined significance threshold (e.g., padj ≤ 0.05) rather than analyzing the full set of detected compounds.

## When NOT to use

- Your analysis goal requires analysis of all detected metabolites regardless of statistical significance (e.g., exploratory profiling of the entire detected metabolome).
- Input data lacks padj or p-value columns (e.g., raw abundance table or untested count data).
- You are performing unsupervised analysis (e.g., PCA) where filtering by significance may bias ordination.

## Inputs

- omu_summary output dataframe (or anova_function output)
- Dataframe columns: metabolite names, Class metadata, padj values, log2FoldChange

## Outputs

- Filtered dataframe (subset of rows meeting padj ≤ threshold)
- Optionally, frequency table (count_fold_changes output)
- Optionally, relative abundance table (ra_table output)
- Optionally, pie_chart or bar visualization object

## How to apply

Load the omu_summary output dataframe containing metabolite names, Class metadata, padj values, and log2FoldChange columns. Use base R subsetting (e.g., subset() or bracket indexing) to filter rows where padj ≤ 0.05 (or your chosen threshold). Optionally, further subset by compound Class (e.g., Class == 'Organic acids') to isolate metabolites of interest. Pass the filtered dataframe to downstream omu functions such as count_fold_changes (with sig_threshold=0.05), ra_table, or pie_chart to generate frequency tables and visualizations. The rationale is that filtering by adjusted p-value controls for multiple testing and ensures only statistically defensible metabolite subsets are retained for interpretation.

## Related tools

- **omu_summary** (Generates univariate statistical test output (t-test or ANOVA) containing padj values and log2FoldChange for all metabolites; output is the primary input to threshold filtering.) — github.com/connor-reid-tiffany/Omu
- **count_fold_changes** (Accepts filtered (padj-thresholded) omu_summary output and generates frequency tables counting significantly increased vs. decreased metabolites by Class.) — github.com/connor-reid-tiffany/Omu
- **ra_table** (Transforms count_fold_changes frequency output to relative abundance (percentage) format for visualization-ready input.) — github.com/connor-reid-tiffany/Omu
- **pie_chart** (Accepts ra_table output (post-threshold) to visualize frequency distribution of significantly altered metabolite classes.) — github.com/connor-reid-tiffany/Omu
- **ggplot2** (Rendering engine for omu visualization objects (pie_chart, plot_bar); figures are ggplot2 objects compatible with ggplot2 themes.)
- **R** (Language and runtime for loading, subsetting, and filtering dataframes using base R indexing and subset() function.)

## Examples

```
filtered_organic_acids <- subset(omu_summary_result, Class == 'Organic acids' & padj <= 0.05); freq_table <- count_fold_changes(filtered_organic_acids, column='Class', sig_threshold=0.05)
```

## Evaluation signals

- Row count of filtered dataframe is ≤ row count of input omu_summary output; all rows in filtered output meet padj ≤ threshold criterion.
- All padj values in filtered output are ≤ the specified threshold (e.g., 0.05); no padj values > threshold remain.
- Downstream count_fold_changes output correctly reflects only the metabolites in the filtered subset (row counts match expected number of increased/decreased compounds).
- Pie chart or bar visualization proportions sum to 100% and include only Classes represented in the filtered subset.
- Log2FoldChange values in filtered output show the expected direction and magnitude of effect (e.g., positive for upregulated, negative for downregulated metabolites).

## Limitations

- Threshold selection (e.g., padj ≤ 0.05) is user-defined and may be overly conservative or permissive depending on study design, sample size, and biological context; no guidance is provided in the article for threshold optimization.
- Filtering by padj removes compounds that may be biologically relevant but fail to meet statistical significance, potentially obscuring subtle but consistent metabolic changes.
- Class metadata must be present and correctly assigned (via assign_hierarchy) prior to filtering; missing or incorrect Class values will cause unexpected behavior in downstream functions.
- The article does not discuss multiple testing correction method or provide options for alternative p-value correction schemes beyond the default omu_summary output.

## Evidence

- [other] Subset the dataframe to rows where Class == 'Organic acids' and padj <= 0.05 using base R subset and indexing.: "Subset the dataframe to rows where Class == 'Organic acids' and padj <= 0.05 using base R subset and indexing."
- [other] Apply count_fold_changes with column='Class' and sig_threshold=0.05 to generate a frequency table counting increased vs. decreased metabolites.: "Apply count_fold_changes with column='Class' and sig_threshold=0.05 to generate a frequency table counting increased vs. decreased metabolites."
- [other] Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively: "Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively"
- [other] The figure is a ggplot2 object, so it is compatible with any ggplot2 themes: "The figure is a ggplot2 object, so it is compatible with any ggplot2 themes"
- [other] Load the omu_summary output dataframe (containing metabolite names, Class metadata, padj values, and log2FoldChange).: "Load the omu_summary output dataframe (containing metabolite names, Class metadata, padj values, and log2FoldChange)."
