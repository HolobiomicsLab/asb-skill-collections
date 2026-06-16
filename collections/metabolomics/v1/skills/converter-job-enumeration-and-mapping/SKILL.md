---
name: converter-job-enumeration-and-mapping
description: Use when building a multi-source metadata annotation pipeline where converters are organized as dynamically discoverable subclasses in separate packages (e.g., MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3068
  tools:
  - pytest
  - MSMetaEnhancer
  - Python
  - MSMetaEnhancer.libs.converters.web
  - MSMetaEnhancer.libs.converters.compute
  - ConverterBuilder
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- make sure the existing tests still work by running ``pytest``
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
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

# converter-job-enumeration-and-mapping

## Summary

Dynamically discover and instantiate all available converter classes from package directories, introspect their conversion specifications, and generate a complete enumeration of source-to-target conversion Job objects. This skill enables MSMetaEnhancer to map metadata transformations (e.g., InChI → SMILES, name → InChI) across multiple external annotation services (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit).

## When to use

Apply this skill when building a multi-source metadata annotation pipeline where converters are organized as dynamically discoverable subclasses in separate packages (e.g., MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute), and you need to automatically enumerate all possible source→target conversion pairs without hardcoding service names or method signatures.

## When NOT to use

- Converters are manually registered via explicit configuration files rather than auto-discovered from class definitions
- Conversion specifications are static and pre-defined in a central registry (use direct lookup instead)
- Only a single, fixed converter is needed and dynamic discovery adds unnecessary overhead

## Inputs

- Package paths (MSMetaEnhancer.libs.converters.web, MSMetaEnhancer.libs.converters.compute)
- Converter class definitions (WebConverter and ComputeConverter subclasses)
- Session objects (for WebConverter initialization)
- Test suite specifications (expected conversion function signatures)

## Outputs

- Job object enumeration: list of (source_attribute, target_attribute, converter_name) tuples
- Aggregated conversion specifications across all available services
- Test validation report (pytest output confirming discovered jobs match expected signatures)

## How to apply

Scan package directories (e.g., MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute) to locate all converter subclass definitions. Instantiate each discovered converter with appropriate initialization arguments (e.g., a session object for WebConverters, no arguments for ComputeConverters). Introspect the instantiated converter's __init__ method to extract the conversions list, which specifies (source_attr, target_attr, conversion_method) tuples. Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification. Aggregate all Job objects into a master enumeration and validate that the enumeration is non-empty and contains all expected converter-specific conversions by running pytest on the ConverterBuilder test suite to verify that discovered jobs match expected conversion function signatures.

## Related tools

- **pytest** (Validates that discovered Job objects match expected conversion function signatures across all available services)
- **Python** (Language for implementing dynamic package scanning, class introspection, and Job object generation)
- **MSMetaEnhancer.libs.converters.web** (Package containing WebConverter subclasses (CIR, CTS, PubChem, IDSM, BridgeDb) to be discovered and enumerated) — https://github.com/RECETOX/MSMetaEnhancer
- **MSMetaEnhancer.libs.converters.compute** (Package containing ComputeConverter subclasses (RDKit) to be discovered and enumerated) — https://github.com/RECETOX/MSMetaEnhancer
- **ConverterBuilder** (Component that implements automatic discovery, instantiation, and Job enumeration) — https://github.com/RECETOX/MSMetaEnhancer

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit

ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
jobs = ConverterBuilder.get_jobs()
```

## Evaluation signals

- Job enumeration is non-empty and contains all expected converter-specific conversions (pytest validates expected signatures)
- All discovered converters are instantiated with correct initialization arguments (session for WebConverters, no arguments for ComputeConverters)
- Each Job object correctly encodes a (source_attribute, target_attribute, converter_name) tuple matching converter class specifications
- No duplicate Job objects are present in the final enumeration
- pytest test suite passes with no missing or unexpected conversion methods

## Limitations

- Requires converters to be organized as subclasses with explicit __init__ method definitions containing conversions lists; ad-hoc or dynamically generated converters may not be discoverable
- WebConverters depend on successful session initialization; if the session cannot be created, instantiation fails and those converters are not enumerated
- Relies on introspection of __init__ to extract conversion specifications; converters that define conversions via other mechanisms (e.g., class variables, factory methods) will not be detected
- The enumeration is static once generated; runtime addition of new converter classes requires re-running the discovery process

## Evidence

- [other] Scan the MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute package directories to dynamically discover all converter class definitions.: "Scan the MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute package directories to dynamically discover all converter class definitions."
- [other] For each discovered converter subclass, instantiate the class with appropriate initialization arguments (session for WebConverters, no arguments for ComputeConverters).: "For each discovered converter subclass, instantiate the class with appropriate initialization arguments (session for WebConverters, no arguments for ComputeConverters)."
- [other] Introspect each instantiated converter to extract the conversions list defined in its __init__ method, which specifies (source_attr, target_attr, conversion_method) tuples.: "Introspect each instantiated converter to extract the conversions list defined in its __init__ method, which specifies (source_attr, target_attr, conversion_method) tuples."
- [other] Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification.: "Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification."
- [other] MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters that the ConverterBuilder must discover and instantiate into Job objects.: "MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters"
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb.: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb."
- [readme] All functionality is tested with the pytest framework.: "All functionality is tested with the pytest framework."
