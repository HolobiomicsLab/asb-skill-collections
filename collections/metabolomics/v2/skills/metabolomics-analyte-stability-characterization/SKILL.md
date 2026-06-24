---
name: metabolomics-analyte-stability-characterization
description: Use when you are designing a blood sampling protocol for metabolomics
  or lipidomics analysis and need to predict whether specific analytes (polar metabolites
  or lipids) will degrade under planned pre-analytical conditions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3373
  tools:
  - Shiny
  - RStudio
  - ALISTER web-app
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

# metabolomics-analyte-stability-characterization

## Summary

Determine whether user-specified metabolites or lipids remain stable in EDTA plasma or serum under specific time-delay and temperature conditions during sample processing. This skill reconstructs and applies ALISTER's prospective-scenario module logic to map analyte–matrix–time–temperature inputs to binary or ranked stability assessments and sampling protocol recommendations.

## When to use

You are designing a blood sampling protocol for metabolomics or lipidomics analysis and need to predict whether specific analytes (polar metabolites or lipids) will degrade under planned pre-analytical conditions (e.g., room-temperature delays before centrifugation, or variable temperatures during sample processing). Use this skill when you must choose between competing sampling protocols or validate that a retrospectively recorded protocol will preserve analytes of interest.

## When NOT to use

- You are assessing analyte stability in non-blood matrices (e.g., urine, CSF, tissue homogenate) — ALISTER is limited to EDTA plasma and serum.
- Your analytes include compounds outside the lipid and polar-metabolite scope (e.g., proteins, nucleic acids) — ALISTER database does not cover these.
- You require stability data for sample storage conditions other than time-delay and temperature during processing (e.g., freeze–thaw cycles, long-term storage at −80 °C) — these are not in the current app scope.

## Inputs

- analyte name (string, RefMet nomenclature for polar metabolites or lipid shorthand nomenclature)
- matrix type (categorical: 'EDTA plasma' or 'serum')
- temperature before centrifugation (numeric, in degrees Celsius)
- temperature after centrifugation (numeric, optional)
- time delay before centrifugation (numeric, in minutes or hours)
- time delay after centrifugation (numeric, optional)
- stability threshold (numeric, fold-change cutoff; default 20% or 30%)

## Outputs

- stability status per analyte (categorical: 'stable', 'unstable', or 'marginal')
- recommended sampling protocol (discrete selection from protocol set, e.g., 'process immediately on ice', 'delay up to 2 h at room temperature')
- fold-change magnitude and direction (numeric, relative to threshold)
- literature citations supporting the stability assessment
- visualized protocol flowchart (PDF or SVG)

## How to apply

Access ALISTER's prospective-scenario module (via Shiny web-app at itmp.shinyapps.io/alister or GitHub repository) and specify: (1) matrix type (EDTA plasma or serum), (2) analyte name(s) (using lipid shorthand nomenclature or RefMet nomenclature for polar metabolites), (3) temperature(s) during processing (before and/or after centrifugation), and (4) time delays before and after centrifugation. The module queries its underlying stability database to extract fold-change thresholds for each analyte–condition combination. Stability is assessed by comparing observed or predicted fold change against a critical threshold (default 20% for single conditions, 30% when combined). The module returns a protocol recommendation ('stable under condition X', 'degrade under condition Y', or an optimal sampling protocol from a discrete set of alternatives). Validate by checking that the returned guidance is consistent with any reference literature cited by the app or with known analyte-stability relationships in your domain.

## Related tools

- **ALISTER web-app** (Primary tool hosting the prospective-scenario module, stability database, and protocol-recommendation engine; user interacts via Shiny interface to query analyte–condition combinations and retrieve stability assessments and protocol guidance.) — https://github.com/Fraunhofer-ITMP/alister
- **Shiny** (Web-application framework used to build ALISTER's interactive interface, including input forms for analyte/matrix/time/temperature specification and reactive rendering of stability visualizations and protocol recommendations.)
- **RStudio** (Development and deployment environment for ALISTER Shiny application.)

## Evaluation signals

- Returned stability status matches the direction and magnitude of fold-change relative to the specified (or default) threshold; e.g., if fold change is 25% and threshold is 20%, status should be 'unstable'.
- Protocol recommendation is one of the discrete protocols presented in ALISTER's protocol search output (e.g., 'immediate processing on ice', 'process within 2 h at room temperature'), not an arbitrary string.
- All cited literature in the stability assessment output appears in ALISTER's reference database and is retrievable via the app's 'Citation' button.
- Stability assessment is reproducible: running the same query (analyte, matrix, time, temperature) twice returns identical stability status and protocol recommendation.
- Generalization logic is transparent: when input conditions do not exactly match database experiments, the app indicates which conditions were approximated (visible on hover in the app UI), confirming that the module correctly interpolated or selected the nearest experimental record.

## Limitations

- ALISTER database scope is limited to influences of time delay and temperature during processing of EDTA plasma and serum samples; other pre-analytical factors (e.g., anticoagulant choice, storage at −80 °C, freeze–thaw cycles, hemolysis) are not covered.
- Analyte matching is exact: the input analyte name must match the app's database nomenclature (lipid shorthand or RefMet); misspellings or synonym use will fail to retrieve stability data.
- When input conditions do not exactly match experimental records in the database, ALISTER performs generalization (interpolation or selection of nearest conditions); the degree of uncertainty introduced by this generalization is not explicitly quantified in the current app version.
- Protocol search is currently only available for plasma samples; serum protocol recommendations are not yet supported.
- The critical fold-change threshold is a user-adjustable parameter (default 20% single, 30% combined); no statistical confidence interval or Bayesian credible region is provided, so the choice of threshold is empirical rather than evidence-based.

## Evidence

- [other] ALISTER's prospective module operates by advising on sampling protocols designed to ensure stability of analytes of interest, with current functionality limited to assessing influences of time delay and temperature during processing of EDTA plasma and serum samples.: "Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples, which have been identified to be among the major pre-analytical"
- [readme] The module maps (analyte, matrix, time-delay, temperature) inputs to a stability assessment or protocol recommendation, validated against the app's prospective scenario workflow.: "In prospective scenarios the app aims to advise on sampling protocols, that ensure stability of analytes of interest"
- [readme] Analytes are categorized by their main lipid class (lipids) or RefMet nomenclature (polar metabolites) and must be matched exactly in the database.: "Lipids are named after the lipid shorthand nomenclature, while polar metabolites are named after their RefMet nomenclature"
- [readme] Critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions; when conditions are combined, threshold is expanded to 30%.: "By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before"
- [readme] When input conditions do not exactly match database experiments, generalization occurs; users can inspect how their input was approximated by hovering over results.: "In some cases, the database underlying ALISTER will not exactly match your conditions. In these cases, generalization needs to happen. Hover your mouse over each analyte in order to see how your"
