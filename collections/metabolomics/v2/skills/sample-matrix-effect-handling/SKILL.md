---
name: sample-matrix-effect-handling
description: Use when you have measured metabolites or lipids from archival blood samples (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Shiny
  - RStudio
  - ALISTER (web-app)
derived_from:
- doi: 10.1016/j.cca.2024.117858
  title: ALISTER
evidence_spans:
- ALISTER is a web-app containing scientific information on pre-analytical blood sample stability in metabolomics and lipidomics
- '[![](https://img.shields.io/badge/Shiny-shinyapps.io-blue?style=flat&labelColor=white&logo=RStudio&logoColor=blue)]'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_alister_cq
    doi: 10.1016/j.cca.2024.117858
    title: ALISTER
  dedup_kept_from: coll_alister_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.cca.2024.117858
  all_source_dois:
  - 10.1016/j.cca.2024.117858
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-matrix-effect-handling

## Summary

Assess and interpret how blood sample matrix type (EDTA plasma or serum) and pre-analytical conditions (time delay, temperature) affect analyte stability in metabolomics and lipidomics. This skill enables retrospective evaluation of whether measurement results should be treated with caution or filtered from analysis based on documented sample processing history.

## When to use

You have measured metabolites or lipids from archival blood samples (e.g., biobank samples) with documented pre-analytical metadata (collection time, storage temperature, time before/after centrifugation, matrix type), and need to determine whether results are reliable or should be flagged as potentially degraded before statistical analysis or reporting.

## When NOT to use

- Sample matrix is not blood plasma or serum (ALISTER is limited to these two matrices).
- Pre-analytical metadata (time delay, temperature, centrifugation timing) is not available or cannot be documented.
- Analyte names do not match ALISTER database nomenclature (lipid shorthand or RefMet); unmapped analytes cannot be queried.

## Inputs

- Pre-analytical metadata: time delay (hours), temperature (°C), matrix type (EDTA plasma or serum)
- Measured analyte list or sample×analyte measurement table (CSV format, lipids in shorthand nomenclature, polar metabolites in RefMet nomenclature)
- Optional: user-defined stability fold-change thresholds

## Outputs

- Analyte stability assessment (stable/degraded) per analyte per sample or query
- Annotated dataset (CSV) with unstable analytes flagged
- Stability confidence metrics and generalized experimental conditions supporting each assessment
- Pie chart summarizing overall stability category distribution

## How to apply

Parse user-provided pre-analytical parameters (time delay in hours before and after centrifugation, temperature in °C, matrix type: EDTA plasma or serum) into a structured query. Query the ALISTER stability database with these normalized parameters to retrieve matching analyte–stability records, including stability flag (stable/degraded) and confidence metrics. Assess each measured analyte against a fold-change threshold (default 20% for single conditions, 30% for combined conditions); flag analytes as unstable if expected degradation exceeds the threshold. Return a structured output (JSON or CSV) mapping analyte identity to stability status and generalized experimental conditions that informed the assessment. Use the hover/details interface to verify how input conditions were approximated against available experimental literature.

## Related tools

- **ALISTER (web-app)** (Hosts the stability database, query engine, and unified interface for retrospective matrix-effect assessment via Sample Search, Analyte Search, and Data Filtering Mode modules.) — https://github.com/Fraunhofer-ITMP/alister
- **Shiny** (Renders the interactive web interface for parameter input, result visualization, and data download.)
- **RStudio** (Development and deployment environment for ALISTER application.)

## Evaluation signals

- All measured analytes in the input table are successfully mapped to ALISTER database entries and return a stability classification (stable/degraded) with non-null confidence or literature support.
- Stability assessment aligns with fold-change thresholds: analytes flagged as unstable have expected degradation ≥ 20% (single conditions) or ≥ 30% (combined conditions) under the stated pre-analytical conditions.
- Hover/details output for each flagged analyte confirms that the input pre-analytical parameters (time, temperature, centrifugation sequence) were correctly interpreted and matched to the most similar available experimental literature.
- Downloaded CSV output contains input metadata, analyte names, stability status, and generalized condition approximations for each row; no unmapped analytes are silently dropped.
- Pie chart and flagged-analyte count match the total number of analytes queried and stability classifications assigned.

## Limitations

- ALISTER currently covers only time delay and temperature as pre-analytical variables; other factors (e.g., anticoagulant type beyond EDTA, pH, light exposure) are not modeled.
- Database is limited to EDTA plasma and serum; other blood fractions (e.g., whole blood, cerebrospinal fluid) are out of scope.
- When user-provided conditions do not exactly match experimental data in the database, generalization and interpolation are applied; hover details must be reviewed to confirm the approximation is acceptable for the study context.
- Stability thresholds are user-adjustable but default values (20%/30% fold-change) may not reflect all regulatory or publication standards; threshold choice should be justified before analysis.
- No changelog or version history is provided; updates to the underlying stability database are not transparently communicated.

## Evidence

- [readme] In retrospective assessment of samples, that ALISTER assesses analytes stability based on pre-analytical sample information provided by the user: "In retrospective assessment of samples, that ALISTER assesses analytes stability based on pre-analytical sample information provided by the user"
- [readme] Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples, which have been identified to be among the major pre-analytical pitfalls.: "Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples, which have been identified to be among the major pre-analytical"
- [other] Parse user-provided pre-analytical parameters (time delay in hours, temperature in °C, matrix type: EDTA plasma or serum) into a structured query object. 2. Query the ALISTER stability database with the parsed parameters to retrieve matching analyte-stability records (analyte name, stability flag, confidence metrics).: "Parse user-provided pre-analytical parameters (time delay in hours, temperature in °C, matrix type: EDTA plasma or serum) into a structured query object. 2. Query the ALISTER stability database with"
- [readme] By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before and after centrifugation) the threshold is expanded to 30%.: "By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before"
- [readme] Lipids are named after the lipid shorthand nomenclature, while polar metabolites are named after their RefMet nomenclature.: "Lipids are named after the lipid shorthand nomenclature, while polar metabolites are named after their RefMet nomenclature"
