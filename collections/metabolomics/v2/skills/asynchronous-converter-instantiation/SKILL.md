---
name: asynchronous-converter-instantiation
description: Use when building a metadata enrichment system that must support multiple pluggable converter backends and you need to automatically discover all available converters at runtime, extract their conversion specifications, and generate Job tuples that can be dispatched to an async annotation engine.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0218
  tools:
  - pytest
  - MSMetaEnhancer
  - Python
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
- make sure the existing tests still work by running ``pytest``
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
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

# asynchronous-converter-instantiation

## Summary

Dynamically discover, instantiate, and enumerate converter classes from plugin packages to generate a complete set of source-to-target metadata conversion Job objects for parallel async annotation. This skill enables the MSMetaEnhancer system to automatically wire together all available external service converters (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) into executable conversion pipelines without manual registration.

## When to use

Use this skill when building a metadata enrichment system that must support multiple pluggable converter backends and you need to automatically discover all available converters at runtime, extract their conversion specifications, and generate Job tuples that can be dispatched to an async annotation engine. Specifically apply this when the converter classes are organized in separate package directories (e.g., MSMetaEnhancer.libs.converters.web and .compute) and each converter defines its own (source_attr, target_attr, conversion_method) specifications in its __init__ method.

## When NOT to use

- Converters are manually registered and fixed at compile-time; dynamic discovery is unnecessary overhead.
- Converter classes do not define conversions in a standard (source_attr, target_attr, method) tuple format in __init__.
- The annotation system does not use async/await semantics or does not require parallel dispatch of conversion requests.

## Inputs

- converter package directories (e.g., MSMetaEnhancer.libs.converters.web, .compute)
- converter class definitions (subclasses of base Converter with __init__ method defining conversions list)
- session object (for WebConverter initialization)
- test suite expectations (pytest assertions on Job enumeration)

## Outputs

- enumerated Job objects as (source_attribute, target_attribute, converter_name) tuples
- master Job enumeration (list of all available conversions across all converters)
- pytest validation report confirming discovered jobs match expected signatures

## How to apply

Scan the converter package directories using Python's introspection or importlib to discover all subclasses of a base Converter type. For each discovered class, instantiate it with appropriate initialization arguments (e.g., a session object for WebConverters, no arguments for ComputeConverters like RDKit). Introspect each instantiated converter instance to extract the conversions list, which defines tuples of (source_attribute, target_attribute, conversion_method). Map each conversion tuple into a Job object as (source_attribute, target_attribute, converter_name). Aggregate all Job objects into a master enumeration. Validate that the enumeration is non-empty, contains expected converter-specific conversions, and matches expected conversion function signatures by running pytest on the ConverterBuilder test suite. This approach decouples converter discovery from Job enumeration and enables async dispatch of heterogeneous service calls.

## Related tools

- **MSMetaEnhancer** (core package containing ConverterBuilder and converter subclasses (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) whose discovery and instantiation this skill orchestrates) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (test framework for validating that discovered Job enumeration matches expected conversion function signatures across all available services)
- **Python** (language and introspection/importlib APIs for dynamic converter class discovery and instantiation)
- **CIR** (external service converter providing metadata fetching (example: InChI to SMILES conversion)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (external service converter providing metadata fetching for chemical structure transformations) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (external service converter providing metadata fetching (e.g., ISOMERIC_SMILES, CANONICAL_SMILES)) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (external service converter providing metadata fetching (name to InChI, InChI to formula/InChIKey/IUPAC name)) — https://idsm.elixir-czech.cz/
- **BridgeDb** (external service converter for identifier mapping and metadata enrichment) — https://bridgedb.github.io/
- **RDKit** (compute-based converter (no external service call) used as reference implementation for compute converter pattern)

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
jobs = ConverterBuilder.enumerate_jobs()
pytest.main(['test_converter_builder.py', '-v'])
```

## Evaluation signals

- Enumerated Job list is non-empty and contains all expected (source_attr, target_attr, converter_name) tuples for each registered converter.
- Each Job's converter_name maps to exactly one instantiated converter instance and its conversions list.
- pytest test suite passes: discovered jobs match expected conversion function signatures and return types.
- All converter subclasses are discovered from package directories without manual enumeration or hard-coded class list.
- Instantiation succeeds for all converter types: WebConverters receive session object, ComputeConverters receive no arguments, no AttributeError or TypeError during introspection of conversions list.

## Limitations

- Converter classes must define conversions as a list of tuples in __init__ using a standard format; deviations in naming or structure will cause introspection to fail.
- WebConverters require a valid session object at instantiation time; if session is None or invalid, instantiation may fail or produce incomplete Job enumeration.
- The skill assumes converter package directories exist and are importable; missing packages or import errors are not gracefully handled without try-except wrapping.
- External service availability and API stability are not validated during instantiation; Job discovery succeeds even if a service is offline, but downstream async annotation will fail.
- Test coverage depends on pytest expectations being up-to-date; if converter classes add new conversions without updating tests, validation will not catch missing Job entries.

## Evidence

- [other] How does the ConverterBuilder component automatically discover and instantiate all available converter classes to create a complete set of source-to-target conversion Job objects?: "How does the ConverterBuilder component automatically discover and instantiate all available converter classes to create a complete set of source-to-target conversion Job objects?"
- [other] Scan the MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute package directories to dynamically discover all converter class definitions.: "Scan the MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute package directories to dynamically discover all converter class definitions."
- [other] For each discovered converter subclass, instantiate the class with appropriate initialization arguments (session for WebConverters, no arguments for ComputeConverters).: "For each discovered converter subclass, instantiate the class with appropriate initialization arguments (session for WebConverters, no arguments for ComputeConverters)."
- [other] Introspect each instantiated converter to extract the conversions list defined in its __init__ method, which specifies (source_attr, target_attr, conversion_method) tuples.: "Introspect each instantiated converter to extract the conversions list defined in its __init__ method, which specifies (source_attr, target_attr, conversion_method) tuples."
- [other] Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification.: "Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification."
- [other] MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters that the ConverterBuilder must discover and instantiate into Job objects.: "MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters that the ConverterBuilder must discover and"
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
- [readme] ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]): "ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])"
- [other] Run pytest on the ConverterBuilder test suite to verify that discovered jobs match expected conversion function signatures across all available services.: "Run pytest on the ConverterBuilder test suite to verify that discovered jobs match expected conversion function signatures across all available services."
