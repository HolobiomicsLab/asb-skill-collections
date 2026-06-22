---
name: metabolite-stability-database-retrieval
description: Use when you have measured metabolites or lipids from blood samples (plasma or serum) and need to assess whether quantitative results may be compromised by pre-analytical handling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Shiny
  - RStudio
  - ALISTER (web application)
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
---

# metabolite-stability-database-retrieval

## Summary

Query a curated pre-analytical stability database to retrieve analyte-specific stability assessments for blood plasma or serum samples under defined time-delay and temperature conditions. This skill enables both retrospective evaluation of existing samples and prospective protocol design for metabolomics and lipidomics studies.

## When to use

You have measured metabolites or lipids from blood samples (plasma or serum) and need to assess whether quantitative results may be compromised by pre-analytical handling. Specifically: you know the time delays (before and/or after centrifugation, in hours) and processing temperatures (°C) your samples experienced, and you need to cross-reference these against experimental stability data to flag analytes at risk of degradation (fold-change threshold: default 20% for single conditions, 30% for combined conditions).

## When NOT to use

- Your samples were processed under conditions not covered by ALISTER's current scope: matrices other than EDTA plasma or serum, or pre-analytical factors beyond time delay and temperature (e.g., pH, anticoagulant type, shipping method).
- You have no pre-analytical metadata for your samples; the skill requires explicit time-delay and temperature inputs to query the database.
- Your analyte identities do not match lipid shorthand or RefMet nomenclature; unrecognized compound names will not retrieve stability records.

## Inputs

- pre-analytical sample metadata: matrix type (EDTA plasma | serum)
- time delay before centrifugation (hours)
- time delay after centrifugation (hours)
- processing temperature before centrifugation (°C)
- processing temperature after centrifugation (°C, optional)
- analyte identities (lipid shorthand nomenclature or RefMet nomenclature for metabolites)
- stability threshold parameters (fold-change %, optional; default 20% single / 30% combined)

## Outputs

- analyte stability assessment table: analyte name, stability status (stable|degraded), fold-change magnitude, confidence metrics
- structured JSON or CSV with query conditions, assessed analytes, stability flags, and literature citations
- generalization warnings indicating which input conditions were approximated against database records
- visual summary (pie chart) of stability distribution across queried analytes

## How to apply

Parse your sample's pre-analytical parameters—matrix type (EDTA plasma or serum), time delay(s) before and after centrifugation (hours), and temperature(s) during processing (°C)—into a structured query. Submit this query to the ALISTER stability database, which will retrieve matching experimental records linking each analyte to its fold-change under those conditions. Compare the observed or expected fold-change against your stability threshold (adjustable; default 20% single, 30% combined). Analytes exceeding the threshold are flagged as 'degraded'; those within tolerance are 'stable'. The database will also return confidence metrics and literature citations supporting the stability assessment. Output results as a structured table or CSV annotated with stability status, fold-change magnitude, and generalization warnings where exact conditions were not available and approximation occurred.

## Related tools

- **ALISTER (web application)** (Interactive database interface for querying pre-analytical stability records; hosts the underlying stability database and provides retrospective and prospective search modes, threshold configuration, data filtering, and result export) — https://github.com/Fraunhofer-ITMP/alister
- **Shiny** (Web application framework used to build ALISTER's user interface and interactive query modules)
- **RStudio** (Development and deployment environment for the ALISTER Shiny application)

## Evaluation signals

- Retrieved stability records exactly or closely match the input matrix type (EDTA plasma or serum) and time-delay / temperature parameters; any generalization is flagged in the output.
- All returned analyte names conform to expected nomenclature (lipid shorthand or RefMet) and correspond to compounds in the input query.
- Stability assessments are reproducible: querying identical pre-analytical conditions returns the same fold-change values and stability flags across runs.
- Fold-change magnitudes are consistent with direction and magnitude of expected degradation (e.g., oxidized lipids or unstable metabolites show positive fold-change when incubated at elevated temperature for extended delay).
- CSV/JSON output schema includes all required fields: analyte identity, stability status, fold-change, confidence metrics, literature citations, and generalization warnings; no null or missing values for assessed analytes.

## Limitations

- Database scope is limited to time delay and temperature as pre-analytical variables; other factors (anticoagulant type, pH, storage container, shipping conditions) are not currently covered.
- Current data only include EDTA plasma and serum matrices; other anticoagulants or whole-blood preparations are not supported.
- Exact matches to user-provided conditions (time delay in hours, temperature in °C) are rare; the database will generalize to the nearest available experimental record and flag the approximation, which may introduce uncertainty.
- Threshold for fold-change (default 20% single condition, 30% combined) is static and may not reflect all biological or analytical requirements; users should adjust thresholds according to their analysis tolerance.
- Protocol search and prospective recommendations are currently available only for plasma samples, not serum.

## Evidence

- [intro] retrospective assessment of sample analyte stability based on pre-analytical information: "In retrospective assessment of samples, that ALISTER assesses analytes stability based on pre-analytical sample information provided by the user"
- [other] database query workflow with parsing and retrieval: "Parse user-provided pre-analytical parameters (time delay in hours, temperature in °C, matrix type: EDTA plasma or serum) into a structured query object. 2. Query the ALISTER stability database with"
- [other] structured JSON or table output format: "Format and return the stability assessment as a structured JSON or table output containing analyte identities, stability status (stable/degraded), and associated metadata."
- [intro] time delay and temperature as major pre-analytical factors: "Time delay and temperature during processing are among the major pre-analytical pitfalls affecting (EDTA) plasma and serum samples"
- [readme] fold-change threshold and generalization handling: "By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before"
- [readme] generalization and approximation of input conditions: "In some cases, the database underlying ALISTER will not exactly match your conditions. In these cases, generalization needs to happen. Hover your mouse over each analyte in order to see how your"
- [readme] nomenclature for analyte naming: "Lipids are named after the lipid shorthand nomenclature, while polar metabolites are named after their RefMet nomenclature"
