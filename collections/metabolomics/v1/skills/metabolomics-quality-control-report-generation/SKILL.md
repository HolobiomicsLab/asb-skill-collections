---
name: metabolomics-quality-control-report-generation
description: Use when after completing outlier detection, batch correction, and quality metric calculation on a SummarizedExperiment object using mzQuality's doAnalysis function, and after manually or automatically filtering compounds and samples using the 'use' column in rowData and colData.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality is a user-friendly R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality
schema_version: 0.2.0
---

# metabolomics-quality-control-report-generation

## Summary

Generate organized quality-control reports from mass spectrometry metabolomics data by creating structured directories containing publication-ready plots, tab-delimited tables, and Excel exports that categorize compounds and samples by confidence levels. This skill produces human-friendly and programmatic-access formats suitable for downstream analysis and stakeholder communication.

## When to use

After completing outlier detection, batch correction, and quality metric calculation on a SummarizedExperiment object using mzQuality's doAnalysis function, and after manually or automatically filtering compounds and samples using the 'use' column in rowData and colData. Apply this skill when you need to export results for peer review, archive analysis outputs with both visual and tabular evidence, or share processed data with collaborators who lack R expertise.

## When NOT to use

- Input SummarizedExperiment has not been processed by doAnalysis (missing required quality metrics in rowData/colData)
- User intends only programmatic data access and does not require visualizations or Excel exports
- Data is still undergoing iterative threshold tuning and does not warrant a final archived report

## Inputs

- SummarizedExperiment object with rowData and colData containing 'use' column (TRUE/FALSE)
- Assay matrix (typically 'area', 'ratio', or 'ratio_corrected' from doAnalysis output)
- Quality metrics in rowData (RSDQC, background percentage, presence values)
- Sample metadata in colData (batch, sample type, QC classifications)

## Outputs

- Parent directory containing report structure
- Plots subdirectory with HTML quality-control visualizations
- Reports subdirectory with tab-delimited text files (rowData.tsv, colData.tsv, assay-specific tables)
- Excel workbook (.xlsx) with multiple sheets for colData, rowData, and assays
- Confidence-level categorization tags for compounds

## How to apply

Call the createReports function on a filtered SummarizedExperiment object with parameters specifying report types (makeSummaryReport=TRUE, makeCompoundReport=TRUE) and quality thresholds (backgroundPercent, cautionRSD, nonReportableRSD). The function generates a parent directory containing two subdirectories: Plots (with HTML files of quality-control visualizations) and Reports (with tab-delimited rowData and colData, per-assay tables, and a consolidated Excel workbook). The function automatically categorizes compounds and samples into confidence tiers (High Confidence, Caution, Low SNR) based on the specified RSD and background thresholds, allowing stakeholders to interpret results according to risk tolerance without needing statistical training.

## Related tools

- **mzQuality** (Performs upstream outlier detection, batch correction, quality metric calculation, and filtering; createReports is the export step in the mzQuality pipeline) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Data structure used throughout mzQuality to store assays, rowData (compound metadata), and colData (sample metadata); required input format for createReports)
- **mzQualityDashboard** (Interactive Shiny application wrapper around mzQuality functions including createReports; provides GUI alternative for users without R programming experience) — https://github.com/hankemeierlab/mzQualityDashboard
- **R** (Language and runtime for executing createReports and all mzQuality package functions)

## Examples

```
exp <- exp[rowData(exp)$use, exp$use]; createReports(exp, makeSummaryReport=TRUE, makeCompoundReport=TRUE, backgroundPercent=40, cautionRSD=15, nonReportableRSD=30, assays='area')
```

## Evaluation signals

- Parent output directory exists and contains exactly two subdirectories: Plots and Reports
- Plots subdirectory contains HTML files with quality-control visualizations (aliquot plots, compound plots, PCA plots, violin plots) and no other file types
- Reports subdirectory contains at least colData.tsv, rowData.tsv, and one assay-specific tab-delimited file with correct column headers matching the input SummarizedExperiment
- An Excel workbook (.xlsx) is present in Reports with multiple sheets (one per assay, plus colData and rowData sheets) with no data truncation
- All compounds in Reports are annotated with confidence-level categories (High Confidence, Caution, Low SNR) consistent with the specified RSD and background thresholds
- The number of rows in exported rowData/assays equals the number of compounds with 'use'=TRUE in the input; similarly, number of colData rows equals samples with 'use'=TRUE

## Limitations

- In the current version of mzQuality, only one sample type can be used for calculating concentrations, limiting multi-matrix quantitative reports to a single reference sample class
- No versioning or audit trail is embedded in the report structure; users must manually document which parameter set (RSD, background percent) was used to generate each report
- Excel exports may encounter size limits or performance degradation with very large compound counts (>10,000) or sample counts (>10,000) depending on system memory

## Evidence

- [other] createReports generates expected directory structure with Plots and Reports subdirectories: "Verify that the output directory contains a Plots subdirectory with quality-control visualizations and a Reports subdirectory with tab-delimited text files and human-friendly Excel exports."
- [readme] Function creates HTML plots, tab-delimited files, and Excel files: "The function `createReports` will create a folder containing HTML files with plots, tab-delimited files containing the *colData*, *rowData*, and the various *assays*, and an Excel file that contains"
- [readme] Quality metrics are used to categorize confidence levels: "Based on the set thresholds, mzQuality distinguishes between `High Confidence`, `Caution`, `Low SNR`"
- [other] createReports accepts specific parameters for report types and thresholds: "Call the createReports function with the specified parameters (makeSummaryReport=TRUE, makeCompoundReport=TRUE, backgroundPercent=40, cautionRSD=15, nonReportableRSD=30, assays='area')."
- [readme] Compounds and samples are pre-selected using 'use' column before report generation: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is"
- [other] doAnalysis must be run before report generation: "Load a pre-processed SummarizedExperiment object created by buildExperiment and doAnalysis from the mzQuality package."
