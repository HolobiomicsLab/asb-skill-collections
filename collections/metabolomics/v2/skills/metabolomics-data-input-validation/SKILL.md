---
name: metabolomics-data-input-validation
description: Use when when importing a tab-delimited or Sciex OS text export metabolomics dataset into mzQuality, before building the SummarizedExperiment object.
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
  techniques:
  - LC-MS
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

# metabolomics-data-input-validation

## Summary

Validate tab-delimited metabolomics data files for mandatory column presence, correct format, and data integrity before constructing a SummarizedExperiment object. This upstream quality gate prevents malformed input from propagating through downstream quality control and analysis workflows in mzQuality.

## When to use

When importing a tab-delimited or Sciex OS text export metabolomics dataset into mzQuality, before building the SummarizedExperiment object. Use this skill whenever you have raw tabular peak-area data that may be missing required columns (aliquots, compounds, assay values) or contain format inconsistencies.

## When NOT to use

- Input is already a SummarizedExperiment object — use directly in downstream analysis without re-validation.
- Data has already been validated and assembled into a SummarizedExperiment in a prior step — skip to quality control metrics.
- Input is in a non-tabular format (e.g., mzML, NetCDF) — use appropriate mass spectrometry data parsing tools before tabular validation.

## Inputs

- tab-delimited text file (TSV) with columns for aliquot/sample identifier, compound name, compound area (primary assay), internal standard area (secondary assay), and sample type
- Sciex OS text export file
- data frame with mandatory metabolomics columns

## Outputs

- validated data frame with mandatory columns confirmed
- SummarizedExperiment object with rowData (compound metadata), colData (sample metadata), and assays (primary assay, secondary assay, computed ratio)

## How to apply

Use the `readData` function to load a tab-delimited input file; it performs automated checks for mandatory columns (sample identifiers, compound names, areas under the curve, internal standard areas, sample types) and validates data integrity. The function will reject or warn on missing columns before returning a validated data frame. After successful validation, pass the returned data frame to `buildExperiment`, which maps user-specified columns to a SummarizedExperiment's rowData (compounds), colData (samples), and assays (compound area, internal standard area, and computed ratio). Inspect the returned object's structure to confirm presence of all expected slots and computed ratio assay.

## Related tools

- **mzQuality** (provides readData and buildExperiment functions for validation and SummarizedExperiment construction) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor class that stores validated metabolomics data with compound metadata, sample metadata, and assays)
- **R** (runtime environment for executing readData and buildExperiment)

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality"); combined <- readData(path); exp <- buildExperiment(combined)
```

## Evaluation signals

- readData completes without warnings or errors and returns a data frame with all mandatory columns present
- buildExperiment successfully constructs a SummarizedExperiment with non-empty rowData (compound names), colData (sample names and types), and at least three assays (primary, secondary, ratio)
- Ratio assay values equal primary assay divided by secondary assay (or equal to primary assay if secondary assay defaulted to 1)
- Column mappings match the user-specified column names; inspect colnames of rowData and colData to confirm
- No missing or NA values in compound names, sample identifiers, or primary assay values; check for NA counts in the returned object

## Limitations

- Only one sample type can be used for calculating concentrations in the current version; this limitation will be addressed in a future version.
- readData does not validate biological plausibility of peak areas or detect impossible values (e.g., negative areas); only checks column presence and basic format integrity.
- secondaryAssay column is optional; when not provided, the ratio assay defaults to primary assay values (internal standard effect is negated).

## Evidence

- [readme] readData function checks for mandatory columns: "Read the file and check if all mandatory columns are present"
- [readme] buildExperiment maps columns to SummarizedExperiment slots: "The function `buildExperiment` allows you to create a *SummarizedExperiment* object from a data frame by specifying the following columns"
- [other] readData performs basic column validation and data integrity checks: "readData function, which performs basic checks on column integrity"
- [other] buildExperiment automatically calculates ratio assay: "The function automatically calculates the compound/internal standard ratio for each sample and stores it in the 'ratio' assay, with the ratio computed as primary assay divided by secondary assay"
- [readme] Tab-delimited and Sciex OS formats are supported: "it features import of data from a variety of formats, including a generalized tab-delimited format and Sciex OS text exports"
- [other] Secondary assay defaults to 1 when not provided: "When secondaryAssay is not provided to buildExperiment, its value defaults to 1, which negates the Internal Standard effect, making the ratio assay equal to the primary assay values"
