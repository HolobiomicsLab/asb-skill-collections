---
name: image-visualization-formatting
description: Use when you have loaded a normalized or raw pixel array (NumPy format) with associated metadata from MSI line-scan data, and need to generate publication-quality ion images with controlled intensity scaling, smoothing, and optional ratio or fractional abundance comparisons across multiple m/z.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - MSIGen
  - Python
  - Jupyter Notebook
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# image-visualization-formatting

## Summary

Apply normalization, scaling, and interpolation transformations to mass spectrometry imaging pixel arrays to produce publication-ready ion images and comparative visualizations (ratio, fractional abundance). This skill bridges processed pixel data to interpretable visual formats suitable for scientific communication.

## When to use

You have loaded a normalized or raw pixel array (NumPy format) with associated metadata from MSI line-scan data, and need to generate publication-quality ion images with controlled intensity scaling, smoothing, and optional ratio or fractional abundance comparisons across multiple m/z layers.

## When NOT to use

- Input pixel array is not in NumPy format or lacks associated metadata JSON—preprocessing to array form is required first.
- Data are already formatted as publication figures or raster images; this skill is for converting numerical arrays to images, not post-processing graphics.
- No clear reference or internal standard compound is available for internal standard normalization and TIC alone does not adequately correct for spatial variations in ionization efficiency.

## Inputs

- NumPy array (pixel array in float64 or uint format)
- JSON metadata file (associated with pixel array, containing m/z list, acquisition parameters)
- Mass list (integer list of m/z indices to visualize)
- Internal standard parameters (optional: std_idx, std_precursor m/z, std_fragment m/z, std_mobility, std_charge)

## Outputs

- Publication-style ion images (PNG, PDF, or matplotlib figure objects)
- Raw pixel intensity arrays (NumPy .npy or CSV format)
- Ratio images (element-wise division of two m/z layers with NaN/inf handling)
- Fractional abundance images (normalized by sum across all m/z layers per pixel)

## How to apply

Load the pixel array and metadata JSON using MSIGen's load_pixels function, then invoke get_and_display_images with your chosen normalization mode (TIC, internal standard, or none), intensity scaling via quantile-based scaling (e.g., scale=0.999 caps intensity at the 99.9th percentile) or manual threshold, and interpolation option (linear or none) to control smoothing. For comparative visualizations, call fractional_abundance_images or ratio_images with the target m/z indices and handle_infinity parameter set appropriately to manage divide-by-zero errors. Specify image_savetype to write outputs as publication-style figures (PNG/PDF), raw arrays (NumPy .npy), or CSV tables. The normalization step is critical: TIC normalization accounts for pixel-to-pixel variation in total signal, while internal standard normalization corrects for ionization efficiency by dividing each pixel's signal by a known reference compound identified by mass, mobility, charge, or list index.

## Related tools

- **MSIGen** (Core package providing get_and_display_images, fractional_abundance_images, ratio_images functions and load_pixels for reading serialized pixel arrays and metadata.) — https://github.com/LabLaskin/MSIGen
- **Jupyter Notebook** (Interactive development environment for executing visualization workflows step-by-step and iterating on normalization and scaling parameters.)
- **Python** (Runtime language for MSIGen; requires version >=3.9 and <=3.11 to ensure compatibility with dependencies.)

## Examples

```
pixels, metadata = msigen.load_pixels('path/to/saved_pixels.npy'); vis.get_and_display_images(pixels, metadata, normalize='TIC', scale=0.999, interpolation='linear', image_savetype='png')
```

## Evaluation signals

- Output images show spatially coherent ion signal distribution without salt-and-pepper noise or clipping artifacts.
- Intensity histograms or quantile metrics confirm that scaling has been applied correctly (e.g., max pixel intensity is at or below the specified quantile threshold).
- Ratio images do not contain unexpected infinity or NaN regions, or such regions are handled according to handle_infinity parameter.
- Metadata embedded in saved figures (e.g., PNG exif or figure title) or accompanying CSV files match the m/z values, normalization mode, and acquisition metadata.
- Visual comparison across multiple normalization modes (TIC vs. internal standard) shows expected differences in relative intensity patterns (internal standard correction should suppress spatially uniform background).

## Limitations

- Quantile-based intensity scaling is data-dependent; the same quantile value may produce over- or under-scaled images across datasets with different noise profiles or dynamic ranges.
- Internal standard normalization requires accurate identification of the standard compound; errors in mass tolerance (mass_tolerance_MS1, mass_tolerance_prec, mass_tolerance_frag) or mobility tolerance can lead to incorrect standard assignment and flawed normalization.
- Interpolation smoothing (linear mode) can blur sharp chemical boundaries or inflate apparent spatial resolution; 'none' option may preserve artifacts.
- MSIGen is designed specifically for nano-DESI MSI data; applicability to other MSI modalities (MALDI, DESI) or non-line-scan acquisition geometries is not documented.

## Evidence

- [other] MSIGen supports image normalization to total ion current (TIC) via normalize='TIC' parameter and to an internal standard via normalize='intl_std' parameter when processing pixel arrays.: "MSIGen supports image normalization to total ion current (TIC) via normalize='TIC' parameter and to an internal standard via normalize='intl_std' parameter when processing pixel arrays."
- [other] Call MSIGen's get_and_display_images function with the chosen normalization parameters (normalize, std_idx, std_precursor, std_mass, std_fragment, std_mobility, std_charge) to apply normalization across all image layers. Optionally apply pixel intensity scaling via scale parameter (quantile-based; e.g., 0.999 sets max to 99.9th percentile) or manual threshold.: "call MSIGen's get_and_display_images function with the chosen normalization parameters (normalize, std_idx, std_precursor, std_mass, std_fragment, std_mobility, std_charge) to apply normalization"
- [other] Save the normalized image output as publication-style figures, raw images, or CSV arrays according to the image_savetype parameter.: "Save the normalized image output as publication-style figures, raw images, or CSV arrays according to the image_savetype parameter."
- [methods] Load previously saved NumPy array and metadata files and Visualize and display ion images with normalization options.: "Load previously saved NumPy array and metadata files; pixels, metadata = msigen.load_pixels(load_path). Visualize and display ion images with normalization options via"
- [methods] Generate fractional abundance images and Generate ratio images with optional handle_infinity parameter to replace infinity values from divide by zero errors.: "Generate fractional abundance images via vis.fractional_abundance_images(pixels, metadata, ...) and ratio images via vis.ratio_images(pixels, metadata, ...); handle_infinity parameter to replace"
- [readme] MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format and is designed with nano-DESI MSI in mind.: "MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format and is designed with nano-DESI MSI in mind."
