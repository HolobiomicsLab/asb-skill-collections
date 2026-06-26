---
name: pre-analytical-stability-assessment
description: Use when you have identified a set of lipid or polar metabolite analytes
  to measure from blood samples and need to determine whether they will remain stable
  under your planned or actual pre-analytical handling conditions (time delays before/after
  centrifugation and processing temperatures).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
  tools:
  - Shiny
  - RStudio
  - ALISTER
  license_tier: open
  provenance_tier: literature
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

# pre-analytical-stability-assessment

## Summary

Assess whether user-specified analytes (lipids or polar metabolites) will remain stable in EDTA plasma or serum samples under given time-delay and temperature conditions during pre-analytical processing. This skill uses ALISTER's prospective and retrospective modules to map (analyte, matrix, time-delay, temperature) inputs to stability classifications and protocol recommendations.

## When to use

You have identified a set of lipid or polar metabolite analytes to measure from blood samples and need to determine whether they will remain stable under your planned or actual pre-analytical handling conditions (time delays before/after centrifugation and processing temperatures). Use prospective assessment when designing a sampling protocol; use retrospective assessment when you already have samples with known pre-analytical history and want to flag analytes at risk of degradation.

## When NOT to use

- Your analytes include compounds outside lipids and polar metabolites (e.g., proteins, nucleic acids, or specialized biomarkers not in the ALISTER database).
- Your pre-analytical conditions include variables other than time delay and temperature (e.g., pH, light exposure, anticoagulant type beyond EDTA, or freeze–thaw cycles), which are not currently supported by ALISTER.
- You need retrospective assessment but do not know the exact time delays or temperatures your samples experienced during processing.

## Inputs

- analyte name(s) (lipid shorthand nomenclature or RefMet nomenclature for polar metabolites)
- matrix type (EDTA plasma or serum)
- processing temperature (°C, pre-centrifugation)
- processing temperature (°C, post-centrifugation, optional)
- time delay before centrifugation (minutes or hours)
- time delay after centrifugation (minutes or hours)
- stability threshold fold-change (optional; default 20% for single condition, 30% for combined)

## Outputs

- stability classification per analyte (stable/unstable/borderline or similar category)
- recommended sampling protocol (for prospective scenario)
- pie chart of stability distribution across selected analytes
- .csv file with query parameters, stability results, and literature citations
- visual indicator (icon) showing stability expectation under recommended protocol

## How to apply

1. Select the matrix type (EDTA plasma or serum) and analyte(s) of interest by name or compound class (lipid class or RefMet nomenclature for polar metabolites). 2. Specify the processing temperatures (pre- and post-centrifugation if they differ). 3. Input time delays before and after centrifugation, recognizing that these may affect analytes differently. 4. Set stability thresholds: the default is 20% fold-change for single conditions and 30% for combined conditions; adjust if stricter or more lenient assessment is needed. 5. Query ALISTER's underlying database to retrieve literature-derived stability classifications for your input conditions; the app will generalize your input to the nearest available experimental data if an exact match is not found. 6. Review the stability indicator for each analyte and the aggregated pie chart; download the .csv output with input conditions, stability classifications, and citations to supporting literature.

## Related tools

- **ALISTER** (Web application containing pre-analytical blood sample stability database and query interface for assessing analyte stability under specified time-delay and temperature conditions) — https://github.com/Fraunhofer-ITMP/alister
- **Shiny** (R web application framework used to implement ALISTER's interactive user interface and search modes)
- **RStudio** (Development and runtime environment for Shiny-based ALISTER deployment)

## Evaluation signals

- Output stability classifications agree with ALISTER's web-app results for the same (analyte, matrix, time-delay, temperature) input combination.
- Downloaded .csv output contains all input parameters, stability assessment, and at least one literature citation per analyte evaluated.
- Pie chart and per-analyte stability indicators correctly reflect the proportion of analytes classified in each stability category (stable/unstable/borderline) under the specified conditions.
- Recommended protocol (prospective scenario) is either the 'Majority Vote' consensus protocol or the strictest protocol that ensures stability for all selected analytes, depending on the user's choice.
- Generalization notices (displayed on hover in the app) show how input conditions were mapped to available experimental data, confirming that inexact condition matches were handled transparently.

## Limitations

- ALISTER currently covers only EDTA plasma and serum; other anticoagulants, matrices, or sample types are not supported.
- Current app functionality is limited to assessing influences of time delay and temperature; other pre-analytical variables (e.g., pH, light, freeze–thaw cycles, hemolysis) are not modeled.
- Analyte stability data are derived from published literature; if your specific analyte or conditions are not represented in the database, ALISTER generalizes to the nearest available data, which may introduce uncertainty.
- Lipids must be named in lipid shorthand nomenclature and polar metabolites in RefMet nomenclature; analytes using alternative naming conventions must be mapped manually or will not be recognized.
- The app does not account for interactions between analytes or matrix components; stability is assessed independently per analyte.

## Evidence

- [readme] Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples, which have been identified to be among the major pre-analytical: "Current app contents are limited to the influences of time delay and temperature during processing of (EDTA) plasma and serum samples, which have been identified to be among the major pre-analytical"
- [readme] In prospective scenarios the app aims to advise on sampling protocols, that ensure stability of analytes of interest: "In prospective scenarios the app aims to advise on sampling protocols, that ensure stability of analytes of interest"
- [readme] In retrospective assessment of samples, that ALISTER assesses analytes stability based on pre-analytical sample information provided by the user: "In retrospective assessment of samples, that ALISTER assesses analytes stability based on pre-analytical sample information provided by the user"
- [readme] By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before and after centrifugation) the threshold is expanded to 30%.: "By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before"
- [readme] Lipids are named after the lipid shorthand nomenclature, while polar metabolites are named after their RefMet nomenclature: "Lipids are named after the lipid shorthand nomenclature, while polar metabolites are named after their RefMet nomenclature"
- [readme] Experiments have shown, that for specific analytes or analyte classes it does matter, whether a time delay occurs before or after centrifugation.: "Experiments have shown, that for specific analytes or analyte classes it does matter, whether a time delay occurs before or after centrifugation"
- [readme] In some cases, the database underlying ALISTER will not exactly match your conditions. In these cases, generalization needs to happen.: "In some cases, the database underlying ALISTER will not exactly match your conditions. In these cases, generalization needs to happen"
