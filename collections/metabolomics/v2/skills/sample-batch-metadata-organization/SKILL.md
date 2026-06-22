---
name: sample-batch-metadata-organization
description: Use when you have tab-delimited metabolomics data with columns for aliquot identifiers, compound names, peak areas (primary and internal standard), sample type (QC, study sample, calibration), batch labels, and injection times, and need to construct a single unified object for batch correction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3068
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
  - xcms
  techniques:
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-batch-metadata-organization

## Summary

Organizing metabolomics measurement data into a structured SummarizedExperiment object by mapping tab-delimited input columns to sample metadata (colData), compound metadata (rowData), and assay matrices. This skill enables downstream quality control and batch correction by establishing a unified data model that links measurements to their batch, injection order, and sample classification.

## When to use

You have tab-delimited metabolomics data with columns for aliquot identifiers, compound names, peak areas (primary and internal standard), sample type (QC, study sample, calibration), batch labels, and injection times, and need to construct a single unified object for batch correction, outlier detection, and quality filtering in mzQuality.

## When NOT to use

- Input data is already a properly formatted SummarizedExperiment object (skip directly to doAnalysis).
- Measurement data lacks mandatory columns (aliquot, compound, area, type, injection_time, batch) — readData will fail validation.
- Data originates from non-mass-spectrometry platforms or lacks internal standard measurements (ratio calculation will be uninformative).

## Inputs

- tab-delimited text file with columns: aliquot, compound, area, type (QC/Study/Calibration), injection_time, batch
- optionally: known concentrations for calibration line samples (for absolute quantitation)
- or pre-built SummarizedExperiment object from xcms or other R metabolomics pipelines

## Outputs

- SummarizedExperiment object with:
-   - rowData: compound metadata (names, internal standard assignments)
-   - colData: sample metadata (aliquot ID, batch, injection_time, type, use flag)
-   - assays: primaryAssay (compound areas), secondaryAssay (IS areas), ratio (compound/IS)

## How to apply

Use mzQuality's readData function to validate the input tab-delimited file for mandatory columns (aliquot, compound, area, type, injection_time, batch) and detect missing or malformed entries. Then call buildExperiment, specifying the aliquotColumn (sample identifier), compoundColumn (feature name), primaryAssay (compound peak area), and secondaryAssay (internal standard area). The function automatically deduces rowData from compound names and colData from aliquot metadata (batch, injection_time, type), and computes the compound/internal-standard ratio assay for each sample. Verify that the resulting SummarizedExperiment contains all expected assays (including the ratio), metadata layers, and that sample type and batch are correctly encoded in colData for subsequent filtering and visualization.

## Related tools

- **mzQuality** (R package providing readData and buildExperiment functions for data import, validation, and SummarizedExperiment construction) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor class for storing rectangular genomics/metabolomics data with row and column metadata; the core data structure used by mzQuality)
- **mzQualityDashboard** (Interactive Shiny application front-end for mzQuality, recommended for non-programmers to perform the same data import and QC workflow without R coding) — https://github.com/hankemeierlab/mzQualityDashboard
- **xcms** (R-based metabolomics peak detection pipeline that produces SummarizedExperiment objects compatible with mzQuality's buildExperiment workflow)

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality")
combined <- readData(path)
exp <- buildExperiment(combined)
```

## Evaluation signals

- readData returns a validated data frame with no missing or malformed entries in mandatory columns; validation report shows pass/fail for each column.
- buildExperiment returns a SummarizedExperiment with non-empty rowData (compound names) and colData (aliquot, batch, injection_time, type).
- Assay slot contains at least three matrices: primaryAssay (compound areas), secondaryAssay (internal standard areas), and ratio (automatically computed quotient); all have matching dimensions (n_compounds × n_samples).
- colData$use column exists and contains logical TRUE/FALSE flags (initialized based on user-specified or default thresholds); rowData$use similarly flags reliable compounds.
- Subset operation exp[rowData(exp)$use, exp$use] successfully extracts high-confidence compounds and samples without errors, confirming metadata integrity.

## Limitations

- Requires strict tab-delimited format with exact column names; Sciex OS text exports are supported but require pre-conversion.
- Internal standard assignments must be specified in advance (e.g., via an additional 'internalStandard' column); automatic recommendation occurs only after doAnalysis.
- Ratio calculation assumes all compounds have a defined internal standard; missing assignments will yield NaN or NA in the ratio assay.
- Data validation in readData does not correct systematic errors (e.g., batch label typos, misaligned injection times); user must clean input before buildExperiment.
- The resulting SummarizedExperiment does not yet include batch correction, outlier flags, or quality metrics; these require doAnalysis in the next workflow step.

## Evidence

- [other] readData function validation behavior: "readData, which performs validation of required columns (aliquot, compound, area, type, injection_time, batch) and checks for missing or incorrect entries"
- [other] buildExperiment function and SummarizedExperiment deduction: "buildExperiment deduces rowData and colData slots from compoundColumn and aliquotColumn, uses primaryAssay and secondaryAssay as compound and Internal Standard areas respectively, and automatically"
- [readme] Input format specification and tab-delimited requirement: "it features import of data from a variety of formats, including a generalized tab-delimited format and Sciex OS text exports"
- [readme] buildExperiment function usage: "The function `buildExperiment` allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns"
- [readme] Automated ratio assay computation: "Calculate the ratio between the compounds and assigned internal standards"
- [readme] Core data structure rationale: "This is the object that mzQuality uses to perform all calculations and analyses and is used throughout the package"
- [readme] Example usage with readData and buildExperiment: "path <- system.file("extdata", "example.tsv", package = "mzQuality"); exp <- buildExperiment(readData(path))"
