---
name: msi-data-table-export
description: Use when after calculating mean intensity values across all spectra in an MSI dataset (or within a manually selected ROI), and you need to store the resulting m/z–intensity table in a portable format for downstream ROI analysis, database annotation, or external statistical pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3750
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msi-data-table-export

## Summary

Export mean intensity spectra and region-of-interest (ROI) derived m/z vs. intensity tables from MSI-Explorer as CSV or HDF5 files for downstream biochemical annotation and statistical analysis. This skill bridges napari-based MSI visualization and external analytical workflows.

## When to use

After calculating mean intensity values across all spectra in an MSI dataset (or within a manually selected ROI), and you need to store the resulting m/z–intensity table in a portable format for downstream ROI analysis, database annotation, or external statistical pipelines.

## When NOT to use

- If you need to export raw spectral data without aggregation (use data import/visualization export instead).
- If your MSI data is still in profile mode and has not been converted to centroid mode, as mean calculation requires discrete m/z bins.
- If you require real-time streaming of spectra during ongoing data acquisition rather than batch export of computed results.

## Inputs

- napari MSI layer with loaded imzML or vendor-specific mass spectrometry imaging data
- calculated mean intensity spectrum (array of m/z and intensity pairs)
- optional: user-drawn ROI mask (label layer)

## Outputs

- CSV file containing m/z vs. mean intensity table
- HDF5 file containing m/z vs. mean intensity table with metadata
- PNG export of spectrum plot (optional)

## How to apply

Following mean spectrum calculation in MSI-Explorer (via 'Show true mean spectrum'), click 'Export spectrum data' to serialize the plotted m/z vs. intensity table as a CSV file; alternatively, select the HDF5 format for compatibility with complex hierarchical metadata. For ROI-specific exports, first define the ROI using the brush and label tools, calculate the ROI mean spectrum via 'Calculate ROI mean spectrum', then export. The exported table contains columns for m/z values and their corresponding arithmetic mean intensities; verify row count matches the number of unique m/z values detected across the dataset.

## Related tools

- **napari** (Plugin host and visualization framework for interactive MSI layer display and ROI selection prior to export) — https://github.com/napari/napari
- **MSI-Explorer** (napari plugin that implements mean intensity calculation, ROI workflow, and CSV/HDF5 export functionality) — https://github.com/MMV-Lab/MSI-Explorer
- **Python** (Runtime environment for MSI-Explorer and CSV/HDF5 I/O libraries (csv, h5py))

## Evaluation signals

- Exported CSV/HDF5 file exists and is readable by standard data analysis tools (pandas, R data.frame).
- Row count in exported table equals the number of unique m/z values detected across all spectra in the dataset.
- Column headers are present and labeled 'm/z' and 'mean_intensity' (or equivalent); no missing or NaN values in m/z column.
- For ROI exports: row count is less than or equal to the full dataset table; intensity values are non-negative and within expected range for the normalization method applied.
- File timestamp and size are consistent with the scale of the input MSI dataset (e.g., 1000–100,000 m/z bins × 4–8 bytes per value).

## Limitations

- Export does not include uncertainty/variance estimates for individual m/z mean intensities; only point estimates are stored.
- CSV export is human-readable but lacks schema metadata; HDF5 is recommended for large datasets or when provenance tracking is critical.
- ROI export requires manual selection via napari brush; automated ROI definition is not supported by this export skill alone.
- Export inherits all preprocessing applied before mean calculation (noise reduction, normalization, hotspot removal); no option to export raw vs. processed side-by-side in a single file.

## Evidence

- [other] For each unique m/z value across all spectra, calculate the arithmetic mean of intensities at that m/z across all pixels/samples. Aggregate results into a structured table (m/z vs. mean intensity) and save as a CSV or HDF5 file compatible with downstream ROI analysis and annotation workflows.: "Aggregate results into a structured table (m/z vs. mean intensity) and save as a CSV or HDF5 file compatible with downstream ROI analysis and annotation workflows."
- [readme] To export the plotted data as .csv file, click `Export spectrum data`. To save the spectrum plot as image, click `Export spectrum plot`.: "To export the plotted data as .csv file, click `Export spectrum data`."
- [readme] To select the ROI, click on `Select ROI for mean spectrum`. Adjust the brush size and label color. You can fill the area by using paint icon. Then click on the `Calculate ROI mean spectrum`. You can export as `.csv` file by using `Export spectrum data`.: "Then click on the `Calculate ROI mean spectrum`. You can export as `.csv` file by using `Export spectrum data`."
- [intro] It covers data import, visualization, mean intensity calculation, region of interest (ROI) analysis, annotation with selected databases and pre-processing such as noise reduction and normalization.: "It covers data import, visualization, mean intensity calculation, region of interest (ROI) analysis, annotation with selected databases and pre-processing such as noise reduction and normalization."
