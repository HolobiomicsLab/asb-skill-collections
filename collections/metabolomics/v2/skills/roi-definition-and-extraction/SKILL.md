---
name: roi-definition-and-extraction
description: Use when when you have loaded imzML MSI data into napari and need to focus analysis on a specific anatomical or morphological region rather than the entire image.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - napari
  - Python
  - MSI-Explorer
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
---

# roi-definition-and-extraction

## Summary

Define and extract mass spectra from annotated regions of interest (ROI) in mass spectrometry imaging data using interactive drawing tools. This skill enables targeted biochemical analysis by isolating spectra within user-defined spatial boundaries and calculating aggregate intensity profiles for database annotation.

## When to use

When you have loaded imzML MSI data into napari and need to focus analysis on a specific anatomical or morphological region rather than the entire image. Use this skill when you want to calculate mean or summed intensity profiles from a spatially localized subset of spectra for targeted annotation against reference databases.

## When NOT to use

- The input data is already aggregated into a feature table or has lost spatial information; ROI extraction requires intact 2D/3D spatial coordinates.
- You need to analyze the entire MSI dataset uniformly without spatial stratification; use global mean spectrum calculation instead.
- MSI data is in profile mode and you have not resolved the profile/centroid conversion dialog that appears upon upload.

## Inputs

- imzML file (mass spectrometry imaging data in imzML format)
- MSI image visualization in napari with loaded spectral data
- Optionally: preprocessed data (noise-reduced, normalized, hotspot-removed)

## Outputs

- Annotated ROI layer in napari (binary mask or labeled image)
- ROI mean or summed intensity spectrum (m/z vs. intensity profile)
- CSV export of ROI spectrum data (m/z values and corresponding intensities)

## How to apply

Load preprocessed or raw imzML data into napari via the MSI-Explorer plugin. Use napari's interactive drawing or selection tools to define a region-of-interest (ROI) boundary on the MSI image, adjusting brush size and label color as needed. Fill the drawn area using the paint icon to mark all pixels belonging to the ROI. Extract all mass spectra contained within the annotated ROI boundary by clicking 'Calculate ROI mean spectrum', which computes either the mean or summed intensity profile for all spectra in that region. Export the resulting ROI spectrum(s) as CSV for downstream database matching. Before selecting a second ROI, remove the first annotation using the eraser tool or by setting the label to 0 to avoid overlap.

## Related tools

- **napari** (Interactive image viewer and annotation platform for drawing ROI boundaries and visualizing MSI data with labeled layers) — https://github.com/napari/napari
- **MSI-Explorer** (napari plugin that wraps ROI selection, mean spectrum calculation, and database annotation workflows for MSI data) — https://github.com/MMV-Lab/MSI-Explorer
- **Python** (Runtime environment for MSI-Explorer and underlying spectral processing logic)

## Examples

```
# In napari with MSI-Explorer plugin loaded:
# 1. Navigate to Plugins → MSI-Explorer
# 2. Click 'Load imzML' and select your .imzML file
# 3. Click 'Select ROI for mean spectrum', adjust brush size
# 4. Paint over the region of interest on the image
# 5. Click 'Calculate ROI mean spectrum'
# 6. Click 'Export spectrum data' to save as CSV
```

## Evaluation signals

- ROI annotation layer is visually overlaid on the MSI image in napari with correct spatial boundaries and non-zero pixel count.
- Exported ROI spectrum CSV contains expected columns (m/z and intensity) with no missing or NaN values within the ROI.
- ROI mean spectrum intensity values are within the expected range (lower than or equal to global mean spectrum for the same m/z range).
- ROI can be successfully exported and reimported; brush size and label color settings are retained across sessions.
- When multiple ROIs are defined sequentially, erasing the previous ROI (via label 0 or eraser) produces a clean new ROI with no pixel overlap.

## Limitations

- Profile-mode MSI data requires explicit centroid conversion via dialog prompt before ROI extraction; profile spectra may yield different mean intensities than centroid-converted data.
- ROI definition is manual and subjective; drawn boundary precision depends on brush size, user dexterity, and visual quality of the underlying MSI image.
- ROI extraction does not automatically perform noise reduction or normalization; preprocessing must be applied before ROI definition if those steps are required for downstream matching.
- Multiple sequential ROI annotations require manual removal (eraser or label 0) between selections; no batch ROI mode is documented.

## Evidence

- [other] Define and annotate a region-of-interest (ROI) using napari's interactive drawing or selection tools.: "Define and annotate a region-of-interest (ROI) using napari's interactive drawing or selection tools."
- [other] Extract all mass spectra contained within the annotated ROI boundary.: "Extract all mass spectra contained within the annotated ROI boundary."
- [other] Calculate mean or summed intensity profile for the ROI spectra.: "Calculate mean or summed intensity profile for the ROI spectra."
- [readme] To select the ROI, click on `Select ROI for mean spectrum`. Adjust the brush size and label color. You can fill the area by using paint icon.: "To select the ROI, click on `Select ROI for mean spectrum`. Adjust the brush size and label color. You can fill the area by using paint icon."
- [readme] Then click on the `Calculate ROI mean spectrum`. You can export as `.csv` file by using `Export spectrum data`.: "Then click on the `Calculate ROI mean spectrum`. You can export as `.csv` file by using `Export spectrum data`."
- [readme] Before selecting the second ROI, remove the first selected area by using eraser or label 0.: "Before selecting the second ROI, remove the first selected area by using eraser or label 0."
- [readme] Upon uploading profile mode data, a pop-up appears prompting you to convert it to centroid mode. Selecting `Yes` converts the data, while `No` keeps it in its original profile format.: "Upon uploading profile mode data, a pop-up appears prompting you to convert it to centroid mode. Selecting `Yes` converts the data, while `No` keeps it in its original profile format."
