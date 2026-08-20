---
name: time-temperature-degradation-modeling
description: Use when you are planning a blood sampling campaign and need to know
  whether specific lipid or polar-metabolite analytes will degrade during storage
  or processing delays at known temperatures, or you are troubleshooting retrospective
  stability concerns for analytes already measured under documented.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - Shiny
  - RStudio
  - ALISTER
  - RefMet Database
  license_tier: open
derived_from:
- doi: 10.1016/j.cca.2024.117858
  title: ALISTER
evidence_spans:
- ALISTER is a web-app containing scientific information on pre-analytical blood sample
  stability in metabolomics and lipidomics
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# time-temperature-degradation-modeling

## Summary

Reconstruct and validate the logic that maps analyte–matrix–time-delay–temperature inputs to stability assessments in ALISTER, enabling prospective selection of blood sampling protocols that preserve analyte integrity during pre-analytical processing. This skill applies literature-derived fold-change thresholds (default 20% single condition, 30% combined) to predict whether EDTA plasma or serum samples will remain suitable for metabolomics/lipidomics analysis.

## When to use

You are planning a blood sampling campaign and need to know whether specific lipid or polar-metabolite analytes will degrade during storage or processing delays at known temperatures, or you are troubleshooting retrospective stability concerns for analytes already measured under documented pre-analytical conditions (time delay before/after centrifugation, temperature before/after centrifugation).

## When NOT to use

- Your samples have already been processed under conditions not documented in ALISTER's database (e.g., exotic anticoagulants, room-temperature storage >24 hours, or non-standard centrifugation protocols) — the module's generalization may not apply reliably.
- You are analyzing analytes outside the current ALISTER scope: only EDTA plasma and serum are supported; other matrices (heparin, citrate, PAXGENE) and non-metabolomics/lipidomics analytes are out of scope.
- Your research question does not involve pre-analytical stability; e.g., you are assessing intra-assay precision, inter-individual variation, or post-analytical instrument drift.

## Inputs

- analyte name (lipid shorthand nomenclature or RefMet database identifier)
- matrix type (EDTA plasma or serum)
- temperature during processing (single value or split: pre-centrifugation and post-centrifugation)
- processing delay before centrifugation (hours or minutes)
- processing delay after centrifugation (hours or minutes)
- optional: user-defined stability fold-change thresholds (default 20%/30%)

## Outputs

- stability classification per analyte (stable, unstable, or borderline)
- fold-change estimate(s) for the input conditions
- protocol recommendation (sampling flowchart for prospective planning)
- visual indicator (icon or pie-chart summary) of expected stability under chosen protocol
- annotated CSV export with query conditions, output classifications, and literature citations
- optional: PDF flowchart of all possible sampling protocols

## How to apply

Access ALISTER's backend data structure (via the Shiny app or GitHub repository) to extract the stability decision rules encoded for your analyte–matrix pair. Input your pre-analytical conditions: matrix type (EDTA plasma or serum), temperature profile (constant or split before/after centrifugation), and processing delays (before and after centrifugation, recorded separately). The module will generalize your inputs to the nearest experimental conditions in the literature database and compute fold-change estimates for each condition independently, then combine them if multiple delays or temperatures apply. Compare the resulting fold-change against the stability thresholds (20% for single factors, 30% for combined), classify the analyte as stable, unstable, or borderline, and use the visual indicator and flowchart output to recommend or reject a sampling protocol. Validate by confirming that the output matches the app's prospective-scenario guidance and is consistent with cited reference data.

## Related tools

- **Shiny** (Interactive web-app framework for the ALISTER user interface and real-time stability query execution) — https://github.com/Fraunhofer-ITMP/alister
- **RStudio** (Development and deployment environment for ALISTER's Shiny application backend) — https://github.com/Fraunhofer-ITMP/alister
- **ALISTER** (Primary web-app containing the time–temperature degradation model and literature stability database for EDTA plasma and serum analytes) — https://github.com/Fraunhofer-ITMP/alister
- **RefMet Database** (Reference nomenclature for polar metabolite identifiers queried in ALISTER analyte search) — https://metabolomicsworkbench.shinyapps.io/refmet_name_search/

## Evaluation signals

- Returned fold-change estimate(s) lie within the known experimental ranges reported in cited literature for the same analyte–matrix–temperature–delay combination.
- Stability classification (stable/unstable) flips consistently at or near the defined threshold (20% single, 30% combined) when you vary a single input parameter (e.g., incrementing delay by 1 hour).
- Protocol recommendations generated by the 'Majority Vote' and 'Maximize stable analytes' modes produce non-empty flowcharts and pie-chart summaries that sum to 100% across all analytes.
- Downloaded CSV output contains all input conditions, fold-change values, stability classifications, and at least one citation matching a reference in the app's embedded database.
- Visual indicators (icons, pie charts) for the same query remain consistent across multiple app sessions or when exported and re-imported into the data filtering mode.

## Limitations

- Current ALISTER contents are limited to EDTA plasma and serum samples; other anticoagulants, matrices, and storage modalities are not supported.
- Time delay and temperature are the only pre-analytical factors modeled; other known pitfalls (e.g., hemolysis, sample contamination, freeze–thaw cycles, light exposure) are not yet integrated.
- When user-supplied pre-analytical conditions do not exactly match experimental data in the literature database, ALISTER applies generalization heuristics that may introduce approximation error; the hovering tooltip indicates how input was interpreted, but no confidence interval is provided.
- Stability thresholds (default 20% fold-change, 30% combined) are user-adjustable but not derived from formal statistical inference; they reflect consensus heuristics and may not be appropriate for all downstream assays or biomarker discovery contexts.
- No changelog is available in the repository, limiting traceability of updates to the underlying stability data or decision rules.
- Protocol search is currently available only for plasma samples, not serum.

## Evidence

- [intro] time_delay_temperature_major_factors: "Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples, which have been identified to be among the major pre-analytical"
- [intro] prospective_protocol_guidance: "In prospective scenarios the app aims to advise on sampling protocols, that ensure stability of analytes of interest"
- [readme] stability_threshold_20_30_percent: "By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before"
- [other] module_reconstruction_workflow: "Reconstruct the module logic that maps (analyte, matrix, time-delay, temperature) inputs to a stability assessment or protocol recommendation."
- [intro] retrospective_stability_assessment: "In retrospective assessment of samples, that ALISTER assesses analytes stability based on pre-analytical sample information provided by the user"
- [readme] generalization_heuristic: "In some cases, the database underlying ALISTER will not exactly match your conditions. In these cases, generalization needs to happen."
- [readme] analyte_search_details_output: "When clicking on 'Details' you can see a summary of the literature information that ALISTER bases its decision on, a generalized form of your input and whether the set individual threshold of fold"
