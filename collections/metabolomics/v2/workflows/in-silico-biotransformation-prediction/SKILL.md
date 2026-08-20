---
name: in-silico-biotransformation-prediction-workflow
description: 'Use when you have a parent structure (drug, natural product, xenobiotic)
  and untargeted LC-MS/MS data and want to find its biotransformation products — predict
  plausible metabolites in-silico by rule-based expansion (BioTransformer mammalian/gut-microbial/
  environmental rules, EnviPath microbial degradation, or MINE/Pickaxe combinatorial
  reaction-network generation), filter candidates to those detectable in the experimental
  mass range, then screen and rank them against the observed LC-MS/MS features to
  annotate which predicted biotransformation products were actually seen.

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
  - spectral-feature-table-generation
  - lcms-feature-detection-and-quantification
  - feature-alignment-metabolomics
  - biotransformation-rule-application
  - biotransformation-prediction-across-microbiota-contexts
  - microbial-biotransformation-prediction
  - small-molecule-structure-input-preparation
  - metabolite-structure-prediction
  - adduct-mass-adjustment-calculation
  - exact-mass-database-matching
  - adduct-mass-shift-calculation
  - in-silico-fragmentation-prediction
  - candidate-metabolite-ranking
  - transformation-product-prediction
  - fragment-ion-scoring-and-ranking
  - structural-similarity-scoring-metabolites
  - biotransformation-candidate-integration-with-networking
  - mass-spectrometry-compound-annotation-database-generation
  - transformation-product-parent-linkage
  - metabolite-structure-annotation-integration
  - parent-product-relationship-tracking
  member_tools:
  - MZmine2
  - Optimus
  - OpenMS
  - BioTransformer
  - EAWAG Biodegradation and Biocatalysis Database
  - EnviPath
  - MINE-Database Pickaxe
  - RDKit
  - mordred
  - pytest
  - MINE-Database Filter base class
  - MAGMa
  - PubChem
  - MetFrag
  - BAM
  - PROXIMAL2
  - GNN-SOM
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

# In-Silico Biotransformation / Metabolite Prediction (parent structure -> matched biotransformation products)

## Summary

Parent SMILES + mzML in, a ranked biotransformation-product annotation table out: rule-based metabolite prediction (BioTransformer / EnviPath / Pickaxe), mass-based candidate filtering, MS/MS-based candidate screening and ranking.


## When to use

Use when you have a parent structure (drug, natural product, xenobiotic) and untargeted LC-MS/MS data and want to find its biotransformation products — predict plausible metabolites in-silico by rule-based expansion (BioTransformer mammalian/gut-microbial/ environmental rules, EnviPath microbial degradation, or MINE/Pickaxe combinatorial reaction-network generation), filter candidates to those detectable in the experimental mass range, then screen and rank them against the observed LC-MS/MS features to annotate which predicted biotransformation products were actually seen.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess

**Goal:** raw mzML -> feature table + MS2 export

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table, mgf/gnps-fbmn

**Candidate leaf skills:** `peak-detection-and-mass-alignment` (primary), `mass-spectrometry-feature-table-construction`, `spectral-feature-table-generation`, `lcms-feature-detection-and-quantification`, `feature-alignment-metabolomics`

**Tools (primary):** MZmine2, Optimus, OpenMS

**Other candidate tools:** Python, pyOpenMS, MSConvert, PFΔScreen, JPA, R, XCMS, MS-Convert, MetaboAnalystR, openNAU, MetaQC

**Grounding:** 5 KB(s); DOIs: 10.1007/s00216-023-05070-2, 10.1021/acs.jnatprod.7b00737, 10.1038/s41467-024-48009-6, 10.21147/j.issn.1000-9604.2023.05.11 …

### Stage 2 — biotransformation_prediction

**Goal:** parent structure -> predicted metabolite/transformation-product structures (rule-based expansion)

**EDAM operation:** operation_3802

**Inputs:** smiles · **Outputs:** tsv

**Candidate leaf skills:** `biotransformation-rule-application` (primary), `biotransformation-prediction-across-microbiota-contexts`, `microbial-biotransformation-prediction`, `small-molecule-structure-input-preparation`, `metabolite-structure-prediction`

**Tools (primary):** BioTransformer, EAWAG Biodegradation and Biocatalysis Database, EnviPath, MINE-Database Pickaxe, RDKit


**Grounding:** 2 KB(s); DOIs: 10.1093/nar/gkac408, 10.1186/s13321-019-0375-2

### Stage 3 — candidate_filtering

**Goal:** predicted candidates -> mass-plausible candidates (filter against the experimental peak list)

**EDAM operation:** operation_3801

**Inputs:** tsv, feature-table · **Outputs:** tsv

**Candidate leaf skills:** `adduct-mass-adjustment-calculation` (primary), `exact-mass-database-matching`, `adduct-mass-shift-calculation`

**Tools (primary):** RDKit, mordred, pytest, MINE-Database Filter base class

**Other candidate tools:** tidyverse, CluMSID, CluMSIDdata, grid, OrgMassSpecR, pheatmap, reshape2, MSMSsim, msentropy, readxl, MSDial, Biotransformer, geoRge, R, basepeak_finder, XCMS, MetaboShiny

**Grounding:** 4 KB(s); DOIs: 10.1007/s11306-020-01717-8, 10.1021/acs.analchem.5b03628, 10.1021/acs.est.5c08558, 10.1186/s12859-023-05149-8

### Stage 4 — ms_matching

**Goal:** mass-plausible candidates -> MS/MS-matched and ranked biotransformation products

**EDAM operation:** operation_3802

**Inputs:** tsv, mgf/gnps-fbmn · **Outputs:** tsv

**Candidate leaf skills:** `in-silico-fragmentation-prediction` (primary), `candidate-metabolite-ranking`, `transformation-product-prediction`, `fragment-ion-scoring-and-ranking`, `structural-similarity-scoring-metabolites`

**Tools (primary):** MAGMa, PubChem, BioTransformer, MetFrag

**Other candidate tools:** patRoon, CTS, PubChemLite, MetaboAnnotatoR, R (version or higher), R, xcms, RamClustR, DeepMASS, Keras, RDKit, IsoSpecPy

**Grounding:** 5 KB(s); DOIs: 10.1021/acs.analchem.1c03032, 10.1021/acs.analchem.8b05405, 10.1186/s13321-019-0375-2, 10.1186/s13321-020-00477-w …

### Stage 5 — report

**Goal:** consolidate parent structure, predicted candidates, and MS/MS-matched hits into a biotransformation-product annotation table

**EDAM operation:** operation_3434

**Inputs:** tsv, feature-table · **Outputs:** tsv

**Candidate leaf skills:** `biotransformation-candidate-integration-with-networking` (primary), `mass-spectrometry-compound-annotation-database-generation`, `transformation-product-parent-linkage`, `metabolite-structure-annotation-integration`, `parent-product-relationship-tracking`

**Tools (primary):** BAM, PROXIMAL2, GNN-SOM

**Other candidate tools:** patRoon, MetFrag, BioTransformer, CTS, screenSuspects, convertToSuspects, RDKit, KEGG or RetroRules

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.analchem.4c01565, 10.1186/s13321-020-00477-w

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
