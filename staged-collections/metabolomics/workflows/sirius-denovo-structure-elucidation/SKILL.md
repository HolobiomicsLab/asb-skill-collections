---
name: sirius-denovo-structure-elucidation-workflow
description: 'Use when you have MS/MS for unknown features (a SIRIUS-flavour mgf /
  .ms) and want de novo annotation without a spectral match — molecular formula (SIRIUS+ZODIAC),
  structure (CSI:FingerID + COSMIC), compound class (CANOPUS), optionally against
  a custom database, filtered by confidence.

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
  - molecular-fingerprint-prediction
  - molecular-fingerprint-parsing
  - web-service-api-integration
  - de-novo-structure-candidate-ranking
  - spectrum-query-formatting
  - chemical-classification-scheme-validation
  - natural-product-classifier-substitution
  - classification-workflow-parameter-toggling
  - chemical-ontology-mapping
  - consensus-classification-reconciliation
  - chemical-structure-validation
  - molecular-structure-input-format-handling
  - structure-standardization-validation
  - compound-structure-processing
  - chemical-structure-serialization
  - sirius-zodiac-score-filtering
  - annotation-table-quality-control
  - spectral-annotation-filtering-by-similarity-metrics
  - metabolite-annotation-validation
  - structural-annotation-integration
  member_tools:
  - SIRIUS
  - MIST-CF
  - msfiddle
  - FIDDLE
  - BUDDY
  - MIST
  - SCARF
  - PyTorch
  - SIRIUS decomp
  - CSI:FingerID
  - CANOPUS
  - MSNovelist
  - NPClassifier
  - GNPS
  - ClassyFire
  - ConCISE
  - Fiehn Labs ClassyFire Batch
  - RDKit
  - PubChemPy
  - Python
  - MetFrag
  - biosynfoni
  - pip
  - PubChem standardization
  - rcdk
  - CFM-ID
  - PHP
  - Symfony
  - MySQL 8
  - MariaDB 10
  - CycloBranch
  - INVENTA
  - MZmine2
  - MZmine3
  - timaR
  - MEMO
  - ISDB
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

End-to-end de novo elucidation with SIRIUS 6: formula, structure and class prediction for novel/unannotated chemistry, with confidence-based filtering.


## When to use

Use when you have MS/MS for unknown features (a SIRIUS-flavour mgf / .ms) and want de novo annotation without a spectral match — molecular formula (SIRIUS+ZODIAC), structure (CSI:FingerID + COSMIC), compound class (CANOPUS), optionally against a custom database, filtered by confidence.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — formula

**Goal:** molecular formula determination (SIRIUS + ZODIAC)

**EDAM operation:** operation_3860

**Inputs:** mgf/sirius · **Outputs:** tsv

**Candidate leaf skills:** `energy-based-formula-scoring` (primary), `molecular-formula-prediction-from-fragmentation`, `molecular-formula-assignment`, `fragment-peak-subformula-enumeration`, `neural-network-based-molecular-formula-inference`

**Tools:** SIRIUS, MIST-CF, msfiddle, FIDDLE, BUDDY, MIST, SCARF

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.jcim.3c01082, 10.1038/s41467-025-66060-9

### Stage 2 — structure

**Goal:** structure prediction (CSI:FingerID + COSMIC)

**EDAM operation:** operation_3801

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `molecular-fingerprint-prediction` (primary), `molecular-fingerprint-parsing`, `web-service-api-integration`, `de-novo-structure-candidate-ranking`, `spectrum-query-formatting`

**Tools:** PyTorch, MIST, MIST-CF, SIRIUS decomp, CSI:FingerID, SIRIUS, CANOPUS, MSNovelist

**Grounding:** 2 KB(s); DOIs: 10.1038/s41587-021-01045-9, 10.1038/s42256-023-00708-3

### Stage 3 — compound_class

**Goal:** compound class prediction (CANOPUS / NPClassifier)

**EDAM operation:** operation_3803

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `chemical-classification-scheme-validation` (primary), `natural-product-classifier-substitution`, `classification-workflow-parameter-toggling`, `chemical-ontology-mapping`, `consensus-classification-reconciliation`

**Tools:** NPClassifier, SIRIUS, GNPS, ClassyFire, ConCISE, Fiehn Labs ClassyFire Batch, CANOPUS

**Grounding:** 1 KB(s); DOIs: 10.3390/metabo12121275

### Stage 4 — custom_db  [OPTIONAL]

**Goal:** (optional) build a custom structure database for the search space

**EDAM operation:** operation_3434

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `chemical-structure-validation` (primary), `molecular-structure-input-format-handling`, `structure-standardization-validation`, `compound-structure-processing`, `chemical-structure-serialization`

**Tools:** RDKit, PubChemPy, Python, SIRIUS, MetFrag, biosynfoni, pip, PubChem standardization, rcdk, CFM-ID, PHP, Symfony, MySQL 8, MariaDB 10, CycloBranch

**Grounding:** 5 KB(s); DOIs: 10.1038/s41592-023-02143-z, 10.1186/s13321-021-00530-2, 10.1186/s13321-023-00695-y, 10.26434/chemrxiv-2025-cwq74 …

### Stage 5 — confidence_filter

**Goal:** filter annotations by ZODIAC / COSMIC confidence

**EDAM operation:** operation_3695

**Inputs:** tsv, tsv · **Outputs:** tsv

**Candidate leaf skills:** `sirius-zodiac-score-filtering` (primary), `annotation-table-quality-control`, `spectral-annotation-filtering-by-similarity-metrics`, `metabolite-annotation-validation`, `structural-annotation-integration`

**Tools:** SIRIUS, INVENTA, CANOPUS, GNPS, MZmine2, MZmine3, timaR, MEMO, ISDB, NPClassifier, ClassyFire, ConCISE

**Grounding:** 3 KB(s); DOIs: 10.1038/s41467-021-23953-9, 10.3389/fmolb.2022.1028334, 10.3390/metabo12121275

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — these are the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
