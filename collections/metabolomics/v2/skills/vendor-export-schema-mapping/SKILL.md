---
name: vendor-export-schema-mapping
description: Use when raw MRM lipidomics data arrives in vendor-specific export formats
  (e.g., Sciex, Waters, Thermo TSV/CSV) with inconsistent or proprietary column naming,
  numeric encoding, and lipid nomenclature.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - pandas
  - Python
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

# vendor-export-schema-mapping

## Summary

Transform vendor-specific raw MRM lipidomics export files (TSV, CSV, vendor proprietary formats) into a standardized tabular schema by extracting, validating, and normalizing column headers and data types. This enables downstream matching, statistical analysis, and visualization workflows.

## When to use

Raw MRM lipidomics data arrives in vendor-specific export formats (e.g., Sciex, Waters, Thermo TSV/CSV) with inconsistent or proprietary column naming, numeric encoding, and lipid nomenclature. Apply this skill when you must ingest heterogeneous vendor outputs into a unified pipeline that expects consistent column headers (retention time, m/z, intensity, lipid ID, sample identifier) and validated numeric types before matching or statistical analysis.

## When NOT to use

- Input is already a validated, standardized feature table with normalized headers and decomposed lipid nomenclature fields.
- Data originates from a standardized, open format (e.g., mzML) that does not require vendor-specific schema mapping.
- Lipid nomenclature is already parsed into separate structured fields in the input.

## Inputs

- vendor-specific MRM export file (TSV or CSV format)
- sample identifier mapping (optional, for enriching with sample metadata)
- lipid nomenclature patterns or reference (for decomposition)

## Outputs

- cleaned, standardized CSV table with normalized column headers
- one row per lipid feature per sample
- decomposed lipid fields (class, chain composition, modification state)
- data quality report flagging missing or malformed rows

## How to apply

Load the vendor export file into a pandas DataFrame using appropriate delimiters (TSV or CSV). Extract and standardize column headers by mapping vendor-specific names to canonical names (e.g., 'RetTime' → 'retention_time', 'MZ' → 'm/z', 'Area' → 'intensity'). Validate data integrity by checking for missing values in critical columns, confirming that m/z and intensity columns are numeric (not strings), and parsing lipid nomenclature into decomposed fields (lipid class, chain composition, modification state) using regex or string-split operations. Flag rows with malformed lipid identifiers or out-of-range values. Output the cleaned, structured table as CSV with one row per lipid feature per sample, ready for downstream processing.

## Related tools

- **pandas** (DataFrame loading, column header extraction, standardization, and data validation for vendor export schema mapping)
- **Python** (Implementation language for regex parsing, string-split operations, and data integrity validation of lipid nomenclature)

## Examples

```
import pandas as pd; df = pd.read_csv('vendor_export.tsv', sep='\t'); df.rename(columns={'RetTime': 'retention_time', 'MZ': 'm/z', 'Area': 'intensity'}, inplace=True); df[['m/z', 'intensity']] = df[['m/z', 'intensity']].apply(pd.to_numeric); df.to_csv('standardized_lipids.csv', index=False)
```

## Evaluation signals

- All critical columns (retention_time, m/z, intensity, lipid_id, sample_id) are present and have expected names after standardization.
- m/z and intensity columns have numeric dtype (float or int), not string; no conversion errors or NaN artefacts introduced.
- Lipid nomenclature is successfully decomposed into separate fields (lipid_class, chain_composition, modification_state) with no rows dropped due to regex mismatch.
- No missing values in critical columns; any rows with missing values are flagged in a data quality report.
- Output CSV row count matches expected sample × feature count; spot-check several rows to confirm header alignment and value preservation.

## Limitations

- Vendor export format must be TSV or CSV; proprietary binary formats require vendor-specific parsing libraries not addressed in this workflow.
- Lipid nomenclature parsing relies on regex or string-split heuristics; non-standard or ambiguous lipid identifiers in the vendor export may fail to decompose correctly and must be manually reviewed or flagged.
- No automated detection of vendor format variant; user must specify or infer correct delimiter, encoding, and header row index from the raw file.
- Schema mapping assumes a fixed set of expected columns; vendors with completely novel or missing column types may require ad-hoc extension.

## Evidence

- [other] Load raw MRM export file (vendor-specific format, e.g., TSV or CSV) into a pandas DataFrame.: "Load raw MRM export file (vendor-specific format, e.g., TSV or CSV) into a pandas DataFrame."
- [other] Extract and standardize column headers (retention time, m/z, intensity, lipid ID, sample identifier).: "Extract and standardize column headers (retention time, m/z, intensity, lipid ID, sample identifier)."
- [other] Parse lipid nomenclature using regex or string-split operations to decompose lipid class, chain composition, and modification state into separate fields.: "Parse lipid nomenclature using regex or string-split operations to decompose lipid class, chain composition, and modification state into separate fields."
- [other] Validate data integrity: check for missing values, confirm numeric types for m/z and intensity columns, and flag rows with malformed lipid identifiers.: "Validate data integrity: check for missing values, confirm numeric types for m/z and intensity columns, and flag rows with malformed lipid identifiers."
- [readme] streamline various tasks such as data parsing, matching, statistical analysis, and visualization: "streamline various tasks such as data parsing, matching, statistical analysis, and visualization"
