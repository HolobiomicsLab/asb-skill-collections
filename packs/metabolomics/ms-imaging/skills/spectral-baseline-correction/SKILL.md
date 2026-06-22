---
name: spectral-baseline-correction
description: Use when you have loaded raw MSI spectral data (imzML format) in profile or centroid mode and need to remove background noise and baseline artifacts before intensity normalization or ROI analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - napari
  - Python
  - MSI-Explorer
  techniques:
  - MS-imaging
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

# spectral-baseline-correction

## Summary

Correct baseline drift and remove background signal from mass spectrometry imaging (MSI) spectra to improve signal-to-noise ratio and enable accurate downstream analysis. This preprocessing step is essential for normalized and cleaned MSI data in targeted biochemical annotation workflows.

## When to use

Apply this skill when you have loaded raw MSI spectral data (imzML format) in profile or centroid mode and need to remove background noise and baseline artifacts before intensity normalization or ROI analysis. Use it when the spectral signal contains non-biological background that degrades peak detection or when comparing intensities across multiple pixels requires a consistent baseline.

## When NOT to use

- Input MSI data is already pre-processed and baseline-corrected by the instrument vendor or upstream pipeline
- You are analyzing already-normalized feature tables or summary statistics (not raw spectral data)
- The analysis goal is exploratory visualization only and does not require quantitative intensity comparisons

## Inputs

- imzML file (profile or centroid mode MSI data)
- MSI spectral dataset loaded in napari viewer
- Noise reduction percentage parameter (user-specified threshold)

## Outputs

- Baseline-corrected MSI spectra with reduced background signal
- Cleaned spectral dataset compatible with downstream visualization and ROI analysis
- Mean spectrum plot (via 'Show true mean spectrum')
- Exportable spectrum data (.csv format)

## How to apply

Load imported MSI spectral data using the MSI-Explorer napari plugin in Python. Select your desired noise reduction level (expressed as a percentage) in the pre-processing panel. The plugin applies noise reduction filtering to remove background signal and improve signal-to-noise ratio across the spectral dataset. Execute the preprocessing step, then verify the result by clicking 'Show true mean spectrum' to visualize the cleaned spectrum. Apply noise reduction before intensity normalization (TIC, RMS, median, or reference peak methods) to ensure that only true biological signal is normalized. The workflow chains noise reduction → normalization → visualization for downstream ROI analysis or database annotation.

## Related tools

- **napari** (Interactive viewer and plugin host for loading MSI data, applying pre-processing controls, and visualizing baseline-corrected spectra) — https://github.com/napari/napari
- **Python** (Underlying language for MSI-Explorer plugin implementation and spectral processing algorithms)
- **MSI-Explorer** (End-to-end napari plugin that integrates data import, noise reduction, normalization, and ROI analysis in a unified workflow) — https://github.com/MMV-Lab/MSI-Explorer

## Evaluation signals

- Visual inspection: mean spectrum plot shows reduced noise floor and sharper peak definition compared to raw data
- Signal-to-noise ratio increases after noise reduction step (quantifiable via peak height vs. baseline variance)
- Exported spectrum data (.csv) contains the same m/z values as input but with lower intensity values in background regions
- Downstream ROI mean spectra are reproducible and consistent across repeated selections when applied to baseline-corrected data
- Normalized intensities (TIC, RMS, etc.) are more comparable across pixels after baseline correction than without it

## Limitations

- Noise reduction level (percentage) is user-specified and may require trial-and-error optimization for different tissue types or ionization modes
- Aggressive noise reduction (high percentage) may remove weak but true biological signals, particularly for low-abundance metabolites
- The plugin also supports hotspot removal (default 99.99% quantile threshold) which may interact unpredictably with noise reduction; combined effects should be validated visually
- Profile mode data must be converted to centroid mode upon import (user prompted interactively); this conversion itself may introduce artifacts

## Evidence

- [other] Apply noise reduction filtering to remove background signal and improve signal-to-noise ratio across the spectral dataset.: "Apply noise reduction filtering to remove background signal and improve signal-to-noise ratio across the spectral dataset."
- [intro] The plugin covers data import, visualization, mean intensity calculation, region of interest (ROI) analysis, annotation with selected databases and pre-processing such as noise reduction and normalization.: "The plugin covers data import, visualization, mean intensity calculation, region of interest (ROI) analysis, annotation with selected databases and pre-processing such as noise reduction and"
- [readme] Users can choose their desired level of noise reduction (shown as a percentage) for their experiment.: "Users can choose their desired level of noise reduction (shown as a percentage) for their experiment."
- [readme] After pre-processing steps are chosen, click `Execute` and `Show true mean spectrum` to calculate the mean intensity.: "After pre-processing steps are chosen, click `Execute` and `Show true mean spectrum` to calculate the mean intensity."
- [readme] The figure shows the spectrum and image of the TIC normalization with 3% noise reduction and hotspot removal for the 99.9% quantile.: "The figure shows the spectrum and image of the TIC normalization with 3% noise reduction and hotspot removal for the 99.9% quantile."
