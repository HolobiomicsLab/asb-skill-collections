---
name: compound-metric-tabulation
description: Use when after completing doAnalysis on a SummarizedExperiment object
  with mzQuality, when you need to share compound-level metrics with non-R users,
  integrate results into downstream reporting systems, or perform meta-analyses across
  multiple metabolomics experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3520
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - mzQualityDashboard
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- The `buildExperiment` function will then take the data and create an experiment
  object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store
  the data
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-metric-tabulation

## Summary

Export quality control metrics and assay values for all compounds into tab-delimited and Excel files after mzQuality analysis. This skill enables programmatic access to batch-corrected ratios, RSDQC, background signal percentages, matrix effects, and presence/concentration data for downstream reporting and integration.

## When to use

After completing doAnalysis on a SummarizedExperiment object with mzQuality, when you need to share compound-level metrics with non-R users, integrate results into downstream reporting systems, or perform meta-analyses across multiple metabolomics experiments. Specifically triggered when makeSummaryReport or makeCompoundReport flags are set to TRUE in createReports.

## When NOT to use

- If the experiment object has not yet been processed with doAnalysis — metrics such as RSDQC, batch correction, and background signal will not be available.
- If you only need interactive visualization of results — use the mzQualityDashboard Shiny application instead for exploratory browsing without file export.
- If the dataset contains no QC samples — mzQuality cannot calculate batch-corrected ratios or RSDQC, making compound reports incomplete.

## Inputs

- SummarizedExperiment object (result of doAnalysis with outlier detection, batch correction, and quality metrics calculated)
- Boolean flags: makeSummaryReport, makeCompoundReport
- Output directory path

## Outputs

- Project folder containing Reports subdirectory
- Tab-delimited text files (rowData, colData, assays: ratio, ratio_corrected, background_signal_pct, matrix_effect, median_area, presence, concentration, R2)
- Excel workbook (.xlsx) with all data in separate sheets
- HTML summary and compound reports (when enabled)

## How to apply

Call createReports on the analyzed experiment object (result of doAnalysis) with makeSummaryReport=TRUE and makeCompoundReport=TRUE to generate tab-delimited text files and an Excel workbook. The function exports rowData (compound annotations and metrics) and all assays (ratio, ratio_corrected, background signal percentage, matrix effect, median area, presence, concentration if calibration lines were supplied, and R² values) into separate sheets. The exported files are organized into a Project folder with Reports subdirectory. Verify that tab-delimited files are readable in spreadsheet applications and that all calculated metrics (RSDQC, background %, matrix effect, presence) are present for each compound. Subset the experiment to include only compounds and samples marked use=TRUE in rowData and colData before export to ensure only reliable results are reported.

## Related tools

- **mzQuality** (Core R package that calculates metrics (RSDQC, batch correction, background signal, matrix effect) and provides createReports function for tabulation export) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor data structure that stores compound metrics in rowData, sample metadata in colData, and assay matrices (ratio, ratio_corrected, etc.)) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **R** (Statistical computing environment in which mzQuality and createReports are executed)
- **mzQualityDashboard** (Shiny-based GUI alternative for interactive viewing and export without requiring R scripting) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
exp <- doAnalysis(exp); createReports(exp, path='output_dir', makeSummaryReport=TRUE, makeCompoundReport=TRUE)
```

## Evaluation signals

- Project folder created in specified output directory with Reports subdirectory present
- Tab-delimited files are readable and contain expected columns: compound identifiers, RSDQC values, background signal percentages, matrix effect, median area, presence counts, and (if calibration supplied) concentrations and R² values
- Excel file contains separate sheets for rowData, colData, and each assay (ratio, ratio_corrected, background_signal_pct, matrix_effect, median_area, presence, concentration, R2) with matching row/column counts to the original SummarizedExperiment
- Number of rows in exported compound files equals number of TRUE entries in rowData$use; number of columns in exported sample files equals number of TRUE entries in colData$use
- Batch-corrected ratio values (ratio_corrected assay) show lower variance than uncorrected ratios in QC samples, confirming batch correction was applied before export

## Limitations

- Tab-delimited format may have issues with special characters or very large datasets; Excel format has row limit (~1 million rows) for some versions.
- Concentrations and R² values are only exported if calibration line samples with known concentrations were supplied during doAnalysis; otherwise those columns will be absent.
- createReports exports the entire filtered experiment; no in-situ filtering of compounds by RSDQC threshold or presence threshold is possible — pre-filter via rowData$use subsetting before calling createReports.
- The exported tab-delimited files contain no markdown or formatting; all visualization context (plots, HTML annotations) resides in the parallel Plots subdirectory and HTML reports, not in the tabular exports.

## Evidence

- [other] Generates a Project folder organized into Plots and Reports subdirectories containing analysis results, including summary reports, compound reports, and tab-delimited text files for programmatic access.: "createReports generates a Project folder organized into Plots and Reports subdirectories containing analysis results, including summary reports, compound reports, and tab-delimited text files for"
- [readme] createReports creates a folder containing HTML files with plots, tab-delimited files containing the colData, rowData, and the various assays, and an Excel file that contains all the data in a single file.: "createReports will create a folder containing HTML files with plots, tab-delimited files containing the *colData*, *rowData*, and the various *assays*, and an Excel file that contains all the data in"
- [other] Call createReports with the experiment object, setting makeSummaryReport=TRUE and makeCompoundReport=TRUE to enable both report types.: "Call createReports with the experiment object, setting makeSummaryReport=TRUE and makeCompoundReport=TRUE to enable both report types."
- [readme] The doAnalysis function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality control samples (SQC), 3. Calculate the percentage of background signal compared to the study samples, 4. Calculate the matrix effect, 5. Calculate the ratio of the QC sample, 6. Calculate the presence of the compounds in the samples, 7. Calculate the median area of the compounds in the samples, 8. Suggest Internal Standards based on the calculated values.: "The `doAnalysis` function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality"
- [readme] mzQuality adds a column called use in both the rowData and colData slots of the SummarizedExperiment. These contain either a TRUE or FALSE value, indicating if the compound or sample is reliable for reporting based on the set thresholds.: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is"
