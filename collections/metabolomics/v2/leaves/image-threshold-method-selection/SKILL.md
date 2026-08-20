---
name: image-threshold-method-selection
description: Use when you have loaded a laser ablation ICP-MS image into pewpew and
  need to separate tissue pixels from background regions to enable region-based analysis
  or quantification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - pewpew
  - pewlib
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c02138
  title: Pew2
- doi: 10.1529/biophysj.103.038422
  title: ''
evidence_spans:
- The built in `Filtering Tool` removes spikes by comparing pixel values to a locally
  defined threshold
- '|pewpew| is an open-source LA-ICP-MS data import and processing application'
- based on the python library pewlib_
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pew2_cq
    doi: 10.1021/acs.analchem.1c02138
    title: Pew2
  dedup_kept_from: coll_pew2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02138
  all_source_dois:
  - 10.1021/acs.analchem.1c02138
  - 10.1529/biophysj.103.038422
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# image-threshold-method-selection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Select and apply an appropriate thresholding method (e.g., Otsu's method) to segment tissue from background in laser ablation ICP-MS images. This skill involves choosing a comparison operator and optional restriction to pre-existing selections to generate binary masks that separate regions of interest.

## When to use

You have loaded a laser ablation ICP-MS image into pewpew and need to separate tissue pixels from background regions to enable region-based analysis or quantification. Use this skill when the Selection Dialog is available and you need to apply threshold-based segmentation rather than manual selection.

## When NOT to use

- The image already contains a manually curated or previously validated selection that does not require re-segmentation.
- Input data is not a 2D LA-ICP-MS image (e.g., if it is a 1D line scan or raw time-series data before image construction).
- Tissue-background contrast is too low or ambiguous for any threshold-based method to produce meaningful separation.

## Inputs

- LA-ICP-MS image (line-by-line, spot-wise, or ablation-time-aligned formats from Agilent, Thermo, PerkinElmer, or delimited text)
- optional: pre-existing selection region

## Outputs

- binary mask image separating tissue from background
- selection overlay visualization

## How to apply

Open the Selection Dialog via right-click context menu on the loaded image. Select a thresholding method from the Method combo-box (Otsu's method is recommended for automatic threshold determination without user-specified values). Set the Comparison operator (e.g., '>' to select pixels above the threshold, '<' for below) to define the segmentation criterion. Optionally check 'Limit thresholding to selected value' to restrict the operation to a pre-existing selection rather than the entire image. Apply the threshold to generate a binary mask. Visualize the resulting selection overlay on the image to confirm segmentation quality before proceeding with downstream analysis.

## Related tools

- **pewpew** (GUI application for importing, visualizing, and interactively segmenting LA-ICP-MS images via the Selection Dialog) — https://github.com/djdt/pewpew
- **pewlib** (Python library providing the filter operations (segment, otsu, mask) that implement threshold-based segmentation) — https://github.com/djdt/pewlib

## Evaluation signals

- The binary mask correctly isolates tissue pixels and excludes background regions, verifiable by visual inspection of the selection overlay.
- The threshold value selected by the method (or user-specified) is appropriate for the image's dynamic range and does not over- or under-segment.
- Pixels classified as tissue in the mask have higher intensity values than background pixels when the comparison operator is correctly applied.
- If 'Limit thresholding to selected value' was checked, the mask respects the pre-existing selection boundary and does not extend beyond it.
- Downstream quantification results (e.g., elemental concentrations in tissue regions) are consistent with expected ranges and do not show artifacts from segmentation errors.

## Limitations

- Otsu's method and other automatic thresholding approaches assume a bimodal (or simple multimodal) intensity distribution; they may fail on images with complex or overlapping tissue/background intensity ranges.
- The Selection Dialog thresholding is applied to a single image; if multiple images require consistent segmentation criteria, the user must manually apply the same parameters to each image or use batch processing.
- No changelog is available for pewlib or pewpew, limiting ability to track changes in filter behavior or thresholding algorithm updates.
- Thresholding alone does not account for spatial structure or connectivity; isolated noise pixels meeting the threshold criterion will also be included in the mask.

## Evidence

- [other] The pew² application implements segmentation through filter operations including Otsu's method and threshold-based masking: "the 'segment' filter creates a mask image from thresholds, the 'otsu' filter applies Otsu's method to an image, and the 'mask' filter selects regions from an image using a binary mask."
- [other] Workflow for applying threshold-based segmentation in pewpew: "Open the Selection Dialog via right-click context menu on the image. Select a thresholding method (e.g., Otsu's method) from the Method combo-box and set the Comparison operator (e.g., '>') to define"
- [other] Optional restriction of thresholding operation: "Optionally check 'Limit thresholding to selected value' to restrict the thresholding operation to a pre-existing selection."
- [other] Segmentation output and verification: "Apply the threshold to generate a binary mask separating tissue pixels from background. Visualize the resulting selection overlay on the image to confirm segmentation quality."
- [readme] Pew² core functionality for LA-ICP-MS data: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library [pewlib]"
