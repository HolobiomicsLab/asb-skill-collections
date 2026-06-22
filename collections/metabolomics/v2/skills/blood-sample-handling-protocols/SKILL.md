---
name: blood-sample-handling-protocols
description: Use when you are planning a blood sampling campaign and need to verify that lipids or polar metabolites of interest will remain stable through your anticipated sample-processing workflow (specific temperature regimes, delays before/after centrifugation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - Shiny
  - RStudio
  - ALISTER
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

# blood-sample-handling-protocols

## Summary

Reconstruct and apply ALISTER's prospective sampling protocol advisory module to determine whether user-specified analytes remain stable in EDTA plasma or serum under specified time-delay and temperature conditions. This skill bridges pre-analytical study design with metabolomics/lipidomics data quality by encoding stability thresholds and decision rules into actionable sampling recommendations.

## When to use

You are planning a blood sampling campaign and need to verify that lipids or polar metabolites of interest will remain stable through your anticipated sample-processing workflow (specific temperature regimes, delays before/after centrifugation). Use this skill when you have: (1) a defined set of target analytes; (2) known or controllable time delays and temperatures during sample collection and processing; (3) a need for prospective protocol recommendations rather than post-hoc stability assessment.

## When NOT to use

- Your analytes are not in ALISTER's database (non-standard nomenclature, non-lipid/non-polar-metabolite compounds, or matrices other than EDTA plasma/serum).
- You are performing retrospective stability assessment of already-collected samples; use Sample Search, Analyte Search (Details tab), or Data Filtering Mode instead.
- Your pre-analytical conditions involve variables not encoded in ALISTER (e.g., anticoagulants other than EDTA, freeze–thaw cycles, light exposure, or chemical additives).

## Inputs

- Target analyte list (lipid shorthand nomenclature or RefMet polar metabolite names)
- Sample matrix (EDTA plasma or serum)
- Processing temperature (single or bifurcated pre/post-centrifugation)
- Time delay before centrifugation (hours or minutes)
- Time delay after centrifugation (hours or minutes)
- Optional custom stability thresholds (fold-change limits, upper/lower bounds)

## Outputs

- Recommended sampling protocol (time and temperature parameters)
- Per-analyte stability classification (stable/unstable) under recommended protocol
- Stability pie chart (percentage distribution across stability categories)
- Protocol flow-chart visualization
- Annotated .csv file (input conditions + stability assessments + citations)
- Literature references supporting each analyte's stability decision

## How to apply

Access ALISTER's Protocol Search or Analyte Search interface (Shiny web app or RStudio environment) and input your target analyte classes (lipid shorthand nomenclature or RefMet-named polar metabolites), processing temperature(s), and time delays before/after centrifugation. The app maps (analyte, matrix, time-delay, temperature) tuples to experimental stability literature and applies critical thresholds (default 20% fold-change for single conditions, 30% for combined conditions) to classify each analyte as stable or unstable. Select either 'Majority Vote' (recommended protocol for most analytes) or 'Maximize stable analytes' (strictest protocol ensuring stability for maximum coverage). Validate the returned protocol recommendations by cross-checking against the app's embedded literature citations and examining the visual stability pie chart and per-analyte flow-chart indicators. Download the annotated .csv output containing input conditions, stability classifications, and all relevant references for protocol documentation.

## Related tools

- **Shiny** (Web application framework hosting the ALISTER interactive interface for protocol search and stability recommendation) — https://github.com/Fraunhofer-ITMP/alister
- **RStudio** (Development and execution environment for Shiny backend and data processing logic) — https://github.com/Fraunhofer-ITMP/alister
- **ALISTER** (Core web application containing pre-analytical blood sample stability database, literature-backed stability thresholds, and protocol recommendation engine) — https://github.com/Fraunhofer-ITMP/alister

## Evaluation signals

- Returned protocol specifies explicit time windows (hours or minutes) and temperature setpoints (°C) that match user inputs or reasonable generalizations thereof.
- All analytes in the selected classes receive a stability icon (checkmark or warning) consistent with their fold-change relative to the chosen threshold (default 20% single, 30% combined).
- Pie chart proportions sum to 100% and reflect all analytes in the input set, with no missing classifications.
- Each analyte's stability decision is traceable to at least one literature citation accessible via the app's 'Citation' tab; citations should appear in output .csv.
- Protocol recommendation differs meaningfully between 'Majority Vote' and 'Maximize stable analytes' modes; the latter should be stricter (lower temperature, shorter delays) or unchanged.
- Downloaded .csv contains 'Variable explanation' tab documenting how input conditions were generalized to match experimental data in ALISTER's backend.

## Limitations

- Current ALISTER functionality is limited to EDTA plasma and serum; other anticoagulants and matrices are not supported.
- Only time-delay and temperature variables are modeled; other pre-analytical pitfalls (light exposure, freeze–thaw, chemical additives) are not considered.
- For conditions not exactly matching experimental data, ALISTER generalizes; hover tooltips and the Details tab in Analyte Search reveal the approximation used, but generalization error bounds are not quantified.
- Protocol Search is currently available for plasma samples only; serum users must use Analyte Search.
- Stability thresholds are user-adjustable but default to 20% / 30% fold-change; different analytical platforms or acceptance criteria may warrant recalibration outside ALISTER's scope.
- No changelog is maintained, making it difficult to assess whether the underlying literature database or decision rules have been updated.

## Evidence

- [other] how does the prospective sampling protocol guidance module in ALISTER determine whether a user-specified analyte will remain stable in EDTA plasma or serum given specific time-delay and temperature conditions: "How does the prospective sampling protocol guidance module in ALISTER determine whether a user-specified analyte will remain stable in EDTA plasma or serum given specific time-delay and temperature"
- [other] prospective module operates by advising on sampling protocols designed to ensure stability of analytes of interest, with current functionality limited to assessing influences of time delay and temperature during processing: "ALISTER's prospective module operates by advising on sampling protocols designed to ensure stability of analytes of interest, with current functionality limited to assessing influences of time delay"
- [other] extract the time-delay and temperature factors (ranges, critical thresholds, or decision rules) that govern analyte stability from the app's backend or configuration files: "Extract the time-delay and temperature factors (ranges, critical thresholds, or decision rules) that govern analyte stability from the app's backend or configuration files."
- [other] reconstruct the module logic that maps (analyte, matrix, time-delay, temperature) inputs to a stability assessment or protocol recommendation: "Reconstruct the module logic that maps (analyte, matrix, time-delay, temperature) inputs to a stability assessment or protocol recommendation."
- [readme] In prospective scenarios the app aims to advise on sampling protocols, that ensure stability of analytes of interest: "In prospective scenarios the app aims to advise on sampling protocols, that ensure stability of analytes of interest."
- [readme] Protocol search is used in the following way: 1. As for the 'Sample search', you can choose the specific analyte classes of interest. 2. If you want to receive the sampling protocol that is recommended in most cases for the selected analytes, choose 'Majority Vote' (default). In other cases, you might want to choose the strictest protocol in order to ensure stability for the maximum number of selected analytes. For this, choose 'Maximize stable analytes'.: "If you want to receive the sampling protocol that is recommended in most cases for the selected analytes, choose 'Majority Vote' (default). In other cases, you might want to choose the strictest"
- [readme] By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before and after centrifugation) the threshold is expanded to 30%.: "By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before"
- [readme] You can download a .csv-file containing your query, as well as the output and all relevant references.: "You can download a .csv-file containing your query, as well as the output and all relevant references."
- [readme] Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples, which have been identified to be among the major pre-analytical pitfalls: "Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples, which have been identified to be among the major pre-analytical"
