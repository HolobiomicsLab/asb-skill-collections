---
name: api-error-handling-and-rate-limiting
description: Use when when enriching mass spectra metadata by querying multiple external web services (CIR, CTS, PubChem, IDSM, BridgeDb) asynchronously, and you need to avoid API rate-limit violations, gracefully skip missing or malformed responses, and maintain pipeline stability without losing partial.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3761
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MSMetaEnhancer
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - RDKit
  - Python
  - pytest
  - aiohttp
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- '**MSMetaEnhancer** is a tool used for `.msp` files annotation'
- '`MSMetaEnhancer/libs/converters/web/` named after your service'
- 'fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation)'
- __all__ = ['IDSM', 'CTS', 'CIR', 'PubChem', 'BridgeDb', 'MyService']
- '[CTS](https://cts.fiehnlab.ucdavis.edu/)'
- '[PubChem](https://pubchem.ncbi.nlm.nih.gov/)'
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

# API Error Handling and Rate Limiting

## Summary

Apply graceful error handling and throttling mechanisms when making asynchronous calls to external web APIs during metadata enrichment. This skill ensures robust, compliant integration with multiple chemical structure databases that have varying API limits and response formats.

## When to use

When enriching mass spectra metadata by querying multiple external web services (CIR, CTS, PubChem, IDSM, BridgeDb) asynchronously, and you need to avoid API rate-limit violations, gracefully skip missing or malformed responses, and maintain pipeline stability without losing partial results from successful queries.

## When NOT to use

- Input APIs are fully documented with guaranteed 100% uptime and zero rate limits—error handling adds unnecessary overhead.
- Spectrum records require real-time single-request completion; asynchronous batching and throttling would cause unacceptable latency.
- All required metadata is already present in the input .msp file and no external API calls are needed.

## Inputs

- Job tuples (source_attribute, target_attribute, converter_name) specifying conversion requests
- Converter registry initialized with web and compute converters (CIR, CTS, PubChem, IDSM, BridgeDb, RDKit)
- Spectrum records with initial identifiers (compound name, mass) from parsed .msp file

## Outputs

- Enriched spectrum records with merged metadata from successful API responses
- Error log or validation report indicating which conversions failed and why
- Response dictionaries (one per converter) merged gracefully into spectrum metadata

## How to apply

Initialize a Throttler rate-limiting mechanism within the Converter dispatcher to enforce per-service API rate limits before each request is invoked. Wrap each converter's asynchronous method call in error handling that catches network failures, timeouts, and malformed responses, returning empty dictionaries instead of raising exceptions. Parse response objects defensively, validating presence and type of expected fields before merging into the spectrum record. Apply exponential backoff or request queuing if an API returns 429/rate-limit status codes. Log all skipped or degraded conversions so users can audit which metadata transformations succeeded or failed for each spectrum.

## Related tools

- **MSMetaEnhancer** (Orchestrator of asynchronous annotation pipeline with Converter dispatcher and Throttler) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web API converter for chemical structure lookups; subject to rate limits) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web API converter for chemical identifier translation; subject to rate limits) — https://cts.fiehnlab.ucdavis.edu/
- **PubChem** (Web API converter for metadata retrieval (SMILES, InChI, CAS); subject to rate limits) — https://pubchem.ncbi.nlm.nih.gov/
- **IDSM** (Web API converter for InChI and formula resolution; subject to rate limits) — https://idsm.elixir-czech.cz/
- **BridgeDb** (Web API converter for identifier cross-linking; subject to rate limits) — https://bridgedb.github.io/
- **aiohttp** (Asynchronous HTTP session manager for concurrent requests)
- **pytest** (Test framework for validating error handling and throttling behavior)

## Examples

```
asyncio.run(app.annotate_spectra(services=['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb'], jobs=[('name', 'inchi', 'IDSM'), ('inchi', 'canonical_smiles', 'IDSM')]))
```

## Evaluation signals

- All 429 (rate-limit) responses are caught and queued for retry without raising unhandled exceptions.
- Malformed or missing response fields do not cause pipeline crashes; empty dictionaries are returned and logged.
- Spectrum records retain all original metadata fields when API calls fail; enrichment is purely additive or absent, never destructive.
- Request rate per converter does not exceed documented API limits; throttling delays are visible in execution logs.
- Error logs contain entries for every failed conversion attempt, including converter name, spectrum ID, and reason (timeout, 4xx, 5xx, parse error).

## Limitations

- Error handling cannot distinguish between transient network failures and permanent API unavailability; users must configure retry policies manually.
- Rate-limit headers vary across services (X-RateLimit-Remaining, X-RateLimit-Reset); throttling may not respect undocumented per-user quotas.
- Graceful degradation means some spectra may have incomplete metadata; users must validate output .msp files post-enrichment to identify gaps.
- Asynchronous error handling does not guarantee all jobs complete within a timeout; long-running jobs may consume memory without logging progress.

## Evidence

- [other] Always handle API errors gracefully and return empty dictionaries when data is not available: "Always handle API errors gracefully and return empty dictionaries when data is not available"
- [other] Respect API rate limits using throttling mechanisms: "Respect API rate limits using throttling mechanisms"
- [other] Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses.: "Parse and merge response dictionaries from each converter into the spectrum record, applying error handling to gracefully skip missing or malformed responses."
- [other] Execute all jobs asynchronously using the Converter dispatcher, which dynamically invokes the matched converter's method and applies Throttler rate-limiting to respect API limits.: "Execute all jobs asynchronously using the Converter dispatcher, which dynamically invokes the matched converter's method and applies Throttler rate-limiting to respect API limits."
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
