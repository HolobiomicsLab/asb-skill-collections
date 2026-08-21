---
name: mean-intensity-aggregation
description: Use when after importing imzML or vendor-specific MSI data into napari
  and visualizing the raw spectral dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - napari
  - Python
  - MSI-Explorer
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
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

# mean-intensity-aggregation

## Summary

Compute mean intensity values across all pixels in a mass spectrometry imaging (MSI) dataset by aggregating intensity arrays at each unique m/z value. This workflow step produces a representative mean spectrum and optionally exports it for downstream ROI analysis and metabolite annotation.

## When to use

Apply this skill after importing imzML or vendor-specific MSI data into napari and visualizing the raw spectral dataset. Use it when you need a global intensity profile across the entire MSI experiment to identify dominant m/z peaks, normalize intensity ranges, or generate a reference spectrum for region-of-interest (ROI) comparisons.

## When NOT to use

- Input MSI data has not been imported and loaded into the napari environment—perform data import first.
- You require intensity values for a single pixel or localized region only—use ROI selection instead.
- The dataset is already pre-aggregated into a mean spectrum; recalculating would be redundant.

## Inputs

- Imported MSI spectral dataset in imzML or vendor-specific format
- m/z values and intensity arrays from all pixels/samples
- Optional pre-processing parameters (noise reduction %, normalization method, hotspot removal quantile)

## Outputs

- Mean spectrum: m/z vs. mean intensity table
- CSV or HDF5 export file of aggregated mean intensities
- Mean spectrum visualization plot (optional)
- Image view of mean intensity distribution (optional)

## How to apply

Load the imported MSI spectral data (imzML or converted centroid format) into the MSI-Explorer napari plugin environment. Extract m/z values and their corresponding intensity arrays for all spectra in the dataset. For each unique m/z value across all pixels/samples, calculate the arithmetic mean of intensities at that m/z. Optionally apply pre-processing steps (noise reduction as a percentage threshold, normalization methods such as TIC, RMS, or reference peak, and hotspot removal at a quantile threshold like 99.9%) before mean calculation. Aggregate results into a structured m/z vs. mean intensity table and export as CSV or HDF5 for compatibility with downstream ROI analysis and annotation workflows.

## Related tools

- **napari** (Plugin framework environment for loading, visualizing, and processing MSI spectral data) — https://github.com/napari/napari
- **MSI-Explorer** (napari plugin that implements mean intensity calculation as a workflow step following data import and visualization) — https://github.com/MMV-Lab/MSI-Explorer
- **Python** (Programming language for arithmetic aggregation and export of mean intensity arrays)

## Evaluation signals

- Output table contains all unique m/z values present in the original dataset with no missing entries
- Each mean intensity value is the arithmetic average of intensities at that m/z across all pixels; spot-check by manual calculation on a subset
- Output file is valid CSV or HDF5 and is compatible with downstream ROI analysis and annotation tools
- Mean spectrum plot shows expected dominant peaks and relative intensity relationships consistent with the raw data distribution
- When pre-processing is applied, mean intensities reflect the specified noise reduction percentage, normalization method, and hotspot removal threshold

## Limitations

- Profile mode MSI data must be converted to centroid mode before processing; the plugin prompts for this conversion but cannot be circumvented
- Mean intensity calculation assumes all pixels have comparable sampling; highly uneven sampling or missing pixels may skew the aggregate
- Pre-processing steps (noise reduction, normalization, hotspot removal) are applied before aggregation; the order and parameters chosen will significantly affect the final mean spectrum
- Export format (CSV vs. HDF5) must be chosen appropriately for downstream tools; some tools may require specific formats

## Evidence

- [other] MSI-Explorer implements mean intensity calculation as a workflow step that processes imported MSI data following data import and visualization stages, operating within the napari plugin framework.: "MSI-Explorer implements mean intensity calculation as a workflow step that processes imported MSI data following data import and visualization stages, operating within the napari plugin framework."
- [other] For each unique m/z value across all spectra, calculate the arithmetic mean of intensities at that m/z across all pixels/samples.: "For each unique m/z value across all spectra, calculate the arithmetic mean of intensities at that m/z across all pixels/samples."
- [other] Aggregate results into a structured table (m/z vs. mean intensity) and save as a CSV or HDF5 file compatible with downstream ROI analysis and annotation workflows.: "Aggregate results into a structured table (m/z vs. mean intensity) and save as a CSV or HDF5 file compatible with downstream ROI analysis and annotation workflows."
- [readme] To calculate the mean spectrum, click on `Show true mean spectrum`. Clicking `Show image` will create an image view of the currently plotted data: "To calculate the mean spectrum, click on `Show true mean spectrum`. Clicking `Show image` will create an image view"
- [readme] After pre-processing steps are chosen, click `Execute` and `Show true mean spectrum` to calculate the mean intensity.: "After pre-processing steps are chosen, click `Execute` and `Show true mean spectrum` to calculate the mean intensity."
