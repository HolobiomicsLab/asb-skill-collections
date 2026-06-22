---
name: web-api-service-integration-mapping
description: Use when you need to support multiple external services (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) for chemical identifier conversions (.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_0154
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

# web-api-service-integration-mapping

## Summary

Systematically enumerate and validate all available conversion jobs across multiple external chemical-metadata services by auto-discovering converter modules, extracting source-target conversion pairs, and generating a unified Job registry. This skill enables reproducible, service-agnostic metadata annotation workflows in MSMetaEnhancer.

## When to use

Apply this skill when you need to support multiple external services (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) for chemical identifier conversions (.msp file annotation) and want to automatically discover which conversions are available, validate their implementation, and expose them to the annotation engine without manual configuration of each service–conversion pair.

## When NOT to use

- If you are working with a single, pre-configured converter with a fixed set of conversions; Job discovery is unnecessary overhead.
- If the external services are not API-based or do not expose structured conversion metadata via module __init__ definitions.
- If you need real-time service capability discovery (e.g., polling each service's API for supported conversions); this skill assumes static converter module definitions.

## Inputs

- converter module discovery directories (MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/)
- converter class instances with conversions list and conversion methods
- converter __init__ metadata (source_attribute, target_attribute, conversion_method_name tuples)

## Outputs

- unified Job registry (list of (source_attr, target_attr, converter_name) triples)
- Job manifest (structured file serialization of all available conversions)
- validated conversion method index (method_name → async/sync callable mapping per converter)

## How to apply

Load the ConverterBuilder module to auto-discover all converter classes from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/ directories. For each discovered converter, extract the conversions list (tuples of source_attribute, target_attribute, conversion_method_name) defined in its __init__ method. Call create_top_level_conversion_methods() on each converter to trigger dynamic method generation. Aggregate all source–target–converter triples into a unified Job registry and validate that each Job's conversion_method exists as an async method (WebConverters) or sync method (ComputeConverters). Serialize the complete Job manifest into a structured file. This approach decouples Job discovery from job scheduling, allowing new converters to be plugged in without modifying the core annotation logic.

## Related tools

- **MSMetaEnhancer** (Host framework for converter discovery and Job registry management; orchestrates async annotation workflows using discovered Jobs) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (External web service converter for chemical structure conversions (InChI ↔ SMILES)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (External web service converter for chemical identifier transformations (e.g., name → InChI)) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (External web service converter for chemical metadata lookup (CID-based SMILES, InChI, formula retrieval)) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (External web service converter for chemical identifier and property conversions (name → inchi, inchi → formula, inchikey, iupac_name, canonical_smiles)) — https://idsm.elixir-czech.cz/
- **BridgeDb** (External web service converter for cross-identifier mapping across biological databases) — https://bridgedb.github.io/
- **RDKit** (Local compute converter for cheminformatics operations (SMILES parsing, structure validation, fingerprint generation))
- **ConverterBuilder** (Utility module responsible for auto-discovery, instantiation, and validation of all converter modules and their Job definitions) — https://github.com/RECETOX/MSMetaEnhancer
- **pytest** (Test framework used to validate converter discovery, Job registry completeness, and method existence)

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'inchikey', 'IDSM')]
```

## Evaluation signals

- All converter modules in web/ and compute/ directories are successfully loaded without import errors.
- Each discovered converter's conversions list is non-empty and contains valid (source_attr, target_attr, method_name) tuples.
- Every Job in the registry has a corresponding callable method on its converter instance with the correct signature (async for web, sync for compute).
- Job manifest serialization includes all discovered conversions with no missing or duplicate entries; schema validation passes.
- Annotation runs using the discovered Job registry produce results identical to manually configured Job lists (regression test via pytest).

## Limitations

- Converter discovery is static: only converters present in the module directories at runtime are discovered; dynamic service capability polling is not supported.
- Conversion method names must be explicitly defined in the converter's __init__ conversions list; unnamed or dynamically generated methods will not be registered.
- API rate limiting and error handling are delegated to individual converter implementations; Job discovery does not validate service availability or health.
- The skill assumes converters follow the MSMetaEnhancer interface (async methods for WebConverters, sync for ComputeConverters); non-compliant custom converters may cause validation to fail.

## Evidence

- [other] Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/ directories.: "Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/"
- [other] For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute, target_attribute, conversion_method_name).: "For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute,"
- [other] Aggregate all discovered Job tuples across web and compute converters into a unified Job registry, where each Job represents one (source_attr, target_attr, converter_name) triple.: "Aggregate all discovered Job tuples across web and compute converters into a unified Job registry, where each Job represents one (source_attr, target_attr, converter_name) triple."
- [other] Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance.: "Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance."
- [readme] ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]): "ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])"
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](...), [CTS](...), [PubChem](...), [IDSM](...), and [BridgeDb](...): "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](...), [CTS](...), [PubChem](...), [IDSM](...), and [BridgeDb](...)"
