---
name: pre-analytical-delay-effect-quantification
description: Use when you have uploaded a pre-analytical data table containing sample metadata, processing delay annotations (pre- and post-centrifugation timestamps or duration), and paired NMR metabolomic measurements for a sample cohort, and you need to quantify how delays at different time-points affect.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - PRIMA-Panel
  - QC-Tool
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

# pre-analytical-delay-effect-quantification

## Summary

Quantify the effect of processing delays (pre- and post-centrifugation) on metabolic parameters in peripheral blood samples by calculating delay-stratified metabolite concentration shifts and data quality degradation metrics. This skill enables cohort-level assessment of pre-analytical stability to inform sample handling protocols and data interpretation.

## When to use

Use this skill when you have uploaded a pre-analytical data table containing sample metadata, processing delay annotations (pre- and post-centrifugation timestamps or duration), and paired NMR metabolomic measurements for a sample cohort, and you need to quantify how delays at different time-points affect metabolite concentrations and measurement reliability.

## When NOT to use

- Input data lacks documented processing delay information (pre- and post-centrifugation timestamps or intervals); the skill requires explicit delay annotations to quantify effects.
- Sample cohort contains only a single processing delay condition or time-point; stratified comparison across delays is required to meaningfully assess delay effects.
- NMR metabolomic data have not been processed to metabolite concentration estimates; raw spectra or unquantified peak data cannot be directly ingested for effect calculation.

## Inputs

- pre-analytical data table (CSV, TSV, or Excel) with columns: sample cohort identifiers, pre-centrifugation delay (minutes), post-centrifugation delay (minutes), sample type (plasma/serum), and NMR metabolomic measurements (metabolite concentrations)

## Outputs

- performance report (HTML or CSV format) with cohort-level statistics, delay-stratified metabolite concentration changes (% shift per metabolite per delay stratum), data quality indicators, and color-coded minor/major change flags
- lollipop plot or bar chart visualization highlighting metabolite stability across time-points stratified by SPREC classification

## How to apply

Load the pre-analytical data table into PRIMA-Panel and parse the table structure to validate presence of required fields: cohort identifiers, pre-centrifugation delay, post-centrifugation delay, and NMR metabolomic measurements. Calculate performance metrics for each metabolite by stratifying samples by delay intervals (aligned to SPREC classification time-points in minutes), measuring concentration shifts as percentage change relative to a reference (minimal-delay) baseline, and flagging minor and major metabolite changes using adjustable thresholds. Generate an interactive performance report summarizing cohort-level statistics, delay-stratified metabolite changes per metabolite, and data quality indicators (e.g., degradation patterns). Export the report as HTML or CSV with color-coded threshold highlights to enable downstream interpretation.

## Related tools

- **PRIMA-Panel** (Interactive data exploration and performance report generation tool that ingests pre-analytical data tables, stratifies samples by processing delay, calculates metabolite concentration shifts, and exports cohort-level performance reports with adjustable color and threshold settings.) — https://github.com/funkam/PRIMA
- **QC-Tool** (Associated quality control and visualization component for highlighting stability time-points and generating alternative data presentations (e.g., lollipop plots) for pre-analytical data.) — https://github.com/funkam/QC-Tool

## Evaluation signals

- Validate that the input table contains all required fields: cohort identifiers, pre-centrifugation delay, post-centrifugation delay, and NMR metabolomic measurements; reject inputs with missing or malformed delay annotations.
- Verify that metabolite concentration shifts are computed as percentage change relative to a defined baseline (e.g., minimal-delay stratum) and that delay strata align with SPREC time-point classifications (e.g., 15, 30, 60 minutes).
- Confirm that performance report includes both minor and major change flags per metabolite, with thresholds (% shift) explicitly reported and color-coded consistently across the report.
- Check that the exported report includes cohort-level summary statistics (mean, SD, or quartile metabolite shifts per delay stratum) and data quality indicators showing degradation patterns across delays.
- Ensure that the report is exportable in both HTML (interactive, downloadable) and CSV (tabular, machine-readable) formats for downstream interpretation and secondary analysis.

## Limitations

- The tool is designed specifically for peripheral blood samples (plasma/serum) and NMR metabolomic measurements; applicability to other sample types or analytical platforms is not established.
- Performance metric calculations rely on accurate pre-analytical metadata; incorrect delay annotations, missing timestamps, or incomplete sample documentation will propagate errors into effect quantification.
- The tool provides interactive visualization and threshold adjustment but does not perform statistical hypothesis testing or significance correction for multiple metabolite comparisons; users must interpret results in context of their study design.
- Color and percentage thresholds for minor/major metabolite changes are adjustable but user-defined; no automated or data-driven threshold recommendation is provided by the tool.

## Evidence

- [readme] The PRIMA-Panel is a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum).: "The PRIMA-Panel is a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum)."
- [readme] The panel functions as a data exploration tool allowing interactive investigation of processing delay effects and creation of performance reports for sample cohorts by uploading pre-analytical data tables.: "The panel functions as a data expoloration tool. It allows to investigate the these effects interactively. Additionally, the PRIMA-Panel allows the creation of so called performance reports for"
- [other] Calculate performance metrics quantifying the effect of processing delays on metabolic parameters across the sample cohort, with delay-stratified metabolite changes and data quality indicators.: "Calculate performance metrics quantifying the effect of processing delays on metabolic parameters (e.g., metabolite concentration shifts, data quality degradation) across the sample cohort."
- [other] Parse and validate input table structure to ensure required fields for cohort identification and processing delay annotation are present.: "Parse and validate the input table structure to ensure required fields for cohort identification and processing delay annotation are present."
- [readme] Time-points are sorted according to SPREC classification and data is split by pre- and post-centrifugation delays; reports can be downloaded as HTML or CSV with adjustable color and percentage thresholds.: "The time-points are sorted according to their SPREC classification. In addition, there is an alternative way of presenting the date in form of lollipop plots. The data is split according the two"
- [readme] A table is generated highlighting minor and major changes for each metabolite in a given timeframe, with adjustable colors and percentage thresholds, downloadable as HTML or CSV.: "A table is then generated that higlights a minor and a major change for each metabolite in that given timeframe. The colors, as well as the % threshholds, can be adjusted. The table can be downloaded"
