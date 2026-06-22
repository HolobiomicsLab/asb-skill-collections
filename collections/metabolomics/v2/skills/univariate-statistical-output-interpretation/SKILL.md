---
name: univariate-statistical-output-interpretation
description: Use when after running omu_summary (t-test) or omu_anova (ANOVA) on metabolomics count data with a defined contrast (e.g., numerator vs. denominator treatment levels), when you need to filter and visualize metabolites by statistical significance and effect size.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - R
  - omu_summary
  - omu_anova
  - plot_volcano
  - count_fold_changes
  - assign_hierarchy
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

# univariate-statistical-output-interpretation

## Summary

Interpret log2 fold-change and adjusted p-value outputs from univariate statistical tests (t-test or ANOVA) to identify metabolites with significant differential abundance between treatment groups. This skill enables extraction of biologically meaningful signals from metabolomics comparison outputs for downstream visualization and functional annotation.

## When to use

After running omu_summary (t-test) or omu_anova (ANOVA) on metabolomics count data with a defined contrast (e.g., numerator vs. denominator treatment levels), when you need to filter and visualize metabolites by statistical significance and effect size. Specifically useful when the output includes log2FoldChange values and adjusted p-values (e.g., BH-corrected), and you aim to subset metabolites meeting joint criteria (e.g., |log2FC| > threshold AND padj < 0.05) for volcano plots or ranked tables.

## When NOT to use

- Input is not a univariate statistical comparison (e.g., raw count data, untransformed intensities, or multivariate PCA scores). Use omu_summary or omu_anova first.
- Treatment factor has more than two levels and you have not specified numerator and denominator contrasts; use omu_anova instead for omnibus testing.
- Metabolite abundance data have not been log-transformed or appropriate variance-stabilizing transformation applied; apply transform_samples before statistical testing.

## Inputs

- omu_summary output object (data.frame with log2FoldChange, adjusted p-values, and metabolite annotations)
- omu_anova output object (alternative univariate model; ANOVA results with p-values and metabolite identifiers)
- hierarchical class annotations from assign_hierarchy (e.g., 'Class' column for metabolite functional categories)

## Outputs

- Stratified metabolite list (upregulated, downregulated, not significant) with log2FC and padj values
- Count summary table (e.g., from count_fold_changes) quantifying metabolites in each category
- ggplot2 volcano plot object (via plot_volcano) showing effect size vs. statistical significance
- Filtered data.frame suitable for downstream functional annotation or KEGG enrichment queries

## How to apply

Extract the omu_summary or omu_anova output object, which contains columns for log2FoldChange and adjusted p-values (e.g., padj_BH). Define statistical thresholds: a p-value cutoff (typically padj < 0.05) to flag significance, and optionally a log2FoldChange magnitude threshold (e.g., |log2FC| > 1) to prioritize large effect sizes. Stratify metabolites into three categories: upregulated (log2FC > 0, padj < threshold), downregulated (log2FC < 0, padj < threshold), and not significant (padj >= threshold or |log2FC| below threshold). Pass the annotated output and category column (e.g., 'Class' from assign_hierarchy) to plot_volcano or count_fold_changes to generate comparative visualizations or summary tables. The interpretation is validated when the resulting plot or table shows clear separation of groups, consistent direction of fold-changes within each category, and a count summary matching the filtering logic applied.

## Related tools

- **omu_summary** (Performs univariate t-test or Welch's t-test on log-transformed metabolomics count data, outputting log2FoldChange and adjusted p-values for a specified contrast (numerator vs. denominator treatment levels).) — github.com/connor-reid-tiffany/Omu
- **omu_anova** (Alternative univariate statistical test; performs ANOVA to measure variance across all groups within a factor, producing p-values for omnibus significance testing.) — github.com/connor-reid-tiffany/Omu
- **plot_volcano** (Generates a ggplot2 volcano plot from omu_summary output, visualizing log2FoldChange vs. -log10(adjusted p-value) with stratified coloring and shaping by metabolite class.) — github.com/connor-reid-tiffany/Omu
- **count_fold_changes** (Consumes omu_summary output to produce a data.frame summarizing the count of metabolites with significantly increased or decreased abundance.) — github.com/connor-reid-tiffany/Omu
- **assign_hierarchy** (Assigns hierarchical metabolite class annotations (e.g., from KEGG) to the count dataframe, enabling stratified interpretation by functional category.) — github.com/connor-reid-tiffany/Omu
- **ggplot2** (Provides theming and customization of volcano plot and other visualization outputs; ensures ggplot2 objects are compatible with theme_bw() and other ggplot2 styling.)

## Examples

```
omu_summary(count_data = c57_nos2KO_mouse_countDF, metadata = c57_nos2KO_mouse_metadata, numerator='Strep', denominator='Mock', Factor='Treatment', log_transform=TRUE, p_adjust='BH', test_type='welch') %>% plot_volcano(column='Class', strpattern=c('Organic acids','Carbohydrates'), fill=c('firebrick2','white','dodgerblue2'))
```

## Evaluation signals

- Volcano plot shows clear clustering: downregulated metabolites (left, padj < 0.05), upregulated metabolites (right, padj < 0.05), and non-significant metabolites (center or high padj values).
- Count summary from count_fold_changes reports integer counts of increased and decreased metabolites; sum matches the total number of metabolites passing the joint significance and effect-size thresholds.
- No metabolites are double-counted across categories (upregulated, downregulated, not significant); stratification logic is mutually exclusive.
- log2FoldChange values in each category are consistent with direction: upregulated group has median log2FC > 0, downregulated group has median log2FC < 0.
- Adjusted p-value distribution shows expected antibiotic patterns: padj < 0.05 for metabolites plotted as significant in volcano plot; padj >= 0.05 for unsignificant points.

## Limitations

- Univariate tests assume independence between metabolites; true correlation structure and false-discovery control depend on downstream multiple-testing correction (e.g., BH) and are sensitive to the number of metabolites tested.
- log2FoldChange magnitude and adjusted p-value thresholds are user-defined and may not generalize across different metabolomics platforms, matrices, or experimental designs; no single cutoff is recommended in the article.
- omu_summary and omu_anova do not account for metabolite co-regulation, pathway-level effects, or hierarchical dependency between metabolites in the same functional class; interpretation is limited to individual metabolite comparisons.
- Results are sensitive to log-transformation and other preprocessing steps (e.g., normalization); failing to apply log_transform=TRUE in omu_summary or omitting transform_samples before statistical testing can lead to inflated false positives.

## Evidence

- [other] univariate-statistical-output-interpretation: "Omu supports two univariate statistical models, t test and anova, using the functions ```omu_summary``` and ```anova_function``` respectively"
