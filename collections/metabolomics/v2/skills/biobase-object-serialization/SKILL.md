---
name: biobase-object-serialization
description: Use when when you have raw peak table data from mass spectrometry or other metabolomic instruments in either a standardized tabular format or one of 12 common software tool outputs (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Biobase
  - devtools
  - readr
  - R base functions
  - NOREVA
derived_from:
- doi: 10.1038/s41596-021-00636-9
  title: NOREVA
evidence_spans:
- '[![R >3.5](https://img.shields.io/badge/R-%3E3.5-success.svg)](https://www.r-project.org/)'
- BiocManager::install("Biobase")
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biobase-object-serialization

## Summary

Convert raw metabolomic peak tables from heterogeneous software formats into standardized Biobase ExpressionSet objects that serve as canonical input for downstream NOREVA preprocessing and assessment workflows. This serialization step ensures consistent representation of intensity matrices, sample metadata, and feature annotations across diverse analytical platforms.

## When to use

When you have raw peak table data from mass spectrometry or other metabolomic instruments in either a standardized tabular format or one of 12 common software tool outputs (e.g., XCMS, MZmine, MetaboAnalyst), accompanied by a label file that annotates samples with class membership or time-course information, and you need to feed this data into NOREVA assessment functions for preprocessing optimization.

## When NOT to use

- Input peak table is already in Biobase ExpressionSet format or another canonical R object structure
- Label file is missing or does not match the number of samples in the peak table
- Peak table is from a software tool not among the 12 supported platforms and cannot be coerced to standardized format

## Inputs

- Peak table (CSV format, either standardized or from 12 supported software tools)
- Label file (CSV with sample identifiers and class/time-course annotations)

## Outputs

- Biobase ExpressionSet object containing expression matrix, phenoData (sample metadata), and featureData (feature metadata)

## How to apply

Load the peak table CSV and label file using R base or readr functions, then validate the table structure by confirming the presence of required columns (sample identifiers and feature intensities) and matching row counts between peak table and label file. Construct a Biobase ExpressionSet object by assigning the intensity matrix to the expression slot, sample metadata (including class/time-series labels from the label file) to phenoData, and feature metadata to featureData. The resulting ExpressionSet object is then passed to downstream NOREVA functions (normulticlassqcall, nortimecourseqcall, etc.) for preprocessing pipeline evaluation. Format code '1' indicates the peak table is already in NOREVA's standardized format; format code '2' indicates conversion from one of the 12 supported software tool formats is required.

## Related tools

- **Biobase** (Construct ExpressionSet objects to encapsulate intensity matrices, phenoData, and featureData in a standardized container for downstream NOREVA functions) — https://bioconductor.org/packages/Biobase
- **readr** (Parse peak table and label CSV files efficiently with type safety)
- **R base functions** (Load and validate CSV peak tables and label files) — https://www.r-project.org/
- **NOREVA** (Provides PrepareInputFiles function that orchestrates the serialization workflow and accepts the resulting ExpressionSet as input for preprocessing assessment) — https://github.com/idrblab/NOREVA

## Examples

```
library(NOREVA); eset <- PrepareInputFiles(dataformat='2', rawdata='raw_peaks.csv', label='sample_labels.csv')
```

## Evaluation signals

- ExpressionSet object successfully instantiated with non-null expression matrix, phenoData, and featureData slots
- Expression matrix dimensions match peak table (rows = features, columns = samples) and phenoData row count equals number of samples
- Sample identifiers in phenoData match between peak table and label file with no mismatches or missing values
- Feature metadata (m/z, retention time, or other software-specific columns) preserved in featureData slot
- Downstream NOREVA assessment function (e.g., normulticlassqcall) accepts the ExpressionSet without error and completes workflow execution

## Limitations

- PrepareInputFiles only supports 12 predefined software formats; peak tables from other instruments or custom pipelines must be manually converted to standardized format before input
- Label file must exactly match the sample count and order in the peak table; no automatic reordering or merging is performed
- The function does not perform missing value imputation or quality control filtering; all preprocessing assessment is deferred to downstream NOREVA functions
- ExpressionSet serialization assumes samples are observations and features (metabolites) are variables; peak tables with transposed layouts require prior transformation

## Evidence

- [other] PrepareInuputFiles accepts a peak table in either standardized format (format code 1) or in formats generated by 12 available software tools (format code 2), along with a label file for time-course/multi-class studies, and produces a prepared input object for downstream NOREVA assessment functions.: "PrepareInuputFiles accepts a peak table in either standardized format (format code 1) or in formats generated by 12 available software tools (format code 2), along with a label file for"
- [other] Validate table structure, checking for required columns (sample identifiers, feature intensities) and matching row counts between peak table and labels.: "Validate table structure, checking for required columns (sample identifiers, feature intensities) and matching row counts between peak table and labels."
- [other] Construct an ExpressionSet object using Biobase, assigning intensity data to the expression matrix, sample metadata (including class/time-series labels) to phenoData, and feature metadata to featureData.: "Construct an ExpressionSet object using Biobase, assigning intensity data to the expression matrix, sample metadata (including class/time-series labels) to phenoData, and feature metadata to"
- [readme] This function enables the preparation and input of peak table which facilitate the subsequent application of other NOREVA functions.: "This function enables the preparation and input of peak table which facilitate the subsequent application of other NOREVA functions."
- [readme] "1" denotes the standardized format of peak table accepted by NOREVA; "2" denotes the customized format of peak table generated by 12 available software tools.: ""1" denotes the standardized format of peak table accepted by NOREVA; "2" denotes the customized format of peak table generated by 12 available software tools."
