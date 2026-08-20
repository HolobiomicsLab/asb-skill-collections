---
name: msi-spectral-data-import
description: Use when use this skill at the start of any MSI analysis workflow when
  you have raw imzML files or vendor-specific MSI data that need to be loaded into
  napari-MSI-Explorer for visualization, mean intensity calculation, ROI analysis,
  or annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3209
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - napari
  - Python
  - MSI-Explorer
  techniques:
  - MS-imaging
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5c01513
  title: MSI-Explorer
evidence_spans:
- The MSI-Explorer napari plugin is a powerful tool designed for targeted biochemical
  annotations in MSI data.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MSI spectral data import

## Summary

Import mass spectrometry imaging (MSI) spectral data from imzML or vendor-specific formats into the napari plugin environment for downstream visualization and analysis. This is the foundational step that loads raw MSI spectra containing m/z values and intensity arrays across all pixels/samples.

## When to use

Use this skill at the start of any MSI analysis workflow when you have raw imzML files or vendor-specific MSI data that need to be loaded into napari-MSI-Explorer for visualization, mean intensity calculation, ROI analysis, or annotation. This is the mandatory entry point before any downstream processing (noise reduction, normalization, or database search) can occur.

## When NOT to use

- Input data is already pre-processed and loaded in memory as a Python data structure — use direct array import instead of file-based import.
- Data format is not imzML or supported vendor format — requires format conversion or alternative import pathway.

## Inputs

- imzML file (or vendor-specific MSI format)
- Associated binary mass spectrometry data file (for imzML: .ibd file)

## Outputs

- Loaded MSI spectral dataset in napari plugin environment
- Extracted m/z values and intensity arrays accessible to visualization and processing modules

## How to apply

Start napari and navigate to Plugins → MSI-Explorer. Click 'Load imzML' and select your imzML file. The plugin will extract m/z values and intensity arrays for all spectra in the dataset. If profile mode data is detected, a dialog will appear asking whether to convert to centroid mode; choose based on your analytical requirements. Once loaded, metadata can be viewed via 'View Metadata' to confirm correct import. The imported spectra are then available for visualization and all downstream workflow steps within the napari plugin framework.

## Related tools

- **napari** (Plugin host environment for interactive MSI data visualization and import interface) — https://github.com/napari/napari
- **MSI-Explorer** (napari plugin providing the imzML load interface and spectral data extraction workflow) — https://github.com/MMV-Lab/MSI-Explorer

## Evaluation signals

- imzML file loads without error and no exceptions are raised during spectral data extraction
- Metadata can be retrieved and displayed via 'View Metadata', confirming file format was correctly parsed
- m/z values and intensity arrays are present and non-empty for all pixels/samples in the dataset
- Spectral data can be visualized in napari without NaN or out-of-range values indicating import corruption
- Profile mode data is correctly detected and user is prompted for centroid conversion; conversion produces valid centroid spectra when accepted

## Limitations

- Only imzML and select vendor-specific MSI formats are supported; other formats require pre-conversion.
- Profile mode data import triggers a conversion dialog; user choice affects downstream peak detection and mean intensity calculations.
- Large imzML files may consume significant memory during import depending on pixel count and spectral resolution; no streaming or chunked import is documented.
- Import success depends on proper structure and validity of the imzML file and associated .ibd binary data file.

## Evidence

- [readme] Select imzML file using `Load imzML`.: "Select imzML file using `Load imzML`."
- [readme] Upon uploading profile mode data, a pop-up appears prompting you to convert it to centroid mode. Selecting `Yes` converts the data, while `No` keeps it in its original profile format.: "Upon uploading profile mode data, a pop-up appears prompting you to convert it to centroid mode. Selecting `Yes` converts the data, while `No` keeps it in its original profile format."
- [other] Load imported MSI spectral data (imzML or vendor-specific format) into the napari plugin environment via the MSI-Explorer data import interface.: "Load imported MSI spectral data (imzML or vendor-specific format) into the napari plugin environment via the MSI-Explorer data import interface."
- [other] Extract m/z values and intensity arrays for all spectra in the dataset.: "Extract m/z values and intensity arrays for all spectra in the dataset."
- [readme] Metadata can be checked by `View Metadata`.: "Metadata can be checked by `View Metadata`."
