---
name: bioconductor-object-structure-inspection
description: Use when after constructing a SummarizedExperiment object from raw metabolomics data via buildExperiment, or after batch correction and ratio computation steps, inspect rowData, colData, and assays slots to verify that compound identities, sample annotations, and computed assay values (primary.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3172
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bioconductor-object-structure-inspection

## Summary

Inspect and validate the internal structure of a Bioconductor SummarizedExperiment object to confirm correct assignment of row metadata (compounds), column metadata (samples), and assay matrices (e.g., compound areas, internal standard areas, computed ratios). This skill ensures data integrity and proper slot population before downstream quality control analyses.

## When to use

After constructing a SummarizedExperiment object from raw metabolomics data via buildExperiment, or after batch correction and ratio computation steps, inspect rowData, colData, and assays slots to verify that compound identities, sample annotations, and computed assay values (primary assay, secondary assay, ratio) are correctly assigned and contain expected numeric ranges or metadata fields.

## When NOT to use

- Input is already a validated, pre-processed SummarizedExperiment with confirmed internal structure and no newly computed assays.
- Working with non-Bioconductor data structures (e.g., plain data frames, matrix objects) that do not have rowData/colData/assays slots.
- Quality control filtering has already been applied and the object's dimensions and slot contents are known and immutable.

## Inputs

- SummarizedExperiment object
- Tab-delimited input file (e.g., example.tsv with compound, sample, area, internal standard area columns)

## Outputs

- Validated SummarizedExperiment with confirmed rowData (compound metadata), colData (sample metadata), and assays (ratio, area, batch-corrected variants)
- Diagnostic report confirming presence and ranges of assay values

## How to apply

Load the SummarizedExperiment object constructed from a tab-delimited input file (e.g., example.tsv) using readData() and buildExperiment(). Access the rowData slot to confirm presence of compound-level metadata and identifiers; access colData to confirm sample-level metadata (sample names, sample types, batch assignments); access the assays slot to verify named assays such as 'ratio' (computed as primary assay / secondary assay), 'area' (raw compound signals), and any batch-corrected variants. Check that the ratio assay contains numeric values for all samples and that no missing or infinite values appear unless explicitly filtered. This structural inspection should occur before filtering, outlier detection, or plotting to catch data transformation errors early.

## Related tools

- **SummarizedExperiment** (Core Bioconductor container class storing metabolomics assay data, row (compound) metadata, column (sample) metadata, and experimental assays (area, ratio, batch-corrected values)) — https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html
- **mzQuality** (R package providing readData() and buildExperiment() functions to construct and populate SummarizedExperiment objects from tab-delimited metabolomics files, and providing inspection and QC analysis capabilities) — https://github.com/hankemeierlab/mzQuality
- **R** (Programming language and environment for executing readData(), buildExperiment(), and accessor functions (rowData(), colData(), assays()) to inspect object structure)

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality"); exp <- buildExperiment(readData(path)); rowData(exp); colData(exp); assays(exp)
```

## Evaluation signals

- rowData contains a row for each compound with unique identifiers and no missing values in key metadata columns.
- colData contains a row for each sample with sample names, sample types, and batch assignments matching the input file dimensions.
- assays() slot returns a named list; 'ratio' assay exists and contains numeric values (no NA or Inf unless explicitly filtered); ratio values equal primary assay / secondary assay for each sample.
- Dimensions of rowData match the number of compounds (nrow); dimensions of colData match the number of samples (ncol); all assays have dimensions matching rowData and colData.
- No Inf or NaN values appear in the ratio assay unless secondary assay values are zero (which should be documented or filtered); ratio values fall within expected range for the metabolomics study (e.g., positive, non-zero).

## Limitations

- The current version of mzQuality supports only one sample type for calculating absolute concentrations; multiple sample types in colData will not all contribute to concentration modeling.
- Missing or malformed columns in the input tab-delimited file will cause readData() to fail validation; column names and types must match the documented mandatory format exactly.
- If secondary assay (internal standard area) contains zero values, the computed ratio assay will contain Inf; users must handle or filter such cases explicitly.

## Evidence

- [other] The buildExperiment function constructs a SummarizedExperiment object from a data frame by mapping user-specified columns to compound names, sample names, primary assay (compound area), secondary assay (internal standard area), and sample types.: "The buildExperiment function constructs a SummarizedExperiment object from a data frame by mapping user-specified columns to compound names, sample names, primary assay (compound area), secondary"
- [other] The function automatically calculates the compound/internal standard ratio for each sample and stores it in the 'ratio' assay, with the ratio computed as primary assay divided by secondary assay.: "The function automatically calculates the compound/internal standard ratio for each sample and stores it in the 'ratio' assay, with the ratio computed as primary assay divided by secondary assay (or"
- [other] Inspect the returned SummarizedExperiment object to confirm presence of rowData (compound metadata), colData (sample metadata), and assays (including the computed 'ratio' assay derived from compound and internal standard areas).: "Inspect the returned SummarizedExperiment object to confirm presence of rowData (compound metadata), colData (sample metadata), and assays (including the computed 'ratio' assay derived from compound"
- [readme] readData function will read in your data and check for any missing or incorrect columns.: "This function will read in your data and check for any missing or incorrect columns."
- [readme] The buildExperiment function will then take the data and create an experiment object that can be used for analysis.: "The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis."
- [readme] See here for an overview on a SummarizedExperiment.: "See [here](https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html) for an overview on a SummarizedExperiment."
