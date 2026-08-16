---
name: multi-service-integration-testing
description: Use when when building or modifying an asynchronous annotation pipeline
  that dispatches metadata enrichment requests to multiple heterogeneous web services
  and must verify that each service's HTTP calls succeed, response parsing is correct,
  and enriched fields are correctly merged into the output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MSMetaEnhancer
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - pytest
  - RDKit
  license_tier: open
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
- 'fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb'
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

# multi-service-integration-testing

## Summary

Validate that an asynchronous metadata enrichment pipeline correctly queries multiple external web services (CIR, CTS, PubChem, IDSM, BridgeDb), parses their responses, and aggregates enriched metadata back into mass spectra records. This skill ensures that service-specific converters handle API communication, response parsing, and data fusion without breaking existing functionality.

## When to use

When building or modifying an asynchronous annotation pipeline that dispatches metadata enrichment requests to multiple heterogeneous web services and must verify that each service's HTTP calls succeed, response parsing is correct, and enriched fields are correctly merged into the output spectra records without data loss or corruption.

## When NOT to use

- Input spectra file is already fully annotated with all target metadata fields (no enrichment needed)
- Only local, in-process metadata transformations are required (no web service calls needed)
- Testing a single converter in isolation without integration with the asynchronous dispatch loop

## Inputs

- .msp spectra file (sample with known compound names/identifiers)
- conversion job specifications (source attribute, target attribute, converter service)
- list of web services (CIR, CTS, PubChem, IDSM, BridgeDb)
- mock or live API responses from each service

## Outputs

- annotated .msp file with enriched metadata (SMILES, InChI, CAS, formula, InChIKey, IUPAC name)
- test report confirming all service queries succeeded
- verification that parsed metadata matches expected schema and types
- pytest output showing no regressions in existing tests

## How to apply

Set up a test suite that (1) loads a sample .msp spectra file with known compound names or identifiers; (2) configures conversion jobs specifying source attributes (e.g., compound name), target attributes (e.g., SMILES, InChI, CAS), and converter services; (3) invokes the asynchronous `annotate_spectra` method to dispatch requests to each web service; (4) for each job, verifies that the WebConverter base class correctly calls `query_the_service` to make HTTP requests to the target API endpoint; (5) validates that service-specific `parse_response` methods extract and return the expected metadata fields; (6) confirms that enriched metadata is aggregated back into the spectra records with no field omission or type mismatch; (7) runs the full test suite with pytest to ensure no regressions in existing converter functionality. Use RDKit as a reference implementation for local converters to validate the pattern.

## Related tools

- **MSMetaEnhancer** (Core framework providing Application class, asynchronous annotation pipeline, and WebConverter base class for service integration) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Chemical Identifier Resolver web service queried for SMILES and InChI conversion) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Chemical Translation Service web service queried for formula, InChI, and SMILES conversion) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (PubChem web service queried for canonical and isomeric SMILES, CAS, and metadata) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (IDSM web service queried for InChI, formula, InChIKey, and IUPAC name conversion) — https://idsm.elixir-czech.cz/
- **BridgeDb** (BridgeDb web service queried for cross-database identifier mapping) — https://bridgedb.github.io/
- **pytest** (Test framework used to validate existing converter functionality and prevent regressions)
- **RDKit** (Reference implementation for local converters to validate asynchronous dispatch pattern)

## Examples

```
asyncio.run(app.annotate_spectra(['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb'], [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'inchikey', 'IDSM')]))
```

## Evaluation signals

- All conversion jobs complete without timeout or HTTP errors; each service returns a non-null response
- Parsed metadata fields (SMILES, InChI, CAS, formula, InChIKey, IUPAC name) match the schema and data types expected by the .msp format
- Enriched metadata is correctly merged back into the spectra records; no fields are lost or overwritten incorrectly
- pytest run passes all existing tests; no regressions introduced in other converters or the core annotation pipeline
- Output .msp file is valid, readable, and contains all enriched metadata fields with non-empty values where services returned results

## Limitations

- External web services (CIR, CTS, PubChem, IDSM, BridgeDb) may have rate limits, downtime, or API changes that break parsing; integration tests may fail transiently without code changes
- Service-specific `parse_response` methods may fail on unexpected API response structures or error messages; test coverage must account for documented service behavior variations
- Asynchronous implementation introduces complexity in test setup and teardown (event loop management); mock services or recorded responses may not capture all real-world failure modes
- Input compound names may be ambiguous or unresolved by multiple services, leading to partial enrichment; tests must validate graceful handling of missing or null metadata

## Evidence

- [other] MSMetaEnhancer enriches .msp files by adding SMILES, InChI, and CAS number metadata retrieved from five external services: "MSMetaEnhancer enriches .msp files by adding SMILES, InChI, and CAS number metadata retrieved from five external services: CIR, CTS, PubChem, IDSM, and BridgeDb."
- [other] The asynchronous annotation method dispatches requests to web services via WebConverter base class: "Invoke the asynchronous `annotate_spectra` method with the defined jobs to dispatch metadata enrichment requests to web services. For each job, the WebConverter base class calls `query_the_service`"
- [other] Service-specific methods extract and parse metadata fields from API responses: "Parse API responses using service-specific `parse_response` methods to extract SMILES, InChI, CAS and other metadata fields."
- [readme] The app uses asynchronous implementation allowing for optimal fetching speed: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
- [other] RDKit converter serves as reference implementation for extending the annotation pipeline: "Use the RDKit converter as a reference implementation"
- [other] Existing tests must pass when modifications are made to converters or the annotation pipeline: "make sure the existing tests still work by running ``pytest``"
