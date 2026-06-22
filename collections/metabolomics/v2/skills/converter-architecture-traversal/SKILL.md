---
name: converter-architecture-traversal
description: Use when when you need to understand which chemical identifier conversions are available in MSMetaEnhancer (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - MSMetaEnhancer
  - Python
  - CIR
  - CTS
  - IDSM
  - PubChem
  - BridgeDb
  - RDKit
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

# converter-architecture-traversal

## Summary

Systematically discover, enumerate, and validate all available chemical identifier conversion Jobs in the MSMetaEnhancer ConverterBuilder by traversing web and compute converter directories, extracting conversion tuples, and aggregating them into a unified Job registry. This skill enables understanding and auditing of all source-to-target conversion routes available across multiple external chemical metadata services.

## When to use

When you need to understand which chemical identifier conversions are available in MSMetaEnhancer (e.g., which services can convert from InChI to SMILES, or from CAS number to formula), audit the completeness of converter implementations, validate that all discovered converters have corresponding async/sync methods, or generate a manifest of supported conversion jobs for documentation or job scheduling.

## When NOT to use

- You only need to invoke a single, pre-known converter (e.g., 'convert using CTS InChI→SMILES'). Use direct converter instantiation instead.
- The MSMetaEnhancer installation is incomplete or the converters/ directory structure is missing or corrupted.
- You need to discover converters from a remote registry or plugin system outside the local MSMetaEnhancer/libs/converters/ paths.

## Inputs

- MSMetaEnhancer/libs/converters/web/ directory containing WebConverter subclass definitions
- MSMetaEnhancer/libs/converters/compute/ directory containing ComputeConverter subclass definitions
- Converter __init__ method definitions specifying conversions list
- ConverterBuilder module instance

## Outputs

- Job registry: aggregated list of (source_attribute, target_attribute, converter_name) tuples
- Job manifest: structured file (e.g., JSON or CSV) listing all available conversions with validation status
- Converter instance map: mapping of converter name to instantiated converter with validated methods

## How to apply

Load the ConverterBuilder module, which auto-discovers all converter classes from MSMetaEnhancer/libs/converters/web/ (CIR, CTS, IDSM, PubChem, BridgeDb) and MSMetaEnhancer/libs/converters/compute/ (RDKit, custom converters) directories. For each discovered converter, extract the conversions list defined in its __init__ method as (source_attribute, target_attribute, conversion_method_name) tuples. Invoke create_top_level_conversion_methods() on each converter to trigger dynamic method generation. Aggregate all Job tuples across web and compute converters into a unified Job registry where each Job is a (source_attr, target_attr, converter_name) triple. Validate that each Job's conversion_method exists as an async method (WebConverters) or sync method (ComputeConverters) on the corresponding converter instance. Serialize and output the complete Job manifest as a structured file listing all available conversions.

## Related tools

- **MSMetaEnhancer** (Provides the ConverterBuilder module and the web/compute converter directories that are traversed to discover and enumerate all available conversion Jobs) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web converter service for chemical structure transformations (e.g., InChI → SMILES)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web converter service for chemical identifier conversions) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Web converter service providing chemical metadata and identifier mappings) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Web converter service for chemical structure and identifier conversions) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Web converter service for chemical identifier bridging and cross-referencing) — https://bridgedb.github.io/
- **RDKit** (Compute converter for local chemical structure transformations (reference implementation for custom converters))
- **Python** (Programming language in which MSMetaEnhancer and all converters are implemented)

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
job_registry = ConverterBuilder.get_all_jobs()
for job in job_registry:
    print(f"Job: {job['source']} → {job['target']} via {job['converter']}")
```

## Evaluation signals

- Job registry contains entries from all expected converter sources (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit)
- Each Job tuple has valid source_attribute, target_attribute, and converter_name fields matching converter class definitions
- For each Job, the corresponding converter instance has a callable method matching conversion_method_name with correct signature (async for web, sync for compute)
- Job manifest file is serializable and parseable (valid JSON/CSV structure with complete field coverage)
- No duplicate or conflicting Job entries exist in the registry; each (source_attr, target_attr, converter_name) triple appears exactly once

## Limitations

- Discovery relies on strict directory structure (MSMetaEnhancer/libs/converters/web/ and /compute/). Custom converters not in these paths will not be auto-discovered unless manually registered.
- Converter classes must follow the expected interface (inherit from WebConverter or ComputeConverter, define __init__ with conversions list, implement create_top_level_conversion_methods()). Non-compliant or deprecated converters may fail validation or cause registry errors.
- Dynamic method generation via create_top_level_conversion_methods() assumes a specific naming convention and method signature. Converters with non-standard method names or signatures will fail validation.
- Web converters depend on external service availability. API outages, rate limiting, or authentication failures during traversal may prevent full Job enumeration.

## Evidence

- [other] Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/ directories.: "Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/"
- [other] For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute, target_attribute, conversion_method_name).: "For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute,"
- [other] Aggregate all discovered Job tuples across web and compute converters into a unified Job registry, where each Job represents one (source_attr, target_attr, converter_name) triple.: "Aggregate all discovered Job tuples across web and compute converters into a unified Job registry, where each Job represents one (source_attr, target_attr, converter_name) triple."
- [other] Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance.: "Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance."
- [other] MSMetaEnhancer fetches chemical metadata including SMILES, InChI, and CAS number from five external services: CIR, CTS, PubChem, IDSM, and BridgeDb, enabling multiple source-to-target conversion routes for chemical identifier annotation.: "MSMetaEnhancer fetches chemical metadata including SMILES, InChI, and CAS number from five external services: CIR, CTS, PubChem, IDSM, and BridgeDb, enabling multiple source-to-target conversion"
- [readme] ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]): "ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])"
