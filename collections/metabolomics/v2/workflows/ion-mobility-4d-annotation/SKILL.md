---
name: ion-mobility-4d-annotation-workflow
description: 'Use when you have ion-mobility LC-IMS-MS/MS data (e.g. timsTOF / PASEF)
  and want CCS-aware annotations — 4D feature extraction with collision cross section,
  CCS calibration and filtering, CCS-aware library matching, and (optional) networking.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - ion-mobility-MS
  stage_count: 4
  member_skills:
  - multidimensional-feature-detection-and-alignment
  - ion-mobility-heatmap-visualization
  - ion-mobility-feature-classification
  - ion-mobility-dimension-detection
  - multidimensional-coordinate-alignment
  - collision-cross-section-calibration-ccs
  - collision-cross-section-calibration
  - collision-cross-section-calculation
  - collision-cross-section-measurement-quality-control
  - collision-cross-section-matching-and-annotation
  - reference-library-alignment
  - 4d-lcimmsms-feature-extraction
  - fragmentation-pattern-spectral-matching
  - feature-based-molecular-network-interpretation
  - spectral-similarity-network-building
  - molecular-networking-construction
  - feature-network-construction-from-mass-spectrometry
  - spectral-similarity-network-generation
  member_tools:
  - DEIMoS
  - Python
  - conda
  - pip
  - Snakemake
  - ProteoWizard msconvert
  - numpy
  - Jupyter Notebook
  - scikit-learn
  - R
  - MZmine3
  - GNPS FBMN
  - Google Colab
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

# Ion Mobility (4D LC-IMS-MS/MS) Annotation

## Summary

End-to-end 4D ion-mobility annotation: extract CCS-resolved features, calibrate CCS, and annotate with collision-cross-section-aware matching.


## When to use

Use when you have ion-mobility LC-IMS-MS/MS data (e.g. timsTOF / PASEF) and want CCS-aware annotations — 4D feature extraction with collision cross section, CCS calibration and filtering, CCS-aware library matching, and (optional) networking.


## When NOT to use

- The data is not ion-mobility-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess_4d

**Goal:** 4D LC-IMS-MS/MS feature extraction (with CCS)

**EDAM operation:** operation_3215

**Inputs:** mzML · **Outputs:** feature-table, mgf

**Candidate leaf skills:** `multidimensional-feature-detection-and-alignment` (primary), `ion-mobility-heatmap-visualization`, `ion-mobility-feature-classification`, `ion-mobility-dimension-detection`, `multidimensional-coordinate-alignment`

**Tools (primary):** DEIMoS, Python, conda, pip, Snakemake, ProteoWizard msconvert

**Other candidate tools:** Mirador, IonToolPack, PeakQC, MOCCal, mzmine, JDK 25, JavaFX 24, numpy

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.1c05017, 10.1021/acs.analchem.3c04290, 10.1021/jasms.4c00146, 10.1038/s41587-023-01690-2

### Stage 2 — ccs_calibration

**Goal:** collision cross section calibration + filtering

**EDAM operation:** operation_3695

**Inputs:** feature-table · **Outputs:** feature-table

**Candidate leaf skills:** `collision-cross-section-calibration-ccs` (primary), `collision-cross-section-calibration`, `collision-cross-section-calculation`, `collision-cross-section-measurement-quality-control`

**Tools (primary):** DEIMoS, conda, pip, Python, numpy

**Other candidate tools:** Snakemake, MOCCal, MOCCal (Multi-Omic CCS Calibrator), DEIMoS (Data-Exploratory Ion Mobility MS), R, MobiLipid, ggplot2, data.table

**Grounding:** 3 KB(s); DOIs: 10.1021/acs.analchem.1c05017, 10.1021/acs.analchem.3c04290, 10.1021/acs.analchem.4c01253

### Stage 3 — ccs_library_match

**Goal:** CCS-aware spectral / library annotation

**EDAM operation:** operation_3631

**Inputs:** mgf, feature-table · **Outputs:** tsv

**Candidate leaf skills:** `collision-cross-section-matching-and-annotation` (primary), `reference-library-alignment`, `4d-lcimmsms-feature-extraction`, `fragmentation-pattern-spectral-matching`

**Tools (primary):** Python, Jupyter Notebook, scikit-learn

**Other candidate tools:** R, MobiLipid, R (ggplot2, data.table, DT packages), RDKit

**Grounding:** 2 KB(s); DOIs: 10.1002/anie.202507483, 10.1021/acs.analchem.4c01253

### Stage 4 — networking  [OPTIONAL]

**Goal:** (optional) molecular networking of IM-resolved features

**EDAM operation:** operation_3432

**Inputs:** mgf, feature-table, tsv · **Outputs:** graphml

**Candidate leaf skills:** `feature-based-molecular-network-interpretation` (primary), `spectral-similarity-network-building`, `molecular-networking-construction`, `feature-network-construction-from-mass-spectrometry`, `spectral-similarity-network-generation`

**Tools (primary):** R, Jupyter Notebook, MZmine3, GNPS FBMN, Google Colab

**Other candidate tools:** q2-qemistree, SIRIUS, CSI:FingerID, ZODIAC, MZmine2, ClassyFire, ENPKG, MZmine, MEMO, networkx, treelib, mass2chem, metDataModel, Python 3, asari, khipu, Optimus, GNPS, Cytoscape

**Grounding:** 5 KB(s); DOIs: 10.1021/acs.analchem.2c05810, 10.1021/acs.jnatprod.7b00737, 10.1021/acscentsci.3c00800, 10.1038/s41589-020-00677-3 …

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
