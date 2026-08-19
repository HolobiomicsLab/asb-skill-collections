---
name: stable-isotope-tracing-fluxomics-workflow
description: 'Use when you have LC-MS data from a stable-isotope (e.g. 13C / 15N)
  tracing experiment and want labelling / flux information — detect features, extract
  per-feature isotopologue distributions, correct for natural isotope abundance, and
  compute mass-isotopomer distributions and fractional labelling enrichment across
  conditions or timepoints.

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
  - mass-spectral-feature-alignment
  - lcms-peak-detection-and-alignment
  - isotope-labeling-data-integration
  - mass-isotopologue-adduct-grouping
  - isotope-labelling-feature-interpretation
  - metabolite-feature-grouping-by-adduct-isotope
  - isotopologue-signature-detection
  - isotopic-impurity-accounting
  - tracer-impurity-correction-modeling
  - natural-isotope-abundance-propagation
  - naturally-occurring-isotope-contribution-accounting
  - isotopologue-distribution-matrix-construction
  - stable-isotope-labeling-quantification
  - fractional-abundance-transformation
  - metabolite-fold-change-statistical-testing
  - metabolite-abundance-normalization-across-conditions
  - tab-delimited-export-formatting-for-metabolomics
  - stable-isotope-labelling-feature-detection
  member_tools:
  - MZmine2
  - Optimus
  - OpenMS
  - geoRge
  - R
  - XCMS
  - ElemCor
  - isoSCAN
  - mzR
  - enviPat
  - Proteowizard MSconvert
  - INTEGRATE
  - Agilent 1290 Infinity UHPLC system + Agilent 6550 iFunnel Q-TOF mass spectrometer
  - constraint-based stoichiometric metabolic models (e.g., ENGRO2)
  coverage_gaps: []
  derived_from_workflows:
  - coll_idsl_ipa_cq
  - coll_corems
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Stable-Isotope Tracing (isotopologue extraction -> labelling analysis)

## Summary

Labelled LC-MS in, a labelling table out: isotopologue extraction, natural-abundance correction, and mass-isotopomer-distribution / enrichment analysis.


## When to use

Use when you have LC-MS data from a stable-isotope (e.g. 13C / 15N) tracing experiment and want labelling / flux information — detect features, extract per-feature isotopologue distributions, correct for natural isotope abundance, and compute mass-isotopomer distributions and fractional labelling enrichment across conditions or timepoints.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess

**Goal:** raw labelled LC-MS -> aligned feature table (all isotopologues)

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table

**Candidate leaf skills:** `peak-detection-and-mass-alignment` (primary), `mass-spectral-feature-alignment`, `lcms-peak-detection-and-alignment`, `isotope-labeling-data-integration`, `mass-isotopologue-adduct-grouping`

**Tools (primary):** MZmine2, Optimus, OpenMS

**Other candidate tools:** R, devtools, BiocManager, dplyr, tidyr, readr, stringr, tibble, purrr, ggplot2, IsoPairFinder, ISFrag, XCMS, CAMERA, MS-DIAL, Centwave, FeatureFinderMetabo, ADAP, SLAW

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.1c01644, 10.1021/acs.analchem.1c02687, 10.1021/acs.jnatprod.7b00737, 10.1101/2021.12.05.471237v2

### Stage 2 — isotopologue_extract

**Goal:** feature table -> per-metabolite isotopologue intensity distributions

**EDAM operation:** operation_3799

**Inputs:** feature-table · **Outputs:** tsv

**Candidate leaf skills:** `isotope-labelling-feature-interpretation` (primary), `metabolite-feature-grouping-by-adduct-isotope`, `isotopologue-signature-detection`

**Tools (primary):** geoRge, R, XCMS

**Other candidate tools:** khipu, Python, Asari, pandas, numpy, scipy, scikit-learn, matplotlib, MamsiStructSearch, MAMSI (MamsiStructSearch)

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.5b03628, 10.1021/acs.analchem.5c01327, 10.1371/journal.pcbi.1011814, 10.1371/journal.pcbi.1011912

### Stage 3 — natural_abundance_correction

**Goal:** correct isotopologue distributions for natural isotope abundance

**EDAM operation:** operation_3435

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `isotopic-impurity-accounting` (primary), `tracer-impurity-correction-modeling`, `natural-isotope-abundance-propagation`, `naturally-occurring-isotope-contribution-accounting`, `isotopologue-distribution-matrix-construction`

**Tools (primary):** ElemCor

**Other candidate tools:** IsoCor, FluxFix

**Grounding:** 1 KB(s); DOIs: 10.1186/s12859-019-2669-9

### Stage 4 — labelling_analysis

**Goal:** corrected distributions -> mass-isotopomer distribution / fractional enrichment

**EDAM operation:** operation_3799

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `stable-isotope-labeling-quantification` (primary), `fractional-abundance-transformation`, `metabolite-fold-change-statistical-testing`

**Tools (primary):** R, isoSCAN, mzR, enviPat, Proteowizard MSconvert

**Other candidate tools:** ElemCor, geoRge, XCMS

**Grounding:** 3 KB(s); DOIs: 10.1021/acs.analchem.0c02998, 10.1021/acs.analchem.5b03628, 10.1186/s12859-019-2669-9

### Stage 5 — report

**Goal:** consolidate labelling / enrichment results into a tracing report table

**EDAM operation:** operation_3434

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `metabolite-abundance-normalization-across-conditions` (primary), `tab-delimited-export-formatting-for-metabolomics`, `stable-isotope-labelling-feature-detection`

**Tools (primary):** INTEGRATE, Agilent 1290 Infinity UHPLC system + Agilent 6550 iFunnel Q-TOF mass spectrometer, constraint-based stoichiometric metabolic models (e.g., ENGRO2)

**Other candidate tools:** R, rmarkdown, knitr, ggplot2, metaboprep, geoRge, XCMS

**Grounding:** 3 KB(s); DOIs: 10.1021/acs.analchem.5b03628, 10.1093/bioinformatics/btac059/6522114, 10.1371/journal.pcbi.1009337

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
