---
name: ionization-mode-and-column-mode-separation
description: Use when your LC-MS peak table from MS-DIAL or similar software contains data from multiple ionization modes (positive and/or negative) and/or multiple chromatographic columns (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3172
  tools:
  - notame
  - R
  - Biobase
  - ExpressionSet
  - MS-DIAL
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

# Ionization Mode and Column Mode Separation

## Summary

Separates LC-MS peak table data by chromatographic column and ionization mode (e.g., positive/negative ESI) to create mode-specific MetaboSet objects, enabling independent preprocessing and later integration of multimodal data. This is a prerequisite step in the notame workflow to preserve mode-specific feature identities and quality metrics.

## When to use

Your LC-MS peak table from MS-DIAL or similar software contains data from multiple ionization modes (positive and/or negative) and/or multiple chromatographic columns (e.g., HILIC, RP-C18), and you need to construct separate MetaboSet objects per mode before quality filtering, drift correction, and imputation. Use this skill when read_from_excel encounters a Split column or when you must specify split_by parameters to distinguish modes.

## When NOT to use

- Your peak table is already separated into mode-specific files—load each file individually without split_by specification.
- Data lacks Ion.mode or LC.column metadata; cannot assign samples to distinct modes unambiguously.
- You are working with a single ionization mode and single column; omit split_by and provide name argument directly instead.

## Inputs

- Excel spreadsheet (.xlsx) with three compartments: sample/phenotype information, feature metadata (Mass or Average_mz, retention time), and peak intensity matrix
- Column designations specifying which columns encode LC mode (e.g., 'LC.column') and ionization mode (e.g., 'Ion.mode')
- Metadata columns: Injection_order (numeric, unique per sample), Ion Mode indicator, and chromatographic column identifier

## Outputs

- List of one or more MetaboSet objects (one per unique mode combination), each with non-empty exprs, fData, and pData slots
- Feature_ID column in fData combining Split, mass, and retention time; matched as row names in exprs
- Sample_ID and QC fields auto-generated if not present (Sample_ID via id_prefix, QC field distinguishing 'QC' from 'Sample')

## How to apply

Call read_from_excel with the Excel file path and specify split_by as a vector of column names (typically 'LC.column' and 'Ion.mode') that will be combined to create a Split field (e.g., 'HILIC_pos', 'HILIC_neg', 'RP_pos'). If the file contains only a single mode, supply a name argument directly (e.g., name='HILIC_pos') instead of split_by. The function parses three data compartments (expression matrix, phenotype data, feature data) and automatically generates the Split identifier by concatenating the split_by column values. Pass the returned components to construct_metabosets with appropriate group_col, time_col, and subject_col parameters. This creates a list containing one MetaboSet per detected mode, with Feature_ID generated as a unique combination of Split, mass (or Average_mz), and retention time, set as row names of the expression matrix.

## Related tools

- **notame** (R package providing read_from_excel and construct_metabosets functions to parse Excel peak tables and instantiate mode-separated MetaboSet objects) — https://github.com/hanhineva-lab/notame
- **Biobase** (Bioconductor package providing ExpressionSet class that MetaboSet extends; defines slot structure (exprs, fData, pData) used to store mode-separated LC-MS data)
- **ExpressionSet** (S4 class from Biobase that serves as the base class for MetaboSet; manages expression matrix and associated feature/phenotype metadata)
- **MS-DIAL** (Peak picking software producing Excel output in the format expected by read_from_excel; generates Ion.mode and LC.column columns) — http://prime.psc.riken.jp/Metabolomics_Software/MS-DIAL/

## Examples

```
modes <- read_from_excel(file='sample_data_whole.xlsx', sheet=1, corner=c(17, 1), split_by=c('LC.column', 'Ion.mode')); metabosets <- construct_metabosets(modes$exprs, modes$pheno_data, modes$feature_data, group_col='Group')
```

## Evaluation signals

- Returned list contains exactly N MetaboSet objects where N equals the number of unique split_by combinations (e.g., 4 for HILIC_pos, HILIC_neg, RP_pos, RP_neg)
- Each MetaboSet has non-empty exprs, fData (with Feature_ID column), and pData slots; row names of exprs match Feature_ID
- Feature_ID entries are unique within each MetaboSet and follow the format Split_mass_retention_time (e.g., 'HILIC_pos_500.123_2.45')
- Sample counts are correctly distributed across modes (each sample appears in only one mode's pData)
- Obligatory columns present and non-null: Injection_order (numeric, unique per mode), Mass or Average_mz, Retention time/rt, Sample_ID, QC field

## Limitations

- Requires that split_by columns are present and populated in the input Excel file; missing or inconsistent Ion.mode or LC.column values will cause incorrect or incomplete mode assignment.
- Retention time format must match one of: 'Retention time', 'RetentionTime', 'Average_rt(min)', or 'rt'; non-standard column names will fail Feature_ID generation.
- Each mode is processed independently; batch effects and drift spanning multiple modes are not corrected until modes are merged post-preprocessing.
- The notame package API is experimental and breaking changes are possible; function signatures or split behavior may change between versions.

## Evidence

- [other] Call read_from_excel with the Excel file path, sheet number, and corner coordinates (row and column where Ion Mode label is located) to parse the three data compartments (pheno data, feature data, exprs). Specify split_by columns (typically LC column and ionization mode) so the function generates the Split field combining these values: "Call read_from_excel with the Excel file path, sheet number, and corner coordinates (row and column where Ion Mode label is located) to parse the three data compartments (pheno data, feature data,"
- [other] Confirm Feature_ID is created by combining Split, mass, and retention time and is set as row names of exprs. Validation: verify the returned list contains one or more MetaboSet objects (one per mode), each with non-empty exprs, fData, and pData slots, Feature_ID column present in fData and matching row names in exprs: "Confirm Feature_ID is created by combining Split, mass, and retention time and is set as row names of exprs. Validation: verify the returned list contains one or more MetaboSet objects (one per"
- [other] To construct a MetaboSet object, you need to have the data read in R. This can be achieved with read_from_excel function. MetaboSet objects are constructed with the construct_metabosets function.: "To construct a ```MetaboSet``` object, you need to have the data read in R. This can be achieved with ```read_from_excel``` function. MetaboSet objects are constructed with the construct_metabosets"
- [other] MetaboSet is built upon the ExpressionSet class from the Biobase package; MetaboSet objects are the primary data structure of this package.: "```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor; ```MetaboSet``` objects are the primary data structure of this package."
- [readme] After peak picking with the dedicated software, we use R for data preprocessing, quality control, statistical analysis and visualization.: "After peak picking with the dedicated software, we use R for data preprocessing, quality control, statistical analysis and visualization."
