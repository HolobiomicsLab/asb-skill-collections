---
name: metabolite-stability-assessment-across-cohorts
description: Use when you have uploaded a pre-analytical data table containing sample
  metadata, processing timestamps (pre- and post-centrifugation), and NMR metabolomic
  measurements for a cohort of peripheral blood samples (plasma/serum), and you need
  to quantify the magnitude and direction of metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - PRIMA-Panel
  - QC-Tool
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-stability-assessment-across-cohorts

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify how pre- and post-centrifugation processing delays affect metabolite concentrations and data quality across a sample cohort using NMR metabolomic measurements. This skill produces stratified performance reports that identify which metabolites are stable or degraded over defined delay windows, enabling prioritization of processing protocols.

## When to use

You have uploaded a pre-analytical data table containing sample metadata, processing timestamps (pre- and post-centrifugation), and NMR metabolomic measurements for a cohort of peripheral blood samples (plasma/serum), and you need to quantify the magnitude and direction of metabolite concentration shifts and data quality loss as a function of processing delay to assess cohort-level stability and generate actionable performance thresholds.

## When NOT to use

- Input data lacks paired pre- and post-centrifugation timestamps or SPREC delay classification — the skill requires explicit delay stratification to compute meaningful comparisons.
- Samples are from tissue or non-blood matrices — the tool is calibrated for peripheral blood (plasma/serum) pre-analytical effects and may not generalize.
- No reference time-point or minimal-delay control is available — the skill compares metabolite shifts relative to a baseline delay state; absence of this anchor undermines relative change calculation.

## Inputs

- Pre-analytical data table (tabular format: .csv, .xlsx, or similar) containing sample identifiers, pre-centrifugation delay (minutes), post-centrifugation delay (minutes), and NMR metabolomic measurements (metabolite names and concentration values)

## Outputs

- Performance report artifact (HTML or CSV table) with delay-stratified metabolite changes, cohort-level statistics (mean, variance by delay bin), data quality indicators, and color-coded stability flags (minor/major change thresholds)
- Interactive visualization dashboard (lollipop plots or alternative representations) showing metabolite stability across time-points by SPREC classification or custom delay grouping

## How to apply

Load the pre-analytical data table into PRIMA-Panel and parse the required fields: sample identifiers, pre- and post-centrifugation delay timestamps (converted to minutes), and corresponding NMR metabolomic measurements. Stratify the cohort by delay intervals (e.g., using SPREC classification or user-defined time-points). For each metabolite, calculate the absolute and relative concentration shift (% change) between the reference (minimal delay) and each delay stratum. Adjust minor and major change % thresholds according to your stability acceptance criteria (default thresholds provided in the tool). Generate a performance report table highlighting metabolites exceeding the major threshold for each delay window, with associated data quality indicators. Color-code entries to visualize stability patterns and export as HTML report or CSV for downstream visualization and threshold justification.

## Related tools

- **PRIMA-Panel** (Interactive data exploration and performance report generation for processing delay effects on metabolite stability; accepts pre-analytical metadata and NMR measurements, computes cohort-level delay-stratified metabolite shifts, and exports structured performance artifacts) — https://github.com/funkam/PRIMA
- **QC-Tool** (Quality control and pre-analytical data validation; supports timestamp parsing and SPREC classification) — https://github.com/funkam/QC-Tool

## Evaluation signals

- Output report contains all metabolites from the input table, with no missing or silently dropped entries; row and column counts match expected dimensions.
- Calculated % changes are directionally consistent with known metabolite stability biology (e.g., glucose and amino acids typically degrade over time; lipids may shift in predictable directions).
- Minor and major change thresholds are applied consistently across all delay strata; metabolites flagged as 'major change' exceed the user-specified % threshold in the corresponding delay bin.
- Cohort-level statistics (mean, SD, count by delay stratum) are internally consistent; counts sum to total sample size, and mean shifts are monotonic or show plausible non-monotonic patterns across increasing delay windows.
- Report can be successfully exported in HTML and CSV formats without data truncation or encoding errors; downstream visualization tools ingest the structured output without schema violations.

## Limitations

- The tool is optimized for peripheral blood (plasma/serum) samples; applicability to other matrices (cerebrospinal fluid, urine, tissue) is not validated.
- Performance thresholds (minor/major % change cutoffs) are user-adjustable but lack evidence-based guidance; practitioners must calibrate thresholds against their own stability acceptance criteria or existing literature standards.
- The skill assumes linear or piecewise-linear metabolite degradation over the observed delay range; non-linear or biphasic stability profiles may not be detected without binning strategy adjustment.
- NMR measurement noise and instrument drift are not explicitly modeled; data quality indicators reflect cohort-level variability but do not deconvolve pre-analytical effects from instrumental variation.
- Requires complete or near-complete metadata (timestamps, metabolite IDs); missing data in delay fields or sparse metabolite coverage will reduce report interpretability and cohort representativeness.

## Evidence

- [other] Workflow step 1: Load pre-analytical data table: "Load the pre-analytical data table (containing sample metadata, processing delay information, and NMR metabolomic measurements) into PRIMA-Panel."
- [other] Workflow step 3: Calculate performance metrics: "Calculate performance metrics quantifying the effect of processing delays on metabolic parameters (e.g., metabolite concentration shifts, data quality degradation) across the sample cohort."
- [intro] Core functionality: Tool investigates processing delay effects: "The PRIMA-Panel is a tool to investigate the effect of processing delays on metabolic parameters in samples of peripheral blood (plasma / serum)."
- [readme] Data module: Delay-stratified visualization: "The Data tab shows different ways of highlighting the different stability time-points in minutes. The time-points are sorted according to their SPREC classification."
- [readme] Performance report module: Threshold-based metabolite change detection: "A table is then generated that higlights a minor and a major change for each metabolite in that given timeframe. The colors, as well as the % threshholds, can be adjusted."
- [readme] Output artifact: Exportable structured report: "The table can be downloaded as a .HTML report or the table directly as .csv (or other formats)."
