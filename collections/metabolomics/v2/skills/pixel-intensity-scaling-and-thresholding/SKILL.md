---
name: pixel-intensity-scaling-and-thresholding
description: Use when after normalizing an MSI pixel array to TIC or an internal standard, when the raw pixel intensity distribution spans multiple orders of magnitude and produces images with poor contrast or where extreme outlier intensities would wash out spatial detail.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - MSIGen
  - Python
  - Jupyter Notebook
  - NumPy
  techniques:
  - MS-imaging
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00178
  all_source_dois:
  - 10.1021/jasms.4c00178
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Pixel Intensity Scaling and Thresholding

## Summary

Apply quantile-based or manual intensity scaling to mass spectrometry imaging pixel arrays to control the dynamic range and visual contrast of ion images. This skill normalizes pixel intensities to publication-quality ranges after image normalization has been applied.

## When to use

After normalizing an MSI pixel array to TIC or an internal standard, when the raw pixel intensity distribution spans multiple orders of magnitude and produces images with poor contrast or where extreme outlier intensities would wash out spatial detail. Use this when generating publication-ready ion images from processed MSI data where you need fine control over the maximum displayable intensity.

## When NOT to use

- Input pixel array has not yet been normalized to TIC or internal standard; apply normalization first, then scale.
- You need to preserve the absolute intensity ratios between different ions for downstream quantitative analysis (scaling and thresholding distort intensity relationships).
- Pixel array is already in the target intensity range (< 1–2 orders of magnitude spread); scaling may introduce unnecessary artifacts or reduce dynamic range.

## Inputs

- Normalized pixel array (NumPy ndarray, shape: [n_ions, n_pixels] after TIC or internal standard normalization)
- Metadata JSON with ion mass list and normalization parameters
- Quantile value (float, 0–1) or manual threshold intensity (float ≥ 0)

## Outputs

- Scaled pixel intensity array (NumPy ndarray, same shape, intensity values remapped to [0, max_intensity])
- Publication-style ion images (PNG, TIFF, or PDF; pixel intensities mapped to colormap range)
- Raw scaled image arrays (CSV or NumPy binary format, optional)

## How to apply

After calling get_and_display_images() with normalization parameters (normalize='TIC' or normalize='intl_std'), apply pixel intensity scaling via the scale parameter, which sets the maximum pixel intensity to the pixel intensity value at the specified quantile (e.g., scale=0.999 caps the display maximum to the 99.9th percentile intensity). Alternatively, use the threshold parameter to manually set a fixed maximum intensity value. The choice between quantile-based and manual thresholds depends on whether your dataset has consistent intensity distributions across experiments (use quantile for consistency) or whether you have a domain-justified fixed cutoff (use manual threshold). After scaling, verify that the resulting image preserves spatial features of interest and that no more than the intended fraction of pixels are saturated to the maximum display value.

## Related tools

- **MSIGen** (Core Python package that implements get_and_display_images() function with scale and threshold parameters for pixel intensity scaling after normalization) — https://github.com/LabLaskin/MSIGen
- **Python** (Runtime environment (version >=3.9 and <=3.11) for executing MSIGen scaling functions)
- **Jupyter Notebook** (Interactive environment for iterative exploration of scale and threshold parameters and visual inspection of scaled images) — https://github.com/LabLaskin/MSIGen/blob/main/other_files/MSIGen_jupyter.ipynb
- **NumPy** (Underlying array computation and quantile calculation for scale parameter)

## Examples

```
vis.get_and_display_images(pixels, metadata, normalize='TIC', scale=0.999, image_savetype='png', output_file_loc='./scaled_images/')
```

## Evaluation signals

- Verify that the output image has improved contrast and preserves spatial detail compared to the unscaled image; no single ion should dominate the entire image or render it as a single flat color.
- Check that the fraction of pixels at the maximum intensity (saturation) matches the specified quantile ± small margin (e.g., for scale=0.999, expect ~0.1% of pixels saturated).
- Confirm that the pixel intensity range after scaling is within the colormap's supported range (typically 0–1 or 0–255) and matches the image_savetype output format (PNG, TIFF, CSV).
- For quantile-based scaling, verify reproducibility by re-running the same scale value on the same pixel array; intensity remapping should be deterministic.
- For manual threshold mode, visually inspect multiple scaled images to confirm that the fixed threshold value produces consistent visual quality across samples with different intensity distributions.

## Limitations

- Quantile-based scaling assumes a smooth, monotonic intensity distribution; highly bimodal or multimodal distributions may produce unintuitive results where the 99.9th percentile is far from visually perceptible signal.
- Manual threshold values are not portable across datasets with different sample types or ionization conditions; a threshold optimized for one tissue type may over- or under-scale another.
- Scaling is applied uniformly across all ions in the pixel array; if different ion masses have vastly different intensities (e.g., abundant metabolites vs. trace lipids), a single scale value may over-saturate abundant ions while leaving rare ions faint.
- The scale and threshold operations are lossy; the original intensity ratios are not recoverable from the scaled image and cannot be used for quantitative comparisons without access to the unscaled array.

## Evidence

- [other] Optionally apply pixel intensity scaling via scale parameter (quantile-based; e.g., 0.999 sets max to 99.9th percentile) or manual threshold.: "Optionally apply pixel intensity scaling via scale parameter (quantile-based; e.g., 0.999 sets max to 99.9th percentile) or manual threshold."
- [other] Image pixel intensity scaling by quantile: "scale sets the maximum pixel intensity to the pixel with the intensity of this quantile"
- [other] Image pixel intensity threshold setting: "threshold parameter to manually set maximum pixel intensity"
- [other] Call MSIGen's get_and_display_images function with the chosen normalization parameters (normalize, std_idx, std_precursor, std_mass, std_fragment, std_mobility, std_charge) to apply normalization across all image layers.: "Call MSIGen's get_and_display_images function with the chosen normalization parameters to apply normalization across all image layers"
- [other] Save the normalized image output as publication-style figures, raw images, or CSV arrays according to the image_savetype parameter.: "Save the normalized image output as publication-style figures, raw images, or CSV arrays according to the image_savetype parameter."
