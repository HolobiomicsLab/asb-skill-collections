---
name: binary-mask-generation-from-thresholding
description: Use when you have imported a laser ablation ICP-MS image into pew² and
  need to distinguish tissue-bearing pixels from background noise or non-ablated regions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pewpew
  - pewlib
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

# binary-mask-generation-from-thresholding

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate a binary mask image from LA-ICP-MS ablation data by applying threshold-based segmentation methods (e.g., Otsu's method) to separate tissue pixels from background. This is a foundational preprocessing step in pew² for isolating regions of interest before quantitative analysis.

## When to use

You have imported a laser ablation ICP-MS image into pew² and need to distinguish tissue-bearing pixels from background noise or non-ablated regions. Use this skill when preparing data for region-based quantification, when you want to restrict subsequent filter operations to tissue only, or when the Selection Dialog threshold controls are appropriate for your segmentation criterion (e.g., intensity > threshold).

## When NOT to use

- Data format is not supported by pew² (only Agilent, Thermo, PerkinElmer, Nu Instruments, CSV, or imzML formats are directly importable)
- The segmentation criterion is not well-defined by intensity alone (e.g., if tissue and background have highly overlapping intensity distributions)
- You require supervised or machine-learning-based segmentation rather than threshold-based methods

## Inputs

- LA-ICP-MS image (line-by-line, spot-wise, or ablation-time-aligned data loaded in pew²)
- Intensity values across all pixels in the image
- Optional: pre-existing selection or region to restrict thresholding

## Outputs

- Binary mask image (NaN for background, valid values for tissue pixels)
- Selection overlay indicating tissue regions

## How to apply

Open the Selection Dialog via right-click context menu on your loaded LA-ICP-MS image. Choose a thresholding method from the Method combo-box (e.g., Otsu's method for automatic determination) and set a Comparison operator (e.g., '>' for pixels above threshold). The 'otsu' filter applies Otsu's method to the image, while the 'segment' filter creates a binary mask from the thresholds, and the 'mask' filter then selects regions from the image using that binary output. Optionally limit thresholding to a pre-existing selection to refine segmentation. Visualize the resulting selection overlay on the image to confirm that tissue pixels are correctly separated from background before proceeding to downstream analysis.

## Related tools

- **pewpew** (GUI application that hosts the Selection Dialog and provides the threshold/segment/mask filter operations for binary mask generation from LA-ICP-MS images) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pew² that implements the segment, otsu, and mask filter operations for programmatic binary mask generation) — https://github.com/djdt/pewlib

## Evaluation signals

- The resulting binary mask contains NaN values for background pixels and numeric values for tissue pixels (no mixed or invalid states)
- Visual overlay of the selection on the original image confirms that all expected tissue regions are included and background is excluded
- Downstream quantitative measurements (e.g., mean element intensity within mask) are plausible and consistent with the ablated material composition
- Mask pixel count and morphology match the expected size and shape of ablated tissue from the experimental design
- If Otsu's method is used, the automatically determined threshold value should reflect a clear separation in the image histogram between two populations

## Limitations

- Threshold-based segmentation requires clear intensity separation between tissue and background; fails when populations overlap significantly
- Otsu's method assumes a bimodal histogram; may produce suboptimal thresholds for multi-modal or heavily skewed intensity distributions
- No built-in morphological cleanup (erosion, dilation, filling); artifact pixels or edge effects may persist in the mask
- Manual threshold selection is subjective and may vary between operators; Otsu's method provides reproducibility but may not match domain-specific criteria

## Evidence

- [other] The Selection Dialog threshold-based tissue segmentation using Otsu's method: "the 'segment' filter creates a mask image from thresholds, the 'otsu' filter applies Otsu's method to an image, and the 'mask' filter selects regions from an image using a binary mask"
- [other] Workflow for opening Selection Dialog and applying threshold: "Open the Selection Dialog via right-click context menu on the image. Select a thresholding method (e.g., Otsu's method) from the Method combo-box and set the Comparison operator (e.g., '>') to define"
- [other] Visualization step for quality control: "Visualize the resulting selection overlay on the image to confirm segmentation quality"
- [readme] pew² purpose and supported data: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data"
- [methods] Filter operations for mask generation: "segment |image, threshold |creates a mask image of `thesholds` ... mask |image, mask |selects from image using `mask`"
