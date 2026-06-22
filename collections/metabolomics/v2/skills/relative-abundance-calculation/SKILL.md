---
name: relative-abundance-calculation
description: Use when after generating a frequency count table (e.g., from count_fold_changes output showing numbers of increased vs. decreased metabolites by class) and before creating proportional visualizations (pie charts, stacked bar plots).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - R
  - count_fold_changes
  - pie_chart
  - ggplot2
  - R (base)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# relative-abundance-calculation

## Summary

Transform frequency count tables of metabolite subsets into relative abundance (percentage) data to enable proportional comparison across compound classes or fold-change categories. This is essential for pie-chart and proportional visualizations in metabolomics workflows where raw counts obscure class-level distributions.

## When to use

After generating a frequency count table (e.g., from count_fold_changes output showing numbers of increased vs. decreased metabolites by class) and before creating proportional visualizations (pie charts, stacked bar plots). Specifically when you have categorical metabolite counts stratified by a variable (e.g., Class, fold-change direction) and need to express each stratum as a percentage of the total.

## When NOT to use

- Input data is already in relative abundance or percentage format (re-normalizing will distort the data).
- Raw metabolite abundance values or normalized intensity counts are the goal; ra_table is for categorical frequency tables only, not individual sample-level metabolite intensities.

## Inputs

- frequency count dataframe (output from count_fold_changes with columns for metabolite class/category and counts of increased/decreased metabolites)

## Outputs

- relative abundance dataframe (percentage values, rows = metabolite classes/categories, columns = fold-change direction or other stratification, values = percentages summing to 100%)

## How to apply

Apply the ra_table function to a frequency dataframe generated from count_fold_changes, specifying the variable parameter to match the column used for stratification (e.g., variable='Class'). The function computes column-wise percentages, converting raw counts into relative abundances that sum to 100% within each grouping. This normalized representation allows fair visual comparison of metabolite proportions across classes regardless of absolute count magnitude, and prepares the data for downstream pie_chart or stacked visualization functions that expect ratio or percentage inputs.

## Related tools

- **count_fold_changes** (generates the frequency count table (raw counts of increased/decreased metabolites by class) that serves as input to ra_table) — github.com/connor-reid-tiffany/Omu
- **pie_chart** (consumes the relative abundance table output by ra_table to render proportional pie-chart visualizations) — github.com/connor-reid-tiffany/Omu
- **ggplot2** (underlying graphics library for rendering outputs compatible with ra_table and pie_chart workflows)
- **R (base)** (execution environment for omu package functions including ra_table)

## Examples

```
ra_table(count_fold_changes(omu_summary_output, column='Class', sig_threshold=0.05), variable='Class')
```

## Evaluation signals

- Output dataframe has the same row and column dimensions as the input frequency table (no rows/columns dropped or added).
- All values in the output are numeric percentages in the range [0, 100].
- For each column in the output, values sum to 100 (or very close, within floating-point precision ~1e-10), confirming proper normalization.
- Subsequent pie_chart rendering executes without errors and produces a plot where slice sizes correspond to the relative abundance percentages.
- Row/column ordering and metadata labels are preserved identically from input to output.

## Limitations

- ra_table operates only on frequency count dataframes; it is not designed for raw metabolite abundance matrices or intensity-normalized data.
- Percentages assume the input frequency table is complete and contains no missing values; incomplete frequency data will produce incorrect normalization.
- When frequency counts are very small (e.g., <5 metabolites per class), percentage estimates may have high uncertainty and are more suitable for descriptive visualization than statistical inference.

## Evidence

- [other] ra_table frequency data generation: "First, a frequency data frame (percentage values) must be made from the count data frame using the ```ra_table``` function"
- [other] ra_table input and usage in pie_chart workflow: "Apply count_fold_changes with column='Class' and sig_threshold=0.05 to generate a frequency table counting increased vs. decreased metabolites. Transform the frequency table to relative abundance"
- [other] ra_table output feeds downstream visualization: "This frequency data frame can be used in the ```pie_chart``` function"
