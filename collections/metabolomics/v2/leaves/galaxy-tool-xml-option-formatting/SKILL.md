---
name: galaxy-tool-xml-option-formatting
description: Use when when integrating a multi-backend metadata enrichment package
  (like MSMetaEnhancer) into Galaxy, and you need to expose all supported conversion
  options—such as SMILES, InChI, or CAS number conversions across multiple web services
  (CIR, CTS, PubChem, IDSM, BridgeDb) and compute backends.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3071
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
  - Galaxy
  license_tier: open
  provenance_tier: literature
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

# galaxy-tool-xml-option-formatting

## Summary

Format metadata conversion options discovered from a converter registry into a JSON-serializable structure suitable for dynamic population of Galaxy tool form dropdowns. This skill bridges abstract converter configurations to Galaxy's XML parameter schema by enumerating all available source-to-target conversion paths and their methods.

## When to use

When integrating a multi-backend metadata enrichment package (like MSMetaEnhancer) into Galaxy, and you need to expose all supported conversion options—such as SMILES, InChI, or CAS number conversions across multiple web services (CIR, CTS, PubChem, IDSM, BridgeDb) and compute backends (RDKit)—as user-selectable dropdown options in a Galaxy tool form.

## When NOT to use

- The conversion options are already static and hardcoded into the Galaxy tool XML; use this skill only when you need to auto-discover and dynamically expose converter options.
- Your converters do not expose a conversions list attribute or follow a different metadata schema; this skill assumes the converter registry follows the ConverterBuilder pattern.
- The Galaxy tool does not support dynamic option generation and requires pre-compiled, static parameter choices.

## Inputs

- ConverterBuilder instance (registry of registered web and compute converters)
- Converter instances (e.g. CTS, CIR, IDSM, PubChem, BridgeDb, RDKit) with populated conversions list attribute

## Outputs

- JSON-serializable dictionary keyed by source attribute name with values as lists of target conversion options
- Galaxy-compatible option structure (nested dict or flat list suitable for XML/form population)

## How to apply

Instantiate a ConverterBuilder and iterate through all registered converter instances (web and compute converters) to extract their conversions list, which contains tuples of (source_attribute, target_attribute, conversion_method). For each conversion tuple, construct a Galaxy option entry with source and target attribute names as human-readable labels and a unique identifier formatted as 'converter_name:conversion_method' to disambiguate identical conversions from different backends. Aggregate all options into a single dictionary keyed by source attribute name, with values as lists of available target conversions. Return the result as a JSON-serializable dictionary that can be programmatically injected into Galaxy tool XML or used to populate dynamic form controls. The rationale is that Galaxy requires all form options to be enumerable at tool load time; by materializing the converter registry into a flat option structure, you enable users to select which conversion service to use without hardcoding service names into tool parameters.

## Related tools

- **MSMetaEnhancer** (The parent package providing the converter registry and conversion definitions that are enumerated by this skill.) — https://github.com/RECETOX/MSMetaEnhancer
- **ConverterBuilder** (Registry class that discovers and instantiates all available web (CIR, CTS, IDSM, PubChem, BridgeDb) and compute (RDKit) converters; iteration over registered instances extracts conversion tuples.) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web converter providing chemical structure conversions; contributes options to the enumerated dictionary.) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web converter providing chemical structure and identifier conversions; contributes options to the enumerated dictionary.) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Web converter providing metadata conversions from chemical names and identifiers; contributes options to the enumerated dictionary.) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Web converter providing chemical structure and property conversions; contributes options to the enumerated dictionary.) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Web converter providing chemical identifier conversions; contributes options to the enumerated dictionary.) — https://bridgedb.github.io/
- **RDKit** (Compute converter providing local, non-web-dependent chemical structure transformations; contributes options to the enumerated dictionary.)
- **Galaxy** (Workflow management system that consumes the formatted options structure to dynamically populate tool form parameter dropdowns.)

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder; from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb; from MSMetaEnhancer.libs.converters.compute import RDKit; ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit]); options = generate_options()
```

## Evaluation signals

- The returned dictionary is JSON-serializable (no non-standard Python objects); can be written to a file and re-parsed without error.
- Every source attribute name (keys) matches an attribute present in at least one converter's conversions list.
- Every target conversion option in the dictionary is traceable back to a conversion tuple from a registered converter, with the format 'converter_name:conversion_method' appearing in the option identifier.
- No duplicate options appear for the same source-to-target pair (aggregation de-duplication works correctly).
- All converter instances registered with ConverterBuilder are represented in the output; iterating over registered converters and checking their conversions list is exhaustive.

## Limitations

- The skill assumes all converters follow the ConverterBuilder registration pattern and expose a conversions list attribute; converters with non-standard interfaces will not contribute options.
- Web service converters (CIR, CTS, IDSM, PubChem, BridgeDb) are only enumerated; their availability or current API status is not checked at option generation time—options may become invalid if a service is down or changes its API.
- Rate limiting and API error handling are not part of this skill; they are deferred to the converter's own implementation and are not validated during option formatting.
- If multiple converters offer the same source-to-target conversion, the returned structure aggregates them into a single list; disambiguation relies on the 'converter_name:conversion_method' identifier being unique and correctly parsed by downstream Galaxy logic.

## Evidence

- [other] MSMetaEnhancer fetches metadata (SMILES, InChI, CAS number) from multiple services: CIR, CTS, PubChem, IDSM, and BridgeDb: "finding: MSMetaEnhancer fetches metadata (SMILES, InChI, CAS number) from multiple services: CIR, CTS, PubChem, IDSM, and BridgeDb, which represent the conversion options that `generate_options()`"
- [other] Iterate through each converter instance and extract the conversions list attribute, which contains tuples of (source_attribute, target_attribute, conversion_method).: "workflow: 2. Iterate through each converter instance and extract the conversions list attribute, which contains tuples of (source_attribute, target_attribute, conversion_method)."
- [other] For each conversion tuple, construct a Galaxy option entry with source and target attribute names as labels and a unique identifier formatted as 'converter_name:conversion_method'.: "workflow: 3. For each conversion tuple, construct a Galaxy option entry with source and target attribute names as labels and a unique identifier formatted as 'converter_name:conversion_method'."
- [other] Aggregate all converter options into a single dictionary keyed by source attribute name, with values as lists of available target conversions.: "workflow: 4. Aggregate all converter options into a single dictionary keyed by source attribute name, with values as lists of available target conversions."
- [other] Return the formatted options structure as a JSON-serializable dictionary suitable for dynamic population of Galaxy tool form dropdowns.: "workflow: 5. Return the formatted options structure as a JSON-serializable dictionary suitable for dynamic population of Galaxy tool form dropdowns."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation), [CTS](https://cts.fiehnlab.ucdavis.edu/), [PubChem](https://pubchem.ncbi.nlm.nih.gov/), [IDSM](https://idsm.elixir-czech.cz/), and [BridgeDb](https://bridgedb.github.io/).: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](...), [CTS](...), [PubChem](...), [IDSM](...), and [BridgeDb](...)."
