---
name: single-cell-spatial-metabolomics-data-processing
description: 'Use when you have raw IMC and SIMS image data from the same tissue region(s)
  and need to: (1) register the two modalities spatially, (2) segment individual cells
  across both images, (3) extract per-cell protein and metabolite intensity vectors,
  and (4) prepare the data for downstream joint analysis.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3382
  tools:
  - ScSpaMet repository
  - Zenodo deposit (raw data)
  - Mesmer
  - Custom affine transformation module (src/)
  - Keras VAE (scSpaMet/)
  techniques:
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-023-43917-5
  title: scSpaMet
- doi: 10.5281/zenodo.6784251
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scspamet_cq
    doi: 10.1038/s41467-023-43917-5
    title: scSpaMet
  dedup_kept_from: coll_scspamet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-43917-5
  all_source_dois:
  - 10.1038/s41467-023-43917-5
  - 10.5281/zenodo.6784251
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# single-cell-spatial-metabolomics-data-processing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A multi-stage pipeline for aligning, segmenting, and extracting single-cell intensity measurements from co-registered imaging mass cytometry (IMC) protein and secondary ion mass spectrometry (SIMS) metabolite image pairs. This skill enables joint proteomics and metabolomics profiling at subcellular resolution in tissue.

## When to use

You have raw IMC and SIMS image data from the same tissue region(s) and need to: (1) register the two modalities spatially, (2) segment individual cells across both images, (3) extract per-cell protein and metabolite intensity vectors, and (4) prepare the data for downstream joint analysis (e.g., clustering, correlation, or VAE embedding). Use this skill when your goal is to produce aligned, segmented single-cell matrices linking proteomics and metabolomics measurements.

## When NOT to use

- Input images are already pre-registered and segmented; start at the intensity extraction step instead.
- You have only one imaging modality (protein or metabolite alone) and do not need spatial co-registration.
- Your tissue or cell types are too dense or morphologically complex for reliable segmentation with available masks or Mesmer model training data.

## Inputs

- Raw IMC (protein) image data (multi-channel matrix format)
- Raw SIMS (metabolite) image data (multi-channel matrix format)
- Image metadata (pixel dimensions, channel annotations)
- Tissue region coordinates or field-of-view (FOV) definitions

## Outputs

- Registered and aligned IMC and SIMS image pairs
- Single-cell segmentation masks (binary or label images)
- Per-cell protein intensity matrix (cells × protein features)
- Per-cell metabolite intensity matrix (cells × metabolite features)
- Segmentation visualization overlays

## How to apply

Execute the ScSpaMet pipeline in sequence: First, apply affine transformation to register IMC and SIMS images using manual or fiducial-based alignment (Notebook 02). Second, perform single-cell segmentation using either classical watershed or Mesmer deep learning (Notebooks 03, 11), generating segmentation masks that define cell boundaries across both modalities. Third, extract single-cell intensity values by applying the segmentation masks to the aligned IMC and SIMS images (Notebook 04), producing per-cell feature vectors for proteins and metabolites respectively. Validate intermediate outputs by confirming segmentation mask dimensions match image dimensions and intensity extraction produces non-empty matrices with consistent row (cell) and column (feature) counts across both modalities. Compare regenerated outputs against reference results from the published paper to confirm correct alignment, cell count, and feature ranges.

## Related tools

- **ScSpaMet repository** (Provides the complete analysis pipeline, custom segmentation, registration, and VAE embedding code; contains Jupyter notebooks orchestrating all processing steps.) — https://github.com/coskunlab/ScSpaMet
- **Zenodo deposit (raw data)** (Hosts raw IMC and SIMS image data and preprocessed intermediate outputs for pipeline reproducibility.) — https://doi.org/10.5281/zenodo.6784251
- **Mesmer** (Deep-learning-based cell segmentation model used as an alternative to classical watershed methods for improved accuracy on dense or morphologically complex tissues.)
- **Custom affine transformation module (src/)** (Implements spatial registration between IMC and SIMS image coordinate systems.) — https://github.com/coskunlab/ScSpaMet
- **Keras VAE (scSpaMet/)** (Enables joint embedding of protein and metabolite feature vectors for integrated analysis after single-cell extraction.) — https://github.com/coskunlab/ScSpaMet

## Evaluation signals

- Registered IMC and SIMS images show spatial overlap of anatomically corresponding tissue regions with sub-pixel accuracy, verified by visual inspection of segmentation overlay.
- Segmentation masks produce a cell count consistent with the published paper and tissue morphology; cells are non-overlapping polygons with area ranges matching expected cell sizes.
- Per-cell intensity matrices are complete (no missing values in expected feature columns), have consistent dimensionality (cells × features) across both modalities, and show protein/metabolite intensity distributions consistent with the reference paper figures.
- Intermediate output file formats (image dimensions, feature names, matrix shapes) match the expected schema documented in the README and reference outputs in Zenodo deposit.
- Regenerated figures (segmentation masks, intensity distributions, cell-type assignments) visually match or have quantitative overlap (e.g., >95% Dice similarity) with published figures.

## Limitations

- Segmentation quality depends on image signal-to-noise ratio and tissue morphology; dense or overlapping cells may be undersegmented or incorrectly split.
- Manual affine registration is user-dependent; misalignment introduces systematic errors in downstream co-localization and correlation analyses.
- Mesmer segmentation requires a pre-trained model; performance may degrade on tissue types or staining protocols substantially different from training data.
- The pipeline assumes all input images have consistent pixel dimensions and channel annotations; missing metadata or channel misidentification will propagate through intensity extraction.

## Evidence

- [readme] Registration of IMC and SIMS images for different imaging regions: "02 Registration of IMC and SIMS images for different imaging regions"
- [readme] Single-cell level segmentation and visualization: "03 Single-cell level segmentation and visualization of segmentation masks"
- [readme] Single-cell intensity extraction workflow: "04 Single-cell level intensity extraction and single-cell proteomics clustering"
- [readme] Raw data repository location: "You can find the raw data here: https://doi.org/10.5281/zenodo.6784251"
- [readme] Custom source code for segmentation and registration: ""src" folder contains customs scripts used: affine transformation"
- [readme] Alternative segmentation approach: "11 Segmentation of single-cell with Mesmer pipeline"
- [other] Paper title indicating joint modality profiling: "A framework for performing single-cell spatial metabolomics with cell-type specific protein profiling for tissue systems biology"
