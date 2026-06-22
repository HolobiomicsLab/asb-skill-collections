---
name: pre-analytical-variable-encoding
description: 'Use when you have collected blood samples under specific pre-analytical conditions (known time delay before/after centrifugation in hours, processing temperature in °C, matrix type: EDTA plasma or serum) and need to query ALISTER''s stability database to assess whether analyte measurements should be.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3407
  tools:
  - Shiny
  - RStudio
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

# pre-analytical-variable-encoding

## Summary

Encode user-provided pre-analytical sample parameters (time delay, temperature, matrix type) into a structured query object suitable for database lookup. This skill bridges raw experimental metadata to ALISTER's stability assessment database by normalizing and validating input across prospective and retrospective scenarios.

## When to use

You have collected blood samples under specific pre-analytical conditions (known time delay before/after centrifugation in hours, processing temperature in °C, matrix type: EDTA plasma or serum) and need to query ALISTER's stability database to assess whether analyte measurements should be treated with caution. Use this skill when you possess exact or approximate pre-analytical metadata but lack a direct database key.

## When NOT to use

- Input samples have pre-analytical conditions outside ALISTER's scope: current app contents are limited to time delay and temperature effects on EDTA plasma and serum only; other matrices, anticoagulants, or variables (e.g., light exposure, pH) are not supported.
- You are designing prospective sampling protocols (use 'Protocol search' encoding instead, which optimizes for a recommended protocol rather than assessing existing conditions).
- Pre-analytical metadata is completely missing or unavailable; encoding requires at minimum matrix type and approximate time/temperature values to function.

## Inputs

- user-provided time delay before centrifugation (hours, numeric)
- user-provided time delay after centrifugation (hours, numeric)
- user-provided processing temperature (°C, numeric, or two temperatures if variable)
- matrix type selection (string: 'EDTA plasma' or 'serum')
- optional stability threshold overrides (numeric fold-change bounds)

## Outputs

- structured query object (JSON or internal representation) with normalized pre-analytical parameters
- generalization flag indicating whether exact match was found or approximation applied
- confidence metrics on parameter matching to available experimental data

## How to apply

Parse user-provided pre-analytical parameters into a structured query object that captures: (1) temperature (single value or two temperatures if different before/after centrifugation); (2) time delay before centrifugation (hours); (3) time delay after centrifugation (hours); (4) matrix type (EDTA plasma or serum). The object must encode whether conditions vary pre- vs. post-centrifugation, since ALISTER's literature basis shows analyte-specific sensitivity to delay timing. Apply generalization logic: if exact conditions are not in the database, the query encoder must select the closest matching experimental conditions from available literature data and flag the approximation confidence. This encoded object is then passed to the stability assessment lookup module, which retrieves matching analyte-stability records and thresholds (default 20% fold-change, expanded to 30% when conditions are combined).

## Related tools

- **Shiny** (Web application framework hosting the pre-analytical parameter input interface and query submission) — https://github.com/Fraunhofer-ITMP/alister
- **RStudio** (Development and deployment environment for ALISTER's query parsing and encoding logic) — https://github.com/Fraunhofer-ITMP/alister

## Evaluation signals

- Query object contains all four required fields (temperature, pre-centrifugation delay, post-centrifugation delay, matrix type) with correct data types (numeric for temporal/thermal parameters, string for matrix).
- Generalization flag is set to 'exact match' only when input parameters exactly match an experimental condition in ALISTER's literature database; otherwise flag should indicate which parameter(s) were approximated and the distance to nearest available data.
- Returned analyte-stability records are non-empty and contain only records matching the encoded matrix type (e.g., no serum analytes when EDTA plasma was encoded).
- Confidence metrics reflect the breadth and recency of literature supporting the matched condition; approximations to underrepresented condition combinations should receive lower confidence scores.
- Encoded object can be serialized to JSON and re-parsed without loss of information or type corruption.

## Limitations

- ALISTER's database is limited to EDTA plasma and serum; encoding cannot handle other anticoagulants (citrate, heparin) or non-blood matrices.
- Current app contents are limited to influences of time delay and temperature; other pre-analytical variables (light exposure, sample agitation, storage vessel material) cannot be encoded.
- Generalization logic relies on proximity matching in the literature space; if experimental data for a given condition combination is sparse, confidence in the stability assessment will be low.
- The encoding step does not validate whether user-provided conditions are physically realistic (e.g., negative time delays or temperatures outside typical laboratory ranges); downstream validation is required.
- No changelog is provided; the version of the stability database underlying the encoding is not explicitly tracked, potentially affecting reproducibility across deployments.

## Evidence

- [other] Parse user-provided pre-analytical parameters (time delay in hours, temperature in °C, matrix type: EDTA plasma or serum) into a structured query object.: "Parse user-provided pre-analytical parameters (time delay in hours, temperature in °C, matrix type: EDTA plasma or serum) into a structured query object."
- [intro] Time delay and temperature during processing are among the major pre-analytical pitfalls affecting (EDTA) plasma and serum samples: "Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples, which have been identified to be among the major pre-analytical"
- [readme] Experiments have shown, that for specific analytes or analyte classes it does matter, whether a time delay occurs before or after centrifugation.: "Experiments have shown, that for specific analytes or analyte classes it does matter, whether a time delay occurs before or after centrifugation."
- [readme] By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before and after centrifugation) the threshold is expanded to 30%.: "By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined the threshold is expanded to 30%."
- [readme] In some cases, the database underlying ALISTER will not exactly match your conditions. In these cases, generalization needs to happen.: "In some cases, the database underlying ALISTER will not exactly match your conditions. In these cases, generalization needs to happen."
