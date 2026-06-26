---
name: interactive-plot-generation-and-export
description: Use when after normalizing a featuredata matrix (samples × metabolites),
  when you need to visually assess the success of normalization across batches or
  sample groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
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

# interactive-plot-generation-and-export

## Summary

Generate interactive and non-interactive diagnostic visualizations of normalized metabolomics data using RlaPlots or PcaPlots functions, with options to save outputs as HTML widgets or static image files. This skill enables assessment of normalization quality and batch effects through interactive Plotly-based plots that highlight outlier samples.

## When to use

After normalizing a featuredata matrix (samples × metabolites), when you need to visually assess the success of normalization across batches or sample groups. Use this skill when you want to interactively explore relative log abundance patterns, identify outlier samples that deviate from group medians, and save publication-ready diagnostic plots. Particularly valuable when the minoutlier threshold (default 0.5) would flag samples for inspection.

## When NOT to use

- Input featuredata is not normalized or log-transformed; apply LogTransform() and normalization methods (NormQcmets, NormQcsamples, NormScaling, or NormCombined) first.
- Groupdata does not align with featuredata row names (sample names mismatch); verify sample correspondence before calling RlaPlots.
- You need to assess missingness patterns or handle missing values prior to normalization assessment; use MissingValues() first.

## Inputs

- featuredata (normalized numeric matrix: samples × metabolites, with unique sample names as row names and unique metabolite names as column names)
- groupdata (vector assigning each sample to a batch, sample type, or grouping variable)
- minoutlier (numeric threshold; default 0.5; samples deviating beyond this are labeled on plots)

## Outputs

- Interactive Plotly plot object (when interactiveplot=TRUE)
- HTML widget file (when saveinteractiveplot=TRUE; interactive browsable output)
- Static plot object (when interactiveplot=FALSE)
- Raster or vector image file (when saveplot=TRUE; format specified by savetype: png, bmp, jpeg, tiff, or pdf)

## How to apply

Load the normalized featuredata matrix and groupdata (batch or sample-type assignment vector) into R. Call RlaPlots() specifying: featuredata (normalized intensity matrix), groupdata (grouping variable), type parameter set to 'ag' (across-group) or 'wg' (within-group) depending on whether you want to assess normalization consistency across all groups or within each group separately, and minoutlier threshold (default 0.5, specifying which samples to label when deviation exceeds this threshold). Set interactiveplot=TRUE to generate interactive Plotly output, and optionally set saveinteractiveplot=TRUE to save as an HTML widget for interactive exploration. For static outputs, set interactiveplot=FALSE and saveplot=TRUE, specifying savetype (png, bmp, jpeg, tiff, or pdf) and plotname. The resulting plots center relative log abundances on the median per group, with outlier samples labeled by sample name.

## Related tools

- **RlaPlots** (Core function for generating relative log abundance diagnostic plots from normalized metabolomics data; accepts featuredata matrix, groupdata, plot type (across-group or within-group), outlier threshold, and output format parameters.) — github.com/metabolomicstats/NormalizeMets
- **PcaPlots** (Alternative visualization function for generating interactive and non-interactive PCA plots from normalized data; shares same save parameters (saveplot, plotname, savetype, saveinteractiveplot).) — github.com/metabolomicstats/NormalizeMets
- **HeatMap** (Complementary function producing interactive and non-interactive heatmaps to visualize whole data matrix patterns after normalization.) — github.com/metabolomicstats/NormalizeMets
- **R** (Statistical computing environment required to execute NormalizeMets functions (version 3.4.3 or higher).)
- **RStudio** (Integrated development environment for R; recommended for interactive development and visualization of plot outputs.)
- **NormalizeMets** (R package containing RlaPlots, PcaPlots, and HeatMap visualization functions; installed via install.packages('NormalizeMets').) — github.com/metabolomicstats/NormalizeMets

## Examples

```
RlaPlots(featuredata=norm_data, groupdata=batch_assignment, type='ag', minoutlier=0.5, interactiveplot=TRUE, saveinteractiveplot=TRUE, plotname='QC_RLA_normalized')
```

## Evaluation signals

- Interactive plot object is successfully created and is responsive to hover, zoom, and selection interactions (Plotly widgets are functional).
- HTML widget file is generated with correct file path and opening in web browser displays interactive plot with sample labels and hover tooltips.
- Static image file exists at specified savetype and resolution; file size and format match requested parameters (e.g., PNG compression, PDF vector quality).
- Plotted relative log abundances are centered on group-specific medians; samples flagged as outliers exceed minoutlier threshold and are visibly labeled with sample names on the plot.
- Across-group (ag) plots show all samples arranged by group; within-group (wg) plots show intra-group deviations—visual structure matches type parameter specification.

## Limitations

- RlaPlots requires pre-normalized featuredata; if data contain batch effects or have not undergone appropriate normalization method, diagnostic plot interpretation may be misleading.
- Outlier labeling (controlled by minoutlier threshold) may become cluttered if many samples exceed the threshold; threshold tuning or separate within-group analysis (type='wg') may be needed for dense datasets.
- Interactive Plotly output requires a web browser or Jupyter/RStudio environment capable of rendering HTML widgets; saveinteractiveplot=TRUE output may not display correctly in all headless or remote compute contexts.
- Static image export quality and file size depend on plot complexity and savetype resolution; vector formats (pdf, tiff) preserve quality but may produce large files for high-dimensional data.
- No changelog provided in repository documentation; version compatibility and API stability across NormalizeMets updates are not explicitly documented.

## Evidence

- [other] Call RlaPlots() with parameters: featuredata (normalized matrix), groupdata (grouping variable), type set to 'ag' (across-group) or 'wg' (within-group), minoutlier threshold (default 0.5), and interactiveplot=TRUE to enable interactive Plotly output.: "Call RlaPlots() with parameters: featuredata (normalized matrix), groupdata (grouping variable), type set to 'ag' (across-group) or 'wg' (within-group), minoutlier threshold (default 0.5), and"
- [other] Optionally set saveinteractiveplot=TRUE to save the interactive plot as an HTML widget. Optionally generate a non-interactive version by setting interactiveplot=FALSE and saveplot=TRUE, specifying savetype (png, bmp, jpeg, tiff, or pdf) and plotname.: "Optionally set saveinteractiveplot=TRUE to save the interactive plot as an HTML widget. Optionally generate a non-interactive version by setting interactiveplot=FALSE and saveplot=TRUE, specifying"
- [other] Return both interactive and non-interactive plot objects showing metabolite relative log abundances centered on the median per group, with samples labeled when deviation exceeds minoutlier threshold.: "Return both interactive and non-interactive plot objects showing metabolite relative log abundances centered on the median per group, with samples labeled when deviation exceeds minoutlier threshold."
- [other] RlaPlots <- function(featuredata, groupdata, minoutlier = 0.5, type=c("ag", "wg"), saveplot=FALSE, plotname = "RLAPlot"...: "RlaPlots <- function(featuredata, groupdata, minoutlier = 0.5, type=c("ag", "wg"), saveplot=FALSE, plotname = "RLAPlot""
- [readme] The input data format consists of three parts: (i) "featuredata" which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be provided as row names and unique metabolite names as column names: "featuredata" which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be provided as row names and unique metabolite names as"
