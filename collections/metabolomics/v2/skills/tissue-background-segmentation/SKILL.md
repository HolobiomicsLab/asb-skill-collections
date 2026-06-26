---
name: tissue-background-segmentation
description: Use when you have loaded a laser ablation ICP-MS image into pew² and
  need to distinguish tissue signal from instrument background or non-ablated substrate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3379
  - http://edamontology.org/topic_3382
  tools:
  - pewpew
  - pewlib
  - pew²
  license_tier: restricted
  provenance_tier: literature
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

# Threshold-Based Tissue–Background Segmentation in LA-ICP-MS Images

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Separates tissue pixels from background in laser ablation ICP-MS images using threshold-based methods (e.g., Otsu's method) applied through pew²'s Selection Dialog. This is essential for isolating regions of analytical interest before quantification or spatial analysis.

## When to use

You have loaded a laser ablation ICP-MS image into pew² and need to distinguish tissue signal from instrument background or non-ablated substrate. Use this skill when the tissue and background occupy distinct intensity ranges and you want to create a binary mask that restricts downstream filtering, calibration, or export to tissue-only regions.

## When NOT to use

- Input image already has a pre-existing, validated tissue mask — use the mask filter directly instead.
- Tissue and background have highly overlapping intensity distributions with no clear threshold — consider k-means clustering or manual region-of-interest selection.
- You need to preserve intensity values within the tissue region — use mask filter after segmentation, not segment alone.

## Inputs

- LA-ICP-MS image (line-by-line, spot-wise, or ablation-time-aligned format supported by pew²)
- Intensity data array (single element or mass channel)

## Outputs

- Binary mask image (pixels marked as tissue or background/NaN)
- Selection overlay (visual confirmation on original image)

## How to apply

Open the Selection Dialog via right-click context menu on the loaded LA-ICP-MS image in pew². Choose a thresholding method from the Method combo-box: Otsu's method (otsu filter) automatically computes an optimal threshold to minimize within-class variance, or manually set a threshold value. Set the Comparison operator (e.g., '>' to select pixels above the threshold, or '<' below) to define your segmentation criterion. Optionally restrict thresholding to an existing selection by checking 'Limit thresholding to selected value'. Apply the threshold to generate a binary mask. Verify segmentation quality by visualizing the resulting selection overlay on the image; adjust threshold parameters or operator if tissue/background separation is incomplete or includes spurious regions.

## Related tools

- **pew²** (GUI for importing, visualizing, and applying threshold-based segmentation to LA-ICP-MS images via the Selection Dialog) — https://github.com/djdt/pewpew
- **pewlib** (Python library providing segment, otsu, and mask filter operations underlying pew²'s segmentation workflow) — https://github.com/djdt/pewlib

## Evaluation signals

- Binary mask contains only 0/1 or tissue/NaN values with no intermediate intensities.
- Tissue pixels correspond to visually identifiable anatomical features in the original image overlay.
- Selection boundary does not include spurious noise clusters or exclude continuous tissue regions.
- Threshold value falls within the observed intensity range; operator direction (>, <, >=, <=) is consistent with tissue/background separation goal.
- Mask can be successfully applied downstream (via 'mask' filter) to isolate tissue-only data for calibration or export without artifact propagation.

## Limitations

- Otsu's method assumes a bimodal intensity distribution; unimodal or multimodal data may produce suboptimal thresholds.
- Fixed threshold does not adapt to spatial heterogeneity in ablation efficiency or matrix effects across the sample.
- Thresholding is blind to morphological context; small isolated pixels or thin filaments may be misclassified.
- No built-in edge-refinement or morphological post-processing (e.g., erosion/dilation) to smooth mask boundaries.
- Relies on manual threshold tuning if automatic methods (Otsu) do not yield acceptable results.

## Evidence

- [other] The pew² application implements segmentation through filter operations including Otsu's method and threshold-based masking: the 'segment' filter creates a mask image from thresholds, the 'otsu' filter applies Otsu's method to an image, and the 'mask' filter selects regions from an image using a binary mask.: "the 'segment' filter creates a mask image from thresholds, the 'otsu' filter applies Otsu's method to an image, and the 'mask' filter selects regions from an image using a binary mask"
- [other] Open the Selection Dialog via right-click context menu on the image. Select a thresholding method (e.g., Otsu's method) from the Method combo-box and set the Comparison operator (e.g., '>') to define the segmentation criterion.: "Open the Selection Dialog via right-click context menu on the image. Select a thresholding method (e.g., Otsu's method) from the Method combo-box and set the Comparison operator"
- [other] Optionally check 'Limit thresholding to selected value' to restrict the thresholding operation to a pre-existing selection. Apply the threshold to generate a binary mask separating tissue pixels from background.: "Apply the threshold to generate a binary mask separating tissue pixels from background"
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data: "GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data"
- [methods] segment |image, threshold |creates a mask image of `thesholds`: "segment |image, threshold |creates a mask image of `thesholds`"
