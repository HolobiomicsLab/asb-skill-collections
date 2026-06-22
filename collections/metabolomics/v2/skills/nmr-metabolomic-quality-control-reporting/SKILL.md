---
name: nmr-metabolomic-quality-control-reporting
description: Use when you have uploaded a pre-analytical data table containing sample metadata, processing delay timestamps (pre- and post-centrifugation), and NMR metabolomic measurements for a cohort of plasma or serum samples, and you need to assess how processing delays affect metabolite concentrations and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
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

# nmr-metabolomic-quality-control-reporting

## Summary

Generate interactive performance reports for NMR-based metabolomic sample cohorts by quantifying the effect of processing delays on metabolic parameter stability. This skill produces delay-stratified metabolite change tables and data quality indicators suitable for pre-analytical quality control assessment in peripheral blood samples.

## When to use

You have uploaded a pre-analytical data table containing sample metadata, processing delay timestamps (pre- and post-centrifugation), and NMR metabolomic measurements for a cohort of plasma or serum samples, and you need to assess how processing delays affect metabolite concentrations and data quality across the cohort.

## When NOT to use

- Input samples are not from peripheral blood (plasma/serum); PRIMA-Panel is designed specifically for blood sample pre-analytical stability.
- Pre- and post-centrifugation delay metadata are not available or cannot be reliably parsed from timestamps.
- Metabolomic measurements are from non-NMR platforms (e.g., LC-MS, GC-MS); PRIMA-Panel is calibrated for NMR metabolomic data.
- The goal is to compare metabolomic profiles across independent cohorts rather than assess within-cohort pre-analytical quality.

## Inputs

- pre-analytical data table (TSV/CSV) with sample metadata, pre-centrifugation delay (minutes), post-centrifugation delay (minutes), and NMR metabolomic measurements (metabolite concentrations)
- cohort sample identifiers
- SPREC classification codes or delay timepoints

## Outputs

- interactive HTML performance report (downloadable)
- tabular performance report (CSV or other formats)
- delay-stratified metabolite change table with minor/major shift annotations
- cohort-level quality metrics (data quality degradation indicators)

## How to apply

Load the pre-analytical data table into PRIMA-Panel and parse/validate that required fields for cohort identification and pre/post-centrifugation delay annotation are present. Calculate metabolomic performance metrics by stratifying samples according to their pre-centrifugation and post-centrifugation delay windows (in minutes, sorted by SPREC classification), then compute minor and major metabolite concentration shifts and data quality degradation indicators for each metabolite within each delay stratum. Configure color thresholds (default % thresholds adjustable in the UI) to highlight clinically or analytically significant changes. Generate an interactive HTML or CSV performance report that cross-tabulates metabolites by delay windows and summarizes cohort-level statistics, enabling visual identification of delay-dependent metabolic instability patterns.

## Related tools

- **PRIMA-Panel** (Primary interactive data exploration and performance report generation platform for investigating processing delay effects on NMR metabolomic stability in blood sample cohorts) — https://github.com/funkam/PRIMA
- **QC-Tool** (Associated quality control tool repository (logo and supporting infrastructure)) — https://github.com/funkam/QC-Tool

## Evaluation signals

- Output report successfully parses and validates all required pre-analytical fields (sample ID, pre-centrifugation time, post-centrifugation time) with no missing values in critical columns.
- Metabolite changes are correctly stratified by delay windows; samples within the same delay window show consistent calculation of minor and major shift percentages.
- HTML report renders interactively and allows adjustment of color threshold parameters; adjustments propagate correctly to table cell highlighting.
- Exported CSV or HTML artifacts are valid; spot-check 5–10 metabolites to verify concentration shift calculations match expected % changes relative to a reference (e.g., shortest delay stratum).
- Cohort-level summary statistics (e.g., mean metabolite shift per delay window, data quality score by stratum) are present and non-null.

## Limitations

- PRIMA-Panel is validated only for peripheral blood samples (plasma/serum); applicability to other biofluids or tissue is unknown.
- Pre- and post-centrifugation delay information must be reliably captured in the input table; incomplete or misformatted timestamps will cause parsing errors.
- Color thresholds and % change cutoffs for 'minor' vs. 'major' metabolite shifts are user-adjustable but lack published clinical or analytical validation; threshold selection remains subjective.
- The tool does not account for individual metabolite-specific stability profiles or matrix-dependent degradation pathways; it applies uniform delay-window logic across all measured metabolites.

## Evidence

- [readme] Core tool definition: "The PRIMA-Panel is a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum)."
- [intro] Primary workflow input and output: "PRIMA-Panel allows the creation of so called performance reports for sample cohorts. Here a data table with pre-analytical information can be uploaded"
- [other] Data parsing and validation step: "Parse and validate the input table structure to ensure required fields for cohort identification and processing delay annotation are present."
- [other] Metric calculation method: "Calculate performance metrics quantifying the effect of processing delays on metabolic parameters (e.g., metabolite concentration shifts, data quality degradation) across the sample cohort."
- [readme] Delay stratification and report generation: "The 'Single' tab allows the user to set a pre-centrifugation time and a post-centrifugation using a Slider. A table is then generated that higlights a minor and a major change for each metabolite in"
- [readme] Output format options: "The table can be downloaded as a .HTML report or the table directly as .csv (or other formats)."
