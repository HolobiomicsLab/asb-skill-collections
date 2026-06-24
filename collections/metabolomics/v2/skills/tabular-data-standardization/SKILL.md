---
name: tabular-data-standardization
description: Use when when you have received raw MRM lipidomics export files in vendor-specific
  formats (TSV, CSV) with inconsistent column naming, unparsed lipid identifiers (e.g.,
  'PC(36:1)' as a single string), and unknown data quality issues.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - pandas
  - Python
  - Python regex (re module)
  - Lipid_MRM_parser.ipynb
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.4c05039
  title: CLAW-MRM
evidence_spans:
- _No usage/docs found._
- streamline various tasks such as data parsing, matching, statistical analysis, and
  visualization
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

# tabular-data-standardization

## Summary

Transform vendor-specific raw MRM lipidomics export files into a normalized, machine-readable tabular format by parsing headers, decomposing lipid nomenclature, and validating data integrity. This skill enables downstream matching, statistical analysis, and visualization by ensuring consistent column structure and data types across heterogeneous input sources.

## When to use

When you have received raw MRM lipidomics export files in vendor-specific formats (TSV, CSV) with inconsistent column naming, unparsed lipid identifiers (e.g., 'PC(36:1)' as a single string), and unknown data quality issues. Apply this skill before attempting lipid matching, statistical testing, or visualization to ensure all rows conform to a validated, decomposed schema.

## When NOT to use

- Input is already a validated, normalized feature table with decomposed lipid fields
- Raw data contains only aggregate lipid totals without individual feature-level intensity measurements
- Vendor export format is binary or proprietary (non-text) — use format conversion first

## Inputs

- Vendor-specific MRM lipidomics export file (TSV or CSV format)
- Raw intensity measurements and m/z values (unvalidated)
- Unparsed lipid identifiers (e.g., 'PC(36:1)', 'PE(38:2)-OH')
- Sample metadata (sample identifiers, group labels)

## Outputs

- Standardized CSV table with canonical column headers
- Decomposed lipid nomenclature fields (lipid_class, chain_composition, modification)
- Validated numeric columns (m/z, retention_time, intensity)
- Data quality report (missing values, malformed identifiers, type mismatches)

## How to apply

Load the raw vendor export into a pandas DataFrame and inspect column headers. Standardize header names to canonical forms (retention time, m/z, intensity, lipid ID, sample identifier). Use regex or string-split operations to parse lipid nomenclature into separate fields: lipid class (e.g., PC), chain composition (e.g., 36:1), and modification state (e.g., oxidation, hydroxylation). Validate data integrity by checking for missing values, confirming m/z and intensity columns are numeric, and flagging rows with malformed lipid identifiers or out-of-range values. Output the cleaned, structured table as CSV with one row per lipid feature per sample and consistent data types across all columns.

## Related tools

- **pandas** (Load, inspect, and transform vendor CSV/TSV export into standardized DataFrame; perform column renaming, data type conversion, and validation)
- **Python regex (re module)** (Parse lipid nomenclature strings to extract lipid class, chain composition, and modification state into separate fields)
- **Lipid_MRM_parser.ipynb** (Jupyter notebook implementing the full data parsing workflow including loading, standardization, parsing, validation, and output) — github.com/chopralab/CLAW

## Examples

```
df = pd.read_csv('raw_mrm_export.tsv', sep='\t'); df.columns = ['retention_time', 'm_z', 'intensity', 'lipid_id', 'sample']; df[['lipid_class', 'chain', 'mod']] = df['lipid_id'].str.extract(r'(\w+)\((\d+:\d+)\)(-\w+)?'); df = df.dropna(subset=['m_z', 'intensity']); df['m_z'] = pd.to_numeric(df['m_z']); df.to_csv('standardized_lipid_data.csv', index=False)
```

## Evaluation signals

- All rows in the output CSV have identical column structure with no missing headers
- m/z and intensity columns are numeric type (float/int) with no non-numeric entries
- Lipid identifiers successfully decomposed into separate fields with no null values or malformed entries
- No rows contain missing values in critical fields (m/z, intensity, lipid_id, sample_identifier)
- Output row count matches input row count (no silent data loss except flagged-invalid rows)

## Limitations

- Regex patterns for lipid nomenclature parsing must be tailored to the specific vendor nomenclature standard (Lipid Maps, SwissLipids, etc.); no universal parser is provided
- Validation checks are schema-based and do not detect biological implausibility (e.g., m/z outside expected range for lipid class or retention time drift across samples)
- No changelog is available to document version-specific changes to parsing rules or validation thresholds

## Evidence

- [other] Extract and standardize column headers (retention time, m/z, intensity, lipid ID, sample identifier): "Extract and standardize column headers (retention time, m/z, intensity, lipid ID, sample identifier)"
- [other] Parse lipid nomenclature using regex or string-split operations to decompose lipid class, chain composition, and modification state into separate fields: "Parse lipid nomenclature using regex or string-split operations to decompose lipid class, chain composition, and modification state into separate fields"
- [other] Validate data integrity: check for missing values, confirm numeric types for m/z and intensity columns, and flag rows with malformed lipid identifiers: "Validate data integrity: check for missing values, confirm numeric types for m/z and intensity columns, and flag rows with malformed lipid identifiers"
- [other] Load raw MRM export file (vendor-specific format, e.g., TSV or CSV) into a pandas DataFrame: "Load raw MRM export file (vendor-specific format, e.g., TSV or CSV) into a pandas DataFrame"
- [readme] streamline various tasks such as data parsing, matching, statistical analysis, and visualization: "streamline various tasks such as data parsing, matching, statistical analysis, and visualization"
