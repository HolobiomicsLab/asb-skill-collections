---
name: sample-metadata-extraction
description: Use when when you have an Excel file uploaded by a user following the InjectionDesign template schema and need to convert it into a modifiable, structured sample list that preserves up to three classification dimensions and QC type assignments for LC/GC-MS multi-omics experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - InjectionDesign
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2023.02.26.530140v1.article-info
  all_source_dois:
  - 10.1101/2023.02.26.530140v1.article-info
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-metadata-extraction

## Summary

Extract and validate sample metadata from Excel templates conforming to a standardized schema, mapping rows to structured sample records with identifiers, classification dimensions, and QC type designations. This skill bridges user-supplied sample data and downstream injection-plate design workflows.

## When to use

When you have an Excel file uploaded by a user following the InjectionDesign template schema and need to convert it into a modifiable, structured sample list that preserves up to three classification dimensions and QC type assignments for LC/GC-MS multi-omics experiments.

## When NOT to use

- Input file does not conform to the downloadable InjectionDesign template schema — validation will fail.
- Sample metadata already exists as a validated structured format (JSON/CSV) — parsing is unnecessary.
- More than three classification dimensions are required — InjectionDesign only supports visual presentation of up to three dimensions.

## Inputs

- Excel file conforming to InjectionDesign template schema
- Template schema specification (column headers, data types, required fields)

## Outputs

- Structured sample list (JSON or CSV) with flattened/hierarchical sample records
- Sample metadata including identifier, classification dimensions, and QC type

## How to apply

Load the uploaded Excel file using a spreadsheet parser (e.g., pandas or openpyxl). Validate that the file structure matches the InjectionDesign template schema, checking column headers, data types, and required fields. Extract each sample metadata row and map it to a sample record, capturing the sample identifier, up to three classification dimensions (e.g., tissue type, treatment, batch), and QC type designation (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, or custom QC). Output the parsed sample list as a structured JSON or CSV file with flattened or hierarchical records suitable for inter-batch balancing and intra-batch randomization in the subsequent injection-plate design step.

## Related tools

- **InjectionDesign** (Web service that accepts the parsed and validated sample list; orchestrates downstream injection-plate design, QC predefinition, inter-batch balancing, and intra-batch randomization) — https://github.com/CSi-Studio/InjectionDesign

## Evaluation signals

- All rows from the Excel file are successfully mapped to sample records with no parsing errors or null identifiers.
- Classification dimension counts do not exceed three per sample; any samples exceeding this threshold are flagged or rejected with a clear error message.
- Each sample is assigned one of the five predefined QC types (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, or custom QC) or raises a validation error.
- Output JSON/CSV schema matches the expected hierarchical or flattened structure and is readable by downstream InjectionDesign plate-design functions.
- All required template columns (as defined by the schema specification) are present and contain valid data types; missing or malformed fields are logged.

## Limitations

- Supports only Excel files conforming to the downloadable InjectionDesign template schema; non-conformant files will fail schema validation.
- Visual presentation is limited to a maximum of three classification dimensions; samples with more dimensions cannot be fully displayed by InjectionDesign.
- QC type assignment is restricted to five predefined types (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, and one custom QC); custom types beyond one may not be supported.
- No explicit handling of missing or ambiguous sample metadata; validation may require manual curation before downstream use.

## Evidence

- [other] Load the uploaded Excel file using a spreadsheet parser (e.g., pandas or openpyxl). 2. Validate that the file structure matches the InjectionDesign template schema (column headers, data types, required fields).: "Load the uploaded Excel file using a spreadsheet parser (e.g., pandas or openpyxl). 2. Validate that the file structure matches the InjectionDesign template schema (column headers, data types,"
- [other] Extract sample metadata rows and map each row to a sample record with sample identifier, classification dimensions (up to three), and QC type designation (Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC, or custom QC).: "Extract sample metadata rows and map each row to a sample record with sample identifier, classification dimensions (up to three), and QC type designation (Blank QC, Solvent QC, Pooled QC, Long-Term"
- [readme] Click "Download Sample Excel" button to download the template excel. Then fill the basic information of samples to the excel and upload the file.: "Click "Download Sample Excel" button to download the template excel. Then fill the basic information of samples to the excel and upload the file."
- [readme] InjectionDesign supports visual presentation of up to three classification dimensions.: "InjectionDesign supports visual presentation of up to three classification dimensions."
- [readme] InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC.: "InjectionDesign predefined four QC type: Blank QC, Solvent QC, Pooled QC, Long-Term Reference QC. and one custom QC."
