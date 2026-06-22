---
name: msi-data-visualization-and-spatial-analysis
description: Use when when you have imzML-format MSI data and need to identify biochemical species in specific tissue regions or anatomical structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0121
  tools:
  - napari
  - Python
  - MSI-Explorer
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.5c01513
  title: MSI-Explorer
evidence_spans:
- The MSI-Explorer napari plugin is a powerful tool designed for targeted biochemical annotations in MSI data.
- '[![Python Version](https://img.shields.io/pypi/pyversions/MSI-Explorer.svg?color=green)](https://python.org)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msi_explorer_cq
    doi: 10.1021/acs.analchem.5c01513
    title: MSI-Explorer
  dedup_kept_from: coll_msi_explorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01513
  all_source_dois:
  - 10.1021/acs.analchem.5c01513
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msi-data-visualization-and-spatial-analysis

## Summary

Interactive visualization and spatial analysis of mass spectrometry imaging (MSI) data within napari, enabling ROI definition, mean spectrum extraction, and targeted biochemical annotation against reference databases. This skill combines image visualization with spectral feature matching to identify biochemical composition in spatial regions.

## When to use

When you have imzML-format MSI data and need to identify biochemical species in specific tissue regions or anatomical structures. Use this skill when you want to move beyond global spectral profiling to targeted, spatially-resolved analysis—for example, extracting mean spectra from tumor margins, healthy tissue boundaries, or manually-drawn regions of interest to match against metabolite or lipid databases.

## When NOT to use

- Input MSI data is already in processed or feature-table format rather than raw imzML; use this skill on raw acquisition data for full spatial and spectral fidelity.
- Analysis goal is untargeted, global profiling (e.g., discovery of all m/z features across the entire image without spatial hypothesis); ROI-based annotation is unnecessary overhead for unsupervised feature detection.
- Reference database is unavailable or incompatible (wrong format, missing exact mass column); annotation step cannot proceed without proper database structure.

## Inputs

- imzML file (MSI raw data in profile or centroid mode)
- napari image layer (loaded MSI data)
- reference database (built-in or custom: exact mass, molecule name, molecular formula)
- ROI definition (drawn or painted region in napari using interactive tools)

## Outputs

- Mean spectrum (CSV export with m/z and intensity values)
- Annotated match table (m/z values, putative identities, match scores, confidence metrics)
- Visualized MSI image with ROI boundary overlay
- Spectrum plot image (exportable as image file)
- Matched annotations linked to detected m/z features

## How to apply

Load imzML data into napari via the MSI-Explorer plugin; optionally convert profile-mode data to centroid mode when prompted. Define a region of interest (ROI) using napari's interactive drawing or paint tools, adjusting brush size and label color as needed. Execute pre-processing if desired (noise reduction as a percentage, normalization methods: TIC, RMS, median, or reference peak; hotspot removal at 99.99% quantile). Calculate the mean or summed intensity profile for all mass spectra within the ROI boundary. Select a reference database (built-in Metabolite_database_ver2, LIPID MAPS, HMDB, or custom library with exact mass, molecule name, and molecular formula columns) and configure charge and adduct settings. Match the extracted ROI spectrum(s) against the database using m/z tolerance and spectral similarity scoring. Export results as CSV (spectrum data and matched annotations with m/z values, putative identities, and match scores) and visualize ROI boundaries overlaid on the original MSI image with matched annotations linked to detected m/z features.

## Related tools

- **napari** (Interactive image viewer and ROI drawing/selection platform; provides the UI layer for defining spatial regions and overlaying annotations on MSI images) — https://github.com/napari/napari
- **Python** (Core language for MSI-Explorer; enables spectrum extraction, mean calculation, database matching, and data export workflows) — https://python.org
- **MSI-Explorer** (napari plugin that wraps the complete workflow: data import, visualization, pre-processing (noise, normalization, hotspot removal), ROI analysis, mean spectrum calculation, and database annotation) — https://github.com/MMV-Lab/MSI-Explorer

## Examples

```
# In napari console after MSI-Explorer plugin is loaded:
# 1. Load imzML: Plugins → MSI-Explorer → Load imzML (select file.imzML)
# 2. Define ROI: Select ROI for mean spectrum → paint region → Calculate ROI mean spectrum
# 3. Annotate: Select database (Metabolite_database_ver2) → set charge/adduct → search
# 4. Export: Export spectrum data → save_roi_spectrum.csv
```

## Evaluation signals

- ROI boundary is correctly visualized and overlaid on the original MSI image with the selected label color and brush dimensions.
- Mean spectrum calculated from ROI contains expected m/z range and intensity profile consistent with the tissue type or region (e.g., lipid-rich region shows characteristic lipid m/z peaks).
- Matched annotations table contains entries only when database m/z values fall within the specified m/z tolerance of detected ROI peaks, and match scores and confidence metrics are populated for each hit.
- Exported CSV files are valid, contain expected column headers (m/z, intensity for spectrum; m/z, putative identity, match score, confidence for annotations), and row counts reflect the spectral points and database hits.
- Pre-processing parameters (noise reduction %, normalization method, hotspot removal threshold) are applied consistently across all spectra in the ROI before mean calculation, verified by comparing raw and processed spectrum plots.

## Limitations

- Profile-mode MSI data must be converted to centroid mode (via user prompt) for reliable m/z matching; centroiding is lossy and may miss low-abundance features or poorly-resolved peaks.
- ROI annotations are manually drawn; operator skill, brush size, and label accuracy directly affect the quality of spatial analysis—no automated region detection is integrated.
- Database matching relies on m/z tolerance and spectral similarity scoring thresholds; ambiguous or mass-shifted peaks (e.g., salt adducts, contaminants) may produce false positive matches if thresholds are not tuned carefully.
- No changelog available in the repository; versioning, bug fixes, and API stability are not explicitly tracked.
- Mean spectrum aggregation loses spatial heterogeneity within the ROI; co-localization of multiple species or fine-scale compositional gradients within the drawn region are not resolved.

## Evidence

- [readme] The MSI-Explorer napari plugin is a powerful tool designed for targeted biochemical annotations in MSI data.: "The MSI-Explorer napari plugin is a powerful tool designed for targeted biochemical annotations in MSI data."
- [readme] It covers data import, visualization, mean intensity calculation, region of interest (ROI) analysis, annotation with selected databases and pre-processing such as noise reduction and normalization.: "It covers data import, visualization, mean intensity calculation, region of interest (ROI) analysis, annotation with selected databases and pre-processing such as noise reduction and normalization."
- [other] 1. Load MSI data into napari via MSI-Explorer plugin. 2. Define and annotate a region-of-interest (ROI) using napari's interactive drawing or selection tools. 3. Extract all mass spectra contained within the annotated ROI boundary. 4. Calculate mean or summed intensity profile for the ROI spectra.: "1. Load MSI data into napari via MSI-Explorer plugin. 2. Define and annotate a region-of-interest (ROI) using napari's interactive drawing or selection tools. 3. Extract all mass spectra contained"
- [other] 5. Match extracted ROI spectrum(s) against a selected reference database (e.g., LIPID MAPS, HMDB, or custom library) using mass-to-charge ratio tolerance and spectral similarity scoring.: "5. Match extracted ROI spectrum(s) against a selected reference database (e.g., LIPID MAPS, HMDB, or custom library) using mass-to-charge ratio tolerance and spectral similarity scoring."
- [readme] To select the ROI, click on `Select ROI for mean spectrum`. Adjust the brush size and label color. You can fill the area by using paint icon. Then click on the `Calculate ROI mean spectrum`.: "To select the ROI, click on `Select ROI for mean spectrum`. Adjust the brush size and label color. You can fill the area by using paint icon. Then click on the `Calculate ROI mean spectrum`."
- [readme] Users can choose their desired level of noise reduction (shown as a percentage) for their experiment.: "Users can choose their desired level of noise reduction (shown as a percentage) for their experiment."
- [readme] The normalization methods that the user can apply are Total ion current (TIC), Root mean square (RMS), Medium, Reference peak (or internal standard): "The normalization methods that the user can apply are Total ion current (TIC), Root mean square (RMS), Medium, Reference peak (or internal standard)"
- [readme] Upon uploading profile mode data, a pop-up appears prompting you to convert it to centroid mode. Selecting `Yes` converts the data, while `No` keeps it in its original profile format.: "Upon uploading profile mode data, a pop-up appears prompting you to convert it to centroid mode. Selecting `Yes` converts the data, while `No` keeps it in its original profile format."
