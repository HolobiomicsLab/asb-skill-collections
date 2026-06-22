---
name: volcano-plot-construction-from-fold-change-and-pvalue
description: Use when you have omu_summary output containing log2FoldChange and adjusted p-values (e.g., BH-corrected) for a pairwise contrast (e.g., Strep vs Mock treatment), and you want to visualize metabolite significance and magnitude simultaneously while stratifying points by hierarchical class (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3694
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - R
  - omu_summary
  - assign_hierarchy
  - ggplot2
  - plot_volcano
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

# volcano-plot-construction-from-fold-change-and-pvalue

## Summary

Construct a publication-ready volcano plot from metabolomics differential abundance results (log2 fold-change and adjusted p-values) using ggplot2. This skill enables visual identification of significantly altered metabolites across treatment contrasts with customizable aesthetic parameters (color, fill, shape, alpha) mapped to hierarchical metabolite classes.

## When to use

You have omu_summary output containing log2FoldChange and adjusted p-values (e.g., BH-corrected) for a pairwise contrast (e.g., Strep vs Mock treatment), and you want to visualize metabolite significance and magnitude simultaneously while stratifying points by hierarchical class (e.g., KEGG Class) to highlight specific metabolite categories of interest.

## When NOT to use

- Input omu_summary output has not been generated with a specified contrast (numerator/denominator) and test_type — use omu_summary first to compute log2FoldChange and p-values.
- Metabolites lack hierarchical class assignments — run assign_hierarchy with appropriate identifier ('KEGG', 'KO_Number', 'Prokaryote', or 'Eukaryote') before calling plot_volcano.
- You want to visualize multivariate patterns across all groups within a factor rather than pairwise contrasts — use PCA_plot or omu_anova instead.

## Inputs

- omu_summary output (data frame with log2FoldChange, adjusted p-value columns, and hierarchical class assignments from assign_hierarchy)
- Metabolite hierarchical class data (KEGG Class or equivalent from assign_hierarchy with identifier='KEGG')

## Outputs

- ggplot2 object (volcano plot with metabolites mapped to x-axis log2FoldChange and -log10(adjusted p-value) on y-axis, colored/filled/shaped by class)

## How to apply

Start with omu_summary output generated from a log-transformed, welch t-test comparison (numerator vs denominator, with p_adjust='BH'). Call plot_volcano() on this output, specifying column='Class' to stratify points by hierarchical metabolite classification, and use strpattern parameter to select which classes to highlight (e.g., 'Organic acids', 'Carbohydrates'). Map aesthetic parameters (fill, color, alpha, shape) to highlight or de-emphasize selected classes; for example, set fill=c('firebrick2','white','dodgerblue2') to distinguish elevated, neutral, and suppressed metabolites across the selected classes. Apply ggplot2 theme customization (e.g., theme_bw() with panel.grid=element_blank()) to produce a clean, publication-ready ggplot2 object. The resulting object is fully compatible with downstream ggplot2 modifications and faceting.

## Related tools

- **omu_summary** (Generates log2FoldChange and adjusted p-values for pairwise metabolite comparisons using t-test or anova; required input for plot_volcano) — github.com/connor-reid-tiffany/Omu
- **assign_hierarchy** (Assigns hierarchical metabolite class data (KEGG, KO_Number, Prokaryote, Eukaryote) required for stratifying volcano plot points by column parameter) — github.com/connor-reid-tiffany/Omu
- **ggplot2** (Provides themeing and customization framework; plot_volcano returns a ggplot2 object compatible with theme_bw(), theme() and other ggplot2 functions)
- **plot_volcano** (Core function in Omu package that constructs volcano plot from omu_summary output with class-based stratification and aesthetic parameter control) — github.com/connor-reid-tiffany/Omu

## Examples

```
plot_volcano(omu_summary_result, column='Class', strpattern=c('Organic acids', 'Carbohydrates'), fill=c('firebrick2','white','dodgerblue2'), color=c('black','black','black'), alpha=c(1,1,1), shape=c(21,21,21)) + theme_bw() + theme(panel.grid=element_blank())
```

## Evaluation signals

- Output is a valid ggplot2 object: verify using class(plot_object) == 'ggplot' and that it renders without errors.
- X-axis correctly represents log2FoldChange values and y-axis represents -log10(adjusted p-value) with expected ranges (e.g., x ∈ [-10, 10], y ∈ [0, 5+]).
- Points are stratified by metabolite class with distinct visual encoding (fill, color, shape, alpha) matching the strpattern and aesthetic parameter mappings specified.
- ggplot2 theme customizations (theme_bw(), panel.grid removal) are applied without errors; no grid lines visible on final plot.
- Metabolites meeting expected significance thresholds (e.g., |log2FC| > 1 and adjusted p < 0.05) are visually prominent and correctly positioned relative to contrast direction.

## Limitations

- plot_volcano requires pre-computed log2FoldChange and adjusted p-values; it does not perform statistical testing independently — ensure omu_summary or equivalent contrast is already computed.
- Stratification by hierarchical class (column parameter) depends on assign_hierarchy having been run first; metabolites lacking class assignments will not be plotted or will default to 'Unknown' if keep_unknowns=TRUE.
- Aesthetic parameters (fill, color, alpha, shape) are mapped per class; overlapping or ambiguous class definitions may obscure discrimination; review strpattern and class definitions before finalizing.
- Visual interpretation is subjective; significance thresholds (e.g., fold-change and p-value cutoffs for highlighting) must be chosen and communicated explicitly; plot does not enforce standard thresholds.

## Evidence

- [other] plot_volcano_output_ggplot2_compat: "The figure is a ggplot2 object, so it is compatible with any ggplot2 themes"
- [other] plot_volcano_stratification_and_aesthetics: "Call plot_volcano on the omu_summary output with column='Class', strpattern=c('Organic acids', 'Carbohydrates'), fill=c('firebrick2','white','dodgerblue2'), color=c('black','black','black'),"
- [other] omu_summary_contrast_setup: "Run omu_summary statistical comparison with numerator='Strep', denominator='Mock', Factor='Treatment', log_transform=TRUE, p_adjust='BH', and test_type='welch' to obtain log2FoldChange and adjusted"
- [other] assign_hierarchy_prerequisite: "To assign hierarchical class data, use the ```assign_hierarchy``` function and pick the correct identifier, either "KEGG", "KO_Number", "Prokaryote", or "Eukaryote""
- [other] ggplot2_theme_customization: "Apply ggplot2 theme customization with theme_bw() and theme(panel.grid=element_blank()) to produce the final volcano plot ggplot2 object"
