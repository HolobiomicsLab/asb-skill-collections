---
name: logging-and-audit-trail-generation
description: Use when when implementing a metadata annotation pipeline for mass spectra
  that fetches values from multiple external services (e.
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
  license_tier: open
  provenance_tier: literature
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

# logging-and-audit-trail-generation

## Summary

Implement structured logging of metadata validation decisions during mass spectra annotation to create an audit trail that records which attributes were validated, their source services, pass/fail outcomes, and the validation rules applied. This skill ensures reproducibility and traceability of metadata enrichment operations in .msp files.

## When to use

When implementing a metadata annotation pipeline for mass spectra that fetches values from multiple external services (e.g., CIR, CTS, PubChem, IDSM, BridgeDb) and you need to demonstrate data quality control, track which records succeeded or failed validation, or provide evidence of which service provided each annotation value for regulatory or reproducibility purposes.

## When NOT to use

- Input metadata has already been manually curated and validated by an expert; logging adds overhead without new information.
- You require real-time streaming validation with sub-millisecond latency; structured logging introduces I/O overhead.
- The annotation services already provide cryptographic signatures or trust-chain guarantees; audit logging becomes redundant.

## Inputs

- converter output dictionaries (parsed API responses from web services)
- mass spectra file in .msp format with compound identifiers
- validation schema defining format rules per attribute type (e.g., SMILES regex, InChI prefix, CAS number pattern)

## Outputs

- validated metadata dictionaries committed to spectra objects
- structured validation report file (JSON or CSV) with per-attribute decision records
- annotated .msp file containing only validated metadata

## How to apply

Insert a Validator class into the conversion pipeline immediately after converter response parsing but before metadata is committed to the spectra object. For each fetched attribute (SMILES, InChI, CAS number, etc.), apply service-specific validation rules and log the result with: attribute name, fetched value, validation rule applied, pass/fail status, and service source. Write all validation decisions to a structured validation report file (e.g., JSON or CSV) that can be parsed for summary statistics. Run end-to-end tests with sample .msp files to confirm that only validated metadata appears in output files and that the validation log captures all decisions without omissions.

## Related tools

- **MSMetaEnhancer** (target application orchestrating metadata annotation and conversion pipeline; validation logging integrates at the converter→spectra commit boundary) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (unit testing framework to verify validation rules accept correct formats and reject malformed data for each supported attribute type)
- **Python** (implementation language for Validator class and logging infrastructure)
- **CIR** (example external service providing chemical identifiers; validation must confirm SMILES and InChI formats before logging acceptance) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (example external service providing chemical identifiers; validation must confirm format compliance before logging acceptance) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (example external service providing chemical identifiers and CAS numbers; validation must confirm format before logging acceptance) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (example external service providing chemical identifiers; validation must confirm format before logging acceptance) — https://idsm.elixir-czech.cz/
- **BridgeDb** (example external service providing chemical identifiers; validation must confirm format before logging acceptance) — https://bridgedb.github.io/

## Examples

```
from MSMetaEnhancer import Application
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.validators import Validator

app = Application()
app.load_data('sample.msp', file_format='msp')
validator = Validator(validation_schema='schemas/metadata_formats.json', log_file='validation_report.json')
app.register_validator(validator)
asyncio.run(app.annotate_spectra(services=['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb'], jobs=[('name', 'inchi', 'IDSM')]))
app.save_data('sample_out.msp', file_format='msp')
```

## Evaluation signals

- Validation report file is created and contains one log entry per metadata fetch attempt, with no missing decisions.
- All entries in the validation report include non-null values for: attribute name, fetched value, validation rule applied, pass/fail status, and service source.
- End-to-end test confirms that rejected metadata (fail status) does not appear in the output .msp file, while accepted metadata (pass status) appears correctly.
- Schema validation on the log file confirms it conforms to the defined structure (e.g., required fields, data types, timestamp format).
- Pytest unit tests verify that the Validator rejects all known malformed formats (e.g., invalid SMILES, InChI without 'InChI=' prefix, CAS numbers with wrong digit patterns) and accepts all correct formats for each service.

## Limitations

- Logging overhead may degrade performance in high-throughput annotation of very large .msp files (thousands of spectra × multiple services); consider asynchronous log writes or batching.
- Validation rules are service-specific and may require updates if external APIs change their response formats; maintenance burden increases with the number of integrated services.
- Logging to file requires disk I/O and storage space; large validation reports may become unwieldy; log rotation or compression strategies should be implemented.
- The audit trail records only whether metadata passed validation, not whether it is scientifically correct or relevant for downstream analysis; validation is a format check, not a semantic check.

## Evidence

- [other] MSMetaEnhancer implements attribute validation tracked in logs to check fetched annotation values before they are written back to spectra: "MSMetaEnhancer implements attribute validation tracked in logs to check fetched annotation values before they are written back to spectra, ensuring data quality during the metadata enrichment process."
- [other] Implement a Validator class that intercepts converter output dictionaries and applies attribute-specific validation rules before metadata is committed to the spectra object: "Implement a Validator class that intercepts converter output dictionaries and applies attribute-specific validation rules before metadata is committed to the spectra object."
- [other] Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file: "Log all validation results (attribute name, fetched value, validation rule applied, pass/fail status, service source) to a structured validation report file."
- [other] Add unit tests using pytest that verify validation accepts correct formats and rejects malformed data for each supported attribute type: "Add unit tests using pytest that verify validation accepts correct formats and rejects malformed data for each supported attribute type."
- [other] Test end-to-end with sample .msp files, confirming only validated metadata reaches output files and validation logs capture all decisions: "Test end-to-end with sample .msp files, confirming only validated metadata reaches output files and validation logs capture all decisions."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation), [CTS](https://cts.fiehnlab.ucdavis.edu/),"
