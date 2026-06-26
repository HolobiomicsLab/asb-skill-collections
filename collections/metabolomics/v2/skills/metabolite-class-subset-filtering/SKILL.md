---
name: metabolite-class-subset-filtering
description: Use when when you have an omu_summary output dataframe with Class metadata
  and adjusted p-values (padj), and you need to focus downstream analysis (e.
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
  - R base subset / logical indexing
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

# metabolite-class-subset-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter a metabolomics summary statistics dataframe to isolate metabolites belonging to a specific compound class and meeting statistical significance thresholds (padj ≤ 0.05). This subset becomes the basis for downstream frequency counting and visualization of altered metabolites within that class.

## When to use

When you have an omu_summary output dataframe with Class metadata and adjusted p-values (padj), and you need to focus downstream analysis (e.g., pie chart visualization, fold-change counting) on a specific metabolite class — such as organic acids, fatty acids, or amino acids — that shows significant alteration (padj ≤ 0.05) in your experiment.

## When NOT to use

- Input dataframe does not contain both Class and padj columns — subsetting will fail or yield empty results.
- Your analysis goal is to examine all metabolites regardless of class or significance — filtering removes data and is unnecessary.
- The padj threshold or Class label does not match your biological question or experimental design.

## Inputs

- omu_summary output dataframe (containing metabolite names, Class metadata, padj values, log2FoldChange)

## Outputs

- Filtered dataframe (subset of omu_summary, rows matching Class and padj ≤ 0.05)

## How to apply

Load the omu_summary output dataframe containing metabolite names, Class metadata, padj values, and log2FoldChange columns. Use base R subsetting (e.g., subset() or logical indexing) to filter rows where Class matches your target (e.g., 'Organic acids') AND padj ≤ 0.05. The resulting subset preserves all column structure and is ready for input to downstream omu functions such as count_fold_changes (with column='Class' and sig_threshold=0.05) to generate frequency tables of increased vs. decreased metabolites, or ra_table to compute relative abundance percentages for visualization.

## Related tools

- **omu_summary** (Generates the input dataframe containing padj and log2FoldChange statistics for metabolites) — github.com/connor-reid-tiffany/Omu
- **count_fold_changes** (Consumes the filtered dataframe to generate frequency tables of increased vs. decreased metabolites by class) — github.com/connor-reid-tiffany/Omu
- **ra_table** (Transforms frequency data from the filtered subset into relative abundance (percentage) format for visualization) — github.com/connor-reid-tiffany/Omu
- **R base subset / logical indexing** (Core subsetting mechanism to filter rows by Class and padj criteria)

## Examples

```
filtered_organicacids <- subset(omu_summary_df, Class == 'Organic acids' & padj <= 0.05)
```

## Evaluation signals

- Verify output dataframe has fewer or equal rows than input; all retained rows have Class matching the target label and padj ≤ 0.05.
- Check that all columns from the input omu_summary output are preserved in the filtered subset (no unexpected column drops).
- Confirm the filtered dataframe is non-empty and contains at least one metabolite; if empty, the class label or threshold may not match the data distribution.
- Validate that downstream functions (count_fold_changes, ra_table, pie_chart) accept the filtered dataframe without errors and produce expected frequency/visualization outputs.
- Cross-check row counts and class labels before and after subsetting using summary() or table(subset_df$Class) to confirm filtering logic worked as intended.

## Limitations

- Subsetting is case-sensitive; Class labels must match exactly (e.g., 'Organic acids' vs. 'organic acids' will yield different subsets).
- If no metabolites meet both the Class and padj ≤ 0.05 criteria, the output is an empty dataframe, which may cause downstream functions to fail or return no visualization.
- The padj threshold (0.05) is fixed in the workflow; if your analysis requires a different significance cutoff, manual adjustment is needed.
- Filtering on Class alone does not account for biological or statistical effect size; metabolites with padj ≤ 0.05 but small log2FoldChange may not be biologically meaningful.

## Evidence

- [other] Subset the dataframe to rows where Class == 'Organic acids' and padj <= 0.05 using base R subset and indexing.: "Subset the dataframe to rows where Class == 'Organic acids' and padj <= 0.05 using base R subset and indexing."
- [other] Load the omu_summary output dataframe (containing metabolite names, Class metadata, padj values, and log2FoldChange).: "Load the omu_summary output dataframe (containing metabolite names, Class metadata, padj values, and log2FoldChange)."
- [other] Apply count_fold_changes with column='Class' and sig_threshold=0.05 to generate a frequency table counting increased vs. decreased metabolites.: "Apply count_fold_changes with column='Class' and sig_threshold=0.05 to generate a frequency table counting increased vs. decreased metabolites."
- [other] Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively: "Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively"
