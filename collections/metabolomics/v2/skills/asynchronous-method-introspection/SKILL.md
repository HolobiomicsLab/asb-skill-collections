---
name: asynchronous-method-introspection
description: Use when you have a plugin-based converter architecture (e.g., web services and compute libraries in separate directories) and you need to automatically discover all available (source_attribute, target_attribute, converter_name) conversion triples without hardcoding them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0092
  tools:
  - MSMetaEnhancer
  - Python
  - CIR
  - CTS
  - IDSM
  - PubChem
  - BridgeDb
  - RDKit
  - ConverterBuilder
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- '**MSMetaEnhancer** is a tool used for `.msp` files annotation'
- '`MSMetaEnhancer/libs/converters/web/` named after your service'
- 'MSMetaEnhancer: A Python package for mass spectra metadata annotation'
- Create a new Python file in `MSMetaEnhancer/libs/converters/web/`
- 'fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation)'
- __all__ = ['IDSM', 'CTS', 'CIR', 'PubChem', 'BridgeDb', 'MyService']
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# asynchronous-method-introspection

## Summary

Dynamically discover, enumerate, and validate asynchronous conversion methods across a modular converter registry to build a unified job manifest of all available source-to-target chemical identifier transformations. This skill enables automatic Job discovery without manual configuration, ensuring that each conversion route is backed by a real async method on the corresponding converter instance.

## When to use

Apply this skill when you have a plugin-based converter architecture (e.g., web services and compute libraries in separate directories) and you need to automatically discover all available (source_attribute, target_attribute, converter_name) conversion triples without hardcoding them. Use it before running batch annotation workflows to confirm which Jobs are actually available and executable.

## When NOT to use

- Converters are statically defined and do not change at runtime — use a static configuration file instead
- You only need a subset of converters; introspecting the entire registry will waste time and resources
- Method signatures are not standardized across converters — inconsistent async/sync calling conventions will cause validation failures

## Inputs

- Converter module paths (web and compute directories)
- Converter class definitions with __init__ method defining conversions list
- Converter instances with method stubs or method templates

## Outputs

- Unified Job registry (list of validated (source_attribute, target_attribute, converter_name) tuples)
- Serialized Job manifest file (structured listing of all available conversions)
- Validated method catalog (mapping of Job triples to actual callable async/sync methods)

## How to apply

Load the ConverterBuilder module to recursively discover all converter classes from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/ directories. For each discovered converter instance, extract its conversions list (defined as tuples of source_attribute, target_attribute, and conversion_method_name) and invoke create_top_level_conversion_methods() to trigger dynamic method generation. Then iterate over each converter's conversions list and validate that the named conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on that instance. Aggregate all validated (source_attr, target_attr, converter_name) triples into a unified Job registry and serialize the result into a structured manifest file that can be queried downstream to determine which conversion routes are safe to request.

## Related tools

- **MSMetaEnhancer** (Host framework containing ConverterBuilder and converter registry; provides async annotation orchestration) — https://github.com/RECETOX/MSMetaEnhancer
- **ConverterBuilder** (Module that auto-discovers, instantiates, and introspects all converter classes) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Example web converter providing chemical identifier conversions via external service) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Example web converter providing chemical identifier conversions via external service) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Example web converter providing chemical identifier conversions via external service) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Example web converter providing chemical identifier conversions via external service) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Example web converter providing chemical identifier conversions via external service) — https://bridgedb.github.io/
- **RDKit** (Example compute converter providing chemical identifier conversions via local computation)
- **Python** (Language used to implement introspection and async method discovery)

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
jobs_manifest = ConverterBuilder.discover_and_validate_jobs()
print(jobs_manifest)
```

## Evaluation signals

- All discovered converter instances have a conversions attribute that is a non-empty list of tuples (source, target, method_name)
- For each Job triple (source_attr, target_attr, converter_name), the corresponding converter instance has a callable method with the specified method_name that is either async (WebConverters) or sync (ComputeConverters)
- The serialized Job manifest contains ≥ 1 entry per registered converter and is syntactically valid (JSON, YAML, or structured text format)
- Invoking a method from the registry on a real converter instance does not raise AttributeError or MethodNotFoundError
- The Job registry is consistent across multiple runs of the introspection routine (no non-deterministic discovery)

## Limitations

- Dynamically generated methods must follow a strict naming convention (method_name derived from source and target attributes); converters that deviate will not be discovered
- Async method introspection cannot validate method signatures or return types at discovery time; validation failures only surface at runtime
- The skill assumes converters are stateless during introspection; stateful converters that require initialization parameters may not be introspectable
- Network-dependent converters (e.g., web services) are not validated to confirm they are actually reachable; only local method presence is checked

## Evidence

- [other] Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/ directories.: "Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/"
- [other] For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute, target_attribute, conversion_method_name).: "For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute,"
- [other] Invoke the create_top_level_conversion_methods() call on each converter to trigger dynamic method generation based on the conversions list.: "Invoke the create_top_level_conversion_methods() call on each converter to trigger dynamic method generation based on the conversions list."
- [other] Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance.: "Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance."
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
- [readme] ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]): "ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])"
