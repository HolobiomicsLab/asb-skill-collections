---
name: unit-test-design-for-cheminformatics
description: Use when when implementing a new ComputeConverter subclass for MSMetaEnhancer that performs local chemical structure conversions using RDKit (e.g., SMILES to InChI, canonical SMILES generation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0091
  tools:
  - MSMetaEnhancer
  - pytest
  - RDKit
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer
schema_version: 0.2.0
---

# unit-test-design-for-cheminformatics

## Summary

Design and implement pytest-based unit tests for cheminformatics converters (e.g. RDKit-based chemical structure transformations) to validate converter instantiation, conversion accuracy, and chemical correctness of outputs. This skill ensures that local molecular transformations (SMILES→InChI, etc.) produce chemically valid and structurally correct results.

## When to use

When implementing a new ComputeConverter subclass for MSMetaEnhancer that performs local chemical structure conversions using RDKit (e.g., SMILES to InChI, canonical SMILES generation). Test-driven validation is essential because incorrect molecular parsing or structure generation can propagate errors through mass spectra metadata annotation workflows.

## When NOT to use

- Input is a web service converter (e.g., CTS, PubChem APIs) — use integration/mock tests instead
- Testing asynchronous annotation workflows across multiple services — this skill focuses on individual converter chemistry validation, not async orchestration
- Validating .msp file format parsing or metadata curation logic — this skill is specific to chemical structure transformation correctness

## Inputs

- Python module file inheriting from ComputeConverter
- Reference SMILES strings (e.g., 'c1ccccc1', 'CCO', 'CC(=O)O')
- RDKit Mol objects (parsed from SMILES input)

## Outputs

- pytest test file with test_* functions
- Test execution report (pass/fail status for converter instantiation and conversion accuracy)
- Validated chemical structure output dictionaries (e.g., {'inchi': 'InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H', 'inchikey': '...'})

## How to apply

Create a pytest test file that validates: (1) converter class instantiation succeeds and internal state (conversions list, async flags) is correctly initialized; (2) each conversion method accepts valid reference SMILES inputs (e.g., benzene 'c1ccccc1', ethanol 'CCO') and produces outputs with the correct target attribute keys (e.g., 'inchi', 'inchikey'); (3) output structure matches expected schema (dictionary format with string values); (4) chemical correctness by comparing generated InChI or SMILES strings against known reference values from RDKit's own InChI generation or canonical SMILES functions. Run pytest to confirm both new converter tests and all existing MSMetaEnhancer tests pass, ensuring no regression in the broader annotation pipeline.

## Related tools

- **pytest** (Test framework for running converter instantiation and conversion accuracy tests) — https://docs.pytest.org/en/6.2.x/contents.html
- **RDKit** (Reference implementation for local chemical structure conversions; provides Chem.MolFromSmiles, Chem.inchi.MolToInchi, and canonical SMILES generation for validation)
- **MSMetaEnhancer** (Host framework defining ComputeConverter base class and converter registration mechanism) — https://github.com/RECETOX/MSMetaEnhancer

## Examples

```
pytest tests/test_rdkit_converter.py -v
```

## Evaluation signals

- Converter instantiation test passes: conversions list attribute populated correctly with source and target fields
- Reference SMILES inputs (e.g., 'c1ccccc1', 'CCO') convert to output dictionaries with expected keys (e.g., 'inchi', 'inchikey')
- Generated InChI and InChIKey strings are non-empty and match reference RDKit-computed values for the same SMILES
- Output structure is dict-typed with string values (no None, Mol objects, or other types leaked)
- All existing MSMetaEnhancer pytest tests still pass after new converter tests are added (no regression)

## Limitations

- RDKit chemical parsing may fail silently for malformed SMILES (e.g., unbalanced rings); tests should include explicit error-case validation
- InChI and InChIKey generation require RDKit to be compiled with InChI support; test environment must verify this dependency
- Tests validate chemistry at the structure level but do not verify behavior under edge cases (e.g., isotopes, stereochemistry variants, tautomeric forms) unless explicitly included in reference test SMILES

## Evidence

- [other] Create a pytest test file that validates converter instantiation and tests conversion accuracy against reference SMILES inputs, verifying output structure and chemical correctness.: "Create a pytest test file that validates converter instantiation and tests conversion accuracy against reference SMILES inputs, verifying output structure and chemical correctness."
- [other] Implement conversion methods using RDKit to perform local molecular structure transformations (e.g., parse SMILES strings with RDKit Chem.MolFromSmiles and generate InChI with Chem.inchi.MolToInchi).: "Implement conversion methods using RDKit to perform local molecular structure transformations (e.g., parse SMILES strings with RDKit Chem.MolFromSmiles and generate InChI with Chem.inchi.MolToInchi)."
- [other] Run pytest to confirm existing tests still pass and new converter tests execute successfully.: "Run pytest to confirm existing tests still pass and new converter tests execute successfully."
- [readme] All functionality is tested with the pytest framework.: "All functionality is tested with the pytest framework."
- [other] make sure the existing tests still work by running ``pytest``: "make sure the existing tests still work by running ``pytest``"
