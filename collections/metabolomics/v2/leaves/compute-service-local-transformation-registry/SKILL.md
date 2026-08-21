---
name: compute-service-local-transformation-registry
description: 'Use when initializing a chemical metadata annotation pipeline and you
  need to: (1) establish which identifier conversions are available across your installed
  converter suite (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit, custom); (2) validate
  that each conversion route can actually be invoked;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3500
  edam_topics:
  - http://edamontology.org/topic_3172
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
  license_tier: open
  provenance_tier: literature
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

# Compute Service Local Transformation Registry

## Summary

Automatically discover, enumerate, and register all available chemical identifier conversion jobs across local compute and web service converters, then validate and serialize them into a unified Job manifest. This skill ensures that all source-to-target transformation routes (e.g., SMILES→InChI, name→CAS) are discoverable and callable at runtime.

## When to use

Apply this skill when initializing a chemical metadata annotation pipeline and you need to: (1) establish which identifier conversions are available across your installed converter suite (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit, custom); (2) validate that each conversion route can actually be invoked; (3) present users with a menu of supported transformations; or (4) route annotation requests to the correct converter and method.

## When NOT to use

- When converters are already manually registered or hard-coded into the application — use registry discovery only when converters are plugin-based or directory-scanned.
- When you only need to perform a single, pre-known conversion route — job discovery overhead is unnecessary for one-off transformations.
- When converter availability changes frequently at runtime and you require real-time method introspection — this skill assumes stable, pre-launch discovery.

## Inputs

- Converter class modules (web and compute) with __init__ definitions of conversions list
- MSMetaEnhancer directory structure (MSMetaEnhancer/libs/converters/web/, compute/)
- Chemical identifier attribute names (e.g., 'name', 'inchi', 'smiles', 'cas_number')

## Outputs

- Unified Job registry (in-memory data structure)
- Serialized Job manifest file (JSON/structured format listing all conversions)
- Validated converter instance pool with dynamically generated conversion methods

## How to apply

Load the ConverterBuilder module and call its auto-discovery mechanism to introspect all converter classes in MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/ directories. For each discovered converter, extract its `conversions` list (defined in `__init__`) as tuples of (source_attribute, target_attribute, conversion_method_name). Invoke `create_top_level_conversion_methods()` on each converter to trigger dynamic method generation. Aggregate all tuples into a unified Job registry, where each Job is a (source_attr, target_attr, converter_name) triple. Validate that each Job's conversion method exists and is callable (async for WebConverters, sync for ComputeConverters). Finally, serialize the complete Job manifest to a structured file (JSON or similar) listing all available conversions for downstream annotation workflows.

## Related tools

- **ConverterBuilder** (Auto-discovers, instantiates, and aggregates all converter classes and their conversion methods into a unified Job registry) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web service converter providing chemical structure identifier conversions (e.g., InChI↔SMILES)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web service converter for chemical identifier transformations) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Web service converter fetching chemical metadata including SMILES, InChI, and CAS number) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Web service converter for chemical structure queries and identifier lookups) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Web service converter for identifier mapping and cross-referencing) — https://bridgedb.github.io/
- **RDKit** (Compute converter for local chemical descriptor and structure transformation (no external API calls)) — https://github.com/RECETOX/MSMetaEnhancer

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit

ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
job_registry = ConverterBuilder.build_job_registry()
```

## Evaluation signals

- All converter classes from web/ and compute/ directories are discovered and instantiated without import errors.
- Each discovered converter's conversions list is non-empty and contains valid (source_attr, target_attr, method_name) tuples.
- Every Job in the registry has a corresponding callable method on its converter instance (verify method exists via hasattr and inspect.iscoroutinefunction for async/sync mismatch).
- The serialized Job manifest is valid JSON/structured format, contains ≥6 distinct converters (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit), and includes at least one job per converter.
- Validation logic detects and reports broken jobs (missing methods, mismatched async/sync signatures) without crashing the registry build.

## Limitations

- If converters are installed as optional dependencies (e.g., RDKit via conda), missing packages will silently skip those converters unless explicitly declared as required.
- API rate limits on web service converters (CIR, CTS, PubChem, IDSM, BridgeDb) are not captured in the Job registry itself; rate limiting is enforced at call time, not discovery time.
- The registry reflects the converters' hardcoded conversions lists at initialization; new conversion routes added to a converter after Application startup will not appear in the registry without re-initialization.
- Cross-converter dependency chains (e.g., 'name→inchi via IDSM, then inchi→formula via RDKit') are not automatically discovered; only direct single-converter routes are enumerated.

## Evidence

- [other] 1. Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/ directories.: "Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/"
- [other] 2. For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute, target_attribute, conversion_method_name).: "For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples"
- [other] 3. Invoke the create_top_level_conversion_methods() call on each converter to trigger dynamic method generation based on the conversions list.: "Invoke the create_top_level_conversion_methods() call on each converter to trigger dynamic method generation based on the conversions list."
- [other] 4. Aggregate all discovered Job tuples across web and compute converters into a unified Job registry, where each Job represents one (source_attr, target_attr, converter_name) triple.: "Aggregate all discovered Job tuples across web and compute converters into a unified Job registry, where each Job represents one (source_attr, target_attr, converter_name) triple."
- [other] 5. Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance.: "Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance."
- [other] MSMetaEnhancer fetches chemical metadata including SMILES, InChI, and CAS number from five external services: CIR, CTS, PubChem, IDSM, and BridgeDb: "MSMetaEnhancer fetches chemical metadata including SMILES, InChI, and CAS number from five external services: CIR, CTS, PubChem, IDSM, and BridgeDb"
- [readme] ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]): "ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])"
- [readme] specify requested jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ...]: "jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'inchikey', 'IDSM')"
