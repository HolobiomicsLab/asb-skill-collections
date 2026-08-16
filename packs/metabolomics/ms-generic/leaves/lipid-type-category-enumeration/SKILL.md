---
name: lipid-type-category-enumeration
description: Use when when you have downloaded or cloned a lipidomics library repository (such as LipidMatch) and need to audit the breadth of lipid-type coverage to ensure the library meets minimum requirements for your analysis scope (e.g., ≥60 distinct lipid categories).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - LipidMatch
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-017-1744-3
  all_source_dois:
  - 10.1186/s12859-017-1744-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-type-category-enumeration

## Summary

Enumerate and count distinct lipid-type categories present in in-silico fragmentation library files to verify comprehensive coverage across lipid taxonomy. This skill validates that a lipidomics tool or resource covers a sufficiently broad range of lipid classes required for unbiased lipid identification in untargeted mass spectrometry workflows.

## When to use

When you have downloaded or cloned a lipidomics library repository (such as LipidMatch) and need to audit the breadth of lipid-type coverage to ensure the library meets minimum requirements for your analysis scope (e.g., ≥60 distinct lipid categories). Apply this skill before committing the library to a production workflow or before claiming comprehensive coverage in a validation study.

## When NOT to use

- The input is already a processed or summary report (e.g., a pre-counted category list) rather than raw library .csv files.
- You only need to identify lipids in a single sample and do not require validation of library breadth; use this skill only for library audits or benchmarking.
- The input data is in a non-.csv format (e.g., mzML, NetCDF, or binary database files) without a clear lipid-type category field; extract or convert to tabular format first.

## Inputs

- .csv library files from lipidomics software repository (e.g., from GarrettLab-UF/LipidMatch)
- Lipid-type category field (column) within each .csv file

## Outputs

- Set of distinct lipid-type categories
- Total count of distinct lipid types
- Summary report with category count, list of categories, and pass/fail status against threshold

## How to apply

Locate and parse all .csv library files in the repository. Extract the lipid-type category field from each record (e.g., the column specifying lipid class such as TAG, DAG, PC, PE, etc.). Aggregate all distinct lipid-type values across all files using a set or unique-count operation to eliminate duplicates. Enumerate the resulting set and count the total number of distinct categories. Compare the count against your threshold requirement (e.g., 60 lipid types for comprehensive coverage). Document pass/fail status along with the actual count achieved. The rationale is that lipid diversity in biological samples spans many classes; enumeration ensures the library captures sufficient structural and fragmentation diversity to support unbiased identification across those classes.

## Related tools

- **LipidMatch** (Source lipidomics library containing in-silico fragmentation data organized by lipid type; libraries are provided as .csv files in the repository.) — https://github.com/GarrettLab-UF/LipidMatch

## Evaluation signals

- Total distinct lipid-type count meets or exceeds the specified threshold (e.g., ≥60 for comprehensive coverage).
- All .csv files in the repository have been parsed and included in the enumeration (no files skipped).
- Duplicate lipid-type entries within or across files are correctly deduplicated using set operations.
- The enumerated category list is reproducible when the same set of library files is re-parsed.
- Summary report explicitly lists all distinct lipid types found and provides evidence (e.g., sample row counts per category) supporting the count.

## Limitations

- The skill assumes lipid-type category is consistently named and formatted across all .csv files; heterogeneous column names or formats may require manual field mapping.
- Enumeration counts categories present in the library but does not assess the quality, accuracy, or completeness of fragmentation patterns within each category; use separate validation methods to verify fragmentation library accuracy.
- The skill does not validate whether the lipid types enumerated are appropriate for your specific biological sample or experimental design; threshold choice (e.g., 60 types) must be informed by your research question.
- The LipidMatch library does not currently support Waters instrument files, which may limit applicability in some workflows.

## Evidence

- [readme] LipidMatch contains in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types.: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [other] Parse each .csv file to extract lipid species identifiers and lipid-type category assignments.: "Parse each .csv file to extract lipid species identifiers and lipid-type category assignments"
- [other] Aggregate distinct lipid species across all files using a set or unique count operation.: "Aggregate distinct lipid species across all files using a set or unique count operation"
- [other] Enumerate distinct lipid-type categories present in the aggregated data.: "Enumerate distinct lipid-type categories present in the aggregated data"
- [readme] LipidMatch allows for facile integration of user generated libraries for unique applications.: "LipidMatch allows for facile integration of user generated libraries for unique applications"
