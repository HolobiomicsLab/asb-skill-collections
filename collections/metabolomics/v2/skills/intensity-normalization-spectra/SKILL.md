---
name: intensity-normalization-spectra
description: Use when after noise reduction when working with imported imzML MSI data where pixel-to-pixel or sample-to-sample intensity variations due to instrumental sensitivity or sample loading differences must be corrected before mean intensity calculation, ROI analysis, or metabolite annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - napari
  - Python
  - MSI-Explorer
derived_from:
- doi: 10.1021/acs.analchem.5c01513
  title: MSI-Explorer
evidence_spans:
- The MSI-Explorer napari plugin is a powerful tool designed for targeted biochemical annotations in MSI data.
- '[![Python Version](https://img.shields.io/pypi/pyversions/MSI-Explorer.svg?color=green)](https://python.org)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msi_explorer_cq
    doi: 10.1021/acs.analchem.5c01513
    title: MSI-Explorer
  dedup_kept_from: coll_msi_explorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01513
  all_source_dois:
  - 10.1021/acs.analchem.5c01513
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# intensity-normalization-spectra

## Summary

Standardize mass spectrometry imaging (MSI) spectral intensities across all pixels and m/z values using one of four normalization methods (TIC, RMS, median, or reference peak) to enable valid comparative analysis and reduce instrumental/sample-preparation bias in downstream ROI and biochemical annotation workflows.

## When to use

Apply this skill after noise reduction when working with imported imzML MSI data where pixel-to-pixel or sample-to-sample intensity variations due to instrumental sensitivity or sample loading differences must be corrected before mean intensity calculation, ROI analysis, or metabolite annotation. Essential when comparing spectra across multiple tissue regions or samples.

## When NOT to use

- Input is already a centroid-mode dataset without raw ion counts (normalization assumes quantitative intensity values).
- Profile-mode data that has not yet been converted to centroid mode (use profile→centroid conversion first).
- Exploratory visualization only, where relative peak heights within a single spectrum are sufficient and inter-pixel comparisons are not needed.

## Inputs

- Imported MSI spectral data (imzML format) with noise reduction applied
- Per-pixel spectral intensity matrix (m/z × pixel)
- Optional: reference m/z value for internal standard normalization

## Outputs

- Intensity-normalized spectral dataset (m/z × pixel matrix)
- Normalized mean spectrum (exportable as CSV)
- Normalized ion image visualization
- Preprocessed MSI data compatible with ROI analysis and database annotation

## How to apply

Within the MSI-Explorer napari plugin, load preprocessed (noise-reduced) imzML data and select one of four normalization methods: Total Ion Current (TIC) normalizes to the sum of all intensities per pixel; Root Mean Square (RMS) normalizes to the per-pixel RMS; Median normalizes to the median intensity; Reference Peak (internal standard) normalizes to a user-specified m/z peak. Execute the normalization, then verify by calculating and visualizing the mean spectrum and corresponding ion image. The choice of method depends on your experimental design: TIC is standard for untargeted profiling, RMS for variance-driven comparisons, Median for robust outlier resistance, and Reference Peak when an internal standard was spiked. Output is the normalized spectral dataset in the standardized MSI data format, ready for downstream visualization and ROI analysis.

## Related tools

- **napari** (Interactive visualization and UI platform hosting the MSI-Explorer plugin for parameter selection, normalization execution, and real-time spectrum/image display) — https://github.com/napari/napari
- **MSI-Explorer** (Napari plugin implementing noise reduction and four normalization methods (TIC, RMS, Median, Reference Peak) for MSI spectra preprocessing and ROI analysis) — https://github.com/MMV-Lab/MSI-Explorer
- **Python** (Programming language for scripting and automation of normalization workflows via the MSI-Explorer API)

## Examples

```
# Within napari MSI-Explorer plugin GUI: load imzML → Plugins > MSI-Explorer → select noise reduction (e.g. 3%) → select TIC normalization → click Execute → click Show true mean spectrum → Export spectrum data as CSV
```

## Evaluation signals

- Mean spectrum after normalization shows comparable total/RMS intensities across all samples or ROIs (no systematic intensity drift by region).
- Ion images for the same m/z peak appear uniform in intensity scale across tissue regions after normalization (contrast-to-noise ratio is stable).
- Per-pixel normalization factors (e.g., TIC sums or RMS values) are within expected ranges; extreme outliers or zero-valued normalizers indicate failed or spurious normalization.
- Normalized spectral data can be successfully exported as CSV and reimported for downstream annotation and ROI analysis without schema or format errors.
- Before/after comparison: unnormalized spectra show systematic intensity variation by pixel; normalized spectra show consistent scaling with preserved peak patterns.

## Limitations

- Reference Peak normalization requires a priori knowledge of an internal standard m/z value; incorrect selection yields misleading results.
- TIC normalization can be biased by a small number of intense ions; not recommended for data with extreme peak outliers (apply hotspot removal beforehand).
- Normalization assumes imzML data is in quantitative intensity units; if imported data is already log-transformed or in arbitrary units, results may not be interpretable.
- No automatic method selection guidance provided; user must choose the normalization method; inappropriate choice can suppress or amplify biologically relevant variability.

## Evidence

- [other] Apply intensity normalization to standardize spectral intensities across all pixels and m/z values.: "Apply intensity normalization to standardize spectral intensities across all pixels and m/z values."
- [readme] The normalization methods that the user can apply are - Total ion current (TIC) - Root mean square (RMS) - Medium - Reference peak (or internal standard): "The normalization methods that the user can apply are - Total ion current (TIC) - Root mean square (RMS) - Medium - Reference peak (or internal standard)"
- [readme] The pre-processing capabilities of MSI-Explorer enhance data quality and prepare MSI data for downstream analysis. Pre-processing steps involve noise reduction and normalization.: "The pre-processing capabilities of MSI-Explorer enhance data quality and prepare MSI data for downstream analysis."
- [readme] After pre-processing steps are chosen, click Execute and Show true mean spectrum to calculate the mean intensity.: "After pre-processing steps are chosen, click Execute and Show true mean spectrum to calculate the mean intensity."
- [intro] It covers data import, visualization, mean intensity calculation, region of interest (ROI) analysis, annotation with selected databases and pre-processing such as noise reduction and normalization.: "pre-processing such as noise reduction and normalization"
