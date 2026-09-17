---
name: blood-sample-processing-parameter-extraction
description: Use when when you have peripheral blood sample cohorts (plasma/serum)
  with multiple timestamps (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# blood-sample-processing-parameter-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract pre- and post-centrifugation processing delay times from date+time stamp differences in peripheral blood sample metadata to enable stratified analysis of processing effects on NMR metabolomic measurements. This skill is essential for quantifying and annotating the pre-analytical variables that drive metabolite stability variation.

## When to use

When you have peripheral blood sample cohorts (plasma/serum) with multiple timestamps (e.g., collection time, centrifugation start/end times) recorded as date+time stamps, and you need to compute precise processing delay intervals to stratify downstream metabolomic stability or quality assessments. Specifically use this when preparing cohort metadata for PRIMA-Panel performance report generation or when investigating the effect of processing delays on metabolic parameter shifts.

## When NOT to use

- Input timestamps are already pre-computed as delay intervals (e.g., 'delay_minutes' column already present)
- Sample cohort lacks timestamp data or timestamps are in unstructured/incomplete formats
- Analysis goal does not require stratification by processing delay (e.g., cross-sectional snapshot with no temporal variation)

## Inputs

- sample metadata table with date+time stamp columns (collection_datetime, centrifugation_start_datetime, centrifugation_end_datetime or equivalent)
- peripheral blood sample records (plasma or serum)

## Outputs

- pre-centrifugation delay in minutes (per sample)
- post-centrifugation delay in minutes (per sample)
- SPREC time-point classification (per sample)
- annotated cohort metadata table with delay columns

## How to apply

Parse the date+time stamp fields in your sample metadata table to compute two delay intervals: (1) pre-centrifugation delay (time from collection to centrifugation start), and (2) post-centrifugation delay (time from centrifugation end to downstream processing or freezing). Calculate the elapsed time in minutes for each interval. Validate that all required timestamp fields are present and in consistent format. Assign each sample to SPREC (Standard PREanalytical Code) time-point classifications based on the computed delays. Use these extracted delay values as cohort stratification dimensions in subsequent metabolite change calculations and performance metric aggregation.

## Related tools

- **PRIMA-Panel** (downstream consumer of extracted processing delays; uses pre- and post-centrifugation times to stratify metabolite change calculations and generate delay-stratified performance reports) — https://github.com/funkam/PRIMA
- **QC-Tool** (supporting visualization and QC infrastructure for PRIMA-Panel) — https://github.com/funkam/QC-Tool

## Evaluation signals

- All samples in the cohort have non-null pre-centrifugation and post-centrifugation delay values (in minutes) with plausible ranges (e.g., 0–120 minutes for pre-centrifugation, 0–480 minutes for post-centrifugation storage before freezing)
- SPREC classifications match expected time-point buckets (e.g., samples with <2 hr pre-centrifugation delay are classified in the appropriate stability tier)
- Delay values are consistent with documented sample handling protocols (e.g., no negative delays, no implausibly long post-centrifugation intervals for frozen samples)
- Downstream PRIMA-Panel performance report correctly stratifies metabolite changes by the extracted delay intervals without errors or missing cohorts
- Timestamp differences resolve to integers or precise fractional minutes with no rounding artifacts that obscure clinically relevant delay boundaries

## Limitations

- Requires accurate and complete timestamp recording at collection, centrifugation start, and centrifugation end; missing or incorrectly recorded timestamps will produce invalid or missing delay estimates
- Time zone or daylight saving time inconsistencies in timestamp data can introduce systematic bias in delay calculations
- The skill extracts only elapsed time intervals; it does not capture other pre-analytical variables (e.g., sample temperature, handling method, anticoagulant type) that also affect metabolite stability
- Precision of delay extraction is limited by the temporal resolution of recorded timestamps (e.g., minute-level precision will not resolve sub-minute processing variations)

## Evidence

- [readme] An additional tab for Tools is available. Currently it consists of a tool for calculating the pre- and post-centrifugation times from the differences of date+time stamps.: "a tool for calculating the pre- and post-centrifugation times from the differences of date+time stamps"
- [other] Load the pre-analytical data table (containing sample metadata, processing delay information, and NMR metabolomic measurements) into PRIMA-Panel.: "pre-analytical data table (containing sample metadata, processing delay information, and NMR metabolomic measurements)"
- [readme] The Data tab shows different ways of highlighting the different stability time-points in minutes. The time-points are sorted according to their SPREC classification.: "stability time-points in minutes. The time-points are sorted according to their SPREC classification"
- [other] Parse and validate the input table structure to ensure required fields for cohort identification and processing delay annotation are present.: "Parse and validate the input table structure to ensure required fields for cohort identification and processing delay annotation are present"
