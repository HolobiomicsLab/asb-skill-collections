---
name: conversion-graph-construction
description: Use when when integrating MSMetaEnhancer into Galaxy or another workflow platform and you need to dynamically populate conversion option menus without hardcoding service-specific logic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3429
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_0091
  tools:
  - MSMetaEnhancer
  - ConverterBuilder
  - Python
  - pytest
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - RDKit
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

# conversion-graph-construction

## Summary

Build a directed graph of available metadata conversion pathways across multiple external services (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit) to enable dynamic enumeration and routing of chemical metadata transformations. This skill ensures that Galaxy tool forms and downstream annotation workflows can discover and display all feasible source→target attribute conversions supported by registered converters.

## When to use

When integrating MSMetaEnhancer into Galaxy or another workflow platform and you need to dynamically populate conversion option menus without hardcoding service-specific logic. Apply this skill when you have multiple heterogeneous metadata conversion services registered and must expose all supported transformations (e.g., SMILES↔InChI, InChI→formula, name→CAS number) to end users or downstream orchestration logic.

## When NOT to use

- When converters are fixed or hardcoded into the application; use static configuration instead.
- When you only need to support a single converter; a simple lookup table is simpler.
- When metadata attributes are already pre-computed in the input .msp file and no new conversions are required.

## Inputs

- list of registered Converter subclass instances (web and compute converters)
- Converter.conversions attribute (list of (source, target, method) tuples per converter)

## Outputs

- conversion graph (dictionary keyed by source attribute → list of {target, converter_id} dicts)
- JSON-serializable options structure for Galaxy tool form population

## How to apply

Instantiate the ConverterBuilder to discover all registered converter instances (both web services and compute converters like RDKit). Iterate through each converter and extract its `conversions` list attribute, which contains tuples of (source_attribute, target_attribute, conversion_method). For each tuple, construct a node pair and directed edge labeled with the converter name and method identifier. Aggregate edges into a dictionary keyed by source attribute name, grouping all reachable target attributes and their corresponding converter identifiers (formatted as 'converter_name:conversion_method'). Validate that the graph is non-empty and that all source/target pairs reference valid metadata fields defined in the MSMetaEnhancer schema. Return the graph as a JSON-serializable dictionary suitable for dynamic population of Galaxy tool form dropdowns and for query-time conversion routing.

## Related tools

- **ConverterBuilder** (discover and instantiate all registered web and compute converters to populate the conversion graph) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (web service providing chemical structure conversions (e.g., InChI→SMILES)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (web service providing chemical metadata transformations) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (web service providing chemical property and structure conversions) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (web service providing InChI-based metadata conversions (formula, InChIKey, IUPAC name)) — https://idsm.elixir-czech.cz/
- **BridgeDb** (web service providing cross-database identifier and structure conversions) — https://bridgedb.github.io/
- **RDKit** (compute converter providing local SMILES↔InChI and structure-derived property conversions) — https://github.com/RECETOX/MSMetaEnhancer
- **MSMetaEnhancer** (parent package integrating all converters and orchestrating annotation) — https://github.com/RECETOX/MSMetaEnhancer

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit

ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
converters = ConverterBuilder.get_converters()
options = {}
for converter in converters:
    for src, tgt, method in converter.conversions:
        if src not in options:
            options[src] = []
        options[src].append({'target': tgt, 'converter_id': f'{converter.__class__.__name__}:{method}'})
```

## Evaluation signals

- All registered converters appear as nodes in the graph with no missing or duplicate entries.
- Each (source_attribute, target_attribute, converter_name:method) edge is present and bidirectionality (if supported by the converter) is correctly represented.
- The JSON serialization contains no cycles or orphaned nodes; all source and target attributes reference valid MSMetaEnhancer metadata field names.
- Galaxy tool form population using the graph produces dropdown menus with no null, malformed, or unreachable conversion options.
- A query for conversions from any populated source attribute returns at least one reachable target and a valid converter identifier formatted as 'converter_name:method'.

## Limitations

- Graph construction depends on ConverterBuilder registration; converters not registered will not appear in the graph.
- Web service converters (CIR, CTS, PubChem, IDSM, BridgeDb) may fail or return incomplete `conversions` lists if their APIs are unavailable or have changed; no fallback is provided during graph construction.
- The conversion graph is static after instantiation; runtime addition or removal of converters requires re-instantiation.
- No built-in cycle detection or path optimization; if multiple converters provide overlapping conversions, the graph may become ambiguous (resolved only at annotation time by job specification).
- Graph assumes all converters implement the `conversions` attribute consistently; non-compliant or custom converters may cause AttributeError.

## Evidence

- [other] MSMetaEnhancer fetches metadata (SMILES, InChI, CAS number) from multiple services: CIR, CTS, PubChem, IDSM, and BridgeDb, which represent the conversion options that `generate_options()` must enumerate for Galaxy tool integration.: "Instantiate the ConverterBuilder to discover all available web converters (CIR, CTS, IDSM, PubChem, BridgeDb) and compute converters (RDKit) registered in the package."
- [other] Iterate through each converter instance and extract the conversions list attribute, which contains tuples of (source_attribute, target_attribute, conversion_method).: "Iterate through each converter instance and extract the conversions list attribute, which contains tuples of (source_attribute, target_attribute, conversion_method)."
- [other] For each conversion tuple, construct a Galaxy option entry with source and target attribute names as labels and a unique identifier formatted as 'converter_name:conversion_method'.: "For each conversion tuple, construct a Galaxy option entry with source and target attribute names as labels and a unique identifier formatted as 'converter_name:conversion_method'."
- [other] Aggregate all converter options into a single dictionary keyed by source attribute name, with values as lists of available target conversions.: "Aggregate all converter options into a single dictionary keyed by source attribute name, with values as lists of available target conversions."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation), [CTS](https://cts.fiehnlab.ucdavis.edu/), [PubChem](https://pubchem.ncbi.nlm.nih.gov/), [IDSM](https://idsm.elixir-czech.cz/), and [BridgeDb](https://bridgedb.github.io/).: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](...), [CTS](...), [PubChem](...), [IDSM](...), and [BridgeDb](...)."
- [readme] ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]): "ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])"
