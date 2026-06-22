---
name: metabolomics-experiment-object-handling
description: Use when when converting raw metabolomics data from external formats (tab-delimited text, Sciex OS exports) into a unified R analysis environment, or when you have an existing SummarizedExperiment from another pipeline (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - xcms
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality_cq
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality_cq
schema_version: 0.2.0
---

# metabolomics-experiment-object-handling

## Summary

Create, validate, and manipulate SummarizedExperiment objects as the canonical data container for mzQuality metabolomics analyses. This skill bridges raw metabolomics data (tab-delimited or Sciex OS formats) into a structured R object that tracks compounds, samples, assays, and quality metrics throughout the analysis pipeline.

## When to use

When converting raw metabolomics data from external formats (tab-delimited text, Sciex OS exports) into a unified R analysis environment, or when you have an existing SummarizedExperiment from another pipeline (e.g., xcms) and need to adapt it to mzQuality's internal schema (with specified compound, aliquot, assay, and type columns). Use this skill as the first step after data import and before any quality control or batch correction analyses.

## When NOT to use

- Input data is already a validated SummarizedExperiment object with mzQuality-compliant internal structure and you intend only to read/subset it (use direct subsetting or accessor functions instead).
- You are performing quality control or batch correction—those operations require a pre-built SummarizedExperiment and are handled by `doAnalysis()`, not by this object-construction skill.
- Input file is missing mandatory columns (compound ID, aliquot ID, assay values, sample type) as `readData()` will reject it; ensure your source data is pre-formatted before attempting object construction.

## Inputs

- tab-delimited text file with mandatory columns: compound identifier, aliquot identifier, assay measurement columns, sample type label
- Sciex OS text export file
- data frame with columns for compound, aliquot, assay, and type
- existing SummarizedExperiment object from xcms or other R-based metabolomics pipelines

## Outputs

- SummarizedExperiment object with compound identifiers in rowData, sample metadata in colData, assay matrix in assays slot
- validated data structure ready for mzQuality downstream analysis

## How to apply

Call `readData()` on your input file to validate mandatory columns and check data format integrity; the function will flag missing or malformed entries. Then call `buildExperiment()` on the resulting data frame to construct a SummarizedExperiment object, specifying which columns correspond to compound identifiers, aliquots, assay measurements, and sample types (e.g., QC, Study Sample, Calibration Line, Blank). The resulting SummarizedExperiment becomes the canonical object passed to downstream mzQuality functions like `doAnalysis()`. If you have an existing SummarizedExperiment from xcms or similar tools, you can supply it directly to mzQuality; the package will internally validate that required metadata and assay slots match mzQuality's expectations. Verify the object by inspecting rowData (compound metadata), colData (sample metadata), and assay names to ensure all expected quality control columns (e.g., Internal Standard assignments, batch labels, known concentrations for calibration lines) are present and correctly mapped.

## Related tools

- **mzQuality** (R package providing readData() and buildExperiment() functions for SummarizedExperiment construction and validation in metabolomics QC workflows) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor S4 class used internally by mzQuality to store and organize compound, sample, and assay data with linked metadata)
- **xcms** (R-based metabolomics feature detection pipeline that produces SummarizedExperiment objects compatible with mzQuality input)

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality"); exp <- buildExperiment(readData(path))
```

## Evaluation signals

- rowData(exp) contains all compounds with correct identifiers and no missing values in mandatory columns (compound name, internal standard assignment if applicable)
- colData(exp) contains all samples with correct identifiers, batch labels, sample type assignments (QC/Study Sample/Calibration Line/Blank), and aliquot mappings
- assays(exp) slot contains at least one numeric matrix with dimensions matching number of compounds (rows) and samples (columns), with no NaN or Inf values in raw measurements
- Subsetting exp[rowData(exp)$use, exp$use] (after doAnalysis) yields a non-empty object, indicating that readData and buildExperiment correctly parsed and retained the data structure
- If calibration lines or known concentrations were supplied, colData(exp) contains a column with numeric concentration values and rowData(exp) can be used to match calibration compounds to study compounds

## Limitations

- readData() requires strict adherence to input format: mandatory columns must be named exactly as documented, and numeric assay columns must not contain text or missing values; non-compliant files will be rejected with informative error messages.
- SummarizedExperiment objects created by buildExperiment() store data in memory; large metabolomics studies (>10,000 samples or >5,000 compounds) may require significant RAM.
- If converting from xcms or other external SummarizedExperiment objects, you must manually verify that column names and metadata structure match mzQuality expectations (compound, aliquot, assay, type) or the subsequent doAnalysis() call may fail or produce incorrect results.
- The skill does not perform any quality filtering, outlier detection, or batch correction—these are separate downstream steps performed by doAnalysis() after object construction.

## Evidence

- [readme] readData and buildExperiment: "To use your own data, either a SummarizedExperiment or a tab-delimited text file can be used. See the vignette [Data input] for an explanation for the format and mandatory columns to be present."
- [readme] buildExperiment function creates SummarizedExperiment: "The function `buildExperiment` allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns"
- [readme] readData validation: "Once your files are ready, you can use the `readData` function to read in your data. It will check if all mandatory columns are present and if the data is in the correct format."
- [readme] xcms compatibility: "Alternatively, you can supply an already built *SummarizedExperiment* object to mzQuality. This is common when R-based metabolomics pipelines are used like *xcms*"
- [readme] Data import formats: "it features import of data from a variety of formats, including a generalized tab-delimited format and Sciex OS text exports"
- [readme] SummarizedExperiment as canonical object: "Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data"
