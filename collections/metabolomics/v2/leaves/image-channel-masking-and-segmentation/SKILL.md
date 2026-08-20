---
name: image-channel-masking-and-segmentation
description: Use when when you have multi-channel LA-ICP-MS images and need to isolate
  specific elemental regions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3382
  - http://edamontology.org/topic_0091
  tools:
  - Calculator
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
- The built in `Calculator` can perform simple calculations on image data by entering
  the desired formula into the `Formula` text box
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

# Image Channel Masking and Segmentation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply pixel-level masking and segmentation operations to LA-ICP-MS elemental image arrays to isolate regions of interest and create binary or labeled masks. This skill enables selective extraction of chemical data by threshold, user-defined masks, k-means clustering, or Otsu's method, producing new derived images for downstream colocalization and quantitative analysis.

## When to use

When you have multi-channel LA-ICP-MS images and need to isolate specific elemental regions (e.g., pixels above a threshold, clustered by k-means, or segmented by Otsu's method) to exclude background, select foreground, or partition spatial domains for independent analysis of colocalization or abundance.

## When NOT to use

- Input image has already been binarized or manually segmented by non-automated means and you need only to apply it; use the direct mask operation instead of re-segmenting.
- Your goal is to measure colocalization across the entire image without spatial isolation; masking will discard data and may bias summary statistics.
- The elemental signal is uniformly distributed or lacks clear spatial structure; automatic thresholding or clustering will not resolve meaningful regions.

## Inputs

- Multi-channel LA-ICP-MS image array (registered in pewpew open images)
- Threshold value (numeric scalar for threshold or Otsu operations)
- K parameter (integer count of clusters for k-means)
- Pre-computed mask image (for mask operation)

## Outputs

- Binary or categorical mask image (NaN for excluded pixels, numeric for included or clustered)
- Registered masked image in pewpew open images (ready for further filtering, export, or colocalization calculation)

## How to apply

Load the registered elemental image array into the Calculator or direct masking/segmentation module. Choose the appropriate filter step based on your segmentation goal: use `threshold |image, value` to create a binary mask by setting all pixels below a cutoff to NaN; use `mask |image, mask_image` to select pixels passing a pre-computed mask; use `segment |image, threshold` to generate thresholds-based segmentation; use `kmeans |image, k` to partition pixels into k clusters by spectral similarity; or use `otsu |image` to automatically compute an optimal intensity threshold. Evaluate the resulting mask or labeled array visually and quantitatively (e.g., region size, mean intensity within masked regions) to confirm that foreground/background separation or clustering is appropriate for your colocalization hypothesis.

## Related tools

- **pewpew** (GUI for importing and interactive filtering of LA-ICP-MS images; hosts masking, segmentation, and threshold operations in the Calculator and direct filter UI.) — https://github.com/djdt/pewpew
- **pewlib** (Underlying Python library that implements image array I/O, arithmetic evaluation, and filter step execution (threshold, mask, segment, kmeans, otsu).) — https://github.com/djdt/pewlib

## Evaluation signals

- Resulting mask image contains only NaN and numeric values (no negative or unintended values); spatial structure matches visual inspection of the input image.
- For threshold or Otsu: histogram or region-size statistics show bimodal separation; foreground region size is consistent with domain knowledge (e.g., cell or tissue area).
- For k-means: cluster labels are stable across repeated runs (deterministic seed or convergence check); cluster centroids are well-separated in intensity/elemental space.
- For segment: resulting mask can be overlaid on the original image with expected foreground–background spatial alignment.
- Pixels set to NaN in the mask are reproducibly excluded from downstream colocalization or intensity calculations; unmasked regions retain original intensity values.

## Limitations

- Threshold and Otsu methods assume unimodal or bimodal intensity distributions; multimodal or skewed elemental distributions may produce spurious thresholds.
- K-means clustering requires pre-specification of k; no automatic k-selection is provided in the described workflow; results are sensitive to initialization.
- Segmentation and masking operations are applied independently to each image; no multi-image statistical thresholding or cross-channel spatial coherence constraints are mentioned.
- NaN pixels introduced by masking propagate through subsequent arithmetic and filtering operations; users must be aware that masked pixels will remain NaN in derived images unless explicitly handled.

## Evidence

- [methods] mask |image, mask |selects from image using `mask`: "mask |image, mask |selects from image using `mask`"
- [methods] segment |image, threshold |creates a mask image of `thesholds`: "segment |image, threshold |creates a mask image of `thesholds`"
- [methods] kmeans |image, k |array of lower k-means bounds: "kmeans |image, k |array of lower k-means bounds"
- [methods] otsu |image |Otsu's method of image: "otsu |image |Otsu's method of image"
- [methods] threshold |image, value |sets all pxiels below `value` to nan: "threshold |image, value |sets all pxiels below `value` to nan"
- [other] Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel.: "Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel."
- [other] Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays, supporting conditional logic and arithmetic operations on elemental data.: "Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays, supporting conditional logic and arithmetic operations on elemental"
- [intro] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data"
- [readme] Pewlib is a library for importing, processing and exporting LA-ICP-MS data.: "Pewlib is a library for importing, processing and exporting LA-ICP-MS data."
