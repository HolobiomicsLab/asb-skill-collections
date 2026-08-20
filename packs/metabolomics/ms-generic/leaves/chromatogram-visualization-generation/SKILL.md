---
name: chromatogram-visualization-generation
description: Use when after importing mass spectrometry data in .raw, .d, or mzXML format into R and before peak analysis or quality control steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - R GUI
  - R GUI (SMART)
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.5c03225
  title: SMART 2.0
evidence_spans:
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_smart_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03225
  all_source_dois:
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatogram-visualization-generation

## Summary

Generate total ion chromatogram (TIC) and mass spectrum visualizations from imported mass spectrometry data in R. This skill transforms raw ion intensity data across retention time and m/z dimensions into publication-ready plots for exploratory analysis and reporting.

## When to use

After importing mass spectrometry data in .raw, .d, or mzXML format into R and before peak analysis or quality control steps. Use this skill when you need to inspect the overall signal distribution across the run, verify data quality visually, or identify regions of interest for targeted analysis.

## When NOT to use

- When working with already-preprocessed feature tables or peak intensity matrices — visualization should occur on raw or minimally processed data to assess instrumental performance.
- When the goal is quantitative peak area extraction or identification — use peak analysis module instead.
- If mass spectrometry data has not yet been imported or format conversion has failed — resolve import errors first.

## Inputs

- Mass spectrometry data files (.raw, .d, or mzXML format)
- Imported mass spectrometry data in R environment
- Retention time range or scan indices (optional, for targeted mass spectra)

## Outputs

- TIC plot (intensity vs. retention time, image file)
- Mass spectrum plots (m/z vs. intensity, one or more image files)
- High-resolution image files suitable for downstream analysis and reporting

## How to apply

Load the imported mass spectrometry data into the R environment. Extract TIC data by aggregating ion intensities across all m/z values for each retention time point, then generate a plot with retention time on the x-axis and summed intensity on the y-axis. For mass spectra, select specific retention time points or scan ranges of interest, extract the m/z and intensity pairs, and generate plots displaying m/z values versus ion intensities. Export all visualizations as high-resolution image files. Verify that TIC shows expected chromatographic peaks and that mass spectra display characteristic fragment patterns for your sample type.

## Related tools

- **R** (Programming environment for data import, aggregation, and plotting of mass spectrometry data) — https://www.r-project.org
- **R GUI (SMART)** (User-friendly graphical interface for executing the Data Visualization module within the SMART workflow) — https://github.com/YuJenL/SMART

## Evaluation signals

- TIC plot displays a smooth intensity profile across the full retention time range with no missing or negative values.
- TIC peaks align with expected retention times for known reference standards or metabolites in the sample.
- Mass spectrum plots show m/z values > 0 and intensity values ≥ 0, with the base peak (highest intensity) clearly visible.
- Generated image files are high-resolution and suitable for inclusion in reports or publications.
- Retention time and intensity ranges on both axes match the original data dimensions (no truncation or scaling artifacts).

## Limitations

- Visualization quality depends on successful prior import of mass spectrometry data; corrupted or malformed .raw, .d, or mzXML files may not import correctly.
- Very large datasets (e.g., high-resolution or long-duration runs) may require optimization or subsetting to avoid memory constraints during aggregation.
- Manual selection of retention time points for targeted mass spectra introduces subjectivity; systematic or automated selection may be needed for consistency across large studies.
- No changelog documented for the SMART software, limiting visibility into visualization refinements or bug fixes across versions.

## Evidence

- [other] The Data Visualization module visually represents various types of data features including total ion chromatogram (TIC) and mass spectra.: "The Data Visualization module visually represents various types of data features including total ion chromatogram (TIC) and mass spectra."
- [other] 1. Load imported mass spectrometry data (supporting .raw, .d, and mzXML formats) into the R environment. 2. Extract and prepare TIC data by aggregating ion intensities across retention time. 3. Generate a TIC plot displaying intensity versus retention time. 4. Extract and prepare mass spectrum data for selected retention time points or scan ranges. 5. Generate mass spectrum plots displaying m/z values versus ion intensities. 6. Export all visualizations as high-resolution image files suitable for downstream analysis and reporting.: "Load imported mass spectrometry data (supporting .raw, .d, and mzXML formats) into the R environment. Extract and prepare TIC data by aggregating ion intensities across retention time. Generate a TIC"
- [readme] Data Visualization: Visually represent various types of data features (e.g., total ion chromatogram (TIC) and mass spectra): "Data Visualization: Visually represent various types of data features (e.g., total ion chromatogram (TIC) and mass spectra)."
- [readme] SMART written in R and R GUI has been developed as user-friendly software for integrated analysis of metabolomics data.: "SMART written in R and R GUI has been developed as user-friendly software for integrated analysis of metabolomics data."
