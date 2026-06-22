---
name: internal-standard-intensity-calibration
description: Use when you have added a known internal standard compound to your nano-DESI MSI sample and want to correct for pixel-to-pixel variation in ionization efficiency or sample deposition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MSIGen
  - Python
  - Jupyter Notebook
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# internal-standard-intensity-calibration

## Summary

Normalize mass spectrometry imaging pixel intensities to an internal standard (IS) rather than total ion current, enabling quantitative comparison across pixels and samples by removing variation in ionization efficiency and sample loading. This is applied during image reconstruction in MSIGen when the identity and mass/mobility properties of an IS compound are known.

## When to use

Apply this skill when you have added a known internal standard compound to your nano-DESI MSI sample and want to correct for pixel-to-pixel variation in ionization efficiency or sample deposition. Use this instead of TIC normalization when IS intensity variation is expected to correlate more strongly with true analyte quantity than total ion current, or when comparing relative abundances across multiple samples or regions with different ionization conditions.

## When NOT to use

- Internal standard is not present in the sample or mass list — use TIC normalization instead.
- IS signal is extremely weak or noisy relative to analytes — division will amplify noise and produce artifacts.
- IS signal varies spatially due to sample inhomogeneity unrelated to ionization efficiency — normalization may remove real biological variation.

## Inputs

- NumPy array of pixel intensities (pixel_array format from MSIGen.load_pixels)
- metadata JSON file mapping mass list indices to m/z, fragment m/z, mobility, charge
- internal standard mass list entry (identified by index or matching parameters: precursor m/z, fragment m/z, mobility, charge)
- pixel array dimensions (img_height, img_width from metadata)

## Outputs

- normalized pixel intensity array (internal standard–normalized)
- publication-style ion images (PNG/PDF) with uniform IS background
- raw normalized image files (NPZ/CSV) for downstream analysis
- optionally, scaled/thresholded visualization with quantile-based intensity clipping

## How to apply

After loading the NumPy pixel array and metadata JSON via MSIGen's load_pixels function, identify your internal standard in the mass list by one of two methods: (1) supply the standard's list index (std_idx parameter), or (2) match by precursor m/z, fragment m/z, ion mobility, and charge (std_precursor, std_mass, std_fragment, std_mobility, std_charge parameters). Call get_and_display_images with normalize='intl_std' and your chosen identification parameters. The function divides all pixel intensities by the IS intensity at each pixel, producing normalized images. Optionally apply quantile-based intensity scaling (scale parameter, e.g., 0.999 sets max to 99.9th percentile) to optimize contrast. Evaluate success by verifying that IS intensity is now uniform across pixels, and that analyte image contrast is preserved relative to the un-normalized version.

## Related tools

- **MSIGen** (provides load_pixels, get_and_display_images functions for IS-normalized image reconstruction; handles pixel array I/O and normalization arithmetic) — https://github.com/LabLaskin/MSIGen
- **Python** (runtime environment for MSIGen (required version >=3.9 and <=3.11))
- **Jupyter Notebook** (interactive environment for calling MSIGen normalization functions and inspecting normalized images)

## Examples

```
pixels, metadata = msigen.load_pixels(load_path); vis.get_and_display_images(pixels, metadata, normalize='intl_std', std_idx=5, scale=0.999, image_savetype='figures')
```

## Evaluation signals

- IS intensity image is spatially uniform (flat across all pixels) after normalization — confirms that per-pixel division was applied.
- Analyte ion images retain expected spatial patterns and contrast after IS normalization — confirms that biological/chemical information is preserved.
- Intensity range and quantile thresholds are consistent with expected dynamic range for the IS compound.
- When applied to replicate samples, IS-normalized images show reduced pixel-to-pixel variance compared to TIC-normalized images.
- Optional: compare IS-normalized image to TIC-normalized and raw images to confirm that ionization artifacts (e.g., edge effects, uneven spray) have been attenuated.

## Limitations

- Internal standard must be co-localized with analytes in all imaged regions; if IS is absent or depleted in some areas, normalization will fail or produce NaN/Inf values in those pixels.
- IS signal intensity must exceed noise floor; weak IS signal can amplify background noise and create spurious structure in normalized images.
- MSIGen requires explicit identification of the IS in the mass list (by index or matching m/z/mobility parameters); incorrect or ambiguous matching will normalize to the wrong compound.
- Normalization assumes IS ionization efficiency is constant across the image; if IS ionization varies spatially (e.g., due to sample matrix effects), residual variation will remain in normalized images.
- No built-in method to detect or flag when IS signal is missing or saturated; user must visually inspect IS intensity image to verify validity.

## Evidence

- [other] MSIGen supports image normalization to an internal standard via normalize='intl_std' parameter when processing pixel arrays.: "normalize to an internal standard via normalize='intl_std' parameter when processing pixel arrays"
- [other] Identify the standard by mass list index (std_idx) or by matching precursor m/z, fragment m/z, mobility, and charge parameters.: "identify the standard by mass list index (std_idx) or by matching precursor m/z, fragment m/z, mobility, and charge parameters"
- [other] Call MSIGen's get_and_display_images function with chosen normalization parameters to apply normalization across all image layers.: "get_and_display_images function with the chosen normalization parameters (normalize, std_idx, std_precursor, std_mass, std_fragment, std_mobility, std_charge) to apply normalization across all image"
- [other] Optionally apply pixel intensity scaling via scale parameter (quantile-based; e.g., 0.999 sets max to 99.9th percentile).: "scale parameter (quantile-based; e.g., 0.999 sets max to 99.9th percentile) or manual threshold"
- [readme] MSIGen is designed with nano-DESI MSI in mind and supports processing of line-scan data to visualizable format.: "MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format and is designed with nano-DESI MSI in mind"
