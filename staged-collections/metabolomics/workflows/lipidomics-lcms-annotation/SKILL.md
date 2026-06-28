---
name: lipidomics-lcms-annotation-workflow
description: 'Use when you have untargeted lipidomics LC-MS/MS data (mzML) and want
  a class- and species-level annotated lipid feature table — preprocessing, lipid
  identification by MS/MS, retention/adduct rule validation, differential analysis,
  and a fused master table.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 5
  member_skills:
  - mass-spectrometry-metadata-extraction
  - file-format-conversion-peak-picking-to-lipidmatch
  - lcms-peak-detection-and-alignment
  - feature-table-normalization
  - mass-spectrometry-data-column-mapping
  - lipid-identification-scoring
  - fragment-ion-library-matching
  - multi-species-lipid-prediction
  - uhplc-hrms-ms-data-matching
  - lipid-library-format-schema
  - false-positive-annotation-filtering
  - lipid-retention-time-rule-application
  - lipid-identification-quality-filtering
  - lipid-species-annotation-assessment
  - multicontrast-statistical-testing-lipidomics
  - fold-change-calculation
  - lipid-abundance-differential-analysis
  - metabolite-feature-anova-analysis
  - enrichment-statistic-interpretation
  - lipid-class-feature-annotation
  - lipid-class-annotation-and-parsing
  - lipid-species-classification-mapping
  - structured-data-matrix-construction
  member_tools:
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - LipidMatch
  - ISFrag
  - R
  - CAMERA
  - Q-Exactive
  - LipidIN EQ module
  - LipidIN LCI module
  - Q-Exactive orbitrap
  - Agilent Q-TOF
  - Bruker Q-TOF
  - SCIEX Q-TOF
  - LipidIN (LCI Module)
  - RaMS
  - LipoCLEAN
  - MetaboAnnotatoR
  - lipidr
  - limma
  - Python (pandas, NumPy, SciPy)
  - R (base stats, tidyverse, or similar)
  - pandas
  - NumPy
  - SciPy
  - edgeR.R
  - ADViSELipidomics
  - edgeR
  - ComBat
  - LIPID MAPS
  - margheRita
  - Skyline
  - SummarizedExperiment
  - LipidSearch
  - LIQUID
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Lipidomics LC-MS/MS Annotation

## Summary

End-to-end lipidomics annotation: raw LC-MS/MS in, a confidence-graded lipid table out, with lipid-class-aware identification and group-wise statistics.


## When to use

Use when you have untargeted lipidomics LC-MS/MS data (mzML) and want a class- and species-level annotated lipid feature table — preprocessing, lipid identification by MS/MS, retention/adduct rule validation, differential analysis, and a fused master table.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess

**Goal:** raw lipidomics mzML -> aligned feature table + MS/MS export

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table, mgf

**Candidate leaf skills:** `mass-spectrometry-metadata-extraction` (primary), `file-format-conversion-peak-picking-to-lipidmatch`, `lcms-peak-detection-and-alignment`, `feature-table-normalization`, `mass-spectrometry-data-column-mapping`

**Tools:** MZmine, XCMS, MS-DIAL, Compound Discoverer, LipidMatch, ISFrag, R, CAMERA

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.analchem.1c01644, 10.1186/s12859-017-1744-3

### Stage 2 — lipid_identification

**Goal:** identify lipids (class + species) from MS/MS fragmentation

**EDAM operation:** operation_3803

**Inputs:** mgf · **Outputs:** tsv

**Candidate leaf skills:** `lipid-identification-scoring` (primary), `fragment-ion-library-matching`, `multi-species-lipid-prediction`, `uhplc-hrms-ms-data-matching`, `lipid-library-format-schema`

**Tools:** LipidMatch, MZmine, XCMS, MS-DIAL, Compound Discoverer, Q-Exactive, CAMERA, LipidIN EQ module, LipidIN LCI module, Q-Exactive orbitrap, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF

**Grounding:** 2 KB(s); DOIs: 10.1038/s41467-025-59683-5, 10.1186/s12859-017-1744-3

### Stage 3 — rule_validation

**Goal:** validate lipid annotations by adduct / retention-time / class rules

**EDAM operation:** operation_3695

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `false-positive-annotation-filtering` (primary), `lipid-retention-time-rule-application`, `lipid-identification-quality-filtering`, `lipid-species-annotation-assessment`

**Tools:** XCMS, CAMERA, LipidIN LCI module, LipidIN (LCI Module), RaMS, LipoCLEAN, MS-DIAL, MetaboAnnotatoR, R

**Grounding:** 3 KB(s); DOIs: 10.1021/acs.analchem.1c03032, 10.1021/acs.analchem.4c04040, 10.1038/s41467-025-59683-5

### Stage 4 — statistics

**Goal:** differential lipid analysis between sample groups

**EDAM operation:** operation_3659

**Inputs:** feature-table, tsv · **Outputs:** tsv

**Candidate leaf skills:** `multicontrast-statistical-testing-lipidomics` (primary), `fold-change-calculation`, `lipid-abundance-differential-analysis`, `metabolite-feature-anova-analysis`, `enrichment-statistic-interpretation`

**Tools:** lipidr, limma, R, Python (pandas, NumPy, SciPy), R (base stats, tidyverse, or similar), pandas, NumPy, SciPy, edgeR.R, ADViSELipidomics, edgeR, ComBat, LIPID MAPS, margheRita, MS-DIAL

**Grounding:** 5 KB(s); DOIs: 10.1021/acs.analchem.4c05039, 10.1021/acs.jproteome.0c00082, 10.1093/bioinformatics/btac706, 10.1101/2024.06.20.599545 …

### Stage 5 — fusion

**Goal:** consolidate lipid annotations + stats into one master table

**EDAM operation:** operation_3434

**Inputs:** feature-table, tsv · **Outputs:** tsv

**Candidate leaf skills:** `lipid-class-feature-annotation` (primary), `lipid-class-annotation-and-parsing`, `lipid-species-classification-mapping`, `structured-data-matrix-construction`

**Tools:** lipidr, R, Skyline, SummarizedExperiment, ADViSELipidomics, limma, edgeR, ComBat, LIPID MAPS, LipidSearch, LIQUID

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.jproteome.0c00082, 10.1093/bioinformatics/btac706

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — these are the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
