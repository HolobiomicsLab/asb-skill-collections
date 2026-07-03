---
name: compound-class-annotation-workflow
description: 'Use when you want chemical-class-level annotations for untargeted LC-MS/MS
  features rather than exact structures — determine molecular formulas with SIRIUS,
  compute CSI:FingerID fingerprints, and predict compound classes with CANOPUS and
  NPClassifier (superclass / class / pathway), producing a class-annotated feature
  table for chemical-inventory and enrichment analysis.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 5
  member_skills:
  - peak-detection-and-mass-alignment
  - mass-spectrometry-feature-table-construction
  - cross-sample-feature-alignment
  - lcms-feature-table-construction
  - mass-spectrometry-feature-annotation
  - molecular-formula-prediction-from-fragmentation
  - energy-based-formula-scoring
  - neural-network-based-molecular-formula-inference
  - molecular-formula-assignment
  - fragment-peak-subformula-enumeration
  - molecular-fingerprint-parsing
  - molecular-fingerprint-prediction
  - spectrum-query-formatting
  - spectral-fingerprint-web-service-query
  - molecular-fingerprint-generation-and-encoding
  - natural-product-classifier-substitution
  - natural-product-classification-prediction
  - classification-workflow-parameter-toggling
  - consensus-classification-reconciliation
  - spectral-feature-chemical-assignment
  - chemical-classification-scheme-validation
  - chemical-ontology-mapping
  - structural-annotation-integration
  member_tools:
  - MZmine2
  - Optimus
  - OpenMS
  - msfiddle
  - FIDDLE
  - BUDDY
  - SIRIUS
  - CSI:FingerID
  - CANOPUS
  - NPClassifier
  - GNPS
  - ClassyFire
  - ConCISE
  coverage_gaps: []
  derived_from_workflows:
  - coll_npclassscore_cq
  - coll_molnetenhancer
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Compound-Class Annotation (SIRIUS formula -> CANOPUS / NPClassifier class)

## Summary

MS2 in, a chemical-class-annotated table out: SIRIUS molecular formula, molecular fingerprint, and CANOPUS / NPClassifier compound-class prediction per feature.


## When to use

Use when you want chemical-class-level annotations for untargeted LC-MS/MS features rather than exact structures — determine molecular formulas with SIRIUS, compute CSI:FingerID fingerprints, and predict compound classes with CANOPUS and NPClassifier (superclass / class / pathway), producing a class-annotated feature table for chemical-inventory and enrichment analysis.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess

**Goal:** raw mzML -> feature table + SIRIUS-flavour MS2 export

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table, mgf/sirius

**Candidate leaf skills:** `peak-detection-and-mass-alignment` (primary), `mass-spectrometry-feature-table-construction`, `cross-sample-feature-alignment`, `lcms-feature-table-construction`, `mass-spectrometry-feature-annotation`

**Tools (primary):** MZmine2, Optimus, OpenMS

**Other candidate tools:** Python, pyOpenMS, MSConvert, PFΔScreen, Centwave, FeatureFinderMetabo, ADAP, ProteoWizard, q2-qemistree, SIRIUS, GNPS FBMN, Classyfire

**Grounding:** 4 KB(s); DOIs: 10.1007/s00216-023-05070-2, 10.1021/acs.analchem.1c02687, 10.1021/acs.jnatprod.7b00737, 10.1038/s41589-020-00677-3

### Stage 2 — formula

**Goal:** MS2 spectra -> molecular formula (SIRIUS + ZODIAC re-ranking)

**EDAM operation:** operation_3860

**Inputs:** mgf/sirius · **Outputs:** tsv

**Candidate leaf skills:** `molecular-formula-prediction-from-fragmentation` (primary), `energy-based-formula-scoring`, `neural-network-based-molecular-formula-inference`, `molecular-formula-assignment`, `fragment-peak-subformula-enumeration`

**Tools (primary):** msfiddle, FIDDLE, BUDDY, SIRIUS

**Other candidate tools:** MIST-CF, MIST, SCARF

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.jcim.3c01082, 10.1038/s41467-025-66060-9

### Stage 3 — fingerprint

**Goal:** formula + MS2 -> molecular fingerprint (CSI:FingerID)

**EDAM operation:** operation_3801

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `molecular-fingerprint-parsing` (primary), `molecular-fingerprint-prediction`, `spectrum-query-formatting`, `spectral-fingerprint-web-service-query`, `molecular-fingerprint-generation-and-encoding`

**Tools (primary):** CSI:FingerID, SIRIUS, CANOPUS

**Other candidate tools:** PyTorch, MIST, MIST-CF, SIRIUS decomp, ClassyFire

**Grounding:** 2 KB(s); DOIs: 10.1038/s41587-021-01045-9, 10.1038/s42256-023-00708-3

### Stage 4 — classify

**Goal:** fingerprint -> compound class (CANOPUS / NPClassifier: superclass/class/pathway)

**EDAM operation:** operation_0224

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `natural-product-classifier-substitution` (primary), `natural-product-classification-prediction`, `classification-workflow-parameter-toggling`

**Tools (primary):** NPClassifier, SIRIUS, GNPS, ClassyFire, ConCISE

**Other candidate tools:** Python, Docker, docker-compose, TensorFlow 2.3.0, Keras, TensorFlow Serving, NP Classifier Repository

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.jnatprod.1c00399, 10.3390/metabo12121275

### Stage 5 — consolidate

**Goal:** consolidate formula + fingerprint + class into a class-annotated feature table

**EDAM operation:** operation_3434

**Inputs:** feature-table, tsv · **Outputs:** tsv

**Candidate leaf skills:** `consensus-classification-reconciliation` (primary), `spectral-feature-chemical-assignment`, `chemical-classification-scheme-validation`, `chemical-ontology-mapping`, `structural-annotation-integration`

**Tools (primary):** SIRIUS, NPClassifier, GNPS, ClassyFire, ConCISE

**Other candidate tools:** Fiehn Labs ClassyFire Batch, CANOPUS

**Grounding:** 1 KB(s); DOIs: 10.3390/metabo12121275

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
