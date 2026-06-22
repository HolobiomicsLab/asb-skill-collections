---
name: fold-change-frequency-aggregation
description: Use when after performing univariate statistical testing (t-test or ANOVA via omu_summary or omu_anova) on metabolomics count data, use this skill when you need to summarize how many metabolites in each class showed significant increase or decrease (padj ≤ 0.05).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - R
  - count_fold_changes
  - omu_summary
  - omu_anova
  - ra_table
  - pie_chart
  - plot_bar
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

# fold-change-frequency-aggregation

## Summary

Aggregate fold-change results from univariate statistical testing into frequency counts of increased vs. decreased metabolites, stratified by compound class or other hierarchical metadata. This enables compact summary tables and downstream visualization of the direction and magnitude of metabolic shifts.

## When to use

After performing univariate statistical testing (t-test or ANOVA via omu_summary or omu_anova) on metabolomics count data, use this skill when you need to summarize how many metabolites in each class showed significant increase or decrease (padj ≤ 0.05). This is essential before generating pie charts, bar plots, or ratio tables to communicate the prevalence of directional metabolic changes across compound classes.

## When NOT to use

- Input is already a pre-aggregated frequency or count table; skip directly to ra_table or visualization.
- Statistical testing has not been performed or padj values are not available; run omu_summary or omu_anova first.
- You need per-metabolite-level results rather than class-level summaries; use the raw omu_summary output instead.

## Inputs

- omu_summary output dataframe (metabolite names, Class metadata, padj, log2FoldChange)
- Grouping variable (e.g., 'Class', 'Pathway', or other hierarchical metadata column)

## Outputs

- Frequency dataframe (counts of increased/decreased metabolites per class)
- Relative abundance table (percentage values per class and direction)

## How to apply

Load the omu_summary output dataframe containing metabolite names, Class metadata, padj values, and log2FoldChange columns. Apply the count_fold_changes function with column='Class' (or other grouping metadata) and sig_threshold=0.05 to generate a frequency table that counts the number of metabolites per class that increased or decreased. The function uses the log2FoldChange sign to determine direction and padj to filter for statistical significance. The resulting frequency dataframe serves as input to ra_table (to convert counts to relative abundance percentages) or directly to pie_chart and plot_bar for visualization.

## Related tools

- **count_fold_changes** (Aggregates omu_summary results into frequency counts of increased vs. decreased metabolites per class) — github.com/connor-reid-tiffany/Omu
- **omu_summary** (Performs univariate statistical testing (t-test) to generate padj and log2FoldChange; output feeds into count_fold_changes) — github.com/connor-reid-tiffany/Omu
- **omu_anova** (Alternative univariate statistical model; output feeds into count_fold_changes) — github.com/connor-reid-tiffany/Omu
- **ra_table** (Transforms frequency counts into relative abundance (percentage) for normalized comparison across classes) — github.com/connor-reid-tiffany/Omu
- **pie_chart** (Visualizes relative abundance of increased/decreased metabolites from ra_table output) — github.com/connor-reid-tiffany/Omu
- **plot_bar** (Alternative visualization for frequency counts stratified by class metadata) — github.com/connor-reid-tiffany/Omu
- **R** (Runtime environment and base indexing/subsetting for filtering by Class and padj threshold)

## Examples

```
count_fold_changes(omu_summary_result, column='Class', sig_threshold=0.05); ra_table(fold_change_freq, variable='Class'); pie_chart(ra_freq_table, variable='Class', column='Decrease', color='black')
```

## Evaluation signals

- Frequency table has correct number of rows equal to unique values in grouping column (e.g., number of metabolite classes).
- Each row contains non-negative integer counts for 'Increase' and 'Decrease' columns; sum of counts per class matches number of significant metabolites in that class.
- Downstream ra_table output sums to 100% (or close, accounting for rounding) within each class.
- Pie chart or bar plot generated from frequency/relative abundance table displays expected proportions without missing or infinite values.
- Subsetting logic correctly excludes metabolites with padj > 0.05; row count of filtered results is ≤ original omu_summary output.

## Limitations

- Requires a valid padj column and log2FoldChange sign from upstream statistical testing; missing or malformed values will cause errors.
- Grouping by 'Class' assumes metabolites have been annotated with hierarchical class data via assign_hierarchy; unannotated metabolites may be excluded or placed in NA categories.
- Binary classification (increase/decrease) does not capture effect size magnitude; metabolites with very small log2FoldChange may appear in counts but have minimal biological relevance.
- Single significance threshold (padj ≤ 0.05) is fixed; alternative thresholds require manual subsetting before applying count_fold_changes.

## Evidence

- [other] Apply count_fold_changes with column='Class' and sig_threshold=0.05 to generate a frequency table counting increased vs. decreased metabolites.: "Apply count_fold_changes with column='Class' and sig_threshold=0.05 to generate a frequency table counting increased vs. decreased metabolites."
- [other] This can be done using the output from omu_summary as an input for the function count_fold_changes, to make a data frame with the number of compounds that significantly increased or [decreased].: "This can be done using the output from ```omu_summary``` as an input for the function ```count_fold_changes```, to make a data frame with the number of compounds that significantly increased or"
- [other] First, a frequency data frame (percentage values) must be made from the count data frame using the ra_table function.: "First, a frequency data frame (percentage values) must be made from the count data frame using the ```ra_table``` function"
- [other] This frequency data frame can be used in the pie_chart function.: "This frequency data frame can be used in the ```pie_chart``` function"
- [other] Omu supports two univariate statistical models, t test and anova, using the functions omu_summary and anova_function respectively.: "Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively"
