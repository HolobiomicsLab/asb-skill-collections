---
name: costes-threshold-segmentation
description: Use when when you have two or more co-registered LA-ICP-MS element channel
  images and need to compute colocalization coefficients (especially Manders) that
  require reproducible, bias-free segmentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3382
  tools:
  - pewpew
  - pewlib
  - Python
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
- python library [pewlib]
- python library
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

# costes-threshold-segmentation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Applies Costes-based automatic thresholding to segment co-registered LA-ICP-MS element images, enabling reproducible binary masks for colocalization analysis without user bias. This method is essential for computing Manders coefficients and other spatial overlap metrics between channels.

## When to use

When you have two or more co-registered LA-ICP-MS element channel images and need to compute colocalization coefficients (especially Manders) that require reproducible, bias-free segmentation. Costes thresholding is particularly indicated when manual threshold selection would introduce subjective variability or when comparing colocalization across multiple image pairs.

## When NOT to use

- Input images are not co-registered or have misaligned spatial dimensions — alignment must precede thresholding.
- Analysis goal does not require reproducible segmentation (e.g., only qualitative visual inspection needed).
- Images have already been manually thresholded or pre-segmented into binary masks — Costes thresholding is redundant.

## Inputs

- Two co-registered LA-ICP-MS element channel images (same spatial dimensions, aligned)
- Image region or selected region (whole image or subset) to threshold

## Outputs

- Binary segmentation mask(s) for each channel (pixels below Costes threshold set to NaN)
- Manders M1 and M2 coefficients quantifying fractional overlap
- Segmented image suitable for export and further analysis

## How to apply

Load two co-registered element images into the Colocalisation Dialog in pewpew. Apply the Costes thresholding method, which automatically determines an optimal intensity threshold for each channel independently, creating binary masks that maximize separation of signal from background without requiring manual parameter entry. The method produces a segmented image where pixels above the Costes threshold are retained and those below are set to NaN. Compute Manders coefficients using the resulting masks to quantify the fraction of each channel overlapping with the other. The Costes approach is grounded in statistical hypothesis testing and avoids bias inherent in manual thresholding by using an automated, reproducible criterion.

## Related tools

- **pewpew** (GUI for loading co-registered images, applying Costes thresholding, and computing Manders coefficients via the Colocalisation Dialog) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pewpew that implements Costes thresholding and colocalization statistics) — https://github.com/djdt/pewlib

## Evaluation signals

- Binary mask(s) are generated with no NaN values above threshold and all values below threshold set to NaN.
- Manders M1 and M2 coefficients are in the range [0, 1] and are symmetric (M1 ≤ 1, M2 ≤ 1).
- Threshold values are consistent across repeated runs on the same image pair (reproducibility check).
- Visual inspection of segmented image shows reasonable separation of signal regions from background with no obvious over- or under-segmentation.
- Exported coefficients match values reported in the dialog left panel without truncation or rounding errors.

## Limitations

- Costes thresholding assumes both channels have distinguishable signal and background intensity distributions; it may fail or produce uninformative masks on very low-contrast or saturated images.
- Method is sensitive to the quality of image co-registration; misalignment will inflate or deflate colocalization metrics even with correct thresholding.
- Costes thresholding is applied independently to each channel; it does not account for channel-specific noise characteristics or detector sensitivity differences.
- The method requires manually loading and aligning images in the GUI; batch processing across large image sets requires scripting via pewlib Python API (not documented in the article).

## Evidence

- [other] Compute Manders coefficients using the Costes thresholding method on the image or selected region.: "Compute Manders coefficients using the Costes thresholding method on the image or selected region."
- [other] The Colocalisation Dialog computes Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding method) to quantify spatial relationships between two element channels in co-registered images.: "The Colocalisation Dialog computes Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding method) to quantify spatial relationships between two element channels in co-registered images."
- [other] Load two co-registered element images (channels) into the Colocalisation Dialog via image or selection context menu.: "Load two co-registered element images (channels) into the Colocalisation Dialog via image or selection context menu."
- [methods] Align the images manually. Overlay image scale can be set via the `Pixel Size`: "Align the images manually. Overlay image scale can be set via the `Pixel Size`"
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data"
