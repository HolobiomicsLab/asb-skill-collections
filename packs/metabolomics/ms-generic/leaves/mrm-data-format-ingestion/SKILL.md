---
name: mrm-data-format-ingestion
description: Use when you have raw MRM lipidomics export files in vendor-specific formats (e.g., TSV or CSV from a mass spectrometry instrument) and need to convert them into a standardized tabular format before performing lipid identification, statistical analysis, or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pandas
  - Python
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.4c05039
  title: CLAW-MRM
evidence_spans:
- _No usage/docs found._
- streamline various tasks such as data parsing, matching, statistical analysis, and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_claw_mrm_cq
    doi: 10.1021/acs.analchem.4c05039
    title: CLAW-MRM
  dedup_kept_from: coll_claw_mrm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05039
  all_source_dois:
  - 10.1021/acs.analchem.4c05039
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mrm-data-format-ingestion

## Summary

Load and standardize vendor-specific MRM lipidomics export files (TSV, CSV) into a structured pandas DataFrame with validated, normalized column headers and data types. This is the entry point for downstream lipid nomenclature parsing, matching, and statistical analysis in MRM workflows.

## When to use

You have raw MRM lipidomics export files in vendor-specific formats (e.g., TSV or CSV from a mass spectrometry instrument) and need to convert them into a standardized tabular format before performing lipid identification, statistical analysis, or visualization. Apply this skill when raw exports contain inconsistent or vendor-specific column naming conventions and before any downstream matching or nomenclature decomposition.

## When NOT to use

- Input is already a validated, standardized feature table with consistent column schemas and confirmed numeric types.
- Data has already been parsed into a structured tabular format by upstream vendor software or prior workflow step.
- Raw export format is not tabular (e.g., binary mzML or NetCDF files that require dedicated parsers).

## Inputs

- Raw MRM export file (vendor-specific TSV or CSV format)
- Vendor format specification or sample export file
- Optional: column mapping configuration (header name aliases)

## Outputs

- Cleaned, structured CSV table with standardized headers
- One row per lipid feature per sample
- Data validation report (missing values, type mismatches, malformed IDs)

## How to apply

Load the raw MRM export file into a pandas DataFrame using the appropriate delimiter (TSV or CSV). Extract and standardize column headers by normalizing names to a consistent schema: retention time, m/z, intensity, lipid ID, and sample identifier. Validate data integrity by checking for missing values, confirming that m/z and intensity columns are numeric types, and flagging rows with malformed lipid identifiers. Handle vendor-specific format quirks (e.g., extra header rows, non-standard delimiters) as preprocessing steps before standardization. Output the cleaned, structured table as CSV with one row per lipid feature per sample, ensuring all rows pass validation.

## Related tools

- **pandas** (Load, parse, standardize column headers, and validate data types in TSV/CSV exports)
- **Python** (Language for implementing data ingestion and validation logic) — github.com/chopralab/CLAW

## Examples

```
import pandas as pd
df = pd.read_csv('raw_mrm_export.csv')
df.columns = df.columns.str.lower().str.strip()
df = df[['retention_time', 'm_z', 'intensity', 'lipid_id', 'sample_id']]
df[['m_z', 'intensity']] = df[['m_z', 'intensity']].apply(pd.to_numeric, errors='coerce')
df.to_csv('cleaned_mrm_data.csv', index=False)
```

## Evaluation signals

- All rows successfully loaded into pandas DataFrame with no I/O errors.
- Column headers match the standardized schema (retention time, m/z, intensity, lipid ID, sample identifier); no vendor-specific or extra columns remain in core fields.
- m/z and intensity columns have numeric dtype (float or int); no string values present in these columns.
- No rows with missing values in required fields (m/z, intensity, lipid ID); missing values are either imputed or rows are flagged/removed with justification logged.
- Lipid ID column contains no malformed entries (e.g., truncated IDs, special characters outside expected nomenclature); validation report documents any flagged rows.

## Limitations

- Vendor-specific export formats may have undocumented or inconsistent header row counts, delimiters, or encoding; preprocessing logic must be tailored per instrument vendor.
- Column name standardization assumes a fixed set of required fields; exports missing one or more core fields (e.g., no retention time) cannot be parsed and must be rejected or require manual mapping.
- No mechanism provided in the workflow description for handling multi-sheet Excel files (.xlsx) or binary formats; CSV/TSV ingestion only.
- Malformed lipid identifiers are flagged but not auto-corrected; manual curation or downstream regex-based repair is required before nomenclature decomposition.

## Evidence

- [other] Load raw MRM export file (vendor-specific format, e.g., TSV or CSV) into a pandas DataFrame.: "Load raw MRM export file (vendor-specific format, e.g., TSV or CSV) into a pandas DataFrame."
- [other] Extract and standardize column headers (retention time, m/z, intensity, lipid ID, sample identifier).: "Extract and standardize column headers (retention time, m/z, intensity, lipid ID, sample identifier)."
- [other] Validate data integrity: check for missing values, confirm numeric types for m/z and intensity columns, and flag rows with malformed lipid identifiers.: "Validate data integrity: check for missing values, confirm numeric types for m/z and intensity columns, and flag rows with malformed lipid identifiers."
- [readme] streamline various tasks such as data parsing, matching, statistical analysis, and visualization: "streamline various tasks such as data parsing, matching, statistical analysis, and visualization"
- [readme] Organize your lipidomics project by creating a project folder. This directory will serve as the central location for all project-related files, including raw data, processed results, plots, and other data files.: "Organize your lipidomics project by creating a project folder. This directory will serve as the central location for all project-related files"
