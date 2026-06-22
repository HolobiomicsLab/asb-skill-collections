---
name: interactive-data-exploration-design
description: Use when you have NMR metabolomics measurements paired with pre-analytical metadata (processing delay times, centrifugation timing, sample type such as plasma vs. serum, cohort identifiers) and need to interactively explore how variation in processing conditions drives changes in metabolic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - PRIMA-Panel
derived_from:
- doi: 10.1021/acs.analchem.4c04938
  title: PRIMA-Panel
evidence_spans:
- Pre-Analytical Investigator for NMR-based Metabolomics (PRIMA-Panel)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_prima_panel_cq
    doi: 10.1021/acs.analchem.4c04938
    title: PRIMA-Panel
  dedup_kept_from: coll_prima_panel_cq
schema_version: 0.2.0
---

# interactive-data-exploration-design

## Summary

Design and implement an interactive data exploration interface that enables cohort-level investigation of how pre-analytical variables (processing delays, sample type) affect quantitative metabolic parameters in NMR metabolomics. This skill combines dynamic filtering, multi-dimensional visualization, and tabular performance reporting to support hypothesis generation around sample stability and pre-analytical quality.

## When to use

Apply this skill when you have NMR metabolomics measurements paired with pre-analytical metadata (processing delay times, centrifugation timing, sample type such as plasma vs. serum, cohort identifiers) and need to interactively explore how variation in processing conditions drives changes in metabolic parameter values across a sample cohort. Use it specifically when the analysis goal is exploratory (identifying stability thresholds, detecting degradation patterns) rather than confirmatory, and when stakeholders need real-time filtering and comparison capabilities.

## When NOT to use

- Do not use this skill when the input lacks paired pre-analytical metadata; interactive exploration requires both metabolite measurements and processing delay / sample handling variables.
- Do not use this skill for confirmatory hypothesis testing or statistical inference requiring p-values and confidence intervals; PRIMA-Panel is explicitly a data exploration and quality assessment tool.
- Do not use this skill on already-aggregated or QC-filtered datasets where pre-analytical variation has been removed; the skill is designed to surface and investigate pre-analytical effects, not to analyze downstream biology after QC.

## Inputs

- NMR metabolite measurement table (metabolite concentrations × samples)
- Pre-analytical metadata table with processing delay times, SPREC classification, sample type (plasma/serum), centrifugation timing (pre- and post-centrifugation intervals in minutes), and cohort identifiers
- User-specified delay thresholds and concentration change percentage cutoffs (minor and major)

## Outputs

- Interactive visualization dashboard (scatter plots, line plots, box plots, lollipop plots)
- Performance report table highlighting minor and major metabolite changes stratified by delay bins or continuous delay values
- Downloadable HTML performance report with color-coded change indicators
- Downloadable .csv tabular summary with descriptive statistics (mean, standard deviation, correlation coefficients between delay and metabolite parameter)

## How to apply

Load the metabolite measurement matrix and pre-analytical metadata (processing delay times binned by SPREC classification, pre- and post-centrifugation intervals, sample type, cohort) into memory and validate that all required columns are present and properly formatted. Construct interactive visualizations (scatter plots of metabolite concentration vs. delay duration, lollipop plots grouped by delay time-points, box plots stratified by sample type) that reveal the relationship between processing delay and individual metabolic parameter stability. Enable dynamic sliders or input fields to set pre-centrifugation and post-centrifugation time thresholds; generate a performance report table that highlights minor and major concentration changes for each metabolite within the selected timeframe, with color-coding and percentage thresholds that can be adjusted by the user. Provide subsetting and filtering controls to isolate specific sample types (plasma or serum), cohorts, or delay ranges. Export outputs as both interactive HTML reports and flat formats (.csv) to facilitate downstream statistical analysis and communication with collaborators.

## Related tools

- **PRIMA-Panel** (Interactive Shiny application that hosts the data exploration, performance report generation, filtering, and visualization components; provides the core interface for dynamic threshold setting and multi-format export) — https://github.com/funkam/PRIMA

## Evaluation signals

- Visualizations correctly render the relationship between processing delay duration (x-axis) and individual metabolic parameter values (y-axis) with no missing or misaligned data points.
- Performance report table correctly identifies metabolites with minor (user-adjustable %) and major concentration changes within the selected pre- and post-centrifugation time interval, and color-coding matches the specified thresholds.
- Dynamic filtering (by sample type, cohort, delay range) produces subsetted visualizations and tables that reflect only the selected samples without data loss or duplication.
- Exported HTML and .csv outputs are valid, readable, and contain all selected samples, metabolites, and pre-analytical metadata without truncation or corruption.
- Descriptive statistics (mean, SD, correlation coefficients) in the tabular output are mathematically consistent with the underlying data when spot-checked on a subset of metabolites.

## Limitations

- PRIMA-Panel currently stratifies delays according to SPREC classification, which may obscure fine-grained relationships between continuous delay values and metabolite stability; users must decide whether binned or continuous delay representation is appropriate for their study.
- The tool requires manual upload of pre-analytical metadata; automated parsing from instrument logs or LIMS systems is not documented, limiting high-throughput integration.
- Color-coding thresholds for minor and major change detection are user-adjustable but not statistically calibrated to biological significance or assay measurement error; users must validate that chosen % cutoffs reflect clinically or analytically meaningful differences.
- Performance reports are generated for individual metabolites; the tool does not implement multivariate statistical tests (e.g., PCA, OPLS-DA) to detect joint degradation patterns across metabolite panels.

## Evidence

- [readme] Core tool function: "The PRIMA-Panel is a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum)"
- [readme] Interactive exploration purpose: "The panel functions as a data expoloration tool. It allows to investigate the these effects interactively"
- [readme] Performance report generation workflow: "The 'Single' tab allows the user to set a pre-centrifugation time and a post-centrifugation using a Slider. A table is then generated that higlights a minor and a major change for each metabolite in"
- [readme] Customizable thresholds and export formats: "The colors, as well as the % threshholds, can be adjusted. The table can be downloaded as a .HTML report or the table directly as .csv (or other formats)"
- [readme] Delay stratification by SPREC: "The time-points are sorted according to their SPREC classification. In addition, there is an alternative way of presenting the date in form of lollipop plots. The data is split according the two"
