---
name: tab-delimited-metabolomics-file-parsing
description: Use when when you have raw metabolomics measurements in tab-delimited
  text format (e.g., from Sciex OS exports) and need to load them into R for quality
  control analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality is a user-friendly R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tab-delimited-metabolomics-file-parsing

## Summary

Parse tab-delimited metabolomics data files into validated data frames for downstream construction of SummarizedExperiment objects. This skill enforces mandatory column presence and data integrity before analyte ratio calculation and batch correction.

## When to use

When you have raw metabolomics measurements in tab-delimited text format (e.g., from Sciex OS exports) and need to load them into R for quality control analysis. Specifically, use this skill when your input file contains compound areas, internal standard areas, sample identifiers, sample type annotations, and aliquot/batch metadata, and you want to validate the structure before constructing a SummarizedExperiment object.

## When NOT to use

- Input is already a SummarizedExperiment object — pass it directly to downstream analysis functions like doAnalysis
- Input is in a binary format (mzML, NetCDF, HDF5) or already a processed feature matrix with ratios pre-computed
- Column names and structure do not match mzQuality's expected schema (compound name, sample name, area columns, sample type column)

## Inputs

- tab-delimited text file with mandatory columns: compound identifiers, sample identifiers, area measurements, internal standard area values, sample type labels, and batch/aliquot annotations
- Sciex OS text export format (alternatively supported)

## Outputs

- validated data frame with all mandatory columns present and integrity checks passed
- SummarizedExperiment object with rowData (compound metadata), colData (sample metadata), and assays including 'area' (primary), 'istd_area' (secondary), and 'ratio' (computed as primary/secondary)

## How to apply

Use the `readData` function to read the tab-delimited file and perform column validation and data integrity checks. The function verifies that all mandatory columns are present (compound identifiers, sample identifiers, area measurements, internal standard assignments, and sample type labels). The validated data frame is then passed to `buildExperiment`, which maps user-specified columns to row features (compounds), column metadata (samples), and assay matrices (compound area, internal standard area). The function automatically calculates the compound/internal standard ratio assay by dividing primary assay (compound area) by secondary assay (internal standard area), or assigns primary assay directly if no secondary assay is provided. Column mapping parameters in `buildExperiment` allow flexibility in naming conventions across different instrument vendors.

## Related tools

- **mzQuality** (Provides readData and buildExperiment functions for parsing and validating tab-delimited metabolomics data; core package for quality control of metabolomics studies) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor container class that stores parsed data, rowData (compound metadata), colData (sample metadata), and assay matrices (areas and ratios))
- **mzQualityDashboard** (Interactive Shiny application wrapper around mzQuality; recommended for users who prefer graphical interface to readData and buildExperiment workflows) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality"); combined <- readData(path); exp <- buildExperiment(combined)
```

## Evaluation signals

- No missing values in mandatory columns after readData execution; function returns without validation errors
- SummarizedExperiment object contains non-empty rowData and colData slots with expected column names (compound identifiers, sample identifiers, sample type, batch)
- Ratio assay is present and contains computed values matching the formula primary_assay / secondary_assay (or equals primary_assay if secondary is absent); no NaN or Inf values except where secondary assay is zero
- Number of rows (compounds) and columns (samples) in the SummarizedExperiment match the input file dimensions
- All sample types and batch labels from input are preserved in colData without loss or corruption

## Limitations

- Column names and structure must match mzQuality's expected schema; user must manually map non-standard column names using buildExperiment parameters
- Only one sample type can be used for calculating concentrations in the current version; this limitation will be addressed in a future version
- Data integrity checks in readData detect missing or incorrectly formatted columns but do not impute values; malformed rows must be manually corrected in the source file

## Evidence

- [other] Column validation and data integrity checks performed by readData: "This function will read in your data and check for any missing or incorrect columns."
- [other] buildExperiment maps user-specified columns to features, samples, and assays: "The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis."
- [intro] Ratio assay is computed as primary divided by secondary; secondary defaults to primary if not provided: "The function automatically calculates the compound/internal standard ratio for each sample and stores it in the 'ratio' assay, with the ratio computed as primary assay divided by secondary assay (or"
- [intro] buildExperiment constructs SummarizedExperiment with rowData, colData, and assays: "Inspect the returned SummarizedExperiment object to confirm presence of rowData (compound metadata), colData (sample metadata), and assays (including the computed 'ratio' assay derived from compound"
- [intro] Supported input formats include tab-delimited and Sciex OS text exports: "it features import of data from a variety of formats, including a generalized tab-delimited format and Sciex OS text exports."
- [intro] Mandatory column specification required for buildExperiment: "The function `buildExperiment` allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns"
