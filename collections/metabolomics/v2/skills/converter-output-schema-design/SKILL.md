---
name: converter-output-schema-design
description: Use when when integrating multiple heterogeneous metadata services (e.g.,
  CIR, CTS, PubChem, IDSM, BridgeDb) that return unstructured or variably-formatted
  responses, and you need to enforce uniform output contracts before committing fetched
  values to mass spectra files (.msp format).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - MSMetaEnhancer
  - Python
  - pytest
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  license_tier: open
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.04494
  all_source_dois:
  - 10.21105/joss.04494
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# converter-output-schema-design

## Summary

Design and implement a structured schema that defines the output format and validation rules for metadata converters in annotation pipelines. This skill ensures consistent, validated data structure across heterogeneous external service responses before metadata is written to spectra files.

## When to use

When integrating multiple heterogeneous metadata services (e.g., CIR, CTS, PubChem, IDSM, BridgeDb) that return unstructured or variably-formatted responses, and you need to enforce uniform output contracts before committing fetched values to mass spectra files (.msp format).

## When NOT to use

- Input is a single, pre-validated, homogeneous data source (schema design is overkill; direct write is sufficient).
- You do not intend to write metadata back to spectra files (schema enforcement is unnecessary if data is only for inspection).
- All converters already guarantee format compliance and your pipeline has no requirement for traceability or rejection of malformed data.

## Inputs

- converter output dictionary (raw response from external service)
- converter service specification (e.g., CIR, CTS, PubChem API documentation)
- input .msp file with compound names and partial metadata

## Outputs

- validated metadata dictionary with pass/fail status per attribute
- structured validation report file (logs attribute name, fetched value, validation rule, pass/fail, service source)
- annotated .msp file with only validated metadata written back to spectra

## How to apply

First, identify all metadata attribute types that converters will produce (e.g., SMILES, InChI, CAS number, formula, InChIKey, IUPAC name) and their service-specific specifications. Design a schema document that defines acceptance criteria for each attribute—such as SMILES format validation, InChI prefix requirements (InChI=1S/), CAS number format rules, and presence/absence constraints. Implement this schema as a Validator class that intercepts converter output dictionaries and applies attribute-specific validation rules before metadata is committed to the spectra object. Integrate the Validator into the conversion pipeline between converter response parsing and spectra write operations, using the existing Job and Converter architecture. Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file for traceability and debugging.

## Related tools

- **MSMetaEnhancer** (orchestration framework that loads .msp files, coordinates converter calls (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit), and writes validated metadata back to output spectra) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (test framework for unit testing validator acceptance of correct formats and rejection of malformed data for each attribute type) — https://docs.pytest.org/en/6.2.x/contents.html
- **Python** (language for implementing Validator class and integrating schema validation into Job/Converter pipeline)
- **CIR** (chemical structure service producing SMILES and InChI outputs subject to schema validation) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (chemical identifier translation service producing multiple metadata types subject to schema validation) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (chemical database service producing SMILES variants, InChI, and formula subject to schema validation) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (metabolite database service producing InChI, formula, InChIKey, IUPAC name subject to schema validation) — https://idsm.elixir-czech.cz/
- **BridgeDb** (identifier mapping service producing cross-references subject to schema validation) — https://bridgedb.github.io/

## Examples

```
from MSMetaEnhancer.libs.converters import Validator; validator = Validator(schema={'inchi': {'prefix': 'InChI=1S/'}, 'smiles': {'regex': r'^[A-Za-z0-9@H()\[\]\-=#\\/]+$'}, 'cas_number': {'regex': r'^\d{1,7}-\d{2}-\d$'}}); result = validator.validate({'inchi': 'InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H', 'smiles': 'c1ccccc1', 'cas_number': '71-43-2'}); print(result['status'], result['log'])
```

## Evaluation signals

- Validation schema correctly accepts well-formed SMILES (linear/branched structures), InChI (prefix InChI=1S/), CAS numbers (digits and hyphens), and rejects malformed variants of each.
- Validator rejects converter outputs missing required fields or containing null/empty values where presence is mandated by schema.
- Structured validation report logs 100% of converter outputs with attribute name, fetched value, rule applied, pass/fail status, and service source; every entry is traceable.
- Unit tests using pytest verify that each attribute type (SMILES, InChI, CAS, formula, InChIKey, IUPAC name) passes when correctly formatted and fails when malformed.
- End-to-end test with sample .msp file confirms only validated metadata reaches output .msp file and invalid entries are excluded, with validation logs capturing all decisions.

## Limitations

- Schema must be maintained and updated whenever converter service APIs change their response formats or add new attributes, requiring manual intervention.
- Validation rules are service-specification-dependent and may conflict (e.g., different canonicalization rules for SMILES across CIR, CTS, and PubChem); schema may need per-service overrides.
- Validation does not guarantee semantic correctness (e.g., a well-formed SMILES string may still represent the wrong chemical structure); only syntactic/format compliance is checked.
- Rate limiting and API errors from external services are handled separately in converter code and are not the responsibility of schema validation; schema only validates successfully-fetched data.

## Evidence

- [other] Design a validation schema defining acceptance criteria for each metadata attribute type (e.g., SMILES format, InChI prefix, CAS number format) based on service specifications.: "Design a validation schema defining acceptance criteria for each metadata attribute type (e.g., SMILES format, InChI prefix, CAS number format) based on service specifications."
- [other] Implement a Validator class that intercepts converter output dictionaries and applies attribute-specific validation rules before metadata is committed to the spectra object.: "Implement a Validator class that intercepts converter output dictionaries and applies attribute-specific validation rules before metadata is committed to the spectra object."
- [other] Integrate the Validator into the conversion pipeline (between converter response parsing and spectra write) using the existing Job and Converter architecture.: "Integrate the Validator into the conversion pipeline (between converter response parsing and spectra write) using the existing Job and Converter architecture."
- [other] Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file.: "Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file."
- [other] MSMetaEnhancer implements attribute validation tracked in logs to check fetched annotation values before they are written back to spectra, ensuring data quality during the metadata enrichment process.: "MSMetaEnhancer implements attribute validation tracked in logs to check fetched annotation values before they are written back to spectra, ensuring data quality during the metadata enrichment process."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR], [CTS], [PubChem], [IDSM], and [BridgeDb].: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR], [CTS], [PubChem], [IDSM], and [BridgeDb]."
- [other] Add unit tests using pytest that verify validation accepts correct formats and rejects malformed data for each supported attribute type.: "Add unit tests using pytest that verify validation accepts correct formats and rejects malformed data for each supported attribute type."
