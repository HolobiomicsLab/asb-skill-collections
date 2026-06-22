---
name: data-format-compliance-checking
description: Use when mSMetaEnhancer fetches metadata from external services (CIR, CTS, PubChem, IDSM, BridgeDb) and must write enriched annotations (SMILES, InChI, CAS numbers, formulas, inchikeys, IUPAC names) into .msp files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MSMetaEnhancer
  - Python
  - pytest
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - RDKit
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-format-compliance-checking

## Summary

Validate fetched metadata against format-specific acceptance criteria before writing annotation values back to mass spectra files, ensuring data quality in metadata enrichment workflows. This skill applies attribute-level schema validation to converter output and logs compliance decisions for audit and quality assurance.

## When to use

Apply this skill when MSMetaEnhancer fetches metadata from external services (CIR, CTS, PubChem, IDSM, BridgeDb) and must write enriched annotations (SMILES, InChI, CAS numbers, formulas, inchikeys, IUPAC names) into .msp files. Use it whenever there is risk that API responses contain malformed, incomplete, or service-specific format variants that could corrupt downstream mass spectrometry analysis or violate file format specifications.

## When NOT to use

- Input metadata has already been validated by the source service and no downstream format transformation occurs
- Validation schema or format specifications for target attribute types are not available or cannot be defined
- Real-time annotation speed is the primary constraint and logging/validation overhead is unacceptable

## Inputs

- converter output dictionaries (parsed API responses from CIR, CTS, PubChem, IDSM, BridgeDb, RDKit)
- metadata attribute values (SMILES strings, InChI strings, CAS numbers, formulas, inchikeys, IUPAC names)
- service specifications and format documentation

## Outputs

- validated metadata annotations ready for .msp file write
- validation report file with pass/fail status for each attribute
- structured validation logs (attribute name, value, rule applied, result, service source)

## How to apply

Design a validation schema that defines acceptance criteria for each metadata attribute type based on service specifications (e.g., SMILES format validation, InChI prefix checking, CAS number structure verification). Implement a Validator class that intercepts converter output dictionaries and applies attribute-specific rules before metadata is committed to the spectra object. Integrate the Validator into the conversion pipeline between converter response parsing and spectra write, leveraging the existing Job and Converter architecture. Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured report file. Verify with unit tests that validation accepts correct formats and rejects malformed data for each supported attribute type, and confirm end-to-end with sample .msp files that only validated metadata reaches output files.

## Related tools

- **MSMetaEnhancer** (Annotation pipeline framework that integrates Validator into conversion workflow between response parsing and spectra write) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (Unit testing framework for verifying validation rules accept correct formats and reject malformed data) — https://docs.pytest.org/en/6.2.x/contents.html
- **CIR** (External service whose responses require validation before write (InChI, SMILES conversions)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (External service whose responses require validation before write) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (External service whose responses require validation (ISOMERIC_SMILES, CANONICAL_SMILES, formula formats)) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (External service whose responses require validation (formula, inchikey, IUPAC name formats)) — https://idsm.elixir-czech.cz/
- **BridgeDb** (External service whose responses require validation before write) — https://bridgedb.github.io/
- **RDKit** (Local compute converter whose outputs require validation before write)

## Examples

```
from MSMetaEnhancer import Application; from MSMetaEnhancer.libs.validators import Validator; app = Application(); app.load_data('sample.msp', file_format='msp'); validator = Validator(schema={'SMILES': 'smiles_format', 'InChI': 'inchi_prefix', 'CAS': 'cas_number_format'}); app.annotate_spectra_with_validation(validator, log_file='validation_report.txt')
```

## Evaluation signals

- Validation report logs show 100% coverage (every fetched attribute has a validation decision recorded)
- All attributes written to output .msp files pass their corresponding validation rules; no malformed SMILES, InChI, or CAS numbers appear in exported files
- Unit tests with pytest demonstrate rejection of known malformed formats (e.g., invalid SMILES syntax, InChI missing prefix, CAS number with wrong checksums) and acceptance of correct formats
- Validation logs capture service source for each attribute, enabling traceability of which service produced each value and which rule applied
- End-to-end test with sample .msp file shows validation logs record pass/fail decisions and only validated entries reach output file

## Limitations

- Validation schema must be manually defined for each supported attribute type and service; no automatic schema inference
- Format validation rules are specific to attribute and service; polymorphic responses (e.g., CANONICAL_SMILES vs ISOMERIC_SMILES from PubChem) require service-aware rule branching
- Validation overhead (logging, schema application) may impact asynchronous annotation performance if not carefully integrated; requires benchmarking
- If validation rules are too strict, valid but non-standard metadata will be rejected; if too lenient, malformed data will pass through

## Evidence

- [other] MSMetaEnhancer implements attribute validation tracked in logs to check fetched annotation values before they are written back to spectra, ensuring data quality during the metadata enrichment process.: "MSMetaEnhancer implements attribute validation tracked in logs to check fetched annotation values before they are written back to spectra, ensuring data quality during the metadata enrichment process."
- [other] Design a validation schema defining acceptance criteria for each metadata attribute type (e.g., SMILES format, InChI prefix, CAS number format) based on service specifications.: "Design a validation schema defining acceptance criteria for each metadata attribute type (e.g., SMILES format, InChI prefix, CAS number format) based on service specifications."
- [other] Implement a Validator class that intercepts converter output dictionaries and applies attribute-specific validation rules before metadata is committed to the spectra object.: "Implement a Validator class that intercepts converter output dictionaries and applies attribute-specific validation rules before metadata is committed to the spectra object."
- [other] Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file.: "Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](...), [CTS](...), [PubChem](...), [IDSM](...), and [BridgeDb](...).: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](...), [CTS](...), [PubChem](...), [IDSM](...), and [BridgeDb](...)."
