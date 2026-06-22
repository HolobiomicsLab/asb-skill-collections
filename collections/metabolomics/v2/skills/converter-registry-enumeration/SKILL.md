---
name: converter-registry-enumeration
description: Use when you need to expose all supported metadata conversion options in a tool interface (e.g., Galaxy tool form, CLI argument parser, or API endpoint) and want to avoid hard-coding conversion paths.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2275
  tools:
  - MSMetaEnhancer
  - ConverterBuilder
  - Python
  - pytest
  - Galaxy
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- '**MSMetaEnhancer** is a tool used for `.msp` files annotation'
- '`MSMetaEnhancer/libs/converters/web/` named after your service'
- 'Converter Builder: Automatically discovers and instantiates available converters'
- 'MSMetaEnhancer: A Python package for mass spectra metadata annotation'
- Create a new Python file in `MSMetaEnhancer/libs/converters/web/`
- make sure the existing tests still work by running ``pytest``
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

# converter-registry-enumeration

## Summary

Enumerate all available metadata conversion pathways (source→target attribute pairs) from a multi-service converter registry to dynamically populate tool interface options. This skill discovers which chemical identifier conversions (SMILES, InChI, CAS number, formula, etc.) are supported across all registered converters (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) and formats them for programmatic consumption by downstream applications like Galaxy workflow tools.

## When to use

You need to expose all supported metadata conversion options in a tool interface (e.g., Galaxy tool form, CLI argument parser, or API endpoint) and want to avoid hard-coding conversion paths. This skill is essential when: (1) multiple conversion services are available but you need a unified option menu, (2) converters may be added or removed at runtime and the interface must remain current, or (3) you are building a Galaxy tool that must dynamically populate dropdowns with 'source attribute → target attribute' pairs keyed by converter name and method.

## When NOT to use

- You need to execute actual conversions (use the converter instances directly instead).
- You want to filter options based on user credentials, data provenance, or request rate limits (enumeration is static; filtering is a separate skill).
- Your input data already specifies a fixed, pre-determined set of allowed conversions (hard-coding is simpler and more maintainable than registry enumeration).

## Inputs

- ConverterBuilder instance (with registered converter classes)
- List of converter classes to instantiate (e.g., [CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])

## Outputs

- Dictionary keyed by source attribute name, with values as lists of {'label': 'target_attr', 'value': 'converter_name:conversion_method'} objects
- JSON-serializable options structure suitable for Galaxy tool form dynamic dropdowns

## How to apply

Instantiate the ConverterBuilder and invoke its registry to discover all registered converter classes (web: CIR, CTS, IDSM, PubChem, BridgeDb; compute: RDKit). Iterate through each converter instance and access its `conversions` list attribute, which contains tuples of (source_attribute, target_attribute, conversion_method). For each tuple, construct an option entry with the source and target attribute names as human-readable labels and a unique identifier formatted as 'converter_name:conversion_method'. Aggregate all options into a dictionary keyed by source attribute name, with values as lists of target conversions available for that source. Validate that all source and target attribute names are non-empty strings and that no duplicate 'converter_name:conversion_method' identifiers exist within a single source key. Return the aggregated structure as a JSON-serializable dictionary suitable for direct insertion into tool form schemas or option menus.

## Related tools

- **MSMetaEnhancer** (Python package providing the ConverterBuilder registry and converter classes (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit) whose conversions list attributes are enumerated) — https://github.com/RECETOX/MSMetaEnhancer
- **ConverterBuilder** (Central registry class that discovers and instantiates all available converter instances; its converters are iterated to extract conversion tuples) — https://github.com/RECETOX/MSMetaEnhancer
- **Galaxy** (Target tool interface for which the enumerated options are formatted as JSON-serializable option structures for dynamic dropdown population)
- **pytest** (Testing framework used to validate that enumeration logic correctly iterates converters and extracts conversion tuples without errors)

## Examples

```
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder

ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
options_dict = generate_options()  # returns {source_attr: [{label, value}, ...]}
```

## Evaluation signals

- All registered converters appear in the output dictionary (check that CIR, CTS, IDSM, PubChem, BridgeDb, and RDKit are represented by at least one 'converter_name:conversion_method' entry).
- No duplicate 'converter_name:conversion_method' identifiers exist within a single source attribute key.
- All source and target attribute names are non-empty strings and match the actual converter.conversions tuple structure (e.g., 'inchi', 'smiles', 'cas_number', 'formula', 'iupac_name').
- The returned dictionary is valid JSON-serializable (no circular references, non-string keys, or unserializable objects).
- When used to populate a Galaxy tool form, all source attribute dropdowns render without errors and each target conversion option is selectable and maps correctly to its 'converter_name:conversion_method' identifier.

## Limitations

- Enumeration reflects only converters registered at the time of instantiation; if converters are added dynamically after ConverterBuilder initialization, the enumeration will not include them without re-running the skill.
- The skill does not validate whether a given conversion will succeed at runtime (e.g., if an API service is down or rate-limited); it only reports that the conversion path exists in the registry.
- No filtering is applied based on API credentials, quota, or data provenance; all registered conversions are exposed regardless of whether a particular user or request has permission to use them.
- The conversions list attribute structure is assumed to be uniform across all converter classes; if a converter deviates from the (source_attribute, target_attribute, conversion_method) tuple format, extraction will fail or produce malformed entries.

## Evidence

- [other] How should the `generate_options()` function in the Galaxy submodule format all supported metadata conversion options for display in a Galaxy tool form?: "How should the `generate_options()` function in the Galaxy submodule format all supported metadata conversion options for display in a Galaxy tool form?"
- [other] MSMetaEnhancer fetches metadata (SMILES, InChI, CAS number) from multiple services: CIR, CTS, PubChem, IDSM, and BridgeDb, which represent the conversion options that `generate_options()` must enumerate for Galaxy tool integration.: "MSMetaEnhancer fetches metadata (SMILES, InChI, CAS number) from multiple services: CIR, CTS, PubChem, IDSM, and BridgeDb, which represent the conversion options"
- [other] Instantiate the ConverterBuilder to discover all available web converters (CIR, CTS, IDSM, PubChem, BridgeDb) and compute converters (RDKit) registered in the package.: "Instantiate the ConverterBuilder to discover all available web converters (CIR, CTS, IDSM, PubChem, BridgeDb) and compute converters (RDKit) registered in the package."
- [other] For each conversion tuple, construct a Galaxy option entry with source and target attribute names as labels and a unique identifier formatted as 'converter_name:conversion_method'.: "For each conversion tuple, construct a Galaxy option entry with source and target attribute names as labels and a unique identifier formatted as 'converter_name:conversion_method'."
- [other] Return the formatted options structure as a JSON-serializable dictionary suitable for dynamic population of Galaxy tool form dropdowns.: "Return the formatted options structure as a JSON-serializable dictionary suitable for dynamic population of Galaxy tool form dropdowns."
- [readme] ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]): "ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])"
