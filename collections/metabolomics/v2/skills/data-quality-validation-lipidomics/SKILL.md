---
name: data-quality-validation-lipidomics
description: Use when after loading and parsing raw MRM export files (TSV, CSV, or vendor-specific formats) into a pandas DataFrame and decomposing lipid nomenclature, before performing lipid matching, statistical analysis, or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - pandas
  - Python
  - Python regex (re module)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-quality-validation-lipidomics

## Summary

Validates the integrity and structural correctness of parsed MRM lipidomics data by checking for missing values, confirming numeric types in quantitative columns, and flagging malformed lipid identifiers before downstream matching and statistical analysis. This skill ensures data reliability and prevents propagation of corrupted records into analysis workflows.

## When to use

After loading and parsing raw MRM export files (TSV, CSV, or vendor-specific formats) into a pandas DataFrame and decomposing lipid nomenclature, before performing lipid matching, statistical analysis, or visualization. Apply this skill whenever you have converted raw instrument output into a structured tabular format and need to confirm it meets minimum quality standards for downstream processing.

## When NOT to use

- Input is already a feature table from a vendor-supplied, pre-validated processing pipeline (e.g., analyst software output confirmed free of parsing errors).
- Data has already undergone quality control and integrity checks in a prior workflow step.
- Raw instrument output is in a binary or compressed format (e.g., .d, .raw) that has not yet been converted to text-based or structured tabular form.

## Inputs

- Parsed pandas DataFrame with standardized columns (retention time, m/z, intensity, lipid ID, sample identifier)
- Lipid nomenclature specification or regex pattern defining valid lipid class and chain composition formats

## Outputs

- Cleaned, validated CSV table with one row per lipid feature per sample
- Validation report or log file listing flagged rows, missing values, type mismatches, and malformed identifiers

## How to apply

After parsing the raw MRM export file and standardizing column headers (retention time, m/z, intensity, lipid ID, sample identifier), systematically validate: (1) scan for missing values in critical numeric columns (m/z, intensity) and flag rows with NaN or null entries; (2) confirm that m/z and intensity columns are numeric types (float or int, not string); (3) apply regex or string-based pattern matching to lipid identifiers to detect malformed nomenclature (e.g., missing chain composition, incorrect class prefix, or invalid modification syntax); (4) log all validation failures with row indices and failure reasons to enable targeted remediation. Rows that fail any check should be flagged and optionally removed before output. The validated, cleaned dataset is output as a CSV with one row per lipid feature per sample, ready for matching and statistical analysis.

## Related tools

- **pandas** (DataFrame loading, column standardization, missing value detection, and type confirmation for numeric columns)
- **Python regex (re module)** (Pattern matching and decomposition of lipid nomenclature to detect malformed identifiers)

## Examples

```
import pandas as pd; df = pd.read_csv('raw_mrm_export.csv'); df = df.dropna(subset=['m/z', 'intensity']); df['m/z'] = pd.to_numeric(df['m/z'], errors='coerce'); df['intensity'] = pd.to_numeric(df['intensity'], errors='coerce'); invalid = df[df['m/z'].isna() | df['intensity'].isna()]; print(f'Flagged {len(invalid)} rows with invalid m/z or intensity'); df_clean = df.dropna(subset=['m/z', 'intensity']); df_clean.to_csv('validated_mrm_data.csv', index=False)
```

## Evaluation signals

- All rows in output CSV have non-null values in m/z and intensity columns, or missing values are explicitly documented in the validation log.
- m/z and intensity columns are confirmed as numeric type (float or int); no string-type entries remain in these fields.
- Every lipid identifier in the output conforms to the specified nomenclature regex pattern (e.g., lipid class prefix, chain composition, and modification state are parseable and complete).
- Validation log lists all flagged rows with row index, column name, and specific failure reason (e.g., 'NaN in intensity', 'malformed lipid ID').
- Output row count equals input row count minus flagged/removed rows; discrepancy is documented and justified.

## Limitations

- Validation logic is dependent on correct specification of lipid nomenclature regex patterns; incorrect or incomplete patterns may fail to detect genuinely malformed identifiers or produce false positives.
- Missing values in non-critical metadata columns (e.g., sample notes) are not flagged by default; custom logic may be needed if such columns are required downstream.
- The skill does not detect semantic errors (e.g., physically impossible m/z values for a given lipid class or retention times inconsistent with the instrumental method) — only syntactic and type-level errors.
- Vendor-specific export format variations (column names, delimiter, encoding) may require case-by-case parser tuning before validation can proceed reliably.

## Evidence

- [other] Validate data integrity: check for missing values, confirm numeric types for m/z and intensity columns, and flag rows with malformed lipid identifiers.: "Validate data integrity: check for missing values, confirm numeric types for m/z and intensity columns, and flag rows with malformed lipid identifiers."
- [readme] streamline various tasks such as data parsing, matching, statistical analysis, and visualization: "streamline various tasks such as data parsing, matching, statistical analysis, and visualization"
- [other] Output cleaned, structured table as CSV with one row per lipid feature per sample.: "Output cleaned, structured table as CSV with one row per lipid feature per sample."
