---
name: excel-template-parsing
description: Use when when you have an Excel file downloaded from InjectionDesign's template or conforming to its schema, and you need to extract sample identifiers, classification dimensions (up to three), and QC type labels (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, or custom) into a structured.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_3520
  tools:
  - InjectionDesign
  - pandas
  - openpyxl
derived_from:
- doi: 10.1101/2023.02.26.530140v1.article-info
  title: InjectionDesign
evidence_spans:
- LC/GC-MS-based Multi-Omics Injection-Plate Design Web Service
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_injectiondesign_cq
    doi: 10.1101/2023.02.26.530140v1.article-info
    title: InjectionDesign
  dedup_kept_from: coll_injectiondesign_cq
schema_version: 0.2.0
---

# excel-template-parsing

## Summary

Parse uploaded Excel files conforming to an InjectionDesign template schema into a structured sample list with support for multiple classification dimensions and QC type designation. This skill enables systematic conversion of user-supplied sample metadata into a machine-readable format ready for injection-plate design optimization.

## When to use

When you have an Excel file downloaded from InjectionDesign's template or conforming to its schema, and you need to extract sample identifiers, classification dimensions (up to three), and QC type labels (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, or custom) into a structured data object for downstream plate design and randomization workflows.

## When NOT to use

- Input file does not conform to InjectionDesign template schema (missing required columns or incompatible data types) — validate schema first or re-download template.
- Sample metadata already exists as a validated structured object (JSON, database table, or feature table) — skip parsing and load directly.
- Excel file is corrupted, password-protected, or unreadable by the parser — recover or export as CSV before attempting parsing.

## Inputs

- Excel file (.xlsx or .xls) conforming to InjectionDesign template schema
- Template schema specification (column headers, data types, required fields)
- Sample metadata rows with identifier, classification dimensions, and QC type

## Outputs

- Structured sample list (JSON or CSV) with flattened or hierarchical records
- Parsed sample objects containing: sample identifier, classification dimensions (1–3), QC type label
- Validation report (null-check results, schema compliance summary)

## How to apply

Load the uploaded Excel file using a spreadsheet parser (e.g., pandas.read_excel or openpyxl). Validate that column headers match the InjectionDesign template schema and that required fields are present. Extract each sample row and map it to a record containing: sample identifier, up to three classification dimensions (preserved in their hierarchy), and QC type designation. Flatten or structure the records hierarchically depending on downstream requirements (JSON or CSV). Verify that no required fields are null and that classification values are consistent with the template's allowed vocabulary before output.

## Related tools

- **InjectionDesign** (Template definition and web service for sample list upload, modification, and visualization; defines the Excel schema and QC type taxonomy) — https://github.com/CSi-Studio/InjectionDesign
- **pandas** (Spreadsheet parser for loading and validating Excel files; enables row extraction and data transformation)
- **openpyxl** (Alternative spreadsheet parser for Excel file I/O with schema-level access to cell metadata)

## Examples

```
import pandas as pd
df = pd.read_excel('sample_template.xlsx')
samples = [{'id': row['Sample_ID'], 'dimensions': [row['Dim1'], row['Dim2'], row['Dim3']], 'qc_type': row['QC_Type']} for _, row in df.iterrows()]
json.dump(samples, open('parsed_samples.json', 'w'))
```

## Evaluation signals

- All parsed sample records contain non-null identifiers, classification dimensions (1–3), and QC type matching the set {Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, custom QC}.
- Row count and column headers in output match the input Excel file after filtering header row.
- Classification dimension values are consistent with the template's controlled vocabulary (no unexpected or malformed values).
- Output JSON/CSV structure is valid and deserializable; hierarchical nesting (if applied) preserves all original classification information without loss.
- No sample identifiers are duplicated unless explicitly allowed by the template design; audit for accidental duplicates.

## Limitations

- Parser supports only Excel files (.xlsx, .xls) conforming to the InjectionDesign template; non-standard formats or custom schemas require schema redefinition.
- Support is limited to up to three classification dimensions as per InjectionDesign specification; additional dimensions require redesign of the template.
- QC types are constrained to InjectionDesign's predefined set (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, one custom QC); custom QC types beyond this set may require manual post-processing.
- No validation of downstream plate design feasibility (e.g., whether the number or distribution of samples can be accommodated on physical plates) occurs during parsing; plate-level validation occurs in subsequent workflow steps.

## Evidence

- [other] InjectionDesign accepts uploaded Excel files conforming to a downloadable template and converts them into a modifiable sample list: "InjectionDesign accepts uploaded Excel files conforming to a downloadable template and converts them into a modifiable sample list"
- [other] Extract sample metadata rows and map each row to a sample record with sample identifier, classification dimensions (up to three), and QC type designation: "Extract sample metadata rows and map each row to a sample record with sample identifier, classification dimensions (up to three), and QC type designation"
- [other] Load the uploaded Excel file using a spreadsheet parser (e.g., pandas or openpyxl). Validate that the file structure matches the InjectionDesign template schema (column headers, data types, required fields).: "Load the uploaded Excel file using a spreadsheet parser (e.g., pandas or openpyxl). Validate that the file structure matches the InjectionDesign template schema"
- [intro] InjectionDesign supports visual presentation of up to three classification dimensions for sample lists: "InjectionDesign supports visual presentation of up to three classification dimensions"
- [readme] InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC: "InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC"
- [readme] Click "Download Sample Excel" button to download the template excel. Then fill the basic information of samples to the excel and upload the file.: "Click "Download Sample Excel" button to download the template excel. Then fill the basic information of samples to the excel and upload the file."
- [other] Output the parsed sample list as a structured JSON or CSV file with flattened or hierarchical records for downstream injection-plate design: "Output the parsed sample list as a structured JSON or CSV file with flattened or hierarchical records for downstream injection-plate design"
