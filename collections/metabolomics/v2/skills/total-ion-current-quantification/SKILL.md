---
name: total-ion-current-quantification
description: Use when you have loaded a mass spectrometry imaging pixel array (NumPy format) and need to correct for variations in total ion signal across pixels before generating ion images or ratio images.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3564
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - MSIGen
  - Python
  - Jupyter Notebook
  - NumPy
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- MSIGen provides tools for processing mass spectrometry imaging data acquired in line-scan mode into images and figures.
- from MSIGen import msigen
- Using an environment with python version >=3.9 and <=3.11
- If you want to use MSIGen in a Jupyter notebook, you may also need to install jupyter notebook
- MSIGen is most easily used through Jupyter Notebooks or through the GUI.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msigen_cq
    doi: 10.1021/jasms.4c00178
    title: MSIGen
  dedup_kept_from: coll_msigen_cq
schema_version: 0.2.0
---

# Total-Ion-Current Quantification

## Summary

Normalize mass spectrometry imaging pixel intensities to total ion current (TIC) to account for local variation in ion abundance and enable cross-pixel intensity comparisons. This is a preprocessing step in MSI workflows that stabilizes visualization and quantification by removing global intensity artifacts unrelated to spatial distribution.

## When to use

Apply this skill when you have loaded a mass spectrometry imaging pixel array (NumPy format) and need to correct for variations in total ion signal across pixels before generating ion images or ratio images. Use TIC normalization when pixel-to-pixel ion abundance varies due to instrumental drift, sample surface topology, or uneven ionization efficiency, rather than genuine analyte abundance differences. This is especially relevant for nano-DESI MSI data where surface contact and ion yield can vary locally.

## When NOT to use

- Input pixel array is already normalized to an internal standard or has been normalized by another method; applying TIC normalization a second time will distort the intensities.
- The goal is to preserve absolute ion abundance information across the imaging region without correction; TIC normalization will obscure global differences in ionization efficiency.
- Data contains significant spatial structure in total ion signal that is itself scientifically meaningful (e.g., matrix crystallinity or ion suppression effects); TIC normalization will remove that signal.

## Inputs

- Pixel array in NumPy format (2D or 3D: spatial dimensions × m/z bins)
- Associated metadata JSON file with m/z axis information
- Optional: scale parameter (float, 0–1 quantile)

## Outputs

- TIC-normalized pixel array (same shape as input)
- Visualization image(s) with corrected intensity scales
- CSV or figure file(s) saved according to image_savetype

## How to apply

Load the pixel array (NumPy format) and associated metadata JSON using MSIGen's load_pixels function. Set the normalize parameter to 'TIC' when calling get_and_display_images. MSIGen will compute the sum of all ion intensities across the m/z dimension for each pixel, then divide each pixel's intensity values by its corresponding TIC. Optionally apply pixel intensity scaling via the scale parameter (quantile-based; e.g., scale=0.999 sets maximum display intensity to the 99.9th percentile of pixel values) to enhance visualization contrast post-normalization. Save the normalized image output according to the image_savetype parameter (publication-style figures, raw images, or CSV arrays).

## Related tools

- **MSIGen** (Core library for loading pixel arrays, applying TIC normalization via get_and_display_images function, and saving normalized output) — https://github.com/LabLaskin/MSIGen
- **Python** (Runtime environment; MSIGen requires Python >=3.9 and <=3.11)
- **Jupyter Notebook** (Interactive environment for exploratory application of TIC normalization and visualization of results)
- **NumPy** (Underlying array format for pixel data; normalization operates on NumPy arrays)

## Examples

```
pixels, metadata = msigen.load_pixels('path/to/saved/pixels'); vis.get_and_display_images(pixels, metadata, normalize='TIC', scale=0.999)
```

## Evaluation signals

- Pixel intensity values after normalization should fall in the range [0, 1] or proportional to TIC, with no pixel exceeding the sum of its pre-normalized intensities.
- Pixels with high total ion current should have proportionally reduced individual ion intensities; pixels with low TIC should have proportionally higher normalized intensities for the same analyte.
- Spatial patterns in ion images should become more visible (contrast improvement) after TIC normalization if local TIC variation was obscuring analyte distribution.
- When comparing ion images before and after TIC normalization, the relative intensity ranking of high-abundance pixels should be preserved, but absolute intensity differences should be reduced.
- Metadata JSON should contain the TIC value (sum of intensities) for each pixel; verify that normalization divides by these values correctly.

## Limitations

- TIC normalization assumes that variation in total ion signal is primarily noise or instrumental artifact; if TIC variation is correlated with scientifically meaningful sample properties (e.g., local matrix concentration), normalization will remove that signal.
- Pixels with very low TIC (near-zero ion signal) may produce unstable or artificially high normalized intensities if not handled with a small pseudocount or minimum threshold; MSIGen's implementation details on zero-handling are not fully specified in the article.
- TIC normalization is sensitive to outlier pixels with extremely high or low TIC; quantile-based scaling (scale parameter) is recommended post-normalization to improve visualization, but this is a separate, optional step.
- Not suitable for time-of-flight (TOF) or other high-resolution instruments where m/z binning strategy significantly affects total ion count; article focuses on nano-DESI MSI and does not address resolution-dependent effects.

## Evidence

- [other] MSIGen supports image normalization to total ion current (TIC) via normalize='TIC' parameter and to an internal standard via normalize='intl_std' parameter when processing pixel arrays.: "normalize='TIC' parameter and to an internal standard via normalize='intl_std' parameter when processing pixel arrays"
- [other] Call MSIGen's get_and_display_images function with the chosen normalization parameters (normalize, std_idx, std_precursor, std_mass, std_fragment, std_mobility, std_charge) to apply normalization across all image layers.: "Call MSIGen's get_and_display_images function with the chosen normalization parameters (normalize, std_idx, ...) to apply normalization across all image layers"
- [other] Optionally apply pixel intensity scaling via scale parameter (quantile-based; e.g., 0.999 sets max to 99.9th percentile) or manual threshold.: "scale parameter (quantile-based; e.g., 0.999 sets max to 99.9th percentile)"
- [other] Load the pixel array (NumPy format) and associated metadata JSON file using MSIGen's load_pixels function.: "Load the pixel array (NumPy format) and associated metadata JSON file using MSIGen's load_pixels function"
- [intro] MSIGen is designed with nano-DESI MSI in mind: "is designed with nano-DESI MSI in mind"
- [methods] normalize = 'TIC' to normalize the images to total ion current: "normalize = 'TIC' to normalize the images to total ion current"
