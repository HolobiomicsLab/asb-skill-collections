---
name: metadata-validation-rule-specification
description: Use when mSMetaEnhancer retrieves metadata attributes (SMILES, InChI, CAS numbers, IUPAC names, formulas) from external services (CIR, CTS, PubChem, IDSM, BridgeDb) and you need to guarantee that only correctly formatted values are written back to .msp output files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0081
  tools:
  - MSMetaEnhancer
  - Python
  - pytest
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- '**MSMetaEnhancer** is a tool used for `.msp` files annotation'
- '`MSMetaEnhancer/libs/converters/web/` named after your service'
- 'MSMetaEnhancer: A Python package for mass spectra metadata annotation'
- Create a new Python file in `MSMetaEnhancer/libs/converters/web/`
- make sure the existing tests still work by running ``pytest``
- 'fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer_cq
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer_cq
schema_version: 0.2.0
---

# metadata-validation-rule-specification

## Summary

Define and implement attribute-specific validation schemas that enforce format and content rules on metadata fetched from external services before writing to mass spectra files. This skill ensures data quality and consistency in MSMetaEnhancer's metadata enrichment pipeline by intercepting and validating converter output against predefined acceptance criteria.

## When to use

Apply this skill when MSMetaEnhancer retrieves metadata attributes (SMILES, InChI, CAS numbers, IUPAC names, formulas) from external services (CIR, CTS, PubChem, IDSM, BridgeDb) and you need to guarantee that only correctly formatted values are written back to .msp output files. Use it whenever converter output requires quality assurance before committing to spectra objects.

## When NOT to use

- Input metadata is already validated by upstream quality control or is sourced from trusted internal databases rather than external web services
- Use case requires accepting any fetched value regardless of format (e.g., exploratory or permissive annotation modes)
- Validation rules or service specifications are undefined or not documented for the metadata attributes being enriched

## Inputs

- .msp spectra files with unvalidated metadata annotations
- converter output dictionaries from web services (CIR, CTS, PubChem, IDSM, BridgeDb)
- attribute-type specifications and format requirements from service documentation

## Outputs

- .msp files with validated metadata annotations
- structured validation report log (attribute name, value, rule, pass/fail status, service source)
- validation statistics and reject/accept counts per attribute type

## How to apply

Design a validation schema that defines acceptance criteria for each metadata attribute type—for example, SMILES format validation, InChI prefix checking, CAS number format verification—based on service-specific specifications. Implement a Validator class that intercepts converter output dictionaries between response parsing and spectra write operations, applying attribute-specific validation rules using the existing Job and Converter architecture. Log all validation decisions (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured report. Unit test each attribute type with pytest to verify correct formats are accepted and malformed data rejected. End-to-end validation with sample .msp files confirms only validated metadata reaches output and all decisions are captured in validation logs.

## Related tools

- **MSMetaEnhancer** (Core platform for .msp file annotation; host for validator integration into Job and Converter architecture) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (Unit testing framework for validating acceptance of correct formats and rejection of malformed data per attribute type)
- **Python** (Language for implementing Validator class and validation schema definitions)
- **CIR** (External service providing chemical metadata subject to validation (e.g., InChI, SMILES conversion)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (External service providing chemical metadata subject to validation) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (External service providing chemical metadata subject to validation (e.g., ISOMERIC_SMILES, CANONICAL_SMILES)) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (External service providing chemical metadata subject to validation) — https://idsm.elixir-czech.cz/
- **BridgeDb** (External service providing chemical metadata subject to validation) — https://bridgedb.github.io/

## Examples

```
from MSMetaEnhancer.libs.validators import Validator; validator = Validator(schema={'SMILES': {'pattern': r'^[A-Za-z0-9()\[\]{}\\%=+#@-]*$'}, 'InChI': {'prefix': 'InChI='}, 'CAS': {'pattern': r'^\d{1,6}-\d{2}-\d'}}); result = validator.validate({'SMILES': 'CCO', 'InChI': 'InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3', 'CAS': '64-17-5'}); print(result)
```

## Evaluation signals

- Validation logs capture all metadata attributes with rule applied, pass/fail status, and source service; 100% traceability of decisions
- Unit tests confirm SMILES, InChI, CAS number, and other attribute formats are correctly accepted when well-formed and rejected when malformed
- End-to-end .msp output files contain only metadata that passed validation; no rejected values are written to spectra
- Validation report shows accept/reject counts and distribution by attribute type and service, revealing data quality patterns
- Structured validation schema schema file documents acceptance criteria for each attribute type with reference to service specifications

## Limitations

- Validation rules must be manually specified based on service documentation; incomplete or ambiguous service specs may result in overly permissive or overly strict schemas
- External service response formats may vary or change unexpectedly, requiring schema updates and test maintenance
- Validated-only approach may discard valid but non-standard metadata values if schema is too narrow; balance between strictness and coverage must be tuned empirically

## Evidence

- [other] Design a validation schema defining acceptance criteria for each metadata attribute type (e.g., SMILES format, InChI prefix, CAS number format) based on service specifications: "Design a validation schema defining acceptance criteria for each metadata attribute type (e.g., SMILES format, InChI prefix, CAS number format) based on service specifications."
- [other] Implement a Validator class that intercepts converter output dictionaries and applies attribute-specific validation rules before metadata is committed to the spectra object: "Implement a Validator class that intercepts converter output dictionaries and applies attribute-specific validation rules before metadata is committed to the spectra object."
- [other] Integrate the Validator into the conversion pipeline (between converter response parsing and spectra write) using the existing Job and Converter architecture: "Integrate the Validator into the conversion pipeline (between converter response parsing and spectra write) using the existing Job and Converter architecture."
- [other] Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file: "Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file."
- [other] MSMetaEnhancer implements attribute validation tracked in logs to check fetched annotation values before they are written back to spectra: "MSMetaEnhancer implements attribute validation tracked in logs to check fetched annotation values before they are written back to spectra, ensuring data quality during the metadata enrichment process."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR], [CTS], [PubChem], [IDSM], and [BridgeDb]: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR], [CTS], [PubChem], [IDSM], and [BridgeDb]."
