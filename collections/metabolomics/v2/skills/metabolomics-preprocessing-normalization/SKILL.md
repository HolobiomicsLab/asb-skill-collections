---
name: metabolomics-preprocessing-normalization
description: Use when you have acquired raw SIMS (secondary ion mass spectrometry)
  metabolite images aligned with tissue regions and segmented single-cell masks, and
  you need to extract normalized metabolite intensity values per cell before performing
  cell-type assignment, VAE embedding, or protein–metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3934
  tools:
  - ScSpaMet custom spatial extraction functions
  - Mesmer segmentation pipeline
  - Jupyter Notebook 01 (Processing of IMC and SIMS images)
  - Jupyter Notebook 02 (Registration of IMC and SIMS images)
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-43917-5
  title: scSpaMet
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-preprocessing-normalization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Preprocessing and normalization of single-cell spatial metabolomics data from imaging mass spectrometry (SIMS), including intensity extraction, quality control, and modal harmonization before downstream clustering and correlation analysis. This skill is essential for converting raw SIMS image stacks into normalized single-cell metabolite intensity matrices suitable for joint proteomics integration.

## When to use

You have acquired raw SIMS (secondary ion mass spectrometry) metabolite images aligned with tissue regions and segmented single-cell masks, and you need to extract normalized metabolite intensity values per cell before performing cell-type assignment, VAE embedding, or protein–metabolite correlation analysis. Apply this skill when raw pixel-level metabolite signals must be aggregated to single-cell resolution and harmonized across imaging regions and modalities.

## When NOT to use

- Input metabolite data are already aggregated to cell-level and normalized (e.g., already a feature table); skip preprocessing and proceed to clustering or correlation.
- Segmentation masks are unavailable or unreliable; defer preprocessing until high-quality masks are obtained or use alternative segmentation methods.
- Analysis goal is limited to bulk tissue metabolomics or regional comparison without single-cell resolution; consider alternative preprocessing workflows that do not require single-cell segmentation.

## Inputs

- Raw SIMS image stacks (one NetCDF or HDF5 file per metabolite m/z)
- Single-cell segmentation masks (labeled image, output from Mesmer or equivalent)
- Image metadata (imaging region coordinates, instrument parameters)

## Outputs

- Normalized single-cell metabolite intensity matrix (cells × metabolites)
- Quality control metrics per cell (e.g., total ion count, signal-to-noise)
- Registration coordinates linking SIMS to IMC protein data

## How to apply

Begin with raw SIMS image stacks (one per metabolite ion m/z) and single-cell segmentation masks generated from Mesmer or equivalent segmentation pipeline (Notebook 11). Use custom spatial extraction functions (src/spatial folder) to aggregate pixel intensities within each cell mask, producing a cell × metabolite intensity matrix. Apply intensity normalization to account for ionization efficiency and imaging depth variations across cells and regions; the ScSpaMet pipeline performs this normalization prior to VAE embedding (Notebook 05). Validate that normalized intensities are positive, dimensionally consistent (cell count matches segmentation mask count), and fall within expected dynamic range. Register metabolite data to corresponding IMC protein images (Notebook 02) to ensure spatial correspondence before joint embedding.

## Related tools

- **ScSpaMet custom spatial extraction functions** (Aggregates pixel-level SIMS intensities within single-cell masks and performs normalization; stored in src/spatial folder) — github.com/coskunlab/ScSpaMet
- **Mesmer segmentation pipeline** (Generates single-cell segmentation masks from IMC protein images used to define cell boundaries for metabolite intensity extraction)
- **Jupyter Notebook 01 (Processing of IMC and SIMS images)** (Implements preprocessing and normalization of raw SIMS and IMC images) — github.com/coskunlab/ScSpaMet
- **Jupyter Notebook 02 (Registration of IMC and SIMS images)** (Registers normalized metabolite data to protein images for spatial correspondence) — github.com/coskunlab/ScSpaMet

## Evaluation signals

- Normalized metabolite intensity matrix has dimensions matching cell count (rows) × detected m/z values (columns), with no NaN or Inf values.
- Intensity values are non-negative and fall within expected dynamic range (e.g., 0–10⁶ counts depending on instrument); median intensity is > 0.
- Quality control metrics (total ion count per cell, signal-to-noise ratio) show no systematic bias across regions or imaging time points.
- Regenerated intensities can be successfully embedded in VAE model (Notebook 05) without convergence errors or dimensional mismatches.
- Normalized metabolite patterns visually match published figures from the paper (e.g., spatial heatmaps in Notebooks 06, 10) when compared side-by-side.

## Limitations

- Preprocessing outcome depends critically on segmentation mask quality; errors or over-/under-segmentation in Mesmer output will propagate through to cell-level metabolite intensity estimates.
- Normalization approach assumes uniform ionization efficiency across cells and regions; significant variations due to tissue heterogeneity (e.g., fibrosis, necrosis) may require region-specific normalization strategies not explicitly documented in the repository.
- Single-cell intensity extraction requires registered SIMS and IMC images; misalignment (Notebook 02) will result in incorrect protein–metabolite associations and compromised downstream analysis.
- Raw SIMS data file formats (NetCDF, HDF5, proprietary vendor formats) and intensity scale (counts vs. normalized units) may vary by instrument; pipeline assumes specific format conventions documented in repository README.

## Evidence

- [readme] 01 Processing of IMC (protein) and SIMS (metabolite) images: "01 Processing of IMC (protein) and SIMS (metabolite) images"
- [readme] 03 Single-cell level segmentation and visualization of segmentation masks; 04 Single-cell level intensity extraction and single-cell proteomics clustering: "03 Single-cell level segmentation and visualization of segmentation masks
- 04 Single-cell level intensity extraction and single-cell proteomics clustering"
- [readme] 05 VAE joint embedding of protein and metabolite modalities: "05 VAE joint embedding of protein and metabolite modalities"
- [readme] "src" folder contains customs scripts used: affine transformation; "utils.py" contains plotting and io custom functions; "spatial" folder contains custom code for spatial interaction functions: ""src" folder contains customs scripts used: affine transformation; "utils.py" contains plotting and io custom functions; "spatial" folder contains custom code for spatial interaction functions"
- [readme] 11 Segmentation of single-cell with Mesmer pipeline; 02 Registration of IMC and SIMS images for different imaging regions: "11 Segmentation of single-cell with Mesmer pipeline
- 02 Registration of IMC and SIMS images for different imaging regions"
