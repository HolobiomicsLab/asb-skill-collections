---
name: tissue-spatial-analysis-pipeline-execution
description: Use when you have raw IMC (protein imaging) and SIMS (metabolite imaging) data from tissue regions that require spatial co-registration, single-cell-level intensity quantification, and joint analysis of protein–metabolite relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3452
  tools:
  - ScSpaMet
  - Mesmer
  - Keras
  - Jupyter Notebook
  - Zenodo Data Repository
  techniques:
  - MS-imaging
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tissue-spatial-analysis-pipeline-execution

## Summary

Execute a documented multi-stage pipeline for integrating spatial imaging data (IMC protein and SIMS metabolite) at single-cell resolution, including image registration, segmentation, feature extraction, and joint embedding. This skill enables reproducible re-execution of the ScSpaMet framework to regenerate published spatial metabolomics and proteomics results.

## When to use

You have raw IMC (protein imaging) and SIMS (metabolite imaging) data from tissue regions that require spatial co-registration, single-cell-level intensity quantification, and joint analysis of protein–metabolite relationships. Use this skill when you need to execute a complete, documented workflow from raw multi-modal imaging through cell-type-specific metabolite and protein profiling, with intermediate quality-control checkpoints.

## When NOT to use

- Input is already a pre-computed single-cell feature table or expression matrix; skip directly to dimension reduction or correlation analysis rather than re-running segmentation and feature extraction.
- Raw imaging data is in a non-standard format (not IMC or SIMS) or lacks the required instrument metadata for co-registration; custom adaptation of the pipeline is needed.
- The analysis goal is exploratory model selection or parameter tuning on a small pilot dataset; use a simplified or reduced-scale execution rather than the full multi-stage pipeline.

## Inputs

- Raw IMC image files (protein intensity stacks)
- Raw SIMS image files (metabolite intensity maps)
- Image metadata (field-of-view coordinates, instrument calibration)
- ScSpaMet repository (GitHub clone)
- Analysis configuration (YAML or JSON parameters for segmentation, clustering thresholds)

## Outputs

- Registered IMC and SIMS image pairs (aligned across modalities)
- Single-cell segmentation masks (binary or label images)
- Single-cell feature matrix (cells × proteins, cells × metabolites)
- Cell-type cluster assignments (from proteomics clustering)
- VAE joint embedding (latent representation of protein–metabolite co-variation)
- Metabolite difference and spatial distance matrices (region-specific or cell-type-specific)
- Protein–metabolite correlation matrices
- Publication-matched figures and summary tables

## How to apply

Clone the ScSpaMet repository and download the raw data deposit from Zenodo (https://doi.org/10.5281/zenodo.6784251). Install all dependencies (Python packages, R libraries, conda environments) as specified in the repository documentation. Execute the numbered Jupyter notebooks sequentially: (01) preprocessing of IMC and SIMS images, (02) image registration across modalities and fields-of-view, (03) single-cell segmentation using Mesmer or alternative pipeline, (04) single-cell intensity extraction and proteomics clustering, (05–10) VAE joint embedding, metabolite regional analysis, correlation analysis, and large FOV quantification. For each major output (segmentation masks, feature matrices, embeddings), verify that intermediate file dimensions, formats, and data ranges match expected outputs from the pipeline configuration before proceeding to the next stage. Compare final results (figures, tables, correlation coefficients, cluster assignments) against reference outputs in the published paper using manual inspection or quantitative diff tools.

## Related tools

- **ScSpaMet** (Complete analysis pipeline orchestrating image registration, segmentation, feature extraction, VAE embedding, and spatial metabolite–protein correlation analysis) — https://github.com/coskunlab/ScSpaMet
- **Mesmer** (Single-cell segmentation of IMC and SIMS images (Notebook 11))
- **Keras** (Variational autoencoder (VAE) implementation for joint protein–metabolite embedding (Notebooks 05–07))
- **Jupyter Notebook** (Interactive execution environment for 12 sequential analysis notebooks)
- **Zenodo Data Repository** (Source of raw IMC and SIMS imaging data) — https://doi.org/10.5281/zenodo.6784251

## Examples

```
cd ScSpaMet && jupyter notebook notebooks/01_processing_imc_sims.ipynb && jupyter notebook notebooks/02_registration.ipynb && jupyter notebook notebooks/03_segmentation.ipynb && jupyter notebook notebooks/04_intensity_extraction.ipynb
```

## Evaluation signals

- Intermediate file dimensions match expected shapes: segmentation masks are 2D images with integer cell labels; single-cell feature matrix has rows = segmented cells, columns = protein or metabolite features.
- Cell-type cluster assignments are reproducible: the proteomics clustering (Notebook 04) produces the same number of clusters and silhouette scores as reported in the paper.
- Registered IMC and SIMS images show visual alignment: overlay of registered images exhibits minimal translation/rotation residuals; manual inspection of 3–5 landmark cells confirms spatial correspondence.
- VAE latent embeddings and protein–metabolite correlations (Notebooks 05, 09) match published correlation coefficients and heatmap patterns within ±5% tolerance.
- Final publication-matched figures and tables (regenerated from pipeline outputs) are visually and numerically identical to those in the paper, confirmed by side-by-side comparison or automated diff tool on figure properties and table values.

## Limitations

- The pipeline is specific to IMC and SIMS imaging modalities; adaptation is required for other spatial proteomics or metabolomics platforms (e.g., MALDI, imaging mass cytometry variants).
- Single-cell segmentation quality depends on image resolution and tissue morphology; segmentation may fail or produce artifacts in samples with poor morphology or high auto-fluorescence.
- VAE embedding hyperparameters (latent dimension, learning rate, regularization) are fixed in the notebooks; systematic parameter optimization and validation on held-out test regions are not documented in the pipeline.
- The pipeline assumes co-registration of IMC and SIMS images is achievable with the documented affine transformation approach; highly distorted or non-aligned images may require manual intervention or custom registration algorithms.

## Evidence

- [readme] ScSpaMet repository organization and notebooks: ""notebooks" folder contains jupyter notebook script used: 01 Processing of IMC (protein) and SIMS (metabolite) images; 02 Registration of IMC and SIMS images; 03 Single-cell level segmentation; 04"
- [intro] Raw data location and format: "You can find the raw data here: https://doi.org/10.5281/zenodo.6784251"
- [other] Pipeline execution workflow: "Execute the pipeline analysis scripts in the order documented in the repository README, processing raw metabolomics and protein data through preprocessing, cell-type assignment, and spatial"
- [other] Verification and comparison with reference: "Compare the regenerated output against the reference result reported in the paper to confirm reproducibility"
- [readme] Custom source code and spatial functions: ""src" folder contains customs scripts used: affine transformation; "utils.py" contains plotting and io custom functions; "spatial" folder contains custom code for spatial interaction functions"
