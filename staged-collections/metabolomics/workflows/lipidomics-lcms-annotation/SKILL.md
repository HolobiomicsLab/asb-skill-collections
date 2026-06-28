---
name: lipidomics-lcms-annotation-workflow
description: 'Use when you have untargeted lipidomics LC-MS/MS data (mzML) and want
  a class- and species-level annotated lipid feature table — preprocessing, normalization,
  lipid identification by MS/MS, retention/adduct rule validation, differential analysis,
  and a fused master table.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 6
  member_skills:
  - lcms-peak-detection-and-alignment
  - mass-spectrometry-metadata-extraction
  - file-format-conversion-peak-picking-to-lipidmatch
  - feature-table-normalization
  - mass-spectrometry-data-column-mapping
  - batch-aware-normalization-workflows
  - batch-correction-quality-assessment
  - batch-effect-correction-in-metabolomics
  - batch-corrected-feature-table-validation
  - batch-effect-correction-workflow
  - lipid-identification-scoring
  - fragment-ion-library-matching
  - multi-species-lipid-prediction
  - uhplc-hrms-ms-data-matching
  - lipid-structure-specification
  - false-positive-annotation-filtering
  - lipid-identification-quality-filtering
  - lipid-retention-time-rule-application
  - lipid-species-annotation-assessment
  - multicontrast-statistical-testing-lipidomics
  - fold-change-calculation
  - lipid-abundance-differential-analysis
  - differential-lipid-expression-analysis
  - metabolite-feature-anova-analysis
  - structured-data-matrix-construction
  - lipid-class-feature-annotation
  - lipid-class-annotation-and-parsing
  - lipid-species-classification-mapping
  member_tools:
  - ISFrag
  - R
  - XCMS
  - CAMERA
  - Python
  - pycombat
  - Asari
  - LipidMatch
  - MZmine
  - MS-DIAL
  - Compound Discoverer
  - LipidIN LCI module
  - lipidr
  - limma
  - ADViSELipidomics
  - LipidSearch
  - LIQUID
  - LIPID MAPS
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

# Lipidomics LC-MS/MS Annotation

## Summary

End-to-end lipidomics annotation: raw LC-MS/MS in, a confidence-graded lipid table out, with lipid-class-aware identification, normalization, and group-wise statistics.


## When to use

Use when you have untargeted lipidomics LC-MS/MS data (mzML) and want a class- and species-level annotated lipid feature table — preprocessing, normalization, lipid identification by MS/MS, retention/adduct rule validation, differential analysis, and a fused master table.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess

**Goal:** raw lipidomics mzML -> aligned feature table + MS/MS export

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table, mgf

**Candidate leaf skills:** `lcms-peak-detection-and-alignment` (primary), `mass-spectrometry-metadata-extraction`, `file-format-conversion-peak-picking-to-lipidmatch`, `feature-table-normalization`, `mass-spectrometry-data-column-mapping`

**Tools (primary):** ISFrag, R, XCMS, CAMERA

**Other candidate tools:** MZmine, MS-DIAL, Compound Discoverer, LipidMatch

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.analchem.1c01644, 10.1186/s12859-017-1744-3

### Stage 2 — normalize

**Goal:** normalize + batch-correct the lipid feature table

**EDAM operation:** operation_3434

**Inputs:** feature-table · **Outputs:** feature-table

**Candidate leaf skills:** `batch-aware-normalization-workflows` (primary), `batch-correction-quality-assessment`, `batch-effect-correction-in-metabolomics`, `batch-corrected-feature-table-validation`, `batch-effect-correction-workflow`

**Tools (primary):** Python, pycombat, Asari

**Other candidate tools:** ThermoRawFileParser, pcpfm, ADViSELipidomics, limma, edgeR, ComBat, R, Jupyter Notebook, Google Colab, FBMN-STATS

**Grounding:** 3 KB(s); DOIs: 10.1038/s41596-024-01046-3, 10.1093/bioinformatics/btac706, 10.1371/journal.pcbi.1011912

### Stage 3 — lipid_identification

**Goal:** identify lipids (class + species) from MS/MS fragmentation

**EDAM operation:** operation_3803

**Inputs:** mgf · **Outputs:** tsv

**Candidate leaf skills:** `lipid-identification-scoring` (primary), `fragment-ion-library-matching`, `multi-species-lipid-prediction`, `uhplc-hrms-ms-data-matching`, `lipid-structure-specification`

**Tools (primary):** LipidMatch, MZmine, XCMS, MS-DIAL, Compound Discoverer

**Other candidate tools:** Q-Exactive, CAMERA, LipidIN EQ module, LipidIN LCI module, Q-Exactive orbitrap, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF

**Grounding:** 2 KB(s); DOIs: 10.1038/s41467-025-59683-5, 10.1186/s12859-017-1744-3

### Stage 4 — rule_validation

**Goal:** validate lipid annotations by adduct / retention-time / class rules

**EDAM operation:** operation_3695

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `false-positive-annotation-filtering` (primary), `lipid-identification-quality-filtering`, `lipid-retention-time-rule-application`, `lipid-species-annotation-assessment`

**Tools (primary):** XCMS, CAMERA, LipidIN LCI module

**Other candidate tools:** LipoCLEAN, MS-DIAL, LipidIN (LCI Module), RaMS, MetaboAnnotatoR, R

**Grounding:** 3 KB(s); DOIs: 10.1021/acs.analchem.1c03032, 10.1021/acs.analchem.4c04040, 10.1038/s41467-025-59683-5

### Stage 5 — statistics

**Goal:** differential lipid analysis between sample groups

**EDAM operation:** operation_3659

**Inputs:** feature-table, tsv · **Outputs:** tsv

**Candidate leaf skills:** `multicontrast-statistical-testing-lipidomics` (primary), `fold-change-calculation`, `lipid-abundance-differential-analysis`, `differential-lipid-expression-analysis`, `metabolite-feature-anova-analysis`

**Tools (primary):** lipidr, limma, R

**Other candidate tools:** Python (pandas, NumPy, SciPy), R (base stats, tidyverse, or similar), pandas, NumPy, SciPy, edgeR.R, ADViSELipidomics, edgeR, ComBat, LIPID MAPS, Metabolomics Workbench API, margheRita, MS-DIAL

**Grounding:** 5 KB(s); DOIs: 10.1021/acs.analchem.4c05039, 10.1021/acs.jproteome.0c00082, 10.1093/bioinformatics/btac706, 10.1101/2024.06.20.599545 …

### Stage 6 — fusion

**Goal:** consolidate lipid annotations + stats into one master table

**EDAM operation:** operation_3434

**Inputs:** feature-table, tsv · **Outputs:** tsv

**Candidate leaf skills:** `structured-data-matrix-construction` (primary), `lipid-class-feature-annotation`, `lipid-class-annotation-and-parsing`, `lipid-species-classification-mapping`

**Tools (primary):** ADViSELipidomics, LipidSearch, LIQUID, LIPID MAPS

**Other candidate tools:** lipidr, R, Skyline, SummarizedExperiment, limma, edgeR, ComBat

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.jproteome.0c00082, 10.1093/bioinformatics/btac706

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
