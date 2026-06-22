---
name: code-artifact-inspection
description: Use when use when the workflow requires code_artifact_inspection.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - GitHub
  - local code artifact
derived_from:
- doi: 10.3389/fmolb.2022.952149
  title: TurboPutative
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qc4metabolomics_cq
    doi: 10.1021/acs.analchem.4c07078
    title: qc4metabolomics
  - build: coll_turboputative_cq
    doi: 10.3389/fmolb.2022.952149
    title: TurboPutative
  dedup_kept_from: coll_turboputative_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fmolb.2022.952149
  all_source_dois:
  - 10.3389/fmolb.2022.952149
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# code_artifact_inspection

## When to use

Use when the workflow requires code_artifact_inspection.
