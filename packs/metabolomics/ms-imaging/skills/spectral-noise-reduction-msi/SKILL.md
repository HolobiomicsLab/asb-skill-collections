---
name: spectral-noise-reduction-msi
description: Use when you have imported raw MSI spectral data in imzML format and observe high background noise or low signal-to-noise ratio that would obscure biochemical annotations or ROI analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
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

# spectral-noise-reduction-msi

## Summary

Remove background signal and improve signal-to-noise ratio from mass spectrometry imaging (MSI) spectra by applying configurable noise reduction filtering before downstream analysis. This preprocessing step enhances peak definition and data quality in imzML-format MSI datasets.

## When to use

Apply this skill when you have imported raw MSI spectral data in imzML format and observe high background noise or low signal-to-noise ratio that would obscure biochemical annotations or ROI analysis. Use it as the first preprocessing step before intensity normalization, database searching, or ROI-based mean spectrum calculation.

## When NOT to use

- Data is already in centroid mode and has been preprocessed by an earlier tool or workflow—verify with metadata first
- Noise reduction is not desired (e.g., preserving weak metabolite peaks for exploratory analysis in a discovery study)
- The input is a feature table or summary spectrum rather than raw pixel-by-pixel spectral data

## Inputs

- imzML file (profile or centroid mode MSI data)
- Imported MSI spectral dataset loaded in napari

## Outputs

- Noise-reduced MSI spectra in standardized format compatible with downstream visualization
- Cleaned spectral dataset ready for intensity normalization and ROI analysis

## How to apply

Load the imzML file into MSI-Explorer via the napari plugin. In the pre-processing panel, select a noise reduction level expressed as a percentage (e.g., 3%) that balances noise suppression against loss of weak but genuine peaks. The noise reduction filter removes background signal across all pixels and m/z values in the spectral dataset. Execute the preprocessing step and verify the result by computing and visualizing the mean spectrum to confirm that noise is reduced while peaks of interest remain intact. Optionally combine with normalization methods (TIC, RMS, median, or reference peak) and hotspot removal (99.99% quantile threshold) in a single preprocessing pipeline before exporting the cleaned spectra.

## Related tools

- **napari** (Interactive viewer and plugin host for MSI data visualization and preprocessing interface) — https://github.com/napari/napari
- **MSI-Explorer** (Napari plugin that wraps noise reduction filtering and provides UI for parameter selection and pipeline execution) — https://github.com/MMV-Lab/MSI-Explorer

## Evaluation signals

- Mean spectrum computed after preprocessing shows suppressed baseline and enhanced peak prominence compared to unfiltered data
- Signal-to-noise ratio (peak height / RMS background) increases visibly in the spectrum plot after filtering
- Hotspot removal (if applied) eliminates outlier pixels while preserving biological signal distribution in ion images
- Exported spectrum data shows consistent intensity values across pixels after noise reduction, indicating successful filtering
- ROI analysis on preprocessed spectra yields cleaner, more interpretable mean spectra with reduced spurious peaks

## Limitations

- Noise reduction is destructive and cannot be fully reversed; choice of percentage threshold (e.g., 3%) is empirical and dataset-dependent
- Very aggressive noise reduction (high percentages) may eliminate weak but genuine metabolite signals
- Profile-mode data must be converted to centroid mode before or during preprocessing; this conversion is irreversible
- No guidance provided in the README for selecting optimal noise reduction percentage for a given sample type or mass range

## Evidence

- [other] Apply noise reduction filtering to remove background signal and improve signal-to-noise ratio across the spectral dataset.: "Apply noise reduction filtering to remove background signal and improve signal-to-noise ratio across the spectral dataset."
- [readme] Users can choose their desired level of noise reduction (shown as a percentage) for their experiment.: "Users can choose their desired level of noise reduction (shown as a percentage) for their experiment."
- [readme] The pre-processing capabilities of MSI-Explorer enhance data quality and prepare MSI data for downstream analysis. Pre-processing steps involve: noise reduction: "The pre-processing capabilities of MSI-Explorer enhance data quality and prepare MSI data for downstream analysis. Pre-processing steps involve: noise reduction"
- [intro] It covers data import, visualization, mean intensity calculation, region of interest (ROI) analysis, annotation with selected databases and pre-processing such as noise reduction and normalization.: "It covers data import, visualization, mean intensity calculation, region of interest (ROI) analysis, annotation with selected databases and pre-processing such as noise reduction and normalization."
