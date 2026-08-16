---
name: r-bioconductor-summarizedexperiment-manipulation
description: Use when when converting raw metabolomics data (tab-delimited text files, Sciex OS exports) into a structured object for batch processing, or when you need to organize compound-level measurements (assays), sample metadata (colData), and feature annotations (rowData) in a single container that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality is a user-friendly R package
- The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data.
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

# R Bioconductor SummarizedExperiment Manipulation

## Summary

Create, populate, and modify Bioconductor SummarizedExperiment objects to store and organize multi-dimensional omics data (assays, row metadata, column metadata) for downstream quality control and statistical analysis. This skill is foundational for working with metabolomics and other -omics datasets in R pipelines.

## When to use

When converting raw metabolomics data (tab-delimited text files, Sciex OS exports) into a structured object for batch processing, or when you need to organize compound-level measurements (assays), sample metadata (colData), and feature annotations (rowData) in a single container that downstream analysis functions like mzQuality's doAnalysis or createReports expect.

## When NOT to use

- Input is already a SummarizedExperiment object and does not require re-building or column validation.
- Data is in a different Bioconductor container (e.g., MSnSet, ExpressionSet) that is not compatible with mzQuality's expected SummarizedExperiment schema.
- Raw instrument files (e.g., .raw, .d, .mzML) need peak-picking and feature detection first; buildExperiment expects pre-aligned, quantified data.

## Inputs

- Tab-delimited text file with mandatory columns (compound name, sample ID, assay values, sample type, internal standard assignment)
- Sciex OS text export
- Data frame with compound, sample, and assay columns
- Pre-built SummarizedExperiment object

## Outputs

- SummarizedExperiment object with assays (e.g., area, intensity, ratio, ratio_corrected)
- SummarizedExperiment object with updated rowData (compound-level metrics: RSDQC, background %, presence, use flag)
- SummarizedExperiment object with updated colData (sample-level metrics: outlier flags, batch, use flag)
- Subset SummarizedExperiment containing only reliable compounds and samples

## How to apply

First, read your input data (tab-delimited format or Sciex OS text export) using readData, which validates mandatory columns (compound identifiers, sample identifiers, assay values such as area or intensity, and sample-type annotations). Next, call buildExperiment to convert the validated data frame into a SummarizedExperiment object, which organizes compounds as rows, samples as columns, and measurements (area, intensity, ratio) as assays. Populate rowData with compound-level metadata (e.g., internal standard assignment, chemical properties) and colData with sample-level metadata (e.g., sample type, batch, QC status). After analysis steps (e.g., doAnalysis for batch correction and quality metrics), the object's rowData and colData slots are updated with calculated columns (e.g., 'use' flags for reliability, RSDQC values, background percentages). Use subsetting (e.g., exp[rowData(exp)$use, exp$use]) to select reliable compounds and samples before visualization or export.

## Related tools

- **mzQuality** (Package that requires SummarizedExperiment objects as input for outlier detection, batch correction, and quality metric calculation; doAnalysis populates assays and metadata slots.) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor core class used internally by mzQuality to store and access compound measurements, sample metadata, and assay data.)
- **mzQualityDashboard** (Shiny application that operates on SummarizedExperiment objects created and manipulated via buildExperiment and doAnalysis.) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality"); exp <- buildExperiment(readData(path)); exp <- doAnalysis(exp = exp); exp_filtered <- exp[rowData(exp)$use, exp$use]
```

## Evaluation signals

- SummarizedExperiment object dimensions match expected data: number of rows = number of compounds, number of columns = number of samples.
- assays() slot contains expected matrices with correct names (e.g., 'area', 'ratio', 'ratio_corrected'); all assays have identical dimensions.
- rowData() slot contains a DataFrame with one row per compound and columns for compound identifiers, internal standard assignment, and (after doAnalysis) calculated metrics (RSDQC, background %, presence, use flag).
- colData() slot contains a DataFrame with one row per sample and columns for sample metadata (sample ID, sample type, batch) and (after doAnalysis) outlier detection results and use flags.
- Subsetting operation exp[rowData(exp)$use, exp$use] produces a valid SummarizedExperiment with reduced dimensions and no NA values in the 'use' columns.

## Limitations

- buildExperiment requires specific mandatory columns in the input data frame; missing or incorrectly named columns will cause readData validation to fail.
- In the current version of mzQuality, only one sample type (e.g., calibration line or quality control) can be used for calculating absolute concentrations; multi-sample-type concentration calculations are not supported.
- SummarizedExperiment subsetting by the 'use' flag is manual; there is no automatic filtering function built into the object class itself, requiring users to remember the correct subsetting syntax.

## Evidence

- [intro] buildExperiment allows creation from a data frame with specified columns for compounds, samples, and assays: "The function `buildExperiment` allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns"
- [intro] mzQuality uses SummarizedExperiment as its core internal data structure: "Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data."
- [readme] readData validates input format and mandatory columns before buildExperiment: "Once your files are ready, you can use the `readData` function to read in your data. It will check if all mandatory columns are present and if the data is in the correct format."
- [readme] doAnalysis updates assay, rowData, and colData slots with calculated metrics: "All calculations will be added to the `assay`, `rowData` and `colData` slots of the experiment, or overwrite the values if they are already present."
- [readme] Subsetting using 'use' flag for reliable compounds and samples: "To retrieve the compounds and samples recommended by mzQuality, you can use the following code to subset the experiment: exp <- exp[rowData(exp)$use, exp$use]"
- [intro] Input data formats accepted: tab-delimited and Sciex OS text exports: "it features import of data from a variety of formats, including a generalized tab-delimited format and Sciex OS text exports."
- [other] Only one sample type can be used for concentration calculations in current version: "Note that in the current version of mzQuality, only one sample type can be used for calculating concentrations."
