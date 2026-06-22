---
name: dynamic-method-discovery
description: Use when you need to enumerate all supported metadata conversions in a plugin-based architecture without hard-coding converter names or method signatures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0081
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
  - pytest
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
---

# dynamic-method-discovery

## Summary

Automatically discover and instantiate conversion methods from converter modules at runtime, enabling a unified registry of chemical metadata transformation routes. This skill allows MSMetaEnhancer to decouple converter implementation from job orchestration by dynamically extracting conversion tuples, invoking method generators, and aggregating available transformations across web and compute services.

## When to use

Use this skill when you need to enumerate all supported metadata conversions in a plugin-based architecture without hard-coding converter names or method signatures. Specifically: when you want to support multiple external services (CIR, CTS, PubChem, IDSM, BridgeDb) or compute backends (RDKit) as interchangeable converters, and you need to automatically extract the (source_attribute, target_attribute) conversion pairs each converter exposes, so that downstream components (e.g., Galaxy UI generators, job schedulers) can query available options without modifying code when a new converter is added.

## When NOT to use

- Converter methods are already hard-coded into a static configuration file — dynamic discovery adds complexity without benefit when conversions are known and stable.
- Each converter exposes a different conversion interface (non-uniform method naming or tuple structure) — discovery assumes a consistent API contract across all converters.
- Converters are third-party binaries or services with no Python class definition — discovery requires introspectable Python modules with a conversions list attribute.

## Inputs

- converter_modules (Python class definitions in web/ and compute/ directories)
- converter_instances (instantiated converter objects with conversions attribute)
- conversions list (list of tuples: (source_attribute, target_attribute, method_name))

## Outputs

- Job registry (unified list of (source_attr, target_attr, converter_name) tuples)
- Job manifest file (serialized structured file listing all available conversions)
- converter_options dictionary (JSON-serializable dict keyed by source attribute, mapping to available target conversions)

## How to apply

Load the ConverterBuilder module and scan the converter directories (MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/) to discover all converter classes. For each discovered converter, instantiate it and extract its conversions list attribute, which contains tuples of (source_attribute, target_attribute, conversion_method_name). Invoke the create_top_level_conversion_methods() call on each converter instance to trigger dynamic method generation based on those tuples. Aggregate all (source_attr, target_attr, converter_name) triples into a unified Job registry, validating that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance. Serialize and output the complete Job manifest as a structured file, enabling downstream systems to query supported conversions without hardcoding converter logic.

## Related tools

- **ConverterBuilder** (Module that auto-discovers and instantiates converters, extracts conversions tuples, and aggregates Job registry across web and compute backends) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web converter exposing chemical identifier conversions (e.g., InChI to SMILES) via external API) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web converter for chemical metadata transformations) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Web converter aggregating chemical structure and metadata lookups) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Web converter for name and structure metadata conversions) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Web converter for identifier mapping across chemical databases) — https://bridgedb.github.io/
- **RDKit** (Compute converter for local cheminformatics transformations without external API calls) — https://github.com/RECETOX/MSMetaEnhancer
- **Python** (Language for implementing converter modules, method introspection, and dynamic method generation)

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit

ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
```

## Evaluation signals

- All converter classes in web/ and compute/ directories are successfully instantiated without errors.
- Each discovered converter exposes a conversions list attribute containing at least one (source_attribute, target_attribute, method_name) tuple.
- The create_top_level_conversion_methods() call completes for each converter, generating the corresponding async/sync methods.
- Every Job in the registry can be validated: the conversion_method exists as a callable on the converter instance with the correct async/sync signature.
- The serialized Job manifest is JSON-serializable and contains all expected (source_attr, target_attr, converter_name) triples with no duplicates.

## Limitations

- Discovery assumes all converters follow the same interface: a conversions list attribute and a create_top_level_conversion_methods() method. Converters with non-standard APIs will not be auto-discovered.
- Method validation only checks existence and signature; it does not verify that the method is functional or handles errors gracefully. Integration testing is required to catch runtime failures.
- Dynamic method generation may fail silently if converter implementation is incomplete, requiring robust error handling and validation at runtime.
- The discovery process must be re-run each time a new converter is added or removed; there is no automatic hot-reload mechanism.

## Evidence

- [other] Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/ directories.: "Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/"
- [other] For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute, target_attribute, conversion_method_name).: "For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute,"
- [other] Invoke the create_top_level_conversion_methods() call on each converter to trigger dynamic method generation based on the conversions list.: "Invoke the create_top_level_conversion_methods() call on each converter to trigger dynamic method generation based on the conversions list."
- [other] Aggregate all discovered Job tuples across web and compute converters into a unified Job registry, where each Job represents one (source_attr, target_attr, converter_name) triple.: "Aggregate all discovered Job tuples across web and compute converters into a unified Job registry, where each Job represents one (source_attr, target_attr, converter_name) triple."
- [other] Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance.: "Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance."
- [other] Instantiate the ConverterBuilder to discover all available web converters (CIR, CTS, IDSM, PubChem, BridgeDb) and compute converters (RDKit) registered in the package.: "Instantiate the ConverterBuilder to discover all available web converters (CIR, CTS, IDSM, PubChem, BridgeDb) and compute converters (RDKit) registered in the package."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb.: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb."
