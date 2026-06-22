---
name: metabolite-change-direction-categorization
description: Use when when you have omu_summary output containing log2FoldChange values and adjusted p-values (padj) for metabolites, and you need to stratify them by direction of change within a specific compound class (e.g., organic acids, amino acids) at a defined significance threshold (typically padj ≤ 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3172
  tools:
  - R
  - count_fold_changes
  - ra_table
  - omu_summary
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

# metabolite-change-direction-categorization

## Summary

Categorize significantly altered metabolites by direction of change (increased vs. decreased) and count their frequencies within compound classes. This skill enables visualization and quantification of metabolite response patterns in metabolomics experiments filtered by statistical significance thresholds.

## When to use

When you have omu_summary output containing log2FoldChange values and adjusted p-values (padj) for metabolites, and you need to stratify them by direction of change within a specific compound class (e.g., organic acids, amino acids) at a defined significance threshold (typically padj ≤ 0.05). Use this skill when preparing data for frequency-based visualizations like pie charts or bar plots that must distinguish between upregulated and downregulated metabolite subsets.

## When NOT to use

- Input lacks log2FoldChange or padj columns — direction and significance cannot be determined.
- All metabolites are already pre-filtered or aggregated — count_fold_changes requires row-level metabolite data.
- You need absolute quantification or intensity values rather than categorical direction counts — use ra_table on raw abundance tables instead.

## Inputs

- omu_summary output dataframe (metabolite names, Class metadata, padj, log2FoldChange)
- statistical significance threshold (e.g., padj ≤ 0.05)
- target compound class identifier (string)

## Outputs

- count_fold_changes frequency table (metabolite counts by direction: Increase vs. Decrease)
- ra_table relative abundance table (percentage values by direction and class)
- metadata-annotated dataframe subset (filtered by significance and class)

## How to apply

Load the omu_summary output dataframe containing metabolite names, Class metadata, padj values, and log2FoldChange columns. Subset the dataframe to rows meeting your significance criterion (e.g., padj ≤ 0.05) and target compound class (e.g., Class == 'Organic acids'). Apply the count_fold_changes function with column='Class' and sig_threshold=0.05 to generate a frequency table that counts metabolites with increased vs. decreased abundance. Transform this frequency table to relative abundance (percentage) using ra_table with variable='Class'. The sign of log2FoldChange determines direction: positive values indicate increased (upregulated) metabolites; negative values indicate decreased (downregulated) metabolites. This categorization is essential before generating pie_chart or plot_bar visualizations that require direction-stratified counts.

## Related tools

- **count_fold_changes** (Generates frequency table counting significantly increased vs. decreased metabolites within a compound class) — https://github.com/connor-reid-tiffany/Omu
- **ra_table** (Transforms count_fold_changes frequency output to relative abundance (percentage) values) — https://github.com/connor-reid-tiffany/Omu
- **omu_summary** (Produces statistical test output (t-test or ANOVA) containing padj and log2FoldChange for all metabolites) — https://github.com/connor-reid-tiffany/Omu
- **pie_chart** (Visualizes direction-stratified frequency or relative abundance counts as pie chart) — https://github.com/connor-reid-tiffany/Omu
- **ggplot2** (Rendering engine for metabolite direction and class visualizations)

## Examples

```
count_fold_changes(omu_summary_output, column='Class', sig_threshold=0.05); ra_table_output <- ra_table(count_result, variable='Class')
```

## Evaluation signals

- Frequency table rows sum to total number of significantly filtered metabolites (padj ≤ threshold) within the target class.
- Relative abundance (ra_table) rows sum to 100% across increase and decrease categories.
- log2FoldChange sign consistency: all Increase category metabolites have positive log2FoldChange; all Decrease category metabolites have negative log2FoldChange.
- No metabolites appear in both Increase and Decrease categories (mutually exclusive partition).
- Pie chart or bar plot correctly reflects direction-stratified counts and visually represents the proportion of up- vs. down-regulated metabolites.

## Limitations

- Requires pre-computed statistical test results (omu_summary or omu_anova output); cannot categorize raw abundance data without p-values.
- Binary categorization (Increase/Decrease) discards magnitude information; log2FoldChange values are lost in frequency counts.
- Direction assignment depends critically on correct sign convention for log2FoldChange (positive = upregulated); non-standard fold-change encodings will produce inverted categorization.
- Statistical power to detect direction depends on sample size and effect magnitude; low-abundance metabolites may be filtered out by padj threshold before categorization.

## Evidence

- [other] count_fold_changes workflow step: "Apply count_fold_changes with column='Class' and sig_threshold=0.05 to generate a frequency table counting increased vs. decreased metabolites"
- [other] ra_table transformation rationale: "Transform the frequency table to relative abundance (percentage) using ra_table with variable='Class'"
- [other] count_fold_changes function definition: "This can be done using the output from ```omu_summary``` as an input for the function ```count_fold_changes```, to make a data frame with the number of compounds that significantly increased or"
- [other] ra_table function definition: "First, a frequency data frame (percentage values) must be made from the count data frame using the ```ra_table``` function"
- [other] Subset by significance and class: "Subset the dataframe to rows where Class == 'Organic acids' and padj <= 0.05 using base R subset and indexing"
