---
name: suspect-screening-exposomics-workflow
description: 'Use when you have untargeted HRMS data and want to screen for a defined
  suspect list of environmental / exposure-relevant compounds — detect features, match
  them to suspect-list entries by exact mass/RT/MS2, elucidate structures of hits
  by in-silico fragmentation, and assign identification confidence levels (Schymanski),
  producing a confidence-annotated suspect-hit table.

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
  - ms1-feature-extraction
  - mass-spectrometry-feature-detection-validation
  - non-targeted-preprocessing-tool-comparison
  - suspect-database-matching
  - mass-spectrometry-screening-workflows
  - feature-annotation-with-chemical-descriptors
  - multi-criterion-scoring-integration
  - in-silico-fragmentation-prediction
  - candidate-structure-ranking
  - candidate-rank-scoring
  - fragment-ion-scoring-and-ranking
  - candidate-structure-ranking-from-spectrum
  - compound-annotation-confidence-assessment
  - metabolite-annotation-confidence-assignment
  - annotation-confidence-assessment
  - annotation-scoring-and-ranking
  - lipid-species-identification
  - suspect-list-format-conversion
  - inchikey-structural-similarity-computation
  - spectral-database-schema-validation
  member_tools:
  - MZmine2
  - Optimus
  - OpenMS
  - R Shiny
  - EISA-EXPOSOME
  - T3DB
  - MAGMa
  - PubChem
  - masscube
  - Python
  - patRoon
  - generateTPs
  - screenSuspects
  - BioTransformer
  - CTS
  coverage_gaps: []
  derived_from_workflows:
  - coll_ms2deepscore
  - coll_metabodirect
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Suspect Screening for Exposomics (suspect lists -> confidence-levelled IDs)

## Summary

HRMS in, a confidence-levelled suspect-hit table out: suspect-list matching, in-silico fragmentation, and identification-confidence assignment for exposomics.


## When to use

Use when you have untargeted HRMS data and want to screen for a defined suspect list of environmental / exposure-relevant compounds — detect features, match them to suspect-list entries by exact mass/RT/MS2, elucidate structures of hits by in-silico fragmentation, and assign identification confidence levels (Schymanski), producing a confidence-annotated suspect-hit table.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess

**Goal:** raw HRMS -> feature table + MS2 export

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table, mgf/gnps-fbmn

**Candidate leaf skills:** `peak-detection-and-mass-alignment` (primary), `mass-spectrometry-feature-table-construction`, `ms1-feature-extraction`, `mass-spectrometry-feature-detection-validation`, `non-targeted-preprocessing-tool-comparison`

**Tools (primary):** MZmine2, Optimus, OpenMS

**Other candidate tools:** Python, pyOpenMS, MSConvert, PFΔScreen, Scannotation, mzRAPP, MZmine 2, R, XCMS, enviPat, Skyline, R (with mzRAPP library)

**Grounding:** 4 KB(s); DOIs: 10.1007/s00216-023-05070-2, 10.1021/acs.est.3c04764, 10.1021/acs.jnatprod.7b00737, 10.1093/bioinformatics/btab231/6214530

### Stage 2 — suspect_match

**Goal:** features -> suspect-list matches by exact mass / RT / MS2

**EDAM operation:** operation_3631

**Inputs:** feature-table, mgf/gnps-fbmn · **Outputs:** tsv

**Candidate leaf skills:** `suspect-database-matching` (primary), `mass-spectrometry-screening-workflows`, `feature-annotation-with-chemical-descriptors`, `multi-criterion-scoring-integration`

**Tools (primary):** R Shiny, EISA-EXPOSOME, T3DB

**Other candidate tools:** patRoon, XCMS, OpenMS, BioTransformer, CTS, MetFrag, SIRIUS, CAMERA, RAMClustR, ProteoWizard, Python, pyOpenMS, MSConvert, PFΔScreen, Scannotation

**Grounding:** 4 KB(s); DOIs: 10.1007/s00216-023-05070-2, 10.1021/acs.analchem.3c02697, 10.1021/acs.est.3c04764, 10.1186/s13321-020-00477-w

### Stage 3 — in_silico_fragment

**Goal:** suspect hits -> in-silico fragmentation structure ranking (MetFrag / SIRIUS)

**EDAM operation:** operation_3860

**Inputs:** tsv, mgf/gnps-fbmn · **Outputs:** tsv

**Candidate leaf skills:** `in-silico-fragmentation-prediction` (primary), `candidate-structure-ranking`, `candidate-rank-scoring`, `fragment-ion-scoring-and-ranking`, `candidate-structure-ranking-from-spectrum`

**Tools (primary):** MAGMa, PubChem

**Other candidate tools:** Python, pyrwr, MetFrag, ChemWalker, DiffSpectra, Diffusion Molecule Transformer (DMT), SpecFormer, Spectra, SIRIUS, R, RDKit, PubChemPy, MetaboAnnotatoR, R (version or higher), xcms, RamClustR, ICEBERG WebUI, SCARF

**Grounding:** 6 KB(s); DOIs: 10.1021/acs.analchem.1c03032, 10.1038/s42256-024-00816-8, 10.1093/bioinformatics/btad078/7067745, 10.1186/s13321-023-00695-y …

### Stage 4 — confidence

**Goal:** assign identification confidence levels (Schymanski 1-5) to hits

**EDAM operation:** operation_0224

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `compound-annotation-confidence-assessment` (primary), `metabolite-annotation-confidence-assignment`, `annotation-confidence-assessment`, `annotation-scoring-and-ranking`, `lipid-species-identification`

**Tools (primary):** masscube, Python

**Other candidate tools:** R, XCMS, MS-Dial, GetFeatistics, patRoon, MS-CleanR, MS-FINDER, commons-math3, jfreechart, jopt-simple, trove4j, Passatutto, MetaboAnnotatoR, R (version or higher), RamClustR, R (≥4.5.0)

**Grounding:** 5 KB(s); DOIs: 10.1021/acs.analchem.0c01594, 10.1021/acs.analchem.1c03032, 10.1038/s41467-025-60640-5, 10.1515/jib-2025-0047 …

### Stage 5 — report

**Goal:** consolidate suspect hits + structures + confidence into an annotated table

**EDAM operation:** operation_3434

**Inputs:** tsv, feature-table · **Outputs:** tsv

**Candidate leaf skills:** `suspect-list-format-conversion` (primary), `inchikey-structural-similarity-computation`, `spectral-database-schema-validation`

**Tools (primary):** patRoon, generateTPs, screenSuspects, BioTransformer, CTS

**Other candidate tools:** MS2Query, GitHub, MS2Deepscore, RDKit, Random forest (scikit-learn or equivalent), R Shiny, T3DB

**Grounding:** 3 KB(s); DOIs: 10.1021/acs.analchem.3c02697, 10.1038/s41467-023-37446-4, 10.1186/s13321-020-00477-w

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
