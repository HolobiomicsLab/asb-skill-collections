---
name: mass-spectrometry-image-normalization
description: Use when after loading a pixel array (NumPy format) and its associated metadata JSON file from MSIGen, when you need to account for pixel-to-pixel variations in total ion signal or when comparing relative abundances of multiple ions within or across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0611
  tools:
  - MSIGen
  - Python
  - Jupyter Notebook
  - NumPy
  - pyBaf2Sql
  techniques:
  - MS-imaging
  - ion-mobility-MS
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

# mass-spectrometry-image-normalization

## Summary

Normalize pixel intensity arrays from mass spectrometry imaging (MSI) data to total ion current (TIC) or an internal standard to enable quantitative and comparable visualization across ion images. This corrects for variations in ion abundance and detector response across the sample.

## When to use

Apply this skill after loading a pixel array (NumPy format) and its associated metadata JSON file from MSIGen, when you need to account for pixel-to-pixel variations in total ion signal or when comparing relative abundances of multiple ions within or across samples. Use TIC normalization when absolute signal variations are expected and should be corrected; use internal standard normalization when a known, stable reference compound is present in the sample and you want intensity ratios relative to that standard.

## When NOT to use

- When the pixel array has already been normalized or when you are working with preprocessed, vendor-supplied normalized images
- When no suitable internal standard is available in the sample and TIC variation is not a meaningful correction for your biological question
- When processing data from imaging modalities other than line-scan nano-DESI MSI, as MSIGen is designed specifically for nano-DESI MSI line-scan data

## Inputs

- NumPy pixel array (from MSIGen load_pixels output)
- metadata JSON file with mass list, image dimensions, and standard information
- mass list file (Excel or compatible format) with m/z, precursor m/z, fragment m/z, ion mobility, and charge for standards

## Outputs

- normalized pixel intensity array (NumPy format)
- publication-style ion images (PNG/PDF)
- raw normalized images (NumPy arrays or CSV)
- normalized metadata file documenting normalization mode and parameters applied

## How to apply

Load the pixel array and metadata using MSIGen's load_pixels() function. Choose a normalization mode: 'TIC' to normalize each pixel to its total ion current, 'intl_std' to normalize to an internal standard, or 'none' to skip normalization. If using 'intl_std', identify the internal standard by mass list index (std_idx) or by matching precursor m/z, fragment m/z, ion mobility, and charge parameters (std_precursor, std_mass, std_fragment, std_mobility, std_charge). Call get_and_display_images() with the chosen normalize parameter and standard identifiers. Optionally apply pixel intensity scaling via the scale parameter (e.g., scale=0.999 sets maximum to the 99.9th percentile of pixel intensities) or manual threshold to improve dynamic range. Save the normalized output according to image_savetype (e.g., publication figures, raw images, or CSV arrays).

## Related tools

- **MSIGen** (Core package providing load_pixels(), get_and_display_images(), and normalization parameter handling) — https://github.com/LabLaskin/MSIGen
- **Python** (Runtime environment; MSIGen requires Python >=3.9 and <=3.11)
- **Jupyter Notebook** (Interactive environment for loading pixels, configuring normalization parameters, and visualizing results)
- **NumPy** (Array data structure for pixel intensity matrices)
- **pyBaf2Sql** (Optional dependency for reading Bruker .baf format raw data files into MSIGen) — https://github.com/gtluu/pyBaf2Sql

## Examples

```
pixels, metadata = msigen.load_pixels(load_path); vis.get_and_display_images(pixels, metadata, normalize='TIC', scale=0.999, image_savetype='fig')
```

## Evaluation signals

- Normalized pixel arrays have intensity distributions appropriate to the chosen method: TIC-normalized pixels should have similar sums across the image; internal standard-normalized pixels should reflect relative abundance ratios to the standard
- Metadata JSON retains all normalization parameters (normalize mode, std_idx, std_precursor, scale, threshold) for reproducibility and audit trail
- Visually inspected ion images show improved contrast and reduced artifactual spatial variation compared to unnormalized raw images, particularly when scale or threshold parameters are applied
- Output image dimensions (height, width) match the input pixel array and metadata specifications
- No infinity or NaN values appear in the normalized array (or are explicitly documented in handle_infinity parameter for ratio images if used downstream)

## Limitations

- TIC normalization assumes that total ion current is a reliable proxy for sample abundance; it may fail or be misleading if ion suppression or enhancement varies spatially across the sample
- Internal standard normalization requires that the standard compound is uniformly distributed across the sample area; inhomogeneous standard distribution will produce incorrect relative intensity maps
- Quantile-based scaling (scale parameter) is sensitive to outlier pixels; extreme signals in a small region can compress the dynamic range of the rest of the image
- MSIGen is designed with nano-DESI MSI in mind; applicability to other MSI acquisition modes (e.g., MALDI, ambient ionization) has not been validated in the article

## Evidence

- [other] MSIGen supports image normalization to total ion current (TIC) via normalize='TIC' parameter and to an internal standard via normalize='intl_std' parameter when processing pixel arrays.: "MSIGen supports image normalization to total ion current (TIC) via normalize='TIC' parameter and to an internal standard via normalize='intl_std' parameter"
- [other] Load the pixel array (NumPy format) and associated metadata JSON file using MSIGen's load_pixels function. Select normalization mode and, if using internal standard, identify the standard by mass list index (std_idx) or by matching precursor m/z, fragment m/z, mobility, and charge parameters.: "Load the pixel array (NumPy format) and associated metadata JSON file using MSIGen's load_pixels function. 2. Select normalization mode ('TIC', 'intl_std', or 'none') and, if using internal standard,"
- [other] Call MSIGen's get_and_display_images function with the chosen normalization parameters (normalize, std_idx, std_precursor, std_mass, std_fragment, std_mobility, std_charge) to apply normalization across all image layers.: "Call MSIGen's get_and_display_images function with the chosen normalization parameters (normalize, std_idx, std_precursor, std_mass, std_fragment, std_mobility, std_charge) to apply normalization"
- [other] Optionally apply pixel intensity scaling via scale parameter (quantile-based; e.g., 0.999 sets max to 99.9th percentile) or manual threshold.: "Optionally apply pixel intensity scaling via scale parameter (quantile-based; e.g., 0.999 sets max to 99.9th percentile) or manual threshold."
- [readme] MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format and is designed with nano-DESI MSI in mind.: "MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format and is designed with nano-DESI MSI in mind."
