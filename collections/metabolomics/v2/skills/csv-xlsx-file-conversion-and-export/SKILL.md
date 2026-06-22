---
name: csv-xlsx-file-conversion-and-export
description: Use when when you have validated mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, and compound identifiers) formatted in one tabular format (CSV or XLSX) and need to convert it to the other format for ingestion into EISA-EXPOSOME or long-term archival.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R Shiny
derived_from:
- doi: 10.1021/acs.analchem.3c02697
  title: EISA-EXPOSOME
evidence_spans:
- We provide a Rshiny program for EISA-EXPOSOME
- We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown below
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eisa_exposome_cq
    doi: 10.1021/acs.analchem.3c02697
    title: EISA-EXPOSOME
  dedup_kept_from: coll_eisa_exposome_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c02697
  all_source_dois:
  - 10.1021/acs.analchem.3c02697
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# csv-xlsx-file-conversion-and-export

## Summary

Convert and export mass spectrometry transition data between CSV and XLSX formats while preserving the EISA-EXPOSOME schema (NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID columns). This skill ensures database files remain compatible with downstream suspect chemical screening workflows.

## When to use

When you have validated mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, and compound identifiers) formatted in one tabular format (CSV or XLSX) and need to convert it to the other format for ingestion into EISA-EXPOSOME or long-term archival. Specifically triggered when the input database file must be compatible with the R Shiny interface, which expects either .xlsx or .csv with the six-column schema.

## When NOT to use

- Input is raw, unvalidated mass spectrometry data that has not yet been cross-referenced against T3DB or had reference compounds (e.g., Methamidophos) verified—perform schema validation and reference checks first.
- Input is already in the required EISA-EXPOSOME format and is being ingested directly into the R Shiny interface without need for format conversion.
- Input lacks the mandatory columns (NAME, PrecursorMZ, ProductMZ, Intensity, ID); restructure and validate data schema before attempting export.

## Inputs

- Raw mass spectrometry transition data in CSV format (.csv) with columns NAME, PrecursorMZ, ProductMZ, Intensity, RT (optional), ID
- Raw mass spectrometry transition data in XLSX format (.xlsx) with columns NAME, PrecursorMZ, ProductMZ, Intensity, RT (optional), ID
- T3DB reference database file in .xlsx format

## Outputs

- Validated and converted database file in XLSX format (.xlsx) with EISA-EXPOSOME schema
- Validated and converted database file in CSV format (.csv) with EISA-EXPOSOME schema

## How to apply

After validating your data contains all required columns (NAME, PrecursorMZ, ProductMZ, Intensity, RT [optional], ID) and checking reference entries (e.g., Methamidophos with PrecursorMZ 142.0086, ProductMZ 94.0046), use a data table library (R's readxl/writexl, Python pandas, or equivalent) to load the source format and export to the target format (.xlsx or .csv). Ensure column order and numeric precision are preserved—particularly for m/z values (4+ decimal places) and intensity integers. Verify file integrity post-export by spot-checking row counts, re-reading the exported file to confirm no silent truncation or type coercion occurred, and validating at least one reference compound entry matches the original. RT column may be omitted if not present in source data, but all other five columns are mandatory.

## Related tools

- **R Shiny** (Graphical interface for filtering and visualizing results from converted EISA-EXPOSOME database files; verifies file schema and data integrity post-export) — https://github.com/Lab-XUE/EISA-EXPOSOME

## Examples

```
# R example: readxl::read_excel('T3DB.xlsx') %>% writexl::write_xlsx('T3DB_exported.xlsx')
# Python example: pd.read_csv('transitions.csv').to_excel('transitions.xlsx', index=False)
```

## Evaluation signals

- Row count of source and exported file are identical; no rows silently dropped during conversion.
- All six required columns (NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID) are present in exported file with correct header names and order.
- Numeric precision preserved: PrecursorMZ and ProductMZ values retain ≥4 decimal places (e.g., 142.0086 → 142.0086, not 142); Intensity remains integer.
- Reference compound Methamidophos entries (PrecursorMZ 142.0086, ProductMZ 94.0046, Intensity 100, RT 2.182, ID 1) are bit-identical before and after conversion.
- Exported file loads without error in R Shiny interface and appears in filter visualization without schema warnings.

## Limitations

- RT (retention time) column is optional and may be absent; conversion must not fail or inject defaults if RT is missing—preserve empty or null values.
- Numeric precision loss can occur with certain libraries or locale settings (e.g., comma vs. period decimal separators in CSV); test on target system.
- Large files (>100k rows) may require chunked reading/writing to avoid memory exhaustion; single-load conversion may fail.
- XLSX and CSV differ in character encoding; ensure UTF-8 encoding is preserved, especially for compound names with special characters.

## Evidence

- [readme] Database schema requirement: "your file (.xlsx /.csv) must contain the following columns:|NAME|PrecursorMZ|ProductMZ|Intensity|RT|ID|, **RT** is not essential."
- [readme] Reference compound validation example: "|Methamidophos|142.0086|94.0046|100|2.182|1|"
- [readme] Provided T3DB database in XLSX format: "We also provide the compiled T3DB database file in .xlsx format."
- [readme] Accepted export formats for database files: "Export the validated database as .xlsx or .csv format and verify file integrity."
- [readme] R Shiny interface accepts both formats: "We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown below, and you can filter the results according to the visualisation interface！"
