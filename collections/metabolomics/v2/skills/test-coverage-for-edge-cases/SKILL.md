---
name: test-coverage-for-edge-cases
description: Use when integrating a new metadata validation step into a conversion
  pipeline that fetches structured chemical identifiers (SMILES, InChI, CAS numbers,
  IUPAC names) from external services.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3372
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

# test-coverage-for-edge-cases

## Summary

Design and implement pytest-based unit tests that verify metadata validation logic accepts correctly formatted annotation values while rejecting malformed data for each supported attribute type (SMILES, InChI, CAS number). This ensures data quality gates in MSMetaEnhancer catch edge cases before validated metadata is committed to .msp files.

## When to use

Apply this skill when integrating a new metadata validation step into a conversion pipeline that fetches structured chemical identifiers (SMILES, InChI, CAS numbers, IUPAC names) from external services. Use it specifically when you need to verify that a Validator class correctly intercepts converter output dictionaries and applies attribute-specific format rules before data is written to spectra files.

## When NOT to use

- Input is unstructured free-text metadata with no well-defined format specification — validation schemas require formal acceptance criteria.
- Metadata has already been manually curated and validated upstream — redundant testing adds no data quality benefit.
- Services return only opaque identifiers (e.g., database IDs) with no parseable structure — attribute-level validation rules cannot be designed.

## Inputs

- Converter output dictionaries (attribute name → fetched value pairs)
- Sample .msp files with diverse metadata
- Service-specific specification documents (API response formats, valid value ranges)

## Outputs

- pytest test suite with parameterized unit tests per attribute type
- Test report showing pass/fail status for each validation rule
- Validation logs capturing attribute name, fetched value, validation rule applied, pass/fail status, and service source

## How to apply

First, design a validation schema that defines acceptance criteria for each metadata attribute type based on service specifications (e.g., SMILES must follow SMILES syntax rules, InChI strings must begin with 'InChI=', CAS numbers must match '^[0-9]{1,7}-[0-9]{2}-[0-9]$'). Second, create pytest test cases for each attribute that exercise both valid and invalid inputs: valid cases confirm the validator passes correctly formatted values, invalid cases confirm it rejects malformed data. Third, use pytest fixtures to parameterize tests across multiple example values per attribute type. Fourth, run the full test suite with `pytest` to ensure validation rules accept all correct formats while uniformly rejecting malformed inputs. Fifth, include end-to-end tests with sample .msp files to confirm only validated metadata reaches output files and validation logs capture all decisions.

## Related tools

- **pytest** (Framework for implementing and executing unit tests that verify validation accepts correct formats and rejects malformed data) — https://docs.pytest.org/en/6.2.x/contents.html
- **MSMetaEnhancer** (System integrating the Validator class into the conversion pipeline; provides Job and Converter architecture for test integration) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Chemical identifier resolution service whose outputs (SMILES, InChI) must be validated for correct format) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **PubChem** (Chemical database service providing SMILES and other metadata attributes requiring format validation) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Service providing InChI, formula, InChIKey, and IUPAC name outputs that must pass validation rules) — https://idsm.elixir-czech.cz/

## Examples

```
pytest MSMetaEnhancer/tests/test_validator.py::test_smiles_validation -v; pytest MSMetaEnhancer/tests/test_validator.py::test_inchi_validation -v; pytest MSMetaEnhancer/tests/test_validator.py::test_cas_validation -v
```

## Evaluation signals

- All pytest tests execute without error and report pass/fail status for each attribute type.
- Validation logs contain structured records (attribute name, fetched value, rule applied, pass/fail, service source) for every validation decision.
- End-to-end test confirms only validated metadata appears in output .msp files; rejected values are either omitted or logged as failures.
- Test suite covers both boundary cases (empty strings, maximum-length values, special characters) and service-specific malformations (invalid SMILES syntax, missing InChI prefix, incorrect CAS number checksum).
- Validation rules are consistent across all supported services — identical attribute types from different sources follow the same acceptance criteria.

## Limitations

- Validation schema must be manually maintained as service specifications change; automated schema updates are not discussed in the article.
- Edge cases specific to local metadata curation (e.g., user-entered values with typos) may require additional validation rules beyond service-level format checking.
- Some valid chemical identifiers may fail validation if the schema is overly restrictive (e.g., if SMILES validator does not handle all valid SMILES dialect variants).

## Evidence

- [other] Design a validation schema defining acceptance criteria for each metadata attribute type (e.g., SMILES format, InChI prefix, CAS number format) based on service specifications.: "Design a validation schema defining acceptance criteria for each metadata attribute type (e.g., SMILES format, InChI prefix, CAS number format) based on service specifications."
- [other] Add unit tests using pytest that verify validation accepts correct formats and rejects malformed data for each supported attribute type.: "Add unit tests using pytest that verify validation accepts correct formats and rejects malformed data for each supported attribute type."
- [other] Test end-to-end with sample .msp files, confirming only validated metadata reaches output files and validation logs capture all decisions.: "Test end-to-end with sample .msp files, confirming only validated metadata reaches output files and validation logs capture all decisions."
- [readme] All functionality is tested with the pytest framework.: "All functionality is tested with the [pytest](https://docs.pytest.org/en/6.2.x/contents.html) framework."
- [other] make sure the existing tests still work by running pytest: "make sure the existing tests still work by running ``pytest``"
