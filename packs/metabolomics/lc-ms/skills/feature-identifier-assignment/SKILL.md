---
name: feature-identifier-assignment
description: Use when after constructing MetaboSet objects from Excel-formatted LC-MS peak tables and before drift correction or quality flagging.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Feature-identifier assignment

## Summary

Construct and assign unique Feature_ID identifiers to LC-MS metabolomic features by combining Split mode, mass, and retention time values into row names of the expression matrix. This ensures consistent feature tracking and traceability across the MetaboSet object structure.

## When to use

After constructing MetaboSet objects from Excel-formatted LC-MS peak tables and before drift correction or quality flagging. Use this skill when Feature_ID is not already present in the input data or when you need to verify that Feature_IDs correctly integrate mode, mass, and retention time information to uniquely identify each molecular feature.

## When NOT to use

- Input is already a MetaboSet or ExpressionSet object with pre-assigned Feature_IDs—verify identifiers are present before attempting reassignment.
- Feature data lacks both mass and retention time columns—Feature_ID construction will fail without these obligatory descriptors.
- Split information cannot be determined (no split_by columns available and no single name supplied)—the mode component of Feature_ID cannot be generated.

## Inputs

- Excel spreadsheet with three data compartments: sample information (pheno data), feature metadata, and peak intensity matrix (exprs)
- Feature data containing Mass or Average_mz column and Retention time or equivalent column
- Sample information containing Injection_order (numeric, unique) and optional Sample_ID and QC columns

## Outputs

- MetaboSet object with Feature_ID as row names in exprs matrix
- Feature metadata (fData) with Feature_ID column present
- Sample metadata (pData) with Sample_ID and QC fields populated

## How to apply

The read_from_excel function automatically generates Feature_ID by combining the Split field (derived from split_by columns such as LC column and ionization mode), mass (from 'Mass' or 'Average_mz' columns), and retention time (from 'Retention time', 'RetentionTime', 'Average_rt(min)', or 'rt' columns). Specify split_by columns when calling read_from_excel, or supply a single name argument (e.g., 'HILIC_pos') if the file contains a single mode. Verify that obligatory columns are present: Mass or Average_mz and retention time in feature data. The constructed Feature_ID is then set as row names of the exprs matrix and included in the fData slot. Confirm the mapping is correct by checking that row names of exprs match the Feature_ID column in fData and that all three components (mode, mass, retention time) are present and non-redundant.

## Related tools

- **notame** (Provides read_from_excel and construct_metabosets functions to parse Excel peak tables and generate Feature_ID identifiers within MetaboSet objects) — https://github.com/hanhineva-lab/notame
- **Biobase** (Provides ExpressionSet class upon which MetaboSet is built; stores feature identifiers as row names and feature metadata)
- **ExpressionSet** (Base class for MetaboSet; row names (Feature_ID) are assigned to the exprs matrix through this class)

## Examples

```
read_from_excel(file='sample_data_whole.xlsx', sheet=1, corner=c(1,1), split_by=c('LC_column', 'ionization_mode')); construct_metabosets(exprs=exprs, pheno_data=pheno_data, feature_data=feature_data, group_col='group')
```

## Evaluation signals

- Feature_ID column is present in fData (feature metadata) slot of the MetaboSet object and is non-empty for all features
- Row names of the exprs matrix exactly match the Feature_ID values in fData (no misalignment or truncation)
- Each Feature_ID is unique (no duplicate identifiers for distinct features across all modes)
- Feature_ID incorporates all three components: mode/Split value, mass value (numeric, non-null), and retention time value (numeric, non-null)
- Obligatory columns (Mass or Average_mz, retention time variant) were present in the input feature data and successfully parsed into identifiers

## Limitations

- Feature_ID generation relies on the presence and correctness of mass and retention time values in the input Excel file; missing or malformed values in these columns will result in partial or incomplete identifiers.
- The Split field is created only if split_by columns are specified or a single name is supplied; absence of mode information reduces Feature_ID discriminative power when multiple ionization modes or LC columns are used.
- Retention time precision and mass accuracy are not validated during identifier assignment; features with very similar mass and retention time may result in visually similar but technically distinct Feature_IDs, potentially causing confusion.
- The notame package API is experimental and subject to breaking changes, which may affect Feature_ID generation logic in future versions.

## Evidence

- [other] Confirm Feature_ID is created by combining Split, mass, and retention time and is set as row names of exprs.: "Confirm Feature_ID is created by combining Split, mass, and retention time and is set as row names of exprs."
- [other] Specify split_by columns (typically LC column and ionization mode) so the function generates the Split field combining these values; alternatively supply a name argument (e.g., 'HILIC_pos') if the file contains a single mode.: "Specify split_by columns (typically LC column and ionization mode) so the function generates the Split field combining these values; alternatively supply a name argument (e.g., 'HILIC_pos') if the"
- [other] Verify obligatory columns are present: Injection_order (numeric, unique) in sample information; Mass or Average_mz in feature data; and Retention time / RetentionTime / Average_rt(min) / rt in feature data.: "Verify obligatory columns are present: Injection_order (numeric, unique) in sample information; Mass or Average_mz in feature data; and Retention time / RetentionTime / Average_rt(min) / rt in"
- [readme] The package API is still quite experimental, and breaking changes are possible: "The package API is still quite experimental, and breaking changes are possible"
- [other] MetaboSet is built upon the ExpressionSet class from the Biobase package by Bioconductor: "MetaboSet is built upon the ExpressionSet class from the Biobase package by Bioconductor"
