---
name: converter-specification-validation
description: Use when adding a new converter class to MSMetaEnhancer or when modifying an existing converter's __init__ method to add/remove conversions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2422
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - pytest
  - MSMetaEnhancer
  - Python
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
---

# converter-specification-validation

## Summary

Validate that dynamically discovered converter classes expose correct conversion specifications (source–target attribute pairs and conversion method signatures) through introspection and test-driven verification. This ensures the ConverterBuilder can reliably enumerate all available source-to-target conversion Jobs across web services (CIR, CTS, PubChem, IDSM, BridgeDb) and compute-based converters (RDKit).

## When to use

Apply this skill when adding a new converter class to MSMetaEnhancer or when modifying an existing converter's __init__ method to add/remove conversions. The skill detects mismatches between declared conversion specifications and actual converter implementation, preventing silent failures in the Job enumeration pipeline.

## When NOT to use

- Do not use this skill on converters that have not been registered with ConverterBuilder.register() — the skill assumes converters are already available for discovery.
- Do not apply this skill to validate .msp file format or metadata content; this skill only validates converter class structure, not input/output data correctness.
- Do not use this skill to test external service availability (CIR, CTS, PubChem, etc.); it validates local converter specifications only.

## Inputs

- converter class definitions from MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute packages
- converter instantiation parameters (session object for WebConverters, no arguments for ComputeConverters)
- pytest test suite for ConverterBuilder

## Outputs

- enumerated Job objects: (source_attribute, target_attribute, converter_name) tuples
- validated conversion method signatures
- pytest test results confirming Job discovery completeness

## How to apply

Introspect each instantiated converter object to extract the conversions list defined in its __init__ method, which specifies (source_attr, target_attr, conversion_method) tuples. For each conversion specification, validate that the conversion_method is callable and exists on the converter instance. Generate Job objects as (source_attribute, target_attribute, converter_name) tuples and verify that the aggregated Job list is non-empty and contains all expected converter-specific conversions with correct function signatures. Run pytest on the ConverterBuilder test suite to confirm that discovered jobs match expected conversion signatures across all available services (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit).

## Related tools

- **pytest** (runs automated tests on the ConverterBuilder test suite to verify discovered Job objects match expected conversion function signatures)
- **Python** (language for introspection, converter instantiation, and dynamic class discovery)
- **MSMetaEnhancer** (package containing converter classes, ConverterBuilder utility, and the conversion specification infrastructure) — https://github.com/RECETOX/MSMetaEnhancer

## Examples

```
import pytest
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit

ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
jobs = ConverterBuilder.build()
assert len(jobs) > 0
assert all(isinstance(job, tuple) and len(job) == 3 for job in jobs)
pytest.main(['-v', 'tests/test_converter_builder.py'])
```

## Evaluation signals

- The aggregated Job list is non-empty and contains at least one Job per registered converter.
- All conversion_method values in Job tuples are callable and exist as methods on the corresponding converter instance.
- pytest test suite passes without errors; discovered jobs match expected (source_attribute, target_attribute, converter_name) tuples for each service.
- All external services (CIR, CTS, PubChem, IDSM, BridgeDb) appear in the Job enumeration with their expected conversion specifications.
- Introspection correctly extracts (source_attr, target_attr, conversion_method) tuples from each converter's __init__ method.

## Limitations

- Validation occurs at class definition and instantiation time; it does not verify that the underlying external services (CIR, CTS, PubChem, IDSM, BridgeDb) will respond correctly at runtime.
- The skill requires converters to follow the MSMetaEnhancer convention of defining conversions as a list in __init__; custom converters that bypass this pattern will not be discovered.
- Introspection assumes WebConverters require a session argument and ComputeConverters require no arguments; converters with different initialization signatures may fail discovery.

## Evidence

- [other] For each discovered converter subclass, instantiate the class with appropriate initialization arguments (session for WebConverters, no arguments for ComputeConverters). Introspect each instantiated converter to extract the conversions list defined in its __init__ method, which specifies (source_attr, target_attr, conversion_method) tuples.: "For each discovered converter subclass, instantiate the class with appropriate initialization arguments (session for WebConverters, no arguments for ComputeConverters). Introspect each instantiated"
- [other] Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification. Aggregate all Job objects into a master enumeration and validate that the list is non-empty and contains expected converter-specific conversions.: "Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification. Aggregate all Job objects into a master enumeration and validate that the list"
- [other] Run pytest on the ConverterBuilder test suite to verify that discovered jobs match expected conversion function signatures across all available services.: "Run pytest on the ConverterBuilder test suite to verify that discovered jobs match expected conversion function signatures across all available services."
- [other] MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters that the ConverterBuilder must discover and instantiate into Job objects.: "MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters that the ConverterBuilder must discover and"
- [readme] All functionality is tested with the pytest framework.: "All functionality is tested with the pytest framework."
