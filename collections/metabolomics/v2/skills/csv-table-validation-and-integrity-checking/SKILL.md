---
name: csv-table-validation-and-integrity-checking
description: Use when you have received a raw peak table CSV (in either standardized format or output from metabolomic software tools like XCMS, MZmine, etc.) and a corresponding label file, and you need to confirm both files are well-formed and mutually consistent before passing them to NOREVA preprocessing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3577
  tools:
  - R
  - devtools
  - readr
  - Biobase
derived_from:
- doi: 10.1038/s41596-021-00636-9
  title: NOREVA
evidence_spans:
- '[![R >3.5](https://img.shields.io/badge/R-%3E3.5-success.svg)](https://www.r-project.org/)'
- '![installed with devtools](https://img.shields.io/badge/installed%20with-devtools-blueviolet.svg)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_noreva_cq
    doi: 10.1038/s41596-021-00636-9
    title: NOREVA
  dedup_kept_from: coll_noreva_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-021-00636-9
  all_source_dois:
  - 10.1038/s41596-021-00636-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CSV Table Validation and Integrity Checking

## Summary

Validate peak table CSV structure and metadata consistency before converting to standardized bioinformatic objects for downstream metabolomic analysis. This skill ensures that raw peak tables conform to required column schemas and match sample counts across intensity and label files.

## When to use

Apply this skill when you have received a raw peak table CSV (in either standardized format or output from metabolomic software tools like XCMS, MZmine, etc.) and a corresponding label file, and you need to confirm both files are well-formed and mutually consistent before passing them to NOREVA preprocessing pipelines or other downstream assessment functions.

## When NOT to use

- Input peak table is already loaded as an R ExpressionSet object or Biobase object; skip directly to preprocessing.
- Peak table is already in normalized or preprocessed form (e.g., already log-transformed or batch-corrected); validation is redundant and may mask prior processing steps.
- Label file is missing or not required (e.g., single-class or quality-control-only studies); validation of label–sample matching is inapplicable.

## Inputs

- Peak table CSV file (standardized format or software-generated format)
- Label file CSV (sample class/time-series annotations, one row per sample)

## Outputs

- Validated peak table structure (schema confirmed, dimensions logged)
- Validated label file structure (sample count matches peak table, no orphan labels)
- Validation report (pass/fail for each structural check)

## How to apply

Load the peak table and label CSV files using R base functions (read.csv) or readr package functions. Inspect the peak table for required columns: sample identifiers (column headers) and feature intensity columns (numeric matrix). Validate the label file structure and confirm row counts match between the intensity matrix and label assignments. Check for missing values, data type consistency (intensities should be numeric), and absence of duplicate sample or feature identifiers. Only after passing these structural and cardinality checks construct the ExpressionSet object for downstream NOREVA functions. The rationale is that malformed input—missing columns, row count mismatches, or non-numeric intensities—will cause silent failures or corruption in the ExpressionSet; early validation prevents wasted computation and ensures traceability of preprocessing decisions.

## Related tools

- **R** (Host language for data loading and validation logic using base functions (read.csv, str, nrow, ncol, colnames, is.numeric)) — https://www.r-project.org/
- **readr** (Alternative data loading library for robust CSV import with type inference and diagnostic messages)
- **Biobase** (Provides ExpressionSet class used to represent validated, structured peak table data post-validation) — https://bioconductor.org/packages/Biobase/

## Examples

```
# Load and validate peak table and label files before PrepareInputFiles
rawdata <- read.csv('peak_table.csv', row.names=1)
labels <- read.csv('labels.csv', row.names=1)
stopifnot(nrow(rawdata) == nrow(labels))
stopifnot(all(sapply(rawdata, is.numeric)))
cat('Validation passed:', nrow(rawdata), 'samples x', ncol(rawdata), 'features\n')
```

## Evaluation signals

- Peak table row count (samples) equals label file row count; no orphan or missing sample assignments.
- All intensity columns are numeric; no character or NA values in feature intensity matrix.
- Required columns present: sample identifiers and at least one feature intensity column.
- No duplicate sample identifiers or feature names within each file.
- ExpressionSet object successfully constructs from validated inputs without errors or coercion warnings.

## Limitations

- Validation checks structure and cardinality but do not assess biological plausibility (e.g., extreme intensity ranges, outlier samples, or batch effects are not flagged during validation).
- If peak table is in customized format (format code 2 from 12 software tools), format-specific column names and metadata structures must be inferred or manually specified; generic validation may miss tool-specific required fields.
- No cross-validation against external reference standards or QC samples; validation is local to the two input files only.

## Evidence

- [other] PrepareInuputFiles accepts a peak table in either standardized format (format code 1) or in formats generated by 12 available software tools (format code 2), along with a label file for time-course/multi-class studies.: "PrepareInuputFiles accepts a peak table in either standardized format (format code 1) or in formats generated by 12 available software tools (format code 2), along with a label file for"
- [other] Validate table structure, checking for required columns (sample identifiers, feature intensities) and matching row counts between peak table and labels.: "Validate table structure, checking for required columns (sample identifiers, feature intensities) and matching row counts between peak table and labels"
- [readme] This variable allows the user to specify the FORMAT of their input peak table. '1' denotes the standardized format of peak table accepted by NOREVA; '2' denotes the customized format of peak table generated by 12 available software tools.: "This variable allows the user to specify the FORMAT of their input peak table. '1' denotes the standardized format of peak table accepted by NOREVA; '2' denotes the customized format of peak table"
