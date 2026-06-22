---
name: excel-file-parsing-for-metabolomics
description: 'Use when you have a preprocessed LC-MS peak table exported from peak-picking software (e.g., MS-DIAL) in Excel format with three logical compartments: sample annotation (rows), feature annotation (columns), and abundance matrix (numeric values).'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - notame
  - R
  - Biobase
  - ExpressionSet
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor'
- '```MetaboSet``` objects are the primary data structure of this package. ```MetaboSet``` is built upon the ```ExpressionSet``` class'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_notame_cq
    doi: 10.3390/metabo10040135
    title: notame
  dedup_kept_from: coll_notame_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo10040135
  all_source_dois:
  - 10.3390/metabo10040135
  - 10.1093/bioinformatics/btr597
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# excel-file-parsing-for-metabolomics

## Summary

Parse LC-MS peak tables from Excel spreadsheets (e.g., MS-DIAL output) into R and construct MetaboSet objects with properly annotated Feature_ID identifiers, sample metadata, and feature annotations. This is the foundational step in the notame workflow that converts raw peak-picking output into a structured, queryable data object for downstream preprocessing and analysis.

## When to use

You have a preprocessed LC-MS peak table exported from peak-picking software (e.g., MS-DIAL) in Excel format with three logical compartments: sample annotation (rows), feature annotation (columns), and abundance matrix (numeric values). You need to ingest this data into R as a MetaboSet object to apply notame's preprocessing functions (drift correction, missing value imputation, batch correction, QC flagging).

## When NOT to use

- Input data is not in Excel format or does not follow MS-DIAL layout conventions (three compartments: sample annotation, feature annotation, abundance matrix).
- Excel file lacks obligatory columns: Injection_order (numeric, unique) in samples; Mass or Average_mz and one of {Retention time, RetentionTime, Average_rt(min), rt} in features.
- Data has already been read into R as a separate matrix, data frame, and annotation pair; use construct_metabosets() directly instead.

## Inputs

- Excel spreadsheet (.xlsx) with MS-DIAL peak table output or equivalent format
- Sheet number (integer) and corner coordinates (row, column) specifying the location of the Ion Mode label
- Column names for split_by (e.g., 'LC_column', 'Ion_mode') or a single name string if unimodal

## Outputs

- MetaboSet object (or list of MetaboSet objects, one per ionization mode)
- ExpressionSet with exprs slot containing feature abundance matrix (features × samples)
- Feature data (fData) with Feature_ID, mass, retention time, and all parsed feature annotations
- Phenotype data (pData) with Sample_ID, Injection_order, QC status, and all parsed sample metadata

## How to apply

Load the notame package and call read_from_excel() with the Excel file path, sheet number, and corner coordinates (row and column where the 'Ion Mode' label is located) to automatically parse the three data compartments. Specify split_by columns (typically LC column and ionization mode) so the function generates a Split field that will be incorporated into Feature_ID; alternatively supply a single name argument if the file contains only one mode. Verify that obligatory columns are present in the sample information (Injection_order as numeric and unique), feature data (Mass or Average_mz, and one of: Retention time, RetentionTime, Average_rt(min), or rt), and that the abundance matrix is numeric. Allow automatic generation of Sample_ID (via id_prefix, default 'ID') and QC field (value 'QC' for QC samples, 'Sample' for biological samples) if not present. Call construct_metabosets() with the three returned data parts and specify group_col and optionally time_col and subject_col to assign special column semantics. The function will automatically create Feature_ID by combining Split, mass, and retention time, set as row names of the expression matrix.

## Related tools

- **notame** (Provides read_from_excel() and construct_metabosets() functions to parse Excel peak tables and assemble MetaboSet objects; core package bundling preprocessing methods for LC-MS metabolomics) — https://github.com/hanhineva-lab/notame
- **Biobase** (Supplies ExpressionSet class upon which MetaboSet is built; provides the eSet infrastructure (exprs, fData, pData slots))
- **ExpressionSet** (Data structure class (from Biobase) that stores expression-level data, feature annotations, and phenotype data in a unified object)
- **R** (Runtime environment for executing read_from_excel(), construct_metabosets(), and downstream notame workflows)

## Examples

```
library(notame); peaks <- read_from_excel('sample_data_whole.xlsx', sheet = 1, corner = c(row = 10, col = 1), split_by = c('LC_column', 'Ion_mode')); metabosets <- construct_metabosets(peaks$exprs, peaks$pheno_data, peaks$feature_data, group_col = 'Group')
```

## Evaluation signals

- The returned MetaboSet object (or list thereof) contains non-empty exprs, fData, and pData slots with matching dimensions: nrow(exprs) == nrow(fData), ncol(exprs) == nrow(pData).
- Feature_ID column is present in fData and matches row names of exprs, with all Feature_IDs unique and formatted as '{Split}_{mass}_{retention_time}'.
- Obligatory columns are fully populated with no missing values: Injection_order is numeric and unique across all samples; Mass/Average_mz and retention time columns are numeric and non-negative in fData; Sample_ID, QC, and group_col assignments are non-empty in pData.
- If split_by was specified, the Split field is correctly generated by concatenating the specified columns (e.g., 'HILIC_pos' from LC_column='HILIC' and Ion_mode='pos'), and each MetaboSet corresponds to one unique Split value.
- Row and column indices are contiguous integers starting from 1, with no gaps or reordering relative to the source Excel worksheet.

## Limitations

- The function assumes a fixed Excel layout: sample metadata in rows, feature metadata in columns, and a single contiguous abundance matrix block. Worksheets with merged cells, multiple tables, or non-standard layouts will fail to parse correctly.
- Retention time columns must be present and unambiguous; if multiple retention time columns exist (e.g., both 'rt' and 'Average_rt(min)'), the function may select unpredictably or error.
- Feature_ID is constructed deterministically from Split, mass, and retention time; if mass or retention time values are duplicated, Feature_IDs will not be unique, violating the assumption that Feature_ID is a primary key.
- The notame package API is described as experimental with possible breaking changes; scripts written for one version may not be compatible with later releases.
- The function does not validate ion mode values or tolerate missing Ion_mode labels; if corner coordinates are incorrect, the parser will misalign data compartments.

## Evidence

- [other] To construct a MetaboSet object, you need to have the data read in R. This can be achieved with read_from_excel function: "To construct a ```MetaboSet``` object, you need to have the data read in R. This can be achieved with ```read_from_excel``` function"
- [other] Call read_from_excel with the Excel file path, sheet number, and corner coordinates (row and column where Ion Mode label is located) to parse the three data compartments: "Call read_from_excel with the Excel file path, sheet number, and corner coordinates (row and column where Ion Mode label is located) to parse the three data compartments (pheno data, feature data,"
- [other] Obligatory columns must include Injection_order (numeric, unique) in sample information; Mass or Average_mz in feature data; and Retention time / RetentionTime / Average_rt(min) / rt in feature data: "Verify obligatory columns are present: Injection_order (numeric, unique) in sample information; Mass or Average_mz in feature data; and Retention time / RetentionTime / Average_rt(min) / rt in"
- [other] Feature_ID is created by combining Split, mass, and retention time and is set as row names of exprs: "Confirm Feature_ID is created by combining Split, mass, and retention time and is set as row names of exprs"
- [readme] The first step is to take raw data files created by the LC-MS instrument and create a peak table using a peak picking software (we use MS-DIAL): "The first step is to take raw data files created by the LC-MS instrument and create a peak table using a peak picking software (we use MS-DIAL)"
- [readme] Reading data from Excel spreadsheets created with MS-DIAL: "Reading data from Excel spreadsheets created with MS-DIAL"
- [other] MetaboSet is built upon the ExpressionSet class from the Biobase package by Bioconductor: "```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor"
