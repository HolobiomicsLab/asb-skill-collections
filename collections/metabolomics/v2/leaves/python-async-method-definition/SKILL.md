---
name: python-async-method-definition
description: Use when when extending MSMetaEnhancer with a new local chemical transformation
  (e.g., SMILES to InChI) that should execute non-blockingly within an asynchronous
  annotation workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - MSMetaEnhancer
  - pytest
  - Python
  - RDKit
  - Python asyncio
  license_tier: open
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
- make sure the existing tests still work by running ``pytest``
- A Python package for mass spectra metadata annotation
- Create a new Python file in `MSMetaEnhancer/libs/converters/web/` named after your
  service
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Define Asynchronous Conversion Methods in Python Converters

## Summary

A structured method for implementing asynchronous conversion methods within MSMetaEnhancer's ComputeConverter subclasses, enabling local chemical structure transformations using RDKit without blocking I/O. This skill ensures proper method signatures, return types, and integration with the framework's asynchronous annotation pipeline.

## When to use

When extending MSMetaEnhancer with a new local chemical transformation (e.g., SMILES to InChI) that should execute non-blockingly within an asynchronous annotation workflow. Apply this skill when the conversion logic is computationally self-contained (does not require external web service calls) and must participate in the app's async batch processing loop.

## When NOT to use

- Input requires calling external web services (CIR, CTS, PubChem, etc.); use WebConverter subclasses instead.
- Conversion is already available in an existing registered converter; reuse or extend the existing converter rather than duplicating.
- Chemical transformation logic is CPU-intensive or requires blocking I/O; consider a synchronous implementation or offloading to a background task queue.

## Inputs

- Python class inheriting from ComputeConverter
- List of conversion specifications (source and target attribute names)
- String input in source chemical format (e.g., SMILES string)

## Outputs

- Async conversion method definitions (async def coroutines)
- Dictionary mapping target attribute key to converted chemical representation
- Integrated converter instance available to MSMetaEnhancer Application

## How to apply

Create a ComputeConverter subclass by inheriting from the abstract base and defining a conversions list with source and target attributes (e.g., 'smiles' to 'inchi'). Call create_top_level_conversion_methods(conversions, asynch=False) to auto-generate dispatcher methods. Implement individual conversion methods as async def coroutines that accept a string input in the source format, use RDKit APIs (e.g., Chem.MolFromSmiles, Chem.inchi.MolToInchi) to perform the molecular transformation, and return a dictionary keyed by the target attribute name. Ensure each async method uses await syntax where applicable and handles None returns from RDKit gracefully by returning an empty dict or raising a descriptive exception. Register the converter in __init__.py and validate with pytest test cases covering instantiation and conversion accuracy against reference SMILES inputs.

## Related tools

- **RDKit** (Provides APIs (Chem.MolFromSmiles, Chem.inchi.MolToInchi) for local molecular structure parsing and conversion within async methods)
- **MSMetaEnhancer** (Framework providing ComputeConverter base class, create_top_level_conversion_methods method, and Application registration mechanism) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (Testing framework for validating converter instantiation and conversion accuracy against reference inputs)
- **Python asyncio** (Provides async/await syntax and event loop integration for non-blocking method execution in annotation pipeline)

## Examples

```
from MSMetaEnhancer.libs.converters.compute import RDKit; from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder; ConverterBuilder.register([RDKit]); import asyncio; result = asyncio.run(RDKit().smiles_to_inchi('CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O'))
```

## Evaluation signals

- Converter class successfully instantiates and methods are callable as async coroutines (no syntax errors).
- Test cases confirm conversion accuracy: reference SMILES inputs produce chemically correct InChI, InChIKey, or formula outputs matching expected canonical forms.
- Return value structure matches expected dictionary schema (target attribute name as key, string or None value).
- Existing MSMetaEnhancer pytest suite still passes after converter registration in __init__.py.
- Converter executes within Application.annotate_spectra() without blocking the event loop and completes within reasonable time bounds for typical molecular inputs (single-digit milliseconds per molecule).

## Limitations

- RDKit's local conversion may fail silently or return None for invalid or ambiguous SMILES inputs; robust error handling and logging are essential.
- Async method overhead (coroutine overhead, event loop scheduling) is minimal but non-zero; for trivial conversions, synchronous methods may be faster in single-threaded contexts.
- RDKit does not support all chemical formats; conversion coverage is limited to what RDKit's API natively provides (e.g., no support for obscure proprietary formats).
- Asynchronous design does not parallelize RDKit execution across cores within a single Python process due to the GIL; true parallelization requires multiprocessing or external service calls.

## Evidence

- [other] Create a new Python file in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter: "Create a new Python file in MSMetaEnhancer/libs/converters/compute/ that inherits from ComputeConverter"
- [other] Define the conversions list with source and target attributes (e.g., 'smiles' to 'inchi') and call create_top_level_conversion_methods: "Define the conversions list with source and target attributes (e.g., 'smiles' to 'inchi') and call create_top_level_conversion_methods with asynch=False"
- [other] Implement conversion methods using RDKit to perform local molecular structure transformations (e.g., parse SMILES strings with RDKit Chem.MolFromSmiles and generate InChI with Chem.inchi.MolToInchi): "Implement conversion methods using RDKit to perform local molecular structure transformations (e.g., parse SMILES strings with RDKit Chem.MolFromSmiles and generate InChI with Chem.inchi.MolToInchi)"
- [other] Return converted data as a dictionary with target attribute keys: "Return converted data as a dictionary with target attribute keys"
- [other] Register the new converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding to __all__: "Register the new converter in MSMetaEnhancer/libs/converters/compute/__init__.py by importing and adding to __all__"
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed"
- [other] Create a pytest test file that validates converter instantiation and tests conversion accuracy against reference SMILES inputs: "Create a pytest test file that validates converter instantiation and tests conversion accuracy against reference SMILES inputs, verifying output structure and chemical correctness"
- [other] Use the RDKit converter as a reference implementation: "Use the RDKit converter as a reference implementation"
