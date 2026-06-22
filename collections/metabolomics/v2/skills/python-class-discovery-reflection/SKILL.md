---
name: python-class-discovery-reflection
description: Use when when building an extensible converter framework where new converter implementations (e.g., WebConverters or ComputeConverters for external chemical services) should be automatically discovered and registered without modifying a central registry.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - pytest
  - Python
  - MSMetaEnhancer
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- make sure the existing tests still work by running ``pytest``
- A Python package for mass spectra metadata annotation
- Create a new Python file in `MSMetaEnhancer/libs/converters/web/` named after your service
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

# Python Class Discovery and Reflection

## Summary

Dynamically discover converter subclasses from package directories and introspect their initialization signatures and metadata attributes to enumerate available conversion operations. This skill enables automatic service discovery and job enumeration without hardcoding class imports or conversion mappings.

## When to use

When building an extensible converter framework where new converter implementations (e.g., WebConverters or ComputeConverters for external chemical services) should be automatically discovered and registered without modifying a central registry. Apply when you need to enumerate all available (source_attribute, target_attribute) conversion pairs across multiple converter plugins at runtime.

## When NOT to use

- When converter classes are already imported and registered manually in a hardcoded list (reflection adds overhead)
- When converters are defined in external services or non-Python packages without Python class definitions
- When the number of converters is small and static — direct imports are simpler and more maintainable

## Inputs

- Package directory paths (e.g., 'MSMetaEnhancer.libs.converters.web', 'MSMetaEnhancer.libs.converters.compute')
- Converter base class type (e.g., WebConverter or ComputeConverter)
- Initialization parameters (e.g., session object for WebConverters)

## Outputs

- Master enumeration of Job objects as (source_attribute, target_attribute, converter_name) tuples
- Dictionary or registry mapping converter names to instantiated converter instances
- Validated conversion specifications with source/target attribute pairs and their associated conversion methods

## How to apply

Scan converter package directories (e.g., MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute) using Python's importlib or pkgutil modules to discover all converter class definitions. For each discovered class, instantiate it with appropriate initialization arguments (e.g., session for WebConverters, no arguments for ComputeConverters). Introspect each instance to extract the conversions list defined in its __init__ method, which specifies (source_attr, target_attr, conversion_method) tuples. Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification. Validate the aggregated job enumeration is non-empty and contains expected converter-specific conversions by running pytest on the ConverterBuilder test suite.

## Related tools

- **pytest** (Verify that discovered jobs match expected conversion function signatures across all available services and validate the job enumeration is non-empty) — https://docs.pytest.org/
- **Python** (Language runtime for dynamic class discovery via importlib/pkgutil, introspection via inspect/getattr, and instantiation with __init__ parameter handling)
- **MSMetaEnhancer** (Reference implementation containing ConverterBuilder that discovers and instantiates web and compute converter plugins from package directories) — https://github.com/RECETOX/MSMetaEnhancer

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
jobs = ConverterBuilder.enumerate_jobs()
print(jobs)  # [(source, target, converter_name), ...]
```

## Evaluation signals

- Discovered converter list is non-empty and includes all expected converter classes from target package directories
- Each instantiated converter successfully yields a conversions list with (source_attr, target_attr, conversion_method) tuples
- Generated Job objects contain correct (source_attribute, target_attribute, converter_name) tuples matching the converter's specification
- pytest test suite passes, confirming discovered jobs match expected conversion function signatures
- Aggregated job enumeration is reproducible across multiple runs and includes service-specific conversions (e.g., CIR, CTS, PubChem, IDSM, BridgeDb conversions)

## Limitations

- Requires converter classes to follow a consistent interface (e.g., conversions list defined in __init__) — heterogeneous converter signatures will cause introspection to fail
- Dynamic discovery depends on proper package structure and importable module paths; circular imports or import-time side effects may cause failures
- Initialization of WebConverters requires a session object; missing or invalid session will prevent instantiation and discovery of web service converters
- Class discovery via filesystem scanning may include abstract base classes or non-converter classes if naming conventions are not enforced

## Evidence

- [other] Scan the MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute package directories to dynamically discover all converter class definitions.: "Scan the MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute package directories to dynamically discover all converter class definitions."
- [other] For each discovered converter subclass, instantiate the class with appropriate initialization arguments (session for WebConverters, no arguments for ComputeConverters).: "For each discovered converter subclass, instantiate the class with appropriate initialization arguments (session for WebConverters, no arguments for ComputeConverters)."
- [other] Introspect each instantiated converter to extract the conversions list defined in its __init__ method, which specifies (source_attr, target_attr, conversion_method) tuples.: "Introspect each instantiated converter to extract the conversions list defined in its __init__ method, which specifies (source_attr, target_attr, conversion_method) tuples."
- [other] Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification.: "Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification."
- [other] Run pytest on the ConverterBuilder test suite to verify that discovered jobs match expected conversion function signatures across all available services.: "Run pytest on the ConverterBuilder test suite to verify that discovered jobs match expected conversion function signatures across all available services."
- [other] MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters that the ConverterBuilder must discover and instantiate into Job objects.: "MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters"
- [readme] ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]): "ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])"
