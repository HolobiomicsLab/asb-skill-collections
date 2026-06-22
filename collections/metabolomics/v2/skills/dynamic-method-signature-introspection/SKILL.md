---
name: dynamic-method-signature-introspection
description: Use when when building an automated converter discovery and job enumeration system where converter classes are dynamically loaded from package directories and you need to extract and validate their internal conversion method signatures without prior knowledge of which converters will be available.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
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

# dynamic-method-signature-introspection

## Summary

Introspect instantiated converter objects to extract their conversion specifications (source attribute, target attribute, conversion method tuples) and validate that discovered conversions match expected function signatures. This skill ensures that dynamically discovered converter classes properly expose their conversion capabilities before being aggregated into a Job enumeration.

## When to use

When building an automated converter discovery and job enumeration system where converter classes are dynamically loaded from package directories and you need to extract and validate their internal conversion method signatures without prior knowledge of which converters will be available at runtime.

## When NOT to use

- When converters are manually registered and their conversion specifications are already known and hardcoded in configuration files—introspection adds unnecessary overhead.
- When converter classes do not follow the MSMetaEnhancer pattern of defining conversions in __init__ as a standardized list attribute.
- When converters are third-party black-box services with opaque internal structure that cannot be safely introspected.

## Inputs

- Instantiated converter objects (WebConverter or ComputeConverter subclass instances)
- Converter class definitions from MSMetaEnhancer.libs.converters.web and MSMetaEnhancer.libs.converters.compute package directories

## Outputs

- Extracted conversions list: list of (source_attr, target_attr, conversion_method) tuples per converter
- Job enumeration: aggregated list of (source_attribute, target_attribute, converter_name) Job objects
- Validation report: pytest results confirming job signatures match converter method signatures

## How to apply

After instantiating each discovered converter class (with session for WebConverters, no arguments for ComputeConverters), introspect the instantiated object to extract the conversions list defined in its __init__ method. This conversions list contains (source_attr, target_attr, conversion_method) tuples that specify what attribute transformations each converter supports. Generate Job objects as (source_attribute, target_attribute, converter_name) tuples from each extraction, then aggregate all Job objects into a master enumeration and validate that the list is non-empty and contains expected converter-specific conversions. Use pytest to verify that discovered jobs match expected conversion function signatures across all available services, confirming that the introspected metadata accurately reflects the converter's actual capabilities.

## Related tools

- **pytest** (Test suite framework used to verify that discovered jobs match expected conversion function signatures across all available converter services.) — https://docs.pytest.org/en/6.2.x/contents.html
- **Python** (Language in which converter classes are implemented and introspected via reflection (getattr, isinstance, type checking) to extract conversion specifications.)
- **MSMetaEnhancer** (Parent framework providing converter base classes (WebConverter, ComputeConverter) and the ConverterBuilder component that orchestrates discovery and introspection.) — https://github.com/RECETOX/MSMetaEnhancer

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
jobs = ConverterBuilder.get_jobs()
assert len(jobs) > 0
assert any(job[2] == 'IDSM' for job in jobs)
```

## Evaluation signals

- Extracted conversions list for each converter is non-empty and contains tuples with exactly three elements (source_attr, target_attr, conversion_method).
- Master Job enumeration contains all expected converter-specific conversions and is non-empty.
- pytest test suite passes when comparing discovered job signatures against the actual method signatures of converter classes (e.g., no AttributeError or TypeError when calling the conversion methods with the inferred signatures).
- Each (source_attribute, target_attribute) pair in the Job list corresponds to a callable conversion_method that exists in the converter instance.
- Converter-specific job counts match expected baselines (e.g., CIR provides InChI→SMILES, CTS provides multiple transformations, IDSM provides name→inchi+formula+inchikey+iupac_name+canonical_smiles).

## Limitations

- Introspection relies on converters exposing a conversions list attribute in __init__; converters that deviate from this pattern will not be discoverable.
- Async/await patterns in WebConverters add complexity when inferring signatures; the introspection may require awaiting conversion methods to fully validate their return types.
- External service converters (CIR, CTS, PubChem, IDSM, BridgeDb) may have varying availability or API changes that invalidate introspected signatures at runtime; validation should include network health checks.
- The introspection approach assumes all converter classes follow a consistent initialization signature (session for WebConverters, no args for ComputeConverters); custom converters may break this assumption.

## Evidence

- [other] For each discovered converter subclass, instantiate the class with appropriate initialization arguments (session for WebConverters, no arguments for ComputeConverters). Introspect each instantiated converter to extract the conversions list defined in its __init__ method, which specifies (source_attr, target_attr, conversion_method) tuples.: "For each discovered converter subclass, instantiate the class with appropriate initialization arguments (session for WebConverters, no arguments for ComputeConverters). Introspect each instantiated"
- [other] Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification. Aggregate all Job objects into a master enumeration and validate that the list is non-empty and contains expected converter-specific conversions.: "Generate Job objects as (source_attribute, target_attribute, converter_name) tuples for each conversion specification. Aggregate all Job objects into a master enumeration and validate that the list"
- [other] Run pytest on the ConverterBuilder test suite to verify that discovered jobs match expected conversion function signatures across all available services.: "Run pytest on the ConverterBuilder test suite to verify that discovered jobs match expected conversion function signatures across all available services."
- [other] MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters that the ConverterBuilder must discover and instantiate into Job objects.: "MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters that the ConverterBuilder must discover and"
- [readme] All functionality is tested with the pytest framework.: "All functionality is tested with the [pytest](https://docs.pytest.org/en/6.2.x/contents.html) framework."
