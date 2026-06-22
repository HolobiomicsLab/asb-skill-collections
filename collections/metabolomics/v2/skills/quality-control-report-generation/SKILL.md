---
name: quality-control-report-generation
description: Use when after completing doAnalysis on an mzQuality SummarizedExperiment object with outlier detection, batch correction, and compound reliability filtering applied.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
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

# quality-control-report-generation

## Summary

Export analyzed metabolomics quality control results as organized project folders containing publication-ready plots, HTML reports, and tab-delimited data tables. This skill packages post-analysis SummarizedExperiment objects into structured reports that distinguish compounds by confidence level (High Confidence, Caution, Low SNR) and enable downstream programmatic access.

## When to use

After completing doAnalysis on an mzQuality SummarizedExperiment object with outlier detection, batch correction, and compound reliability filtering applied. Use this skill when you need to communicate results to non-R users, create publication-quality visualizations, or enable programmatic re-analysis of flagged compounds and samples in external software.

## When NOT to use

- Input SummarizedExperiment has not been processed through doAnalysis (missing outlier detection, batch correction, and reliability flags)
- You need to perform further interactive data inspection or sample/compound selection (use mzQualityDashboard Shiny application instead)
- Raw data has not yet been imported via readData and buildExperiment

## Inputs

- SummarizedExperiment object (post-doAnalysis, with batch correction and outlier detection applied)
- mzQuality experiment with rowData and colData populated by doAnalysis

## Outputs

- Project folder directory
- Plots subdirectory (exported visualizations)
- Reports subdirectory (HTML files with interactive results)
- Tab-delimited text files (colData, rowData, assays)
- Excel file (.xlsx) containing all data in single workbook

## How to apply

Call the createReports function on the analyzed experiment object, specifying makeSummaryReport=TRUE and makeCompoundReport=TRUE to enable both report types. The function creates a Project folder with two subdirectories: Plots (containing publication-ready visualizations) and Reports (containing HTML files with interactive results and tab-delimited text exports). The reports automatically stratify results by mzQuality's confidence classifications—High Confidence, Caution, and Low SNR—based on RSDQC, background signal percentage, and QC sample presence thresholds set during doAnalysis. Verify that all expected files are generated and that row and column metadata from the SummarizedExperiment are correctly represented in tab-delimited and Excel outputs for downstream integration.

## Related tools

- **mzQuality** (Core R package providing doAnalysis and createReports functions for metabolomics QC analysis and report generation) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor container object for storing assays, row metadata, and column metadata passed to createReports)
- **mzQualityDashboard** (Shiny application for interactive inspection and manual override of automatic selections before report generation) — https://github.com/hankemeierlab/mzQualityDashboard
- **R** (Runtime environment and scripting language for executing createReports and related mzQuality functions)

## Examples

```
exp <- doAnalysis(exp); createReports(exp, makeSummaryReport=TRUE, makeCompoundReport=TRUE, output_directory="./results")
```

## Evaluation signals

- Project folder exists at specified output directory with exactly two subdirectories: Plots and Reports
- Plots subdirectory contains visualizations (aliquot plots, compound scatter plots, PCA plots, violin plots) with no missing or truncated images
- Reports subdirectory contains HTML files with confidence-level stratification (High Confidence, Caution, Low SNR sections visible and populated)
- Tab-delimited files export complete rowData (compounds) and colData (samples) matching the SummarizedExperiment dimensions with no truncation
- Excel file successfully opens and contains all assays, rowData, and colData in separate sheets; no data corruption or missing values

## Limitations

- Report generation requires prior execution of doAnalysis; createReports does not re-run QC calculations
- HTML reports are static snapshots; interactive exploration requires mzQualityDashboard or manual reimport into R
- Tab-delimited exports may become large for high-dimensional datasets (many compounds × many samples); Excel files have cell limits (~1M rows)
- Confidence classifications (High Confidence, Caution, Low SNR) are based on fixed thresholds set during doAnalysis; manual override requires re-opening in R or the dashboard

## Evidence

- [other] createReports generates a Project folder organized into Plots and Reports subdirectories containing analysis results, including summary reports, compound reports, and tab-delimited text files for programmatic access.: "createReports generates a Project folder organized into Plots and Reports subdirectories containing analysis results, including summary reports, compound reports, and tab-delimited text files"
- [readme] The createReports function creates a folder containing HTML files with plots, tab-delimited files containing the colData, rowData, and the various assays, and an Excel file that contains all the data in a single file.: "The `createReports` function will create a folder containing HTML files with plots, tab-delimited files containing the *colData*, *rowData*, and the various *assays*, and an Excel file that contains"
- [intro] mzQuality provides a function to export the results of the analysis. The createReports function creates a folder containing the results.: "mzQuality provides a function to export the results of the analysis. The `createReports` function creates a folder containing the results"
- [other] Call createReports with the experiment object, setting makeSummaryReport=TRUE and makeCompoundReport=TRUE to enable both report types.: "Call createReports with the experiment object, setting makeSummaryReport=TRUE and makeCompoundReport=TRUE to enable both report types."
- [readme] Based on the set thresholds, mzQuality distinguishes between High Confidence, Caution, Low SNR reports.: "Based on the set thresholds, mzQuality distinguishes between `High Confidence`, `Caution`, `Low SNR`"
