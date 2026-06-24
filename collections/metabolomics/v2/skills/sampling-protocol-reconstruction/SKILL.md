---
name: sampling-protocol-reconstruction
description: Use when you have access to ALISTER's web app or codebase and need to
  understand, validate, or replicate the internal logic that maps (analyte, matrix,
  time-delay, temperature) tuples to stability assessments and protocol recommendations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3407
  tools:
  - Shiny
  - RStudio
  - ALISTER (Fraunhofer-ITMP/alister)
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

# Reconstruct the prospective-scenario sampling-protocol advisory module

## Summary

Extract and reverse-engineer the decision logic underlying ALISTER's prospective sampling protocol module to determine which time-delay and temperature combinations will maintain stability of user-specified analytes in EDTA plasma or serum. This skill enables reconstruction of the analyte-matrix-condition-to-recommendation mapping that governs protocol guidance.

## When to use

You have access to ALISTER's web app or codebase and need to understand, validate, or replicate the internal logic that maps (analyte, matrix, time-delay, temperature) tuples to stability assessments and protocol recommendations. Use this skill when the prospective workflow output must be explained, audited, or ported to a new system, or when you need to verify that guidance aligns with known analyte-stability relationships from literature.

## When NOT to use

- Your task is retrospective assessment of already-collected samples: use 'Sample search' or 'Data filtering mode' instead to classify measured analytes against known pre-analytical conditions.
- You need guidance for a single analyte without protocol exploration: use 'Analyte search' directly rather than reverse-engineering the underlying module.
- You are working with analytes or matrices outside ALISTER's scope (non-EDTA matrices, or analyte classes not in metabolomics/lipidomics).

## Inputs

- ALISTER Shiny app instance (live or local)
- ALISTER GitHub repository codebase (Fraunhofer-ITMP/alister)
- Analyte-matrix-condition stability database or configuration files
- User-specified analyte names (lipid shorthand nomenclature or RefMet nomenclature for polar metabolites)
- Temperature parameters (pre- and post-centrifugation, in °C)
- Time-delay parameters (before and after centrifugation, in minutes or hours)

## Outputs

- Reconstructed decision logic mapping (analyte, matrix, time-delay, temperature) → stability classification
- Extracted stability thresholds and fold-change cutoff rules
- Protocol recommendation rules (e.g., 'Majority Vote' selection logic)
- Validation report comparing reconstructed outputs against app prospective workflow
- Documented generalization rules for conditions not exactly matching experimental data

## How to apply

Access ALISTER via the Shiny web-app or GitHub repository (Fraunhofer-ITMP/alister) and identify the data structure encoding stability thresholds for each (analyte, matrix) pair. Extract the critical time-delay and temperature parameters (e.g., ranges, fold-change cutoffs, decision thresholds) that trigger stability or instability classifications from the backend configuration or app logic. Reconstruct the module's decision rules by mapping observed user inputs (e.g., 'time delay before centrifugation = 30 min, temperature = 4 °C') to expected outputs (e.g., 'stable' or 'degradation risk'). Cross-validate the reconstructed logic against the app's prospective workflow for consistency (e.g., 'Majority Vote' vs. 'Maximize stable analytes' branches) and against reference literature cited within the app or its download outputs. Document the stability thresholds (default: 20% fold-change single condition, 30% combined conditions) and any generalization rules applied when exact experimental data are unavailable.

## Related tools

- **Shiny** (Web application framework hosting ALISTER's prospective-scenario protocol advisory interface and decision logic execution) — https://github.com/Fraunhofer-ITMP/alister
- **RStudio** (Development and execution environment for R-based Shiny application logic and backend data queries) — https://github.com/Fraunhofer-ITMP/alister
- **ALISTER (Fraunhofer-ITMP/alister)** (Source application containing the prospective sampling-protocol module logic to be reconstructed) — https://github.com/Fraunhofer-ITMP/alister

## Evaluation signals

- Reconstructed logic returns stability classifications ('stable', 'unstable', or degradation warning) consistent with ALISTER's prospective workflow output for ≥90% of test analyte-condition combinations.
- Extracted fold-change thresholds match documented defaults (20% for single conditions, 30% for combined time-delay and temperature) and are applied correctly in decision rules.
- Protocol recommendations ('Majority Vote' vs. 'Maximize stable analytes') are reproducible from reconstructed logic and align with app-generated flowchart outputs.
- Generalization rules (used when exact experimental match is unavailable) are documented and validated against app hover-over explanations or 'Details' panels.
- All stability assessments can be traced to underlying literature sources cited in app downloads or citation links, confirming that reconstructed logic does not introduce unexplained divergence from reference data.

## Limitations

- ALISTER's underlying stability database is limited to EDTA plasma and serum matrices; reconstruction cannot extend to other matrices (e.g., lithium heparin, PAXGENE) or collection tubes not represented in the app.
- Current app contents are limited to time-delay and temperature influences; other pre-analytical factors (pH, hemolysis, lipemia) are not encoded and cannot be reconstructed from this module.
- When exact experimental data do not match user-specified conditions, ALISTER applies generalization rules that may not be fully documented in the UI; reverse-engineering these rules requires access to backend configuration or codebase inspection.
- No changelog is available for ALISTER, so historical changes to threshold values or decision logic cannot be tracked, and reconstructed logic may diverge between app versions.
- Protocol search functionality is currently only available for plasma samples, limiting reconstruction scope for serum-based prospective protocols.

## Evidence

- [readme] In prospective scenarios the app aims to advise on sampling protocols, that ensure stability of analytes of interest: "In prospective scenarios the app aims to advise on sampling protocols, that ensure stability of analytes of interest"
- [readme] Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples: "Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples"
- [readme] By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before and after centrifugation) the threshold is expanded to 30%.: "By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined the threshold is expanded to 30%"
- [readme] If you want to receive the sampling protocol that is recommended in most cases for the selected analytes, choose 'Majority Vote' (default). In other cases, you might want to choose the strictest protocol in order to ensure stability for the maximum number of selected analytes.: "If you want to receive the sampling protocol that is recommended in most cases for the selected analytes, choose 'Majority Vote' (default). In other cases, you might want to choose the strictest"
- [readme] In some cases, the database underlying ALISTER will not exactly match your conditions. In these cases, generalization needs to happen.: "In some cases, the database underlying ALISTER will not exactly match your conditions. In these cases, generalization needs to happen"
