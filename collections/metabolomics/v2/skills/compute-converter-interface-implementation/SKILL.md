---
name: compute-converter-interface-implementation
description: Use when you need to add a new local chemical structure conversion capability to MSMetaEnhancer when existing web-service converters (CTS, CIR, PubChem) are unavailable, too slow, or unsuitable for your workflow, and you have a chemical transformation (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_3070
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer
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

# Compute-Converter Interface Implementation

## Summary

Implement a local chemical structure conversion tool by subclassing ComputeConverter and using RDKit to perform in-process molecular transformations (e.g., SMILES to InChI) without external web service calls. This skill enables offline chemical metadata enrichment within the MSMetaEnhancer ecosystem.

## When to use

You need to add a new local chemical structure conversion capability to MSMetaEnhancer when existing web-service converters (CTS, CIR, PubChem) are unavailable, too slow, or unsuitable for your workflow, and you have a chemical transformation (e.g., SMILES → InChI, SMILES → InChIKey) that RDKit can perform natively without network latency.

## When NOT to use

- The conversion you need is already provided by an existing web-service converter (CTS, CIR, IDSM, PubChem, BridgeDb) and network latency is acceptable.
- You require metadata beyond RDKit's local capabilities (e.g., PubChem substance IDs, vendor availability data, biological activity annotations) that necessitate external API queries.
- Your input SMILES strings are malformed or contain non-standard chemistry that RDKit cannot parse without fallback to a web service.

## Inputs

- Python module inheriting from ComputeConverter base class
- Chemical identifiers (SMILES strings, InChI strings, or molecular structures)
- List of source→target conversion pairs (e.g., [{'source': 'smiles', 'target': 'inchi'}])

## Outputs

- Registered converter class instance in MSMetaEnhancer.libs.converters.compute
- Dictionary of converted chemical properties keyed by target attribute names
- Pytest test module validating converter behavior and chemical correctness

## How to apply

Create a new Python file in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter. Define a conversions list with source and target attributes (e.g., 'smiles' to 'inchi') and call create_top_level_conversion_methods(conversions, asynch=False). Implement conversion methods using RDKit functions (e.g., Chem.MolFromSmiles to parse SMILES strings, Chem.inchi.MolToInchi to generate InChI output). Return converted data as a dictionary keyed by the target attribute. Register the converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding it to __all__. Write pytest tests to validate converter instantiation and verify conversion accuracy against reference SMILES inputs, checking output structure and chemical correctness. Run pytest to confirm all existing tests pass and new converter tests execute successfully.

## Related tools

- **RDKit** (Perform local molecular structure transformations (SMILES parsing, InChI generation, molecular property computation))
- **pytest** (Validate converter instantiation, test conversion accuracy against reference inputs, and verify existing test suite still passes)
- **MSMetaEnhancer** (Provide the ComputeConverter base class interface and converter registration/orchestration framework) — https://github.com/RECETOX/MSMetaEnhancer

## Examples

```
from MSMetaEnhancer.libs.converters.compute import RDKit; from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder; ConverterBuilder.register([RDKit]); converter = RDKit(); result = converter.smiles_to_inchi('CCO'); print(result)
```

## Evaluation signals

- Converter class is successfully instantiated and registered in __all__; no import errors occur.
- All pytest tests for the new converter pass; reference SMILES inputs produce chemically correct and structurally valid outputs (e.g., InChI strings conform to IUPAC format).
- Existing MSMetaEnhancer test suite still passes after converter registration (pytest run shows no regressions).
- Output dictionary keys exactly match the target attribute names specified in the conversions list.
- Conversion methods handle edge cases gracefully (e.g., malformed SMILES return None or raise a documented exception rather than crashing).

## Limitations

- RDKit is limited to chemical transformations it natively supports; complex conversions requiring external chemical databases (e.g., CAS number lookup, IUPAC name generation) must still use web-service converters.
- Malformed or non-standard SMILES strings may fail silent parsing by RDKit; error handling and input validation must be explicitly implemented in conversion methods.
- Asynchronous annotation workflows in MSMetaEnhancer expect async-compatible converters; ComputeConverter subclasses with asynch=False may create bottlenecks in large batch processing pipelines.

## Evidence

- [other] MSMetaEnhancer uses RDKit as a reference implementation for implementing ComputeConverter subclasses that perform local chemical structure conversions.: "MSMetaEnhancer uses RDKit as a reference implementation for implementing ComputeConverter subclasses that perform local chemical structure conversions"
- [other] Create a new Python file in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter. Define the conversions list with source and target attributes (e.g., 'smiles' to 'inchi') and call create_top_level_conversion_methods with asynch=False.: "Create a new Python file in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter. Define the conversions list with source and target attributes (e.g., 'smiles' to 'inchi') and"
- [other] Implement conversion methods using RDKit to perform local molecular structure transformations (e.g., parse SMILES strings with RDKit Chem.MolFromSmiles and generate InChI with Chem.inchi.MolToInchi).: "Implement conversion methods using RDKit to perform local molecular structure transformations (e.g., parse SMILES strings with RDKit Chem.MolFromSmiles and generate InChI with Chem.inchi.MolToInchi)"
- [other] Register the new converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding to __all__.: "Register the new converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding to __all__"
- [other] Create a pytest test file that validates converter instantiation and tests conversion accuracy against reference SMILES inputs, verifying output structure and chemical correctness.: "Create a pytest test file that validates converter instantiation and tests conversion accuracy against reference SMILES inputs, verifying output structure and chemical correctness"
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb.: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb"
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed"
