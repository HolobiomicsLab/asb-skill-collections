---
name: quality-control-metric-interpretation
description: Use when after normalizing a metabolomics featuredata matrix (samples
  × metabolites), use this skill to visually and quantitatively assess normalization
  quality. Specifically, apply it when you need to decide whether a chosen normalization
  method (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NormalizeMets
  - RStudio
  - RlaPlots
  - PcaPlots
  - HeatMap
  license_tier: open
  provenance_tier: literature
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

# quality-control-metric-interpretation

## Summary

Interpret relative log abundance (RLA) diagnostic plots and other normalization quality metrics to assess whether batch effects, unwanted variation, and normalization success have been adequately controlled in metabolomics data. This skill enables selection of appropriate normalization methods by evaluating how well samples cluster by expected group and identifying outlier metabolites or samples that deviate beyond acceptable thresholds.

## When to use

After normalizing a metabolomics featuredata matrix (samples × metabolites), use this skill to visually and quantitatively assess normalization quality. Specifically, apply it when you need to decide whether a chosen normalization method (e.g., RLSC, median scaling, RUV2) has sufficiently reduced batch effects or technical variation, or when comparing multiple normalization methods to select the best one. Trigger: you have a normalized featuredata matrix, grouping variables (batch, sample type, or cohort assignment), and need to evaluate whether relative log abundances are centered on the median per group with minimal outlier deviation.

## When NOT to use

- Input featuredata has not been log-transformed or normalized; RlaPlots requires pre-normalized, log-scale data to produce interpretable relative log abundances.
- Groupdata is missing or does not correspond 1:1 with featuredata sample rows; grouping variable must be complete and aligned.
- No meaningful batch or group structure exists in the study design; RlaPlots is designed for grouped comparisons and will not reveal useful patterns if samples are ungrouped.

## Inputs

- featuredata: normalized metabolomics matrix (samples × metabolites, numeric)
- groupdata: vector of batch or group assignments per sample (factor or character)
- minoutlier: numeric threshold for flagging outlier deviation (default 0.5, relative log scale)
- type: character, 'ag' for across-group or 'wg' for within-group comparison

## Outputs

- RLA plot object (interactive Plotly or static raster/vector image)
- Labeled sample and metabolite outliers exceeding minoutlier threshold
- Visual assessment of normalization success (median centering, group clustering)

## How to apply

Load the normalized featuredata matrix (samples as rows, metabolites as columns) and a groupdata vector assigning each sample to a batch or group. Call RlaPlots() with the featuredata, groupdata, and type parameter set to 'ag' (across-group) to compare relative log abundance distributions across all groups or 'wg' (within-group) to assess within-group consistency. Set minoutlier threshold (default 0.5) to flag samples whose metabolite abundances deviate beyond this relative log scale; samples exceeding this threshold will be labeled on the plot for manual inspection. Enable interactiveplot=TRUE for interactive Plotly visualization or saveplot=TRUE to export a static image (png, bmp, jpeg, tiff, or pdf). Interpret the resulting plot by examining whether metabolite relative log abundances cluster around zero (median-centered) within each group—this indicates successful normalization. Samples or metabolites with large labeled deviations suggest incomplete batch correction, quality issues, or potential outliers requiring further investigation or exclusion.

## Related tools

- **RlaPlots** (Primary function for generating relative log abundance diagnostic plots from normalized metabolomics data, with configurable group comparison type, outlier threshold, and output format (interactive or static).) — github.com/metabolomicstats/NormalizeMets
- **NormalizeMets** (R package providing normalization methods (RLSC, median, RUV2, etc.) and QC functions including RlaPlots, PcaPlots, and HeatMap for assessing and visualizing normalization quality.) — github.com/metabolomicstats/NormalizeMets
- **PcaPlots** (Complementary QC function for visualizing principal component clustering by group; used alongside RlaPlots to assess whether normalization has reduced unwanted variation.) — github.com/metabolomicstats/NormalizeMets
- **HeatMap** (Interactive and non-interactive heatmap visualization enabling whole-matrix inspection of normalized featuredata to identify batch or sample-type patterns.) — github.com/metabolomicstats/NormalizeMets
- **R** (Statistical computing environment in which NormalizeMets functions are executed.)
- **RStudio** (Recommended integrated development environment (IDE) for running RlaPlots and interactive Plotly visualization.)

## Examples

```
RlaPlots(featuredata = normalized_metabolites, groupdata = batch_assignment, type = 'ag', minoutlier = 0.5, interactiveplot = TRUE, saveinteractiveplot = TRUE, plotname = 'normalization_qc')
```

## Evaluation signals

- Relative log abundances are centered on zero (median) within each batch or group on the RLA plot; large systematic deviations from zero indicate incomplete batch correction.
- Number of outlier samples and metabolites flagged at the minoutlier threshold is minimal and consistent with expected experimental error; excessive outliers suggest data quality issues or poor normalization method choice.
- Within-group ('wg') RLA plots show tight clustering around the group median with small spread; across-group ('ag') plots show distinct separation between batch medians only if batch is a true confound (not a biological variable of interest).
- Visual comparison of RLA plots before and after normalization, or across multiple normalization methods, shows improved median centering and reduced outlier deviation after applying the chosen method.
- Interactive Plotly labels identify specific samples or metabolites deviating beyond minoutlier threshold; manual inspection of these outliers reveals whether they correspond to known quality issues, instrumental drift, or genuine biological signals.

## Limitations

- RlaPlots assumes featuredata have been log-transformed and normalized; application to raw or non-log-scale data will produce uninterpretable relative log abundances.
- The minoutlier threshold (default 0.5) is heuristic and may require adjustment depending on the magnitude of expected biological variation relative to technical noise; no automated threshold optimization is provided.
- RlaPlots is a univariate visualization tool and does not account for multivariate correlations between metabolites; outliers identified in RLA plots may not reflect true multivariate anomalies.
- The skill assesses normalization quality post-hoc but does not prescribe corrective actions; identification of poor normalization requires the user to manually re-select methods or investigate sample/instrumental issues.
- Presence of genuine biological batch-metabolite interactions (true effect modification) may be conflated with incomplete batch correction in RLA plots, requiring domain knowledge to disambiguate.

## Evidence

- [other] RlaPlots accepts a normalized featuredata matrix, grouping variables, outlier threshold, plot type, and output parameters to generate relative log abundance plots for normalization assessment.: "The RlaPlots function accepts a normalized featuredata matrix, grouping variables, outlier threshold, plot type (across-group or within-group), and output parameters to generate relative log"
- [other] RlaPlots returns plots showing metabolite relative log abundances centered on the median per group, with samples labeled when deviation exceeds minoutlier threshold.: "Return both interactive and non-interactive plot objects showing metabolite relative log abundances centered on the median per group, with samples labeled when deviation exceeds minoutlier threshold."
- [readme] NormalizeMets contains functions to assess, select, and implement statistical methods for normalizing metabolomics data subject to batch effects and matrix effects.: "The NormalizeMets R package contains a collection of functions to aid in the statistical analysis of metabolomic data and can be used assess, select and implement statistical methods for normalizing"
- [readme] Metabolomics data are subject to unwanted variation from batch effects, matrix effects, and confounding biological variation.: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation."
- [other] RlaPlots parameters include type set to 'ag' (across-group) or 'wg' (within-group), minoutlier threshold, and saveplot options.: "Call RlaPlots() with parameters: featuredata (normalized matrix), groupdata (grouping variable), type set to 'ag' (across-group) or 'wg' (within-group), minoutlier threshold (default 0.5)"
