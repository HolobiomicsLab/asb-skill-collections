---
name: ms-imaging-spatial-metabolomics-workflow
description: 'Use when you have mass-spectrometry imaging data (imzML, e.g. MALDI/DESI)
  and want spatially-resolved metabolite annotations — pixel preprocessing and m/z
  alignment, FDR-controlled spatial annotation, spatial segmentation, and region-wise
  comparison.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - MS-imaging
  stage_count: 4
  member_skills:
  - mass-spectrometry-imaging-data-import
  - mass-spectrometry-peak-detection-and-alignment
  - mass-spectrometry-image-reconstruction
  - spatial-pixel-coordinate-alignment
  - spectral-peak-alignment-across-pixels
  - spatial-metabolomics-feature-annotation
  - imaging-mass-spectrometry-ion-identification
  - mass-spectral-feature-annotation
  - m-z-metabolite-annotation-mapping
  - metabolite-annotation-at-scale
  - spatial-segmentation-shrunken-centroids
  - cardinal-object-structure-understanding
  - spatial-coordinate-mapping-msi
  - single-cell-spatial-metabolomics-data-processing
  - mass-spectrometry-peak-intensity-encoding
  - spatial-correlation-analysis-in-imaging-mass-spectrometry
  - spot-level-intensity-aggregation
  member_tools:
  - Cardinal
  - CardinalIO
  - R
  - matter
  - BiocManager
  - BiocParallel
  - Cardinal 3.6
  - pewpew
  - pewlib
  - pewpew (pew²)
  - Python
  - imzML Writer
  - imzML Scout
  - msconvert
  - SpaMTP
  - Seurat
  - pandas
  - h5py
  - Graph-attention autoencoder
  - scanpy
  - SMART
  - RefineLipids
  - SearchAnnotations
  - dplyr
  - HMDB Database
  - Lipidmaps Database
  - ScSpaMet repository
  - Zenodo deposit (raw data)
  - Mesmer
  - STAGATE
  - mass2adduct
  - corrPairsMSI
  - corrPairsMSIchunks
  - msimat
  - adductMatch
  - diffGetPeaks
  - mass2adduct (R package)
  - spatialMETA
  - spatialmeta.pp.filter_cells_sm
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Mass Spectrometry Imaging — Spatial Metabolomics

## Summary

End-to-end MSI spatial metabolomics: from imzML to FDR-controlled ion-image annotations and anatomically-segmented, region-compared metabolite maps.


## When to use

Use when you have mass-spectrometry imaging data (imzML, e.g. MALDI/DESI) and want spatially-resolved metabolite annotations — pixel preprocessing and m/z alignment, FDR-controlled spatial annotation, spatial segmentation, and region-wise comparison.


## When NOT to use

- The data is not MS-imaging.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — preprocess_imaging

**Goal:** load imzML, peak pick, align m/z across pixels

**EDAM operation:** operation_3215

**Inputs:** imzML · **Outputs:** feature-table

**Candidate leaf skills:** `mass-spectrometry-imaging-data-import` (primary), `mass-spectrometry-peak-detection-and-alignment`, `mass-spectrometry-image-reconstruction`, `spatial-pixel-coordinate-alignment`, `spectral-peak-alignment-across-pixels`

**Tools:** Cardinal, CardinalIO, R, matter, BiocManager, BiocParallel, Cardinal 3.6, pewpew, pewlib, pewpew (pew²), Python, imzML Writer, imzML Scout, msconvert

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.1c02138, 10.1021/acs.analchem.4c06520, 10.1093/bioinformatics/btv146, 10.1529/biophysj.103.038422

### Stage 2 — spatial_annotation

**Goal:** annotate ion images to metabolites with FDR control

**EDAM operation:** operation_3803

**Inputs:** feature-table · **Outputs:** tsv

**Candidate leaf skills:** `spatial-metabolomics-feature-annotation` (primary), `imaging-mass-spectrometry-ion-identification`, `mass-spectral-feature-annotation`, `m-z-metabolite-annotation-mapping`, `metabolite-annotation-at-scale`

**Tools:** SpaMTP, R, Seurat, Cardinal, pandas, h5py, Graph-attention autoencoder, scanpy, SMART, RefineLipids, SearchAnnotations, dplyr, HMDB Database, Lipidmaps Database

**Grounding:** 3 KB(s); DOIs: 10.1021/acs.analchem.4c06210, 10.1101/2024.10.14.618269, 10.1101/2024.10.31.621429v1

### Stage 3 — segmentation

**Goal:** spatial segmentation / clustering into regions

**EDAM operation:** operation_3432

**Inputs:** feature-table · **Outputs:** tsv

**Candidate leaf skills:** `spatial-segmentation-shrunken-centroids` (primary), `cardinal-object-structure-understanding`, `spatial-coordinate-mapping-msi`

**Tools:** SpaMTP, dplyr, R, Cardinal, Seurat

**Grounding:** 2 KB(s); DOIs: 10.1101/2024.10.14.618269, 10.1101/2024.10.31.621429v1

### Stage 4 — region_statistics

**Goal:** compare metabolite intensities across spatial regions

**EDAM operation:** operation_3659

**Inputs:** tsv, tsv · **Outputs:** tsv

**Candidate leaf skills:** `single-cell-spatial-metabolomics-data-processing` (primary), `mass-spectrometry-peak-intensity-encoding`, `spatial-correlation-analysis-in-imaging-mass-spectrometry`, `spot-level-intensity-aggregation`

**Tools:** ScSpaMet repository, Zenodo deposit (raw data), Mesmer, scanpy, STAGATE, pandas, h5py, mass2adduct, R, corrPairsMSI, corrPairsMSIchunks, msimat, adductMatch, diffGetPeaks, mass2adduct (R package), spatialMETA, spatialmeta.pp.filter_cells_sm

**Grounding:** 5 KB(s); DOIs: 10.1021/acs.analchem.0c04720, 10.1021/acs.analchem.4c06210, 10.1038/s41467-023-43917-5, 10.1038/s41467-025-63915-z …

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — these are the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
