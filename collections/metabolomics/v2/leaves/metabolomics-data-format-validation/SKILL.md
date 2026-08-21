---
name: metabolomics-data-format-validation
description: Use when you have a tab-delimited metabolomics data file (raw measurement
  output from xcms, Sciex OS, or similar acquisition pipelines) and need to load it
  into mzQuality before building a SummarizedExperiment.
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
  - xcms
  - mzQualityDashboard
  techniques:
  - LC-MS
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

# metabolomics-data-format-validation

## Summary

Validate tab-delimited metabolomics input files for mandatory columns, data types, and completeness before constructing SummarizedExperiment objects. This skill ensures data integrity and early detection of format errors that would otherwise propagate through downstream QC analyses.

## When to use

Apply this skill when you have a tab-delimited metabolomics data file (raw measurement output from xcms, Sciex OS, or similar acquisition pipelines) and need to load it into mzQuality before building a SummarizedExperiment. The skill is essential before any quality control, batch correction, or internal standard recommendation steps can proceed—missing or malformed mandatory columns will halt downstream analysis.

## When NOT to use

- Input is already a SummarizedExperiment object that was not constructed by mzQuality—use direct conversion instead of readData.
- Data has already been validated and loaded by another pipeline (e.g., xcms output piped directly); re-validation adds no value.
- Input is in a proprietary binary format (e.g., .raw files from mass spectrometry instruments)—preprocessing to tab-delimited is required first.

## Inputs

- Tab-delimited text file with columns: aliquot, compound, area, type, injection_time, batch
- Optional: Sciex OS text export file
- Optional: pre-built SummarizedExperiment object for conversion to mzQuality format

## Outputs

- Validated data frame (if readData succeeds)
- Error messages or warnings identifying format violations (if validation fails)
- Ready-to-build input for buildExperiment function

## How to apply

Use the `readData` function in mzQuality to validate the input tab-delimited file. The function automatically checks for presence of all six mandatory columns (aliquot, compound, area, type, injection_time, batch), verifies their data types and ranges, and reports any missing or incorrect entries with clear error messages. If validation succeeds, `readData` returns a data frame suitable for passing to `buildExperiment`. The validation acts as a gatekeeper: it fails fast on schema violations rather than allowing silent data corruption downstream. Validation includes logical checks such as ensuring aliquot IDs are unique identifiers, area values are numeric and non-negative, type values match expected sample classifications (e.g., 'QC', 'Study Sample'), batch assignments are consistent, and injection times are ordered chronologically within batches.

## Related tools

- **mzQuality** (R package containing readData function for validation and buildExperiment for SummarizedExperiment construction) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor class that stores validated metabolomics data with assays, rowData (compound metadata), and colData (sample metadata))
- **xcms** (R-based metabolomics pipeline that can export tab-delimited output for mzQuality validation)
- **mzQualityDashboard** (Shiny application wrapper around mzQuality that provides GUI-based data import and validation without programming) — https://github.com/hankemeierlab/mzQualityDashboard

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality")
combined <- readData(path)
exp <- buildExperiment(combined)
```

## Evaluation signals

- readData returns a data frame with all six mandatory columns (aliquot, compound, area, type, injection_time, batch) present and no missing values in critical fields
- No error or warning messages are emitted by readData—validation passed cleanly
- All numeric columns (area, injection_time) contain valid numbers with no NaN, Inf, or negative area values; batch and type columns contain expected categorical values
- Returned data frame can be passed directly to buildExperiment without additional preprocessing or column renaming
- Row count and unique identifier counts (aliquots, compounds) match expectations from raw data source

## Limitations

- readData validates schema and basic data types but does not detect biological implausibilities (e.g., internal standard areas that are orders of magnitude smaller than expected; such detection requires domain-specific thresholds applied downstream by doAnalysis).
- Validation assumes tab-delimited format; other delimiters (comma, semicolon) will cause parsing failure unless the file is first converted.
- Missing values in mandatory columns cause validation to fail; mzQuality does not impute or interpolate missing measurements—the file must be corrected at the source.
- Validation does not cross-check consistency between aliquot, compound, and type assignments; duplicate sample-compound pairs or inconsistent type labels per aliquot may pass readData but create logical errors in QC calculations.

## Evidence

- [other] This function will read in your data and check for any missing or incorrect columns.: "This function will read in your data and check for any missing or incorrect columns."
- [other] mzQuality requires a specific format for the input data.: "mzQuality requires a specific format for the input data."
- [intro] it features import of data from a variety of formats, including a generalized tab-delimited format and Sciex OS text exports: "it features import of data from a variety of formats, including a generalized tab-delimited format and Sciex OS text exports"
- [readme] To get an idea of the capabilities of mzQuality, an example dataset containing 105 compounds and 584 samples has been added.: "To get an idea of the capabilities of mzQuality, an example dataset containing 105 compounds and 584 samples has been added."
- [readme] To use your own data, either a SummarizedExperiment or a tab-delimited text file can be used.: "To use your own data, either a SummarizedExperiment or a tab-delimited text file can be used."
