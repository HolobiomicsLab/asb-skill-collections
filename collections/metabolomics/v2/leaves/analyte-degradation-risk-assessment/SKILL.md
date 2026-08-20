---
name: analyte-degradation-risk-assessment
description: Use when you have measured metabolites or lipids from biobanked or processed
  blood samples (EDTA plasma or serum) and know the pre-analytical conditions (time
  delay before/after centrifugation in hours, processing temperature in °C, sample
  matrix).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Shiny
  - RStudio
  - ALISTER (web app)
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

# analyte-degradation-risk-assessment

## Summary

Assess whether blood-derived metabolite and lipid analytes have degraded or remain stable under known pre-analytical conditions (time delay, temperature, matrix type). This skill enables retrospective evaluation of measurement reliability in metabolomics and lipidomics datasets by querying experimental stability data.

## When to use

You have measured metabolites or lipids from biobanked or processed blood samples (EDTA plasma or serum) and know the pre-analytical conditions (time delay before/after centrifugation in hours, processing temperature in °C, sample matrix). You need to flag which analytes may have degraded beyond a stability threshold (default 20–30% fold-change) and thus require cautious interpretation or exclusion from downstream analysis.

## When NOT to use

- Sample matrix is not EDTA plasma or serum (e.g., whole blood, urine, cerebrospinal fluid); ALISTER currently only covers these two matrices.
- Pre-analytical conditions are completely unknown or poorly documented; the skill requires explicit numeric input for time delays and temperatures to query the database.
- The analyte names do not conform to lipid shorthand nomenclature or RefMet nomenclature; automatic matching will fail and manual curation is required.

## Inputs

- pre-analytical sample metadata (time delay hours before centrifugation, time delay hours after centrifugation, temperature °C before centrifugation, temperature °C after centrifugation, matrix type: EDTA plasma or serum)
- analyte name list (lipid shorthand nomenclature or RefMet nomenclature for polar metabolites)
- optional: measured analyte abundance table (rows=samples, columns=analytes; .csv format)

## Outputs

- analyte stability assessment table (analyte name, stability flag: stable/degraded, fold-change estimate, confidence/generalization metrics, literature citations)
- aggregated stability summary (pie chart or percentage breakdown of stable vs. degraded analytes under input conditions)
- annotated dataset (input analyte table with instability flags appended; for data filtering mode)
- downloadable .csv or PDF report containing query parameters, stability results, and reference metadata

## How to apply

Parse the known pre-analytical parameters (time delay before centrifugation, time delay after centrifugation, temperature pre- and post-centrifugation, matrix type) into a structured query. Submit this query against ALISTER's underlying stability database, which returns literature-derived stability assessments for each analyte under the matched or generalized conditions. Stability is assessed as a binary flag (stable/degraded) and a fold-change metric. Apply the default 20% threshold for single pre-analytical conditions or 30% for combined conditions; adjust thresholds if stricter or more permissive criteria are needed. Return a structured output (CSV or JSON) annotating each analyte with its stability status, fold-change estimate, confidence metadata, and supporting literature citations. Use the confidence or generalization metrics to assess how closely the database matched your exact input conditions.

## Related tools

- **ALISTER (web app)** (Query interface and stability database engine for retrospective and prospective pre-analytical stability assessment) — https://github.com/Fraunhofer-ITMP/alister
- **Shiny** (User interface framework for the web app)
- **RStudio** (Development and deployment environment)

## Evaluation signals

- Stability status (stable/degraded) aligns with literature-reported fold-change thresholds: ≤20% fold-change under single condition = stable; >20% or combined conditions >30% = degraded.
- Analyte names are successfully matched against ALISTER's database; unmatched analytes are logged or flagged for manual review.
- Confidence/generalization metrics indicate how closely the queried conditions matched available experimental data; high confidence suggests direct literature support, low confidence indicates interpolation or extrapolation.
- Output structure is valid (JSON schema or CSV headers) and includes mandatory fields: analyte identity, stability flag, fold-change estimate, and at least one citation.
- When data filtering mode is used, unstable analytes are consistently flagged in the output and can be filtered from downstream analysis; filtering produces a subset table with reduced analyte count and matched sample rows.

## Limitations

- Database coverage is limited to influences of time delay and temperature; other pre-analytical variables (e.g., pH, anticoagulant batch, centrifuge speed) are not currently modeled.
- Only EDTA plasma and serum matrices are supported; other blood fractionation methods or tissues are out of scope.
- When exact experimental conditions are not in the database, ALISTER performs generalization (interpolation or nearest-neighbor matching); the degree and direction of generalization is reported but may reduce confidence in edge cases.
- Analytes must be named in lipid shorthand nomenclature or RefMet nomenclature; common names or non-standard identifiers will not match and require manual curation.
- Stability assessment is based on aggregate literature data and does not account for sample-specific factors (e.g., individual variation in enzyme activity, hemolysis, lipemia) that may affect real-world degradation kinetics.

## Evidence

- [readme] In retrospective assessment of samples, that ALISTER assesses analytes stability based on pre-analytical sample information provided by the user: "In retrospective assessment of samples, that ALISTER assesses analytes stability based on pre-analytical sample information provided by the user"
- [other] Parse user-provided pre-analytical parameters (time delay in hours, temperature in °C, matrix type: EDTA plasma or serum) into a structured query object. Query the ALISTER stability database with the parsed parameters to retrieve matching analyte-stability records (analyte name, stability flag, confidence metrics).: "Parse user-provided pre-analytical parameters (time delay in hours, temperature in °C, matrix type: EDTA plasma or serum) into a structured query object. Query the ALISTER stability database with the"
- [readme] By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before and after centrifugation) the threshold is expanded to 30%.: "By default the critical threshold for assessing instability is set to 20% fold change due to specific pre-analytical conditions. When conditions are combined (e.g. added change due to delay before"
- [intro] Time delay and temperature during processing are among the major pre-analytical pitfalls affecting (EDTA) plasma and serum samples: "Time delay and temperature during processing are among the major pre-analytical pitfalls affecting (EDTA) plasma and serum samples"
- [readme] Lipids are named after the lipid shorthand nomenclature, while polar metabolites are named after their RefMet nomenclature.: "Lipids are named after the lipid shorthand nomenclature, while polar metabolites are named after their RefMet nomenclature."
