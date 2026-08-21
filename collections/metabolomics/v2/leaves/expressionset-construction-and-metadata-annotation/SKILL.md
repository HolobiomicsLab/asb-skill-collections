---
name: expressionset-construction-and-metadata-annotation
description: Use when after validating a peak table (either standardized format or
  software tool–generated format) and its corresponding label file, before applying
  any NOREVA assessment functions (normulticlassqcall, nortimecourseqcall, etc.).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - devtools
  - Biobase
  - readr
  - R base functions
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# expressionset-construction-and-metadata-annotation

## Summary

Construct a Biobase ExpressionSet object from validated peak table and label data, organizing feature intensities, sample metadata (class/time-series labels), and feature annotations into a unified data structure for downstream NOREVA preprocessing assessment. This bridges raw metabolomic peak tables into the standardized bioinformatic container required by NOREVA's multi-class and time-course evaluation functions.

## When to use

After validating a peak table (either standardized format or software tool–generated format) and its corresponding label file, before applying any NOREVA assessment functions (normulticlassqcall, nortimecourseqcall, etc.). Use this skill when you have intensity data, sample class/time-series assignments, and feature metadata that must be organized into a single, queryable object.

## When NOT to use

- Input peak table is already in ExpressionSet format or other Bioconductor S4 object structure
- Label file is missing or sample identifiers in peak table do not match label file rows
- Peak table structure is malformed (e.g., missing required columns, inconsistent data types, sample count mismatch with labels)

## Inputs

- CSV peak table (format 1: standardized NOREVA format, or format 2: software tool–generated format from 12 available tools)
- CSV label file (sample identifiers with corresponding class labels or time-course time points)
- Feature metadata (optional; feature names, m/z, retention time, or other annotations)

## Outputs

- Biobase ExpressionSet object containing expression matrix (features × samples), phenoData (sample metadata), and featureData (feature metadata)

## How to apply

Load the CSV peak table and label file using R base functions or readr. Validate table structure by checking for required columns (sample identifiers, feature intensities) and confirming row counts match between peak table and labels. Construct an ExpressionSet object from the Biobase package by assigning the intensity data matrix to the expression slot, sample metadata (including class/time-series labels) to phenoData, and feature metadata to featureData. Return the ExpressionSet as the prepared input object for NOREVA preprocessing pipelines. The ExpressionSet ensures consistent access to intensities, phenotypes, and annotations downstream.

## Related tools

- **Biobase** (Provides ExpressionSet class definition and constructor for unified storage of expression matrix, sample metadata, and feature annotations)
- **readr** (Loads CSV peak table and label file into R data frames with robust type inference)
- **R base functions** (Performs table validation, row/column operations, and metadata merging)

## Examples

```
library(Biobase); eset <- ExpressionSet(assayData=as.matrix(peak_table[,-1]), phenoData=AnnotatedDataFrame(label_df), featureData=AnnotatedDataFrame(feature_annotations))
```

## Evaluation signals

- ExpressionSet object is successfully created without errors; check class(object) == 'ExpressionSet'
- Expression matrix dimensions match input peak table: nrow(exprs(object)) == number of features, ncol(exprs(object)) == number of samples
- phenoData row names match sample identifiers in peak table; all class/time-series labels present in phenoData@data
- featureData row names match feature identifiers in peak table; no NA values in required annotation columns
- ExpressionSet passes downstream NOREVA function input validation (e.g., PrepareInuputFiles returns object without warnings)

## Limitations

- Requires exact row count and identifier match between peak table and label file; mismatches will cause construction failure
- Supports only 13 predefined peak table formats (1 standardized + 12 software tools); custom formats must be reformatted to one of these standards first
- Missing or inconsistent sample identifiers across peak table and labels will cause the ExpressionSet to be incomplete or unusable
- No direct support for internal standards (IS) metadata in ExpressionSet phenoData; IS information must be stored in featureData or external documentation

## Evidence

- [other] Construct an ExpressionSet object using Biobase, assigning intensity data to the expression matrix, sample metadata (including class/time-series labels) to phenoData, and feature metadata to featureData.: "Construct an ExpressionSet object using Biobase, assigning intensity data to the expression matrix, sample metadata (including class/time-series labels) to phenoData, and feature metadata to"
- [other] PrepareInuputFiles accepts a peak table in either standardized format (format code 1) or in formats generated by 12 available software tools (format code 2): "PrepareInuputFiles accepts a peak table in either standardized format (format code 1) or in formats generated by 12 available software tools (format code 2)"
- [other] Validate table structure, checking for required columns (sample identifiers, feature intensities) and matching row counts between peak table and labels.: "Validate table structure, checking for required columns (sample identifiers, feature intensities) and matching row counts between peak table and labels."
- [other] Load the CSV peak table and label file using R base functions or readr.: "Load the CSV peak table and label file using R base functions or readr."
- [other] Return the ExpressionSet as the prepared input object ready for NOREVA preprocessing pipelines.: "Return the ExpressionSet as the prepared input object ready for NOREVA preprocessing pipelines."
- [readme] This function enables the preparation and input of peak table which facilitate the subsequent application of other NOREVA functions.: "This function enables the preparation and input of peak table which facilitate the subsequent application of other NOREVA functions."
