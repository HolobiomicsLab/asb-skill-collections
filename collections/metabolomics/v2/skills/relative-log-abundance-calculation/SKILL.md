---
name: relative-log-abundance-calculation
description: Use when after applying a normalization method (e.g., median scaling,
  RUV, RLSC) to metabolomics peak intensity data, when you need to visually assess
  whether normalization has successfully reduced batch effects and whether samples
  cluster appropriately by biological group.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NormalizeMets
  - RStudio
  - Plotly
  license_tier: restricted
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive
  Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
- The use of RStudio is also recommended. RStudio is an integrated development environment
  (IDE)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_normalizemets_cq
    doi: 10.1007/s11306-018-1347-7
    title: NormalizeMets
  dedup_kept_from: coll_normalizemets_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-018-1347-7
  all_source_dois:
  - 10.1007/s11306-018-1347-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# relative-log-abundance-calculation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute relative log abundances (RLA) from normalized metabolomics feature matrices by centering each metabolite's intensities on the median within sample groups, enabling detection of normalization artifacts and outlier samples. This diagnostic visualization reveals batch effects and within-group heterogeneity that persist after normalization.

## When to use

After applying a normalization method (e.g., median scaling, RUV, RLSC) to metabolomics peak intensity data, when you need to visually assess whether normalization has successfully reduced batch effects and whether samples cluster appropriately by biological group. Use RlaPlots when you have a normalized featuredata matrix (samples × metabolites), grouping variables (batch or sample type), and want to identify samples with anomalous metabolite profiles relative to their group median.

## When NOT to use

- Input featuredata is not yet normalized (apply a normalization method first, e.g., median scaling, RLSC, or RUV).
- groupdata contains fewer than 2 groups or has missing group assignments for any sample.
- Your goal is to identify differential abundance of individual metabolites across groups (use LinearModelFit or similar instead).

## Inputs

- normalized featuredata matrix (samples × metabolites, numeric)
- groupdata vector (factor or character, length = number of samples)
- minoutlier threshold (numeric, default 0.5)
- plot type parameter ('ag' or 'wg')

## Outputs

- interactive RLA plot object (Plotly widget, optional HTML file)
- non-interactive RLA plot (PNG, PDF, JPEG, TIFF, or BMP file)
- sample labels for outliers exceeding minoutlier threshold

## How to apply

Load the normalized featuredata matrix (samples as rows, metabolites as columns) and a groupdata vector assigning each sample to a batch or experimental group. Call RlaPlots() with the matrix and groupdata, specifying type='ag' for across-group comparison (to assess batch homogeneity) or type='wg' for within-group comparison (to assess biological consistency). Set minoutlier threshold (default 0.5) to flag samples whose relative log abundance deviates beyond ±minoutlier log2 units from the group median; these labeled samples indicate potential outliers or normalization failures. Enable interactiveplot=TRUE to produce an interactive Plotly output or saveplot=TRUE with a non-interactive format (png, pdf, etc.) for publication. The plot centers each metabolite's relative abundances on zero per group, making it easy to visually detect batch-driven separation, skew, or high-variance samples.

## Related tools

- **NormalizeMets** (R package housing RlaPlots() function and upstream normalization methods (NormScaling, NormQcmets, NormCombined) used to generate the input normalized matrix) — github.com/metabolomicstats/NormalizeMets
- **R** (execution environment for loading featuredata, groupdata, and calling RlaPlots())
- **RStudio** (recommended IDE for interactive development and parameter tuning of RlaPlots calls)
- **Plotly** (underlying graphics library for interactive visualization when interactiveplot=TRUE)

## Examples

```
RlaPlots(featuredata=normalized_matrix, groupdata=batch_assignments, type='ag', minoutlier=0.5, interactiveplot=TRUE, saveinteractiveplot=TRUE, plotname='RLA_diagnostic')
```

## Evaluation signals

- All samples are labeled with their sample IDs on the plot if they deviate >minoutlier log2 units from the group median for any metabolite; unlabeled samples have ≤minoutlier deviation.
- Samples within the same biological group cluster together horizontally (low variance around zero), indicating successful normalization; samples in different batches show distinct vertical separation or skew, indicating remaining batch effects.
- The plot's y-axis shows metabolite names and x-axis shows relative log abundance centered on zero; the plot is symmetric around the zero line if normalization is unbiased.
- Interactive plot renders as an HTML widget with hover tooltips showing sample ID, metabolite, and RLA value; non-interactive version has crisp labels and no missing/overlapping sample annotations.
- Output file (if saveplot=TRUE) is created in the specified format (png, pdf, etc.) with dimensions and resolution appropriate for publication.

## Limitations

- RlaPlots assumes the input featuredata is already normalized; it diagnoses whether normalization was effective, not corrects raw data.
- High-dimensional data (many metabolites) may produce crowded plots with overlapping metabolite labels; interactive mode mitigates this via hover tooltips.
- minoutlier threshold is a visual aid; choosing too low a value flags many benign samples, while too high a value misses real outliers—no automated selection is provided.
- RlaPlots does not test statistical significance of outliers; it is a diagnostic visualization tool, not a hypothesis test.
- The function requires balanced or near-balanced group sizes; very imbalanced groups may produce unreliable group medians and median absolute deviations.

## Evidence

- [other] The RlaPlots function accepts a normalized featuredata matrix, grouping variables, outlier threshold, plot type (across-group or within-group), and output parameters to generate relative log abundance plots for normalization assessment.: "The RlaPlots function accepts a normalized featuredata matrix, grouping variables, outlier threshold, plot type (across-group or within-group), and output parameters to generate relative log"
- [other] Call RlaPlots() with parameters: featuredata (normalized matrix), groupdata (grouping variable), type set to 'ag' (across-group) or 'wg' (within-group), minoutlier threshold (default 0.5), and interactiveplot=TRUE to enable interactive Plotly output.: "Call RlaPlots() with parameters: featuredata (normalized matrix), groupdata (grouping variable), type set to 'ag' (across-group) or 'wg' (within-group), minoutlier threshold (default 0.5), and"
- [other] Return both interactive and non-interactive plot objects showing metabolite relative log abundances centered on the median per group, with samples labeled when deviation exceeds minoutlier threshold.: "Return both interactive and non-interactive plot objects showing metabolite relative log abundances centered on the median per group, with samples labeled when deviation exceeds minoutlier threshold"
- [readme] Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation.: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation"
- [other] RlaPlots <- function(featuredata, groupdata, minoutlier = 0.5, type=c('ag', 'wg'), saveplot=FALSE, plotname = 'RLAPlot'...: "RlaPlots <- function(featuredata, groupdata, minoutlier = 0.5, type=c("ag", "wg"), saveplot=FALSE, plotname = "RLAPlot""
