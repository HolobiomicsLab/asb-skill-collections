---
name: cell-type-protein-profiling-integration
description: Use when you have co-registered IMC (protein imaging mass cytometry)
  and SIMS (secondary ion mass spectrometry for metabolites) data from the same tissue
  regions, cell segmentation masks, and need to assign cell types based on protein
  expression patterns, then overlay those assignments onto.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3179
  tools:
  - scSpaMet VAE joint embedding module
  - Mesmer segmentation pipeline
  - scSpaMet spatial interaction functions (custom code)
  - Jupyter notebooks 02–05 (ScSpaMet pipeline)
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

# cell-type-protein-profiling-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate cell-type assignments derived from single-cell proteomics clustering with spatial metabolomics data to enable joint analysis of protein and metabolite modalities at single-cell resolution. This skill bridges high-dimensional protein intensity profiles with co-registered spatial metabolite distributions to support systems-level biological interpretation.

## When to use

Apply this skill when you have co-registered IMC (protein imaging mass cytometry) and SIMS (secondary ion mass spectrometry for metabolites) data from the same tissue regions, cell segmentation masks, and need to assign cell types based on protein expression patterns, then overlay those assignments onto metabolite intensity maps to study protein–metabolite relationships or identify cell-type-specific metabolic signatures.

## When NOT to use

- Input IMC and SIMS images are not spatially co-registered; registration error > acceptable tolerance for your downstream analysis (notebook 02 should be run first).
- Single-cell segmentation masks are unavailable or do not align with both imaging modalities; the pipeline requires valid ROI-to-cell mapping for both protein and metabolite extraction.
- Cell-type assignments are already provided from an independent, non-protein-based method (e.g., flow cytometry gating or external annotation); this skill is designed to derive cell types *from* protein intensity clustering within the same spatial context.

## Inputs

- Registered IMC (protein) images in standardized raster format (e.g., TIFF or HDF5)
- Registered SIMS (metabolite) images in matching spatial coordinate system
- Single-cell segmentation masks (from Mesmer or equivalent segmentation pipeline)
- IMC raw intensity data indexed by cell ID
- Cell-type cluster assignments or protein expression feature matrix

## Outputs

- Cell-type labels mapped to spatial coordinates and segmentation IDs
- Joint protein–metabolite expression table (rows=cells, columns=protein intensity + metabolite intensity features)
- Spatial cell-type annotation map (visualization overlay of cell types on tissue region)
- Metadata table linking cell ID, cell type, spatial location, and modality-specific intensity vectors

## How to apply

First, extract single-cell level protein intensities from the registered IMC images using the segmentation masks (notebook 03–04 in the pipeline). Cluster these intensity profiles using proteomics-driven methods (e.g., k-means or hierarchical clustering) to define cell-type groups. Then map these cell-type labels back to the corresponding spatial coordinates and segmentation IDs. Finally, use the same segmentation masks and coordinate system to extract metabolite intensities per cell, creating a joint protein–metabolite table indexed by cell ID and spatial location. Validate alignment by checking that IMC and SIMS registration (notebook 02) preserves coordinate consistency and that cell IDs in the protein intensity matrix match cell IDs in the metabolite matrix.

## Related tools

- **scSpaMet VAE joint embedding module** (Performs joint dimensionality reduction and integration of protein and metabolite modalities after cell-type profiling; used in notebook 05 to embed protein–metabolite pairs into a shared latent space) — github.com/coskunlab/ScSpaMet
- **Mesmer segmentation pipeline** (Single-cell segmentation engine that generates the segmentation masks required to extract per-cell intensities from both IMC and SIMS images)
- **scSpaMet spatial interaction functions (custom code)** (Computes spatial clustering, distance-based metabolite analysis, and cell–cell interaction metrics conditioned on cell-type assignments) — github.com/coskunlab/ScSpaMet
- **Jupyter notebooks 02–05 (ScSpaMet pipeline)** (Orchestrate registration (notebook 02), segmentation (notebook 03), intensity extraction and proteomics clustering (notebook 04), and VAE integration (notebook 05)) — github.com/coskunlab/ScSpaMet

## Examples

```
# Execute notebook 04 to extract single-cell protein intensities and perform proteomics clustering; then run notebook 05 to integrate with metabolite data:
jupyter nbconvert --to notebook --execute --inplace 04_single_cell_intensity_extraction_clustering.ipynb && jupyter nbconvert --to notebook --execute --inplace 05_VAE_joint_embedding.ipynb
```

## Evaluation signals

- Cell-type cluster centroids in protein space are well-separated (silhouette score > 0.5 or equivalent internal cluster validity metric).
- Spatial cell-type map shows coherent tissue-level organization consistent with known histology or morphology (e.g., cell types cluster in expected anatomical regions).
- Joint protein–metabolite table has no missing values or segmentation artifacts; row count equals number of segmented cells; column count = number of protein features + number of metabolite features.
- Cross-modal validation: metabolite signatures within each cell-type group show lower within-group variance and higher between-group variance than random shuffled assignments.
- Registration check: coordinates of the same cell in both IMC and SIMS modalities align within expected pixel tolerance (typically ≤ 2–5 pixels for high-resolution imaging).

## Limitations

- Cell-type assignments depend entirely on the quality and completeness of the protein intensity matrix; missing or weak protein signals in certain regions will produce uncertain or artifact-driven cell-type calls.
- Segmentation errors (over- or under-segmentation) directly propagate into the joint protein–metabolite table; validation of segmentation quality (e.g., visual inspection, nuclei overlap checks) is essential before downstream analysis.
- The skill assumes linear or near-linear relationships between segmentation mask boundaries and true cell membranes; highly irregular or overlapping cell morphologies may cause intensity assignment errors.
- Protein clustering methods (k-means, hierarchical) require choice of number of clusters; no automated consensus method is described in the repository documentation, creating risk of over- or under-clustering cell-type diversity.

## Evidence

- [readme] Single-cell level segmentation and visualization of segmentation masks: "03 Single-cell level segmentation and visualization of segmentation masks"
- [readme] Single-cell level intensity extraction and proteomics clustering: "04 Single-cell level intensity extraction and single-cell proteomics clustering"
- [readme] VAE joint embedding of protein and metabolite modalities: "05 VAE joint embedding of protein and metabolite modalities"
- [readme] Registration of IMC and SIMS images: "02 Registration of IMC and SIMS images for different imaging regions"
- [readme] Processing of IMC (protein) and SIMS (metabolite) images: "01 Processing of IMC (protein) and SIMS (metabolite) images"
- [intro] Framework for performing single-cell spatial metabolomics with cell-type specific protein profiling: "A framework for performing single-cell spatial metabolomics with cell-type specific protein profiling for tissue systems biology"
