---
name: sample-metadata-integration
description: Use when when you have LC-MS peak table data in Excel format (e.g., from MS-DIAL peak picking) with separate compartments for sample information, feature properties, and intensity values, and you need to construct a structured R object that enforces consistency between sample metadata (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
  - build: coll_fbmn_stats_cq
    doi: 10.1038/s41596-024-01046-3
    title: FBMN-STATS
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

# sample-metadata-integration

## Summary

Integration of sample metadata (phenotypic data) with LC-MS feature abundance matrices into a unified MetaboSet object that preserves sample identifiers, injection order, QC status, and experimental design information. This skill enables downstream quality control, batch correction, and statistical analysis by co-locating sample annotations with their corresponding intensity measurements.

## When to use

When you have LC-MS peak table data in Excel format (e.g., from MS-DIAL peak picking) with separate compartments for sample information, feature properties, and intensity values, and you need to construct a structured R object that enforces consistency between sample metadata (e.g., Injection_order, QC status) and abundance data before drift correction, imputation, or batch effect correction.

## When NOT to use

- Input is already a feature abundance table with sample metadata in R memory (use direct ExpressionSet construction instead).
- Data are in mzML, netCDF, or other raw LC-MS vendor formats (use peak picking software first).
- Sample metadata and feature data are in separate, disconnected files with no explicit relationship mechanism (reconcile before calling read_from_excel).

## Inputs

- Excel spreadsheet with three data regions: sample information table, feature metadata table, and intensity matrix (e.g., sample_data_whole.xlsx)
- Row and column coordinates specifying the location of the Ion Mode label
- Column names for grouping (e.g., group_col), time tracking (time_col), and subject identifiers (subject_col)

## Outputs

- List of one or more MetaboSet objects (one per ionization mode), each an ExpressionSet subclass containing:
-   - exprs slot: intensity matrix with Feature_ID row names and Sample_ID column names
-   - fData slot: feature metadata including Feature_ID, Split, mass, retention time, and quality flags
-   - pData slot: sample metadata including Injection_order, QC status, Sample_ID, group, time, and subject columns

## How to apply

Load the notame package and use read_from_excel to parse an Excel file with three data compartments: pheno data (sample information), feature data (mass, retention time), and exprs (intensity matrix). Specify the corner coordinates where the Ion Mode label appears to anchor the parser. Ensure obligatory columns are present: Injection_order (numeric, unique) in sample information; Mass or Average_mz and Retention_time/RetentionTime/Average_rt(min)/rt in feature data. Use the split_by argument to specify columns (typically LC column and ionization mode) for generating Split identifiers, or provide a name argument if a single mode is present. Then call construct_metabosets with the returned exprs, pheno_data, and feature_data, specifying group_col and optionally time_col and subject_col. This creates one MetaboSet per ionization mode, each with Feature_ID row names combining Split, mass, and retention time. Validate that fData contains Feature_ID matching exprs row names and all obligatory columns are populated.

## Related tools

- **notame** (Provides read_from_excel and construct_metabosets functions to parse Excel files and integrate sample metadata with LC-MS abundances into MetaboSet objects) — https://github.com/hanhineva-lab/notame
- **Biobase** (Provides ExpressionSet class upon which MetaboSet is built, defining slots for exprs, fData, and pData)
- **R** (Runtime environment for executing notame functions and managing data structures)

## Examples

```
read_from_excel('sample_data_whole.xlsx', sheet=1, corner=list(row=10, col=2), split_by=c('LC_method', 'Ion_mode')) %>% construct_metabosets(group_col='Treatment', time_col='Time_point', subject_col='Subject_ID')
```

## Evaluation signals

- Returned object is a list containing one or more MetaboSet objects (length > 0), one per distinct ionization mode or split category.
- Each MetaboSet has non-empty exprs slot (matrix of numeric intensities), fData slot (feature metadata), and pData slot (sample metadata).
- Feature_ID column is present in fData and exactly matches the row names of the exprs matrix.
- All obligatory columns in pData are populated: Injection_order is numeric and unique per sample, QC field contains only 'QC' or 'Sample' values.
- All obligatory columns in fData are populated: Mass or Average_mz is numeric, retention time column (e.g., Average_rt(min)) is numeric, Split field correctly identifies ionization mode and/or LC column.
- Sample_ID column in pData matches exprs column names; no NAs in obligatory metadata columns.

## Limitations

- Excel file must follow a rigid three-compartment layout (sample info, feature info, intensity matrix); other formats require pre-conversion.
- The function requires manual specification of corner coordinates (row and column of Ion Mode label), making it sensitive to file layout changes.
- If obligatory columns (Injection_order, mass, retention time) are absent or misnamed, the function fails; no automatic fallback to alternative column names beyond the listed aliases.
- The package API is experimental, and breaking changes are possible as noted in the notame README; users should pin package versions.
- notame primarily supports MS-DIAL peak table output; integration with other peak pickers (e.g., XCMS, MZmine) requires manual reformatting to the expected Excel structure.

## Evidence

- [other] read_from_excel_construction: "Call read_from_excel with the Excel file path, sheet number, and corner coordinates (row and column where Ion Mode label is located) to parse the three data compartments (pheno data, feature data,"
- [other] obligatory_columns: "Verify obligatory columns are present: Injection_order (numeric, unique) in sample information; Mass or Average_mz in feature data; and Retention time / RetentionTime / Average_rt(min) / rt in"
- [other] construct_metabosets: "Call construct_metabosets with the three returned data parts (exprs, pheno_data, feature_data) and specify group_col and optionally time_col and subject_col to set special column names."
- [other] feature_id_generation: "Confirm Feature_ID is created by combining Split, mass, and retention time and is set as row names of exprs."
- [other] metaboset_definition: "```MetaboSet``` objects are the primary data structure of this package. ```MetaboSet``` is built upon the ```ExpressionSet``` class"
- [readme] readme_read_from_excel: "To construct a ```MetaboSet``` object, you need to have the data read in R. This can be achieved with ```read_from_excel``` function"
- [readme] readme_metaboset_construction: "```MetaboSet``` objects are constructed with the ```construct_metabosets``` function"
- [readme] readme_data_storage: "Data is stored in a custom object that holds all the information about the features and samples along with the feature abundance matrix."
