---
name: targeted-lcms-quantification-workflow
description: 'Use when you have targeted LC-MS data for a defined panel of analytes
  and want absolute or relative concentrations — extract and integrate the target
  transitions/ion chromatograms, build calibration curves from standards with internal-standard
  normalization, apply them to samples, and QC the batch (response drift, QC-sample
  RSD) to a reportable quantification table.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 5
  member_skills:
  - targeted-peak-detection-and-integration
  - chromatographic-peak-detection-and-integration
  - targeted-peak-detection-screening-and-validation
  - targeted-peak-extraction-ms1
  - m-z-and-retention-time-window-validation
  - calibration-curve-fitting-metabolomics
  - calibration-curve-validation
  - linear-regression-concentration-calibration
  - linear-regression-model-fitting
  - concentration-prediction-from-calibration-model
  - linear-regression-absolute-quantification
  - concentration-prediction-from-calibration-curves
  - qc-sample-variability-assessment
  - qc-sample-reliability-evaluation
  - qc-sample-batch-drift-correction
  - batch-effect-assessment-via-quality-metrics
  - signal-trend-assessment-across-injections
  - quality-control-report-generation
  - quality-control-metric-threshold-configuration
  - quality-control-metric-computation
  - qc-summary-table-extraction
  - compound-metric-tabulation
  member_tools:
  - TARDIS
  - Spectra
  - R
  - MSConvert (ProteoWizard)
  - xcms
  - MsExperiment
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
  - R (lm, weighted.lm)
  coverage_gaps: []
  derived_from_workflows:
  - coll_fbmn_stats_cq
  - coll_peakqc_cq
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Targeted LC-MS Quantification (calibration -> absolute concentrations)

## Summary

Targeted transitions in, a QC'd quantification table out: peak integration, calibration-curve fitting, internal-standard normalization, and batch QC.


## When to use

Use when you have targeted LC-MS data for a defined panel of analytes and want absolute or relative concentrations — extract and integrate the target transitions/ion chromatograms, build calibration curves from standards with internal-standard normalization, apply them to samples, and QC the batch (response drift, QC-sample RSD) to a reportable quantification table.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — integrate

**Goal:** raw targeted LC-MS -> integrated peak areas for target transitions

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table

**Candidate leaf skills:** `targeted-peak-detection-and-integration` (primary), `chromatographic-peak-detection-and-integration`, `targeted-peak-detection-screening-and-validation`, `targeted-peak-extraction-ms1`, `m-z-and-retention-time-window-validation`

**Tools (primary):** TARDIS, Spectra, R, MSConvert (ProteoWizard), xcms, MsExperiment

**Other candidate tools:** knitr, kableExtra, ProteoWizard MSConvert, IonToolPack, PeakQuant, PeakQC, Comparador

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.analchem.5c00567, 10.1021/jasms.4c00146

### Stage 2 — calibrate

**Goal:** calibrant standards -> calibration curves with internal-standard normalization

**EDAM operation:** operation_3435

**Inputs:** feature-table · **Outputs:** tsv

**Candidate leaf skills:** `calibration-curve-fitting-metabolomics` (primary), `calibration-curve-validation`, `linear-regression-concentration-calibration`, `linear-regression-model-fitting`

**Tools (primary):** R, mzQuality, SummarizedExperiment, mzQualityDashboard, R (lm, weighted.lm)

**Other candidate tools:** Shiny, QuantyFey, GetFeatistics, lme4, AER, R base, Python 3, networkx, mass2chem, khipu, RawFileReader, rawrr, R base stats package (lm function)

**Grounding:** 6 KB(s); DOIs: 10.1016/j.aca.2025.344571, 10.1021/acs.analchem.2c05810, 10.1021/acs.jproteome.0c00866, 10.1021/jasms.5c00073 …

### Stage 3 — quantify

**Goal:** apply calibration -> absolute / relative concentrations per sample

**EDAM operation:** operation_3799

**Inputs:** feature-table, tsv · **Outputs:** tsv

**Candidate leaf skills:** `concentration-prediction-from-calibration-model` (primary), `linear-regression-absolute-quantification`, `concentration-prediction-from-calibration-curves`

**Tools (primary):** R, mzQuality, SummarizedExperiment, mzQualityDashboard

**Other candidate tools:** GetFeatistics, lme4, AER

**Grounding:** 2 KB(s); DOIs: 10.1021/jasms.5c00073, 10.1515/jib-2025-0047

### Stage 4 — qc  [OPTIONAL]

**Goal:** (optional) batch QC — response drift, QC-sample RSD, outlier flagging

**EDAM operation:** operation_3435

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `qc-sample-variability-assessment` (primary), `qc-sample-reliability-evaluation`, `qc-sample-batch-drift-correction`, `batch-effect-assessment-via-quality-metrics`, `signal-trend-assessment-across-injections`

**Tools (primary):** R, mzQuality, SummarizedExperiment, mzQualityDashboard

**Other candidate tools:** notame, Biobase, MetCorR, OUKS, QComics, Sciex Multiquant

**Grounding:** 5 KB(s); DOIs: 10.1021/acs.analchem.3c03660, 10.1021/acs.jproteome.1c00392, 10.1021/jasms.5c00073, 10.1093/bioinformatics/btr597 …

### Stage 5 — report

**Goal:** consolidate concentrations + QC into a reportable quantification table

**EDAM operation:** operation_3434

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `quality-control-report-generation` (primary), `quality-control-metric-threshold-configuration`, `quality-control-metric-computation`, `qc-summary-table-extraction`, `compound-metric-tabulation`

**Tools (primary):** R, mzQuality, SummarizedExperiment, mzQualityDashboard

**Other candidate tools:** R ≥4.1.2, OUKS step 4 (Correction.R), OUKS step 6 (Filtering.R), ggplot, data.table, mpactr, ggplot2

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.2c04632, 10.1021/acs.jproteome.1c00392, 10.1021/jasms.5c00073, 10.1128/mra.00997-24

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
