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
  - ion-mobility-feature-classification
  - multidimensional-feature-detection-and-alignment
  - ion-mobility-heatmap-visualization
  - ion-mobility-dimension-detection
  - multidimensional-coordinate-alignment
  - collision-cross-section-calibration-ccs
  - collision-cross-section-calibration
  - collision-cross-section-calculation
  - collision-cross-section-measurement-quality-control
  - collision-cross-section-matching-and-annotation
  - reference-library-alignment
  - ion-mobility-reference-matching
  - 4d-lcimmsms-feature-extraction
  - fragmentation-pattern-spectral-matching
  - molecular-networking-construction
  - spectral-library-molecular-networking
  - spectral-similarity-network-building
  - metabolomic-spectral-annotation-and-molecular-family-clustering
  - spectral-similarity-network-generation
  member_tools:
  - Python
  - MOCCal
  - DEIMoS
  - conda
  - pip
  - Snakemake
  - ProteoWizard msconvert
  - Mirador
  - IonToolPack
  - PeakQC
  - mzmine
  - JDK 25
  - JavaFX 24
  - numpy
  - MOCCal (Multi-Omic CCS Calibrator)
  - DEIMoS (Data-Exploratory Ion Mobility MS)
  - R
  - MobiLipid
  - ggplot2
  - data.table
  - Jupyter Notebook
  - scikit-learn
  - R (ggplot2, data.table, DT packages)
  - RDKit
  - ENPKG
  - MEMO
  - MSHub
  - GNPS
  - q2-qemistree
  - SIRIUS
  - CSI:FingerID
  - ZODIAC
  - MZmine2
  - GNPS FBMN
  - ClassyFire
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - MIBiG
  - Optimus
  - Cytoscape
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

**Candidate leaf skills:** `ion-mobility-feature-classification` (primary), `multidimensional-feature-detection-and-alignment`, `ion-mobility-heatmap-visualization`, `ion-mobility-dimension-detection`, `multidimensional-coordinate-alignment`

**Tools:** Python, MOCCal, DEIMoS, conda, pip, Snakemake, ProteoWizard msconvert, Mirador, IonToolPack, PeakQC, mzmine, JDK 25, JavaFX 24, numpy

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.1c05017, 10.1021/acs.analchem.3c04290, 10.1021/jasms.4c00146, 10.1038/s41587-023-01690-2

### Stage 2 — ccs_calibration

**Goal:** collision cross section calibration + filtering

**EDAM operation:** operation_3695

**Inputs:** feature-table · **Outputs:** feature-table

**Candidate leaf skills:** `collision-cross-section-calibration-ccs` (primary), `collision-cross-section-calibration`, `collision-cross-section-calculation`, `collision-cross-section-measurement-quality-control`

**Tools:** DEIMoS, conda, pip, Python, numpy, Snakemake, MOCCal, MOCCal (Multi-Omic CCS Calibrator), DEIMoS (Data-Exploratory Ion Mobility MS), R, MobiLipid, ggplot2, data.table

**Grounding:** 3 KB(s); DOIs: 10.1021/acs.analchem.1c05017, 10.1021/acs.analchem.3c04290, 10.1021/acs.analchem.4c01253

### Stage 3 — ccs_library_match

**Goal:** CCS-aware spectral / library annotation

**EDAM operation:** operation_3631

**Inputs:** mgf, feature-table · **Outputs:** tsv

**Candidate leaf skills:** `collision-cross-section-matching-and-annotation` (primary), `reference-library-alignment`, `ion-mobility-reference-matching`, `4d-lcimmsms-feature-extraction`, `fragmentation-pattern-spectral-matching`

**Tools:** Python, Jupyter Notebook, scikit-learn, R, MobiLipid, R (ggplot2, data.table, DT packages), MOCCal, DEIMoS, RDKit

**Grounding:** 3 KB(s); DOIs: 10.1002/anie.202507483, 10.1021/acs.analchem.3c04290, 10.1021/acs.analchem.4c01253

### Stage 4 — networking  [OPTIONAL]

**Goal:** (optional) molecular networking of IM-resolved features

**EDAM operation:** operation_3432

**Inputs:** mgf · **Outputs:** graphml

**Candidate leaf skills:** `molecular-networking-construction` (primary), `spectral-library-molecular-networking`, `spectral-similarity-network-building`, `metabolomic-spectral-annotation-and-molecular-family-clustering`, `spectral-similarity-network-generation`

**Tools:** ENPKG, MZmine, MEMO, MSHub, GNPS, q2-qemistree, SIRIUS, CSI:FingerID, ZODIAC, MZmine2, GNPS FBMN, ClassyFire, antiSMASH, BiG-SCAPE, NPLinker, MIBiG, Optimus, Cytoscape

**Grounding:** 6 KB(s); DOIs: 10.1021/acs.jnatprod.7b00737, 10.1021/acscentsci.3c00800, 10.1038/s41587-020-0700-3, 10.1038/s41589-020-00677-3 …

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — these are the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
