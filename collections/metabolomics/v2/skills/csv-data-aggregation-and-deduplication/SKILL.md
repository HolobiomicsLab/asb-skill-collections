---
name: csv-data-aggregation-and-deduplication
description: Use when when you have downloaded a multi-file .csv library repository (e.g., LipidMatch) and need to verify that it meets minimum thresholds for species diversity (e.g., 500,000+ distinct lipid species) and category breadth (e.g., 60+ lipid-type categories).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3906
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
  tools:
  - LipidMatch
  - Python pandas or native set operations
  - R data.table or dplyr
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
---

# csv-data-aggregation-and-deduplication

## Summary

Load and parse multiple .csv library files, extract species identifiers and category assignments, aggregate distinct entries using set operations, and enumerate unique categories to verify library completeness. This skill is essential for validating the coverage and diversity of in-silico fragmentation libraries used in lipidomics workflows.

## When to use

When you have downloaded a multi-file .csv library repository (e.g., LipidMatch) and need to verify that it meets minimum thresholds for species diversity (e.g., 500,000+ distinct lipid species) and category breadth (e.g., 60+ lipid-type categories). Use this when reported library sizes or composition are claimed but not yet empirically verified in your environment.

## When NOT to use

- Input is already a pre-aggregated, single .csv file with deduplicated entries — skip directly to threshold validation.
- Library files are in non-CSV formats (e.g., JSON, binary, or proprietary formats) — use format-specific parsers instead.
- You only need to identify a single lipid species or category, not comprehensively validate library coverage — use targeted lookup instead.

## Inputs

- .csv library files from a GitHub repository (e.g., GarrettLab-UF/LipidMatch)
- Repository directory path or clone URL
- Column names or positional indices for species identifier and lipid-type category

## Outputs

- Distinct lipid species count (integer)
- Enumeration of unique lipid-type categories (list or set)
- Summary report with species count, category count, and pass/fail status for each threshold
- Aggregated species and category metadata (optional: deduplicated .csv or in-memory data structure)

## How to apply

Clone or download the target GitHub repository (e.g., GarrettLab-UF/LipidMatch). Locate all .csv library files in the repository directory structure. Programmatically load each .csv file and parse rows to extract two fields: the lipid species identifier (typically a column with systematic lipid nomenclature) and the lipid-type category (e.g., 'PC', 'PE', 'TAG'). Aggregate all species identifiers into a set data structure to remove duplicates across files. Count the total number of unique species and enumerate the distinct categories. Compare the species count against your minimum threshold (e.g., 500,000) and the category count against your minimum threshold (e.g., 60). Document pass/fail status for each threshold in a summary report.

## Related tools

- **LipidMatch** (in-silico fragmentation library source; contains .csv library files to be aggregated and deduplicated) — https://github.com/GarrettLab-UF/LipidMatch
- **Python pandas or native set operations** (CSV parsing and deduplication (set or unique count operations))
- **R data.table or dplyr** (CSV loading, grouping, and distinct counting)

## Examples

```
import pandas as pd; from pathlib import Path; csvs = list(Path('LipidMatch').glob('*.csv')); all_data = pd.concat([pd.read_csv(f) for f in csvs]); unique_species = all_data['species_id'].nunique(); unique_categories = all_data['lipid_type'].nunique(); print(f'Species: {unique_species}, Categories: {unique_categories}')
```

## Evaluation signals

- Total distinct species count meets or exceeds the minimum threshold (e.g., 500,000)
- Number of unique lipid-type categories meets or exceeds the minimum threshold (e.g., 60)
- Set operations correctly remove duplicate species identifiers across files (spot-check by reloading a single file twice and verifying no duplication)
- All .csv files in the repository directory are loaded — verify file count matches expectation and no files are skipped
- Summary report is generated and reproducible: running the same aggregation pipeline twice yields identical species and category counts

## Limitations

- LipidMatch does not currently support Waters instrument files; if your experimental data comes from Waters instruments, the library will not be validated against those data downstream.
- The skill depends on consistent column naming and data structure across all .csv files; heterogeneous formats or missing columns will cause parsing errors or incomplete aggregation.
- This skill validates library completeness but does not assess quality, accuracy, or biological relevance of the in-silico fragments — it is a coverage check, not a performance benchmark.

## Evidence

- [readme] LipidMatch contains in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [other] Parse each .csv file to extract lipid species identifiers and lipid-type category assignments: "Parse each .csv file to extract lipid species identifiers and lipid-type category assignments"
- [other] Aggregate distinct lipid species across all files using a set or unique count operation: "Aggregate distinct lipid species across all files using a set or unique count operation"
- [other] Compare total species count against the threshold of 500,000 and lipid-type category count against 60: "Compare total species count against the threshold of 500,000 and lipid-type category count against 60"
- [readme] The link at the bottom of this page contains a manual, lipid libraries in .csv format: "lipid libraries in .csv format"
