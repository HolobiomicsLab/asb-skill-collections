---
name: quality-control-visualization-metabolomics
description: Use when after completing kNN imputation, outlier sample removal, and variance-stabilizing normalization (vsn) on a MultiAssayExperiment object containing metabolite measurements.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3316
  tools:
  - MetaboDiff
  - R
  - MultiAssayExperiment
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
---

# quality-control-visualization-metabolomics

## Summary

Generate and interpret quality control plots that verify normalized metabolite measurements show comparable distributions across samples and experimental groups after preprocessing. This skill validates that variance stabilization and outlier removal have achieved homogeneous signal quality before downstream statistical analysis.

## When to use

After completing kNN imputation, outlier sample removal, and variance-stabilizing normalization (vsn) on a MultiAssayExperiment object containing metabolite measurements. Use this skill to confirm that normalized measurements exhibit stable variance across the measurement range and comparable distributions within and between sample groups (e.g., tumor vs. normal tissue) before proceeding to differential analysis or correlation network construction.

## When NOT to use

- Input data has not yet been normalized via vsn or equivalent variance-stabilizing method; use na_heatmap and outlier_heatmap first.
- Outlier samples have not been identified and removed; quality_plot will not accurately reflect true signal quality if outliers remain.
- Sample grouping factor is not available or is undefined in colData; the grouping parameter is essential for stratified visualization.

## Inputs

- MultiAssayExperiment object (preprocessed: post-imputation, post-outlier removal, post-vsn normalization)
- sample metadata (colData) with group assignments (e.g., tumor_normal factor)

## Outputs

- quality control plot (visualization of normalized metabolite distributions stratified by sample group)
- visual assessment of variance homogeneity and inter-group comparability

## How to apply

Call the quality_plot function on the preprocessed MultiAssayExperiment object, specifying the grouping factor (e.g., group_factor='tumor_normal') and group-specific label colors to visualize measurement distributions stratified by sample class. The plot should display normalized metabolite values across samples, revealing whether variance remains nearly constant over the measured spectrum and whether distributions are comparable across groups. Inspect the plot for outlier samples persisting after preprocessing, asymmetric or heavy-tailed distributions that suggest incomplete normalization, and systematic differences in variance or central tendency between groups that would indicate batch effects or preprocessing failure. Success is confirmed when all samples show similar distribution shapes and spreads, group-specific patterns are driven by biology rather than technical artifact, and no isolated samples deviate markedly from their group's distribution.

## Related tools

- **MetaboDiff** (Provides quality_plot function for QC visualization of normalized metabolite measurements in MultiAssayExperiment objects) — https://github.com/andreasmock/MetaboDiff
- **MultiAssayExperiment** (Container object that integrates assay (normalized metabolite measurements), rowData (metabolite annotations), and colData (sample metadata with group labels) for quality_plot input)
- **R** (Environment for executing quality_plot and related MetaboDiff QC functions)

## Examples

```
quality_plot(met, group_factor="tumor_normal", label_colors=c("darkseagreen","dodgerblue"))
```

## Evaluation signals

- Normalized metabolite measurements display comparable distribution shapes and spreads across all samples within each group.
- Variance (spread/dispersion) remains approximately constant across the full range of normalized metabolite values, with no systematic increase or decrease with signal intensity.
- Group-specific patterns in the plot reflect expected biological differences (e.g., tumor vs. normal) rather than technical artifacts or preprocessing failures.
- No isolated samples deviate markedly from their assigned group's distribution, indicating successful outlier removal in prior preprocessing steps.
- Visual inspection confirms that samples do not cluster into unexpected sub-groups that would suggest unaccounted batch effects or unknown stratification.

## Limitations

- quality_plot provides visual assessment only; it does not quantify variance homogeneity or perform formal statistical tests (e.g., Levene's test), so interpretation requires domain judgment.
- The plot's interpretability depends on the choice of grouping factor; if samples are grouped incorrectly or mixed-effects structure is present (e.g., multiple batches within a group), the plot may not reveal true preprocessing success.
- If outlier samples were not removed in prior steps, quality_plot will show them as deviants but will not automatically exclude them; the user must re-run outlier_heatmap and remove_cluster to improve signal quality and then regenerate the plot.
- Label color choices and plot aesthetics are user-specified; poor color contrast or overcrowding of samples can obscure distributional patterns even if preprocessing was successful.

## Evidence

- [methods] quality_plot - generates quality control plots: "Generate a quality control plot with quality_plot to verify that normalized measurements show comparable distributions across samples and groups."
- [methods] vsn ensures constant variance over the measured spectrum: "Variance stabilizing normalization (vsn) is used to ensure that the variance remains nearly constant over the measured spectrum"
- [methods] quality_plot function call with group_factor: "quality_plot(met, group_factor="tumor_normal", label_colors=c("darkseagreen","dodgerblue"))"
- [readme] MetaboDiff QC workflow context: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
