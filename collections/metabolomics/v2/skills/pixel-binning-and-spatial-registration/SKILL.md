---
name: pixel-binning-and-spatial-registration
description: Use when you have raw line-scan mass spectrometry imaging data from nano-DESI
  or other line-scan acquisition modes and need to produce a georeferenced 3D pixel
  array.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
  tools:
  - MSIGen
  - Python
  - Jupyter Notebook
  - pyBaf2Sql
  - NumPy
  techniques:
  - MS-imaging
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- MSIGen provides tools for processing mass spectrometry imaging data acquired in
  line-scan mode into images and figures.
- from MSIGen import msigen
- Using an environment with python version >=3.9 and <=3.11
- If you want to use MSIGen in a Jupyter notebook, you may also need to install jupyter
  notebook
- MSIGen is most easily used through Jupyter Notebooks or through the GUI.
- If you are planning on using Bruker .d data in the .baf format, you will also need
  to install pyBaf2Sql from GitHub
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

# Pixel Binning and Spatial Registration

## Summary

This skill consolidates spatially adjacent mass spectrometry imaging (MSI) measurements into fixed-size pixels and registers them to a uniform coordinate system. It is essential for converting raw line-scan MSI data into a standardized 3D array suitable for visualization and comparative analysis across samples.

## When to use

Apply this skill when you have raw line-scan mass spectrometry imaging data from nano-DESI or other line-scan acquisition modes and need to produce a georeferenced 3D pixel array. Specifically, use it when you have defined the scanned area dimensions (height and width in physical units such as mm), specified the desired image normalization strategy (max, min, or mean pixels per line), and want to generate a uniform spatial grid where each pixel contains aggregated m/z-matched spectra.

## When NOT to use

- Input spectra have not yet been matched to m/z targets within specified tolerance windows—complete tolerance filtering first.
- Scanned area dimensions or pixel acquisition geometry are unknown or unavailable—spatial binning requires definitive physical coordinates.
- Data is already in a pre-binned or raster format (e.g., previously processed imaging data from commercial software)—re-binning may introduce interpolation artifacts.

## Inputs

- Extracted mass spectra (m/z arrays with intensities)
- Matched m/z list (with target m/z, precursor m/z, fragment m/z, and/or ion mobility values)
- Scanned area dimensions (height and width in mm or other physical units)
- Tolerance parameters for mass and mobility filtering (ppm, m/z, 1/K0, or μs)
- Scan line metadata (number of lines, pixels per line)

## Outputs

- 3D NumPy pixel array of shape (n+1, y, x) where n = number of matched masses, y = normalized height, x = normalized width
- Pixels metadata JSON file containing m/z values, ion mobility values (if applicable), normalization method, and array dimensions
- pixels.npy (binary NumPy array)
- pixels_metadata.json (JSON metadata file)

## How to apply

After extracting spectra and matching m/z values within specified tolerances (MS1, precursor, fragment, and mobility tolerances as applicable), initialize the MSIGen object with image acquisition parameters: scanned area height, scanned area width, and normalization method. Call get_image_data(verbose=True) to bin the matched spectra spatially into a 3D array of shape (n+1, y, x), where n is the number of targeted masses and the extra dimension holds the total ion current (TIC) image. The normalization parameter controls how pixels per line are scaled: 'max' uses the maximum, 'min' uses the minimum, or 'mean' uses the average number of pixels per line across all lines. This ensures consistent spatial resolution and allows fair comparison across acquisitions with variable scan densities.

## Related tools

- **MSIGen** (Core Python package that implements pixel binning and spatial registration via the get_image_data() method and msigen class initialization) — https://github.com/LabLaskin/MSIGen
- **Python** (Runtime environment (version ≥3.9 and ≤3.11) required to execute MSIGen binning logic)
- **NumPy** (Underlying library used to create and manage the 3D pixel array output)

## Examples

```
metadata, pixels = MSIGen_generator.get_image_data(verbose=True)
where MSIGen_generator = msigen(example_file='data.d', mass_list_dir='masses.xlsx', mass_tolerance_MS1=5, img_height=10, img_width=10, normalize_img_sizes='mean', output_file_loc='./output/')
```

## Evaluation signals

- Output pixels.npy array has shape (n+1, y, x) where n matches the number of unique m/z targets, and y and x match the normalized scanned area dimensions
- pixels_metadata.json contains all registered m/z values, ion mobility values (if applicable), normalization method used, and correct array shape
- Pixel intensity values are non-negative and consistent with input spectrum intensity units (e.g., counts or relative abundance)
- When visualized, ion images show coherent spatial patterns aligned with the known sample geometry and absence of discontinuities or aliasing artifacts at line boundaries
- Reproducibility: re-running with identical input parameters, tolerance windows, and normalization method produces identical or near-identical pixel arrays (byte-for-byte or within numerical precision)

## Limitations

- Pixel binning resolution is constrained by the input scan density and normalization method; sparsely sampled lines may produce coarse spatial features.
- Normalization to max, min, or mean pixels per line can create artificial heterogeneity if scan speed or dwell time varies significantly across the sample.
- MSIGen is designed with nano-DESI MSI in mind; applicability to other line-scan modalities (e.g., MALDI, secondary ion mass spectrometry) may require validation.
- Ion mobility matching is optional; if mobility_tolerance is not specified, ion mobility filtering is not applied and may lead to co-localization of isobars.
- The pipeline does not perform image interpolation or deconvolution; to smooth the output, apply interpolation post-binning using the visualization module (e.g., 'linear' interpolation option).

## Evidence

- [methods] bin pixels spatially, and generate a 3D array of shape (n+1, y, x) where n is the number of masses plus one TIC image: "bin pixels spatially, and generate a 3D array of shape (n+1, y, x) where n is the number of masses plus one TIC image"
- [methods] Set image acquisition parameters: scanned area height and width in specified units (e.g., mm), and whether to normalize all images to the same size using max, min, or mean pixels per line.: "Set image acquisition parameters: scanned area height and width in specified units (e.g., mm), and whether to normalize all images to the same size using max, min, or mean pixels per line"
- [methods] Initialize the msigen object with all parameters and call get_image_data(verbose=True) to extract spectra, match m/z values and mobility values within tolerances: "Initialize the msigen object with all parameters and call get_image_data(verbose=True) to extract spectra, match m/z values and mobility values within tolerances"
- [intro] MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format: "MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format"
- [methods] Verify output files pixels.npy and pixels_metadata.json are written to the specified output directory with correct dimensions and metadata fields.: "Verify output files pixels.npy and pixels_metadata.json are written to the specified output directory with correct dimensions and metadata fields"
