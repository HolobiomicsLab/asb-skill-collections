---
name: sirius-denovo-structure-elucidation-workflow
description: 'Use when you have MS/MS for unknown features (a SIRIUS-flavour mgf /
  .ms) and want de novo annotation without a spectral match — molecular formula (SIRIUS+ZODIAC),
  structure (CSI:FingerID + COSMIC), compound class (CANOPUS), optionally against
  a custom database, filtered by confidence. Library-FREE by design.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 5
  member_skills:
  - energy-based-formula-scoring
  - molecular-formula-prediction-from-fragmentation
  - molecular-formula-assignment
  - fragment-peak-subformula-enumeration
  - neural-network-based-molecular-formula-inference
  - compound-structure-processing
  - chemical-structure-validation
  - molecular-structure-input-format-handling
  - structure-standardization-validation
  - chemical-structure-serialization
  - de-novo-structure-candidate-ranking
  - molecular-fingerprint-prediction
  - molecular-fingerprint-parsing
  - web-service-api-integration
  - spectrum-query-formatting
  - compound-class-annotation-parsing
  - natural-product-classifier-substitution
  - classification-workflow-parameter-toggling
  - chemical-ontology-mapping
  - consensus-classification-reconciliation
  - chemical-class-assignment-classyfire
  - sirius-zodiac-score-filtering
  - annotation-table-quality-control
  - metabolite-annotation-validation
  - structural-annotation-integration
  - compound-candidate-ranking
  member_tools:
  - SIRIUS
  - MIST-CF
  - ZODIAC
  - CFM-ID
  - MSNovelist
  - CSI:FingerID
  - CANOPUS
  - INVENTA
  coverage_gaps: []
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# SIRIUS De Novo Structure Elucidation

## Summary

End-to-end de novo elucidation with SIRIUS 6: formula, structure and class prediction for novel/unannotated chemistry, with confidence-based filtering. No spectral library.


## When to use

Use when you have MS/MS for unknown features (a SIRIUS-flavour mgf / .ms) and want de novo annotation without a spectral match — molecular formula (SIRIUS+ZODIAC), structure (CSI:FingerID + COSMIC), compound class (CANOPUS), optionally against a custom database, filtered by confidence. Library-FREE by design.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — formula

**Goal:** molecular formula determination (SIRIUS + ZODIAC)

**EDAM operation:** operation_3860

**Inputs:** mgf/sirius · **Outputs:** tsv

**Candidate leaf skills:** `energy-based-formula-scoring` (primary), `molecular-formula-prediction-from-fragmentation`, `molecular-formula-assignment`, `fragment-peak-subformula-enumeration`, `neural-network-based-molecular-formula-inference`

**Tools (primary):** SIRIUS, MIST-CF, ZODIAC

**Other candidate tools:** msfiddle, FIDDLE, BUDDY, MIST, SCARF

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.jcim.3c01082, 10.1038/s41467-025-66060-9

### Stage 2 — custom_db  [OPTIONAL]

**Goal:** (optional) build a custom structure database for the search space

**EDAM operation:** operation_3434

**Inputs:** smiles · **Outputs:** tsv

**Candidate leaf skills:** `compound-structure-processing` (primary), `chemical-structure-validation`, `molecular-structure-input-format-handling`, `structure-standardization-validation`, `chemical-structure-serialization`

**Tools (primary):** CFM-ID

**Other candidate tools:** RDKit, PubChemPy, Python, SIRIUS, MetFrag, biosynfoni, pip, PubChem standardization, rcdk, PHP, Symfony, MySQL 8, MariaDB 10, CycloBranch

**Grounding:** 5 KB(s); DOIs: 10.1038/s41592-023-02143-z, 10.1186/s13321-021-00530-2, 10.1186/s13321-023-00695-y, 10.26434/chemrxiv-2025-cwq74 …

### Stage 3 — structure

**Goal:** structure prediction (CSI:FingerID + COSMIC)

**EDAM operation:** operation_3801

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `de-novo-structure-candidate-ranking` (primary), `molecular-fingerprint-prediction`, `molecular-fingerprint-parsing`, `web-service-api-integration`, `spectrum-query-formatting`

**Tools (primary):** MSNovelist, SIRIUS, CSI:FingerID, CANOPUS

**Other candidate tools:** PyTorch, MIST, MIST-CF, SIRIUS decomp

**Grounding:** 2 KB(s); DOIs: 10.1038/s41587-021-01045-9, 10.1038/s42256-023-00708-3

### Stage 4 — compound_class

**Goal:** compound class prediction (CANOPUS / NPClassifier)

**EDAM operation:** operation_3803

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `compound-class-annotation-parsing` (primary), `natural-product-classifier-substitution`, `classification-workflow-parameter-toggling`, `chemical-ontology-mapping`, `consensus-classification-reconciliation`, `chemical-class-assignment-classyfire`

**Tools (primary):** CANOPUS, SIRIUS

**Other candidate tools:** NPClassifier, GNPS, ClassyFire, ConCISE, matchms, MS2DeepScore, scikit-learn, Python, RDKit

**Grounding:** 3 KB(s); DOIs: 10.1038/s41587-021-01045-9, 10.1186/s13321-021-00558-4, 10.3390/metabo12121275

### Stage 5 — confidence_filter

**Goal:** filter annotations by ZODIAC / COSMIC confidence

**EDAM operation:** operation_3695

**Inputs:** tsv, tsv · **Outputs:** tsv

**Candidate leaf skills:** `sirius-zodiac-score-filtering` (primary), `annotation-table-quality-control`, `metabolite-annotation-validation`, `structural-annotation-integration`, `compound-candidate-ranking`

**Tools (primary):** SIRIUS, INVENTA, CANOPUS

**Other candidate tools:** GNPS, ISDB, timaR, NPClassifier, ClassyFire, ConCISE, RDKit, PubChemPy, Python, MetFrag

**Grounding:** 4 KB(s); DOIs: 10.1038/s41467-021-23953-9, 10.1186/s13321-023-00695-y, 10.3389/fmolb.2022.1028334, 10.3390/metabo12121275

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
