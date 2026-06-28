---
name: gcms-deconvolution-identification-workflow
description: 'Use when you have GC-MS data (mzML / CDF, typically EI) and want deconvolved,
  retention-index-validated compound identifications — spectral deconvolution of co-eluting
  peaks, EI library matching, RI calibration, and differential analysis.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - GC-MS
  stage_count: 5
  member_skills:
  - gc-ms-spectral-deconvolution
  - gcms-spectrum-deconvolution
  - pure-component-spectrum-extraction
  - mass-spectral-component-extraction
  - deconvolved-spectrum-comparison
  - electron-ionization-spectral-comparison
  - spectral-similarity-scoring-ei-simple
  - gc-ms-spectral-library-matching
  - mass-spectrometry-network-construction
  - retention-index-calibration-application
  - retention-index-assignment-and-filtering
  - low-resolution-compound-identification
  - gc-column-polarity-specific-ri-filtering
  - kovats-retention-index-extraction-and-assignment
  - group-comparison-statistics
  - gc-ms-data-preprocessing-and-normalization
  - gcxgc-ms-multivariate-analysis
  - univariate-statistical-testing-for-metabolomics
  - permanova-statistical-testing-multivariate-groups
  - feature-consolidation-across-samples
  - mass-spectrometry-feature-grouping
  - feature-table-matrix-assembly
  - feature-alignment-metabolomics
  member_tools:
  - MSHub
  - GNPS
  - GNPS_GC
  - PyTorch
  - Python 3
  - conda
  - GCMSFormer
  - mssearchr
  - R
  - NIST API
  - CoreMS
  - LowResMassSpectralMatch
  - GC_RI_Calibration
  - MetaMS
  - PNNLMetV20191015.MSL
  - mspcompiler
  - future
  - future.apply
  - Lib2NIST
  - MS-DIAL
  - MoNA
  - RIKEN
  - NIST MS Search
  - MS Search
  - R statistical environment
  - NIST Library Installation
  - LargeMetabo
  - Marker_Identify
  - e1071
  - FSelector
  - mixOmics
  - siggenes
  - NPFimg
  - XCMS
  - RGCxGC
  - colorRamps
  - omu (omu_summary function)
  - assign_hierarchy
  - omu_summary
  - omu_anova
  - count_fold_changes
  - transform_samples
  - MetaboDirect
  - vegan (R package)
  - Python 3.8
  - R 4.0.2
  - vegan
  - Python
  - BreathXplorer
  - Python pandas
  - patRoon
  - OpenMS
  - enviPick
  - KPIC2
  - PFΔScreen
  - pyOpenMS
  - pandas
  - MsFeatures
  - faahKO
  - mzrtsim
  - SummarizedExperiment
  - R base
  - openNAU
  - MetaQC
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# GC-MS Deconvolution and Identification

## Summary

End-to-end GC-MS annotation: deconvolve co-eluting EI spectra, match to GC-MS libraries with retention-index support, and compare groups.


## When to use

Use when you have GC-MS data (mzML / CDF, typically EI) and want deconvolved, retention-index-validated compound identifications — spectral deconvolution of co-eluting peaks, EI library matching, RI calibration, and differential analysis.


## When NOT to use

- The data is not GC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — deconvolution

**Goal:** GC-MS EI spectral deconvolution + peak detection

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table, mgf

**Candidate leaf skills:** `gc-ms-spectral-deconvolution` (primary), `gcms-spectrum-deconvolution`, `pure-component-spectrum-extraction`, `mass-spectral-component-extraction`, `deconvolved-spectrum-comparison`

**Tools:** MSHub, GNPS, GNPS_GC, PyTorch, Python 3, conda, GCMSFormer

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.analchem.3c05772, 10.1038/s41587-020-0700-3

### Stage 2 — ei_library_match

**Goal:** identify compounds by EI spectral library matching

**EDAM operation:** operation_3631

**Inputs:** mgf · **Outputs:** tsv

**Candidate leaf skills:** `electron-ionization-spectral-comparison` (primary), `spectral-similarity-scoring-ei-simple`, `gc-ms-spectral-library-matching`, `mass-spectrometry-network-construction`

**Tools:** mssearchr, R, NIST API, CoreMS, LowResMassSpectralMatch, GC_RI_Calibration, MetaMS, GNPS_GC

**Grounding:** 3 KB(s); DOIs: 10.1021/jasms.5c00322, 10.1038/s41587-020-0700-3, 10.5281/zenodo.14009575

### Stage 3 — retention_index

**Goal:** retention index calibration + RI-filtered identifications

**EDAM operation:** operation_3695

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `retention-index-calibration-application` (primary), `retention-index-assignment-and-filtering`, `low-resolution-compound-identification`, `gc-column-polarity-specific-ri-filtering`, `kovats-retention-index-extraction-and-assignment`

**Tools:** CoreMS, GC_RI_Calibration, LowResMassSpectralMatch, PNNLMetV20191015.MSL, mspcompiler, R, future, future.apply, Lib2NIST, MS-DIAL, MoNA, RIKEN, NIST MS Search, MS Search, R statistical environment, NIST Library Installation

**Grounding:** 2 KB(s); DOIs: 10.1021/acs.analchem.2c05389, 10.5281/zenodo.14009575

### Stage 4 — statistics

**Goal:** differential GC-MS feature analysis between groups

**EDAM operation:** operation_3659

**Inputs:** feature-table, tsv · **Outputs:** tsv

**Candidate leaf skills:** `group-comparison-statistics` (primary), `gc-ms-data-preprocessing-and-normalization`, `gcxgc-ms-multivariate-analysis`, `univariate-statistical-testing-for-metabolomics`, `permanova-statistical-testing-multivariate-groups`

**Tools:** LargeMetabo, Marker_Identify, e1071, FSelector, mixOmics, siggenes, NPFimg, XCMS, RGCxGC, R, colorRamps, omu (omu_summary function), assign_hierarchy, omu_summary, omu_anova, count_fold_changes, transform_samples, MetaboDirect, vegan (R package), Python 3.8, R 4.0.2, vegan, Python

**Grounding:** 7 KB(s); DOIs: 10.1016/j.microc.2020.104830, 10.1021/acs.analchem.1c03163, 10.1021/acs.analchem.1c03163?ref=, 10.1093/bib/bbac455 …

### Stage 5 — fusion

**Goal:** consolidate GC-MS identifications + stats into a master table

**EDAM operation:** operation_3434

**Inputs:** feature-table, tsv · **Outputs:** tsv

**Candidate leaf skills:** `feature-consolidation-across-samples` (primary), `mass-spectrometry-feature-grouping`, `feature-table-matrix-assembly`, `feature-alignment-metabolomics`

**Tools:** Python, BreathXplorer, Python pandas, patRoon, XCMS, OpenMS, enviPick, KPIC2, PFΔScreen, pyOpenMS, pandas, MsFeatures, faahKO, R, mzrtsim, SummarizedExperiment, R base, openNAU, MetaQC

**Grounding:** 6 KB(s); DOIs: 10.1007/s00216-023-05070-2, 10.1021/ac051437y, 10.1021/acs.analchem.5c01213, 10.1021/jasms.4c00152 …

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — these are the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
