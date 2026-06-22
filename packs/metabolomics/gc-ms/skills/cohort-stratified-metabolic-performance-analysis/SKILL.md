---
name: cohort-stratified-metabolic-performance-analysis
description: Use when when you have uploaded a pre-analytical data table containing sample metadata, processing delay annotations (pre- and post-centrifugation times), and paired NMR metabolomic measurements for a plasma or serum cohort, and you need to determine how processing delays impact metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3745
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - PRIMA-Panel
  - QC-Tool
  techniques:
  - LC-MS
  - GC-MS
  - NMR
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c04938
  all_source_dois:
  - 10.1021/acs.analchem.4c04938
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Cohort-stratified metabolic performance analysis

## Summary

This skill uses PRIMA-Panel to quantify the effect of pre- and post-centrifugation processing delays on NMR metabolomic measurements across a sample cohort, generating delay-stratified performance reports that surface metabolite concentration shifts and data quality degradation.

## When to use

When you have uploaded a pre-analytical data table containing sample metadata, processing delay annotations (pre- and post-centrifugation times), and paired NMR metabolomic measurements for a plasma or serum cohort, and you need to determine how processing delays impact metabolite stability and quantify minor vs. major concentration changes across the cohort.

## When NOT to use

- Input data lacks pre-analytical metadata (e.g., centrifugation timing, SPREC classification) — PRIMA-Panel requires these fields to parse and validate the structure.
- Sample cohort contains only a single time-point (no delay variation) — the skill is designed to investigate effects *across* processing delay strata.
- Metabolomic platform is not NMR (e.g., LC-MS/MS, GC-MS) — PRIMA-Panel is instrument-specific to NMR-based measurements.
- Data are already aggregated into summary statistics — the skill requires raw or minimally processed per-sample metabolite measurements.

## Inputs

- Pre-analytical data table (CSV, TSV, or Excel) with columns: sample identifier, pre-centrifugation delay (minutes), post-centrifugation delay (minutes), SPREC classification, and NMR metabolomic measurements (metabolite concentrations)

## Outputs

- Interactive performance report table (HTML or CSV) summarizing cohort-level metabolite concentration shifts, stratified by pre- and post-centrifugation delay windows
- Delay-stratified metabolite change annotations (minor and major threshold violations per metabolite)
- Data quality indicators and stability metrics across the sample cohort

## How to apply

Load the pre-analytical data table into PRIMA-Panel and parse its structure to validate presence of required fields for cohort identification and processing delay annotation (pre-centrifugation delay in minutes and post-centrifugation delay in minutes, stratified by SPREC classification). Use the 'Single' tab to set slider-controlled thresholds for pre- and post-centrifugation time windows. PRIMA-Panel then calculates per-metabolite concentration shifts and flags minor and major changes relative to user-adjustable percentage thresholds. The resulting interactive table displays cohort-level statistics and identifies which metabolites degrade most severely within each delay window. Download the report as HTML (formatted) or CSV (raw table) for downstream interpretation.

## Related tools

- **PRIMA-Panel** (Interactive data exploration and performance report generation platform; accepts uploaded pre-analytical tables and calculates metabolite concentration shifts stratified by processing delay windows) — https://github.com/funkam/PRIMA
- **QC-Tool** (Associated quality control utility for pre-analytical data validation and SPREC classification) — https://github.com/funkam/QC-Tool

## Evaluation signals

- Parsed input table contains all required fields (sample ID, pre-centrifugation delay, post-centrifugation delay, SPREC classification, metabolite concentrations) with no missing values in the delay or metabolite columns.
- Generated report table lists all metabolites present in the input cohort and flags minor/major changes according to user-specified percentage thresholds for each delay window.
- Cohort-level statistics (e.g., mean concentration, SD, delay-stratified subgroup counts) are consistent with manual spot-checks of the input data.
- HTML and CSV exports are non-empty, properly formatted, and contain identical underlying data (format-agnostic verification).
- Metabolite concentration shifts increase monotonically (or step-wise) with increasing processing delay, consistent with known stability degradation in blood samples.

## Limitations

- PRIMA-Panel is specialized to peripheral blood samples (plasma/serum); applicability to other biofluids or tissue types is not documented.
- The tool assumes NMR metabolomic measurements; integration with other omics modalities (proteomics, lipidomics) is not supported.
- Percentage thresholds for minor/major changes and color scheme are user-adjustable but not validated against external stability benchmarks; calibration is analyst-dependent.
- Processing delay times must be accurately recorded in the input table; timing errors or missing delay annotations will cause validation failure or misinterpretation.

## Evidence

- [readme] Core tool definition: "The PRIMA-Panel is a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum)."
- [readme] Input data requirements: "PRIMA-Panel allows the creation of so called performance reports for sample cohorts. Here a data table with pre-analytical information can be uploaded"
- [other] Workflow: parsing and delay stratification: "Parse and validate the input table structure to ensure required fields for cohort identification and processing delay annotation are present."
- [other] Workflow: performance metric calculation: "Calculate performance metrics quantifying the effect of processing delays on metabolic parameters (e.g., metabolite concentration shifts, data quality degradation) across the sample cohort."
- [readme] Output format and interaction: "The 'Single' tab allows the user to set a pre-centrifugation time and a post-centrifugation using a Slider. A table is then generated that higlights a minor and a major change for each metabolite in"
- [readme] Export capabilities: "The table can be downloaded as a .HTML report or the table directly as .csv (or other formats)."
