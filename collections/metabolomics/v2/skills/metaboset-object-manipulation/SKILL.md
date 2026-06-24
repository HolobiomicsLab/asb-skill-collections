---
name: metaboset-object-manipulation
description: Use when when you have read LC-MS peak table data from Excel (or equivalent)
  into R and need to organize it into a structured object that tracks feature abundances,
  sample information (injection order, QC status), and feature metadata (mass, retention
  time, Feature_ID) simultaneously.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3643
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - notame
  - R
  - missForest
  - doParallel
  - Biobase
  - ExpressionSet
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- The implementation we use (from the missForest package) can be parallelized
- Load the libraries (doParallel is used for parallel processing)
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package
  by Bioconductor'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MetaboSet Object Manipulation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Create, inspect, and modify MetaboSet objects—the primary Biobase-derived data structure in the notame workflow—to organize LC-MS abundances, sample metadata, and feature annotations in a unified, interoperable format.

## When to use

When you have read LC-MS peak table data from Excel (or equivalent) into R and need to organize it into a structured object that tracks feature abundances, sample information (injection order, QC status), and feature metadata (mass, retention time, Feature_ID) simultaneously. Use this when the input is raw expression matrix columns, phenotype data rows, and feature annotation rows that must be bound into a single object for downstream notame preprocessing steps (drift correction, flagging, imputation).

## When NOT to use

- Input is already in Bioconductor ExpressionSet format; use construct_metabosets directly on the three data parts instead of read_from_excel.
- Peak table data is in native mzML, netCDF, or vendor raw formats; first run peak-picking software (e.g., MS-DIAL) to produce a processed peak table spreadsheet.
- Missing obligatory columns (Injection_order, mass/mz, retention time) in the input file; read_from_excel will fail or produce incomplete MetaboSet objects.

## Inputs

- Excel (.xlsx) peak table file with three data compartments: sample phenotype data, feature annotation data, and abundance expression matrix
- Row and column corner coordinates identifying where the Ion Mode label is located in the spreadsheet
- Column specification mapping (group_col, time_col, subject_col) to designate special sample metadata fields

## Outputs

- One or more MetaboSet objects (list) — one per LC-MS mode or split_by value
- Each MetaboSet contains: exprs (abundance matrix with Feature_ID as row names), fData (feature annotations including Feature_ID, mass, retention time, Flag column), and pData (sample metadata including Sample_ID, Injection_order, QC status, group designation)

## How to apply

First, use read_from_excel to parse an Excel peak table file, specifying the corner coordinates (row and column where the Ion Mode label appears) to demarcate the three data compartments: pheno data, feature data, and expression matrix. Verify that obligatory columns are present: Injection_order (numeric, unique) in sample information; Mass or Average_mz in feature data; and a retention time column (Retention time / RetentionTime / Average_rt(min) / rt) in feature data. The function will automatically generate Sample_ID and QC fields if absent. Then call construct_metabosets with the three returned data parts (exprs, pheno_data, feature_data), specifying group_col and optionally time_col and subject_col to designate special column semantics. This produces one or more MetaboSet objects (one per LC-MS mode or split_by combination), each built on the ExpressionSet class from Biobase, with Feature_ID automatically created by combining Split, mass, and retention time and set as row names of the exprs matrix. Subsequent notame functions (flag_detection, flag_quality, mark_nas, impute_rf) operate on this unified object, reading and updating the Flag column in fData and the exprs abundance matrix.

## Related tools

- **notame** (Core package providing read_from_excel and construct_metabosets functions for MetaboSet creation and manipulation) — https://github.com/hanhineva-lab/notame
- **Biobase** (Provides ExpressionSet class upon which MetaboSet is built, enabling unified storage of exprs, fData, and pData)
- **ExpressionSet** (Bioconductor data structure for storing high-dimensional abundance data with associated feature and sample metadata)
- **R** (Language and runtime environment for executing read_from_excel, construct_metabosets, and subsequent MetaboSet manipulations)

## Examples

```
library(notame); mbs_list <- read_from_excel('sample_data_whole.xlsx', sheet=1, corner=c('A','1'), split_by=c('LC_column', 'Ion_mode')); mbs <- construct_metabosets(mbs_list$exprs, mbs_list$pheno_data, mbs_list$feature_data, group_col='treatment')
```

## Evaluation signals

- Returned list contains one or more MetaboSet objects with non-empty exprs, fData, and pData slots.
- Feature_ID column is present in fData and exactly matches row names of the exprs matrix.
- All obligatory columns (Injection_order, mass/Average_mz, retention time) are populated with non-NA values across all samples and features.
- QC field in pData correctly distinguishes QC samples (value='QC') from biological samples (value='Sample').
- Sample_ID values are unique and correspond to rows in pData; Injection_order is numeric and unique; Feature_ID is a character string combining Split, mass, and retention time.

## Limitations

- The read_from_excel parser is tightly coupled to MS-DIAL output format; Excel files from other peak-picking software may require manual reformatting to match the expected three-compartment layout.
- Feature_ID generation concatenates Split, mass, and retention time; collision (identical IDs for different features) can occur if mass and retention time precision are low or if Split names overlap.
- The MetaboSet structure assumes that a single injection_order column and QC designation exist; complex experimental designs with multiple sample groupings or nested batches may require post-hoc modification of pData.
- The package API is described as experimental; breaking changes are possible between versions.

## Evidence

- [other] MetaboSet structure and purpose: "To construct a ```MetaboSet``` object, you need to have the data read in R. This can be achieved with ```read_from_excel``` function"
- [other] Obligatory columns requirement: "Verify obligatory columns are present: Injection_order (numeric, unique) in sample information; Mass or Average_mz in feature data; and Retention time / RetentionTime / Average_rt(min) / rt in"
- [other] Feature_ID generation and role: "Confirm Feature_ID is created by combining Split, mass, and retention time and is set as row names of exprs."
- [other] ExpressionSet inheritance and multi-compartment design: "```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor"
- [other] Downstream integration with notame preprocessing: "Subsequent notame functions (flag_detection, flag_quality, mark_nas, impute_rf) operate on this unified object, reading and updating the Flag column in fData"
